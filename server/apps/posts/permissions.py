# Imports
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


# Get the user model
User = get_user_model()


class CanCreateEditPost(permissions.BasePermission):
    """Permission for users that can create or edit a post.

    This class defines the permission for users that can create or edit a post.

    Attributes:
        message: str -- The message.

    Methods:
        has_permission: Returns whether the user has the permission to create or edit a post.
    """

    message = "You do not have the permission to create or edit this post."

    def has_permission(self, request: Request, view: View) -> bool:
        """Returns whether the user has the permission to create or edit a post.

        Arguments:
            request: Request -- The request.
            view: View -- The view.

        Returns:
            bool: Whether the user has the permission to create or edit a post.
        """

        user = request.user

        if not user or not user.is_authenticated:
            self.message = "You must be authenticated to create or edit a post."
            return False

        if user.is_superuser or user.is_staff:
            return True

        profile = getattr(user, "profile", None)

        if profile and profile.occupation == Profile.Occupation.TENANT:
            return True

        return False
