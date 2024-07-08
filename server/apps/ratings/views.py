# Imports
from typing import Dict
from apps.common.renderers import GenericJSONRenderer
from apps.profiles.models import Profile
from apps.ratings.models import Rating
from apps.ratings.serializers import RatingSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


# Get the user model
User = get_user_model()


class RatingCreateAPIView(generics.CreateAPIView):
    """Rating create view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        serializer_class: RatingSerializer -- The rating serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        create: Method to create a rating.
    """

    serializer_class = RatingSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "rating"

    def create(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to create a rating.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- The arguments.
            **kwargs: Dict -- The keyword arguments.

        Returns:
            Response: The response object.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rated_user_username = serializer.validated_data.get("rated_user_username")

        try:
            rated_user = User.objects.get(username=rated_user_username)
        except User.DoesNotExist:
            raise NotFound(f"User with username {rated_user_username} does not exist.")

        rating_user = request.user
        if rating_user == rated_user:
            raise PermissionDenied("You cannot rate yourself.")

        try:
            rating_user_occupation = rating_user.profile.occupation
            rated_user_occupation = rated_user.profile.occupation
        except Profile.DoesNotExist:
            raise ValidationError("Both occupations must have valid occupation.")

        if (
            rating_user_occupation == Profile.Occupation.TENANT
            and rated_user_occupation == Profile.Occupation.TENANT
        ):
            raise PermissionDenied("A tenant cannot rate another tenant.")

        allowed_occupations = [
            Profile.Occupation.CARPENTER,
            Profile.Occupation.ELECTRICIAN,
            Profile.Occupation.PLUMBER,
            Profile.Occupation.HVAC,
            Profile.Occupation.MASON,
            Profile.Occupation.ROOFER,
            Profile.Occupation.PAINTER,
        ]

        if (
            rating_user_occupation == Profile.Occupation.TENANT
            and rated_user_occupation not in allowed_occupations
        ):
            raise PermissionDenied("A tenant can only rate a service provider.")

        if (
            rating_user_occupation != Profile.Occupation.TENANT
            and rating_user == rated_user
        ):
            raise PermissionDenied("A service provider cannot rate itself.")

        if (
            rating_user_occupation != Profile.Occupation.TENANT
            and rated_user_occupation != Profile.Occupation.TENANT
        ):
            raise PermissionDenied(
                "A service provider cannot rate another service provider."
            )

        rating = serializer.save(rating_user=rating_user, rated_user=rated_user)

        serializer = self.get_serializer(rating)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
