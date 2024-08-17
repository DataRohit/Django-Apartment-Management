# Imports
from apps.common.admin import ContentViewInline
from apps.common.models import ContentView
from apps.issues.models import Issue
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


# Register the Issue model with the admin panel
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """IssueAdmin

    IssueAdmin class is used to customize the admin panel for the Issue model.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        list_display_links (list): A list of fields to link to the detail page.
        list_filter (list): A list of fields to filter by.
        search_fields (list): A list of fields to search by.
        ordering (list): A list of fields to order by.
        autocomplete_fields (list): A list of fields to autocomplete.
        inlines (list): A list of inline classes to include.

    Methods:
        get_total_views: Get the total views.
    """

    # Attributes
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

    # Method to get the total views
    def get_total_views(self, obj: Issue) -> int:
        """Get the total views.

        Args:
            obj (Issue): The Issue object.

        Returns:
            int: The total number of views.
        """

        # Get the content type
        content_type = ContentType.objects.get_for_model(obj)

        # Get the total views
        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        # Return the total views
        return views

    # Set the short description for the total views
    get_total_views.short_description = "Total Views"
