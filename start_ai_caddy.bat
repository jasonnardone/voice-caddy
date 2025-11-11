@echo off
echo.
echo ===============================================
echo   GSPro AI Voice Caddy
echo ===============================================
echo.

REM Check if API key is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY not set!
    echo.
    echo Please set your API key:
    echo   set ANTHROPIC_API_KEY=your_key_here
    echo.
    echo Or get your API key at: https://console.anthropic.com/
    echo.
    pause
    exit /b 1
)

echo Select Caddy Personality:
echo.
echo 1. Normal (Professional)
echo 2. Smart Ass (Sarcastic - Recommended!)
echo 3. Encouraging (Motivational)
echo 4. Analytical (Data-Driven)
echo 5. Drunk (Hilarious)
echo 6. Zen (Philosophical)
echo.
set /p choice="Enter number (1-6): "

if "%choice%"=="1" set personality=normal
if "%choice%"=="2" set personality=smartass
if "%choice%"=="3" set personality=encouraging
if "%choice%"=="4" set personality=analytical
if "%choice%"=="5" set personality=drunk
if "%choice%"=="6" set personality=zen

if not defined personality (
    echo Invalid choice!
    pause
    exit /b 1
)

echo.
echo Starting AI Caddy with %personality% personality...
echo Press Ctrl+C to stop
echo.

python gspro_ai_caddy.py --personality %personality%

pause
