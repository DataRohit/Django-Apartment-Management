# Imports
from django.contrib import admin
from apps.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin.

    This class is used to customize the Django admin for the Profile model.

    Attributes:
        list_display: list -- The fields to display in the Django admin.
        list_display_links: list -- The fields to link to the Profile detail page.
        list_filter: list -- The fields to filter the Profile list.
    """

    list_display = ["id", "user", "gender", "occupation", "slug"]
    list_display_links = ["id", "user"]
    list_filter = ["occupation"]
