# Imports
from apps.issues.views import (
    AssignedIssuesListAPIView,
    IssueCreateAPIView,
    IssueDeleteAPIView,
    IssueDetailAPIView,
    IssueListAPIView,
    IssueUpdateAPIView,
    MyIssuesListAPIView,
)
from django.urls import path

# Set the url patterns
urlpatterns = [
    path("", IssueListAPIView.as_view(), name="list-issues"),
    path("assigned/", AssignedIssuesListAPIView.as_view(), name="list-assigned-issues"),
    path("my-issues/", MyIssuesListAPIView.as_view(), name="list-my-issues"),
    path(
        "create/<uuid:apartment_id>/", IssueCreateAPIView.as_view(), name="create-issue"
    ),
    path("<uuid:id>/", IssueDetailAPIView.as_view(), name="detail-issue"),
    path("update/<uuid:id>/", IssueUpdateAPIView.as_view(), name="update-issue"),
    path("delete/<uuid:id>/", IssueDeleteAPIView.as_view(), name="delete-issue"),
]
