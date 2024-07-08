# Imports
from apps.apartments.views import ApartmentCreateAPIView, ApartmentListAPIView
from django.urls import path


# Set the url patterns
urlpatterns = [
    path("add/", ApartmentCreateAPIView.as_view(), name="add-apartment"),
    path("my-apartments/", ApartmentListAPIView.as_view(), name="list-my-apartments"),
]
