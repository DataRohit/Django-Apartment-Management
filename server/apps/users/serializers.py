# Imports
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


# Get the user model
User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    """Create User Serializer.

    This class is used to create a user.

    Extends:
        UserCreateSerializer

    Meta:
        model: User -- The user model.
        fields: tuple -- The fields to include.
        extra_kwargs: dict -- The extra keyword arguments.
    """

    class Meta(UserCreateSerializer.Meta):
        """Meta Class.

        Attributes:
            model: User -- The user model.
            fields: tuple -- The fields to include.
            extra_kwargs: dict -- The extra keyword arguments.
        """

        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """Custom User Serializer.

    This class is used to serialize a user.

    Extends:
        UserSerializer

    Attributes:
        full_name: str -- The full name of the the user.
        gender: str -- Gender of the user.
        slug: str -- The slug of the user.
        occupation: str -- The occupation of the user.
        phone_number: str -- The phone number of the user.
        country: str -- The country of the user.
        city: str -- The city of the user.
        avatar: str -- The avatar of the user.
        reputation: int -- The reputation of the user.

    Meta:
        model: User -- The user model.
        fields: tuple -- The fields to include.
        read_only_fields: tuple -- The fields that are read only.
    """

    full_name = serializers.ReadOnlyField()
    gender = serializers.ReadOnlyField(source="profile.gender")
    slug = serializers.ReadOnlyField(source="profile.slug")
    occupation = serializers.ReadOnlyField(source="profile.occupation")
    phone_number = PhoneNumberField(source="profile.phone_number")
    country = CountryField(source="profile.country_of_origin")
    city = serializers.ReadOnlyField(source="profile.city_of_origin")
    avatar = serializers.ReadOnlyField(source="profile.avatar.url")
    reputation = serializers.ReadOnlyField(source="profile.reputation")

    class Meta(UserSerializer.Meta):
        """Meta Class.

        Attributes:
            model: User -- The user model.
            fields: tuple -- The fields to include.
            read_only_fields: tuple -- The fields that are read only.
        """

        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "username",
            "slug",
            "gender",
            "occupation",
            "phone_number",
            "country",
            "city",
            "avatar",
            "reputation",
            "date_joined",
        )
        read_only_fields = ("id", "email", "date_joined")
