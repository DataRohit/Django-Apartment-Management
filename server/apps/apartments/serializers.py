# Imports
from apps.apartments.models import Apartment
from rest_framework import serializers


# Apartment Serializer
class ApartmentSerializer(serializers.ModelSerializer):
    """ApartmentSerializer

    ApartmentSerializer class is used to serialize the apartment model.

    Attributes:
        tenant (HiddenField): The tenant of the apartment.

    Meta Class:
        model (Apartment): The apartment model.
        exclude (tuple): The fields to exclude.
    """

    # Attributes
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Apartment): The apartment model.
            exclude (tuple): The fields to exclude.
        """

        # Attributes
        model = Apartment
        exclude = ("pkid", "updated_at")
