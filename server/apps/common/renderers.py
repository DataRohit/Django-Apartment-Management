# Imports
import json
from typing import Any, Optional, Union
from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


class GenericJSONRenderer(JSONRenderer):
    """Generic JSON Renderer for the API.

    This renderer is used to render the API response in a generic JSON format.

    Attributes:
        charset: str -- The charset to use for encoding the data.
        object_label: str -- The label to use for the object in the JSON response.

    Methods:
        render: Union[bytes, str] -- Method to render the data.
    """

    charset = "utf-8"
    object_label = "object"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> Union[bytes, str]:
        """Method to render the data.

        Arguments:
            data: Any -- The data to render.
            accepted_media_type: Optional[str] -- The accepted media type.
            renderer_context: Optional[dict] -- The renderer context.

        Returns:
            Union[bytes, str] -- The rendered data.

        Raises:
            ValueError: If the renderer context does not contain a response object.
        """

        if renderer_context is None:
            renderer_context = {}

        view = renderer_context.get("view")

        if hasattr(view, "object_label"):
            object_label = view.object_label
        else:
            object_label = self.object_label

        response = renderer_context.get("response")

        if not response:
            raise ValueError(_("Renderer context does not contain a response object"))

        status_code = response.status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(GenericJSONRenderer, self).render(data)

        return json.dumps({"status_code": status_code, object_label: data}).encode(
            self.charset
        )
