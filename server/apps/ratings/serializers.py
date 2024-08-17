# Imports
from apps.ratings.models import Rating
from rest_framework import serializers


# Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    """Rating serializer.

    This class is used to serialize a rating.

    Extends:
        serializers.ModelSerializer

    Attributes:
        rated_user_username (CharField): The username of the rated user.

    Meta Class:
        model (Rating): The rating model.
        fields (list): The fields to include in the serialized data.
        read_only_fields (list): The fields that are read-only.

    Returns:
        Rating: The rating object.
    """

    # Attributes
    rated_user_username = serializers.CharField(write_only=True)

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Rating): The rating model.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that are read-only.
        """

        # Attributes
        model = Rating
        fields = [
            "id",
            "rated_user_username",
            "rating",
            "comment",
        ]
        read_only_fields = ["id"]

    # Method to create a rating
    def create(self, validated_data: dict) -> Rating:
        """Method to create a rating.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Rating: The rating object.
        """

        # Pop the rated user username
        validated_data.pop("rated_user_username")

        # Create the rating object
        return Rating.objects.create(**validated_data)
