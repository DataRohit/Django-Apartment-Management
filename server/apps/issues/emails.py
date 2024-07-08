# Imports
import logging
from apps.issues.models import Issue
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Get the logger
logger = logging.getLogger(__name__)


def send_issue_confirmation_email(issue: Issue) -> None:
    """Send an email to the user who reported the issue.

    Arguments:
        issue: Issue -- The issue that was reported.

    Raises:
        Exception: If there was an error sending the email.
    """

    try:
        subject = "Issue Report Confirmation"
        context = {"issue": issue, "site_name": settings.SITE_NAME}

        html_email = render_to_string("issues/issue_confirmation_email.html", context)
        text_email = strip_tags(html_email)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = [issue.reported_by.email]

        email = EmailMultiAlternatives(subject, text_email, from_email, to)
        email.attach_alternative(html_email, "text/html")

        email.send()

    except Exception as e:
        logger.error(
            f"Failed to send confirmation email for issue '{issue.title}':{e}",
            exc_info=True,
        )


def send_issue_resolved_email(issue: Issue) -> None:
    """Send an email to the user who reported the issue.

    Arguments:
        issue: Issue -- The issue that was resolved.

    Raises:
        Exception: If there was an error sending the email.
    """

    try:
        subject = "Issue Resolved"
        context = {"issue": issue, "site_name": settings.SITE_NAME}

        html_email = render_to_string(
            "issues/issue_resolved_notification_email.html", context
        )
        text_email = strip_tags(html_email)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = [issue.reported_by.email]

        email = EmailMultiAlternatives(subject, text_email, from_email, to)
        email.attach_alternative(html_email, "text/html")

        email.send()

    except Exception as e:
        logger.error(
            f"Failed to send resolution email for issue '{issue.title}':{e}",
            exc_info=True,
        )


def send_resolution_email(issue: Issue) -> None:
    """Send an email to the user who reported the issue.

    Arguments:
        issue: Issue -- The issue that was resolved.

    Raises:
        Exception: If there was an error sending the email.
    """

    try:
        subject = f"Issue Resolved: {issue.title}"
        context = {"issue": issue, "site_name": settings.SITE_NAME}

        html_email = render_to_string(
            "issues/issue_resolved_notification_email.html", context
        )
        text_email = strip_tags(html_email)

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [issue.reported_by.email]

        email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
        email.attach_alternative(html_email, "text/html")

        email.send()

    except Exception as e:
        logger.error(
            f"Failed to send resolution email for issue '{issue.title}':{e}",
            exc_info=True,
        )
