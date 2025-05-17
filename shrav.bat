@echo off
:: ShravScript language runner

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.6 or higher.
    exit /b 1
)

:: Get the directory containing this batch file
set "SCRIPT_DIR=%~dp0"

:: Run the ShravScript interpreter with all arguments
python "%SCRIPT_DIR%src\main.py" %* 