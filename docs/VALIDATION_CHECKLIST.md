# ✅ Validation Checklist

After refactoring, verify that everything is working correctly.

## 📋 Setup Verification

- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] All modules can be imported
  ```bash
  python -c "from src import *; print('✓ Modules imported successfully')"
  ```

- [ ] Configuration working
  ```bash
  python main.py config-show
  ```

## 🧪 Command Tests

### Test copy-cnf

```bash
# Dry run - just show help
python main.py copy-cnf --help
```

✅ **Expected:** Shows command help and options

### Test find-string

```bash
# Search in XMLs directory for a test string
python main.py find-string --path XMLs --string "<?xml"
```

✅ **Expected:** Reports number of files checked and found

### Test find-strings

```bash
# Create test file
echo 60002496 > test_strings.txt
echo 60002497 >> test_strings.txt

# Search for strings
python main.py find-strings --path XMLs --file test_strings.txt

# Cleanup
del test_strings.txt
```

✅ **Expected:** Reports which strings were found/not found

### Test update-xml

```bash
# Show help
python main.py update-xml --help
```

✅ **Expected:** Shows command help and options

## 📊 Logs Verification

Check that logs are created:

```bash
# List log files
dir logs\
```

✅ **Expected:** Log files created (app.log, etc.)

```bash
# Check log content
type logs\app.log
```

✅ **Expected:** Log entries with timestamps

## 🔧 Configuration Tests

### Test environment variables

```bash
set SOURCE_DIR=C:\test\path
python main.py config-show
```

✅ **Expected:** Shows updated SOURCE_DIR

### Test .env file

```bash
# Create .env
copy .env.example .env

# Edit and set a value
set SOURCE_DIR=C:\my\path

python main.py config-show
```

✅ **Expected:** Uses values from environment

## 📁 Directory Structure

Verify all directories exist:

```bash
# Check structure
dir src\
dir logs\
dir result\
```

✅ **Expected:** All directories present

## 🐍 Python API Tests

### Test FileFinder programmatically

```python
from pathlib import Path
from src.file_finder import FileFinder

finder = FileFinder()
result = finder.find_string_in_directory(
    Path("XMLs"),
    "<?xml"
)
print(f"Found: {len(result.found_files)}")
```

✅ **Expected:** Returns SearchResult with file list

### Test Configuration API

```python
from src.config import config

print(config.SOURCE_DIR)
print(config.DESTINATION_DIR)
print(config.LOG_LEVEL)
```

✅ **Expected:** Prints configuration values

## 🎯 Integration Tests

### Full workflow test

```bash
# 1. Show config
python main.py config-show

# 2. Search in XMLs
python main.py find-string --path XMLs --string "<?xml"

# 3. Check logs
type logs\app.log
type logs\file_finder.log
```

✅ **Expected:** All commands execute without errors

## 🐛 Error Handling Tests

### Test with invalid path

```bash
python main.py find-string --path "C:\nonexistent\path" --string "test"
```

✅ **Expected:** Clear error message in logs

### Test with missing required parameter

```bash
python main.py find-string --path "C:\path"
```

✅ **Expected:** Shows error about missing --string parameter

### Test with invalid file encoding

```bash
set FILE_ENCODING=invalid-codec
python main.py find-string --path XMLs --string "test"
```

✅ **Expected:** Graceful error handling

## 🚀 Performance Tests

### Test with large search list

Create `large_list.txt` with 100+ strings:
```bash
# Generate test file
(for /L %i in (1,1,100) do echo 600%i) > large_list.txt

# Search
python main.py find-strings --path XMLs --file large_list.txt

# Check performance
type logs\file_finder.log | find /C "operation completed"
```

✅ **Expected:** Completes in reasonable time with clear logging

## 📚 Documentation Tests

### Verify README is readable

```bash
# Check file exists
if exist README.md echo ✓ README exists
```

✅ **Expected:** README.md is present

### Verify GUIA_RAPIDO

```bash
if exist GUIA_RAPIDO.md echo ✓ GUIA_RAPIDO exists
```

✅ **Expected:** GUIA_RAPIDO.md is present

### Verify MIGRATION_GUIDE

```bash
if exist MIGRATION_GUIDE.md echo ✓ MIGRATION_GUIDE exists
```

✅ **Expected:** MIGRATION_GUIDE.md is present

## 🔍 Code Quality Checks

### Check for Python errors

```bash
python -m py_compile src\config.py
python -m py_compile src\logger.py
python -m py_compile src\file_finder.py
python -m py_compile src\file_copier.py
python -m py_compile src\xml_modifier.py
python -m py_compile main.py
```

✅ **Expected:** No compilation errors

### Check imports

```bash
python -c "from src.config import config; from src.logger import logger"
python -c "from src.file_finder import FileFinder"
python -c "from src.file_copier import FileCopier"
python -c "from src.xml_modifier import XMLModifier"
```

✅ **Expected:** All imports successful

## ✨ Windows-Specific Tests

### Test .bat launcher

```bash
run.bat --help
```

✅ **Expected:** Shows main.py help

### Test quickstart

```bash
# Should show interactive menu (press 6 for help)
python quickstart.py
```

✅ **Expected:** Displays interactive menu

## 📊 Final Verification Checklist

- [ ] Python version checked
- [ ] Dependencies installed
- [ ] All modules importable
- [ ] main.py --help works
- [ ] copy-cnf command works
- [ ] find-string command works
- [ ] find-strings command works
- [ ] update-xml command works
- [ ] config-show works
- [ ] Logs directory created
- [ ] Log files contain entries
- [ ] README.md readable
- [ ] Documentation complete
- [ ] No Python errors
- [ ] All imports work
- [ ] Windows .bat launcher works

**Total Tests Passed: ___ / 16**

## 🎉 Success Criteria

✅ All tests pass
✅ Documentation is complete
✅ Commands execute without errors
✅ Logs are created and populated
✅ Configuration is working
✅ No Python errors

If all checks pass: **✅ Project is ready for production use!**

---

## 📞 Troubleshooting Quick Links

If you encounter issues, check:

1. **Python/Dependencies Issues**
   - Run: `pip install -r requirements.txt`
   - Check: `python --version`

2. **Configuration Issues**
   - Run: `python main.py config-show`
   - Edit: `.env` file with correct paths

3. **Command Failures**
   - Check: `logs/app.log`
   - Run: `python main.py [command] --help`

4. **Specific Module Issues**
   - See: [README.md](README.md#troubleshooting)
   - Check: MIGRATION_GUIDE.md

---

## 📝 Notes

Record any issues found during validation:

```
Issue: ___________________________________
Solution: ___________________________________
Date Fixed: ___________________________________
```

---

**Validation Date:** ____________________
**Validated By:** ____________________
**Status:** ☐ PASSED  ☐ FAILED

---

Start validation with:
```bash
python main.py config-show
```
