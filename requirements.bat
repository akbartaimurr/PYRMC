@echo off
REM Install Python packages listed in requirements.txt

REM Ensure pip is up-to-date
python -m pip install --upgrade pip

REM Install packages from requirements.txt
python -m pip install -r requirements.txt

REM Check if installation was successful
if %errorlevel% equ 0 (
    echo All packages were successfully installed.
) else (
    echo Error occurred during package installation.
)
pause