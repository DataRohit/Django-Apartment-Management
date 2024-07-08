# Imports
from apps.users.views import (
    CustomProviderAuthAPIView,
    CustomTokenObtainPairAPIView,
    CustomTokenRefreshAPIView,
    LogoutAPIView,
)
from django.urls import path, re_path

# Set the url patterns
urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthAPIView.as_view(),
        name="user-provider-auth",
    ),
    path(
        "login/", CustomTokenObtainPairAPIView.as_view(), name="user-token-obtain-pair"
    ),
    path("refresh/", CustomTokenRefreshAPIView.as_view(), name="user-token-refresh"),
    path("logout/", LogoutAPIView.as_view(), name="user-logout"),
]
