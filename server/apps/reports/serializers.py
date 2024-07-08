# Imports
from apps.reports.models import Report
from django.contrib.auth import get_user_model
from rest_framework import serializers


# Get the user model
User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):
    """Report Serializer.

    This class is used to serialize a report.

    Extends:
        serializers.ModelSerializer

    Attributes:
        reported_user_username: str -- The username of the reported user.

    Meta:
        model: Report -- The report model.
        fields: list -- The fields to serialize.

    Methods:
        validate_reported_user_username: Validates the reported user username.
        create: Creates a report.
    """

    reported_user_username = serializers.CharField(write_only=True)

    class Meta:
        """Meta Class.

        The meta class for the ReportSerializer.

        Attributes:
            model: Report -- The report model.
            fields: list -- The fields to serialize.
        """

        model = Report
        fields = [
            "id",
            "title",
            "description",
            "reported_user_username",
            "created_at",
        ]

    def validate_reported_user_username(self, value: str) -> str:
        """Validates the reported user username.

        Arguments:
            value: str -- The reported user username.

        Returns:
            str: The reported user username.

        Raises:
            serializers.ValidationError: If the user with the username does not exist.
        """

        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "The user with that username does not exist."
            )
        return value

    def create(self, validated_data: dict) -> Report:
        """Creates a report.

        Arguments:
            validated_data: dict -- The validated data.

        Returns:
            Report: The created report.

        Raises:
            serializers.ValidationError: If the user with the username does not exist.
        """

        reported_user_username = validated_data.pop("reported_user_username")

        try:
            reported_user = User.objects.get(username=reported_user_username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "The tenant with that username does not exist."
            )

        report = Report.objects.create(reported_user=reported_user, **validated_data)
        return report


class ReportListSerializer(serializers.ModelSerializer):
    """Report list serializer.

    This class is used to serialize a list of reports.

    Extends:
        serializers.ModelSerializer

    Attributes:
        reported_user_username: str -- The username of the reported user.
        reported_user_full_name: str -- The full name of the reported user.

    Meta:
        model: Report -- The report model.
        fields: list -- The fields to serialize.
        read_only_fields: list -- The fields that are read only.
    """

    reported_user_username = serializers.CharField(
        source="reported_user.username", read_only=True
    )
    reported_user_full_name = serializers.CharField(
        source="reported_user.full_name", read_only=True
    )

    class Meta:
        """Meta Class.

        The meta class for the ReportListSerializer.

        Attributes:
            model: Report -- The report model.
            fields: list -- The fields to serialize.
            read_only_fields: list -- The fields that are read only.
        """

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
