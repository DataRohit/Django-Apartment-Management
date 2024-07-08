# Imports
import os
import uuid
from typing import Any
from apps.common.models import TimeStampedModel
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# Get the user model
User = get_user_model()


def get_user_username(instance: "Profile") -> str:  # type: ignore
    """Get the user username.

    This function is used to get the username of the user.

    Arguments:
        instance: Profile -- The Profile instance.

    Returns:
        str -- The username of the user.
    """

    return instance.user.username


def avatar_upload_to(instance: "Profile", filename: str) -> str:
    """Generate a unique filename for the avatar.

    This function generates a unique filename using UUID and preserves the original file extension.

    Arguments:
        instance: Profile -- The Profile instance.
        filename: str -- The original filename.

    Returns:
        str -- The unique filename.
    """

    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("avatars/", filename)


class Profile(TimeStampedModel):
    """Profile Model.

    This model is used to store the profile of the user.

    Extends:
        TimeStampedModel

    Attributes:
        Gender: TextChoices -- Choices for the gender
        Occupation: TextChoices -- Choices for the occupation

        user: User {OneToOne} -- The user
        avatar: CloudinaryField -- Cloudinary field for the avatar image
        gender: str -- The character field to store user gender
        bio: text -- The text field for user
        occupation: str -- The character field for user
        phone_number: PhoneNumberField -- The phone number field for user
        country_of_origin: CountryField -- The country field for user
        city_of_origin: str -- The character field for user
        report_count: int -- The integer field to track how many times the user has been reported
        reputation: int -- The integer field to store the reputation of the user
        slug: AutoSlugField -- Slug field for the user profile

    Properties:
        is_banned: Check if the user is banned

    Methods:
        update_reputation: Update the reputation of the user
        save: Save the profile
    """

    # Gender choices
    class Gender(models.TextChoices):
        MALE = ("male", _("Male"))
        FEMALE = ("female", _("Female"))
        OTHER = ("other", _("Other"))

    # Occupation choices
    class Occupation(models.TextChoices):
        MASON = ("mason", _("Mason"))
        CARPENTER = ("carpenter", _("Carpenter"))
        PLUMBER = ("plumber", _("Plumber"))
        ROOFER = ("roofer", _("Roofer"))
        PAINTER = ("painter", _("Painter"))
        ELECTRICIAN = ("electrician", _("Electrician"))
        HVAC = ("hvac", _("HVAC"))
        TENANT = ("tenant", _("Tenant"))

    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.FileField(_("Avatar"), upload_to=avatar_upload_to, blank=True, null=True)
    gender = models.CharField(
        _("Gender"), choices=Gender.choices, max_length=10, default=Gender.OTHER
    )
    bio = models.TextField(_("Bio"), blank=True, null=True)
    occupation = models.CharField(
        _("Occupation"),
        choices=Occupation.choices,
        max_length=20,
        default=Occupation.TENANT,
    )
    phone_number = PhoneNumberField(
        _("Phone Number"),
        max_length=15,
        default="+91-9204178296",
    )
    country_of_origin = CountryField(_("Country of Origin"), default="IN")
    city_of_origin = models.CharField(
        _("City of Origin"), max_length=180, default="Nagpur"
    )
    report_count = models.PositiveIntegerField(_("Report Count"), default=0)
    reputation = models.PositiveIntegerField(_("Reputation"), default=100)
    slug = AutoSlugField(
        _("Slug"),
        populate_from=get_user_username,
        unique=True,
        always_update=True,
    )

    # Method to check if the user is banned
    @property
    def is_banned(self) -> bool:
        """Check if the user is banned

        This property is used to check if the user is banned.

        Returns:
            bool -- True if the user is banned, False otherwise.
        """
        return self.report_count >= 5

    # Method to update the reputation
    def update_reputation(self) -> None:
        """Update the reputation

        This method is used to update the reputation of the user.
        """
        self.reputation = max(0, 100 - self.report_count * 20)

    # Method to save the profile
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the profile

        This method is used to save the profile.
        """
        self.update_reputation()
        super().save(*args, **kwargs)
