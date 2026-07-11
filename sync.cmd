@echo off
setlocal

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

if not exist ".env" (
  echo Missing .env. Copy .env.example to .env and fill in Trilium settings. 1>&2
  exit /b 2
)

set "VENV_PY=%ROOT_DIR%.venv\Scripts\python.exe"

if exist "%VENV_PY%" goto ensure_deps

where py >nul 2>nul
if %ERRORLEVEL%==0 goto create_venv_with_py

where python >nul 2>nul
if %ERRORLEVEL%==0 goto create_venv_with_python

echo Missing Python. Install Python 3 or make sure py/python is on PATH. 1>&2
exit /b 127

:create_venv_with_py
py -3 -m venv "%ROOT_DIR%.venv"
if errorlevel 1 exit /b 1
goto ensure_deps

:create_venv_with_python
python -m venv "%ROOT_DIR%.venv"
if errorlevel 1 exit /b 1
goto ensure_deps

:ensure_deps
"%VENV_PY%" -c "import markdown_it" >nul 2>nul
if %ERRORLEVEL%==0 goto run_sync

echo Installing Python dependencies...
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency install failed. If this is a network issue, set HTTP_PROXY and HTTPS_PROXY to http://127.0.0.1:7897 and retry. 1>&2
  exit /b 1
)

:run_sync
"%VENV_PY%" scripts\sync_to_trilium.py %*
exit /b %ERRORLEVEL%
