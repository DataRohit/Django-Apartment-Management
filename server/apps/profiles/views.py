# Imports
import os
import uuid
from typing import Dict, List

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


# StandardResultSetPagination
class StandardResultSetPagination(PageNumberPagination):
    """StandardResultSetPagination

    StandardResultSetPagination class is used to paginate the results.

    Extends:
        PageNumberPagination

    Attributes:
        page_size (int): The number of items per page.
        page_size_query_param (str): The query parameter for the page size.
        max_page_size (int): The maximum number of items per page.
    """

    # Attributes
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ProfileListAPIView Class
class ProfileListAPIView(generics.ListAPIView):
    """ProfileListAPIView

    ProfileListAPIView class is used to list profiles.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class (ProfileSerializer): The profile serializer class.
        renderer_classes (tuple): The renderer classes.
        pagination_class (StandardResultSetPagination): The pagination class.
        object_label (str): The object label.
        filter_backends (tuple): The filter backends.
        search_fields (tuple): The search fields.
        filterset_fields (tuple): The filter fields.

    Methods:
        get_queryset() -> List[Profile]: Get the queryset.
    """

    # Attributes
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

    # Method to get the queryset
    def get_queryset(self) -> List[Profile]:
        """Get the queryset.

        Returns:
            List[Profile]: The queryset.
        """

        # Return the queryset
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .filter(occupation=Profile.Occupation.TENANT)
        )


# ProfileDetailAPIView Class
class ProfileDetailAPIView(generics.RetrieveAPIView):
    """ProfileDetailAPIView

    ProfileDetailAPIView class is used to retrieve a profile.

    Extends:
        generics.RetrieveAPIView

    Attributes:
        serializer_class (ProfileSerializer): The profile serializer class.
        renderer_classes (tuple): The renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset() -> QuerySet: Get the queryset.
        get_object() -> Profile: Get the object.

    Raises:
        Http404: If the profile does not exist.
    """

    # Attributes
    serializer_class = ProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "profile"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset.

        Returns:
            QuerySet: The queryset.
        """

        # Return the profile queryset
        return Profile.objects.select_related("user").all()

    # Method to get the object
    def get_object(self) -> Profile:
        """Get the object.

        Returns:
            Profile: The profile.

        Raises:
            Http404: If the profile does not exist.
        """

        # Try to get the profile
        try:
            # Return the profile
            return Profile.objects.get(user=self.request.user)

        # If the profile does not exist
        except Profile.DoesNotExist:
            # Raise an Http404 error
            raise Http404("Profile does not exist")


# ProfileUpdateAPIView Class
class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """ProfileUpdateAPIView

    ProfileUpdateAPIView class is used to update a profile.

    Extends:
        generics.RetrieveUpdateAPIView

    Attributes:
        serializer_class (UpdateProfileSerializer): The update profile serializer class.
        renderer_classes (tuple): The renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset() -> None: Get the queryset.
        get_object() -> Profile: Get the object.
        perform_update(serializer: UpdateProfileSerializer) -> Profile: Perform the update.
    """

    # Attributes
    serializer_class = UpdateProfileSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "profile"

    # Method to get the queryset
    def get_queryset(self) -> None:
        """Get the queryset.

        Returns:
            None
        """

        # Return an empty queryset
        return Profile.objects.none()

    # Method to get the object
    def get_object(self) -> Profile:
        """Get the object.

        Returns:
            Profile: The profile.
        """

        # Get or create the profile
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        # Return the profile
        return profile

    # Method to perform the update
    def perform_update(self, serializer: UpdateProfileSerializer) -> Profile:
        """Perform the update.

        Args:
            serializer (UpdateProfileSerializer): The update profile serializer.

        Returns:
            Profile: The profile.
        """

        # Get the user data
        user_data = serializer.validated_data.pop("user", {})

        # Save the profile
        profile = serializer.save()

        # Get the user and update the user
        User.objects.filter(id=self.request.user.id).update(**user_data)

        # Return the profile
        return profile


# AvatarUploadAPIView Class
class AvatarUploadAPIView(APIView):
    """AvatarUploadAPIView

    AvatarUploadAPIView class is used to upload an avatar.

    Extends:
        APIView

    Methods:
        patch(request: Request, *args: Dict, **kwargs: Dict) -> Response: Patch method.
        upload_avatar(request: Request, *args: Dict, **kwargs: Dict) -> Response: Upload the avatar.

    Raises:
        Http404: If the profile does not exist.
    """

    # Method to patch
    def patch(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to patch.

        Args:
            request (Request): The request.
            *args (Dict): The arguments.
            **kwargs (Dict): The keyword arguments.

        Returns:
            Response: The response.
        """

        # Return the upload avatar method
        return self.upload_avatar(request, *args, **kwargs)

    # Method to upload the avatar
    def upload_avatar(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to upload the avatar.

        Args:
            request (Request): The request.
            *args (Dict): The arguments.
            **kwargs (Dict): The keyword arguments.

        Returns:
            Response: The response.

        Raises:
            Http404: If the profile does not exist.
        """

        # Try to get the user profile
        try:
            profile = request.user.profile

        # If the profile does not exist
        except ObjectDoesNotExist:
            # Raise an Http404 error
            raise Http404("Profile does not exist")

        # Get the avatar upload serializer
        serializer = AvatarUploadSerializer(profile, data=request.data)

        # If the serializer is valid
        if serializer.is_valid():
            # Get the image
            image = serializer.validated_data.get("avatar")

            # If the image is None
            if image is None:
                # Return a response
                return Response(
                    {"avatar": ["This field is required."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Read the image content
            image_content = image.read()

            # Get the image extension
            ext = os.path.splitext(image.name)[1]

            # Generate a unique image name
            image_name = f"{uuid.uuid4()}{ext}"

            # Save the image
            profile.avatar.save(image_name, ContentFile(image_content))

            # Return a response
            return Response(
                {"message": "Avatar uploaded successfully"},
                status=status.HTTP_200_OK,
            )

        # Return a response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# NonTenantProfileListAPIView Class
class NonTenantProfileListAPIView(generics.ListAPIView):
    """NonTenantProfileListAPIView

    NonTenantProfileListAPIView class is used to list non-tenant profiles.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class (ProfileSerializer): The profile serializer class.
        renderer_classes (tuple): The renderer classes.
        pagination_class (StandardResultSetPagination): The pagination class.
        object_label (str): The object label.
        filter_backends (tuple): The filter backends.
        search_fields (tuple): The search fields.
        filterset_fields (tuple): The filter fields.

    Methods:
        get_queryset() -> List[Profile]: Get the queryset.
    """

    # Attributes
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

    # Method to get the queryset
    def get_queryset(self) -> List[Profile]:
        """Get the queryset.

        Returns:
            List[Profile]: The queryset.
        """

        # Return the queryset
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .exclude(occupation=Profile.Occupation.TENANT)
        )
