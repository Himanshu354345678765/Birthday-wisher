"""
Simple script to start both Flask app and scheduler service
"""

import subprocess
import sys
import os
import time
import signal
from multiprocessing import Process

def start_flask_app():
    """Start the Flask application"""
    os.system("python app.py")

def start_scheduler():
    """Start the scheduler service"""
    os.system("python run_scheduler.py")

def main():
    print("Starting Birthday Reminder App...")
    
    # Start Flask app in a separate process
    flask_process = Process(target=start_flask_app)
    flask_process.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start scheduler in a separate process
    scheduler_process = Process(target=start_scheduler)
    scheduler_process.start()
    
    try:
        print("Both services are running...")
        print("Flask app: http://localhost:5000")
        print("Press Ctrl+C to stop all services")
        
        # Wait for processes
        flask_process.join()
        scheduler_process.join()
        
    except KeyboardInterrupt:
        print("\nStopping services...")
        
        # Terminate processes
        flask_process.terminate()
        scheduler_process.terminate()
        
        # Wait for clean shutdown
        flask_process.join(timeout=5)
        scheduler_process.join(timeout=5)
        
        print("Services stopped")

if __name__ == "__main__":
    main()
