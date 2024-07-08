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


class CookieAuthentication(JWTAuthentication):
    """Cookie Authentication Class.

    This class is used to authenticate the user using a cookie.

    Inherits From:
        JWTAuthentication

    Methods:
        authenticate: Authenticate the user using a cookie.
    """

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        """Authenticate the user using a cookie.

        Arguments:
            request: Request -- The request object.

        Returns:
            Optional[Tuple[AuthUser, Token]]: A tuple containing the authenticated user and the token.
        """

        header = self.get_header(request)

        raw_token = None

        if header is not None:
            raw_token = self.get_raw_token(header)

        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)

        if raw_token is not None:
            try:
                validated_token = self.get_validated_token(raw_token)
            except TokenError as e:
                logger.error(f"Token error: {e}")
                return None

            user = self.get_user(validated_token)

            return user, validated_token

        return None
