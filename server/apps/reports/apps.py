# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReportsConfig(AppConfig):
    """Reports App Config

    This class is used to configure the Reports app.

    Attributes:
        default_auto_field: str -- The default auto field to use for models.
        name: str -- The name of the app.
        verbose_name: str -- The human-readable name of the app.

    Methods:
        ready: This method is called when the app is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
    verbose_name = _("Reports")

    def ready(self) -> None:
        """Ready Method

        This method is called when the app is ready.
        """

        import apps.reports.signals
