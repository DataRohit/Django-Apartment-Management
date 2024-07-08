# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    """Posts App Config

    This class is used to configure the Posts app.

    Attributes:
        default_auto_field: str -- The default auto field.
        name: str -- The name of the app.
        verbose_name: str -- The human-readable name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.posts"
    verbose_name = _("Posts")
