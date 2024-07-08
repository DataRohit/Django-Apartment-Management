# Imports
from apps.apartments.models import Apartment
from rest_framework import serializers


class ApartmentSerializer(serializers.ModelSerializer):
    """Apartment Serializer.

    This class is used to serialize an apartment.

    Extends:
        serializers.ModelSerializer

    Attributes:
        tenant: HiddenField -- The tenant of the apartment.

    Meta:
        model: Apartment -- The apartment model.
        exclude: tuple -- The fields to exclude.
    """

    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta Class.

        Attributes:
            model: Apartment -- The apartment model.
            exclude: tuple -- The fields to exclude.
        """

        model = Apartment
        exclude = ("pkid", "updated_at")
