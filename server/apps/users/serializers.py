# Imports
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer


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
