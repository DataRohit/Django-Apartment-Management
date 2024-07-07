# Imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm


# Get the User model
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User Admin.

    This class defines the user admin interface.

    Attributes:
        form: UserChangeForm -- The form to change the user.
        add_form: UserCreationForm -- The form to add a user.
        list_display: list -- The fields to display in the list.
        list_display_links: list -- The fields to link in the list.
        search_fields: list -- The fields to search in the list.
        ordering: list -- The fields to order in the list.
        fieldsets: tuple -- The fields to display in the form.
        add_fieldsets: tuple -- The fields to display in the add form.
    """

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_superuser",
    ]
    list_display_links = ["pkid", "id", "email", "username"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["pkid"]
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
