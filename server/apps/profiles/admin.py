# Imports
from apps.profiles.models import Profile
from django.contrib import admin


# Register the Profile model with the Django admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ProfileAdmin

    ProfileAdmin class is used to customize the admin panel for the Profile model.

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        list_display_links (list): A list of fields to link to the detail page.
        list_filter (list): A list of fields to filter by.
    """

    # Attributes
    list_display = ["id", "user", "gender", "occupation", "slug"]
    list_display_links = ["id", "user"]
    list_filter = ["occupation"]
