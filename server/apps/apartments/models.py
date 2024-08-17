# Imports
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Get the user model
User = get_user_model()


# Apartment Model
class Apartment(TimeStampedModel):
    """Apartment

    Apartment class is used to represent an apartment in the database.

    Extends:
        TimeStampedModel

    Attributes:
        unit_number (str): The unit number of the apartment.
        building (str): The building of the apartment.
        floor (int): The floor of the apartment.
        tenant (ForeignKey): The tenant of the apartment.

    Methods:
        __str__(): Return the string representation of the apartment.
    """

    # Attributes
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

    # String Representation
    def __str__(self) -> str:
        """Return the string representation of the apartment.

        Returns:
            str: The string representation of the apartment.
        """

        # Return the string representation
        return f"Unit: {self.unit_number} - Building: {self.building} - Floor: {self.floor}"
