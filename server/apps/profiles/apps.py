# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# ProfilesConfig Class
class ProfilesConfig(AppConfig):
    """ProfilesConfig

    ProfilesConfig class is used to configure the profiles app.

    Attributes:
        default_auto_field (str): The default auto field to use for models.
        name (str): The name of the app.
        verbose_name (str): The human-readable name of the app.

    Methods:
        ready: This method is called when the app is ready
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.profiles"
    verbose_name = _("Profiles")

    # Ready Method
    def ready(self) -> None:
        """Ready Method"""

        # Imports
        import apps.profiles.signals  # noqa: F401
