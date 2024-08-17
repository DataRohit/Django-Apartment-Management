# Imports
from apps.reports.models import Report
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    """Report Serializer

    This class is used to serialize a report.

    Extends:
        serializers.ModelSerializer

    Attributes:
        reported_user_username (str): The username of the reported user.

    Meta Class:
        model (Report): The report model.
        fields (list): The fields to include in the serialized data.

    Methods:
        validate_reported_user_username(value: str) -> str: Validate the reported user username.
        create(validated_data: dict) -> Report: Create a report.

    Raises:
        serializers.ValidationError: If the user with that username does not exist.
    """

    # Attributes
    reported_user_username = serializers.CharField(write_only=True)

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Report): The report model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Report
        fields = [
            "id",
            "title",
            "description",
            "reported_user_username",
            "created_at",
        ]

    # Method to validate the reported user username
    def validate_reported_user_username(self, value: str) -> str:
        """Validate the reported user username.

        Args:
            value (str): The reported user username.

        Returns:
            str: The reported user username.

        Raises:
            serializers.ValidationError: If the user with that username does not exist.
        """

        # If the user does not exist
        if not User.objects.filter(username=value).exists():
            # Raise a validation error
            raise serializers.ValidationError(
                "The user with that username does not exist."
            )

        # Return the value
        return value

    # Method to create a report
    def create(self, validated_data: dict) -> Report:
        """Create a report.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Report: The created report.

        Raises:
            serializers.ValidationError: If the user with that username does not exist.
        """

        # Get the reported user username
        reported_user_username = validated_data.pop("reported_user_username")

        # Try to get the reported user
        try:
            reported_user = User.objects.get(username=reported_user_username)

        # If the user does not exist
        except User.DoesNotExist:
            # Raise a validation error
            raise serializers.ValidationError(
                "The tenant with that username does not exist."
            )

        # Create the report
        report = Report.objects.create(reported_user=reported_user, **validated_data)

        # Return the report
        return report


# Report List Serializer
class ReportListSerializer(serializers.ModelSerializer):
    """Report List Serializer

    This class is used to serialize a list of reports.

    Extends:
        serializers.ModelSerializer

    Attributes:
        reported_user_username (str): The username of the reported user.
        reported_user_full_name (str): The full name of the reported user.

    Meta Class:
        model (Report): The report model.
        fields (list): The fields to include in the serialized data.
        read_only_fields (list): The fields that are read-only.
    """

    # Attributes
    reported_user_username = serializers.CharField(
        source="reported_user.username", read_only=True
    )
    reported_user_full_name = serializers.CharField(
        source="reported_user.full_name", read_only=True
    )

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Report): The report model.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that are read-only.
        """

        # Attributes
        model = Report
        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "reported_user_username",
            "reported_user_full_name",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "reported_user_username",
            "reported_user_full_name",
        ]
