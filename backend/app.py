from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
import os
import dj_database_url
from werkzeug.exceptions import BadRequest
from whatsapp_service import WhatsAppService, create_whatsapp_service

app = Flask(__name__)

# Configure database based on environment
if os.environ.get('RENDER') or os.environ.get('FLASK_ENV') == 'production':
    # Use PostgreSQL in production (Render)
    database_url = os.environ.get('DATABASE_URL', '')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to PostgreSQL URL format for Render
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/birthday_app'
        print("WARNING: No DATABASE_URL found, using default PostgreSQL configuration")
else:
    # Use SQLite in development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday_app.db'
    print("Using SQLite database for development")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

db = SQLAlchemy(app)
CORS(app)

# Health & root endpoints for platform checks
@app.route('/')
def root():
    return jsonify({ 'ok': True, 'service': 'birthday-backend' })

@app.route('/api/health')
def health():
    return jsonify({ 'ok': True })

@app.route('/api/init-db', methods=['POST'])
def initialize_database():
    """Initialize the database (useful for Render deployments)"""
    try:
        from database import ensure_database_exists
        success = ensure_database_exists()
        
        if success:
            return jsonify({'success': True, 'message': 'Database initialized successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to initialize database'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Database Models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.birthdate.isoformat(),
            'whatsapp_number': self.whatsapp_number,
            'created_at': self.created_at.isoformat()
        }

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wisher_name = db.Column(db.String(100), nullable=False)
    twilio_account_sid = db.Column(db.String(100))
    twilio_auth_token = db.Column(db.String(100))
    twilio_whatsapp_number = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'wisher_name': self.wisher_name,
            'twilio_account_sid': self.twilio_account_sid,
            'twilio_auth_token': self.twilio_auth_token,
            'twilio_whatsapp_number': self.twilio_whatsapp_number
        }

# API Routes
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    try:
        data = request.get_json()
        print(f"Received contact data: {data}")
        
        # Validate required fields
        if not all(k in data for k in ('name', 'birthdate', 'whatsapp_number')):
            print(f"Missing required fields in data: {data}")
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse birthdate
        try:
            birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        except ValueError as ve:
            print(f"Invalid birthdate format: {data['birthdate']}. Error: {str(ve)}")
            return jsonify({'error': 'Invalid birthdate format. Use YYYY-MM-DD'}), 400
        
        # Create contact object
        try:
            contact = Contact(
                name=data['name'],
                birthdate=birthdate,
                whatsapp_number=data['whatsapp_number']
            )
            
            # Add to session and commit
            db.session.add(contact)
            db.session.commit()
            print(f"Contact added successfully: {contact.id}")
            
            return jsonify(contact.to_dict()), 201
        except Exception as db_error:
            db.session.rollback()
            print(f"Database error adding contact: {str(db_error)}")
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
    
    except Exception as e:
        print(f"Unexpected error in add_contact: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/scheduler/preview', methods=['GET'])
def preview_scheduled_messages():
    """Preview today's scheduled messages: contacts, message text, and scheduler status"""
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        status = scheduler.get_status()

        # Load settings and create whatsapp service for message formatting
        settings = Settings.query.first()
        if not settings:
            return jsonify({'error': 'Settings not configured'}), 400

        whatsapp_service = create_whatsapp_service(settings.to_dict())

        # Get today's birthday contacts
        today = date.today()
        birthday_contacts = Contact.query.filter(
            db.extract('month', Contact.birthdate) == today.month,
            db.extract('day', Contact.birthdate) == today.day
        ).all()

        contacts_data = []
        for c in birthday_contacts:
            message_text = whatsapp_service.format_birthday_message(c.name, settings.wisher_name) if whatsapp_service else ""
            contacts_data.append({
                'id': c.id,
                'name': c.name,
                'whatsapp_number': c.whatsapp_number,
                'message_text': message_text
            })

        return jsonify({
            'date': today.isoformat(),
            'contacts': contacts_data,
            'count': len(contacts_data),
            'scheduler_status': status
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        if 'name' in data:
            contact.name = data['name']
        if 'birthdate' in data:
            contact.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        if 'whatsapp_number' in data:
            contact.whatsapp_number = data['whatsapp_number']
        
        db.session.commit()
        return jsonify(contact.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = Settings.query.first()
    if settings:
        return jsonify(settings.to_dict())
    return jsonify({'wisher_name': '', 'twilio_account_sid': '', 'twilio_auth_token': '', 'twilio_whatsapp_number': ''})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    try:
        data = request.get_json()
        settings = Settings.query.first()
        
        if settings:
            settings.wisher_name = data.get('wisher_name', settings.wisher_name)
            settings.twilio_account_sid = data.get('twilio_account_sid', settings.twilio_account_sid)
            settings.twilio_auth_token = data.get('twilio_auth_token', settings.twilio_auth_token)
            settings.twilio_whatsapp_number = data.get('twilio_whatsapp_number', settings.twilio_whatsapp_number)
        else:
            settings = Settings(
                wisher_name=data.get('wisher_name', ''),
                twilio_account_sid=data.get('twilio_account_sid', ''),
                twilio_auth_token=data.get('twilio_auth_token', ''),
                twilio_whatsapp_number=data.get('twilio_whatsapp_number', '')
            )
            db.session.add(settings)
        
        db.session.commit()
        return jsonify(settings.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/birthdays/today', methods=['GET'])
def get_todays_birthdays():
    today = date.today()
    contacts = Contact.query.filter(
        db.extract('month', Contact.birthdate) == today.month,
        db.extract('day', Contact.birthdate) == today.day
    ).all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/api/whatsapp/send-birthday-messages', methods=['POST'])
def send_birthday_messages():
    """Send birthday messages to all contacts with birthdays today"""
    try:
        # Get settings
        settings = Settings.query.first()
        if not settings or not settings.wisher_name:
            return jsonify({'error': 'Settings not configured. Please set your name in settings.'}), 400
        
        # Create WhatsApp service
        whatsapp_service = create_whatsapp_service(settings.to_dict())
        
        if not whatsapp_service.is_configured():
            return jsonify({'error': 'WhatsApp integration not configured. Please add Twilio credentials in settings.'}), 400
        
        # Get today's birthdays
        today = date.today()
        birthday_contacts = Contact.query.filter(
            db.extract('month', Contact.birthdate) == today.month,
            db.extract('day', Contact.birthdate) == today.day
        ).all()
        
        if not birthday_contacts:
            return jsonify({'message': 'No birthdays today', 'sent_count': 0, 'results': []})
        
        results = []
        sent_count = 0
        
        for contact in birthday_contacts:
            success, message = whatsapp_service.send_birthday_message(
                contact.name, 
                contact.whatsapp_number, 
                settings.wisher_name
            )
            
            results.append({
                'contact_name': contact.name,
                'contact_number': contact.whatsapp_number,
                'success': success,
                'message': message
            })
            
            if success:
                sent_count += 1
        
        return jsonify({
            'message': f'Birthday messages processed for {len(birthday_contacts)} contacts',
            'sent_count': sent_count,
            'total_count': len(birthday_contacts),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/send-test', methods=['POST'])
def send_test_message():
    """Send a test WhatsApp message"""
    try:
        data = request.get_json()
        test_number = data.get('test_number')
        
        if not test_number:
            return jsonify({'error': 'Test number is required'}), 400
        
        # Get settings
        settings = Settings.query.first()
        if not settings or not settings.wisher_name:
            return jsonify({'error': 'Settings not configured. Please set your name in settings.'}), 400
        
        # Create WhatsApp service
        whatsapp_service = create_whatsapp_service(settings.to_dict())
        
        if not whatsapp_service.is_configured():
            return jsonify({'error': 'WhatsApp integration not configured. Please add Twilio credentials in settings.'}), 400
        
        success, message = whatsapp_service.send_test_message(test_number, settings.wisher_name)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/send-individual', methods=['POST'])
def send_individual_birthday_message():
    """Send birthday message to a specific contact"""
    try:
        data = request.get_json()
        contact_id = data.get('contact_id')
        
        if not contact_id:
            return jsonify({'error': 'Contact ID is required'}), 400
        
        # Get contact
        contact = Contact.query.get_or_404(contact_id)
        
        # Get settings
        settings = Settings.query.first()
        if not settings or not settings.wisher_name:
            return jsonify({'error': 'Settings not configured. Please set your name in settings.'}), 400
        
        # Create WhatsApp service
        whatsapp_service = create_whatsapp_service(settings.to_dict())
        
        if not whatsapp_service.is_configured():
            return jsonify({'error': 'WhatsApp integration not configured. Please add Twilio credentials in settings.'}), 400
        
        success, message = whatsapp_service.send_birthday_message(
            contact.name, 
            contact.whatsapp_number, 
            settings.wisher_name
        )
        
        if success:
            return jsonify({
                'success': True, 
                'message': f'Birthday message sent to {contact.name}',
                'details': message
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/status', methods=['GET'])
def get_whatsapp_status():
    """Check WhatsApp integration status"""
    try:
        settings = Settings.query.first()
        
        if not settings:
            return jsonify({
                'configured': False,
                'message': 'No settings found'
            })
        
        whatsapp_service = create_whatsapp_service(settings.to_dict())
        is_configured = whatsapp_service.is_configured()
        
        return jsonify({
            'configured': is_configured,
            'has_wisher_name': bool(settings.wisher_name),
            'has_twilio_credentials': bool(settings.twilio_account_sid and settings.twilio_auth_token),
            'has_whatsapp_number': bool(settings.twilio_whatsapp_number),
            'message': 'WhatsApp integration is ready' if is_configured else 'WhatsApp integration needs configuration'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Note: Avoid top-level import of scheduler_service to prevent circular imports.

@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """Start the birthday scheduler"""
    try:
        from scheduler_service import get_scheduler
        data = request.get_json() or {}
        hour = data.get('hour', 9)  # Default to 9 AM
        minute = data.get('minute', 0)  # Default to 0 minutes
        
        # Validate time
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            return jsonify({'error': 'Invalid time format. Hour must be 0-23, minute must be 0-59'}), 400
        
        scheduler = get_scheduler()
        success, message = scheduler.start_daily_check(hour, minute)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """Stop the birthday scheduler"""
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        success, message = scheduler.stop_daily_check()
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """Get scheduler status"""
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        status = scheduler.get_status()
        return jsonify(status)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/start-interval', methods=['POST'])
def start_interval_scheduler():
    """Start the interval birthday scheduler (every N minutes)"""
    try:
        from scheduler_service import get_scheduler
        data = request.get_json() or {}
        minutes = data.get('minutes', 5)
        
        if not isinstance(minutes, int):
            return jsonify({'error': 'Minutes must be an integer'}), 400
        
        scheduler = get_scheduler()
        success, message = scheduler.start_interval_check(minutes)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/stop-interval', methods=['POST'])
def stop_interval_scheduler():
    """Stop the interval birthday scheduler"""
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        success, message = scheduler.stop_interval_check()
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/start-interval-until', methods=['POST'])
def start_interval_until():
    """Start interval scheduler every N minutes until a specific IST time today"""
    try:
        from scheduler_service import get_scheduler
        data = request.get_json() or {}
        minutes = data.get('minutes', 5)
        end_hour = data.get('end_hour')
        end_minute = data.get('end_minute')

        if end_hour is None or end_minute is None:
            return jsonify({'error': 'end_hour and end_minute are required'}), 400
        if not isinstance(minutes, int) or not isinstance(end_hour, int) or not isinstance(end_minute, int):
            return jsonify({'error': 'minutes, end_hour, end_minute must be integers'}), 400

        scheduler = get_scheduler()
        success, message = scheduler.start_interval_until(minutes, end_hour, end_minute)

        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/run-now', methods=['POST'])
def run_scheduler_now():
    """Run birthday check manually"""
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        success, message = scheduler.run_manual_check()
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/birthdays/upcoming', methods=['GET'])
def get_upcoming_birthdays():
    """Get upcoming birthdays"""
    try:
        from scheduler_service import get_scheduler
        days_ahead = request.args.get('days', 7, type=int)
        
        if days_ahead < 1 or days_ahead > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        scheduler = get_scheduler()
        upcoming = scheduler.get_next_birthdays(days_ahead)
        
        return jsonify({
            'upcoming_birthdays': upcoming,
            'days_ahead': days_ahead,
            'count': len(upcoming)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize database handled in __main__ block below

if __name__ == '__main__':
    # Initialize database
    from database import ensure_database_exists
    ensure_database_exists()
    
    # Auto-start scheduler at 21:55 IST each day
    try:
        from scheduler_service import get_scheduler
        scheduler = get_scheduler()
        # 21:50 in IST (scheduler timezone is configured to Asia/Kolkata)
        scheduler.start_daily_check(21, 50)
    except Exception as e:
        # Fail silently if scheduler cannot start; API will still run
        print(f"Scheduler auto-start failed: {e}")

    # Bind to Render's host/port
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host=host, port=port, debug=debug)
