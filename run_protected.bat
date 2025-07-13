@echo off
title Advanced Recoil Helper v2.0 - Protected Mode
color 0A

:: Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Administrator privileges required!
    echo [!] Right-click and select "Run as administrator"
    pause
    exit /b 1
)

:: Display banner
echo ===============================================
echo    Advanced Recoil Helper v2.0
echo    Protected Mode - Educational Only
echo    User: %USERNAME%
echo ===============================================
echo.

:: Check protection status
echo [*] Checking protection status...
python -c "from advanced_protection_v2 import get_protection_status; print('[+] Protection available' if get_protection_status() else '[-] Protection not initialized')"

echo.
echo Select mode:
echo   1. Console Mode (Advanced)
echo   2. GUI Mode (User Friendly)
echo   3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo [*] Starting Console Mode with Protection...
    python integrated_protection.py
) else if "%choice%"=="2" (
    echo.
    echo [*] Starting GUI Mode with Protection...
    python gui_interface.py
) else if "%choice%"=="3" (
    exit
) else (
    echo [!] Invalid choice!
    pause
    goto :eof
)

pause