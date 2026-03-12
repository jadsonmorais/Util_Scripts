"""
File finder module for searching strings in XML files.
Provides utilities to find files containing specific strings.
"""

import re
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass

from src.logger import setup_logger


logger = setup_logger(__name__, "file_finder.log")


@dataclass
class SearchResult:
    """Result of a file search operation."""
    search_string: str
    found_files: List[Path]
    total_files_checked: int


class FileFinder:
    """Utility class for finding files containing specific strings."""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        Initialize the FileFinder.
        
        Args:
            encoding: File encoding to use when reading files
        """
        self.encoding = encoding
    
    def find_string_in_directory(
        self,
        directory: Path,
        search_string: str,
        file_pattern: str = "*.xml",
        use_regex: bool = False,
        recursive: bool = True
    ) -> SearchResult:
        """
        Find files containing a specific string.
        
        Args:
            directory: Directory to search in
            search_string: String or regex pattern to find
            file_pattern: File pattern to match (default: *.xml)
            use_regex: Whether to treat search_string as regex
            recursive: Whether to search subdirectories
        
        Returns:
            SearchResult with files containing the string
        """
        directory = Path(directory)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory}")
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        logger.info(f"Searching for '{search_string}' in {directory}")
        
        # Find files
        glob_pattern = f"**/{file_pattern}" if recursive else file_pattern
        files = list(directory.glob(glob_pattern))
        
        found_files = []
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding=self.encoding) as f:
                    content = f.read()
                
                # Check if string is found
                if use_regex:
                    if re.search(search_string, content):
                        found_files.append(file_path)
                        logger.debug(f"Found in: {file_path.name}")
                else:
                    if search_string in content:
                        found_files.append(file_path)
                        logger.debug(f"Found in: {file_path.name}")
            
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")
        
        result = SearchResult(
            search_string=search_string,
            found_files=found_files,
            total_files_checked=len(files)
        )
        
        logger.info(
            f"Found {len(found_files)} files containing '{search_string}' "
            f"out of {len(files)} files"
        )
        
        return result
    
    def find_multiple_strings(
        self,
        directory: Path,
        search_strings: List[str],
        file_pattern: str = "*.xml",
        use_regex: bool = False
    ) -> Dict[str, SearchResult]:
        """
        Find multiple strings in directory.
        
        Args:
            directory: Directory to search in
            search_strings: List of strings to find
            file_pattern: File pattern to match
            use_regex: Whether to treat strings as regex
        
        Returns:
            Dictionary mapping search string to SearchResult
        """
        results = {}
        
        for search_string in search_strings:
            results[search_string] = self.find_string_in_directory(
                directory,
                search_string,
                file_pattern,
                use_regex
            )
        
        return results
    
    def find_not_found_strings(
        self,
        directory: Path,
        search_strings: List[str],
        file_pattern: str = "*.xml"
    ) -> Tuple[List[str], Dict[str, SearchResult]]:
        """
        Find which strings were not found in any file.
        
        Args:
            directory: Directory to search in
            search_strings: List of strings to find
            file_pattern: File pattern to match
        
        Returns:
            Tuple of (not_found_list, results_dict)
        """
        results = self.find_multiple_strings(
            directory,
            search_strings,
            file_pattern
        )
        
        not_found = [
            search_str
            for search_str, result in results.items()
            if not result.found_files
        ]
        
        return not_found, results
