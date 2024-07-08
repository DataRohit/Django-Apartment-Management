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


class Post(TimeStampedModel):
    """Post Model.

    This class defines the post model.

    Attributes:
        title: models.CharField -- The title.
        slug: AutoSlugField -- The slug.
        body: models.TextField -- The body.
        tags: TaggableManager -- The tags.
        author: models.ForeignKey {User} -- The author.
        bookmarked_by: models.ManyToManyField {User} -- The users who bookmarked the post.
        upvotes: models.PositiveIntegerField -- The upvotes.
        upvoted_by: models.ManyToManyField {User} -- The users who upvoted the post.
        downvotes: models.PositiveIntegerField -- The downvotes.
        downvoted_by: models.ManyToManyField {User} -- The users who downvoted the post.
        content_views: GenericRelation {ContentView} -- The content views.

    Methods:
        __str__: Returns the string representation of the post.
        get_popular_tags: Gets the popular tags.
        save: Saves the model.

    Meta:
        verbose_name: str -- The verbose name.
        verbose_name_plural: str -- The verbose name in plural.
    """

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

    def __str__(self) -> str:
        """String Representation.

        Returns:
            str: The string representation of the post.
        """

        return self.title

    @classmethod
    def get_popular_tags(cls, limit=5) -> QuerySet:
        """Get popular tags.

        This method gets the popular tags.

        Arguments:
            limit: int -- The limit.

        Returns:
            QuerySet: The popular tags.
        """

        return cls.tags.annotate(post_count=Count("taggit_taggeditem_items")).order_by(
            "-post_count"
        )[:limit]

    def save(self, *args, **kwargs) -> None:
        """Save Method.

        This method saves the model.

        Raises:
            ValueError: If the author is not a superuser, staffuser or tenant.
        """

        if not (
            self.author.is_superuser
            or self.author.is_staff
            or self.author.profile.occupation == Profile.Occupation.TENANT
        ):
            raise ValueError(
                _("Only superusers, staffusers and tenants can create posts")
            )

        super().save(*args, **kwargs)

    class Meta:
        """Meta Class.

        This class defines the meta options for the post model.

        Attributes:
            verbose_name: str -- The verbose name.
            verbose_name_plural: str -- The verbose name in plural.
        """

        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class Reply(TimeStampedModel):
    """Reply Model.

    This class defines the reply model.

    Attributes:
        post: models.ForeignKey {Post} -- The post.
        author: models.ForeignKey {User} -- The author.
        body: models.TextField -- The body.

    Methods:
        __str__: Returns the string representation of the reply.

    Meta:
        verbose_name: str -- The verbose name.
        verbose_name_plural: str -- The verbose name in plural.
    """

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

    def __str__(self) -> str:
        """String Representation.

        Returns:
            str: The string representation of the reply.
        """

        return f"Reply by {self.author.full_name} on {self.post.title}"

    class Meta:
        """Meta Class.

        This class defines the meta options for the reply model.

        Attributes:
            verbose_name: str -- The verbose name.
            verbose_name_plural: str -- The verbose name in plural.
        """

        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
