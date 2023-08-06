"""Context handler for Flask."""
import flask
import uuid
from autoinject.informants import ContextInformant


def register_flask_context(injector):
    """Register the flask context informant to ensure Flask requests have individual contexts."""
    injector.register_informant(FlaskContextInformant())


class FlaskContextInformant(ContextInformant):
    """Provides a unique identifier for each request to the context manager."""

    def __init__(self):
        super().__init__("flask")

    def get_context_id(self) -> str:
        """Provide a unique ID to the context manager."""
        if not flask.has_request_context():
            return ""
        if not hasattr(flask.g, "autoinject_id"):
            flask.g.autoinject_id = str(uuid.uuid4())
        return flask.g.autoinject_id
