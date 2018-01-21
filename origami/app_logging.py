"""Logging configuration file."""

import logging


def get_logger(name, level=logging.INFO):
    """Get a logger with the specified name and level."""
    logger = logging.getLogger(name)

    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(name)-15s - %(asctime)s - %(levelname)-8s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
