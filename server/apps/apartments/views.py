# Imports
from typing import Any
from apps.apartments.models import Apartment
from apps.apartments.serializers import ApartmentSerializer
from apps.common.renderers import GenericJSONRenderer
from apps.profiles.models import Profile
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response


class ApartmentCreateAPIView(generics.CreateAPIView):
    """Apartment create view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset: QuerySet -- The apartment queryset.
        serializer_class: ApartmentSerializer -- The apartment serializer class.
        renderer_classes: tuple -- The tuple of renderer classes.
        object_label: str -- The object label.

    Methods:
        create: Creates an apartment.
    """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "apartment"

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create method.

        This method creates an apartment.

        Arguments:
            request: Request -- The request object.

        Returns:
            Response -- The response object.

        Raises:
            Http403: The HTTP 403 Forbidden status code.
        """

        user = request.user

        if user.is_superuser or (
            hasattr(user, "profile")
            and user.profile.occupation == Profile.Occupation.TENANT
        ):
            return super().create(request, *args, **kwargs)

        return Response(
            {"error": "You are not authorized to create an apartment."},
            status=status.HTTP_403_FORBIDDEN,
        )


class ApartmentListAPIView(generics.ListAPIView):
    """Apartment list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: ApartmentSerializer -- The apartment serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "apartments"

    def get_queryset(self):
        """Method to get the queryset.

        This method returns the queryset of apartments for the current user.

        Returns:
            QuerySet -- The queryset of apartments.
        """

        return self.request.user.apartment.all()
