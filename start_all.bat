@echo off
start "RANL PRINT Backend" cmd /k "%~dp0start_backend.bat"
timeout /t 3 /nobreak >nul
start "RANL PRINT Browser" http://127.0.0.1:8000/
