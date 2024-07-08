# Imports
from apps.posts.views import (
    BookmarkedPostsListAPIView,
    BookmarkPostAPIView,
    DownvotePostAPIView,
    MyPostListAPIView,
    PopularTagsListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostsByTagListAPIView,
    PostUpdateAPIView,
    ReplyCreateAPIView,
    ReplyListAPIView,
    TopPostsListAPIView,
    UnbookmarkPostAPIView,
    UpvotePostAPIView,
)
from django.urls import path

# Set the url patterns
urlpatterns = [
    path("all/", PostListAPIView.as_view(), name="list-posts"),
    path(
        "tags/<str:tag_slug>/",
        PostsByTagListAPIView.as_view(),
        name="list-posts-by-tag",
    ),
    path("top-posts/", TopPostsListAPIView.as_view(), name="list-top-posts"),
    path("popular-tags/", PopularTagsListAPIView.as_view(), name="list-popular-tags"),
    path("create/", PostCreateAPIView.as_view(), name="create-post"),
    path("my-posts/", MyPostListAPIView.as_view(), name="list-my-posts"),
    path("<slug:slug>/", PostDetailAPIView.as_view(), name="retrieve-post"),
    path("<slug:slug>/update/", PostUpdateAPIView.as_view(), name="update-post"),
    path("<slug:slug>/bookmark/", BookmarkPostAPIView.as_view(), name="bookmark-post"),
    path(
        "<slug:slug>/unbookmark/",
        UnbookmarkPostAPIView.as_view(),
        name="unbookmark-post",
    ),
    path(
        "bookmarked/posts/",
        BookmarkedPostsListAPIView.as_view(),
        name="list-bookmarked-posts",
    ),
    path("<uuid:post_id>/reply/", ReplyCreateAPIView.as_view(), name="create-reply"),
    path("<uuid:post_id>/replies/", ReplyListAPIView.as_view(), name="list-replies"),
    path("<uuid:post_id>/upvote/", UpvotePostAPIView.as_view(), name="upvote-post"),
    path(
        "<uuid:post_id>/downvote/", DownvotePostAPIView.as_view(), name="downvote-post"
    ),
]
