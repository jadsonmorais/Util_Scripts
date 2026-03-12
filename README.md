# XML Processing Project

Professional Python utilities for XML file operations and analysis.

## Overview

This project provides a comprehensive set of tools for handling XML files, including:
- **Copy XML files** based on CNF codes
- **Search for strings** in XML files
- **Find multiple strings** and report missing ones
- **Update and compress** XML files
- **Comprehensive logging** for all operations

## Project Structure

```
Analise_01/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── logger.py                # Logging setup
│   ├── file_finder.py           # File search utilities
│   ├── file_copier.py           # File copy utilities
│   └── xml_modifier.py          # XML modification utilities
├── main.py                      # CLI interface (recommended)
├── copy_cnf_files.py            # Copy files by CNF codes
├── find_string.py               # Find single string
├── find_strings.py              # Find multiple strings
├── update_xml.py                # Update XML files
├── requirements.txt             # Python dependencies
├── config/                      # Configuration directory
├── XMLs/                        # XML files to process
├── result/                      # Output directory
└── logs/                        # Log files
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables (optional):**
   ```bash
   # Create .env file in project root
   SOURCE_DIR=C:\path\to\source
   DESTINATION_DIR=C:\path\to\destination
   DAYS_BACK=7
   CNF_CODES=046005,046006,046007
   LOG_LEVEL=INFO
   ```

## Usage

### Using the Main CLI (Recommended)

```bash
# Show help
python main.py --help

# Show all available commands
python main.py --help

# Show configuration
python main.py config-show
```

### Command: Copy CNF Files

Copy XML files containing specific CNF codes from recent dates:

```bash
python main.py copy-cnf \
    --source "C:\path\to\source" \
    --destination "C:\path\to\dest" \
    --cnf-codes "046005,046006,046007" \
    --days-back 7
```

**Options:**
- `--source`: Source directory (default: from config)
- `--destination`: Where to copy files (default: from config)
- `--cnf-codes`: Comma-separated CNF codes to search
- `--days-back`: Only copy files modified in last N days

### Command: Find String

Find files containing a specific string:

```bash
python main.py find-string \
    --path "C:\path\to\search" \
    --string "TAIBA" \
    --pattern "*.xml"
```

**Options:**
- `--path`: Directory to search (required)
- `--string`: String to find (required)
- `--pattern`: File pattern to match (default: *.xml)
- `--regex`: Treat string as regex pattern (flag)

**Example with regex:**
```bash
python main.py find-string \
    --path "C:\path\to\search" \
    --string "600019[0-9]{2}" \
    --regex
```

### Command: Find Multiple Strings

Find multiple strings and report which ones are missing:

```bash
# Using command-line strings
python main.py find-strings \
    --path "C:\path\to\search" \
    --strings "60002496,60002497,80008482"

# Using a file
python main.py find-strings \
    --path "C:\path\to\search" \
    --file strings.txt
```

**File format (strings.txt):**
```
60002496
60002497
80008482
60002505
```

**Options:**
- `--path`: Directory to search (required)
- `--strings`: Comma-separated strings OR
- `--file`: Text file with one string per line
- `--pattern`: File pattern to match (default: *.xml)

### Command: Update XML

Update XML files with default transformations and optionally compress them:

```bash
python main.py update-xml \
    --path "C:\path\to\xmls" \
    --pattern "*.xml" \
    --compress \
    --no-overwrite
```

**Options:**
- `--path`: Directory with XML files (required)
- `--pattern`: File pattern to match (default: *.xml)
- `--compress/--no-compress`: Create ZIP files (default: True)
- `--overwrite`: Modify original files instead of creating new ones

**Default transformations:**
1. Update XML declaration to include UTF-8 encoding
2. Remove all line breaks
3. Remove specific XML tags:
   - `<SendBillHeader>`, `</SendBillHeader>`
   - `<SendBillProfiles>`, `</SendBillProfiles>`
   - `<SendBillItens>`, `</SendBillItens>`
   - `<SendDailyItens>`, `</SendDailyItens>`
   - `<SendDeposits>`, `</SendDeposits>`
   - `<SendTrxCode>`, `</SendTrxCode>`
4. Rename tag: `cmfdailyItens` → `CmfdailyItens`

### Using Individual Scripts

Each command has a dedicated script file for convenience:

```bash
# Copy CNF files
python copy_cnf_files.py \
    --source "C:\source" \
    --destination "C:\dest" \
    --cnf-codes "046005,046006"

# Find string
python find_string.py \
    --path "C:\search" \
    --string "TAIBA" \
    --pattern "*.xml"

# Find multiple strings
python find_strings.py \
    --path "C:\search" \
    --strings "60002496,60002497"

# Update XML
python update_xml.py \
    --path "C:\xmls" \
    --compress
```

## Configuration

### config.py

The `src/config.py` file centralizes all configuration:

```python
from src.config import config

# Access configuration
print(config.SOURCE_DIR)
print(config.DESTINATION_DIR)
print(config.CNF_CODES)
print(config.DAYS_BACK)
```

### Environment Variables

Override config values using environment variables:

```bash
set SOURCE_DIR=C:\new\source
set DAYS_BACK=14
set CNF_CODES=046005,046006
python main.py copy-cnf
```

### Logging

Logs are automatically created in the `logs/` directory:
- `app.log`: General application log
- `file_finder.log`: File search operations
- `file_copier.log`: File copy operations
- `xml_modifier.log`: XML modification operations

Configure log level:
```bash
set LOG_LEVEL=DEBUG
python main.py find-string --path "C:\search" --string "test"
```

## Python API

Use the modules directly in your Python code:

### File Finder

```python
from src.file_finder import FileFinder
from pathlib import Path

finder = FileFinder()

# Find single string
result = finder.find_string_in_directory(
    Path("C:/path"),
    "search_string",
    "*.xml"
)

print(f"Found {len(result.found_files)} files")

# Find multiple strings
results = finder.find_multiple_strings(
    Path("C:/path"),
    ["string1", "string2", "string3"]
)

# Find which strings are missing
not_found, results = finder.find_not_found_strings(
    Path("C:/path"),
    ["string1", "string2"]
)

print(f"Not found: {not_found}")
```

### File Copier

```python
from src.file_copier import FileCopier
from pathlib import Path

copier = FileCopier()

result = copier.copy_by_cnf_codes(
    Path("C:/source"),
    Path("C:/dest"),
    {"046005", "046006"},
    days_back=7
)

print(f"Copied: {result.copied_count}")
print(f"Failed: {result.failed_count}")
```

### XML Modifier

```python
from src.xml_modifier import XMLModifier, ModificationRule
from pathlib import Path

modifier = XMLModifier()

rules = [
    ModificationRule(
        pattern='<SendBillHeader>',
        replacement=''
    ),
    ModificationRule(
        pattern='cmfdailyItens',
        replacement='CmfdailyItens'
    ),
]

result = modifier.modify_files(
    Path("C:/xmls"),
    rules,
    create_new=True,
    compress=True
)

print(f"Modified: {result.modified_count}")
```

## Examples

### Example 1: Process Recent CNF Files

```bash
python main.py copy-cnf \
    --source "C:\CMFlexScheduller\ItensEnviados\Magna" \
    --destination "C:\Projects\Analise_01\result" \
    --cnf-codes "046005,046006,046007" \
    --days-back 7
```

### Example 2: Find Missing Checks

Create `checks.txt`:
```
60002496
60002497
80008482
60002505
60002507
60002508
```

```bash
python main.py find-strings \
    --path "C:\NFCe\src\cmflex\ItensEnviados\Taiba" \
    --file checks.txt \
    --pattern "*.xml"
```

Output:
```
=== Find Multiple Strings Operation ===
Found:     10 string(s)
Not found: 3 string(s)

⚠ Strings NOT found:
  ✗ 80008499
  ✗ 80008497
  ✗ 20003243
```

### Example 3: Update and Compress XML Files

```bash
python main.py update-xml \
    --path "C:\Projects\Analise_01\XMLs" \
    --pattern "*.xml" \
    --compress
```

This will:
1. Create new files with `_modificado` suffix
2. Apply all transformations
3. Create `.zip` files for each modified XML

## Troubleshooting

### Permission Denied Errors

Ensure the user has read/write permissions to:
- Source and destination directories
- Log directory
- XML files

### File Not Found Errors

Check that paths exist:
```bash
python main.py config-show
```

See the configured directories and verify they exist.

### Encoding Errors

If you encounter encoding errors with non-ASCII characters:

```bash
set FILE_ENCODING=latin-1
python main.py find-string --path "C:\search" --string "ação"
```

## Performance Tips

1. **Large directories**: Use `--pattern` to narrow down file search
2. **Many files**: Update `days-back` to recent dates only
3. **Memory usage**: Process files in batches using scripts
4. **Logging**: Set `LOG_LEVEL=WARNING` to reduce I/O

## Error Handling

All commands provide clear error messages:

```
✗ Error: Directory not found: C:\invalid\path
```

Check logs for detailed information:

```bash
cat logs/app.log
# or on Windows
type logs\app.log
```

## Development

### Adding New Commands

1. Create utility class in `src/`
2. Add command to `main.py`
3. Create standalone script if needed
4. Document in README.md

### Running Tests (Future)

```bash
pytest tests/
```

## Version History

**v1.0.0** (Current)
- Initial release
- File finding, copying, and XML modification
- Professional CLI interface
- Comprehensive logging

## License

Proprietary - All rights reserved

## Support

For issues or questions, check:
1. README.md documentation
2. Inline code comments
3. Log files in `logs/` directory

---

**Note:** This is a professional-grade utility. Always test on sample data before processing production files.
