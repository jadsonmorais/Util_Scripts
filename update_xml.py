#!/usr/bin/env python
"""
Update and compress XML files with specific transformations.
Converts old PowerShell: AtualizarXML.ps1
"""

import click
from pathlib import Path
from typing import List

from src.xml_modifier import XMLModifier, ModificationRule
from src.logger import setup_logger


logger = setup_logger(__name__, "update_xml.log")


def get_default_rules() -> List[ModificationRule]:
    """Get default XML modification rules."""
    return [
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
        ModificationRule(
            pattern="<SendBillHeader>",
            replacement=""
        ),
        ModificationRule(
            pattern="<SendBillProfiles>",
            replacement=""
        ),
        ModificationRule(
            pattern="<SendBillItens>",
            replacement=""
        ),
        ModificationRule(
            pattern="<SendDailyItens>",
            replacement=""
        ),
        ModificationRule(
            pattern="<SendDeposits>",
            replacement=""
        ),
        ModificationRule(
            pattern="<SendTrxCode>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendBillHeader>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendBillProfiles>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendBillItens>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendDailyItens>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendDeposits>",
            replacement=""
        ),
        ModificationRule(
            pattern="</SendTrxCode>",
            replacement=""
        ),
        ModificationRule(
            pattern="cmfdailyItens",
            replacement="CmfdailyItens"
        ),
    ]


@click.command()
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
    help="File pattern to match (default: *.xml)"
)
@click.option(
    "--compress",
    is_flag=True,
    default=True,
    help="Compress modified files as ZIP (default: True)"
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite original files instead of creating new ones"
)
def update_xml(path: str, pattern: str, compress: bool, overwrite: bool):
    """Update XML files and optionally compress them."""
    
    directory = Path(path)
    
    logger.info(f"Starting XML update in: {directory}")
    logger.info(f"File pattern: {pattern}")
    logger.info(f"Compress: {compress}")
    logger.info(f"Overwrite: {overwrite}")
    
    try:
        modifier = XMLModifier()
        rules = get_default_rules()
        
        result = modifier.modify_files(
            directory,
            rules,
            pattern,
            create_new=not overwrite,
            compress=compress
        )
        
        click.echo(f"\n{'='*60}")
        click.echo(f"XML Update Operation Completed")
        click.echo(f"{'='*60}")
        click.echo(f"Modified: {result.modified_count}")
        click.echo(f"Failed:   {result.failed_count}")
        click.echo(f"{'='*60}\n")
        
        if result.modified_files:
            click.echo("Modified files:")
            for file in result.modified_files:
                click.echo(f"  ✓ {file.name}")
            click.echo()
    
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        click.echo(f"\nError: {e}\n", err=True)
        raise


if __name__ == "__main__":
    update_xml()
