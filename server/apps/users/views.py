# Imports
import logging
from typing import Dict, Optional

from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Get the logger
logger = logging.getLogger(__name__)


# Function to set the authentication cookies
def set_auth_cookies(
    res: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    """Set the authentication cookies.

    Args:
        res (Response): The response object.
        access_token (str): The access token.
        refresh_token (Optional[str]): The refresh token.
    """

    # Get the access token lifetime from settings
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()

    # Get the cookie settings
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }

    # Set the access token cookie
    res.set_cookie("access", access_token, **cookie_settings)

    # If the refresh token is provided
    if refresh_token:
        # Get the refresh token lifetime from settings
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()

        # Make a copy of the cookie settings
        refresh_cookie_settings = cookie_settings.copy()

        # Update the max age for the refresh token
        refresh_cookie_settings["max_age"] = refresh_token_lifetime

        # Set the refresh token cookie
        res.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    # Make a copy of the cookie settings
    logged_in_cookie_settings = cookie_settings.copy()

    # Set the httponly to False
    logged_in_cookie_settings["httponly"] = False

    # Set the logged in cookie
    res.set_cookie("logged_in", "true", **logged_in_cookie_settings)


# Custom Token Obtain Pair API View
class CustomTokenObtainPairAPIView(TokenObtainPairView):
    """Custom Token Obtain Pair API View

    This class extends the TokenObtainPairView class to set the authentication cookies.

    Extends:
        TokenObtainPairView

    Methods:
        post(request: Request, *args: Dict, **kwargs: Dict) -> Response: Handle the POST request.

    Returns:
        Response: The response object.
    """

    # Method to handle the POST request
    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Handle the POST request.

        Args:
            request (Request): The request object.
            *args (dict): The arguments.
            **kwargs (dict): The keyword arguments.

        Returns:
            Response: The response object
        """

        # Get the response
        res = super().post(request, *args, **kwargs)

        # If the status code is 200
        if res.status_code == status.HTTP_200_OK:
            # Get the access and refresh tokens
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            # If the access and refresh tokens are provided
            if access_token and refresh_token:
                # Set the authentication cookies
                set_auth_cookies(res, access_token, refresh_token)

                # Remove the access and refresh tokens from the response data
                res.data.pop("access")
                res.data.pop("refresh")

                # Add the message to the response data
                res.data["message"] = "Login successful."

            # Else
            else:
                # Add the message to the response data
                res.data["message"] = "Login failed."

                # Log the error
                logger.error("Access or refresh token not provided in response data.")

        # Return the response
        return res


# Custom Token Refresh API View
class CustomTokenRefreshAPIView(TokenRefreshView):
    """Custom Token Refresh API View

    This class extends the TokenRefreshView class to set the authentication cookies.

    Args:
        TokenRefreshView

    Methods:
        post(request: Request, *args: Dict, **kwargs: Dict) -> Response: Handle the POST request.

    Returns:
        Response: The response object.
    """

    # Method to handle the POST request
    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Handle the POST request.

        Args:
            request (Request): The request object.
            *args (dict): The arguments.
            **kwargs (dict): The keyword arguments.

        Returns:
            Response: The response object.
        """

        # Get the refresh token from the cookies
        refresh_token = request.COOKIES.get("refresh")

        # If the refresh token is provided
        if refresh_token:
            # Add the refresh token to the request data
            request.data["refresh"] = refresh_token

        # Get the response
        res = super().post(request, *args, **kwargs)

        # If the status code is 200
        if res.status_code == status.HTTP_200_OK:
            # Get the access and refresh tokens
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            # If the access and refresh tokens are provided
            if access_token and refresh_token:
                # Set the authentication cookies
                set_auth_cookies(res, access_token, refresh_token)

                # Remove the access and refresh tokens from the response data
                res.data.pop("access")
                res.data.pop("refresh")

                # Add the message to the response data
                res.data["message"] = "Access token refreshed successfully."

            # Else
            else:
                # Add the message to the response data
                res.data["message"] = (
                    "Access or refresh token not provided in response data."
                )

                # Log the error
                logger.error("Access or refresh token not provided in response data.")

        # Return the response
        return res


# Custom Provider Auth API View
class CustomProviderAuthAPIView(ProviderAuthView):
    """Custom Provider Auth API View

    This class extends the ProviderAuthView class to set the authentication cookies.

    Args:
        ProviderAuthView

    Methods:
        post(request: Request, *args: Dict, **kwargs: Dict) -> Response: Handle the POST request.

    Returns:
        Response: The response object.
    """

    # Method to handle the POST request
    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Handle the POST request.

        Args:
            request (Request): The request object.
            *args (dict): The arguments.
            **kwargs (dict): The keyword arguments.

        Returns:
            Response: The response object.
        """

        # Get the response
        res = super().post(request, *args, **kwargs)

        # If the status code is 201
        if res.status_code == status.HTTP_201_CREATED:
            # Get the access and refresh tokens
            access_token = res.data.get("access")
            refresh_token = res.data.get("refresh")

            # If the access and refresh tokens are provided
            if access_token and refresh_token:
                # Set the authentication cookies
                set_auth_cookies(res, access_token, refresh_token)

                # Remove the access and refresh tokens from the response data
                res.data.pop("access")
                res.data.pop("refresh")

                # Set the message in the response data
                res.data["message"] = "You are logged in successfully."

            # Else
            else:
                # Set the in the response data
                res.data["message"] = (
                    "Access or refresh token not found in provider response."
                )

                # Log the error message
                logger.error("Access or refresh token not provided in response data.")

        # Return the response
        return res


# Logout API View
class LogoutAPIView(APIView):
    """Logout API View

    This class is used to logout the user by deleting the authentication cookies.

    Extends:
        APIView

    Methods:
        post(request: Request, *args: Dict, **kwargs: Dict) -> Response: Handle the POST request.

    Returns:
        Response: The response object.
    """

    # Method to handle the POST request
    def post(self, request: Request, *args: Dict, **kwargs: Dict) -> Response:
        """Handle the POST request.

        Args:
            request (Request): The request object.
            *args (dict): The arguments.
            **kwargs (dict): The keyword arguments.

        Returns:
            Response: The response object.
        """

        # Create a response object
        res = Response(status=status.HTTP_204_NO_CONTENT)

        # Delete the authentication cookies
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        res.delete_cookie("logged_in")

        # Return the response
        return res
