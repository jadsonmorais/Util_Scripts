#!/usr/bin/env python
"""
Copy CVG (CNF codes) from source directory to destination.
Converts old PowerShell: analise_cupons.ps1
"""

import click
from pathlib import Path
from typing import Set

from src.config import config
from src.file_copier import FileCopier
from src.logger import setup_logger


logger = setup_logger(__name__, "copy_cnf.log")


@click.command()
@click.option(
    "--source",
    type=click.Path(exists=True),
    default=None,
    help="Source directory with XML files"
)
@click.option(
    "--destination",
    type=click.Path(),
    default=None,
    help="Destination directory for copied files"
)
@click.option(
    "--cnf-codes",
    type=str,
    default=None,
    help="Comma-separated CNF codes (e.g., '046005,046006,046007')"
)
@click.option(
    "--days-back",
    type=int,
    default=7,
    help="Number of days back to consider (default: 7)"
)
def copy_cnf_files(source: str, destination: str, cnf_codes: str, days_back: int):
    """Copy XML files containing specific CNF codes."""
    
    # Use config values or command-line overrides
    source_dir = Path(source) if source else Path(config.SOURCE_DIR)
    dest_dir = Path(destination) if destination else Path(config.DESTINATION_DIR)
    
    # Parse CNF codes
    if cnf_codes:
        codes = set(code.strip() for code in cnf_codes.split(","))
    else:
        codes = set(code.strip() for code in config.CNF_CODES)
    
    logger.info(f"Starting CNF file copy operation")
    logger.info(f"Source: {source_dir}")
    logger.info(f"Destination: {dest_dir}")
    logger.info(f"CNF codes: {codes}")
    logger.info(f"Days back: {days_back}")
    
    try:
        copier = FileCopier()
        result = copier.copy_by_cnf_codes(
            source_dir,
            dest_dir,
            codes,
            days_back
        )
        
        click.echo(f"\n{'='*50}")
        click.echo(f"Copy Operation Completed")
        click.echo(f"{'='*50}")
        click.echo(f"Copied:  {result.copied_count}")
        click.echo(f"Skipped: {result.skipped_count}")
        click.echo(f"Failed:  {result.failed_count}")
        click.echo(f"{'='*50}\n")
        
        if result.copied_files:
            click.echo("Copied files:")
            for file in result.copied_files:
                click.echo(f"  - {file.name}")
    
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        click.echo(f"\nError: {e}\n", err=True)
        raise


if __name__ == "__main__":
    config.ensure_directories()
    copy_cnf_files()
