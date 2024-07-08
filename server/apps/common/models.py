# Imports
import uuid
from typing import Optional
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _


# Get the user model
User = get_user_model()


# TimeStampedModel
class TimeStampedModel(models.Model):
    """Time-stamped model.

    This class provides the fields to store the creation and update timestamps.

    Extends:
        models.Model

    Attributes:
        pkid: models.BigAutoField -- The primary key.
        id: models.UUIDField -- The UUID of the record.
        created_at: models.DateTimeField -- The timestamp when the record was created.
        updated_at: models.DateTimeField -- The timestamp when the record was last updated.

    Meta:
        abstract: bool -- Whether the model is abstract or not.
        ordering: list -- The default ordering.
    """

    pkid = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        """Meta Class.

        Attributes:
            abstract: bool -- Whether the model is abstract or not.
            ordering: list -- The default ordering.
        """

        abstract = True
        ordering = ["-created_at", "-updated_at"]


class ContentView(TimeStampedModel):
    """Content View.

    This class stores the count of views that a content is inheriting from.

    Attributes:
        content_type: models.ForeignKey -- The content type of the object.
        object_id: models.PositiveIntegerField -- The object ID.
        content_object: GenericForeignKey -- The object itself.
        user: models.ForeignKey -- The user who viewed the content.
        viewer_ip: models.GenericIPAddressField -- The IP address of the viewer.
        last_viewed: models.DateTimeField -- The timestamp when the content was last viewed.

    Meta:
        verbose_name: str -- The human-readable name of the model.
        verbose_name_plural: str -- The human-readable plural name of the model.
        unique_together: list -- The unique constraints of the model.
        ordering: list -- The default ordering.

    Methods:
        __str__: Return the string representation of the model.
        record_view: Record a view of the content.
    """

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="content_views",
        verbose_name=_("User"),
    )
    viewer_ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_("Viewer IP")
    )
    last_viewed = models.DateTimeField(auto_now=True, verbose_name=_("Last Viewed At"))

    class Meta:
        """Meta Class.

        Attributes:
            verbose_name: str -- The human-readable name of the model.
            verbose_name_plural: str -- The human-readable plural name of the model.
            unique_together: list -- The unique constraints of the model.
            ordering: list -- The default ordering.
        """

        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        unique_together = ["content_type", "object_id", "user", "viewer_ip"]
        ordering = ["-last_viewed"]

    def __str__(self) -> str:
        """Return the string representation of the model.

        Returns:
            str: The string representation of the model.
        """

        return (
            f"{self.content_object} viewed by {self.user.full_name or self.viewer_ip}"
        )

    @classmethod
    def record_view(
        cls,
        content_object,
        user: Optional[User] = None,  # type: ignore
        viewer_ip: Optional[str] = None,
    ) -> None:
        """Record a view of the content.

        Arguments:
            content_object: object -- The content object.
            user: User -- The user who viewed the content.
            viewer_ip: str -- The IP address of the viewer.

        Raises:
            IntegrityError: If the view already exists.
        """

        content_type = ContentType.objects.get_for_model(content_object)

        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.pk,
                user=user,
                defaults={"user": user, "viewer_ip": viewer_ip},
            )
            if not created:
                view.last_viewed = view.last_viewed
                view.save()
        except IntegrityError:
            pass
