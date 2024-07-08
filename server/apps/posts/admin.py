# Imports
from apps.common.admin import ContentViewInline
from apps.common.models import ContentView
from apps.posts.models import Post, Reply
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from rest_framework.request import Request


class ReplyInline(admin.TabularInline):
    """Reply Inline.

    This class defines the reply inline interface.

    Attributes:
        model: model -- The model.
        extra: int -- The number of extra forms.
    """

    model = Reply
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post Admin.

    This class defines the post admin interface.

    Attributes:
        list_display: list -- The list display fields.
        inlines: list -- The inlines fields.

    Methods:
        get_total_views: Get the total views of the post.
        get_queryset: Get the queryset of the post.
        tag_list: Get the tag list of the post.
    """

    list_display = ["title", "tag_list", "get_total_views"]
    inlines = [ContentViewInline, ReplyInline]

    def get_total_views(self, obj: Post) -> int:
        """Get the total views of the post.

        Arguments:
            obj: Post -- The post object.

        Returns:
            int: The total views of the post.
        """

        content_type = ContentType.objects.get_for_model(obj)

        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        return views

    def get_queryset(self, request: Request) -> QuerySet:
        """Get the queryset of the post.

        Arguments:
            request: Request -- The request object.

        Returns:
            Queryset: The queryset of the post.
        """

        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj: Post) -> str:
        """Get the tag list of the post.

        Arguments:
            obj: Post -- The post object.

        Returns:
            str: The tag list of the post.
        """

        return ", ".join(o.name for o in obj.tags.all())
