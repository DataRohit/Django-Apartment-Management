# Imports
from apps.profiles.models import Profile
from celery import shared_task


@shared_task(name="update_all_reputations")
def update_all_reputations() -> None:
    """Update the reputation of all profiles."""

    profiles = Profile.objects.all()

    for profile in profiles:
        profile.update_reputation()
        profile.save()
