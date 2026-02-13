@echo off
REM Quick start script for Resume Application System (Windows)

echo Resume Application System - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed.flag" (
    echo Installing dependencies...
    pip install -q -r requirements.txt
    echo. > venv\installed.flag
    echo Dependencies installed
)

REM Run the application
echo.
echo Starting Resume Application System...
echo.
python src\main.py
