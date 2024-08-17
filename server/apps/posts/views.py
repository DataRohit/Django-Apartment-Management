# Imports
import logging
from typing import Dict

from apps.common.models import ContentView
from apps.common.renderers import GenericJSONRenderer
from apps.posts.filters import PostFilter
from apps.posts.models import Post, Reply
from apps.posts.permissions import CanCreateEditPost
from apps.posts.serializers import (
    DownvotePostSerializer,
    PopularTagSerializer,
    PostByTagSerializer,
    PostSerializer,
    ReplySerializer,
    TopPostSerialzier,
    UpvotePostSerializer,
)
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Get the logger
logger = logging.getLogger(__name__)


# StandardResultsSetPagination class
class StandardResultsSetPagination(PageNumberPagination):
    """StandardResultsSetPagination class for paginating results.

    This class extends PageNumberPagination to provide custom pagination settings.

    Attributes:
        page_size (int): The number of items to include on a page.
        page_size_query_param (str): The name of the 'page size' query parameter.
        max_page_size (int): The maximum number of items that can be requested per page.
    """

    # Attributes
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# PostListAPIView class
class PostListAPIView(generics.ListAPIView):
    """API view to list all posts.

    This view provides a paginated list of all posts, ordered by upvotes and creation date.

    Attributes:
        serializer_class (PostSerializer): The serializer class for the Post model.
        filterset_class (PostFilter): The filter class for the Post model.
        pagination_class (StandardResultsSetPagination): The pagination class to use.
        permission_classes (tuple): The permission classes required to access this view.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being returned.

    Methods:
        get_queryset: Get the queryset of posts.
    """

    # Attributes
    serializer_class = PostSerializer
    filterset_class = PostFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (GenericJSONRenderer,)
    object_label = "posts"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of posts.

        Returns:
            QuerySet: A queryset of Post objects, annotated with reply count and ordered.
        """
        # Annotate posts with reply count and order by upvotes and creation date
        return Post.objects.annotate(replies_count=Count("replies")).order_by(
            "-upvotes", "-created_at"
        )


# MyPostListAPIView class
class MyPostListAPIView(generics.ListAPIView):
    """API view to list posts by the current user.

    This view provides a list of posts created by the authenticated user.

    Attributes:
        serializer_class (PostSerializer): The serializer class for the Post model.
        filterset_class (PostFilter): The filter class for the Post model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being returned.

    Methods:
        get_queryset: Get the queryset of posts for the current user.
    """

    # Attributes
    serializer_class = PostSerializer
    filterset_class = PostFilter
    renderer_classes = (GenericJSONRenderer,)
    object_label = "my_posts"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of posts for the current user.

        Returns:
            QuerySet: A queryset of Post objects created by the current user.
        """
        # Filter posts by the current user and order by upvotes and creation date
        return Post.objects.filter(author=self.request.user).order_by(
            "-upvotes", "-created_at"
        )


# PostDetailAPIView class
class PostDetailAPIView(generics.RetrieveAPIView):
    """API view to retrieve details of a specific post.

    This view provides detailed information about a single post, identified by its slug.

    Attributes:
        serializer_class (PostSerializer): The serializer class for the Post model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being returned.
        lookup_field (str): The field to use for looking up the post.

    Methods:
        get_queryset: Get the queryset of posts, annotated with reply count.
        get_object: Get the specific post object and record the view.
        record_post_view: Record a view for the given post.

    Raises:
        Http404: If the post is not found.
    """

    # Attributes
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    lookup_field = "slug"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset of posts, annotated with reply count.

        Returns:
            QuerySet: A queryset of Post objects, annotated with reply count.
        """

        # Return the queryset of posts, annotated with reply count
        return Post.objects.annotate(replies_count=Count("replies"))

    # Method to get the object
    def get_object(self):
        """Get the specific post object and record the view.

        Returns:
            Post: The requested Post object.

        Raises:
            Http404: If the post is not found.
        """

        # Get the queryset
        queryset = self.get_queryset()

        # Use the lookup_field to filter the queryset
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}

        # Get the post or raise a 404 error
        post = get_object_or_404(queryset, **filter_kwargs)

        # Record the view for this post
        self.record_post_view(post)

        # Return the post
        return post

    # Method to record a post view
    def record_post_view(self, post: Post) -> None:
        """Record a view for the given post.

        Args:
            post (Post): The post being viewed.
        """

        # Get the ContentType for the Post model
        content_type = ContentType.objects.get_for_model(Post)

        # Get the viewer's IP address
        viewer_ip = self.get_client_ip()

        # Create or update the ContentView object
        ContentView.objects.get_or_create(
            content_type=content_type,
            object_id=post.pk,
            viewer_ip=viewer_ip,
            user=self.request.user,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    def get_client_ip(self) -> str:
        """
        Get the client's IP address from the request.

        Returns:
            str: The client's IP address.
        """
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # Get the first IP if multiple are present
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        return ip


# PostCreateAPIView class
class PostCreateAPIView(generics.CreateAPIView):
    """API view to create a new post.

    This view handles the creation of new Post objects.

    Attributes:
        queryset (QuerySet): The queryset of all Post objects.
        serializer_class (PostSerializer): The serializer class for the Post model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being created.
        permission_classes (tuple): The permission classes required to access this view.

    Methods:
        perform_create: Perform the creation of a new post.
    """

    # Attributes
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    permission_classes = (CanCreateEditPost,)

    # Method to perform the creation
    def perform_create(self, serializer: PostSerializer) -> None:
        """
        Perform the creation of a new post.

        Args:
            serializer (PostSerializer): The serializer instance.
        """

        # Save the post
        serializer.save()


# PostUpdateAPIView class
class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    """API view to retrieve and update a post.

    This view handles the retrieval and updating of existing Post objects.

    Attributes:
        queryset (QuerySet): The queryset of all Post objects.
        serializer_class (PostSerializer): The serializer class for the Post model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being updated.
        permission_classes (tuple): The permission classes required to access this view.
        lookup_field (str): The field to use for looking up the post.

    Methods:
        get_object: Get the specific post object and check permissions.
        perform_update: Perform the update of a post.
        update: Handle the update request and return the updated post with reply count.
    """

    # Attributes
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    permission_classes = (CanCreateEditPost,)
    lookup_field = "slug"

    # Method to get the object
    def get_object(self):
        """
        Get the specific post object and check permissions.

        Returns:
            Post: The requested Post object.

        Raises:
            PermissionDenied: If the user doesn't have permission to edit the post.
        """

        # Get the post object
        post = super().get_object()

        # Check if the current user is the author of the post
        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")

        # Return the post
        return post

    # Method to perform the update
    def perform_update(self, serializer: PostSerializer) -> None:
        """Perform the update of a post.

        Args:
            serializer (PostSerializer): The serializer instance.
        """

        # Update the post
        super().perform_update(serializer)

        # Set the post instance
        self.post_instance = serializer.instance

    # Method to update the post
    def update(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Handle the update request and return the updated post with reply count.

        Args:
            request (Request): The update request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the updated post data.
        """

        # Update the post
        super().update(request, *args, **kwargs)

        # Get the updated post with reply count
        post_with_replies_count = Post.objects.annotate(
            replies_count=Count("replies")
        ).get(pk=self.post_instance.pk)

        # Serialize the updated post
        response = self.get_serializer(post_with_replies_count).data

        # Return the response
        return Response(response)


# PostDeleteAPIView class
class BookmarkPostAPIView(APIView):
    """API view to bookmark a post.

    This view handles the bookmarking of a post by a user.

    Methods:
        patch: Handle the PATCH request to bookmark a post.
    """

    # Method to handle the PATCH request
    def patch(self, request: Request, slug: str) -> Response:
        """Handle the PATCH request to bookmark a post.

        Args:
            request (Request): The request object.
            slug (str): The slug of the post to bookmark.

        Returns:
            Response: The response indicating success or failure.
        """

        # Get the user and post
        user = request.user
        post = get_object_or_404(Post.objects, slug=slug)

        # Check if the post is already bookmarked by the user
        if user in post.bookmarked_by.all():
            return Response(
                {"message": "Post already bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Add the user to the post's bookmarked_by field
        post.bookmarked_by.add(user)

        # Return the response
        return Response(
            {"message": "Post bookmarked successfully."},
            status=status.HTTP_200_OK,
        )


# UnbookmarkPostAPIView class
class UnbookmarkPostAPIView(APIView):
    """API view to unbookmark a post.

    This view handles the removal of a bookmark from a post by a user.

    Methods:
        patch: Handle the PATCH request to unbookmark a post
    """

    # Method to handle the PATCH request
    def patch(self, request: Request, slug: str) -> Response:
        """Handle the PATCH request to unbookmark a post.

        Args:
            request (Request): The request object.
            slug (str): The slug of the post to unbookmark.

        Returns:
            Response: The response indicating success or failure.
        """

        # Get the user and post
        user = request.user
        post = get_object_or_404(Post, slug=slug)

        # Check if the post is bookmarked by the user
        if user not in post.bookmarked_by.all():
            return Response(
                {"message": "Post not bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remove the user from the post's bookmarked_by field
        post.bookmarked_by.remove(user)

        # Return the response
        return Response(
            {"message": "Post unbookmarked successfully."},
            status=status.HTTP_200_OK,
        )


# BookmarkedPostsListAPIView class
class BookmarkedPostsListAPIView(generics.ListAPIView):
    """API view to list bookmarked posts.

    This view provides a list of posts bookmarked by the current user.

    Attributes:
        serializer_class (PostSerializer): The serializer class for the Post model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being returned.

    Methods:
        get_queryset: Get the queryset of bookmarked posts for the current user.
    """

    # Attributes
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "bookmarked_posts"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset of bookmarked posts for the current user.

        Returns:
            QuerySet: A queryset of Post objects bookmarked by the current user.
        """

        # Get the current user
        user = self.request.user

        # Return the queryset of bookmarked posts
        return Post.objects.filter(bookmarked_by=user)


# ReplyCreateAPIView class
class ReplyCreateAPIView(generics.CreateAPIView):
    """API view to create a new reply.

    This view handles the creation of new Reply objects.

    Attributes:
        queryset (QuerySet): The queryset of all Reply objects.
        serializer_class (ReplySerializer): The serializer class for the Reply model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being created.

    Methods:
        perform_create: Perform the creation of a new reply.
    """

    # Attributes
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "reply"

    # Method to perform the creation
    def perform_create(self, serializer: ReplySerializer) -> None:
        """Perform the creation of a new reply.

        Args:
            serializer (ReplySerializer): The serializer instance.
        """

        # Get the post ID from the URL
        post_id = self.kwargs.get("post_id")

        # Get the post object
        post = get_object_or_404(Post, id=post_id)

        # Get the current user
        user = self.request.user

        # Save the reply
        serializer.save(author=user, post=post)


# ReplyListAPIView class
class ReplyListAPIView(generics.ListAPIView):
    """API view to list replies for a specific post.

    This view provides a list of replies for a given post.

    Attributes:
        serializer_class (ReplySerializer): The serializer class for the Reply model.
        renderer_classes (tuple): The renderer classes for the API response.
        object_label (str): A label for the object type being returned.

    Methods:
        get_queryset: Get the queryset of replies for a specific post.
    """

    # Attributes
    serializer_class = ReplySerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "replies"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset of replies for a specific post.

        Returns:
            QuerySet: A queryset of Reply objects for the given post.
        """

        # Get the post ID from the URL
        post_id = self.kwargs.get("post_id")

        # Return the queryset of replies for the given post
        return Reply.objects.filter(post__id=post_id).order_by("-created_at")


# UpvotePostAPIView class
class UpvotePostAPIView(APIView):
    """API view to upvote a post.

    This view handles the upvoting of a post by a user.

    Methods:
        patch: Handle the PATCH request to upvote a post.
    """

    # Method to handle the PATCH request
    def patch(self, request: Request, post_id: str) -> Response:
        """Handle the PATCH request to upvote a post.

        Args:
            request (Request): The request object.
            post_id (str): The ID of the post to upvote.

        Returns:
            Response: The response indicating success or failure.
        """

        # Get the post object
        post = get_object_or_404(Post, id=post_id)

        # Create the serializer instance
        serializer = UpvotePostSerializer(
            post, data=request.data, context={"request": request}
        )

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serializer
            serializer.save()

            # Return the response
            return Response(
                {
                    "message": "Post upvoted successfully.",
                },
                status=status.HTTP_200_OK,
            )

        # Return the error response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# DownvotePostAPIView class
class DownvotePostAPIView(APIView):
    """API view to downvote a post.

    This view handles the downvoting of a post by a user.

    Methods:
        patch: Handle the PATCH request to downvote a post.
    """

    # Method to handle the PATCH request
    def patch(self, request: Request, post_id: str) -> Response:
        """Handle the PATCH request to downvote a post.

        Args:
            request (Request): The request object.
            post_id (str): The ID of the post to downvote.

        Returns:
            Response: The response indicating success or failure.
        """

        # Get the post object
        post = get_object_or_404(Post, id=post_id)

        # Create the serializer instance
        serializer = DownvotePostSerializer(post, data={}, context={"request": request})

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serializer
            serializer.save()

            # Return the response
            return Response(
                {
                    "message": "Post downvoted successfully.",
                },
                status=status.HTTP_200_OK,
            )

        # Return the error response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# PopularTagsListAPIView class
class PopularTagsListAPIView(generics.ListAPIView):
    """API view to list popular tags.

    This view provides a list of popular tags used in posts.

    Attributes:
        serializer_class (PopularTagSerializer): The serializer class for popular tags.
        renderer_classes (tuple): The renderer classes for the API response.
        permission_classes (tuple): The permission classes required to access this view.
        object_label (str): A label for the object type being returned.
    """

    # Attributes
    serializer_class = PopularTagSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "popular_tags"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of popular tags.

        Returns:
            QuerySet: A queryset of popular tags.
        """

        # Return the popular tags
        return Post.get_popular_tags()


# TopPostsListAPIView class
class TopPostsListAPIView(generics.ListAPIView):
    """API view to list top posts.

    This view provides a list of top posts based on upvotes, views, and replies.

    Attributes:
        serializer_class (TopPostSerialzier): The serializer class for top posts.
        renderer_classes (tuple): The renderer classes for the API response.
        permission_classes (tuple): The permission classes required to access this view.
        object_label (str): A label for the object type being returned.
    """

    # Attributes
    serializer_class = TopPostSerialzier
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "top_posts"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset of top posts.

        Returns:
            QuerySet: A queryset of top Post objects.
        """

        # Annotate and order the posts
        queryset = Post.objects.annotate(
            replies_count=Count("replies", distinct=True),
            view_count=Count("content_views", distinct=True),
        ).order_by("-upvotes", "-view_count", "-replies_count")[:6]

        # Return the queryset
        return queryset


# PostsByTagListAPIView class
class PostsByTagListAPIView(generics.ListAPIView):
    """API view to list posts by tag.

    This view provides a list of posts associated with a specific tag.

    Attributes:
        serializer_class (PostByTagSerializer): The serializer class for posts by tag.
        renderer_classes (tuple): The renderer classes for the API response.
        permission_classes (tuple): The permission classes required to access this view.
        object_label (str): A label for the object type being returned.
    """

    # Attributes
    serializer_class = PostByTagSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "posts_by_tag"

    # Method to get the queryset
    def get_queryset(self) -> QuerySet:
        """Get the queryset of posts for a specific tag.

        Returns:
            QuerySet: A queryset of Post objects associated with the given tag.
        """

        # Get the tag slug from the URL
        tag_slug = self.kwargs.get("tag_slug")

        # Return the queryset of posts for the given tag
        return Post.objects.filter(tags__slug=tag_slug).annotate(
            replies_count=Count("replies")
        )
