# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Set the django urls
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/apartments/", include("apps.apartments.urls")),
    path("api/v1/issues/", include("apps.issues.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path("api/v1/posts/", include("apps.posts.urls")),
]


# Swagger urls
urlpatterns += [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="swagger-schema"),
    path(
        "api/v1/swagger/",
        SpectacularSwaggerView.as_view(url_name="swagger-schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="swagger-schema"),
        name="swagger-redoc",
    ),
]


# Admin configuration
admin.site.site_header = "Alpha Apartments Admin"
admin.site.site_title = "Alpha Apartments Admin"
admin.site.index_title = "Welcome to Alpha Apartments Admin"
