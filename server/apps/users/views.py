# Imports
import logging
from typing import Optional, Dict
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Get the logger
logger = logging.getLogger(__name__)


def set_auth_cookies(
    res: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    """Function to set the authentication cookies on the response.

    Arguments:
        res: Response -- The response object.
        access_token: str -- The access token.
        refresh_token: str -- The refresh token.
    """

    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()

    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }

    res.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()

        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        res.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    res.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairAPIView(TokenObtainPairView):
    """Custom TokenObtainPairAPIView.

    This class is used to return the access and refresh tokens as cookies.

    Methods:
        post: Function to handle the POST request.
    """

    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Function to handle the POST request.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- Additional arguments.
            **kwargs: Dict -- Additional keyword arguments.

        Returns:
            Response -- The response object.
        """

        res = super().post(request, *args, **kwargs)

        if res.status_code == status.HTTP_200_OK:
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(res, access_token, refresh_token)

                res.data.pop("access")
                res.data.pop("refresh")

                res.data["message"] = "Login successful."

            else:
                res.data["message"] = "Login failed."
                logger.error("Access or refresh token not provided in response data.")

        return res


class CustomTokenRefreshAPIView(TokenRefreshView):
    """Custom TokenRefreshAPIView.

    This class is used to return the access and refresh tokens as cookies.

    Methods:
        post: Function to handle the POST request.
    """

    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Function to handle the POST request.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- Additional arguments.
            **kwargs: Dict -- Additional keyword arguments.

        Returns:
            Response -- The response object.
        """

        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        res = super().post(request, *args, **kwargs)

        if res.status_code == status.HTTP_200_OK:
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(res, access_token, refresh_token)

                res.data.pop("access")
                res.data.pop("refresh")

                res.data["message"] = "Access token refreshed successfully."

            else:
                res.data["message"] = (
                    "Access or refresh token not provided in response data."
                )
                logger.error("Access or refresh token not provided in response data.")

        return res


class CustomProviderAuthAPIView(ProviderAuthView):
    """Custom ProviderAuthAPIView.

    This class is used to return the access and refresh tokens as cookies.

    Methods:
        post: Function to handle the POST request.
    """

    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Function to handle the POST request.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- Additional arguments.
            **kwargs: Dict -- Additional keyword arguments.

        Returns:
            Response -- The response object.
        """

        res = super().post(request, *args, **kwargs)

        if res.status_code == status.HTTP_201_CREATED:
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(res, access_token, refresh_token)

                res.data.pop("access")
                res.data.pop("refresh")

                res.data["message"] = "You are logged in successfully."

            else:
                res.data["message"] = (
                    "Access or refresh token not found in provider response."
                )
                logger.error("Access or refresh token not provided in response data.")

        return res


class LogoutAPIView(APIView):
    """LogoutAPIView .

    This class is used to remove the access and refresh tokens from the cookies.

    Methods:
        post: Function to handle the POST request.
    """

    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Function to handle the POST request.

        Arguments:
            request: Request -- The request object.
            *args: Dict -- Additional arguments.
            **kwargs: Dict -- Additional keyword arguments.

        Returns:
            Response -- The response object.
        """

        res = Response(status=status.HTTP_204_NO_CONTENT)

        res.delete_cookie("access")
        res.delete_cookie("refresh")
        res.delete_cookie("logged_in")

        return res
