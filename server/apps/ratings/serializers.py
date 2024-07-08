# Imports
from apps.ratings.models import Rating
from rest_framework import serializers


class RatingSerializer(serializers.ModelSerializer):
    """Rating Serializer.

    This class is used to serialize a rating.

    Extends:
        serializers.ModelSerializer

    Attributes:
        rated_user_username: str -- The username of the rated user.

    Meta:
        model: Rating -- The rating model.
        fields: list -- The fields to serialize.
        read_only_fields: list -- The fields that are read only.

    Methods:
        create: Creates a rating.
    """

    rated_user_username = serializers.CharField(write_only=True)

    class Meta:
        """Meta Class.

        The meta class for the serializer.

        Attributes:
            model: Rating -- The rating model.
            fields: list -- The fields to serialize.
            read_only_fields: list -- The fields that are read only.
        """

        model = Rating
        fields = [
            "id",
            "rated_user_username",
            "rating",
            "comment",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Rating:
        """Creates a rating.

        Arguments:
            validated_data: dict -- The validated data.

        Returns:
            Rating: The created rating.
        """

        validated_data.pop("rated_user_username")

        return Rating.objects.create(**validated_data)
