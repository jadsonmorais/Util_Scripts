#!/usr/bin/env python
"""
Main CLI for XML Processing Project.
Central interface for all XML processing operations.
"""

import click
import sys
from pathlib import Path

from src.config import config
from src.logger import setup_logger
from src.file_finder import FileFinder
from src.file_copier import FileCopier
from src.xml_modifier import XMLModifier, ModificationRule


logger = setup_logger(__name__, "main.log")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """XML Processing Project - Professional XML handling utilities."""
    config.ensure_directories()


@cli.command()
@click.option(
    "--source",
    type=click.Path(exists=True),
    default=config.SOURCE_DIR,
    help="Source directory with XML files"
)
@click.option(
    "--destination",
    type=click.Path(),
    default=config.DESTINATION_DIR,
    help="Destination directory for copied files"
)
@click.option(
    "--cnf-codes",
    type=str,
    default=",".join(config.CNF_CODES),
    help="Comma-separated CNF codes"
)
@click.option(
    "--days-back",
    type=int,
    default=config.DAYS_BACK,
    help="Number of days back to consider"
)
def copy_cnf(source, destination, cnf_codes, days_back):
    """Copy XML files containing specific CNF codes."""
    
    source_dir = Path(source)
    dest_dir = Path(destination)
    codes = set(code.strip() for code in cnf_codes.split(","))
    
    click.echo(f"\n{'='*60}")
    click.echo("📋 Copy CNF Files Operation")
    click.echo(f"{'='*60}")
    click.echo(f"Source:      {source_dir}")
    click.echo(f"Destination: {dest_dir}")
    click.echo(f"CNF codes:   {', '.join(codes)}")
    click.echo(f"Days back:   {days_back}")
    click.echo(f"{'='*60}\n")
    
    try:
        copier = FileCopier()
        result = copier.copy_by_cnf_codes(
            source_dir,
            dest_dir,
            codes,
            days_back
        )
        
        click.echo(f"\n✓ Operation Completed Successfully")
        click.echo(f"  Copied:  {result.copied_count} file(s)")
        click.echo(f"  Skipped: {result.skipped_count} file(s)")
        click.echo(f"  Failed:  {result.failed_count} file(s)\n")
    
    except Exception as e:
        logger.error(f"Copy operation failed: {e}")
        click.echo(f"\n✗ Error: {e}\n", err=True)
        sys.exit(1)


@cli.command()
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
    help="File pattern to match"
)
@click.option(
    "--regex",
    is_flag=True,
    help="Treat string as regex pattern"
)
def find_string(path, string, pattern, regex):
    """Find files containing a specific string."""
    
    directory = Path(path)
    
    click.echo(f"\n{'='*60}")
    click.echo("🔍 Find String Operation")
    click.echo(f"{'='*60}")
    click.echo(f"Directory: {directory}")
    click.echo(f"String:    {string}")
    click.echo(f"Pattern:   {pattern}")
    click.echo(f"Regex:     {regex}")
    click.echo(f"{'='*60}\n")
    
    try:
        finder = FileFinder()
        result = finder.find_string_in_directory(
            directory,
            string,
            pattern,
            use_regex=regex
        )
        
        click.echo(f"\n✓ Search Completed")
        click.echo(f"  Total files checked: {result.total_files_checked}")
        click.echo(f"  Files found: {len(result.found_files)}\n")
        
        if result.found_files:
            click.echo("Results:")
            for file in result.found_files:
                click.echo(f"  ✓ {file.name}")
            click.echo()
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        click.echo(f"\n✗ Error: {e}\n", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="Directory to search in"
)
@click.option(
    "--strings",
    type=str,
    default=None,
    help="Comma-separated strings to search for"
)
@click.option(
    "--file",
    "input_file",
    type=click.File("r"),
    default=None,
    help="Read strings from file (one per line)"
)
@click.option(
    "--pattern",
    type=str,
    default="*.xml",
    help="File pattern to match"
)
def find_strings(path, strings, input_file, pattern):
    """Find multiple strings and report which were not found."""
    
    directory = Path(path)
    
    # Parse strings
    if input_file:
        search_strings = [line.strip() for line in input_file if line.strip()]
    elif strings:
        search_strings = [s.strip() for s in strings.split(",")]
    else:
        click.echo("Error: Provide strings via --strings or --file\n", err=True)
        sys.exit(1)
    
    click.echo(f"\n{'='*60}")
    click.echo("🔍 Find Multiple Strings Operation")
    click.echo(f"{'='*60}")
    click.echo(f"Directory:      {directory}")
    click.echo(f"Strings to find: {len(search_strings)}")
    click.echo(f"Pattern:        {pattern}")
    click.echo(f"{'='*60}\n")
    
    try:
        finder = FileFinder()
        not_found, results = finder.find_not_found_strings(
            directory,
            search_strings,
            pattern
        )
        
        found = [s for s in search_strings if s not in not_found]
        
        click.echo(f"\n✓ Search Completed")
        click.echo(f"  Found:     {len(found)} string(s)")
        click.echo(f"  Not found: {len(not_found)} string(s)\n")
        
        if not_found:
            click.echo(f"⚠ Strings NOT found in any file:")
            for string in not_found:
                click.echo(f"  ✗ {string}")
            click.echo()
        else:
            click.echo("✓ All strings were found in the files!\n")
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        click.echo(f"\n✗ Error: {e}\n", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="Directory with XML files to update"
)
@click.option(
    "--pattern",
    type=str,
    default="*.xml",
    help="File pattern to match"
)
@click.option(
    "--compress/--no-compress",
    default=True,
    help="Compress modified files (default: True)"
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite original files"
)
def update_xml(path, pattern, compress, overwrite):
    """Update XML files with default transformations and optionally compress."""
    
    directory = Path(path)
    
    click.echo(f"\n{'='*60}")
    click.echo("✏️  Update XML Operation")
    click.echo(f"{'='*60}")
    click.echo(f"Directory: {directory}")
    click.echo(f"Pattern:   {pattern}")
    click.echo(f"Compress:  {compress}")
    click.echo(f"Overwrite: {overwrite}")
    click.echo(f"{'='*60}\n")
    
    # Default modification rules
    rules = [
        ModificationRule(
            pattern=r'<\?xml version="1\.0"\?>',
            replacement='<?xml version="1.0" encoding="utf-8"?>',
            is_regex=True
        ),
        ModificationRule(
            pattern=r"(\r?\n)",
            replacement="",
            is_regex=True
        ),
        ModificationRule(pattern="<SendBillHeader>", replacement=""),
        ModificationRule(pattern="<SendBillProfiles>", replacement=""),
        ModificationRule(pattern="<SendBillItens>", replacement=""),
        ModificationRule(pattern="<SendDailyItens>", replacement=""),
        ModificationRule(pattern="<SendDeposits>", replacement=""),
        ModificationRule(pattern="<SendTrxCode>", replacement=""),
        ModificationRule(pattern="</SendBillHeader>", replacement=""),
        ModificationRule(pattern="</SendBillProfiles>", replacement=""),
        ModificationRule(pattern="</SendBillItens>", replacement=""),
        ModificationRule(pattern="</SendDailyItens>", replacement=""),
        ModificationRule(pattern="</SendDeposits>", replacement=""),
        ModificationRule(pattern="</SendTrxCode>", replacement=""),
        ModificationRule(pattern="cmfdailyItens", replacement="CmfdailyItens"),
    ]
    
    try:
        modifier = XMLModifier()
        result = modifier.modify_files(
            directory,
            rules,
            pattern,
            create_new=not overwrite,
            compress=compress
        )
        
        click.echo(f"\n✓ Operation Completed Successfully")
        click.echo(f"  Modified: {result.modified_count} file(s)")
        click.echo(f"  Failed:   {result.failed_count} file(s)\n")
    
    except Exception as e:
        logger.error(f"Update operation failed: {e}")
        click.echo(f"\n✗ Error: {e}\n", err=True)
        sys.exit(1)


@cli.command()
def config_show():
    """Show current configuration."""
    
    click.echo(f"\n{'='*60}")
    click.echo("⚙️  Configuration")
    click.echo(f"{'='*60}")
    click.echo(f"Project Root:    {config.PROJECT_ROOT}")
    click.echo(f"XML Directory:   {config.XMLS_DIR}")
    click.echo(f"Result Directory: {config.RESULT_DIR}")
    click.echo(f"Log Directory:   {config.LOG_DIR}")
    click.echo(f"Source Directory: {config.SOURCE_DIR}")
    click.echo(f"Dest Directory:  {config.DESTINATION_DIR}")
    click.echo(f"Days Back:       {config.DAYS_BACK}")
    click.echo(f"CNF Codes:       {', '.join(config.CNF_CODES)}")
    click.echo(f"Log Level:       {config.LOG_LEVEL}")
    click.echo(f"File Encoding:   {config.FILE_ENCODING}")
    click.echo(f"{'='*60}\n")


if __name__ == "__main__":
    cli()
