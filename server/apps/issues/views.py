# Imports
import logging
from typing import Any, Dict
from apps.apartments.models import Apartment
from apps.common.models import ContentView
from apps.common.renderers import GenericJSONRenderer
from apps.issues.emails import send_issue_confirmation_email, send_issue_resolved_email
from apps.issues.models import Issue
from apps.issues.serializers import IssueSerializer, IssueStatusUpdateSerializer
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


# Get the logger
logger = logging.getLogger(__name__)


class IsStaffOrSuperUser(permissions.BasePermission):
    """Custom permission class to check if the user is staff or superuser.

    Extends:
        permissions.BasePermission

    Attributes:
        message: str -- The error message to display.

    Methods:
        has_permission: Checks if the user is staff or superuser.

    Raises:
        PermissionDenied: If the user is not staff or superuser.
    """

    def __init__(self) -> None:
        self.message = None

    def has_permission(self, request: Request, view: Any) -> bool:
        """Check if the user is staff or superuser.

        Arguments:
            request: Request -- The request object.
            view: Any -- The view object.

        Returns:
            bool -- True if the user is staff or superuser, False otherwise.

        Raises:
            PermissionDenied: If the user is not staff or superuser.
        """

        is_authorized = (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )

        if not is_authorized:
            self.message = "Access to this information is restricted to staff and admin users only."

        return is_authorized


class IssueListAPIView(generics.ListAPIView):
    """Issue list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        permission_classes: List -- The list of permission classes.
        object_label: str -- The object label.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (IsStaffOrSuperUser,)
    object_label = "issues"


class AssignedIssuesListAPIView(generics.ListAPIView):
    """Assigned issues list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "assigned_issues"

    def get_queryset(self):
        """Method to get the queryset.

        This method returns the list of issues assigned to the user.

        Returns:
            QuerySet -- The queryset of issues.
        """

        return self.queryset.filter(assigned_to=self.request.user)


class MyIssuesListAPIView(generics.ListAPIView):
    """My issues list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "my_issues"

    def get_queryset(self):
        """Method to get the queryset.

        This method returns the list of issues reported by the user.

        Returns:
            QuerySet -- The queryset of issues.
        """

        return self.queryset.filter(reported_by=self.request.user)


class IssueCreateAPIView(generics.CreateAPIView):
    """Issue create view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        perform_create: Method to perform the create operation.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"

    def perform_create(self, serializer: IssueSerializer) -> None:
        """Method to perform the create operation.

        This method creates a new issue and sends a confirmation email.

        Arguments:
            serializer: IssueSerializer -- The issue serializer.

        Raises:
            ValidationError: If the apartment ID is not provided.
            PermissionDenied: If the user does not have permission to report issues for the apartment.
        """

        apartment_id = self.kwargs.get("apartment_id")

        if not apartment_id:
            raise ValidationError({"apartment_id": ["Apartment ID is required."]})

        try:
            apartment = Apartment.objects.get(id=apartment_id, tenant=self.request.user)

        except Apartment.DoesNotExist:
            raise PermissionDenied(
                "You do have the permission to report issues for this apartment."
            )

        issue = serializer.save(reported_by=self.request.user, apartment=apartment)

        send_issue_confirmation_email(issue)


class IssueDetailAPIView(generics.RetrieveAPIView):
    """Issue detail view class.

    Extends:
        generics.RetrieveAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
        lookup_field: str -- The lookup field.

    Methods:
        get_object: Method to get the issue object.
        record_issue_view: Method to record the issue view.
        get_client_ip: Method to get the client IP address.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"
    lookup_field = "id"

    def get_object(self) -> Issue:
        """Method to get the issue object.

        This method gets the issue object and records the issue view.

        Returns:
            Issue: The issue object.

        Raises:
            PermissionDenied: If the user does not have permission to view the issue.
        """

        issue = super().get_object()

        user = self.request.user

        if not (
            user == issue.reported_by or user.is_staff or user == issue.assigned_to
        ):
            raise PermissionDenied("You do not have permission to view this issue.")

        self.record_issue_view(issue)

        return issue

    def record_issue_view(self, issue: Issue) -> None:
        """Method to record the issue view.

        This method records the issue view by creating a new content view object.

        Arguments:
            issue: Issue -- The issue object.
        """

        content_type = ContentType.objects.get_for_model(issue)

        viewer_ip = self.get_client_ip()

        user = self.request.user

        obj, created = ContentView.objects.get_or_create(
            content_type=content_type,
            object_id=issue.pk,
            user=user,
            viewer_ip=viewer_ip,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    def get_client_ip(self) -> str:
        """Method to get the client IP address.

        This method gets the client IP address from the request object.

        Returns:
            str -- The client IP address.
        """

        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()

        else:
            ip = self.request.META.get("REMOTE_ADDR")

        return ip


class IssueUpdateAPIView(generics.UpdateAPIView):
    """Issue update view class.

    Extends:
        generics.UpdateAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        serializer_class: IssueSerializer -- The issue serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
        lookup_field: str -- The lookup field.

    Methods:
        get_object: Method to get the issue object.
    """

    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueStatusUpdateSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"

    def get_object(self) -> Issue:
        """Method to get the issue object.

        This method gets the issue object and checks if the user has permission to update the issue status.

        Returns:
            Issue -- The issue object.
        """

        issue = super().get_object()

        user = self.request.user

        if not (user.is_staff or user == issue.assigned_to):
            logger.warning(
                f"Unauthorized issue status update attempt by the user {user.full_name} on issue {issue.title}"
            )

            raise PermissionDenied("You do not have permission to update the issue")

        return issue


class IssueDeleteAPIView(generics.DestroyAPIView):
    """Issue delete view class.

    Extends:
        generics.DestroyAPIView

    Attributes:
        queryset: QuerySet -- The queryset of issues.
        lookup_field: str -- The lookup field.
        serializer_class: IssueSerializer -- The issue serializer class.

    Methods:
        get_object: Method to get the issue object.
        delete: Method to delete the issue.
    """

    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueSerializer

    def get_object(self) -> Issue:
        """Method to get the issue object.

        This method gets the issue object and checks if the user has permission to delete the issue.

        Returns:
            Issue -- The issue object.

        Raises:
            Http404: If the issue is not found.
            PermissionDenied: If the user does not have permission to delete the issue.
        """

        try:
            issue = super().get_object()

        except Http404:
            raise Http404("Issue not found")

        if not (self.request.user.is_staff or self.request.user == issue.reported_by):
            logger.warning(
                f"Unauthorized issue deletion attempt by {self.request.user} on issue {issue.title}"
            )

            raise PermissionDenied(
                "You do not have permission to delete this issue. Please contact the admin."
            )

        return issue

    def delete(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to delete the issue.

        This method deletes the issue and returns a response with status code 204.

        Arguments:
            request: Request -- The request object.
            args: dict -- The arguments.
            kwargs: dict -- The keyword arguments.

        Returns:
            Response -- The response object with status code 204.
        """

        super().delete(request, *args, **kwargs)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
