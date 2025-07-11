@echo off
cd ..

@echo Setting up virtual environment...

@REM Remove existing virtual environment if it exists
if exist .venv (
    echo Removing existing virtual environment...
    rmdir /s /q .venv
)

@REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

@REM Install dependencies
echo Installing dependencies...
call .venv\Scripts\activate
pip install -r setup\requirements.txt
call .venv\Scripts\deactivate.bat

echo Virtual environment setup complete.