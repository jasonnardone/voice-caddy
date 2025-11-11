@echo off
echo.
echo ===============================================
echo   GSPro Voice Caddy - Quick Start
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting Voice Caddy...
echo.
echo Press Ctrl+C to stop
echo.

python gspro_voice_caddy.py --debug

pause
