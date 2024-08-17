# Imports
from typing import Dict

from apps.common.renderers import GenericJSONRenderer
from apps.profiles.models import Profile
from apps.ratings.serializers import RatingSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

# Get the user model
User = get_user_model()


# Rating Create API View
class RatingCreateAPIView(generics.CreateAPIView):
    """Rating Create API View

    Extends:
        generics.CreateAPIView

    Attributes:
        serializer_class (RatingSerializer): The rating serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        create(request: Request, *args: Dict, **kwargs: Dict) -> Response: Create a rating.

    Returns:
        Response: The response.

    Raises:
        NotFound: If the user does not exist.
        PermissionDenied: If the user tries to rate itself.
        ValidationError: If the occupations are not valid.
    """

    # Attributes
    serializer_class = RatingSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "rating"

    # Method to create a rating
    def create(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Create a rating.

        Args:
            request (Request): The request object.
            *args (Dict): The arguments.
            **kwargs (Dict): The keyword arguments.

        Returns:
            Response: The response.

        Raises:
            NotFound: If the user does not exist.
            PermissionDenied: If the user tries to rate itself.
            ValidationError: If the occupations are not valid.
        """

        # Get the serializer and validate the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the rated user username
        rated_user_username = serializer.validated_data.get("rated_user_username")

        # Get the rated user
        try:
            rated_user = User.objects.get(username=rated_user_username)

        # If the user does not exist
        except User.DoesNotExist:
            # Raise a not found exception
            raise NotFound(f"User with username {rated_user_username} does not exist.")

        # Get the rating user
        rating_user = request.user

        # If the rating user is the rated user
        if rating_user == rated_user:
            # Raise a permission denied exception
            raise PermissionDenied("You cannot rate yourself.")

        # Try to get the occupations
        try:
            rating_user_occupation = rating_user.profile.occupation
            rated_user_occupation = rated_user.profile.occupation

        # If profile does not exist
        except Profile.DoesNotExist:
            # Raise a validation error
            raise ValidationError("Both occupations must have valid occupation.")

        # If the rating user is a tenant and the rated user is a tenant
        if (
            rating_user_occupation == Profile.Occupation.TENANT
            and rated_user_occupation == Profile.Occupation.TENANT
        ):
            # Raise a permission denied exception
            raise PermissionDenied("A tenant cannot rate another tenant.")

        # Initialize the allowed occupations
        allowed_occupations = [
            Profile.Occupation.CARPENTER,
            Profile.Occupation.ELECTRICIAN,
            Profile.Occupation.PLUMBER,
            Profile.Occupation.HVAC,
            Profile.Occupation.MASON,
            Profile.Occupation.ROOFER,
            Profile.Occupation.PAINTER,
        ]

        # If the rating user is a tenant and the rated user is not in the allowed occupations
        if (
            rating_user_occupation == Profile.Occupation.TENANT
            and rated_user_occupation not in allowed_occupations
        ):
            # Raise a permission denied exception
            raise PermissionDenied("A tenant can only rate a service provider.")

        # If the rating user is not a tenant and the rated user is not a tenant
        if (
            rating_user_occupation != Profile.Occupation.TENANT
            and rating_user == rated_user
        ):
            # Raise a permission denied exception
            raise PermissionDenied("A service provider cannot rate itself.")

        # If the rating user is not a tenant and the rated user is a tenant
        if (
            rating_user_occupation != Profile.Occupation.TENANT
            and rated_user_occupation != Profile.Occupation.TENANT
        ):
            # Raise a permission denied exception
            raise PermissionDenied(
                "A service provider cannot rate another service provider."
            )

        # Get the rating
        rating = serializer.save(rating_user=rating_user, rated_user=rated_user)

        # Get the serialized data
        serializer = self.get_serializer(rating)

        # Get the headers
        headers = self.get_success_headers(serializer.data)

        # Return the response and the headers
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
