# Imports
import json
from typing import Any, Optional, Union

from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


# GenericJSONRenderer Class
class GenericJSONRenderer(JSONRenderer):
    """Generic JSON Renderer

    This class is used to render the JSON data.

    Extends:
        JSONRenderer

    Attributes:
        charset (str): The character set.
        object_label (str): The object label.

    Methods:
        render: Method to render the data.

    Raises:
        ValueError: If the renderer context does not contain a response object.
    """

    # Attributes
    charset = "utf-8"
    object_label = "object"

    # Method to render the data
    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> Union[bytes, str]:
        """Method to render the data.

        Args:
            data (Any): The data to render.
            accepted_media_type (Optional[str]): The accepted media type.
            renderer_context (Optional[dict]): The renderer context.

        Returns:
            Union[bytes, str]: The rendered data.

        Raises:
            ValueError: If the renderer context does not contain a response object.
        """

        # If the renderer context is None
        if renderer_context is None:
            # Initialize the renderer context
            renderer_context = {}

        # Get the view
        view = renderer_context.get("view")

        # If the view has an object label
        if hasattr(view, "object_label"):
            # Set the object label
            object_label = view.object_label

        # Else
        else:
            # Set the object label
            object_label = self.object_label

        # Get the response
        response = renderer_context.get("response")

        # If the response is None
        if not response:
            # Raise a ValueError
            raise ValueError(_("Renderer context does not contain a response object"))

        # Get the status code
        status_code = response.status_code

        # Get the errors
        errors = data.get("errors", None)

        # If errors is not None
        if errors is not None:
            # Return the errors
            return super(GenericJSONRenderer, self).render(data)

        # Return the JSON data
        return json.dumps({"status_code": status_code, object_label: data}).encode(
            self.charset
        )
