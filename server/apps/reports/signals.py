# Imports
from typing import Dict, Type

from apps.reports.emails import send_deactivation_email, send_warning_email
from apps.reports.models import Report
from django.db import transaction
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver


# Signal to update the user report count and reputation
@receiver(post_save, sender=Report)
def update_user_report_count_and_reputation(
    sender: Type[ModelBase], instance: Report, created: bool, **kwargs: Dict
) -> None:
    """Update the user report count and reputation.

    Args:
        sender (Type[ModelBase]): The model class.
        instance (Report): The report instance.
        created (bool): Whether the report was created.
        **kwargs (Dict): Additional keyword arguments.
    """

    # If the report was created
    if created:
        # Create a transaction
        with transaction.atomic():
            # Get the reported user profile
            reported_user_profile = instance.reported_user.profile

            # Update the report count and save the profile
            reported_user_profile.report_count += 1
            reported_user_profile.save()

            # If the report count is 1
            if reported_user_profile.report_count == 1:
                # Send the warning email
                send_warning_email(
                    user=instance.reported_user,
                    title=instance.title,
                    description=instance.description,
                )

            # If the report count is greater than or equal to 5
            elif reported_user_profile.report_count >= 5:
                # If the reported user is active
                instance.reported_user.is_active = False

                # Save the reported user
                instance.reported_user.save()

                # Send the deactivation email
                send_deactivation_email(
                    user=instance.reported_user,
                    title=instance.title,
                    description=instance.description,
                )
