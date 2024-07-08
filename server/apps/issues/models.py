# Imports
import logging
from typing import Dict
from apps.apartments.models import Apartment
from apps.common.models import TimeStampedModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


# Get the user model
User = get_user_model()


# Get the logger
logger = logging.getLogger(__name__)


class Issue(TimeStampedModel):
    """Issue Model

    This model is used to store the issues reported by the users.

    Extends:
        TimeStampedModel

    Attributes:
        IssueStatus: TextChoices -- Choices for the issue status
        Priority: TextChoices -- Choices for the issue priority

        apartment: Apartment {ForeignKey} -- The apartment
        reported_by: User {ForeignKey} -- The user who reported the issue
        assigned_to: User {ForeignKey} -- The user assigned to resolve the issue
        title: str -- The character field for the issue title
        description: text -- The text field for the issue description
        status: str -- The character field for the issue status
        priority: str -- The character field for the issue priority
        resolved_on: date -- The date field for the issue resolved date

    Methods:
        __str__:  String representation
        save: Save the issue and notify the assigned user
        notify_assigned_user: Notify the assigned user
    """

    class IssueStatus(models.TextChoices):
        REPORTED = ("reported", _("Reported"))
        RESOLVED = ("resolved", _("Resolved"))
        IN_PROGRESS = ("in_progress", _("In Progress"))

    class Priority(models.TextChoices):
        LOW = ("low", _("Low"))
        MEDIUM = ("medium", _("Medium"))
        HIGH = ("high", _("High"))

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="issues",
        verbose_name=_("Apartment"),
    )
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reported_by_issues",
        verbose_name=_("Reported By"),
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_to_issues",
        verbose_name=_("Assigned To"),
    )
    title = models.CharField(_("Issue Title"), max_length=255)
    description = models.TextField(_("Issue Description"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=IssueStatus.choices,
        default=IssueStatus.REPORTED,
    )
    priority = models.CharField(
        _("Priority"),
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    resolved_on = models.DateField(_("Resolved On"), null=True, blank=True)

    def __str__(self) -> str:
        """String representation

        Returns:
            str: The issue title
        """

        return self.title

    def save(self, *args: Dict, **kwargs: Dict) -> None:
        """Save the issue and notify the assigned user

        This method is used to save the issue and notify the assigned user.

        Arguments:
            *args: dict -- The arguments
            **kwargs: dict -- The keyword arguments
        """

        is_existing = self.pk is not None

        old_assigned_to = None

        if is_existing:
            old_issue = Issue.objects.get(pk=self.pk)
            old_assigned_to = old_issue.assigned_to

        super().save(*args, **kwargs)

        if (
            is_existing
            and old_assigned_to != self.assigned_to
            and self.assigned_to is not None
        ):
            self.notify_assigned_user()

    def notify_assigned_user(self) -> None:
        """Notify the assigned user

        This method is used to notify the assigned user.

        Raises:
            Exception: If the email sending fails.
        """

        try:
            subject = f"New Issue Assigned: {self.title}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.assigned_to.email]

            context = {
                "issue": self,
                "site_name": settings.SITE_NAME,
            }

            html_email = render_to_string(
                "issues/issue_assignment_notification_email.html", context
            )
            text_email = strip_tags(html_email)

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_email,
                from_email=from_email,
                to=recipient_list,
            )
            email.attach_alternative(html_email, "text/html")

            email.send()

        except Exception as e:
            logger.error(
                f"Failed to send issue assignment email for issue '{self.title}': {e}"
            )
