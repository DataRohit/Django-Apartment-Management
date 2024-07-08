# Imports
from apps.common.models import TimeStampedModel
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Get the user model
User = get_user_model()


class Report(TimeStampedModel):
    """Report Model.

    This class defines the report model.

    Attributes:
        title: models.CharField -- The title.
        slug: AutoSlugField -- The slug.
        reported_by: models.ForeignKey -- The user who made the report.
        reported_user: models.ForeignKey -- The user who is reported.
        description: models.TextField -- The description.

    Methods:
        __str__: str -- Returns the string representation of the report.

    Meta:
        verbose_name: str -- Sets the human-readable name for the model in the Django admin.
        verbose_name_plural: str -- Sets the human-readable plural name for the model in the Django admin.
        ordering: list -- Sets the default ordering for the model.
    """

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_made",
        verbose_name=_("Reported by"),
    )
    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received",
        verbose_name=_("Reported user"),
    )
    description = models.TextField(verbose_name=_("Description"))

    def __str__(self) -> str:
        """String Representation.

        Returns:
            str: The string representation of the report.
        """

        return f"Report by {self.reported_by.full_name} against {self.reported_user.full_name}"

    class Meta:
        """Meta Class.

        This class defines the meta options for the report model.

        Attributes:
            verbose_name: str -- Sets the human-readable name for the model in the Django admin.
            verbose_name_plural: str -- Sets the human-readable plural name for the model in the Django admin.
            ordering: list -- Sets the default ordering for the model.
        """

        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ["-created_at"]
