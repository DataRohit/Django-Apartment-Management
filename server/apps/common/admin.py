# Imports
from apps.common.models import ContentView
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    """Content View Admin.

    This class defines the content view admin interface.

    Attributes:
        list_display: list -- The list display fields.
    """

    list_display = ["content_type", "user", "viewer_ip", "created_at"]


class ContentViewInline(GenericTabularInline):
    """Content View Inline.

    This class defines the content view inline interface.

    Attributes:
        model: ContentView -- The content view model.
        extra: int -- The number of extra forms to display.
        readonly_fields: list -- The read-only fields.
    """

    model = ContentView
    extra = 0
    readonly_fields = ["user", "viewer_ip", "created_at"]
