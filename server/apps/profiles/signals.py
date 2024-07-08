# Imports
import logging
from typing import Any, Type
from apps.profiles.models import Profile
from config.settings.base import AUTH_USER_MODEL
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver


# Get the logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:
    """Signal to create a profile for the user.

    Arguments:
        sender: Type[Model] -- The sender of the signal.
        instance: Model -- The instance of the sender.
        created: bool -- A boolean indicating if the instance was created.
        **kwargs: Dict -- Additional keyword arguments.
    """

    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.full_name}")

    else:
        logger.info(f"Profile already exists for user {instance.full_name}")
