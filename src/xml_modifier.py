"""
XML modifier module for processing and modifying XML files.
Provides utilities to update XML files with specific transformations and compression.
"""

import re
import zipfile
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
import tempfile

from src.logger import setup_logger


logger = setup_logger(__name__, "xml_modifier.log")


@dataclass
class ModificationRule:
    """A rule for modifying XML content."""
    pattern: str
    replacement: str
    is_regex: bool = False


@dataclass
class ModifyResult:
    """Result of XML modification operation."""
    modified_count: int
    failed_count: int
    modified_files: List[Path]


class XMLModifier:
    """Utility class for modifying XML files."""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        Initialize the XMLModifier.
        
        Args:
            encoding: File encoding to use
        """
        self.encoding = encoding
    
    def update_xml_declaration(
        self,
        content: str,
        declaration: str = '<?xml version="1.0" encoding="utf-8"?>'
    ) -> str:
        """
        Update XML declaration in content.
        
        Args:
            content: XML content
            declaration: New XML declaration
        
        Returns:
            Modified content
        """
        # Remove old declaration
        content = re.sub(r'<\?xml[^?]*\?>', '', content)
        # Add new declaration
        return declaration + content
    
    def remove_line_breaks(self, content: str) -> str:
        """Remove all line breaks from content."""
        return re.sub(r'(\r?\n)', '', content)
    
    def remove_tags(self, content: str, tags: List[str]) -> str:
        """
        Remove specific XML tags from content.
        
        Args:
            content: XML content
            tags: List of tag names to remove (opening and closing)
        
        Returns:
            Modified content
        """
        for tag in tags:
            # Remove opening tag
            content = re.sub(f'<{tag}>', '', content)
            # Remove closing tag
            content = re.sub(f'</{tag}>', '', content)
        
        return content
    
    def replace_text(
        self,
        content: str,
        old_text: str,
        new_text: str
    ) -> str:
        """Replace text in content (case-sensitive)."""
        return content.replace(old_text, new_text)
    
    def apply_rules(
        self,
        content: str,
        rules: List[ModificationRule]
    ) -> str:
        """
        Apply a list of modification rules to content.
        
        Args:
            content: XML content
            rules: List of ModificationRule objects
        
        Returns:
            Modified content
        """
        for rule in rules:
            if rule.is_regex:
                content = re.sub(rule.pattern, rule.replacement, content)
            else:
                content = content.replace(rule.pattern, rule.replacement)
        
        return content
    
    def modify_files(
        self,
        directory: Path,
        rules: List[ModificationRule],
        file_pattern: str = "*.xml",
        create_new: bool = True,
        compress: bool = False
    ) -> ModifyResult:
        """
        Modify multiple XML files with specified rules.
        
        Args:
            directory: Directory containing XML files
            rules: List of modification rules
            file_pattern: File pattern to match
            create_new: Create new files instead of overwriting
            compress: Create ZIP files of modified XMLs
        
        Returns:
            ModifyResult with statistics
        """
        directory = Path(directory)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory}")
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        logger.info(f"Starting XML modification in {directory}")
        
        result = ModifyResult(
            modified_count=0,
            failed_count=0,
            modified_files=[]
        )
        
        files = list(directory.glob(file_pattern))
        logger.info(f"Found {len(files)} files to process")
        
        for file_path in files:
            try:
                # Read original content
                with open(file_path, "r", encoding=self.encoding) as f:
                    content = f.read()
                
                # Apply modifications
                modified_content = self.apply_rules(content, rules)
                
                # Determine output file
                if create_new:
                    output_file = file_path.parent / (
                        file_path.stem + "_modificado" + file_path.suffix
                    )
                else:
                    output_file = file_path
                
                # Write modified content
                with open(output_file, "w", encoding=self.encoding) as f:
                    f.write(modified_content)
                
                logger.info(f"Modified: {file_path.name} -> {output_file.name}")
                
                # Compress if requested
                if compress:
                    zip_file = Path(str(output_file) + ".zip")
                    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.write(output_file, output_file.name)
                    logger.info(f"Compressed: {zip_file.name}")
                
                result.modified_count += 1
                result.modified_files.append(output_file)
            
            except Exception as e:
                result.failed_count += 1
                logger.error(f"Error modifying {file_path}: {e}")
        
        logger.info(
            f"Modification completed: {result.modified_count} modified, "
            f"{result.failed_count} failed"
        )
        
        return result
