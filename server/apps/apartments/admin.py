# Imports
from apps.apartments.models import Apartment
from django.contrib import admin


# Register the Apartment model with the admin panel
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """ApartmentAdmin

    ApartmentAdmin class is used to customize the admin panel for the Apartment model.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        list_display_links (list): A list of fields to link to the detail page.
        list_filter (list): A list of fields to filter by.
        search_fields (list): A list of fields to search by.
        ordering (list): A list of fields to order by.
        autocomplete_fields (list): A list of fields to autocomplete.
    """

    # Attributes
    list_display = ["id", "unit_number", "building", "floor", "tenant"]
    list_display_links = ["id", "unit_number"]
    list_filter = ["building", "floor"]
    search_fields = ["unit_number", "building", "floor"]
    ordering = ["building", "floor"]
    autocomplete_fields = ["tenant"]
