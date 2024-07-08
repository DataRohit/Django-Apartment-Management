# Imports
from apps.ratings.models import Rating
from django.contrib import admin
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpRequest


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating Admin.

    This class defines the rating admin interface.

    Attributes:
        list_display: list -- The list display fields.
        search_fields: list -- The search fields.
        list_filter: list -- The list filter fields.

    Methods:
        get_queyrset: Get the queryset.
        get_average_rating: Get the average rating.
    """

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

    def get_queryset(self, request: HttpRequest) -> QuerySet[Rating]:
        """Get the queryset.

        This method overrides the default get_queryset method to annotate the average rating.

        Arguments:
            request: HttpRequest -- The request object.

        Returns:
            QuerySet[Rating]: The queryset.
        """

        queryset = super().get_queryset(request)

        queryset = queryset.annotate(
            average_rating=Avg("rated_user__received_ratings__rating")
        )

        return queryset

    def get_average_rating(self, obj: Rating) -> float:
        """Get the average rating.

        This method gets the average rating for the rated user.

        Arguments:
            obj: Rating -- The rating object.

        Returns:
            float: The average rating.
        """

        return round(obj.average_rating, 2) if obj.average_rating is not None else None

    get_average_rating.short_description = "Average Rating"
    get_average_rating.admin_order_field = "average_rating"
