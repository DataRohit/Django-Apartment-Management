# Generated by Django 4.2.13 on 2024-07-28 03:26

import autoslug.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
            ],
            options={
                "verbose_name": "Reply",
                "verbose_name_plural": "Replies",
            },
        ),
    ]
