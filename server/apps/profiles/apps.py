# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    """Profiles App Config

    This class is used to configure the Profiles app.

    Attributes:
        default_auto_field: str -- The default auto field to use for models.
        name: str -- The name of the app.
        verbose_name: str -- The human-readable name of the app.

    Methods:
        ready: This method is called when the app is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.profiles"
    verbose_name = _("Profiles")

    def ready(self) -> None:
        """Ready Method

        This method is called when the app is ready.
        """

        # Imports
        import apps.profiles.signals
