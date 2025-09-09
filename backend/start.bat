@echo off
echo Starting Birthday Reminder App...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed.
    pause
    exit /b 1
)

REM Install dependencies
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

REM Initialize database
echo Initializing database...
python database.py

REM Start the services
echo Starting Flask app and scheduler...
python start_service.py

pause
