"""Logging configuration."""

import logging
import sys
from pathlib import Path

from loguru import logger

from src.config import get_settings


def setup_logger(name: str = None) -> logger:
    """
    Setup and configure logger.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.debug else "INFO",
        colorize=True,
    )

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "aim_bot.log",
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    # Error log file
    logger.add(
        log_dir / "errors.log",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    return logger
