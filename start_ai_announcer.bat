@echo off
echo.
echo ===============================================
echo   GSPro AI Announcer - Quick Start
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

REM Check for API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY environment variable not set!
    echo.
    echo Please set your API key:
    echo   set ANTHROPIC_API_KEY=your-key-here
    echo.
    echo Get your key at: https://console.anthropic.com/
    echo.
    pause
    exit /b 1
)

echo Starting AI Announcer...
echo.
echo Choose personality mode:
echo   1. Normal (Professional)
echo   2. Smartass (Funny/Sarcastic)
echo   3. Hype (HIGH ENERGY!)
echo   4. Zen (Calm/Meditative)
echo   5. Pirate (Yarr!)
echo   6. British (Posh)
echo   7. Custom (enter mode name)
echo.

set /p choice="Enter choice (1-7): "

if "%choice%"=="1" set MODE=normal
if "%choice%"=="2" set MODE=smartass
if "%choice%"=="3" set MODE=hype
if "%choice%"=="4" set MODE=zen
if "%choice%"=="5" set MODE=pirate
if "%choice%"=="6" set MODE=british
if "%choice%"=="7" (
    set /p MODE="Enter personality mode name: "
)

if "%MODE%"=="" set MODE=normal

echo.
echo Starting with %MODE% mode...
echo Press Ctrl+C to stop
echo.

python gspro_ai_announcer.py --mode %MODE%

pause
