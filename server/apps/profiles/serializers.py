# Imports
from apps.apartments.serializers import ApartmentSerializer
from apps.profiles.models import Profile
from django_countries.serializer_fields import CountryField
from rest_framework import serializers


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer

    This class is used to serialize a profile.

    Extends:
        serializers.ModelSerializer

    Attributes:
        first_name (ReadOnlyField): The first name of the user.
        last_name (ReadOnlyField): The last name of the user.
        username (ReadOnlyField): The username of the user.
        full_name (ReadOnlyField): The full name of the user.
        country_of_origin (CountryField): The country of origin of the user.
        avatar (SerializerMethodField): The avatar of the user.
        date_joined (DateTimeField): The date the user joined.
        apartment (SerializerMethodField): The apartment the user belongs to.
        average_rating (SerializerMethodField): The average rating of the user.

    Methods:
        get_avatar(obj: Profile) -> str | None: Get the avatar of the user.
        get_apartment(obj: Profile) -> list | None: Get the apartment the user belongs to.
        get_average_rating(obj: Profile) -> float: Get the average rating

    Meta Class:
        model (Profile): The profile model.
        fields (list): The fields to include in the serialized data.
    """

    # Attributes
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.full_name")
    country_of_origin = CountryField(name_only=True)
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    apartment = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Profile): The profile model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Profile
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "username",
            "full_name",
            "gender",
            "country_of_origin",
            "city_of_origin",
            "bio",
            "occupation",
            "reputation",
            "date_joined",
            "avatar",
            "apartment",
            "average_rating",
        ]

    # Method to get the avatar url
    def get_avatar(self, obj: Profile) -> str | None:
        """Get the avatar of the user.

        Args:
            obj (Profile): The profile.

        Returns:
            str | None: The avatar of the user.
        """

        # Try to get the avatar url
        try:
            return obj.avatar.url

        # If the avatar does not exist
        except ValueError:
            # Return None
            return None

    # Method to get the apartment
    def get_apartment(self, obj: Profile) -> list | None:
        """Get the apartment the user belongs to.

        Args:
            obj (Profile): The profile.

        Returns:
            list | None: The apartment the user belongs to.
        """

        # Get all the apartments
        apartments = obj.user.apartment.all()

        # If the apartments exist
        if apartments:
            # Serialize the apartments
            return ApartmentSerializer(apartments, many=True).data

        # Return None
        return None

    # Method to get the average rating
    def get_average_rating(self, obj: Profile) -> float:
        """Get the average rating.

        Args:
            obj (Profile): The profile.

        Returns:
            float: The average rating.
        """

        # Return the average rating
        return obj.get_average_rating()


# Update Profile Serializer
class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update profile serializer

    This class is used to serialize the update of a profile.

    Extends:
        serializers.ModelSerializer

    Attributes:
        first_name (ReadOnlyField): The first name of the user.
        last_name (ReadOnlyField): The last name of the user.
        username (ReadOnlyField): The username of the user.
        country_of_origin (CountryField): The country of origin of the user.

    Meta Class:
        model (Profile): The profile model.
        fields (list): The fields to include in the serialized data.
    """

    # Attributes
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    country_of_origin = CountryField(name_only=True)

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Profile): The profile model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "username",
            "gender",
            "country_of_origin",
            "city_of_origin",
            "bio",
            "occupation",
            "phone_number",
        ]


# Avatar Upload Serializer
class AvatarUploadSerializer(serializers.ModelSerializer):
    """Avatar upload serializer

    This class is used to serialize the upload of an avatar.

    Extends:
        serializers.ModelSerializer

    Meta Class:
        model (Profile): The profile model.
        fields (list): The fields to include in the serialized data.
    """

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Profile): The profile model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Profile
        fields = ["avatar"]
