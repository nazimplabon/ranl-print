@echo off
setlocal
cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python environment...
    py -m venv .venv
    if errorlevel 1 goto error
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    if errorlevel 1 goto error
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto error
)

".venv\Scripts\python.exe" manage.py migrate
if errorlevel 1 goto error
".venv\Scripts\python.exe" manage.py runserver 8000
goto end

:error
echo.
echo Startup failed. Read the error above, then check Python and requirements.txt.
pause
:end
endlocal
