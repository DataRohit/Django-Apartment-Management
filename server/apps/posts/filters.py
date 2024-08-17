# Imports
import django_filters
from apps.posts.models import Post
from django.db.models import Count
from django.db.models.query import QuerySet
from taggit.models import Tag


# PostFilter Class
class PostFilter(django_filters.FilterSet):
    """PostFilter

    PostFilter class is used to filter the Post model.

    Extends:
        django_filters.FilterSet

    Attributes:
        tags (django_filters.ModelMultipleChoiceFilter): The tags.
        author_username (django_filters.CharFilter): The author's username.
        most_replied_to (django_filters.BooleanFilter): The most replied to.
        ordering (django_filters.OrderingFilter): The ordering.

    Methods:
        filter_most_replied_to: Filter the most replied to.

    Meta Class:
        model (Post): The Post model.
        fields (list): The fields to filter
    """

    # Attributes
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__name",
        to_field_name="name",
        queryset=Tag.objects.all(),
        lookup_expr="icontains",
    )
    author_username = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )
    most_replied_to = django_filters.BooleanFilter(method="filter_most_replied_to")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "oldest"),
            ("-created_at", "most_recent"),
            ("-replies_count", "most_replied_to"),
        )
    )

    # Methods
    def filter_most_replied_to(
        self, queryset: QuerySet, name: str, value: bool
    ) -> QuerySet:
        """Filter the most replied to.

        Args:
            queryset (QuerySet): The queryset.
            name (str): The name of the filter.
            value (bool): The value of the filter.

        Returns:
            QuerySet: The filtered queryset.
        """

        # Filter the most replied to
        if value:
            # Return the queryset
            return queryset.annotate(reply_count=Count("replies")).filter(
                reply_count__gt=0
            )

        # Return the queryset
        return queryset

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Post): The Post model.
            fields (list): The fields to filter.
        """

        # Attributes
        model = Post
        fields = ["tags", "author_username", "most_replied_to", "ordering"]
