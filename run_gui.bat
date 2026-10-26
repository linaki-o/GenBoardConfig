@echo off
rem GenBoardConfig launcher - no venv activation needed (works under PowerShell execution policy)
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment .venv ...
    python -m venv .venv
    if errorlevel 1 goto :fail
)

set "PY=.venv\Scripts\python.exe"

echo [2/3] Installing dependencies ...
"%PY%" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :fail

echo [3/3] Starting GenBoardConfig ...
set "PYTHONPATH=%~dp0src"
"%PY%" -m genboardconfig
if errorlevel 1 goto :fail
goto :eof

:fail
echo.
echo [FAILED] See the error above. If pip is slow, use a mirror:
echo    .venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
exit /b 1
