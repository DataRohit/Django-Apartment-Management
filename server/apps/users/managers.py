# Imports
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_email_address(email: str):
    """Validate the email address.

    This function validates the email address.

    Arguments:
        email: str -- The email address to validate.

    Raises:
        ValidationError: If the email address is invalid.
    """

    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address"))


class UserManager(DjangoUserManager):
    """User Manager.

    This class defines the user manager.

    Methods:
        _create_user: Create a user.
        create_user: Create a normal user.
        create_superuser: Create a superuser.
    """

    def _create_user(
        self, username: str, email: str, password: str | None, **extra_fields
    ) -> "User":  # type: ignore
        """Create a user.

        This method creates a user.

        Arguments:
            username: str -- The username of the user.
            email: str -- The email address of the user.
            password: str | None -- The password of the user.
            **extra_fields: Dict -- The extra fields.

        Raises:
            ValueError: If the username is not provided.
            ValueError: If the email address is not provided.

        Returns:
            User: The user object.
        """
        if not username:
            raise ValueError(_("The username must be provided."))

        if not email:
            raise ValueError(_("The email address must be provided."))

        email = self.normalize_email(email)
        validate_email_address(email)

        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ) -> "User":  # type: ignore
        """Create a normal user.

        This method creates a normal user.

        Arguments:
            username: str -- The username of the user.
            email: str -- The email address of the user.
            password: str | None -- The password of the user.
            **extra_fields: Dict -- The extra fields.

        Raises:
            ValueError: If the username is not provided.
            ValueError: If the email address is not provided.

        Returns:
            User: The user object.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ) -> "User":  # type: ignore
        """Create a superuser.

        This method creates a superuser.

        Arguments:
            username: str -- The username of the user.
            email: str -- The email address of the user.
            password: str | None -- The password of the user.
            **extra_fields: Dict -- The extra fields.

        Raises:
            ValueError: If the username is not provided.
            ValueError: If the email address is not provided.
            ValueError: If the superuser does not have is_staff=True.
            ValueError: If the superuser does not have is_superuser=True.

        Returns:
            User: The user object.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(username, email, password, **extra_fields)
