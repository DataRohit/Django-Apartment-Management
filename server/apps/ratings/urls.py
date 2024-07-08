# Imports
from apps.ratings.views import RatingCreateAPIView
from django.urls import path

# Set the url patterns
urlpatterns = [
    path("create/", RatingCreateAPIView.as_view(), name="create-rating"),
]
