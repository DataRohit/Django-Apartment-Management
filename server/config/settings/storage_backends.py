# Imports
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


# Custom storage backend for S3
class CustomS3Boto3Storage(S3Boto3Storage):
    # Constructor
    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Set the endpoint URL and custom domain
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    # Method to return the URL of the file
    def url(self, name, parameters=None, expire=None):
        # Get the URL
        url = super().url(name, parameters, expire)

        # If the urls starts with https
        if url.startswith('https'):
            # Replace https with http
            url = 'http' + url[5:]

        # Return the URL
        return url


# Custom storage backend for static files
class StaticStorage(CustomS3Boto3Storage):
    location = "static"
    default_acl = "private"
    file_overwrite = False


# Custom storage backend for media files
class MediaStorage(CustomS3Boto3Storage):
    location = "media"
    default_acl = "private"
    file_overwrite  = False
