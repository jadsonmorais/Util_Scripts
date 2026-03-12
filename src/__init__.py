"""
XML Processing Project
Professional Python utilities for XML file operations.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Professional XML processing utilities"

from src.config import config
from src.logger import logger, setup_logger
from src.file_finder import FileFinder, SearchResult
from src.file_copier import FileCopier, CopyResult
from src.xml_modifier import XMLModifier, ModificationRule, ModifyResult

__all__ = [
    "config",
    "logger",
    "setup_logger",
    "FileFinder",
    "SearchResult",
    "FileCopier",
    "CopyResult",
    "XMLModifier",
    "ModificationRule",
    "ModifyResult",
]
