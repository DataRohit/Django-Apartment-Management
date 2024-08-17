# Imports
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

# Get the user model
User = get_user_model()


# CanCreateEditPost
class CanCreateEditPost(permissions.BasePermission):
    """CanCreateEditPost

    CanCreateEditPost class is used to check if the user has the permission to create or edit a post.

    Extends:
        permissions.BasePermission

    Attributes:
        message (str): The error message to display.

    Methods:
        has_permission: Check if the user has the permission.
    """

    # Attributes
    message = "You do not have the permission to create or edit this post."

    # Method to check if the user has the permission
    def has_permission(self, request: Request, view: View) -> bool:
        """Check if the user has the permission.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """

        # Get the user
        user = request.user

        # If user is not authenticated
        if not user or not user.is_authenticated:
            # Set the error message
            self.message = "You must be authenticated to create or edit a post."

            # Return false
            return False

        # If user is a superuser or staff
        if user.is_superuser or user.is_staff:
            # Return true
            return True

        # Get the user profile
        profile = getattr(user, "profile", None)

        # If user is a tenant
        if profile and profile.occupation == Profile.Occupation.TENANT:
            # Return true
            return True

        # Return false
        return False
