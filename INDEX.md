# 📑 Project Index

## Complete File Reference Guide

---

## 🔷 Core Modules (src/)

### src/__init__.py
**Purpose:** Package initialization and exports
- Imports all public classes and functions
- Version information
- Quick access to main utilities

### src/config.py ⭐
**Purpose:** Centralized configuration management
- Project paths and directories
- Environment variable support
- Configuration validation
- Dataclass-based structure
**Key Classes:** `Config`
**Key Methods:** `ensure_directories()`

### src/logger.py ⭐
**Purpose:** Professional logging infrastructure
- Console and file logging
- Log rotation (10MB max)
- Configurable log levels
- Formatted output
**Key Functions:** `setup_logger()`

### src/file_finder.py ⭐
**Purpose:** File search and discovery utilities
- Single string search with regex
- Multiple string search
- Find not-found items
- Typed results
**Key Classes:** `FileFinder`, `SearchResult`
**Key Methods:**
- `find_string_in_directory()`
- `find_multiple_strings()`
- `find_not_found_strings()`

### src/file_copier.py ⭐
**Purpose:** File copy operations based on criteria
- Copy by CNF codes
- Date-based filtering
- Copy by pattern matching
- Result statistics
**Key Classes:** `FileCopier`, `CopyResult`
**Key Methods:**
- `copy_by_cnf_codes()`
- `copy_by_pattern()`

### src/xml_modifier.py ⭐
**Purpose:** XML file transformations
- Update XML declarations
- Remove line breaks
- Remove specific tags
- Apply modification rules
- ZIP compression
**Key Classes:** `XMLModifier`, `ModificationRule`, `ModifyResult`
**Key Methods:**
- `modify_files()`
- `update_xml_declaration()`
- `remove_tags()`
- `apply_rules()`

---

## 🚀 CLI Entry Points

### main.py ⭐ RECOMMENDED
**Purpose:** Central command-line interface
**Type:** Click-based CLI
**Commands:**
- `copy-cnf` - Copy files by CNF codes
- `find-string` - Find single string
- `find-strings` - Find multiple strings
- `update-xml` - Update XML files
- `config-show` - Display configuration

**Usage:**
```bash
python main.py [command] [options]
python main.py --help
python main.py --version
```

### copy_cnf_files.py
**Purpose:** Standalone script for copying CNF files
**Replaces:** Old analise_cupons.ps1.txt
**Equivalent to:** `python main.py copy-cnf`
**Usage:**
```bash
python copy_cnf_files.py --source "path" --destination "path"
```

### find_string.py
**Purpose:** Standalone script for searching single string
**Replaces:** Old find_string_on_folder.ps1, find_filename.ps1
**Equivalent to:** `python main.py find-string`
**Usage:**
```bash
python find_string.py --path "path" --string "text"
```

### find_strings.py
**Purpose:** Standalone script for searching multiple strings
**Replaces:** Old find_string_on_folder_list.ps1
**Equivalent to:** `python main.py find-strings`
**Usage:**
```bash
python find_strings.py --path "path" --strings "s1,s2,s3"
```

### update_xml.py
**Purpose:** Standalone script for XML updates
**Replaces:** Old AtualizarXML.ps1
**Equivalent to:** `python main.py update-xml`
**Usage:**
```bash
python update_xml.py --path "path" --compress
```

---

## 🪟 Windows Utilities

### run.bat
**Purpose:** Windows batch launcher
- Interactive menu
- Automatic dependency check
- Error handling
**Type:** Batch script
**Usage:**
```bash
run.bat              # Shows menu
run.bat copy-cnf    # Direct command
```

### quickstart.py
**Purpose:** Interactive CLI menu launcher
**Type:** Python script with Click
**Usage:**
```bash
python quickstart.py
```

---

## 📦 Configuration Files

### requirements.txt ⭐
**Purpose:** Python package dependencies
**Packages:**
- Click==8.1.7 (CLI framework)
- python-dotenv==1.0.0 (Environment variables)
**Usage:**
```bash
pip install -r requirements.txt
```

### pyproject.toml ⭐
**Purpose:** Modern Python project metadata
**Contents:**
- Project information
- Dependencies
- Tool configurations (black, mypy, pytest)
- Build settings
**Standards:**
- PEP 518 compliant
- PyPI ready

### .env.example
**Purpose:** Configuration template
**Contents:**
- SOURCE_DIR
- DESTINATION_DIR
- DAYS_BACK
- CNF_CODES
- FILE_ENCODING
- LOG_LEVEL
**How to use:**
```bash
copy .env.example .env
# Edit .env with your values
```

### .gitignore
**Purpose:** Git ignore rules
**Ignores:**
- Python cache and bytecode
- Virtual environments
- IDE configuration
- Logs and temporary files
- Operating system files

---

## 📖 Documentation

### README.md ⭐ START HERE
**Purpose:** Complete project documentation
**Length:** 500+ lines
**Contents:**
- Installation instructions
- All command examples
- Configuration guide
- Python API reference
- Troubleshooting section
- Error handling guide
**Audience:** End users and developers

### GUIA_RAPIDO.md ⭐ START HERE (Português)
**Purpose:** Portuguese quick start guide
**Type:** Quick reference
**Contents:**
- Installation steps
- Main commands
- Practical examples
- Windows usage
- Troubleshooting
- Tips and tricks
**Audience:** Portuguese speakers

### MIGRATION_GUIDE.md ⭐
**Purpose:** Migration from PowerShell to Python
**Contents:**
- Before/After comparisons
- Step-by-step examples
- Equivalent commands
- Benefits overview
- Implementation details
**Audience:** Users of old PowerShell scripts

### REFACTORING_SUMMARY.md ⭐
**Purpose:** Complete refactoring report
**Contents:**
- Project restructuring overview
- Module descriptions
- Code quality improvements
- File migration mapping
- Professional standards applied
- Summary of changes
**Audience:** Project stakeholders and developers

### VALIDATION_CHECKLIST.md
**Purpose:** Testing and validation procedures
**Contents:**
- Setup verification
- Command tests
- Logs verification
- Configuration tests
- Performance tests
- Troubleshooting links
**How to use:** Follow checklist after setup

### PROJECT_STRUCTURE.py
**Purpose:** Visual project structure representation
**Type:** Executable Python script
**Usage:**
```bash
python PROJECT_STRUCTURE.py
```
**Output:** Prints ASCII-art project structure

---

## 📝 Examples

### strings_example.txt
**Purpose:** Example file for batch string searches
**Contents:** Sample search strings for testing
**Usage:**
```bash
python main.py find-strings --path "C:\path" --file strings_example.txt
```

---

## 📁 Data Directories

### config/
**Purpose:** Configuration files directory
**Status:** Initially empty
**Usage:** Store custom configurations here

### XMLs/
**Purpose:** Input XML files directory
**Status:** Initially empty
**Usage:** Place XML files to process here

### result/
**Purpose:** Output directory for processed files
**Status:** Created automatically
**Usage:** Processed files appear here

### logs/
**Purpose:** Application logs directory
**Status:** Created automatically on first run
**Contents:**
- `app.log` - Main application log
- `file_finder.log` - File finder operations
- `file_copier.log` - File copy operations
- `xml_modifier.log` - XML modification operations

---

## 📊 File Statistics

### Total Files
- Core modules: 6
- CLI scripts: 5
- Documentation: 5
- Configuration: 4
- Utilities: 2
- Examples: 1
- **Total: 23 files**

### Total Lines of Code
- Core modules: ~1,500 lines
- CLI scripts: ~1,000 lines
- Documentation: ~2,500 lines
- Configuration: ~100 lines
- **Total: ~5,100 lines**

### File Types Distribution
- Python (.py): 10 files
- Markdown (.md): 5 files
- Configuration: 4 files
- Batch/Example: 2 files
- **Total: 21 files**

---

## 🔄 File Dependencies

```
src/
├── __init__.py
│   └── Imports: config, logger, file_finder, file_copier, xml_modifier
├── config.py
│   └── No internal dependencies
├── logger.py
│   └── Depends on: config.py
├── file_finder.py
│   └── Depends on: logger.py
├── file_copier.py
│   └── Depends on: logger.py
└── xml_modifier.py
    └── Depends on: logger.py

CLI/
├── main.py
│   └── Depends on: All src modules
├── copy_cnf_files.py
│   └── Depends on: config, logger, file_copier
├── find_string.py
│   └── Depends on: file_finder, logger
├── find_strings.py
│   └── Depends on: file_finder, logger
└── update_xml.py
    └── Depends on: config, logger, xml_modifier
```

---

## ✅ File Purpose Summary

| File | Purpose | Type | Status |
|------|---------|------|--------|
| src/config.py | Configuration management | Module | ⭐ New |
| src/logger.py | Logging infrastructure | Module | ⭐ New |
| src/file_finder.py | File search utilities | Module | ⭐ New |
| src/file_copier.py | File copy operations | Module | ⭐ New |
| src/xml_modifier.py | XML transformations | Module | ⭐ New |
| main.py | Central CLI interface | Script | ⭐ Recommended |
| copy_cnf_files.py | CNF copier | Script | ✨ Refactored |
| find_string.py | String finder | Script | ✨ Converted |
| find_strings.py | Multiple string finder | Script | ✨ Converted |
| update_xml.py | XML updater | Script | ✨ Converted |
| requirements.txt | Dependencies | Config | ⭐ New |
| pyproject.toml | Project metadata | Config | ⭐ New |
| .env.example | Config template | Config | ⭐ New |
| README.md | Main documentation | Docs | ⭐ New |
| GUIA_RAPIDO.md | Portuguese guide | Docs | ⭐ New |
| MIGRATION_GUIDE.md | Migration guide | Docs | ⭐ New |
| REFACTORING_SUMMARY.md | Refactoring report | Docs | ⭐ New |

---

## 🎯 Quick Navigation

### For First Time Users
1. Read: [README.md](README.md)
2. Then: [GUIA_RAPIDO.md](GUIA_RAPIDO.md) (if Portuguese speaker)
3. Run: `python main.py --help`

### For PowerShell Users Coming from Old System
1. Read: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
2. Compare: Old scripts with new equivalents
3. Run: First test with `python main.py config-show`

### For Developers
1. Study: [README.md](README.md#python-api)
2. Review: `src/` modules
3. Test: Use [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md)

### For Verification
1. Follow: [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md)
2. Check: All tests pass
3. Verify: Logs in `logs/` directory

### For Troubleshooting
1. Check: `logs/` directory
2. See: README.md Troubleshooting section
3. Apply: Relevant solution

---

## 📋 Before → After

### Old System
```
analise_cupons.ps1.txt     ──┐
AtualizarXML.ps1           ──├──→ Unstructured
copy_files_contains.py     ──├──→ No logging
find_*.ps1                 ──┘
No documentation
```

### New System
```
src/ [Reusable Modules]
├── config.py    ──────────┐
├── logger.py    ───────────├──→ Professional
├── file_*.py    ───────────├──→ Documented
└── xml_*.py     ──────────┘

main.py [Central CLI] ✨
[Standalone scripts]
[Complete Documentation]
[Configuration Management]
```

---

## 🚀 Getting Started Paths

### Path 1: Quick Start (5 minutes)
```bash
1. pip install -r requirements.txt
2. python main.py config-show
3. python main.py find-string --path "." --string "test"
```

### Path 2: Full Setup (15 minutes)
```bash
1. pip install -r requirements.txt
2. copy .env.example .env
3. [Edit .env with your paths]
4. Read GUIA_RAPIDO.md
5. Run all four main commands
```

### Path 3: Migration from Old System (30 minutes)
```bash
1. Read MIGRATION_GUIDE.md
2. Update .env with old paths
3. Convert first PowerShell command to new Python equivalent
4. Test and compare results
5. Migrate remaining scripts one by one
```

---

## 📚 Documentation Map

```
README.md                 ← START: Complete guide
├── GUIA_RAPIDO.md      ← Portuguese quick guide
├── MIGRATION_GUIDE.md   ← Come from PowerShell?
└── REFACTORING_SUMMARY.md ← What changed?
├── VALIDATION_CHECKLIST.md ← Verify setup
└── PROJECT_STRUCTURE.py ← View structure
```

---

## ✨ Key Features By File

| Feature | File(s) |
|---------|---------|
| Configuration | `src/config.py`, `.env.example` |
| Logging | `src/logger.py`, `logs/*` |
| File Search | `src/file_finder.py`, `find_string.py`, `find_strings.py` |
| File Copy | `src/file_copier.py`, `copy_cnf_files.py` |
| XML Modification | `src/xml_modifier.py`, `update_xml.py` |
| CLI | `main.py`, `run.bat`, `quickstart.py` |
| Documentation | `README.md`, `GUIA_RAPIDO.md`, `MIGRATION_GUIDE.md` |

---

**Last Updated:** March 11, 2026
**Total Documentation:** 2,500+ lines
**Total Code:** 2,600+ lines
**Total Project Files:** 23

---

🎉 **Everything is documented and organized!**

Start with `README.md` or `GUIA_RAPIDO.md` depending on your language preference.
