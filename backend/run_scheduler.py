"""
Standalone script to run the birthday scheduler service
This can be run as a separate process for production deployments
"""

import sys
import os
import time
import signal
import logging
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scheduler_service import BirthdayScheduler
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('birthday_scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = None
        self.running = False
    
    def start(self, check_hour=9, check_minute=0):
        """Start the scheduler service"""
        logger.info("Starting Birthday Scheduler Service...")
        
        try:
            with app.app_context():
                self.scheduler = BirthdayScheduler()
                success, message = self.scheduler.start_daily_check(check_hour, check_minute)
                
                if success:
                    self.running = True
                    logger.info(f"Scheduler started successfully: {message}")
                    
                    # Keep the service running
                    self.keep_alive()
                else:
                    logger.error(f"Failed to start scheduler: {message}")
                    sys.exit(1)
        
        except Exception as e:
            logger.error(f"Error starting scheduler service: {str(e)}")
            sys.exit(1)
    
    def stop(self):
        """Stop the scheduler service"""
        logger.info("Stopping Birthday Scheduler Service...")
        
        if self.scheduler:
            self.scheduler.stop_daily_check()
        
        self.running = False
        logger.info("Scheduler service stopped")
    
    def keep_alive(self):
        """Keep the service running"""
        logger.info("Scheduler service is running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
            self.stop()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    service.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    check_hour = 9  # Default to 9 AM
    check_minute = 0  # Default to 0 minutes
    
    if len(sys.argv) > 1:
        try:
            check_hour = int(sys.argv[1])
        except ValueError:
            logger.error("Invalid hour argument. Using default (9)")
    
    if len(sys.argv) > 2:
        try:
            check_minute = int(sys.argv[2])
        except ValueError:
            logger.error("Invalid minute argument. Using default (0)")
    
    # Validate time
    if not (0 <= check_hour <= 23) or not (0 <= check_minute <= 59):
        logger.error("Invalid time. Hour must be 0-23, minute must be 0-59")
        sys.exit(1)
    
    # Start the service
    service = SchedulerService()
    service.start(check_hour, check_minute)
