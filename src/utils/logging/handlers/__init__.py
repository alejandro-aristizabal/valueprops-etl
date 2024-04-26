"""The handlers module for the logging package."""

from .base_handler import BaseHandler
from .console_handler import ConsoleHandler
from .file_handler import FileHandler


def get_handler(
    handler_name: str, config: dict[str, str]
) -> ConsoleHandler | FileHandler | BaseHandler:
    """Get the handler for the logger.

    Args:
        handler_name (str): The name of the handler.
        config (dict[str, str]): The configuration.

    Returns:
        ConsoleHandler | FileHandler | AppInsightsHandler | BlobHandler: The handler.
    """
    handlers = {
        "console": ConsoleHandler,
        "file": FileHandler
    }

    handler_class = handlers.get(handler_name)
    if not handler_class:
        raise ValueError(f"Handler does not exist: {handler_name}")
    return handler_class(config)
