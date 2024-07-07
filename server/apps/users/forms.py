# Imports
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm


# Get the user model
User = get_user_model()


class UserChangeForm(BaseUserChangeForm):
    """User Change Form.

    This form is used to change the user's information.

    Meta:
        model: User -- The user model.
        fields: list -- The fields to display in the form.
    """

    class Meta(BaseUserChangeForm.Meta):
        """Meta Class.

        This class defines the metadata for the UserChangeForm.

        Attributes:
            model: User -- The user model.
            fields: list -- The fields to display in the form.
        """

        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserCreationForm(admin_forms.UserCreationForm):
    """User Creation Form.

    This form is used to create a new user.

    Meta:
        model: User -- The user model.
        fields: list -- The fields to display in the form.

    Attributes:
        error_messages: dict -- The error messages.

    Methods:
        clean_username: Clean the username field.
        clean_email: Clean the email field.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        """Meta Class.

        This class defines the metadata for the UserCreationForm.

        Attributes:
            model: User -- The user model.
            fields: list -- The fields to display in the form.
        """

        model = User
        fields = ["first_name", "last_name", "username", "email"]

    # Set the error messages
    error_messages = {
        "duplicate_username": "A user with that username already exists.",
        "duplicate_email": "A user with that email already exists.",
    }

    def clean_email(self) -> str:
        """Clean the email field.

        Returns:
            email: str -- The cleaned email address.

        Raises:
            ValidationError: If the email address is already taken.
        """

        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email

    def clean_username(self) -> str:
        """Clean the username field.

        Returns:
            username: str -- The cleaned username.

        Raises:
            ValidationError: If the username is already taken.
        """

        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages["duplicate_username"])
        return username
