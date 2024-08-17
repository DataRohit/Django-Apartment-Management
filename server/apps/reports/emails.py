# Imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()


# Function to send a warning email
def send_warning_email(user: User, title: str, description: str) -> None:  # type: ignore
    """Send a warning email to a user.

    Args:
        user (User): The user to send the email to.
        title (str): The title of the email.
        description (str): The description of the email.
    """

    # Set the email subject
    subject = f"Warning: {user.full_name} You have been reported!"

    # Set the email sender and recipient
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Create the email context
    context = {
        "user": user,
        "title": title,
        "description": description,
        "site_name": settings.SITE_NAME,
    }

    # Render the HTML email
    html_email = render_to_string("reports/warning_email.html", context)
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


# Function to send a deactivation email
def send_deactivation_email(user: User, title: str, description: str) -> None:  # type: ignore
    """Send a deactivation email to a user.

    Args:
        user (User): The user to send the email to.
        title (str): The title of the email.
        description (str): The description of the email.
    """

    # Set the email subject
    subject = f"Account Deactivation & Eviction Notice! : {user.full_name}"

    # Set the email sender and recipient
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Create the email context
    context = {
        "user": user,
        "title": title,
        "description": description,
        "site_name": settings.SITE_NAME,
    }

    # Render the HTML email
    html_email = render_to_string("reports/deactivation_email.html", context)
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
