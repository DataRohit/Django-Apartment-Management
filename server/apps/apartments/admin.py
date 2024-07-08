# Imports
from apps.apartments.models import Apartment
from django.contrib import admin


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """Apartment Admin.

    This class defines the apartment admin interface.

    Attributes:
        list_display: list -- The list display fields.
        list_display_links: list -- The list display links.
        list_filter: list -- The list filter fields.
        search_fields: list -- The search fields.
        ordering: list -- The default ordering.
        autocomplete_fields: list -- The autocomplete fields.
    """

    list_display = ["id", "unit_number", "building", "floor", "tenant"]
    list_display_links = ["id", "unit_number"]
    list_filter = ["building", "floor"]
    search_fields = ["unit_number", "building", "floor"]
    ordering = ["building", "floor"]
    autocomplete_fields = ["tenant"]
