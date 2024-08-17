# Imports
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

# Get the user model
User = get_user_model()


# User Change Form
class UserChangeForm(BaseUserChangeForm):
    """User Change Form

    This class is used to change the user's information.

    Extends:
        BaseUserChangeForm

    Meta Class:
        model (User): The user model.
        fields (list): The fields to include in the form.
    """

    # Meta Class
    class Meta(BaseUserChangeForm.Meta):
        """Meta Class.

        Attributes:
            model (User): The user model.
            fields (list): The fields to include in the form
        """

        # Attributes
        model = User
        fields = ["first_name", "last_name", "username", "email"]


# User Creation Form
class UserCreationForm(admin_forms.UserCreationForm):
    """User Creation Form

    This class is used to create a new user.

    Extends:
        UserCreationForm

    Meta Class:
        model (User): The user model.
        fields (list): The fields to include in the form.

    Attributes:
        error_messages (dict): The error messages to display.

    Methods:
        clean_email() -> str: Clean the email.
        clean_username() -> str: Clean the username.
    """

    # Meta Class
    class Meta(admin_forms.UserCreationForm.Meta):
        """Meta Class

        Attributes:
            model (User): The user model.
            fields (list): The fields to include in the form
        """

        # Attributes
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    # Set the error messages
    error_messages = {
        "duplicate_username": "A user with that username already exists.",
        "duplicate_email": "A user with that email already exists.",
    }

    # Method to clean the email
    def clean_email(self) -> str:
        """Clean the email.

        Returns:
            str: The cleaned email.

        Raises:
            forms.ValidationError: If the email already exists
        """

        # Get the email
        email = self.cleaned_data["email"]

        # If the email exists
        if User.objects.filter(email=email).exists():
            # Raise a validation error
            raise forms.ValidationError(self.error_messages["duplicate_email"])

        # Return the email
        return email

    # Method to clean the username
    def clean_username(self) -> str:
        """Clean the username.

        Returns:
            str: The cleaned username.

        Raises:
            forms.ValidationError: If the username already exists.
        """

        # Get the username
        username = self.cleaned_data["username"]

        # If the username exists
        if User.objects.filter(username=username).exists():
            # Raise a validation error
            raise forms.ValidationError(self.error_messages["duplicate_username"])

        # Return the username
        return username
