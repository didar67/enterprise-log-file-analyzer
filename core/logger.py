"""
Provides a configured RotatingFileHandler-based logger.

This module ensures `if not logger.hasHandlers()` is used to avoid double handlers
when the module is imported multiple times (e.g., during unit tests).
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def get_logger(name: str = "log_file_analyzer", *, config: Optional[dict] = None) -> logging.Logger:
    """Return a configured `logging.Logger` instance.

    If `config` is provided it should be a mapping compatible with internal keys:
      - level
      - rotating.filename
      - rotating.max_bytes
      - rotating.backup_count

    Args:
        name: logger name
        config: optional mapping with logging configuration

    Returns:
        logging.Logger
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        # Avoid adding duplicate handlers when called multiple times
        return logger

    # Default configuration values
    level = logging.INFO
    filename = Path("logs/analyzer.log")
    max_bytes = 10 * 1024 * 1024  # 10 MB default max size for rotation
    backup_count = 5

    if config is not None:
        try:
            # Using getattr for level to allow passing level as string in config
            level = getattr(logging, config.get("level", "INFO"))
            rot = config.get("rotating", {})
            filename = Path(rot.get("filename", filename))
            max_bytes = int(rot.get("max_bytes", max_bytes))
            backup_count = int(rot.get("backup_count", backup_count))
        except Exception:
            # On config error, fallback silently to defaults
            pass

    logger.setLevel(level)

    # Ensure log directory exists before creating handlers
    filename.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Console handler added so user sees runtime info/errors live
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger