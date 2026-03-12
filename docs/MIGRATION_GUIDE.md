# Migration Guide: PowerShell to Python

This guide shows how to migrate from old PowerShell scripts to the new professional Python implementation.

## Overview of Changes

| Old Script | New Implementation | Status |
|------------|-------------------|--------|
| `analise_cupons.ps1.txt` | `copy_cnf_files.py` / `main.py copy-cnf` | ✅ Improved |
| `find_filename.ps1` | `find_string.py` / `main.py find-string` | ✅ Improved |
| `find_string_on_folder.ps1` | `find_string.py` / `main.py find-string` | ✅ Improved |
| `find_string_on_folder_list.ps1` | `find_strings.py` / `main.py find-strings` | ✅ Enhanced |
| `AtualizarXML.ps1` | `update_xml.py` / `main.py update-xml` | ✅ Improved |
| `copy_files_contains.py` | `copy_cnf_files.py` | ✅ Refactored |

## Migration Examples

### 1. Copy CNF Files

**OLD - PowerShell (analise_cupons.ps1.txt):**
```powershell
$PastaDePesquisa = "C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna"
$diretorio_destino = "C:\Users\Windows\CMFlexScheduller\Analise_01\result"
$cnf_list = @("046005", "046006", "046007")

# Manual loop processing...
```

**NEW - Python:**
```bash
# Using main.py (recommended)
python main.py copy-cnf \
    --source "C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna" \
    --destination "C:\Users\Windows\CMFlexScheduller\Analise_01\result" \
    --cnf-codes "046005,046006,046007" \
    --days-back 7

# Or using dedicated script
python copy_cnf_files.py \
    --source "C:\path\to\source" \
    --destination "C:\path\to\dest" \
    --cnf-codes "046005,046006"
```

**Improvements:**
- ✅ Centralized configuration
- ✅ Better error handling
- ✅ Comprehensive logging
- ✅ Type hints for safety
- ✅ Cleaner CLI interface

### 2. Find String in Folder

**OLD - PowerShell (find_string_on_folder.ps1):**
```powershell
$PastaDePesquisa = "C:\RoboImportSATCFE\Cupons"
$StringDePesquisa = "TAIBA"
$TipoDeArquivo = "*.xml"

foreach ($Arquivo in $Arquivos) {
    $Conteudo = Get-Content $Arquivo.FullName
    $Encontrado = $Conteudo | Select-String -Pattern $StringDePesquisa
    if ($Encontrado) {
        Write-Host "String encontrada em: $($Arquivo.FullName)"
    }
}
```

**NEW - Python:**
```bash
# Using main.py (recommended)
python main.py find-string \
    --path "C:\RoboImportSATCFE\Cupons" \
    --string "TAIBA" \
    --pattern "*.xml"

# Or using dedicated script
python find_string.py \
    --path "C:\search\path" \
    --string "TAIBA"

# With regex support
python main.py find-string \
    --path "C:\path" \
    --string "^600019[0-9]{2}$" \
    --regex
```

**Improvements:**
- ✅ Regex support
- ✅ Better performance
- ✅ Cleaner output format
- ✅ Detailed logging
- ✅ Better error messages

### 3. Find Multiple Strings

**OLD - PowerShell (find_string_on_folder_list.ps1):**
```powershell
$StringsDePesquisa = @(
    "60002496",
    "60002497",
    "80008482",
    # ... 100+ more strings
)

$Found = @{}
foreach ($s in $StringsDePesquisa) { $Found[$s] = $false }

# Complex nested loops...
```

**NEW - Python:**
```bash
# Using main.py with string list
python main.py find-strings \
    --path "C:\NFCe\src\cmflex\ItensEnviados\Taiba" \
    --strings "60002496,60002497,80008482,60002505"

# Or using a text file (recommended for long lists)
python main.py find-strings \
    --path "C:\NFCe\src\cmflex" \
    --file strings.txt

# Using dedicated script
python find_strings.py \
    --path "C:\search\path" \
    --strings "60002496,60002497"
```

**strings.txt format:**
```
60002496
60002497
80008482
60002505
60002507
```

**Improvements:**
- ✅ File-based input for large lists
- ✅ Clear report of missing items
- ✅ Performance optimizations
- ✅ Better memory usage
- ✅ Formatted output

### 4. Update XML Files

**OLD - PowerShell (AtualizarXML.ps1):**
```powershell
$pasta = "C:\Users\jadson.morais\Projects\Analise_01\XMLs"
$arquivosXml = Get-ChildItem -Path $pasta -Filter "*.xml"

foreach ($arquivo in $arquivosXml) {
    $conteudo = Get-Content -Path $arquivo.FullName
    
    # Manual replacements...
    $conteudoModificado = $conteudo -replace '\<\?xml version="1\.0"\?\>', '<?xml version="1.0" encoding="utf-8"?>'
    $conteudoModificado = $conteudoModificado -replace "(\r?\n)", ""
    # ... 15+ more replacements
    
    # Compress...
    Compress-Archive -Path $novoArquivo -DestinationPath $arquivoZip
}
```

**NEW - Python:**
```bash
# Using main.py
python main.py update-xml \
    --path "C:\Users\jadson.morais\Projects\Analise_01\XMLs" \
    --pattern "*.xml" \
    --compress

# Or using dedicated script
python update_xml.py \
    --path "C:\path\to\xmls" \
    --compress \
    --no-overwrite

# Without compression
python main.py update-xml \
    --path "C:\xmls" \
    --no-compress

# Overwrite original files
python main.py update-xml \
    --path "C:\xmls" \
    --overwrite
```

**Improvements:**
- ✅ Cleaner code
- ✅ Extensible modification rules
- ✅ Better compression
- ✅ Error recovery
- ✅ Progress feedback
- ✅ Custom rule support

## Quick Reference

### Python Program vs PowerShell

| Feature | PowerShell | Python |
|---------|-----------|--------|
| Cross-platform | ❌ Windows only | ✅ Yes (Windows, Linux, Mac) |
| CLI Framework | Manual parsing | ✅ Click framework |
| Error Handling | Basic | ✅ Comprehensive |
| Logging | Write-Host only | ✅ Professional logging |
| Type Hints | ❌ | ✅ Yes |
| Configuration | Hard-coded | ✅ Centralized + environment vars |
| Testing | Difficult | ✅ Easy (pytest support) |
| Performance | Slower | ✅ Faster |
| Code Reusability | Low | ✅ High (modules) |
| Documentation | Minimal | ✅ Comprehensive |
| Maintenance | Hard | ✅ Easy |

## Environment Configuration

Instead of editing scripts, use configuration:

**OLD - PowerShell (Edit script):**
```powershell
$PastaDePesquisa = "C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna"  # Change here
```

**NEW - Python (Use environment or config file):**

Option 1 - Environment variables:
```bash
set SOURCE_DIR=C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna
python main.py copy-cnf
```

Option 2 - .env file:
```
SOURCE_DIR=C:\Users\Windows\CMFlexScheduller\ItensEnviados\Magna
DAYS_BACK=7
```

Option 3 - Command-line arguments:
```bash
python main.py copy-cnf --source "C:\path" --destination "C:\dest"
```

Option 4 - config.py:
```python
from src.config import config
print(config.SOURCE_DIR)
```

## Implementation Details

### Before: copy_files_contains.py (Old Python)

```python
# Unstructured, single-purpose script
cnf_list = {"046005", "046006", "046007"}
dias_atras = 7

for arquivo in os.listdir(diretorio_origem):
    # No error handling, no logging
    # No type hints
    # Hard-coded paths
```

### After: file_copier.py (New Professional)

```python
# Well-structured, reusable module
from dataclasses import dataclass
from typing import Set, List

@dataclass
class CopyResult:
    """Result of copy operation."""
    copied_count: int
    copied_files: List[Path]

class FileCopier:
    """Professional file copier."""
    
    def copy_by_cnf_codes(
        self,
        source_dir: Path,
        destination_dir: Path,
        cnf_codes: Set[str],
        days_back: int = 7
    ) -> CopyResult:
        """Copy files with proper typing and documentation."""
```

## Benefits of Migration

1. **Maintainability** - Clean, professional code structure
2. **Reusability** - Each module can be used independently
3. **Testability** - Easy to test with pytest
4. **Scalability** - Easy to add new features
5. **Documentation** - Comprehensive docstrings and README
6. **Performance** - Python is faster than PowerShell
7. **Cross-platform** - Works on Windows, Linux, Mac
8. **Logging** - Professional logging throughout
9. **Error Handling** - Proper exception handling
10. **Configuration** - Centralized configuration management

## Next Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the new scripts:**
   ```bash
   python main.py --help
   python main.py config-show
   ```

3. **Configure for your environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your paths
   ```

4. **Run your first command:**
   ```bash
   python main.py find-string --path "C:\search" --string "test"
   ```

5. **Archive old PowerShell scripts** (for reference)
   - Keep in a `legacy/` folder if needed
   - Update documentation with migration dates

## Troubleshooting Migration

### Issue: "ModuleNotFoundError: No module named 'click'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Python is not installed"

**Solution:**
Download and install Python 3.8+ from https://www.python.org/

### Issue: Some old PowerShell paths don't work

**Solution:**
Update paths in `.env` file to exactly match your system.

## Support

For detailed help on each command:
```bash
python main.py [command] --help
python main.py copy-cnf --help
python main.py find-string --help
```

For more information, see [README.md](README.md)
