# Imports
from typing import Dict
import logging
from apps.common.models import ContentView
from apps.issues.emails import send_resolution_email
from apps.issues.models import Issue
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import serializers


# Get the logger
logger = logging.getLogger(__name__)


class IssueSerializer(serializers.ModelSerializer):
    """Issue Serializer.

    This class is used to serialize an issue.

    Extends:
        serializers.ModelSerializer

    Attributes:
        apartment_unit: str -- The unit number of the apartment.
        reported_by: str -- The user who reported the issue.
        assigned_to: str -- The user assigned to the issue.
        view_count: int -- The number of views the issue has.

    Meta:
        model: Issue -- The issue model.
        fields: list -- The fields to include.

    Methods:
        get_view_count: Returns the number of views the issue has.
    """

    apartment_unit = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.full_name")
    assigned_to = serializers.ReadOnlyField(source="assigned_to.full_name")
    view_count = serializers.SerializerMethodField()

    class Meta:
        """Meta Class.

        Attributes:
            model: Issue -- The issue model.
            fields: list -- The fields to include.
        """

        model = Issue
        fields = [
            "id",
            "apartment_unit",
            "reported_by",
            "assigned_to",
            "title",
            "description",
            "status",
            "priority",
            "view_count",
        ]

    def get_view_count(self, obj: Issue) -> int:
        """Return the number of views the issue has.

        Arguments:
            obj: Issue -- The issue object.

        Returns:
            int -- The number of views the issue has.
        """

        content_type = ContentType.objects.get_for_model(obj)

        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        return views


class IssueStatusUpdateSerializer(serializers.ModelSerializer):
    """Issue status update serializer.

    This class is used to serialize an issue status update.

    Extends:
        serializers.ModelSerializer

    Attributes:
        apartment: str -- The unit number of the apartment.
        reported_by: str -- The user who reported the issue.
        resolved_by: str -- The user who resolved the issue.

    Meta:
        model: Issue -- The issue model.
        fields: list -- The fields to include.

    Methods:
        update: Updates the issue and sends an email if resolved.
    """

    apartment = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.full_name")
    resolved_by = serializers.ReadOnlyField(source="assigned_to.full_name")

    class Meta:
        """Meta Class.

        Attributes:
            model: Issue -- The issue model.
            fields: list -- The fields to include.
        """

        model = Issue
        fields = [
            "title",
            "description",
            "apartment",
            "reported_by",
            "status",
            "resolved_by",
            "resolved_on",
        ]

    def update(self, instance: Issue, validated_data: Dict) -> Issue:
        """Update the issue and send an email if resolved.

        Arguments:
            instance: Issue -- The issue instance.
            validated_data: dict -- The validated data.

        Returns:
            Issue -- The updated issue instance.
        """

        status_was_resolved = (
            validated_data.get("status") == Issue.IssueStatus.RESOLVED
            and instance.status != Issue.IssueStatus.RESOLVED
        )

        instance = super().update(instance, validated_data)

        if status_was_resolved:
            instance.resolved_on = timezone.now().date()
            instance.save()
            send_resolution_email(instance)

        return instance
