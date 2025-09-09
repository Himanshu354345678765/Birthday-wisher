from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, date
import logging
import atexit
from app import app, db, Contact, Settings
from whatsapp_service import create_whatsapp_service
import threading
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BirthdayScheduler:
    def __init__(self):
        # Use India Standard Time for all scheduled jobs
        ist = pytz.timezone('Asia/Kolkata')
        self.scheduler = BackgroundScheduler(timezone=ist)
        self.scheduler.start()
        self.is_running = False
        self.is_interval_running = False
        self.interval_end_job_id = 'interval_end_timer'
        
        # Register shutdown handler
        atexit.register(lambda: self.scheduler.shutdown())
        
        logger.info("Birthday Scheduler initialized")
    
    def start_daily_check(self, hour=0, minute=0):
        """Start the daily birthday check at specified time"""
        try:
            # Remove existing job if it exists
            if self.scheduler.get_job('daily_birthday_check'):
                self.scheduler.remove_job('daily_birthday_check')
            
            # Add new job
            self.scheduler.add_job(
                func=self.check_and_send_birthday_messages,
                trigger=CronTrigger(hour=hour, minute=minute),
                id='daily_birthday_check',
                name='Daily Birthday Check',
                replace_existing=True
            )
            
            self.is_running = True
            logger.info(f"Daily birthday check scheduled for {hour:02d}:{minute:02d}")
            return True, f"Scheduler started - daily check at {hour:02d}:{minute:02d}"
            
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            return False, f"Failed to start scheduler: {str(e)}"
    
    def stop_daily_check(self):
        """Stop the daily birthday check"""
        try:
            if self.scheduler.get_job('daily_birthday_check'):
                self.scheduler.remove_job('daily_birthday_check')
                self.is_running = False
                logger.info("Daily birthday check stopped")
                return True, "Scheduler stopped"
            else:
                return False, "No scheduled job found"
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {str(e)}")
            return False, f"Failed to stop scheduler: {str(e)}"

    def start_interval_check(self, minutes: int = 5):
        """Start an interval job to run every N minutes"""
        try:
            if minutes < 1 or minutes > 1440:
                return False, "Minutes must be between 1 and 1440"

            # Remove existing job if present
            if self.scheduler.get_job('interval_birthday_check'):
                self.scheduler.remove_job('interval_birthday_check')

            self.scheduler.add_job(
                func=self.check_and_send_birthday_messages,
                trigger=IntervalTrigger(minutes=minutes),
                id='interval_birthday_check',
                name=f'Interval Birthday Check ({minutes}m)',
                replace_existing=True
            )

            self.is_interval_running = True
            logger.info(f"Interval birthday check scheduled every {minutes} minute(s)")
            return True, f"Interval scheduler started - every {minutes} minute(s)"

        except Exception as e:
            logger.error(f"Failed to start interval scheduler: {str(e)}")
            return False, f"Failed to start interval scheduler: {str(e)}"

    def stop_interval_check(self):
        """Stop the interval birthday check"""
        try:
            if self.scheduler.get_job('interval_birthday_check'):
                self.scheduler.remove_job('interval_birthday_check')
                self.is_interval_running = False
                logger.info("Interval birthday check stopped")
                # Also remove any pending end timer
                if self.scheduler.get_job(self.interval_end_job_id):
                    self.scheduler.remove_job(self.interval_end_job_id)
                return True, "Interval scheduler stopped"
            else:
                return False, "No interval job found"
        except Exception as e:
            logger.error(f"Failed to stop interval scheduler: {str(e)}")
            return False, f"Failed to stop interval scheduler: {str(e)}"

    def start_interval_until(self, minutes: int, end_hour: int, end_minute: int):
        """Start interval checks that automatically stop at specified IST time today"""
        try:
            if minutes < 1 or minutes > 1440:
                return False, "Minutes must be between 1 and 1440"
            if not (0 <= end_hour <= 23 and 0 <= end_minute <= 59):
                return False, "Invalid end time. Hour must be 0-23, minute 0-59"

            # Start or restart the interval job
            success, message = self.start_interval_check(minutes)
            if not success:
                return False, message

            # Schedule a one-time stop at end time (IST)
            ist = self.scheduler.timezone
            now_ist = datetime.now(ist)
            end_dt = now_ist.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
            if end_dt <= now_ist:
                # If end time already passed today, stop immediately
                self.stop_interval_check()
                return False, "End time is in the past; interval not started"

            # Remove existing end timer if present
            if self.scheduler.get_job(self.interval_end_job_id):
                self.scheduler.remove_job(self.interval_end_job_id)

            self.scheduler.add_job(
                func=self.stop_interval_check,
                trigger=DateTrigger(run_date=end_dt, timezone=ist),
                id=self.interval_end_job_id,
                name=f'Interval End Timer ({end_dt.isoformat()})',
                replace_existing=True
            )

            logger.info(f"Interval end timer scheduled for {end_dt.isoformat()}")
            return True, f"Interval scheduler started - every {minutes} minute(s) until {end_dt.strftime('%H:%M IST')}"
        except Exception as e:
            logger.error(f"Failed to start interval-until scheduler: {str(e)}")
            return False, f"Failed to start interval-until scheduler: {str(e)}"
    
    def check_and_send_birthday_messages(self):
        """Check for today's birthdays and send messages"""
        logger.info("Starting daily birthday check...")
        
        try:
            with app.app_context():
                # Get settings
                settings = Settings.query.first()
                if not settings or not settings.wisher_name:
                    logger.warning("Settings not configured - skipping birthday check")
                    return
                
                # Create WhatsApp service
                whatsapp_service = create_whatsapp_service(settings.to_dict())
                
                if not whatsapp_service.is_configured():
                    logger.warning("WhatsApp integration not configured - skipping birthday check")
                    return
                
                # Get today's birthdays
                today = date.today()
                birthday_contacts = Contact.query.filter(
                    db.extract('month', Contact.birthdate) == today.month,
                    db.extract('day', Contact.birthdate) == today.day
                ).all()
                
                if not birthday_contacts:
                    logger.info("No birthdays today")
                    return
                
                logger.info(f"Found {len(birthday_contacts)} birthday(s) today")
                
                sent_count = 0
                failed_count = 0
                
                for contact in birthday_contacts:
                    try:
                        success, message = whatsapp_service.send_birthday_message(
                            contact.name, 
                            contact.whatsapp_number, 
                            settings.wisher_name
                        )
                        
                        if success:
                            sent_count += 1
                            logger.info(f"Birthday message sent to {contact.name}")
                        else:
                            failed_count += 1
                            logger.error(f"Failed to send birthday message to {contact.name}: {message}")
                    
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Error sending message to {contact.name}: {str(e)}")
                
                logger.info(f"Birthday check completed - Sent: {sent_count}, Failed: {failed_count}")
                
        except Exception as e:
            logger.error(f"Error during birthday check: {str(e)}")
    
    def run_manual_check(self):
        """Run birthday check manually (for testing)"""
        logger.info("Running manual birthday check...")
        
        # Run in a separate thread to avoid blocking
        thread = threading.Thread(target=self.check_and_send_birthday_messages)
        thread.daemon = True
        thread.start()
        
        return True, "Manual birthday check started"
    
    def get_status(self):
        """Get scheduler status"""
        jobs = self.scheduler.get_jobs()
        daily_job = self.scheduler.get_job('daily_birthday_check')
        interval_job = self.scheduler.get_job('interval_birthday_check')
        interval_end_job = self.scheduler.get_job(self.interval_end_job_id)

        status = {
            'job_count': len(jobs),
            'daily': {
                'running': bool(daily_job),
                'next_run': daily_job.next_run_time.isoformat() if daily_job and daily_job.next_run_time else None,
            },
            'interval': {
                'running': bool(interval_job),
                'next_run': interval_job.next_run_time.isoformat() if interval_job and interval_job.next_run_time else None,
                'interval_minutes': None,
                'end_time': interval_end_job.next_run_time.isoformat() if interval_end_job and interval_end_job.next_run_time else None
            }
        }

        # Try to parse interval from job name
        if interval_job and interval_job.trigger and hasattr(interval_job.trigger, 'interval'):
            try:
                total_seconds = interval_job.trigger.interval.total_seconds()
                status['interval']['interval_minutes'] = int(total_seconds // 60)
            except Exception:
                pass

        # Back-compat top-level flags
        status['running'] = bool(daily_job or interval_job)
        status['next_run'] = status['daily']['next_run'] or status['interval']['next_run']
        return status
    
    def get_next_birthdays(self, days_ahead=7):
        """Get upcoming birthdays in the next N days"""
        try:
            with app.app_context():
                upcoming = []
                today = date.today()
                
                contacts = Contact.query.all()
                
                for contact in contacts:
                    # Calculate next birthday
                    birth_month = contact.birthdate.month
                    birth_day = contact.birthdate.day
                    
                    # Try this year first
                    try:
                        next_birthday = date(today.year, birth_month, birth_day)
                        if next_birthday < today:
                            # Birthday already passed this year, use next year
                            next_birthday = date(today.year + 1, birth_month, birth_day)
                    except ValueError:
                        # Handle leap year edge case (Feb 29)
                        next_birthday = date(today.year + 1, birth_month, birth_day)
                    
                    days_until = (next_birthday - today).days
                    
                    if 0 <= days_until <= days_ahead:
                        upcoming.append({
                            'contact': contact.to_dict(),
                            'next_birthday': next_birthday.isoformat(),
                            'days_until': days_until
                        })
                
                # Sort by days until birthday
                upcoming.sort(key=lambda x: x['days_until'])
                
                return upcoming
                
        except Exception as e:
            logger.error(f"Error getting upcoming birthdays: {str(e)}")
            return []

# Global scheduler instance
birthday_scheduler = BirthdayScheduler()

def get_scheduler():
    """Get the global scheduler instance"""
    return birthday_scheduler
