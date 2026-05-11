@echo off
REM Frontend startup script for Windows

echo Installing dependencies...
call npm install

echo.
echo Starting development server...
call npm run dev

pause
