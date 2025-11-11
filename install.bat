@echo off
echo.
echo ===============================================
echo   GSPro Voice Caddy - Installation
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [1/3] Python found!
python --version
echo.

echo [2/3] Installing Python dependencies...
echo.
pip install pytesseract Pillow pyttsx3
echo.

echo [3/3] Checking Tesseract OCR...
echo.
python -c "import pytesseract; print('Tesseract version:', pytesseract.get_tesseract_version())" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Tesseract OCR not found!
    echo.
    echo Please install Tesseract OCR:
    echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Run the installer
    echo 3. Make sure it's added to your PATH
    echo.
    echo After installing Tesseract, run this script again.
    echo.
) else (
    echo.
    echo ===============================================
    echo   Installation Complete!
    echo ===============================================
    echo.
    echo Next steps:
    echo 1. Run: python test_setup.py
    echo 2. If tests pass, run: python gspro_voice_caddy.py --debug
    echo 3. Launch GSPro and start playing!
    echo.
)

pause
