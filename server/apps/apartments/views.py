# Imports
from typing import Any

from apps.apartments.models import Apartment
from apps.apartments.serializers import ApartmentSerializer
from apps.common.renderers import GenericJSONRenderer
from apps.profiles.models import Profile
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response


# ApartmentCreateAPIView Class
class ApartmentCreateAPIView(generics.CreateAPIView):
    """ApartmentCreateAPIView

    ApartmentCreateAPIView class is used to create an apartment.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset (QuerySet): The queryset of apartments.
        serializer_class (ApartmentSerializer): The apartment serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        create: Method to create an apartment.

    Raises:
        Http403: The HTTP 403 Forbidden status code.
    """

    # Attributes
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "apartment"

    # Method to create an apartment
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Method to create an apartment.

        Args:
            request (Request): The request object.
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            Response: The response object.

        Raises:
            Http403: The HTTP 403 Forbidden status code.
        """

        # Get the user
        user = request.user

        # Check if the user is authorized to create an apartment
        if user.is_superuser or (
            hasattr(user, "profile")
            and user.profile.occupation == Profile.Occupation.TENANT
        ):
            # Create the apartment
            return super().create(request, *args, **kwargs)

        # Return the error response
        return Response(
            {"error": "You are not authorized to create an apartment."},
            status=status.HTTP_403_FORBIDDEN,
        )


# ApartmentDetailAPIView Class
class ApartmentListAPIView(generics.ListAPIView):
    """ApartmentListAPIView

    ApartmentListAPIView class is used to list the apartments.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class (ApartmentSerializer): The apartment serializer class.
        renderer_classes (list): The list of renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset: Method to get the queryset.

    Raises:
        Http403: The HTTP 403 Forbidden status code.
    """

    # Attributes
    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "apartments"

    # Method to get the queryset
    def get_queryset(self):
        """Method to get the queryset.

        Returns:
            QuerySet: The queryset of apartments.
        """

        # Return the queryset
        return self.request.user.apartment.all()
