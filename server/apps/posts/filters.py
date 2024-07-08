# Imports
import django_filters
from apps.posts.models import Post
from django.db.models import Count
from django.db.models.query import QuerySet
from taggit.models import Tag


class PostFilter(django_filters.FilterSet):
    """Post Filter.

    This class defines the post filter.

    Attributes:
        tags: django_filters.ModelMultipleChoiceFilter -- The tags.
        author_username: django_filters.CharFilter -- The author's username.
        most_replied_to: django_filters.BooleanFilter -- The most replied to.
        ordering: django_filters.OrderingFilter -- The ordering.

    Methods:
        filter_most_replied_to: Filters the most replied to.

    Meta:
        model: Post -- The model.
        fields: list -- The fields.
    """

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

    def filter_most_replied_to(
        self, queryset: QuerySet, name: str, value: bool
    ) -> QuerySet:
        """Filters the most replied to.

        Arguments:
            queryset: QuerySet -- The queryset.
            name: str -- The name.
            value: bool -- The value.

        Returns:
            QuerySet: The queryset.
        """

        if value:
            return queryset.annotate(reply_count=Count("replies")).filter(
                reply_count__gt=0
            )

        return queryset

    class Meta:
        """Meta Class.

        This class defines the meta options for the post filter.

        Attributes:
            model: Post -- The model.
            fields: list -- The fields.
        """

        model = Post
        fields = ["tags", "author_username", "most_replied_to", "ordering"]
