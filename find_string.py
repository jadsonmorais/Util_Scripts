#!/usr/bin/env python
"""
Find files containing specific strings in a directory.
Converts old PowerShell: find_string_on_folder.ps1
"""

import click
from pathlib import Path

from src.file_finder import FileFinder
from src.logger import setup_logger


logger = setup_logger(__name__, "find_string.log")


@click.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="Directory to search in"
)
@click.option(
    "--string",
    type=str,
    required=True,
    help="String to search for"
)
@click.option(
    "--pattern",
    type=str,
    default="*.xml",
    help="File pattern to match (default: *.xml)"
)
@click.option(
    "--regex",
    is_flag=True,
    help="Treat string as regex pattern"
)
def find_string(path: str, string: str, pattern: str, regex: bool):
    """Find files containing a specific string."""
    
    directory = Path(path)
    
    logger.info(f"Starting search in: {directory}")
    logger.info(f"Search string: {string}")
    logger.info(f"File pattern: {pattern}")
    logger.info(f"Using regex: {regex}")
    
    try:
        finder = FileFinder()
        result = finder.find_string_in_directory(
            directory,
            string,
            pattern,
            use_regex=regex
        )
        
        click.echo(f"\n{'='*60}")
        click.echo(f"Search Results")
        click.echo(f"{'='*60}")
        click.echo(f"Search string: {result.search_string}")
        click.echo(f"Files checked: {result.total_files_checked}")
        click.echo(f"Found: {len(result.found_files)}")
        click.echo(f"{'='*60}\n")
        
        if result.found_files:
            click.echo("Files containing the string:")
            for file in result.found_files:
                click.echo(f"  ✓ {file}")
        else:
            click.echo("No files found containing the string.")
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        click.echo(f"\nError: {e}\n", err=True)
        raise


if __name__ == "__main__":
    find_string()
