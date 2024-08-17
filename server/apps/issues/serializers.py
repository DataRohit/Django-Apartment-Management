# Imports
import logging
from typing import Dict

from apps.common.models import ContentView
from apps.issues.emails import send_resolution_email
from apps.issues.models import Issue
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import serializers

# Get the logger
logger = logging.getLogger(__name__)


# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    """Issue serializer

    This class is used to serialize an issue.

    Extends:
        serializers.ModelSerializer

    Attributes:
        apartment_unit (ReadOnlyField): The unit number of the apartment.
        reported_by (ReadOnlyField): The user who reported the issue.
        assigned_to (ReadOnlyField): The user assigned to the issue.
        view_count (SerializerMethodField): The number of views the issue has.

    Meta Class:
        model (Issue): The issue model.
        fields (list): The fields to include in the serialized data.

    Methods:
        get_view_count(obj: Issue) -> int: Get the number
    """

    # Attributes
    apartment_unit = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.full_name")
    assigned_to = serializers.ReadOnlyField(source="assigned_to.full_name")
    view_count = serializers.SerializerMethodField()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Issue): The issue model.
            fields (list): The fields to include in the serialized
        """

        # Attributes
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

    # Method to get the view count
    def get_view_count(self, obj: Issue) -> int:
        """Get the number of views the issue has.

        Args:
            obj (Issue): The issue.

        Returns:
            int: The number of views the issue has.
        """

        # Get the content type
        content_type = ContentType.objects.get_for_model(obj)

        # Get the number of views
        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        # Return the number of views
        return views


# Issue Status Update Serializer
class IssueStatusUpdateSerializer(serializers.ModelSerializer):
    """Issue status update serializer

    This class is used to serialize the status update of an issue.

    Extends:
        serializers.ModelSerializer

    Attributes:
        apartment (ReadOnlyField): The unit number of the apartment.
        reported_by (ReadOnlyField): The user who reported the issue.
        resolved_by (ReadOnlyField): The user who resolved the issue.

    Meta Class:
        model (Issue): The issue model.
        fields (list): The fields to include in the serialized data.

    Methods:
        update(instance: Issue, validated_data: Dict) -> Issue: Update the issue.

    Raises:
        Exception: If the email sending fails.
    """

    # Attributes
    apartment = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.full_name")
    resolved_by = serializers.ReadOnlyField(source="assigned_to.full_name")

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Issue): The issue model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
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

    # Method to update the issue
    def update(self, instance: Issue, validated_data: Dict) -> Issue:
        """Update the issue.

        Args:
            instance (Issue): The issue instance.
            validated_data (dict): The validated data.

        Returns:
            Issue: The updated issue.

        Raises:
            Exception: If the email sending fails.
        """

        # Check if the status was resolved
        status_was_resolved = (
            validated_data.get("status") == Issue.IssueStatus.RESOLVED
            and instance.status != Issue.IssueStatus.RESOLVED
        )

        # Update the issue
        instance = super().update(instance, validated_data)

        # If the status was resolved
        if status_was_resolved:
            # Update the resolved on date
            instance.resolved_on = timezone.now().date()

            # Save the issue
            instance.save()

            # Send the resolution email
            send_resolution_email(instance)

        # Return the updated issue
        return instance
