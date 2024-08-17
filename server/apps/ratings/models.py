# Imports
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


# Rating Model
class Rating(TimeStampedModel):
    """Rating

    Rating class is used to represent a rating in the database.

    Extends:
        TimeStampedModel

    Attributes:
        rated_user (ForeignKey): The user being rated.
        rating_user (ForeignKey): The user giving the rating.
        rating (int): The rating value.
        comment (str): The comment for the rating.

    Methods:
        __str__(): Return the string representation of the rating.

    Constants:
        RatingChoices: The choices for the rating.

    Meta Class:
        verbose_name (str): The human-readable name for the model.
        verbose_name_plural (str): The human-readable plural name for the model.
    """

    # Constants for the rating choices
    class RatingChoices(models.IntegerChoices):
        ONE = (
            1,
            _("Very Poor"),
        )
        TWO = (
            2,
            _("Poor"),
        )
        THREE = (
            3,
            _("Average"),
        )
        FOUR = (
            4,
            _("Good"),
        )
        FIVE = 5, _("Excellent")

    # Attributes
    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_ratings",
        verbose_name=_("Rated User"),
    )
    rating_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        verbose_name=_("Rating User"),
    )
    rating = models.IntegerField(
        choices=RatingChoices.choices,
        verbose_name=_("Rating"),
    )
    comment = models.TextField(
        _("Comment"),
        blank=True,
    )

    # String Representation
    def __str__(self) -> str:
        """Return the string representation of the rating.

        Returns:
            str: The string representation of the rating.
        """

        # Return the rating
        return f"{self.rating_user} rated {self.rated_user} - {self.rating}"

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            verbose_name (str): The human-readable name for the model.
            verbose_name_plural (str): The human-readable plural name for the model.
        """

        # Attributes
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
