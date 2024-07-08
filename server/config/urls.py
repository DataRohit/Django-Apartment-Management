# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

# Set the django urls
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/apartments/", include("apps.apartments.urls")),
    path("api/v1/issues/", include("apps.issues.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
]


# Admin configuration
admin.site.site_header = "Alpha Apartments Admin"
admin.site.site_title = "Alpha Apartments Admin"
admin.site.index_title = "Welcome to Alpha Apartments Admin"
