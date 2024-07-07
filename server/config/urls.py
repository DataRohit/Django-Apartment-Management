# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import path


# Set the django urls
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]


# Admin configuration
admin.site.site_header = "Alpha Apartments Admin"
admin.site.site_title = "Alpha Apartments Admin"
admin.site.index_title = "Welcome to Alpha Apartments Admin"
