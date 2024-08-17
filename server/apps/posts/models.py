# Imports
from apps.common.models import ContentView, TimeStampedModel
from apps.profiles.models import Profile
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

# Get the user model
User = get_user_model()


# Post Model
class Post(TimeStampedModel):
    """Post

    Post class is used to represent a post in the database.

    Extends:
        TimeStampedModel

    Attributes:
        title (str): The title of the post.
        slug (AutoSlugField): The slug of the post.
        body (str): The body of the post.
        tags (TaggableManager): The tags of the post.
        author (ForeignKey): The author of the post.
        bookmarked_by (ManyToManyField): The users who bookmarked the post.
        upvotes (PositiveIntegerField): The number of upvotes the post has.
        upvoted_by (ManyToManyField): The users who upvoted the post.
        downvotes (PositiveIntegerField): The number of downvotes the post has.
        downvoted_by (ManyToManyField): The users who downvoted the post.
        content_views (GenericRelation): The content views of the post.

    Methods:
        get_popular_tags(cls, limit=5) -> QuerySet: Get the popular tags.

    Meta Class:
        verbose_name (str): The verbose name of the post.
        verbose_name_plural (str): The plural verbose name of the post.
    """

    # Attributes
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = AutoSlugField(
        populate_from="title", unique=True, verbose_name=_("Slug"), always_update=True
    )
    body = models.TextField(verbose_name=_("Body"))
    tags = TaggableManager(verbose_name=_("Tags"))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Author"),
    )
    bookmarked_by = models.ManyToManyField(
        User,
        related_name="bookmarked_posts",
        verbose_name=_("Bookmarked by"),
        blank=True,
    )
    upvotes = models.PositiveIntegerField(default=0, verbose_name=_("Upvotes"))
    upvoted_by = models.ManyToManyField(
        User,
        related_name="upvoted_posts",
        verbose_name=_("Upvoted by"),
        blank=True,
    )
    downvotes = models.PositiveIntegerField(default=0, verbose_name=_("Downvotes"))
    downvoted_by = models.ManyToManyField(
        User,
        related_name="downvoted_posts",
        verbose_name=_("Downvoted by"),
        blank=True,
    )
    content_views = GenericRelation(ContentView, related_query_name="posts")

    # String representation
    def __str__(self) -> str:
        """Return the string representation of the post.

        Returns:
            str: The title of the post.
        """

        # Return the title
        return self.title

    # Get the popular tags
    @classmethod
    def get_popular_tags(cls, limit=5) -> QuerySet:
        """Get the popular tags.

        Args:
            limit (int): The limit.

        Returns:
            QuerySet: The popular tags.
        """

        # Return the popular tags
        return cls.tags.annotate(post_count=Count("taggit_taggeditem_items")).order_by(
            "-post_count"
        )[:limit]

    # Save Method
    def save(self, *args, **kwargs) -> None:
        """Save the post.

        Raises:
            ValueError: If the author is not a superuser, staffuser or tenant.
        """

        # If the author is not a superuser, staffuser or tenant
        if not (
            self.author.is_superuser
            or self.author.is_staff
            or self.author.profile.occupation == Profile.Occupation.TENANT
        ):
            # Raise a value error
            raise ValueError(
                _("Only superusers, staffusers and tenants can create posts")
            )

        # Save the post
        super().save(*args, **kwargs)

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            verbose_name (str): The verbose name of the post.
            verbose_name_plural (str): The plural verbose name of the post.
        """

        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


# Reply Model
class Reply(TimeStampedModel):
    """Reply

    Reply class is used to represent a reply in the database.

    Extends:
        TimeStampedModel

    Attributes:
        post (ForeignKey): The post.
        author (ForeignKey): The author of the reply.
        body (TextField): The body of the reply.

    Methods:
        __str__(): Return the string representation of the reply.

    Meta Class:
        verbose_name (str): The verbose name of the reply.
        verbose_name_plural (str): The plural verbose name of the reply.
    """

    # Attributes
    post = models.ForeignKey(
        Post, verbose_name=_("Post"), on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Author"),
    )
    body = models.TextField(verbose_name=_("Reply"))

    # String representation
    def __str__(self) -> str:
        """Return the string representation of the reply.

        Returns:
            str: The string representation of the reply.
        """

        # Return the string representation
        return f"Reply by {self.author.full_name} on {self.post.title}"

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            verbose_name (str): The verbose name of the reply.
            verbose_name_plural (str): The plural verbose name of the reply.
        """

        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
