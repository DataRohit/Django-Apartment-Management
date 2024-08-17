# Imports
import logging
from typing import Optional, Tuple

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token

# Get the logger
logger = logging.getLogger(__name__)


# CookieAuthentication Class
class CookieAuthentication(JWTAuthentication):
    """CookieAuthentication

    CookieAuthentication class is used to authenticate the user using a cookie.

    Extends:
        JWTAuthentication

    Methods:
        authenticate: Authenticate the user using a cookie.
    """

    # Method to authenticate the user using a cookie
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        """Method to authenticate the user using a cookie.

        Args:
            request (Request): The request object.

        Returns:
            Optional[Tuple[AuthUser, Token]]: The authenticated user and token.
        """

        # Get the header
        header = self.get_header(request)

        # Initialize the raw token
        raw_token = None

        # If header is not None
        if header is not None:
            # Set the raw token
            raw_token = self.get_raw_token(header)

        # If the cookie in request headers
        elif settings.COOKIE_NAME in request.COOKIES:
            # Set the raw token
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)

        # If raw token is not None
        if raw_token is not None:
            # Try
            try:
                # Get the validated token
                validated_token = self.get_validated_token(raw_token)

            # If token error
            except TokenError as e:
                # Log the error
                logger.error(f"Token error: {e}")

                # Return None
                return None

            # Get the user
            user = self.get_user(validated_token)

            # Return the user and validated token
            return user, validated_token

        # Return None
        return None
