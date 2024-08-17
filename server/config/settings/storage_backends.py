# Imports
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Custom storage backend for S3
class CustomS3Boto3Storage(S3Boto3Storage):
    """Custom S3 Boto3 Storage

    CustomS3Boto3Storage class is used to create a custom storage backend for S3.

    Extends:
        S3Boto3Storage

    Attributes:
        endpoint_url (str): The endpoint URL of the S3 bucket.
        custom_domain (str): The custom domain of the S3 bucket.

    Methods:
        url: Get the URL of the file.
    """

    # Constructor
    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Set the endpoint URL and custom domain
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    # Method to return the URL of the file
    def url(self, name, parameters=None, expire=None):
        """Get the URL of the file.

        Args:
            name (str): The name of the file.
            parameters (dict): The parameters for the URL.
            expire (int): The expiration time for the URL.

        Returns:
            str: The URL of the file.
        """

        # Get the URL
        url = super().url(name, parameters, expire)

        # If the urls starts with https
        if url.startswith("https"):
            # Replace https with http
            url = "http" + url[5:]

        # Return the URL
        return url


# Custom storage backend for static files
class StaticStorage(CustomS3Boto3Storage):
    """Custom Static Storage

    CustomStaticStorage class is used to create a custom storage backend for static files.

    Extends:
        CustomS3Boto3Storage

    Attributes:
        location (str): The location of the static files.
        default_acl (str): The default ACL for the static files.
        file_overwrite (bool): Whether to overwrite the file if it already exists.
    """

    # Attributes
    location = "static"
    default_acl = "private"
    file_overwrite = False


# Custom storage backend for media files
class MediaStorage(CustomS3Boto3Storage):
    """Custom Media Storage

    CustomMediaStorage class is used to create a custom storage backend for media files.

    Extends:
        CustomS3Boto3Storage

    Attributes:
        location (str): The location of the media files.
        default_acl (str): The default ACL for the media files.
        file_overwrite (bool): Whether to overwrite the file if it already exists.
    """

    # Attributes
    location = "media"
    default_acl = "private"
    file_overwrite = False
