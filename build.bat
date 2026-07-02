@echo off
title Building Dashboard Launcher

echo.
echo ===============================
echo Building Dashboard Launcher...
echo ===============================
echo.

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Dashboard Launcher.spec" del /f /q "Dashboard Launcher.spec"

pyinstaller ^
--onefile ^
--windowed ^
--icon=launcher.ico ^
--name="Dashboard Launcher" ^
launcher.py

echo.
echo ===============================
echo BUILD COMPLETED
echo ===============================
echo.

pause
