# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# IssuesConfig Class
class IssuesConfig(AppConfig):
    """IssuesConfig

    IssuesConfig class is used to configure the issues app.

    Attributes:
        default_auto_field (str): The default auto field to use for models.
        name (str): The name of the app.
        verbose_name (str): The human-readable name of the app.
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.issues"
    verbose_name = _("Issues")
