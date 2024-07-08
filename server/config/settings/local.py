# Imports
from .base import *
from .base import INSTALLED_APPS, env


# General
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="QTMT8ZsZaDOSmVFhCTmJULzMu1DLNxbqoKKAGBsFwUwQKRjIzXYyeKCeRRqvGn23",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://0.0.0.0:8080',
    'http://127.0.0.1:8080',
]
SITE_NAME = "Alpha Apartments"


# Caches
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": BASE_DIR / ".cache",
    },
}


# MinIO settings
# ------------------------------------------------------------------------------
MINIO_STORAGE_ENDPOINT = env("MINIO_STORAGE_ENDPOINT")
MINIO_STORAGE_ACCESS_KEY = env("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = env("MINIO_STORAGE_SECRET_KEY")
MINIO_STORAGE_USE_HTTPS = False


# AWS S3 settings (assuming MinIO setup)
# ------------------------------------------------------------------------------
AWS_S3_ENDPOINT_URL = f"http://{MINIO_STORAGE_ENDPOINT}"
AWS_ACCESS_KEY_ID = MINIO_STORAGE_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_STORAGE_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = "alpha-apartments"
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "private"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True
AWS_S3_CUSTOM_DOMAIN = f"localhost:8080/minio/storage/{AWS_STORAGE_BUCKET_NAME}"


# Static files settings
# ------------------------------------------------------------------------------
STATIC_URL = f"http://localhost:8080/alpha-apartments/static/"
STATICFILES_STORAGE = "config.settings.storage_backends.StaticStorage"


# Media files settings
# ------------------------------------------------------------------------------
MEDIA_URL = f"http://localhost:8080/alpha-apartments/media/"
DEFAULT_FILE_STORAGE = "config.settings.storage_backends.MediaStorage"


# Static files finders and directories
# ------------------------------------------------------------------------------
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Email
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND")
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_PORT = env("DJANGO_EMAIL_PORT")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")


# Django Extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]


# Celery
# ------------------------------------------------------------------------------
CELERY_TASK_EAGER_PROPAGATES = True
