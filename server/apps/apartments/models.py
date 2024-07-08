# Imports
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Get the user model
User = get_user_model()


class Apartment(TimeStampedModel):
    """Apartment Model.

    This class defines the apartment model.

    Attributes:
        unit_number: models.CharField -- The unit number.
        building: models.CharField -- The building.
        floor: models.PositiveIntegerField -- The floor.
        tenant: models.ForeignKey -- The tenant.

    Methods:
        __str__: Returns the string representation of the apartment.
    """

    unit_number = models.CharField(
        max_length=10, unique=True, verbose_name=_("Unit Number")
    )
    building = models.CharField(max_length=50, verbose_name=_("Building"))
    floor = models.PositiveIntegerField(verbose_name=_("Floor"))
    tenant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apartment",
        verbose_name=_("Tenant"),
    )

    def __str__(self) -> str:
        """Return the string representation of the apartment.

        Returns:
            str: The string representation.
        """

        return f"Unit: {self.unit_number} - Building: {self.building} - Floor: {self.floor}"
