# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# ReportsConfig Class
class ReportsConfig(AppConfig):
    """ReportsConfig

    ReportsConfig class is used to configure the reports app.

    Attributes:
        default_auto_field (str): The default auto field to use for models.
        name (str): The name of the app.
        verbose_name (str): The human-readable name of the app.

    Methods:
        ready: Import the signals module when the app is ready.
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
    verbose_name = _("Reports")

    # Ready Method
    def ready(self) -> None:
        """Ready Method"""

        # Imports
        import apps.reports.signals  # noqa: F401
