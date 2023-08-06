"""
A simple function to display log messages of all formats and levels.
"""

from copy import deepcopy
import logging
import logging.config
from typing import Optional
import uuid

from django.conf import settings


logger = logging.getLogger(__name__)


def loggers_test(
    indent: str | int = 2,
    logger_name: Optional[str] = None,
) -> None:
    """
    Display log messages of all formats and levels.

    The purpose of this is quick and easy testing and configuration of loggers.

    :param indent: Either a string or an `int` number of spaces to prepend to
        each printed line to make it easier to read (to distinguish blocks of
        output belonging to the same formatters). Set to `0` or `""` to avoid
        indentation.
    :param logger_name: The name of the logger to be used for printing test
        messages. If not set, a random UUID4 string is used.
    """
    if logger_name is None:
        logger_name = str(uuid.uuid4())

    # Grab loggers' definitions.
    try:
        LOGGING = deepcopy(settings.LOGGING)
    except AttributeError:
        logger.error("settings.LOGGING is not defined.")
        return

    # Resolve and prepend indentation to existing formats.
    if isinstance(indent, int):
        indent = " " * indent
    if indent:
        for formatter_def in LOGGING.get("formatters", dict()).values():
            try:
                format_def = formatter_def["format"]
            except KeyError:
                continue
            else:
                formatter_def["format"] = f"{indent}{format_def}"

    # Get temporary logger.
    temp_logger = logging.getLogger(logger_name)
    # Prepare logger's configuration.
    config = logging.config.DictConfigurator(LOGGING)  # type: ignore
    config.configure()
    # Remove any Django-configured handlers.
    for handler in temp_logger.handlers:
        temp_logger.removeHandler(handler)
    # Allow messages of all levels to be seen.
    temp_logger.setLevel(logging.NOTSET)
    temp_logger.propagate = False

    # Print all formats for all levels.
    for fmt_name in LOGGING["formatters"]:
        print(f"Formatter: {fmt_name}")
        handler = config.configure_handler({
            "class": "logging.StreamHandler",
            "formatter": fmt_name,
        })
        temp_logger.addHandler(handler)
        for level_value, level_name in sorted(logging._levelToName.items()):
            temp_logger.log(
                level_value,
                f"Test message for level {level_name}.",
            )
        temp_logger.removeHandler(handler)
        print()
