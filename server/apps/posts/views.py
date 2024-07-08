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


class StandardResultsSetPagination(PageNumberPagination):
    """Standard results set pagination class.

    Extends:
        PageNumberPagination

    Attributes:
        page_size: int -- The page size.
        page_size_query_param: str -- The page size query param.
        max_page_size: int -- The max page size.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostListAPIView(generics.ListAPIView):
    """Post list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: PostSerializer -- The post serializer class.
        filterset_class: PostFilter -- The post filter class.
        pagination_class: StandardResultsSetPagination -- The standard results set pagination class.
        permission_classes: List -- The list of permission classes.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the query set.
    """

    serializer_class = PostSerializer
    filterset_class = PostFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (GenericJSONRenderer,)
    object_label = "posts"

    def get_queryset(self) -> QuerySet:
        """Method to get the query set.

        This method gets the query set and annotates the replies count.

        Returns:
            QuerySet: The query set.
        """

        return Post.objects.annotate(replies_count=Count("replies")).order_by(
            "-upvotes", "-created_at"
        )


class MyPostListAPIView(generics.ListAPIView):
    """My post list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: PostSerializer -- The post serializer class.
        filterset_class: PostFilter -- The post filter class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
    """

    serializer_class = PostSerializer
    filterset_class = PostFilter
    renderer_classes = (GenericJSONRenderer,)
    object_label = "my_posts"

    def get_queryset(self) -> QuerySet:
        """Method to get the query set.

        This method gets the query set and filters the posts by the current user.

        Returns:
            QuerySet: The query set.
        """

        return Post.objects.filter(author=self.request.user).order_by(
            "-upvotes", "-created_at"
        )


class PostDetailAPIView(generics.RetrieveAPIView):
    """Post detail api view class.

    Extends:
        generics.RetrieveAPIView

    Attributes:
        serializer_class: PostSerializer -- The post serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
        lookup_field: str -- The lookup field.

    Methods:
        get_queryset: Method to get the query set.
        get_object: Method to get the object.
        record_post_view: Method to record the post view.
        get_client_ip: Method to get the client ip.
    """

    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet:
        """Method to get the query set.

        This method gets the query set and annotates the replies count.

        Returns:
            QuerySet: The query set.
        """

        return Post.objects.annotate(replies_count=Count("replies"))

    def get_object(self):
        """Method to get the object.

        This method gets the post object.

        Returns:
            Post: The post object.
        """

        queryset = self.get_queryset()

        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}

        post = get_object_or_404(queryset, **filter_kwargs)
        self.record_post_view(post)

        return post

    def record_post_view(self, post: Post) -> None:
        """Method to record the post view.

        This method records the post view for the current user.

        Arguments:
            post: Post -- The post object.
        """

        content_type = ContentType.objects.get_for_model(Post)

        viewer_ip = self.get_client_ip()

        obj, created = ContentView.objects.get_or_create(
            content_type=content_type,
            object_id=post.pk,
            viewer_ip=viewer_ip,
            user=self.request.user,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    def get_client_ip(self) -> str:
        """Method to get the client ip.

        This method gets the client ip address.

        Returns:
            str: The client ip address.
        """

        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        return ip


class PostCreateAPIView(generics.CreateAPIView):
    """Post create api view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset: QuerySet -- The query set.
        serializer_class: PostSerializer -- The post serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
        permission_classes: List -- The list of permission classes.

    Methods:
        perform_create: Method to perform the create.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    permission_classes = (CanCreateEditPost,)

    def perform_create(self, serializer: PostSerializer) -> None:
        """Method to perform the create.

        This method saves the post and sets the author field to the current user.

        Arguments:
            serializer: PostSerializer -- The post serializer.
        """

        serializer.save()


class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Post update api view class.

    Extends:
        generics.RetrieveUpdateAPIView

    Attributes:
        queryset: QuerySet -- The query set.
        serializer_class: PostSerializer -- The post serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.
        permission_classes: List -- The list of permission classes.
        lookup_field: str -- The lookup field.

    Methods:
        get_object: Method to get the object.
        perform_update: Method to perform the update.
        update: Method to update the post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "post"
    permission_classes = (CanCreateEditPost,)
    lookup_field = "slug"

    def get_object(self):
        """Method to get the object.

        This method gets the post object.

        Returns:
            Post: The post object.
        """

        post = super().get_object()

        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")

        return post

    def perform_update(self, serializer: PostSerializer) -> None:
        """Method to perform the update.

        This method saves the post and sets the updated_at field to the current time.

        Arguments:
            serializer: PostSerializer -- The post serializer.
        """

        super().perform_update(serializer)

        self.post_instance = serializer.instance

    def update(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Method to update the post.

        This method updates the post and returns the updated post.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- The arguments.
            **kwargs: Dict -- The keyword arguments.

        Returns:
            Response: The response object.
        """

        super().update(request, *args, **kwargs)

        post_with_replies_count = Post.objects.annotate(
            replies_count=Count("replies")
        ).get(pk=self.post_instance.pk)

        response = self.get_serializer(post_with_replies_count).data

        return Response(response)


class BookmarkPostAPIView(APIView):
    """Bookmark post api view class.

    Extends:
        APIView

    Methods:
        patch: Method to handle the patch request.
    """

    def patch(self, request: Request, slug: str) -> Response:
        """Method to handle the patch request.

        This method bookmarks the post for the user.

        Arguments:
            request: Request -- The request object.
            slug: str -- The post slug.

        Returns:
            Response: The response object.
        """

        user = request.user

        post = get_object_or_404(Post.objects, slug=slug)

        if user in post.bookmarked_by.all():
            return Response(
                {"message": "Post already bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.bookmarked_by.add(user)

        return Response(
            {"message": "Post bookmarked successfully."},
            status=status.HTTP_200_OK,
        )


class UnbookmarkPostAPIView(APIView):
    """Unbookmark post api view class.

    Extends:
        APIView

    Methods:
        patch: Method to handle the patch request.
    """

    def patch(self, request: Request, slug: str) -> Response:
        """Method to handle the patch request.

        This method unbookmarks the post for the user.

        Arguments:
            request: Request -- The request object.
            slug: str -- The post slug.

        Returns:
            Response: The response object.
        """

        user = request.user

        post = get_object_or_404(Post, slug=slug)

        if user not in post.bookmarked_by.all():
            return Response(
                {"message": "Post not bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.bookmarked_by.remove(user)

        return Response(
            {"message": "Post unbookmarked successfully."},
            status=status.HTTP_200_OK,
        )


class BookmarkedPostsListAPIView(generics.ListAPIView):
    """Bookmarked posts list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: PostSerializer -- The post serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = PostSerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "bookmarked_posts"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method gets the bookmarked posts for the user.

        Returns:
            QuerySet: The query set.
        """

        user = self.request.user

        return Post.objects.filter(bookmarked_by=user)


class ReplyCreateAPIView(generics.CreateAPIView):
    """Reply create api view class.

    Extends:
        generics.CreateAPIView

    Attributes:
        queryset: QuerySet -- The query set.
        serializer_class: ReplySerializer -- The reply serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        perform_create: Method to perform the create.
    """

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "reply"

    def perform_create(self, serializer: ReplySerializer) -> None:
        """Method to perform the create.

        This method saves the reply and sets the author field to the current user.

        Arguments:
            serializer: ReplySerializer -- The reply serializer.
        """

        post_id = self.kwargs.get("post_id")

        post = get_object_or_404(Post, id=post_id)
        user = self.request.user

        serializer.save(author=user, post=post)


class ReplyListAPIView(generics.ListAPIView):
    """Reply list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: ReplySerializer -- The reply serializer class.
        renderer_classes: List -- The list of renderer classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = ReplySerializer
    renderer_classes = (GenericJSONRenderer,)
    object_label = "replies"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method gets the replies for the post.

        Returns:
            QuerySet: The query set.
        """

        post_id = self.kwargs.get("post_id")

        return Reply.objects.filter(post__id=post_id).order_by("-created_at")


class UpvotePostAPIView(APIView):
    """Upvote post api view class.

    Extends:
        APIView

    Methods:
        patch: Method to handle the patch method.
    """

    def patch(self, request: Request, post_id: str) -> Response:
        """Method to handle the patch method.

        This method upvotes the post.

        Arguments:
            request: Request -- The request object.
            post_id: str -- The post id.

        Returns:
            Response: The response object.
        """

        post = get_object_or_404(Post, id=post_id)

        serializer = UpvotePostSerializer(
            post, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Post upvoted successfully.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DownvotePostAPIView(APIView):
    """Downvote post api view class.

    Extends:
        APIView

    Methods:
        patch: Method to handle the patch method.
    """

    def patch(self, request: Request, post_id: str) -> Response:
        """Method to handle the patch method.

        This method downvotes the post.

        Arguments:
            request: Request -- The request object.
            post_id: str -- The post id.

        Returns:
            Response: The response object.
        """

        post = get_object_or_404(Post, id=post_id)

        serializer = DownvotePostSerializer(post, data={}, context={"request": request})

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Post downvoted successfully.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class PopularTagsListAPIView(generics.ListAPIView):
    """Popular tags list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: PopularTagSerializer -- The popular tag serializer class.
        renderer_classes: List -- The list of renderer classes.
        permission_classes: List -- The list of permission classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = PopularTagSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "popular_tags"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method gets the popular tags.

        Returns:
            QuerySet: The query set.
        """

        return Post.get_popular_tags()


class TopPostsListAPIView(generics.ListAPIView):
    """Top posts list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: TopPostSerializer -- The top post serializer class.
        renderer_classes: List -- The list of renderer classes.
        permission_classes: List -- The list of permission classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = TopPostSerialzier
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "top_posts"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method gets the top posts.

        Returns:
            QuerySet: The query set.
        """

        queryset = Post.objects.annotate(
            replies_count=Count("replies", distinct=True),
            view_count=Count("content_views", distinct=True),
        ).order_by("-upvotes", "-view_count", "-replies_count")[:6]

        return queryset


class PostsByTagListAPIView(generics.ListAPIView):
    """Posts by tag list api view class.

    Extends:
        generics.ListAPIView

    Attributes:
        serializer_class: PostByTagSerializer -- The post by tag serializer class.
        renderer_classes: List -- The list of renderer classes.
        permission_classes: List -- The list of permission classes.
        object_label: str -- The object label.

    Methods:
        get_queryset: Method to get the queryset.
    """

    serializer_class = PostByTagSerializer
    renderer_classes = (GenericJSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    object_label = "posts_by_tag"

    def get_queryset(self) -> QuerySet:
        """Method to get the queryset.

        This method gets the posts by tag.

        Returns:
            QuerySet: The query set.
        """

        tag_slug = self.kwargs.get("tag_slug")

        return Post.objects.filter(tags__slug=tag_slug).annotate(
            replies_count=Count("replies")
        )
