# Imports
from apps.reports.views import ReportCreateAPIView, ReportListAPIView
from django.urls import path

# Set the url patterns
urlpatterns = [
    path("create/", ReportCreateAPIView.as_view(), name="create-report"),
    path("my-reports/", ReportListAPIView.as_view(), name="list-my-reports"),
]
