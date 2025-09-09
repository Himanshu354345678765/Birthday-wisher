import os
from app import app, db, Contact, Settings

def init_db():
    """Initialize the database with tables"""
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
            return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False

def add_sample_data():
    """Add sample data for testing"""
    try:
        with app.app_context():
            # Check if data already exists
            if Contact.query.first():
                print("Sample data already exists!")
                return True
            
            from datetime import date
            
            # Add sample contacts
            sample_contacts = [
                Contact(name="John Doe", birthdate=date(1990, 12, 25), whatsapp_number="+1234567890"),
                Contact(name="Jane Smith", birthdate=date(1985, 6, 15), whatsapp_number="+0987654321"),
                Contact(name="Bob Johnson", birthdate=date(1992, 3, 8), whatsapp_number="+1122334455")
            ]
            
            for contact in sample_contacts:
                db.session.add(contact)
            
            # Add default settings
            default_settings = Settings(
                wisher_name="Your Name",
                twilio_account_sid="",
                twilio_auth_token="",
                twilio_whatsapp_number=""
            )
            db.session.add(default_settings)
            
            db.session.commit()
            print("Sample data added successfully!")
            return True
    except Exception as e:
        print(f"Error adding sample data: {str(e)}")
        return False

def ensure_database_exists():
    """Ensure database exists and is initialized with tables and sample data"""
    # Only add sample data in development environment
    is_production = os.environ.get('RENDER') or os.environ.get('FLASK_ENV') == 'production'
    
    if init_db():
        if not is_production:
            add_sample_data()
            print("Development database initialized with sample data")
        else:
            print("Production database initialized without sample data")
        return True
    return False

if __name__ == '__main__':
    ensure_database_exists()
