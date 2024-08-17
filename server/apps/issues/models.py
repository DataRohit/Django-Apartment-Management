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


# Issue Model
class Issue(TimeStampedModel):
    """Issue

    Issue class is used to represent an issue in the database.

    Extends:
        TimeStampedModel

    Attributes:
        apartment (ForeignKey): The apartment the issue belongs to.
        reported_by (ForeignKey): The user who reported the issue.
        assigned_to (ForeignKey): The user assigned to the issue.
        title (str): The title of the issue.
        description (str): The description of the issue.
        status (str): The status of the issue.
        priority (str): The priority of the issue.
        resolved_on (Date): The date when the issue was resolved.

    Methods:
        __str__(): Return the string representation of the issue.
        save(*args, **kwargs): Save the issue and notify the assigned user.
        notify_assigned_user(): Notify the assigned user.

    Constants:
        IssueStatus: The status of the issue.
        Priority: The priority of the issue.
    """

    # Constants for the issue status
    class IssueStatus(models.TextChoices):
        REPORTED = ("reported", _("Reported"))
        RESOLVED = ("resolved", _("Resolved"))
        IN_PROGRESS = ("in_progress", _("In Progress"))

    # Constants for the issue priority
    class Priority(models.TextChoices):
        LOW = ("low", _("Low"))
        MEDIUM = ("medium", _("Medium"))
        HIGH = ("high", _("High"))

    # Attributes
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

    # String Representation
    def __str__(self) -> str:
        """Return the string representation of the issue.

        Returns:
            str: The string representation of the issue.
        """

        # Return the title
        return self.title

    # Save Method
    def save(self, *args: Dict, **kwargs: Dict) -> None:
        """Save the issue and notify the assigned user.

        Args:
            *args (dict): The arguments.
            **kwargs (dict): The keyword arguments.

        Raises:
            Exception: If the email sending fails.
        """

        # Check if the issue is existing
        is_existing = self.pk is not None

        # Get the old assigned user
        old_assigned_to = None

        # If the issue is existing
        if is_existing:
            # Get the old issue
            old_issue = Issue.objects.get(pk=self.pk)

            # Update the old assigned user
            old_assigned_to = old_issue.assigned_to

        # Save the issue
        super().save(*args, **kwargs)

        # If the issue is existing and the assigned user has changed
        if (
            is_existing
            and old_assigned_to != self.assigned_to
            and self.assigned_to is not None
        ):
            # Send the notification
            self.notify_assigned_user()

    # Notify Assigned User Method
    def notify_assigned_user(self) -> None:
        """Notify the assigned user.

        Raises:
            Exception: If the email sending fails.
        """

        # Try
        try:
            # Set the subject, from email, and recipient list
            subject = f"New Issue Assigned: {self.title}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.assigned_to.email]

            # Set the context
            context = {
                "issue": self,
                "site_name": settings.SITE_NAME,
            }

            # Set the HTML and text email
            html_email = render_to_string(
                "issues/issue_assignment_notification_email.html", context
            )
            text_email = strip_tags(html_email)

            # Create the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_email,
                from_email=from_email,
                to=recipient_list,
            )
            email.attach_alternative(html_email, "text/html")

            # Send the email
            email.send()

        # Except
        except Exception as e:
            # Log the error
            logger.error(
                f"Failed to send issue assignment email for issue '{self.title}': {e}"
            )
