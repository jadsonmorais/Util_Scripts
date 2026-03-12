#!/usr/bin/env python3
"""
Quick launcher script for common operations.
Provides an interactive menu for quick access to main features.
"""

import click
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from main import cli


def show_menu():
    """Display interactive menu for operations."""
    
    click.clear()
    click.echo("\n")
    click.echo("  " + "="*56)
    click.echo("  " + " "*12 + "XML Processing Project")
    click.echo("  " + "="*56)
    click.echo("\n")
    click.echo("  Available Operations:\n")
    click.echo("    1. Copy XML files by CNF codes              [copy-cnf]")
    click.echo("    2. Find string in files                    [find-string]")
    click.echo("    3. Find multiple strings                   [find-strings]")
    click.echo("    4. Update and compress XML files           [update-xml]")
    click.echo("    5. Show current configuration              [config-show]")
    click.echo("    6. Show help                               [--help]")
    click.echo("    0. Exit")
    click.echo("\n  " + "="*56 + "\n")


def main():
    """Interactive menu launcher."""
    
    while True:
        show_menu()
        
        choice = input("  Select operation (0-6): ").strip()
        
        args_map = {
            "1": ["copy-cnf", "--help"],
            "2": ["find-string", "--help"],
            "3": ["find-strings", "--help"],
            "4": ["update-xml", "--help"],
            "5": ["config-show"],
            "6": ["--help"],
        }
        
        if choice == "0":
            click.echo("\n  Goodbye!\n")
            break
        elif choice in args_map:
            sys.argv = ["quickstart.py"] + args_map[choice]
            try:
                cli()
            except SystemExit:
                pass
            
            input("\n  Press Enter to continue...")
        else:
            click.echo("\n  Invalid option. Please try again.\n")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        click.echo("\n\n  Operation cancelled.\n")
        sys.exit(0)
