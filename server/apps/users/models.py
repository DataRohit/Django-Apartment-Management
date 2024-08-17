# Imports
import uuid

from apps.users.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


# Username Validator
class UsernameValidator(validators.RegexValidator):
    """Username Validator

    UsernameValidator class is used to validate the username field.

    Extends:
        RegexValidator

    Attributes:
        regex (str): The regular expression for the username field.
        message (str): The error message for the username field.
        flag (int): The flags for the regular expression.
    """

    # Attributes
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain letters, numbers, a dot, "
        "@ symbol, + symbol and a hyphen "
    )
    flag = 0


# User Model
class User(AbstractUser):
    """User

    User class is used to represent a user in the database.

    Extends:
        AbstractUser

    Attributes:
        pkid (BigAutoField): The primary key of the user.
        id (UUIDField): The unique identifier of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (EmailField): The email address of the user.
        username (str): The username of the user.

    Properties:
        full_name (str): The full name of the user.

    Meta Class:
        verbose_name (str): The verbose name of the user.
        verbose_name_plural (str): The verbose name of the user in plural.
        ordering (List[str]): The default ordering of the user.

    Constants:
        EMAIL_FIELD (str): The email field of the user.
        USERNAME_FIELD (str): The username field of the user.
        REQUIRED_FIELDS (List[str]): The required fields for the user.

    Managers:
        objects (UserManager): The user manager.
    """

    # Attributes
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=60)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=60)
    email = models.EmailField(
        verbose_name=_("Email Address"), unique=True, db_index=True
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=60,
        unique=True,
        validators=[UsernameValidator],
    )

    # Constants for email and username fields
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    # Constants for required fields
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # Set the user manager
    objects = UserManager()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            verbose_name (str): The verbose name of the user.
            verbose_name_plural (str): The verbose name of the user in plural.
            ordering (List[str]): The default ordering of the user.
        """

        # Attributes
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    # Property to get the full name
    @property
    def full_name(self) -> str:
        """Get the full name of the user.

        Returns:
            str: The full name of the user.
        """

        # Get the full name
        full_name = f"{self.first_name} {self.last_name}"

        # Return the full name
        return full_name.strip()
