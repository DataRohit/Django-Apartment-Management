# Generated by Django 4.2.13 on 2024-07-28 03:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rating",
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
                (
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "Very Poor"),
                            (2, "Poor"),
                            (3, "Average"),
                            (4, "Good"),
                            (5, "Excellent"),
                        ],
                        verbose_name="Rating",
                    ),
                ),
                ("comment", models.TextField(blank=True, verbose_name="Comment")),
            ],
            options={
                "verbose_name": "Rating",
                "verbose_name_plural": "Ratings",
            },
        ),
    ]
