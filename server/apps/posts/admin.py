# Imports
from apps.common.admin import ContentViewInline
from apps.common.models import ContentView
from apps.posts.models import Post, Reply
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from rest_framework.request import Request


# Reply Inline
class ReplyInline(admin.TabularInline):
    """ReplyInline

    ReplyInline class is used to customize the admin panel for the Reply model.

    Extends:
        admin.TabularInline

    Attributes:
        model (Reply): The Reply model.
        extra (int): The number of extra forms to display.
    """

    # Attributes
    model = Reply
    extra = 1


# Register the Post model with the admin panel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """PostAdmin

    PostAdmin class is used to customize the admin panel for the Post model.

    Extends:
        admin.ModelAdmin

    Attributes:
        list_display (list): A list of fields to display in the admin panel.
        inlines (list): A list of inline classes to include.

    Methods:
        get_total_views: Get the total
        get_queryset: Get the queryset.
        tag_list: Get the tag list.
    """

    # Attributes
    list_display = ["title", "tag_list", "get_total_views"]
    inlines = [ContentViewInline, ReplyInline]

    # Methods
    def get_total_views(self, obj: Post) -> int:
        """Get the total views.

        Args:
            obj (Post): The Post object.

        Returns:
            int: The total number of views.
        """

        # Get the content type
        content_type = ContentType.objects.get_for_model(obj)

        # Get the views
        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

        # Return the views
        return views

    # Get the queryset
    def get_queryset(self, request: Request) -> QuerySet:
        """Get the queryset.

        Args:
            request (Request): The request.

        Returns:
            QuerySet: The queryset.
        """

        # Return the queryset
        return super().get_queryset(request).prefetch_related("tags")

    # Get the tag list
    def tag_list(self, obj: Post) -> str:
        """Get the tag list.

        Args:
            obj (Post): The Post object.

        Returns:
            str: The tag list.
        """

        # Return the tag list
        return ", ".join(o.name for o in obj.tags.all())
