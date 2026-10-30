@echo off
title VYRON AI 2.0 - Local Server Runner
color 0B
cls
echo =================================================================
echo        VYRON AI 2.0 - MULTILINGUAL PUBLIC INTELLIGENCE
echo =================================================================
echo.
echo Starting Vyron AI server on http://127.0.0.1:8000 ...
echo Opening your browser automatically in 2 seconds...
echo.

:: Open browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

:: Try py first, fallback to python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py main.py
) else (
    python main.py
)

pause
