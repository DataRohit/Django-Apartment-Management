# Imports
from apps.profiles.models import Profile
from celery import shared_task


# Create a shared task to update all reputations
@shared_task(name="update_all_reputations")
def update_all_reputations() -> None:
    """Update all reputations.

    This function is used to update all reputations.
    """

    # Get all the profiles
    profiles = Profile.objects.all()

    # Traverse over each profile
    for profile in profiles:
        # Update the reputation
        profile.update_reputation()

        # Save the profile
        profile.save()
