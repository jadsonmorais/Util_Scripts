"""
Configuration module for XML processing project.
Centralizes all configuration variables and provides environment-based overrides.
"""

import os
from pathlib import Path
from typing import Set
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration."""
    
    # Project root directory
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    
    # Directories
    XMLS_DIR: Path = PROJECT_ROOT / "XMLs"
    RESULT_DIR: Path = PROJECT_ROOT / "result"
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    
    # Source and destination for file operations
    SOURCE_DIR: str = os.getenv("SOURCE_DIR", r"C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna")
    DESTINATION_DIR: str = os.getenv("DESTINATION_DIR", str(RESULT_DIR))
    
    # Search configurations
    FILE_PATTERN: str = "*.xml"
    FILE_ENCODING: str = "utf-8"
    
    # Days back for file filtering
    DAYS_BACK: int = int(os.getenv("DAYS_BACK", "7"))
    
    # CNF codes to search (configurable via environment)
    CNF_CODES: Set[str] = field(default_factory=lambda: os.getenv("CNF_CODES", "046005,046006,046007").split(","))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # XML modifications
    XML_ENCODING: str = '<?xml version="1.0" encoding="utf-8"?>'
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.RESULT_DIR.mkdir(parents=True, exist_ok=True)
        Path(cls.DESTINATION_DIR).mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()
