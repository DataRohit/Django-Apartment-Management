# Imports
from apps.reports.models import Report
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest


# Register the Report model with the admin panel
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """ReportAdmin

    ReportAdmin class is used to customize the admin panel for the Report model.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        search_fields (list): A list of fields to search by.

    Methods:
        get_queryset: Get the queryset.
        get_report_count: Get the report count.
    """

    # Attributes
    list_display = [
        "title",
        "reported_by",
        "reported_user",
        "get_report_count",
        "created_at",
    ]
    search_fields = [
        "title",
        "reported_by__first_name",
        "reported_user__first_name",
        "reported_user__last_name",
    ]

    # Method to get the queryset
    def get_queryset(self, request: HttpRequest) -> QuerySet[Report]:
        """Get the queryset

        Args:
            request (HttpRequest): The request object.

        Returns:
            QuerySet[Report]: The queryset.
        """

        # Get the queryset
        queryset = super().get_queryset(request)

        # Get the related fields
        queryset = queryset.select_related("reported_user__profile")

        # Return the queryset
        return queryset

    # Method to get the report count
    def get_report_count(self, obj: Report) -> int:
        """Get the report count.

        Args:
            obj (Report): The Report object.

        Returns:
            int: The report count.
        """

        # Return the report count
        return obj.reported_user.profile.report_count

    # Set the short description for the report count
    get_report_count.short_description = "Report Count"
