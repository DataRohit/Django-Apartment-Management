# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# UsersConfig Class
class UsersConfig(AppConfig):
    """UsersConfig

    UsersConfig class is used to configure the users app.

    Attributes:
        default_auto_field (str): The default auto field to use for models.
        name (str): The name of the app.
        verbose_name (str): The human-readable name of the app.
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = _("Users")
