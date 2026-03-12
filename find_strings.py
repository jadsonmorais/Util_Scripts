#!/usr/bin/env python
"""
Find multiple strings in directory and report which ones were not found.
Converts old PowerShell: find_string_on_folder_list.ps1
"""

import click
from pathlib import Path
from typing import List

from src.file_finder import FileFinder
from src.logger import setup_logger


logger = setup_logger(__name__, "find_strings_list.log")


@click.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="Directory to search in"
)
@click.option(
    "--strings",
    type=str,
    required=True,
    help="Comma-separated strings to search for"
)
@click.option(
    "--pattern",
    type=str,
    default="*.xml",
    help="File pattern to match (default: *.xml)"
)
@click.option(
    "--file",
    "input_file",
    type=click.File("r"),
    default=None,
    help="Read strings from file (one per line)"
)
def find_strings(path: str, strings: str, pattern: str, input_file):
    """Find multiple strings in directory and report not found."""
    
    directory = Path(path)
    
    # Parse strings from command line or file
    if input_file:
        search_strings = [line.strip() for line in input_file if line.strip()]
    else:
        search_strings = [s.strip() for s in strings.split(",")]
    
    logger.info(f"Starting search in: {directory}")
    logger.info(f"Searching for {len(search_strings)} strings")
    logger.info(f"File pattern: {pattern}")
    
    try:
        finder = FileFinder()
        not_found, results = finder.find_not_found_strings(
            directory,
            search_strings,
            pattern
        )
        
        click.echo(f"\n{'='*60}")
        click.echo(f"Search Results Summary")
        click.echo(f"{'='*60}")
        click.echo(f"Total strings searched: {len(search_strings)}")
        click.echo(f"Found in files: {len(search_strings) - len(not_found)}")
        click.echo(f"Not found: {len(not_found)}")
        click.echo(f"{'='*60}\n")
        
        # Show found strings
        found = [s for s in search_strings if s not in not_found]
        if found:
            click.echo(f"✓ Strings found in files ({len(found)}):")
            for string in found:
                found_count = len(results[string].found_files)
                click.echo(f"  ✓ {string} (found in {found_count} file(s))")
        
        click.echo()
        
        # Show not found strings
        if not_found:
            click.echo(f"✗ Strings NOT found ({len(not_found)}):")
            for string in not_found:
                click.echo(f"  ✗ {string}")
            click.echo()
        else:
            click.echo("All strings were found!")
        
        click.echo(f"{'='*60}\n")
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        click.echo(f"\nError: {e}\n", err=True)
        raise


if __name__ == "__main__":
    find_strings()
