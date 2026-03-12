"""
Logging module for XML processing project.
Provides centralized logging with console and file outputs.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config import config


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: str = None
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        level: Log level (defaults to config.LOG_LEVEL)
    
    Returns:
        Configured logger instance
    """
    if level is None:
        level = config.LOG_LEVEL
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log file specified)
    if log_file:
        log_path = config.LOG_DIR / log_file
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger
logger = setup_logger(__name__, "app.log")
