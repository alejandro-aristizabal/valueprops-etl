"""File handler for logging."""

from loguru import logger

from .base_handler import BaseHandler


class FileHandler(BaseHandler):
    """File handler for logging."""

    def setup(self) -> None:
        selected_format = self.config["logging"]["formats"][
            self.config["logging"]["file"]["format"]
        ]
        level = self.config["logging"]["file"]["level"]
        logger.add(
            self.config["logging"]["file"]["path"],
            rotation=self.config["logging"]["file"]["rotation"],
            retention=self.config["logging"]["file"]["retention"],
            format=selected_format,
            level=level,
        )
