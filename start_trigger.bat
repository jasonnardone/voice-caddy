@echo off
echo.
echo ===============================================
echo   GSPro AI Announcer - TRIGGER MODE
echo   (Only announces when screen changes!)
echo ===============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

REM Check API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY not set!
    echo.
    echo Set it with:
    echo   set ANTHROPIC_API_KEY=your-key-here
    echo.
    echo Get key at: https://console.anthropic.com/
    pause
    exit /b 1
)

echo Choose personality:
echo   1. Normal (Professional)
echo   2. Smartass (Funny)
echo   3. Hype (HIGH ENERGY!)
echo   4. Zen (Calm)
echo   5. Pirate (Yarr!)
echo   6. British (Posh)
echo.

set /p choice="Enter (1-6): "

if "%choice%"=="1" set MODE=normal
if "%choice%"=="2" set MODE=smartass
if "%choice%"=="3" set MODE=hype
if "%choice%"=="4" set MODE=zen
if "%choice%"=="5" set MODE=pirate
if "%choice%"=="6" set MODE=british

if "%MODE%"=="" set MODE=smartass

echo.
echo Starting TRIGGER MODE with %MODE% personality...
echo (Only announces when screen changes - MUCH more efficient!)
echo.
echo Press Ctrl+C to stop
echo.

python gspro_ai_trigger.py --mode %MODE% --threshold 3.0

pause
