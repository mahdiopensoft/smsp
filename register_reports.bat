@echo off
chcp 65001 > nul
title Register Reports Screens - OpenSoftCore

echo ========================================================
echo   Registering 15 Report Screens in Database...
echo ========================================================

set PYTHON_CMD=python

if exist "..\sharing\work_core_venv\Scripts\python.exe" set "PYTHON_CMD=..\sharing\work_core_venv\Scripts\python.exe"
if exist "..\..\sharing\work_core_venv\Scripts\python.exe" set "PYTHON_CMD=..\..\sharing\work_core_venv\Scripts\python.exe"
if exist "work_core_venv\Scripts\python.exe" set "PYTHON_CMD=work_core_venv\Scripts\python.exe"
if exist "venv\Scripts\python.exe" set "PYTHON_CMD=venv\Scripts\python.exe"
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=.venv\Scripts\python.exe"

echo Python: %PYTHON_CMD%
echo.

"%PYTHON_CMD%" register_reports.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run register_reports.py.
    echo Please make sure the Python virtual environment is activated.
) else (
    echo.
    echo ========================================================
    echo [SUCCESS] All 15 report screens registered successfully!
    echo ========================================================
)

pause
