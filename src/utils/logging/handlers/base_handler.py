"""Base handler for all handlers."""

from typing import Any


class BaseHandler:
    """Base class for all handlers.

    Args:
        config (dict[str, dict[str, str]]): The configuration.
    """

    def __init__(self, config: Any) -> None:
        """Initialize the BaseHandler.

        Args:
            config (dict[str, dict[str, str]]): The configuration.
        """
        self.config = config

    def setup(self) -> None:
        """Setup the handler."""
