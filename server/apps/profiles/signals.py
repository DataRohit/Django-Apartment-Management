# Imports
import logging
from typing import Dict, Type

from apps.profiles.models import Profile
from config.settings.base import AUTH_USER_MODEL
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Get the logger
logger = logging.getLogger(__name__)


# Signal to trigger the creation of a profile for a new user
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Dict
) -> None:
    """Create user profile.

    This function is used to create a profile for a new user.

    Args:
        sender (Type[Model]): The sender model.
        instance (Model): The instance model.
        created (bool): The flag to check if the instance was created.
        **kwargs (Dict): The keyword arguments.
    """

    # If the user was created
    if created:
        # Create a profile for the user
        Profile.objects.create(user=instance)

        # Log the creation of the profile
        logger.info(f"Profile created for user {instance.full_name}")

    # Else
    else:
        # Log the existence of the profile
        logger.info(f"Profile already exists for user {instance.full_name}")
