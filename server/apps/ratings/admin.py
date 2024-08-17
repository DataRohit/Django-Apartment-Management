# Imports
from apps.ratings.models import Rating
from django.contrib import admin
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpRequest


# Register the Rating model with the admin panel
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """RatingAdmin

    RatingAdmin class is used to customize the admin panel for the Rating model.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        search_fields (list): A list of fields to search by.
        list_filter (list): A list of fields to filter by.

    Methods:
        get_queryset: Get the queryset.
        get_average_rating: Get the average rating.
    """

    # Attributes
    list_display = [
        "rating_user",
        "rated_user",
        "rating",
        "comment",
        "get_average_rating",
    ]
    search_fields = [
        "rating_user__username",
        "rated_user__username",
    ]
    list_filter = ["rating", "created_at"]

    # Method to get the queryset
    def get_queryset(self, request: HttpRequest) -> QuerySet[Rating]:
        """Get the queryset.

        Args:
            request (HttpRequest): The request object.

        Returns:
            QuerySet[Rating]: The queryset.
        """

        # Get the queryset
        queryset = super().get_queryset(request)

        # Annotate the queryset with the average rating
        queryset = queryset.annotate(
            average_rating=Avg("rated_user__received_ratings__rating")
        )

        # Return the queryset
        return queryset

    # Method to get the average rating
    def get_average_rating(self, obj: Rating) -> float:
        """Get the average rating.

        Args:
            obj (Rating): The rating object.

        Returns:
            float: The average rating.
        """

        # Return the average rating
        return round(obj.average_rating, 2) if obj.average_rating is not None else None

    # Set the short description for the average rating
    get_average_rating.short_description = "Average Rating"
    get_average_rating.admin_order_field = "average_rating"
