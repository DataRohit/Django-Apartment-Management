# Imports
from apps.common.models import ContentView
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


# Register the Content View model
@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    """Content View Admin

    This class defines the content view admin interface.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): The list of display fields.
    """

    # Attributes
    list_display = ["content_type", "user", "viewer_ip", "created_at"]


# Content View Inline
class ContentViewInline(GenericTabularInline):
    """Content View Inline

    This class defines the content view inline interface.

    Extends:
        GenericTabularInline

    Attributes:
        model (ContentView): The content view model.
        extra (int): The number of extra fields.
        readonly_fields (list): The list of read-only fields.
    """

    # Attributes
    model = ContentView
    extra = 0
    readonly_fields = ["user", "viewer_ip", "created_at"]
