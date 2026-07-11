@echo off
setlocal

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

if not exist ".env" (
  echo Missing .env. Copy .env.example to .env and fill in Trilium settings. 1>&2
  exit /b 2
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\sync_to_trilium.py %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python scripts\sync_to_trilium.py %*
  exit /b %ERRORLEVEL%
)

echo Missing Python. Install Python 3 or make sure py/python is on PATH. 1>&2
exit /b 127
