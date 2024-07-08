# Imports
from apps.common.models import ContentView
from apps.posts.models import Post, Reply
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField


# Get the user model
User = get_user_model()


class PopularTagSerializer(serializers.ModelSerializer):
    """Popular tag serializer.

    This class is used to serialize a popular tag.

    Extends:
        serializers.ModelSerializer

    Attributes:
        post_count: int -- The number of posts with the tag.

    Meta:
        model: Tag -- The tag model.
        fields: list -- The fields to serialize.
    """

    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Meta class for the PopularTagSerializer.

        Attributes:
            model: Tag -- The tag model.
            fields: list -- The fields to serialize.
        """

        model = Tag
        fields = ["name", "slug", "post_count"]


class TopPostSerialzier(serializers.ModelSerializer):
    """Top post serializer.

    This class is used to serialize a top post.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username: str -- The username of the author.
        replies_count: int -- The number of replies.
        view_count: int -- The number of views.
        avatar: str | None -- The avatar of the author.

    Meta:
        model: Post -- The post model.
        fields: list -- The fields to serialize.

    Methods:
        get_avatar: Gets the avatar of the author.
    """

    author_username = serializers.CharField(source="author.username", read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the TopPostSerialzier.

        Attributes:
            model: Post -- The post model.
            fields: list -- The fields to serialize.
        """

        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author_username",
            "upvotes",
            "view_count",
            "replies_count",
            "avatar",
            "created_at",
        ]

    def get_avatar(self, obj: Post) -> str | None:
        """Method to get the avatar of the author.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            str | None: The avatar of the author.
        """

        if obj.author.profile.avatar:
            return obj.author.profile.avatar.url

        return None


class ReplySerializer(serializers.ModelSerializer):
    """Reply serializer.

    This class is used to serialize a reply.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username: str -- The username of the author.
        post: uuid4 -- The ID of the post.
        avatar: str | None -- The avatar of the author.

    Meta:
        model: Reply -- The reply model.
        fields: list -- The fields to serialize.
        read_only_fields: list -- The fields that are read only.

    Methods:
        get_avatar: Gets the avatar of the author.
    """

    author_username = serializers.CharField(source="author.username", read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the ReplySerializer.

        Attributes:
            model: Reply -- The reply model.
            fields: list -- The fields to serialize.
            read_only_fields: list -- The fields that are read only.
        """

        model = Reply
        fields = [
            "id",
            "post",
            "author_username",
            "body",
            "avatar",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author_username", "created_at", "updated_at"]

    def get_avatar(self, obj: Post) -> str | None:
        """Method to get the avatar of the author.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            str | None: The avatar of the author.
        """

        if obj.author.profile.avatar:
            return obj.author.profile.avatar.url

        return None


class UpvotePostSerializer(serializers.ModelSerializer):
    """Upvote post serializer.

    This class is used to serialize an upvote on a post.

    Extends:
        serializers.ModelSerializer

    Meta:
        model: Post -- The post model.
        fields: list -- The fields to serialize.

    Methods:
        update: Updates the post with an upvote.
    """

    class Meta:
        """Meta class for the UpvotePostSerializer.

        Attributes:
            model: Post -- The post model.
            fields: list -- The fields to serialize.
        """

        model = Post
        fields = []

    def update(self, instance: Post, validated_data: dict) -> Post:
        """Method to update the post with an upvote.

        Arguments:
            instance: Post -- The post instance.
            validated_data: dict -- The validated data.

        Returns:
            Post: The updated post.
        """

        user = self.context.get("request").user

        if user not in instance.upvoted_by.all():
            instance.upvoted_by.add(user)
            instance.upvotes = F("upvotes") + 1
            instance.save()

        return instance


class DownvotePostSerializer(serializers.ModelSerializer):
    """Downvote post serializer.

    This class is used to serialize an downvote on a post.

    Extends:
        serializers.ModelSerializer

    Meta:
        model: Post -- The post model.
        fields: list -- The fields to serialize.

    Methods:
        update: Updates the post with an downvote.
    """

    class Meta:
        """Meta class for the DownvotePostSerializer.

        Attributes:
            model: Post -- The post model.
            fields: list -- The fields to serialize.
        """

        model = Post
        fields = []

    def update(self, instance: Post, validated_data: dict) -> Post:
        """Method to update the post with an downvote.

        Arguments:
            instance: Post -- The post instance.
            validated_data: dict -- The validated data.

        Returns:
            Post: The updated post.
        """

        user = self.context.get("request").user

        if user in instance.upvoted_by.all():
            instance.upvoted_by.remove(user)
            instance.upvotes = F("upvotes") - 1

        if user not in instance.downvoted_by.all():
            instance.downvoted_by.add(user)
            instance.downvotes = F("downvotes") + 1

        else:
            instance.downvoted_by.remove(user)
            instance.downvotes = F("downvotes") - 1

        instance.save()
        instance.refresh_from_db()

        return instance


class BasePostSerializer(serializers.ModelSerializer):
    """Base post serializer.

    This class is used to serialize a post.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username: str -- The username of the author.
        is_bookmarked: bool -- True if the post is bookmarked by the user, False otherwise.
        created_at: str -- The created_at field.
        updated_at: str -- The updated_at field.
        view_count: int -- The view_count field.
        is_upvoted: bool -- True if the post is upvoted by the user, False otherwise.
        replies_count: int -- The number of replies.
        avatar: str | None -- The avatar of the author.

    Meta:
        model: Post -- The post model.
        fields: list -- The fields to serialize.
        read_only_fields: list -- The fields that are read only.

    Methods:
        get_is_bookmarked: Gets the is_bookmarked field.
        get_created_at: Gets the created_at field.
        get_updated_at: Gets the updated_at field.
        get_view_count: Gets the view_count field.
        get_is_upvoted: Gets the is_upvoted field.
        get_avatar: Gets the avatar of the author.
    """

    author_username = serializers.ReadOnlyField(source="author.username")
    is_bookmarked = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    is_upvoted = serializers.SerializerMethodField()
    replies_count = serializers.IntegerField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the BasePostSerializer.

        Attributes:
            model: Post -- The post model.
            fields: list -- The fields to serialize.
            read_only_fields: list -- The fields that are read only.
        """

        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author_username",
            "is_bookmarked",
            "created_at",
            "updated_at",
            "view_count",
            "upvotes",
            "downvotes",
            "is_upvoted",
            "replies_count",
            "avatar",
        ]
        read_only_fields = ["id", "slug", "author_username", "created_at", "updated_at"]

    def get_is_bookmarked(self, obj: Post) -> bool:
        """Method to get the is_bookmarked field.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            bool: True if the post is bookmarked by the user, False otherwise.
        """

        user = self.context.get("request").user

        if user.is_authenticated:
            return obj.bookmarked_by.filter(id=user.id).exists()

        return False

    def get_created_at(self, obj: Post) -> str:
        """Method to get the created_at field.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            str: The created_at field.
        """

        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj: Post) -> str:
        """Method to get the updated_at field.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            str: The updated_at field.
        """

        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_view_count(self, obj: Post) -> int:
        """Method to get the view_count field.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            int: The view_count field.
        """

        content_type = ContentType.objects.get_for_model(obj)

        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

    def get_is_upvoted(self, obj: Post) -> bool:
        """Method to get the is_upvoted field.

        Arguments:
            obj: Post -- The post instance.

        Returns:
            bool: True if the post is upvoted by the user, False otherwise.
        """

        user = self.context.get("request").user

        if user.is_authenticated:
            return obj.upvoted_by.filter(id=user.id).exists()

        return False

    def get_avatar(self, obj: Post) -> str | None:
        """Method to get the avatar of the author.

        Arguments:
            obj: Post -- The post instance.
        """

        if obj.author.profile.avatar:
            return obj.author.profile.avatar.url

        return None


class PostSerializer(TaggitSerializer, BasePostSerializer):
    """Post serializer.

    This class is used to serialize a post.

    Extends:
        TaggitSerializer
        BasePostSerializer

    Attributes:
        tags: TagListSerializerField -- The tags of the post.
        replies: ReplySerializer -- The replies of the post.

    Meta:
        fields: list -- The fields to serialize.

    Methods:
        create: Creates a post.
        update: Updates a post.
    """

    tags = TagListSerializerField()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta(BasePostSerializer.Meta):
        """Meta class for the PostSerializer.

        Attributes:
            fields: list -- The fields to serialize.
        """

        fields = BasePostSerializer.Meta.fields + ["body", "tags", "replies"]

    def create(self, validated_data: dict) -> Post:
        """Method to create a post.

        Arguments:
            validated_data: dict -- The validated data.

        Returns:
            Post: The created post.
        """

        tags = validated_data.pop("tags")
        user = self.context.get("request").user

        post = Post.objects.create(author=user, **validated_data)
        post.tags.set(tags)

        return post

    def update(self, instance: Post, validated_data: dict) -> Post:
        """Method to update a post.

        Arguments:
            instance: Post -- The post instance.
            validated_data: dict -- The validated data.

        Returns:
            Post: The updated post.
        """

        tags = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags is not None:
            instance.tags.set(tags)
        instance.save()

        return instance


class PostByTagSerializer(TaggitSerializer, BasePostSerializer):
    """Post by tag serializer.

    This class is used to serialize a post by tag.

    Extends:
        TaggitSerializer
        BasePostSerializer

    Attributes:
        tags: TagListSerializerField -- The tags of the post.

    Meta:
        fields: list -- The fields to serialize.
    """

    tags = TagListSerializerField()

    class Meta(BasePostSerializer.Meta):
        """Meta class for the PostByTagSerializer.

        Attributes:
            fields: list -- The fields to serialize.
        """

        fields = BasePostSerializer.Meta.fields + ["body", "tags"]
