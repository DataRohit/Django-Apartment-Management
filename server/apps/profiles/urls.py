# Imports
from apps.profiles.views import (
    AvatarUploadAPIView,
    NonTenantProfileListAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
)
from django.urls import path

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="list-profiles"),
    path(
        "non-tenant-profiles/",
        NonTenantProfileListAPIView.as_view(),
        name="list-non-tenant-profiles",
    ),
    path(
        "user/my-profile/", ProfileDetailAPIView.as_view(), name="retrieve-my-profile"
    ),
    path("user/update/", ProfileUpdateAPIView.as_view(), name="update-my-profile"),
    path(
        "user/avatar/",
        AvatarUploadAPIView.as_view(),
        name="upload-user-avatar",
    ),
]
