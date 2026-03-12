"""
File copier module for copying files based on content criteria.
Provides utilities to copy XML files with specific codes or patterns.
"""

import shutil
import re
from pathlib import Path
from typing import Set, List
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.logger import setup_logger


logger = setup_logger(__name__, "file_copier.log")


@dataclass
class CopyResult:
    """Result of a copy operation."""
    copied_count: int
    skipped_count: int
    failed_count: int
    copied_files: List[Path]


class FileCopier:
    """Utility class for copying files based on content criteria."""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        Initialize the FileCopier.
        
        Args:
            encoding: File encoding to use when reading files
        """
        self.encoding = encoding
    
    def copy_by_cnf_codes(
        self,
        source_dir: Path,
        destination_dir: Path,
        cnf_codes: Set[str],
        days_back: int = 7,
        file_pattern: str = "*.xml"
    ) -> CopyResult:
        """
        Copy files containing specific CNF codes from past N days.
        
        Args:
            source_dir: Source directory
            destination_dir: Destination directory
            cnf_codes: Set of CNF codes to search for
            days_back: Only copy files modified in the last N days
            file_pattern: File pattern to match
        
        Returns:
            CopyResult with statistics
        """
        source_dir = Path(source_dir)
        destination_dir = Path(destination_dir)
        
        if not source_dir.exists():
            logger.error(f"Source directory not found: {source_dir}")
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate date limit
        date_limit = datetime.now() - timedelta(days=days_back)
        
        logger.info(
            f"Copying files with CNF codes {cnf_codes} modified after "
            f"{date_limit.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        result = CopyResult(
            copied_count=0,
            skipped_count=0,
            failed_count=0,
            copied_files=[]
        )
        
        # Get all XML files
        files = list(source_dir.glob(file_pattern))
        
        for file_path in files:
            try:
                # Check modification date
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if mod_time < date_limit:
                    result.skipped_count += 1
                    continue
                
                # Read file content
                with open(file_path, "r", encoding=self.encoding) as f:
                    content = f.read()
                
                # Check if any CNF code is present
                found_cnf = None
                for cnf_code in cnf_codes:
                    pattern = f"<nCFe>{cnf_code}</nCFe>"
                    if pattern in content:
                        found_cnf = cnf_code
                        break
                
                # Copy file if CNF code found
                if found_cnf:
                    dest_file = destination_dir / file_path.name
                    shutil.copy2(file_path, dest_file)
                    result.copied_count += 1
                    result.copied_files.append(dest_file)
                    logger.info(
                        f"Copied: {file_path.name} (CNF: {found_cnf}) "
                        f"- {mod_time.strftime('%d/%m/%Y %H:%M:%S')}"
                    )
                else:
                    result.skipped_count += 1
            
            except Exception as e:
                result.failed_count += 1
                logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(
            f"Copy operation completed: {result.copied_count} copied, "
            f"{result.skipped_count} skipped, {result.failed_count} failed"
        )
        
        return result
    
    def copy_by_pattern(
        self,
        source_dir: Path,
        destination_dir: Path,
        search_pattern: str,
        use_regex: bool = False,
        file_pattern: str = "*.xml"
    ) -> CopyResult:
        """
        Copy files matching a pattern.
        
        Args:
            source_dir: Source directory
            destination_dir: Destination directory
            search_pattern: Pattern to search for
            use_regex: Whether to treat pattern as regex
            file_pattern: File pattern to match
        
        Returns:
            CopyResult with statistics
        """
        source_dir = Path(source_dir)
        destination_dir = Path(destination_dir)
        
        if not source_dir.exists():
            logger.error(f"Source directory not found: {source_dir}")
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Copying files matching pattern: {search_pattern}")
        
        result = CopyResult(
            copied_count=0,
            skipped_count=0,
            failed_count=0,
            copied_files=[]
        )
        
        # Get all matching files
        files = list(source_dir.glob(file_pattern))
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding=self.encoding) as f:
                    content = f.read()
                
                # Check if pattern matches
                matches = False
                if use_regex:
                    matches = bool(re.search(search_pattern, content))
                else:
                    matches = search_pattern in content
                
                if matches:
                    dest_file = destination_dir / file_path.name
                    shutil.copy2(file_path, dest_file)
                    result.copied_count += 1
                    result.copied_files.append(dest_file)
                    logger.info(f"Copied: {file_path.name}")
                else:
                    result.skipped_count += 1
            
            except Exception as e:
                result.failed_count += 1
                logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(
            f"Copy operation completed: {result.copied_count} copied, "
            f"{result.skipped_count} skipped, {result.failed_count} failed"
        )
        
        return result
