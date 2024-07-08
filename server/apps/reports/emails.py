# Imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Get the user model
User = get_user_model()


def send_warning_email(user: User, title: str, description: str) -> None:  # type: ignore
    """Send a warning email to the user.

    Arguments:
        user: User -- The user to send the email to.
        title: str -- The title of the warning.
        description: str -- The description of the warning.
    """

    subject = f"Warning: {user.full_name} You have been reported!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    context = {
        "user": user,
        "title": title,
        "description": description,
        "site_name": settings.SITE_NAME,
    }

    html_email = render_to_string("reports/warning_email.html", context)
    text_email = strip_tags(html_email)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_email,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_email, "text/html")

    email.send()


def send_deactivation_email(user: User, title: str, description: str) -> None:  # type: ignore
    """Send a deactivation email to the user.

    Arguments:
        user: User -- The user to send the email to.
        title: str -- The title of the deactivation.
        description: str -- The description of the deactivation.
    """

    subject = f"Account Deactivation & Eviction Notice! : {user.full_name}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    context = {
        "user": user,
        "title": title,
        "description": description,
        "site_name": settings.SITE_NAME,
    }

    html_email = render_to_string("reports/deactivation_email.html", context)
    text_email = strip_tags(html_email)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_email,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_email, "text/html")

    email.send()
