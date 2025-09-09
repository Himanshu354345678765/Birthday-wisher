# Birthday Reminder Backend

Flask-based REST API server for the Birthday Reminder application.

## Features

- RESTful API for contact and settings management
- WhatsApp integration using Twilio API
- Background scheduler for automatic birthday checks
- SQLite database with SQLAlchemy ORM
- Comprehensive error handling and logging

## Installation

1. **Install Dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Initialize Database**:
   \`\`\`bash
   python database.py
   \`\`\`

3. **Start Server**:
   \`\`\`bash
   python app.py
   \`\`\`

## Configuration

### Environment Variables

Create a `.env` file:

\`\`\`env
SECRET_KEY=your-secret-key-here
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
\`\`\`

### Database

The application uses SQLite by default. The database file `birthday_app.db` will be created automatically.

## API Endpoints

### Contacts
- `GET /api/contacts` - Get all contacts
- `POST /api/contacts` - Create new contact
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact

### Settings
- `GET /api/settings` - Get application settings
- `POST /api/settings` - Update settings

### WhatsApp
- `POST /api/whatsapp/send-birthday-messages` - Send birthday messages
- `POST /api/whatsapp/send-test` - Send test message
- `POST /api/whatsapp/send-individual` - Send individual message
- `GET /api/whatsapp/status` - Check integration status

### Scheduler
- `POST /api/scheduler/start` - Start daily scheduler
- `POST /api/scheduler/stop` - Stop scheduler
- `GET /api/scheduler/status` - Get scheduler status
- `POST /api/scheduler/run-now` - Run manual check

### Birthdays
- `GET /api/birthdays/today` - Get today's birthdays
- `GET /api/birthdays/upcoming` - Get upcoming birthdays

## Running as Service

### Background Scheduler
\`\`\`bash
python run_scheduler.py [hour] [minute]
\`\`\`

### Combined Service
\`\`\`bash
python start_service.py
\`\`\`

## Logging

Logs are written to:
- Console output
- `birthday_scheduler.log` (for scheduler service)

## Database Schema

### Contacts Table
- `id` - Primary key
- `name` - Contact name
- `birthdate` - Birthday date
- `whatsapp_number` - WhatsApp phone number
- `created_at` - Creation timestamp

### Settings Table
- `id` - Primary key
- `wisher_name` - Name to appear in messages
- `twilio_account_sid` - Twilio Account SID
- `twilio_auth_token` - Twilio Auth Token
- `twilio_whatsapp_number` - Twilio WhatsApp number
