# Imports
from apps.reports.models import Report
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report Admin.

    This class defines the report admin interface.

    Attributes:
        list_display: list -- The list display fields.
        search_fields: list -- The search fields.

    Methods:
        get_queryset: Get the queryset.
        get_report_count: Get the report count.
    """

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

    def get_queryset(self, request: HttpRequest) -> QuerySet[Report]:
        """Get the queryset.

        This method overrides the default get_queryset method to select related fields.

        Arguments:
            request: HttpRequest -- The request object.

        Returns:
            QuerySet[Report]: The queryset.
        """

        queryset = super().get_queryset(request)
        queryset = queryset.select_related("reported_user__profile")
        return queryset

    def get_report_count(self, obj: Report) -> int:
        """Get the report count.

        This method gets the report count for the reported user.

        Arguments:
            obj: Report -- The report object.

        Returns:
            int: The report count.
        """

        return obj.reported_user.profile.report_count

    get_report_count.short_description = "Report Count"
