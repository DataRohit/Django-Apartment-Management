# Imports
from apps.common.renderers import GenericJSONRenderer
from apps.reports.models import Report
from apps.reports.serializers import ReportListSerializer, ReportSerializer
from rest_framework import generics, serializers


# ReportCreateAPIView Class
class ReportCreateAPIView(generics.CreateAPIView):
    """ReportCreateAPIView

    ReportCreateAPIView class is used to create a report.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset (Report): The queryset of reports.
        serializer_class (ReportSerializer): The report serializer.
        renderer_classes (tuple): The tuple of renderer classes.
        object_label (str): The object label.

    Methods:
        perform_create(serializer: ReportSerializer) -> None: Perform the creation of a report.

    Raises:
        serializers.ValidationError: If the user tries to report themselves.
    """

    # Attributes
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "report"

    # Method to perform the creation of a report
    def perform_create(self, serializer: ReportSerializer) -> None:
        """Perform the creation of a report.

        Args:
            serializer (ReportSerializer): The report serializer.

        Raises:
            serializers.ValidationError: If the user tries to report themselves.
        """

        # If the user tries to report themselves
        if (
            self.request.user.username
            == serializer.validated_data["reported_user_username"]
        ):
            # Raise a validation error
            raise serializers.ValidationError(
                {"reported_user_username": "You cannot report yourself."}
            )

        # Save the report
        serializer.save(reported_by=self.request.user)


# ReportListAPIView Class
class ReportListAPIView(generics.ListAPIView):
    """ReportListAPIView

    ReportListAPIView class is used to list reports.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class (ReportListSerializer): The report list serializer.
        renderer_classes (tuple): The tuple of renderer classes.
        object_label (str): The object label.

    Methods:
        get_queryset() -> Report: Get the queryset of reports.
    """

    # Attributes
    serializer_class = ReportListSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "report"

    # Method to get the queryset of reports
    def get_queryset(self) -> Report:
        """Get the queryset of reports.

        Returns:
            Report: The queryset of reports.
        """

        # Get the user
        user = self.request.user

        # Return the reports reported by the user
        return Report.objects.filter(reported_by=user)
