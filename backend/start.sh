#!/bin/bash

# Birthday Reminder App Startup Script

echo "Starting Birthday Reminder App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Initialize database
echo "Initializing database..."
python3 database.py

# Start the services
echo "Starting Flask app and scheduler..."
python3 start_service.py
