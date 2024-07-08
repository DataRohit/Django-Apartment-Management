# Imports
from apps.common.admin import ContentViewInline
from apps.common.models import ContentView
from apps.issues.models import Issue
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Issue Admin.

    This class defines the issue admin interface.

    Attributes:
        list_display: list -- The list display fields.
        list_display_links: list -- The list display links.
        list_filter: list -- The list filter fields.
        search_fields: list -- The search fields.
        ordering: list -- The ordering fields.
        autocomplete_fields: list -- The autocomplete fields.
        inlines: list -- The inlines.

    Methods:
        get_total_views: Get the total views.
    """

    list_display = (
        "id",
        "apartment",
        "reported_by",
        "assigned_to",
        "status",
        "priority",
        "get_total_views",
    )
    list_display_links = ("id", "apartment")
    list_filter = ("status", "priority")
    search_fields = (
        "apartment__unit_number",
        "reported_by__first_name",
        "assigned_to__first_name",
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("apartment", "reported_by", "assigned_to")
    inlines = (ContentViewInline,)

    def get_total_views(self, obj: Issue) -> int:
        """Get the total views.

        This method gets the total views for the issue.

        Arguments:
            obj: Issue -- The issue object.

        Returns:
            int: The total views.
        """

        content_type = ContentType.objects.get_for_model(obj)

        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        return views

    get_total_views.short_description = "Total Views"
