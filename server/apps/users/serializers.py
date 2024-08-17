# Imports
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

# Get the user model
User = get_user_model()


# Create User Serializer
class CreateUserSerializer(UserCreateSerializer):
    """CreateUserSerializer

    CreateUserSerializer class is used to create a user.

    Extends:
        UserCreateSerializer

    Meta Class:
        model (User): The user model.
        fields (tuple): The fields to include in the serialized data.
        extra_kwargs (dict): The extra keyword arguments.
    """

    # Meta Class
    class Meta(UserCreateSerializer.Meta):
        """Meta Class

        Attributes:
            model (User): The user model.
            fields (tuple): The fields to include in the serialized data.
            extra_kwargs (dict): The extra keyword arguments.
        """

        # Attributes
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}


# Custom User Serializer
class CustomUserSerializer(UserSerializer):
    """CustomUserSerializer

    CustomUserSerializer class is used to serialize a user.

    Extends:
        UserSerializer

    Attributes:
        full_name (ReadOnlyField): The full name of the user.
        gender (ReadOnlyField): The gender of the user's profile.
        slug (ReadOnlyField): The slug of the user's profile.
        occupation (ReadOnlyField): The occupation of the user's profile.
        phone_number (PhoneNumberField): The phone number of the user's profile.
        country (CountryField): The country of origin of the user's profile.
        city (ReadOnlyField): The city of origin of the user's profile.
        avatar (ReadOnlyField): The avatar URL of the user's profile.
        reputation (ReadOnlyField): The reputation of the user's profile.

    Meta Class:
        model (User): The user model.
        fields (tuple): The fields to include in the serialized data.
        read_only_fields (tuple): The fields to make read-only.
    """

    # Attributes
    full_name = serializers.ReadOnlyField()
    gender = serializers.ReadOnlyField(source="profile.gender")
    slug = serializers.ReadOnlyField(source="profile.slug")
    occupation = serializers.ReadOnlyField(source="profile.occupation")
    phone_number = PhoneNumberField(source="profile.phone_number")
    country = CountryField(source="profile.country_of_origin")
    city = serializers.ReadOnlyField(source="profile.city_of_origin")
    avatar = serializers.ReadOnlyField(source="profile.avatar.url")
    reputation = serializers.ReadOnlyField(source="profile.reputation")

    # Meta Class
    class Meta(UserSerializer.Meta):
        """Meta Class

        Attributes:
            model (User): The user model.
            fields (tuple): The fields to include in the serialized data.
            read_only_fields (tuple): The fields to make read-only.
        """

        # Attributes
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
