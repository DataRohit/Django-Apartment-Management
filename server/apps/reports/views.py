# Imports
from apps.common.renderers import GenericJSONRenderer
from apps.reports.models import Report
from apps.reports.serializers import ReportListSerializer, ReportSerializer
from rest_framework import generics, serializers


class ReportCreateAPIView(generics.CreateAPIView):
    """Report create view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset: QuerySet -- The query set.
        serializer_class: ReportSerializer -- The report serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        perform_create: Method to perform the create.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "report"

    def perform_create(self, serializer: ReportSerializer) -> None:
        """Method to perform the create.

        This method saves the report and sets the reported_by field to the current user.

        Arguments:
            serializer: ReportSerializer -- The report serializer.
        """

        if (
            self.request.user.username
            == serializer.validated_data["reported_user_username"]
        ):
            raise serializers.ValidationError(
                {"reported_user_username": "You cannot report yourself."}
            )

        serializer.save(reported_by=self.request.user)


class ReportListAPIView(generics.ListAPIView):
    """Report list view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: ReportSerializer -- The report serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = ReportListSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "report"

    def get_queryset(self) -> Report:
        """Method to get the queryset.

        This method returns the reports reported by the current user.

        Returns:
            Report: The reports reported by the current user.
        """

        user = self.request.user
        return Report.objects.filter(reported_by=user)
