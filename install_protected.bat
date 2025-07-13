    @echo off
title Advanced Recoil Helper - Protected Installation
color 0A

echo ===============================================
echo    Advanced Recoil Helper v2.0
echo    Protected Installation
echo    User: %USERNAME%
echo    Date: %DATE% %TIME%
echo ===============================================
echo.
echo [!] This installation will:
echo     - Install protection components
echo     - Configure Windows settings
echo     - Install kernel driver (educational)
echo     - Create shortcuts
echo.
echo [!] Administrator privileges required
echo.

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Please run as administrator!
    pause
    exit /b 1
)

echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo [*] Starting protected installation...
echo.

:: Run protection installer
python protection_installer.py

if %errorLevel% equ 0 (
    echo.
    echo ===============================================
    echo    Installation Completed Successfully!
    echo ===============================================
    echo.
    echo You can now run:
    echo   - Desktop shortcuts
    echo   - run_protected.bat
    echo.
) else (
    echo.
    echo [!] Installation failed!
    echo [!] Check the error messages above
    echo.
)

pause