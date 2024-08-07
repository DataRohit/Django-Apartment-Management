# Generated by Django 4.2.13 on 2024-07-08 14:29

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Title")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        always_update=True,
                        editable=False,
                        populate_from="title",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                ("body", models.TextField(verbose_name="Body")),
                (
                    "upvotes",
                    models.PositiveIntegerField(default=0, verbose_name="Upvotes"),
                ),
                (
                    "downvotes",
                    models.PositiveIntegerField(default=0, verbose_name="Downvotes"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "bookmarked_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="bookmarked_posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Bookmarked by",
                    ),
                ),
                (
                    "downvoted_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="downvoted_posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Downvoted by",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "upvoted_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="upvoted_posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Upvoted by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.CreateModel(
            name="Reply",
            fields=[
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                ("body", models.TextField(verbose_name="Reply")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="posts.post",
                        verbose_name="Post",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reply",
                "verbose_name_plural": "Replies",
            },
        ),
    ]
