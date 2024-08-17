# Imports
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


# Function to validate the email address
def validate_email_address(email: str):
    """Validate the email address.

    Args:
        email (str): The email address to validate.

    Raises:
        ValidationError: If the email address is not valid.
    """

    # Try to validate the email address
    try:
        validate_email(email)

    # If the email address is not valid
    except ValidationError:
        # Raise a validation error
        raise ValidationError(_("Enter a valid email address"))


# User Manager
class UserManager(DjangoUserManager):
    """User Manager

    This class is used to manage the users.

    Extends:
        DjangoUserManager

    Methods:
        _create_user(username: str, email: str, password: str | None, **extra_fields) -> User: Create a user.
        create_user(username: str, email: str | None = None, password: str | None = None, **extra_fields) -> User: Create a user.
        create_superuser(username: str, email: str | None = None, password: str | None = None, **extra_fields) -> User: Create a superuser.
    """

    # Function to create a user
    def _create_user(
        self, username: str, email: str, password: str | None, **extra_fields
    ) -> "User":  # type: ignore  # noqa: F821
        """Create a user.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str | None): The password of the user.
            **extra_fields: The extra fields.

        Returns:
            User: The created user.

        Raises:
            ValueError: If the username or email is not provided.
        """

        # If the username is not provided
        if not username:
            # Raise a value error
            raise ValueError(_("The username must be provided."))

        # If the email is not provided
        if not email:
            # Raise a value error
            raise ValueError(_("The email address must be provided."))

        # Normalize the email
        email = self.normalize_email(email)

        # Validate the email address
        validate_email_address(email)

        # Create the user
        user = self.model(username=username, email=email, **extra_fields)

        # Set the password
        if password:
            user.set_password(password)

        # Save the user
        user.save(using=self._db)

        # Return the user
        return user

    # Method to create a user
    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ) -> "User":  # type: ignore  # noqa: F821
        """Create a user.

        Args:
            username (str): The username of the user.
            email (str | None): The email of the user.
            password (str | None): The password of the user.
            **extra_fields: The extra fields.

        Returns:
            User: The created user.
        """

        # Set the extra fields for a normal user
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Create the user
        return self._create_user(username, email, password, **extra_fields)

    # Method to create a superuser
    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ) -> "User":  # type: ignore  # noqa: F821
        """Create a superuser.

        Args:
            username (str): The username of the superuser.
            email (str | None): The email of the superuser.
            password (str | None): The password of the superuser.
            **extra_fields: The extra fields.

        Returns:
            User: The created superuser.
        """

        # Set the extra fields for a superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # If the user is not a staff user
        if extra_fields.get("is_staff") is not True:
            # Raise a value error
            raise ValueError(_("Superuser must have is_staff=True."))

        # If the user is not a superuser
        if extra_fields.get("is_superuser") is not True:
            # Raise a value error
            raise ValueError(_("Superuser must have is_superuser=True."))

        # Create the superuser
        return self._create_user(username, email, password, **extra_fields)
