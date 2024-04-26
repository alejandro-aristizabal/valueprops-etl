"""Console handler for logging."""

import sys

from loguru import logger

from .base_handler import BaseHandler


class ConsoleHandler(BaseHandler):
    """Console handler for logging."""

    def setup(self) -> None:
        selected_format = self.config["logging"]["formats"][
            self.config["logging"]["console"]["format"]
        ]
        level = self.config["logging"]["console"]["level"]
        logger.add(sys.stdout, format=selected_format, level=level)
