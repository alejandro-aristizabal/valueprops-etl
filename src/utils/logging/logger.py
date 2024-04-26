"""This module contains the logger setup function."""

import os

import toml
from loguru import logger

from utils.logging.handlers import get_handler


def setup_logging(
    config_path: str = "config.toml",
    current_dir: str = os.path.dirname(__file__),
) -> None:
    """Setup the logging configuration.

    Args:
        config_path (str, optional): The path to the configuration file. Defaults to "config.toml".
        current_dir (str, optional): The current directory. Defaults to os.path.dirname(__file__).
    """

    with open(os.path.join(current_dir, config_path), "r", encoding="utf-8") as f:
        config = toml.load(f)

    # remove the default logger
    logger.remove()
    selected_loggers = config["loggers_selection"]["loggers"]

    for logger_name in selected_loggers:
        handler = get_handler(logger_name, config)
        handler.setup()


if __name__ == "__main__":
    setup_logging()
