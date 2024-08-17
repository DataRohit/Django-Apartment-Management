# Imports
import logging
from typing import Any, Dict

from apps.apartments.models import Apartment
from apps.common.models import ContentView
from apps.common.renderers import GenericJSONRenderer
from apps.issues.emails import send_issue_confirmation_email
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


# Custom permission class to check if the user is staff or superuser
class IsStaffOrSuperUser(permissions.BasePermission):
    """Custom permission class to check if the user is staff or superuser.

    Extends:
        permissions.BasePermission

    Attributes:
        message (str): The message attribute.

    Methods:
        has_permission: Method to check if the user is staff or superuser.
    """

    # Attributes
    def __init__(self) -> None:
        self.message = None

    # Method to check if the user is staff or superuser
    def has_permission(self, request: Request, view: Any) -> bool:
        """Method to check if the user is staff or superuser.

        Args:
            request (Request): The request object.
            view (Any): The view object.

        Returns:
            bool: The boolean value.
        """

        # Check if the user is authorized
        is_authorized = (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )

        # If the user is not authorized
        if not is_authorized:
            # Set the message
            self.message = "Access to this information is restricted to staff and admin users only."

        # Return if the user is authorized
        return is_authorized


# IssueListAPIView Class
class IssueListAPIView(generics.ListAPIView):
    """IssueListAPIView

    IssueListAPIView class is used to list all the issues.

    Extends:
        generics.ListAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        renderer_classes (list): The list of renderer classes.
        permission_classes (list): The list of permission classes.
        object_label (str): The object label.
    """

    # Attributes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (IsStaffOrSuperUser,)
    object_label = "issues"


# AssignedIssuesListAPIView Class
class AssignedIssuesListAPIView(generics.ListAPIView):
    """AssignedIssuesListAPIView

    AssignedIssuesListAPIView class is used to list the issues assigned to the user.

    Extends:
        generics.ListAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset: Method to get the queryset of issues.
    """

    # Attributes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "assigned_issues"

    # Method to get the queryset of issues
    def get_queryset(self):
        """Method to get the queryset of issues.

        Returns:
            QuerySet: The queryset of issues assigned to the user.
        """

        # Return the queryset of issues assigned to the user
        return self.queryset.filter(assigned_to=self.request.user)


# MyIssuesListAPIView Class
class MyIssuesListAPIView(generics.ListAPIView):
    """MyIssuesListAPIView

    MyIssuesListAPIView class is used to list the issues reported by the user.

    Extends:
        generics.ListAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset: Method to get the queryset of issues.
    """

    # Attributes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "my_issues"

    # Method to get the queryset of issues
    def get_queryset(self):
        """Method to get the queryset of issues.

        Returns:
            QuerySet: The queryset of issues reported by the user.
        """

        # Return the queryset of issues reported by the user
        return self.queryset.filter(reported_by=self.request.user)


# IssueCreateAPIView Class
class IssueCreateAPIView(generics.CreateAPIView):
    """IssueCreateAPIView

    IssueCreateAPIView class is used to create an issue.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        perform_create: Method to create an issue.

    Raises:
        ValidationError: The validation error.
        PermissionDenied: The permission denied error.
    """

    # Attributes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"

    # Method to create an issue
    def perform_create(self, serializer: IssueSerializer) -> None:
        """Method to create an issue.

        Args:
            serializer (IssueSerializer): The issue serializer.

        Raises:
            ValidationError: The validation error.
            PermissionDenied: The permission denied error.
        """

        # Get the apartment ID
        apartment_id = self.kwargs.get("apartment_id")

        # If the apartment ID is not provided
        if not apartment_id:
            # Raise the validation error
            raise ValidationError({"apartment_id": ["Apartment ID is required."]})

        # Try to get the apartment
        try:
            apartment = Apartment.objects.get(id=apartment_id, tenant=self.request.user)

        # If the apartment does not exist
        except Apartment.DoesNotExist:
            # Raise the validation error
            raise PermissionDenied(
                "You do have the permission to report issues for this apartment."
            )

        # Save the issue
        issue = serializer.save(reported_by=self.request.user, apartment=apartment)

        # Send the issue confirmation email
        send_issue_confirmation_email(issue)


# IssueDetailAPIView Class
class IssueDetailAPIView(generics.RetrieveAPIView):
    """IssueDetailAPIView

    IssueDetailAPIView class is used to retrieve an issue.

    Extends:
        generics.RetrieveAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.
        lookup_field (str): The lookup field.

    Methods:
        get_object: Method to get the issue object.
        record_issue_view: Method to record the issue view.
        get_client_ip: Method to get the

    Raises:
        PermissionDenied: The permission denied error.
    """

    # Attributes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"
    lookup_field = "id"

    # Method to get the issue object
    def get_object(self) -> Issue:
        """Method to get the issue object.

        Returns:
            Issue: The issue object.

        Raises:
            PermissionDenied: The permission denied error.
        """

        # Get the issue
        issue = super().get_object()

        # Get the user
        user = self.request.user

        # If the user is not the reporter, staff, or assignee
        if not (
            user == issue.reported_by or user.is_staff or user == issue.assigned_to
        ):
            # Raise the permission denied error
            raise PermissionDenied("You do not have permission to view this issue.")

        # Record the issue view
        self.record_issue_view(issue)

        # Return the issue
        return issue

    # Method to record the issue view
    def record_issue_view(self, issue: Issue) -> None:
        """Method to record the issue view.

        Args:
            issue (Issue): The issue object.
        """

        # Get the content type
        content_type = ContentType.objects.get_for_model(issue)

        # Get the viewer IP
        viewer_ip = self.get_client_ip()

        # Get the user
        user = self.request.user

        # Get or create the content view
        ContentView.objects.get_or_create(
            content_type=content_type,
            object_id=issue.pk,
            user=user,
            viewer_ip=viewer_ip,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    # Method to get the client IP
    def get_client_ip(self) -> str:
        """Method to get the client IP.

        Returns:
            str: The client IP.
        """

        # Get the X-Forwarded-For header
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")

        # If the X-Forwarded-For header is present
        if x_forwarded_for:
            # Get the IP address
            ip = x_forwarded_for.split(",")[0].strip()

        # If the X-Forwarded-For header is not present
        else:
            # Get the IP address
            ip = self.request.META.get("REMOTE_ADDR")

        # Return the IP address
        return ip


# IssueUpdateAPIView Class
class IssueUpdateAPIView(generics.UpdateAPIView):
    """IssueUpdateAPIView

    IssueUpdateAPIView class is used to update an issue.

    Extends:
        generics.UpdateAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueStatusUpdateSerializer): The issue status update serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        get_object: Method to get the issue object.

    Raises:
        PermissionDenied: The permission denied error.
    """

    # Attributes
    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueStatusUpdateSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "issue"

    # Method to get the issue object
    def get_object(self) -> Issue:
        """Method to get the issue object.

        Returns:
            Issue: The issue object.

        Raises:
            PermissionDenied: The permission denied error.
        """

        # Get the issue
        issue = super().get_object()

        # Get the user
        user = self.request.user

        # If the user is not staff or the assignee
        if not (user.is_staff or user == issue.assigned_to):
            # Log the unauthorized issue status update attempt
            logger.warning(
                f"Unauthorized issue status update attempt by the user {user.full_name} on issue {issue.title}"
            )

            # Raise the permission denied error
            raise PermissionDenied("You do not have permission to update the issue")

        # Return the issue
        return issue


# IssueDeleteAPIView Class
class IssueDeleteAPIView(generics.DestroyAPIView):
    """IssueDeleteAPIView

    IssueDeleteAPIView class is used to delete an issue.

    Extends:
        generics.DestroyAPIView

    Attributes:
        queryset (QuerySet): The queryset of issues.
        serializer_class (IssueSerializer): The issue serializer class.
        lookup_field (str): The lookup field.

    Methods:
        get_object: Method to get the issue object.
        delete: Method to delete the issue.

    Raises:
        Http404: The HTTP 404 Not Found status code.
        PermissionDenied: The permission denied error
    """

    # Attributes
    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueSerializer

    # Method to get the issue object
    def get_object(self) -> Issue:
        """Method to get the issue object.

        Returns:
            Issue: The issue object.

        Raises:
            Http404: The HTTP 404 Not Found status code.
            PermissionDenied: The permission denied error
        """

        # Try to get the issue
        try:
            issue = super().get_object()

        # If the issue does not exist
        except Http404:
            # Raise the HTTP 404 Not Found status code
            raise Http404("Issue not found")

        # If the user is not staff or the reporter
        if not (self.request.user.is_staff or self.request.user == issue.reported_by):
            # Log the unauthorized issue deletion attempt
            logger.warning(
                f"Unauthorized issue deletion attempt by {self.request.user} on issue {issue.title}"
            )

            # Raise the permission denied error
            raise PermissionDenied(
                "You do not have permission to delete this issue. Please contact the admin."
            )

        # Return the issue
        return issue

    # Method to delete the issue
    def delete(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to delete the issue.

        Args:
            request (Request): The request object.
            *args (Dict): Variable length argument list.
            **kwargs (Dict): Arbitrary keyword arguments.

        Returns:
            Response: The response object.

        Raises:
            Http404: The HTTP 404 Not Found status code.
            PermissionDenied: The permission denied error
        """

        # Get the issue
        super().delete(request, *args, **kwargs)

        # Return the response
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
