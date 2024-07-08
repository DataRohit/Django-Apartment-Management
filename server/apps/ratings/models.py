# Imports
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Get the user model
User = get_user_model()


class Rating(TimeStampedModel):
    """Rating Model.

    This model is used to store the rating of the user.

    Extends:
        TimeStampedModel

    Attributes:
        RatingChoices: IntegerChoices -- Choices for the rating

        rated_user: User {ForeignKey} -- The user who is rated
        rating_user: User {ForeignKey} -- The user who rated
        rating: int -- The integer field to store the rating
        comment: text -- The text field for the comment

    Methods:
        __str__: Get the string representation of the model

    Meta:
        verbose_name: str -- The singular name for the model
        verbose_name_plural: str -- The plural name for the model
    """

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

    def __str__(self) -> str:
        """Get the string representation of the model

        Returns:
            str: The rating user rated the rated user with the rating
        """

        return f"{self.rating_user} rated {self.rated_user} - {self.rating}"

    class Meta:
        """Meta Class.

        The meta class for the rating model.

        Attributes:
            verbose_name: str -- The singular name for the model
            verbose_name_plural: str -- The plural name for the model
        """

        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
