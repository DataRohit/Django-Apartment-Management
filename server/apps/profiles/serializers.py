# Imports
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Profile Serializer.

    This class is used to serialize a profile.

    Extends:
        serializers.ModelSerializer

    Attributes:
        first_name: str -- The first name of the user.
        last_name: str -- The last name of the user.
        username: str -- The username of the user.
        full_name: str -- The full name of the user.
        country_of_origin: str -- The country of origin of the user.
        avatar: str -- The avatar of the user.
        date_joined: datetime -- The date the user joined.

    Meta:
        model: Profile -- The profile model.
        fields: list -- The fields to include.
    """

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    country_of_origin = CountryField(name_only=True)
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        """Meta Class.

        Attributes:
            model: Profile -- The profile model.
            fields: list -- The fields to include.
        """

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
        ]

    def get_avatar(self, obj: Profile) -> str | None:
        """Get the avatar of the user.

        Arguments:
            obj: Profile -- The profile object.

        Returns:
            str | None: The avatar of the user.
        """
        try:
            return obj.avatar.url
        except AttributeError:
            return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update Profile Serializer.

    This class is used to serialize a profile for updating.

    Extends:
        serializers.ModelSerializer

    Attributes:
        first_name: str -- The first name of the user.
        last_name: str -- The last name of the user.
        username: str -- The username of the user.
        country_of_origin: str -- The country of origin of the user.

    Meta:
        model: Profile -- The profile model.
        fields: list -- The fields to include.
    """

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    country_of_origin = CountryField(name_only=True)

    class Meta:
        """Meta Class.

        Attributes:
            model: Profile -- The profile model.
            fields: list -- The fields to include.
        """

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


class AvatarUploadSerializer(serializers.ModelSerializer):
    """Avatar Upload Serializer.

    This class is used to serialize an avatar upload.

    Extends:
        serializers.ModelSerializer

    Meta:
        model: Profile -- The profile model.
        fields: list -- The fields to include.
    """

    class Meta:
        """Meta Class.

        Attributes:
            model: Profile -- The profile model.
            fields: list -- The fields to include.
        """

        model = Profile
        fields = ["avatar"]
