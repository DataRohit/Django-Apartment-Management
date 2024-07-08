# Imports
from typing import Dict, Type
from apps.reports.emails import send_deactivation_email, send_warning_email
from apps.reports.models import Report
from django.db import transaction
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Report)
def update_user_report_count_and_reputation(
    sender: Type[ModelBase], instance: Report, created: bool, **kwargs: Dict
) -> None:
    """Signal to update the user reputation and report count.

    Arguments:
        sender: Type[ModelBase] -- The sender of the signal.
        instance: Report -- The instance of the sender.
        created: bool -- A boolean indicating if the instance was created.
        **kwargs: dict -- Additional keyword arguments.
    """

    if created:
        with transaction.atomic():
            reported_user_profile = instance.reported_user.profile
            reported_user_profile.report_count += 1
            reported_user_profile.save()

            if reported_user_profile.report_count == 1:
                send_warning_email(
                    user=instance.reported_user,
                    title=instance.title,
                    description=instance.description,
                )

            elif reported_user_profile.report_count >= 5:
                instance.reported_user.is_active = False
                instance.reported_user.save()
                send_deactivation_email(
                    user=instance.reported_user,
                    title=instance.title,
                    description=instance.description,
                )
