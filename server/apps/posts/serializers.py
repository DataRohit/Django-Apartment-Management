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


# PopularTagSerializer
class PopularTagSerializer(serializers.ModelSerializer):
    """PopularTagSerializer

    PopularTagSerializer class is used to serialize a popular tag.

    Extends:
        serializers.ModelSerializer

    Attributes:
        post_count (IntegerField): The number of posts with the tag.

    Meta Class:
        model (Tag): The Tag model.
    """

    # Attributes
    post_count = serializers.IntegerField(read_only=True)

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Tag): The Tag model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Tag
        fields = ["name", "slug", "post_count"]


# TopPostSerialzier
class TopPostSerialzier(serializers.ModelSerializer):
    """TopPostSerialzier

    TopPostSerialzier class is used to serialize a top post.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username (CharField): The username of the author.
        replies_count (IntegerField): The number of replies.
        view_count (IntegerField): The number of views.
        avatar (SerializerMethodField): The avatar of the author.

    Meta Class:
        model (Post): The Post model.
        fields (list): The fields to include in the serialized data.

    Methods:
        get_avatar(obj: Post) -> str | None: Get the avatar of the author.
    """

    # Attributes
    author_username = serializers.CharField(source="author.username", read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    avatar = serializers.SerializerMethodField()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Post): The Post model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
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

    # Method to get the avatar of the author
    def get_avatar(self, obj: Post) -> str | None:
        """Get the avatar of the author.

        Args:
            obj (Post): The post.

        Returns:
            str | None: The avatar of the author.
        """

        # If the author has an avatar
        if obj.author.profile.avatar:
            # Return the avatar
            return obj.author.profile.avatar.url

        # Return None
        return None


# ReplySerializer
class ReplySerializer(serializers.ModelSerializer):
    """ReplySerializer

    ReplySerializer class is used to serialize a reply.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username (CharField): The username of the author.
        post (PrimaryKeyRelatedField): The post.
        avatar (SerializerMethodField): The avatar of the author.

    Meta Class:
        model (Reply): The Reply model.
        fields (list): The fields to include in the serialized data.
        read_only_fields (list): The fields that are read-only.

    Methods:
        get_avatar(obj: Post) -> str | None: Get the avatar of the author.
    """

    # Attributes
    author_username = serializers.CharField(source="author.username", read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    avatar = serializers.SerializerMethodField()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Reply): The Reply model.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that are read-only.
        """

        # Attributes
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

    # Method to get the avatar of the author
    def get_avatar(self, obj: Post) -> str | None:
        """Get the avatar of the author.

        Args:
            obj (Post): The post.

        Returns:
            str | None: The avatar of the author.
        """

        # If the author has an avatar
        if obj.author.profile.avatar:
            # Return the avatar
            return obj.author.profile.avatar.url

        # Return None
        return None


# UpvotePostSerializer
class UpvotePostSerializer(serializers.ModelSerializer):
    """UpvotePostSerializer

    UpvotePostSerializer class is used to serialize an upvote post request.

    Extends:
        serializers.ModelSerializer

    Meta Class:
        model (Post): The Post model.
        fields (list): The fields to include in the serialized data.

    Methods:
        update(instance: Post, validated_data: dict) -> Post: Update the post.
    """

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Post): The Post model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Post
        fields = []

    # Method to update the post
    def update(self, instance: Post, validated_data: dict) -> Post:
        """Update the post.

        Args:
            instance (Post): The post instance.
            validated_data (dict): The validated data.

        Returns:
            Post: The updated post.

        Raises:
            Exception: If the email sending fails.
        """

        # Get the user
        user = self.context.get("request").user

        # If the user has not upvoted the post
        if user not in instance.upvoted_by.all():
            # Add the user to the upvoted by list
            instance.upvoted_by.add(user)

            # Update the upvotes
            instance.upvotes = F("upvotes") + 1

            # Save the instance
            instance.save()

        # Return the instance
        return instance


# DownvotePostSerializer
class DownvotePostSerializer(serializers.ModelSerializer):
    """DownvotePostSerializer

    DownvotePostSerializer class is used to serialize a downvote post request.

    Extends:
        serializers.ModelSerializer

    Meta Class:
        model (Post): The Post model.
        fields (list): The fields to include in the serialized data.

    Methods:
        update(instance: Post, validated_data: dict) -> Post: Update the post.
    """

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Post): The Post model.
            fields (list): The fields to include in the serialized data.
        """

        # Attributes
        model = Post
        fields = []

    # Method to update the post
    def update(self, instance: Post, validated_data: dict) -> Post:
        """Update the post.

        Args:
            instance (Post): The post instance.
            validated_data (dict): The validated data.

        Returns:
            Post: The updated post.
        """

        # Get the user
        user = self.context.get("request").user

        # If the user has not downvoted the post
        if user in instance.upvoted_by.all():
            # Add the user to the downvoted by list
            instance.upvoted_by.remove(user)

            # Update the upvotes
            instance.upvotes = F("upvotes") - 1

        # If the user has not downvoted the post
        if user not in instance.downvoted_by.all():
            # Add the user to the downvoted by list
            instance.downvoted_by.add(user)

            # Update the downvotes
            instance.downvotes = F("downvotes") + 1

        # Else
        else:
            # Remove the user from the downvoted by list
            instance.downvoted_by.remove(user)

            # Update the downvotes
            instance.downvotes = F("downvotes") - 1

        # Save the instance and refresh from the database
        instance.save()
        instance.refresh_from_db()

        # Return the instance
        return instance


# BasePostSerializer
class BasePostSerializer(serializers.ModelSerializer):
    """BasePostSerializer

    BasePostSerializer class is used to serialize a base post.

    Extends:
        serializers.ModelSerializer

    Attributes:
        author_username (ReadOnlyField): The username of the author.
        is_bookmarked (SerializerMethodField): The bookmark status.
        created_at (SerializerMethodField): The created date.
        updated_at (SerializerMethodField): The updated date.
        view_count (SerializerMethodField): The view count.
        is_upvoted (SerializerMethodField): The upvote status.
        replies_count (IntegerField): The number of replies.
        avatar (SerializerMethodField): The avatar of the author.

    Meta Class:
        model (Post): The Post model.
        fields (list): The fields to include in the serialized data.
        read_only_fields (list): The fields that are read-only.

    Methods:
        get_is_bookmarked(obj: Post) -> bool: Get the bookmark status.
        get_created_at(obj: Post) -> str: Get the created date.
        get_updated_at(obj: Post) -> str: Get the updated date.
        get_view_count(obj: Post) -> int: Get the view count.
        get_is_upvoted(obj: Post) -> bool: Get the upvote status.
        get_avatar(obj: Post) -> str | None: Get the avatar of the author.
    """

    # Attributes
    author_username = serializers.ReadOnlyField(source="author.username")
    is_bookmarked = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    is_upvoted = serializers.SerializerMethodField()
    replies_count = serializers.IntegerField(read_only=True)
    avatar = serializers.SerializerMethodField()

    # Meta Class
    class Meta:
        """Meta Class

        Attributes:
            model (Post): The Post model.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that are read-only.
        """

        # Attributes
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

    # Method to get the bookmark status
    def get_is_bookmarked(self, obj: Post) -> bool:
        """Get the bookmark status.

        Args:
            obj (Post): The post.

        Returns:
            bool: The bookmark status.
        """

        # Get the user
        user = self.context.get("request").user

        # If the user is authenticated
        if user.is_authenticated:
            # Return the bookmark status
            return obj.bookmarked_by.filter(id=user.id).exists()

        # Return false
        return False

    # Method to get the created date
    def get_created_at(self, obj: Post) -> str:
        """Get the created date.

        Args:
            obj (Post): The post.

        Returns:
            str: The created date.
        """

        # Return the created date
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    # Method to get the updated date
    def get_updated_at(self, obj: Post) -> str:
        """Get the updated date.

        Args:
            obj (Post): The post.

        Returns:
            str: The updated date.
        """

        # Return the updated date
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    # Method to get the view count
    def get_view_count(self, obj: Post) -> int:
        """Get the view count.

        Args:
            obj (Post): The post.

        Returns:
            int: The view count.
        """

        # Get the content type
        content_type = ContentType.objects.get_for_model(obj)

        # Get the view count
        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

    # Method to get the upvote status
    def get_is_upvoted(self, obj: Post) -> bool:
        """Get the upvote status.

        Args:
            obj (Post): The post.

        Returns:
            bool: The upvote status.
        """

        # Get the user
        user = self.context.get("request").user

        # If the user is authenticated
        if user.is_authenticated:
            # Return the upvote status
            return obj.upvoted_by.filter(id=user.id).exists()

        # Return false
        return False

    # Method to get the avatar of the author
    def get_avatar(self, obj: Post) -> str | None:
        """Get the avatar of the author.

        Args:
            obj (Post): The post.

        Returns:
            str | None: The avatar of the author.
        """

        # If the author has an avatar
        if obj.author.profile.avatar:
            # Return the avatar
            return obj.author.profile.avatar.url

        # Return None
        return None


# PostSerializer
class PostSerializer(TaggitSerializer, BasePostSerializer):
    """PostSerializer

    PostSerializer class is used to serialize a post.

    Extends:
        BasePostSerializer
        TaggitSerializer

    Attributes:
        tags (TagListSerializerField): The tags.
        replies (ReplySerializer): The replies.

    Meta Class:
        fields (list): The fields to include in the serialized data.

    Methods:
        create(validated_data: dict) -> Post: Create the post.
        update(instance: Post, validated_data: dict) -> Post: Update the post.
    """

    # Attributes
    tags = TagListSerializerField()
    replies = ReplySerializer(many=True, read_only=True)

    # Meta Class
    class Meta(BasePostSerializer.Meta):
        """Meta Class

        Args:
            BasePostSerializer (_type_): The base post serializer.
        """

        # Attributes
        fields = BasePostSerializer.Meta.fields + ["body", "tags", "replies"]

    # Method to create the post
    def create(self, validated_data: dict) -> Post:
        """Create the post.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Post: The created post.
        """

        # Get the tags
        tags = validated_data.pop("tags")

        # Get the user
        user = self.context.get("request").user

        # Create the post
        post = Post.objects.create(author=user, **validated_data)

        # Add the tags
        post.tags.set(tags)

        # Return the post
        return post

    # Method to update the post
    def update(self, instance: Post, validated_data: dict) -> Post:
        """Update the post.

        Args:
            instance (Post): The post instance.
            validated_data (dict): The validated data.

        Returns:
            Post: The updated post.
        """

        # Get the tags
        tags = validated_data.pop("tags", None)

        # Traverse the validated data
        for attr, value in validated_data.items():
            # Set the attribute
            setattr(instance, attr, value)

        # If tags is not None
        if tags is not None:
            # Set the tags
            instance.tags.set(tags)

        # Save the instance
        instance.save()

        # Return the instance
        return instance


# PostByTagSerializer
class PostByTagSerializer(TaggitSerializer, BasePostSerializer):
    """PostByTagSerializer

    PostByTagSerializer class is used to serialize a post by tag.

    Extends:
        TaggitSerializer
        BasePostSerializer

    Attributes:
        tags (TagListSerializerField): The tags.

    Meta Class:
        fields (list): The fields to include in the serialized data.
    """

    # Attributes
    tags = TagListSerializerField()

    # Meta Class
    class Meta(BasePostSerializer.Meta):
        """Meta Class

        Args:
            BasePostSerializer (_type_): The base post serializer.
        """

        # Attributes
        fields = BasePostSerializer.Meta.fields + ["body", "tags"]
