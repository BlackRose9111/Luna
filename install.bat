:: Check if Python 3 is installed on the system

@echo off
set "MIN_PYTHON_MAJOR_VERSION=3"
set "MIN_PYTHON_MINOR_VERSION=8"

REM Check if Python is installed and meets the minimum version requirement
for /f "tokens=2 delims=." %%a in ('python --version 2^>^&1') do (
    set "PYTHON_VERSION=%%a"
    set "PYTHON_MINOR_VERSION=%%b"
)

REM Compare the Python version with the minimum required version
if %PYTHON_VERSION% LSS %MIN_PYTHON_MAJOR_VERSION% (
    echo Python is not installed or does not meet the minimum version requirement. Exiting
    exit /b 1
) else if %PYTHON_VERSION% EQU %MIN_PYTHON_MAJOR_VERSION% (
    if %PYTHON_MINOR_VERSION% LSS %MIN_PYTHON_MINOR_VERSION% (
        echo Python is installed, but the version is below the required minimum version of %MIN_PYTHON_MAJOR_VERSION%.%MIN_PYTHON_MINOR_VERSION%. Exiting
        exit /b 1
    )
) else (
    echo Python %MIN_PYTHON_MAJOR_VERSION%.%MIN_PYTHON_MINOR_VERSION% or higher is installed.
)

:: create a virtual environment and install the required packages
if exist venv (
    rd /s /q venv
)

python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

:: create a Token.json file and write {} to it
echo {} > Token.json

echo Installation completed, run start.bat to start the bot
pause
