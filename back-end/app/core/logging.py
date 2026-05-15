from __future__ import annotations

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()
    logger = logging.getLogger("awen")
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.handlers.clear()
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"awen.{name}")
