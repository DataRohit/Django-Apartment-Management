# Imports
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from apps.users.managers import UserManager


class UsernameValidator(validators.RegexValidator):
    """Username Validator.

    This class validates the username.

    Attributes:
        regex: str -- The regular expression to validate the username.
        message: str -- The error message to display.
        flags: int -- The flags to use.
    """

    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain letters, numbers, a dot, "
        "@ symbol, + symbol and a hyphen "
    )
    flag = 0


class User(AbstractUser):
    """Custom User Model.

    This model is used to store the user information.

    Extends:
        AbstractUser

    Attributes:
        pkid: models.BigAutoField -- The primary key of the user.
        id: models.UUIDField -- The UUID of the user.
        first_name: models.CharField -- The first name of the user.
        last_name: models.CharField -- The last name of the user.
        email: models.EmailField -- The email of the user.
        username: models.CharField -- The username of the user.

        EMAIL_FIELD: str -- The email field.
        USERNAME_FIELD: str -- The username field.

        REQUIRED_FIELDS: list -- The required fields.

        objects: UserManager -- The custom manager.

    Meta:
        verbose_name: str -- The verbose name of the model.
        verbose_name_plural: str -- The verbose name of the model in plural.
        ordering: list -- The default ordering of the model.

    Properties:
        full_name: str -- The full name of the user.
    """

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

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        """Meta Class.

        This class defines the metadata for the model.

        Attributes:
            verbose_name: str -- The verbose name of the model.
            verbose_name_plural: str -- The verbose name of the model in plural.
            ordering: list -- The default ordering of the model.
        """

        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    @property
    def get_full_name(self) -> str:
        """Get the user's full name.

        Returns:
            str: The full name of the user.
        """

        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
