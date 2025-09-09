from app import app, db, Contact, Settings

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def add_sample_data():
    """Add sample data for testing"""
    with app.app_context():
        # Check if data already exists
        if Contact.query.first():
            print("Sample data already exists!")
            return
        
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

if __name__ == '__main__':
    init_db()
    add_sample_data()
