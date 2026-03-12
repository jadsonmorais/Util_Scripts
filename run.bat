@echo off
REM Windows batch script to run XML Processing commands
REM This is a convenience wrapper for the Python CLI

setlocal enabledelayedexpansion

REM Change to project directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import click" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Show menu if no arguments
if "%1"=="" (
    echo.
    echo ======================================
    echo     XML Processing - Main Menu
    echo ======================================
    echo.
    echo Available commands:
    echo   1. copy-cnf           - Copy files by CNF codes
    echo   2. find-string        - Find string in files
    echo   3. find-strings       - Find multiple strings
    echo   4. update-xml         - Update XML files
    echo   5. config-show        - Show configuration
    echo   6. help               - Show help
    echo.
    set /p choice="Enter command or number: "
    
    if "!choice!"=="1" (
        set choice=copy-cnf
    ) else if "!choice!"=="2" (
        set choice=find-string
    ) else if "!choice!"=="3" (
        set choice=find-strings
    ) else if "!choice!"=="4" (
        set choice=update-xml
    ) else if "!choice!"=="5" (
        set choice=config-show
    ) else if "!choice!"=="6" (
        set choice=--help
    )
) else (
    set choice=%1
)

REM Execute the command
python main.py %choice% %2 %3 %4 %5 %6 %7 %8 %9

endlocal
