# Imports
import os
import uuid
from typing import List, Dict
from apps.common.renderers import GenericJSONRenderer
from apps.profiles.models import Profile
from apps.profiles.serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Get the user model
User = get_user_model()


class StandardResultSetPagination(PageNumberPagination):
    """Standard result set pagination class.

    Attributes:
        page_size: int -- The number of items per page.
        page_size_query_param: str -- The query parameter to set the page size.
        max_page_size: int -- The maximum number of items per page.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProfileListAPIView(generics.ListAPIView):
    """Profile list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: ProfileSerializer -- The profile serializer class.
        renderer_classes: List -- The list of renderer classes.
        pagination_class: StandardResultSetPagination -- The pagination class.
        object_label: str -- The object label.
        filter_backends: List -- The list of filter backends.
        search_fields: List -- The list of search fields.
        filterset_fields: List -- The list of filterset fields.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = ProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    pagination_class = StandardResultSetPagination
    object_label = "profiles"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    filterset_fields = ("occupation", "gender", "country_of_origin")

    def get_queryset(self) -> List[Profile]:
        """Method to get the queryset.

        This method returns the list of profiles of users who are not staff or superusers and are tenants.

        Returns:
            List[Profile] -- The list of profiles.
        """

        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .filter(occupation=Profile.Occupation.TENANT)
        )


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """Profile detail view class.

    Extends:
        generics.RetrieveAPIView

    Attributes:
        serializer_class: ProfileSerializer -- The profile serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
        get_object: Method to get the object.
    """

    serializer_class = ProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "profile"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method returns the list of profiles of users who are not staff or superusers.

        Returns:
            QuerySet -- The queryset of profiles.
        """

        return Profile.objects.select_related("user").all()

    def get_object(self) -> Profile:
        """Method to get the object.

        This method returns the profile object of the user.

        Returns:
            Profile -- The profile object.

        Raises:
            Http404: If the profile does not exist.
        """

        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Profile update view class.

    Extends:
        generics.RetrieveUpdateAPIView

    Attributes:
        serializer_class: UpdateProfileSerializer -- The update profile serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
        get_object: Method to get the object.
        perform_update: Method to perform the update.
    """

    serializer_class = UpdateProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "profile"

    def get_queryset(self) -> None:
        """Method to get the queryset.

        This method returns an empty queryset.
        """

        return Profile.objects.none()

    def get_object(self) -> Profile:
        """Method to get the object.

        This method returns the profile object of the user.

        Returns:
            Profile -- The profile object.
        """

        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer: UpdateProfileSerializer) -> Profile:
        """Method to perform the update.

        This method updates the profile and user data.

        Arguments:
            serializer: UpdateProfileSerializer -- The update profile serializer.

        Returns:
            Profile -- The updated profile.
        """

        user_data = serializer.validated_data.pop("user", {})
        profile = serializer.save()

        User.objects.filter(id=self.request.user.id).update(**user_data)

        return profile


class AvatarUploadAPIView(APIView):
    """Avatar upload view class.

    Extends:
        APIView

    Methods:
        patch: Method to handle the PATCH request.
        upload_avatar: Method to upload the avatar.
    """

    def patch(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to handle the PATCH request.

        This method calls the upload_avatar method.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- The arguments.
            **kwargs: Dict -- The keyword arguments.

        Returns:
            Response -- The response object.
        """

        return self.upload_avatar(request, *args, **kwargs)

    def upload_avatar(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to upload the avatar.

        This method uploads the avatar to the user's profile.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- The arguments.
            **kwargs: Dict -- The keyword arguments.

        Returns:
            Response -- The response object.

        Raises:
            Http404: If the profile does not exist.
        """

        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            raise Http404("Profile does not exist")

        serializer = AvatarUploadSerializer(profile, data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data.get("avatar")

            if image is None:
                return Response(
                    {"avatar": ["This field is required."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            image_content = image.read()

            ext = os.path.splitext(image.name)[1]

            image_name = f"{uuid.uuid4()}{ext}"

            profile.avatar.save(image_name, ContentFile(image_content))

            return Response(
                {"message": "Avatar uploaded successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class NonTenantProfileListAPIview(generics.ListAPIView):
    """Non Tenant Profile list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: ProfileSerializer -- The profile serializer class.
        renderer_classes: List -- The list of renderer classes.
        pagination_class: StandardResultSetPagination -- The pagination class.
        object_label: str -- The object label.
        filter_backends: List -- The list of filter backends.
        search_fields: List -- The list of search fields.
        filterset_fields: List -- The list of filterset fields.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = ProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    pagination_class = StandardResultSetPagination
    object_label = "non_tenant_profiles"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    filterset_fields = ("occupation", "gender", "country_of_origin")

    def get_queryset(self) -> List[Profile]:
        """Method to get the queryset.

        This method returns the list of profiles of users who are not staff or superusers and are not tenants.

        Returns:
            List[Profile] -- The list of profiles.
        """

        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .exclude(occupation=Profile.Occupation.TENANT)
        )
