# Birthday Reminder App

A complete PC-based web application that automatically sends personalized WhatsApp birthday messages to your contacts using Twilio's WhatsApp API.

## Features

- 📱 **WhatsApp Integration**: Send automated birthday messages via Twilio WhatsApp API
- 📅 **Daily Scheduler**: Automatic daily checks for birthdays at configurable times
- 👥 **Contact Management**: Easy-to-use interface for managing contacts and birthdays
- 🎨 **Modern UI**: Clean, responsive React frontend with professional design
- ⚙️ **Settings Management**: Configure your name, Twilio credentials, and scheduler settings
- 🔄 **Manual Controls**: Send individual messages or run manual birthday checks
- 📊 **Dashboard**: View upcoming birthdays and system status

## Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **SQLAlchemy**: Database ORM with SQLite
- **APScheduler**: Background task scheduling
- **Twilio**: WhatsApp message delivery
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: Modern UI framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icons
- **Date-fns**: Date manipulation utilities

## Prerequisites

- **Python 3.7+** with pip
- **Node.js 14+** with npm
- **Twilio Account** (free tier available)
- **Modern web browser**

## Quick Start

### 1. Clone or Download

Download the project files to your computer and extract them to a folder.

### 2. Backend Setup

\`\`\`bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Start the Flask server
python app.py
\`\`\`

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

\`\`\`bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
\`\`\`

The frontend will start on `http://localhost:3000`

### 4. Configure Twilio WhatsApp

1. **Create Twilio Account**: Sign up at [twilio.com](https://www.twilio.com)
2. **Get Credentials**: Find your Account SID and Auth Token in the Console
3. **Enable WhatsApp Sandbox**: Go to Messaging → Try it out → Send a WhatsApp message
4. **Configure in App**: Add credentials in the Settings page

### 5. Add Contacts and Start Scheduler

1. Open `http://localhost:3000` in your browser
2. Go to **Settings** and configure your name and Twilio credentials
3. Go to **Contacts** and add people with their birthdays
4. Return to **Dashboard** and start the scheduler

## Detailed Setup Instructions

### Backend Installation

1. **Install Python Dependencies**:
   \`\`\`bash
   cd backend
   pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-CORS==4.0.0 APScheduler==3.10.4 twilio==8.9.1 python-dotenv==1.0.0
   \`\`\`

2. **Environment Configuration** (Optional):
   \`\`\`bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env
   \`\`\`

3. **Database Setup**:
   \`\`\`bash
   # Initialize database and add sample data
   python database.py
   \`\`\`

4. **Start Backend Server**:
   \`\`\`bash
   # Development mode
   python app.py
   
   # Or with scheduler service
   python start_service.py
   \`\`\`

### Frontend Installation

1. **Install Node.js Dependencies**:
   \`\`\`bash
   cd frontend
   npm install
   \`\`\`

2. **Start Development Server**:
   \`\`\`bash
   npm start
   \`\`\`

3. **Build for Production** (Optional):
   \`\`\`bash
   npm run build
   \`\`\`

### Twilio WhatsApp Setup

#### Step 1: Create Twilio Account
1. Go to [twilio.com](https://www.twilio.com) and sign up
2. Verify your email and phone number
3. Complete the account setup process

#### Step 2: Get Your Credentials
1. Go to the [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token** on the dashboard
3. Copy these values for later use

#### Step 3: Enable WhatsApp Sandbox
1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Follow the instructions to join the sandbox:
   - Send a WhatsApp message to the provided number (usually +1 415 523 8886)
   - Send the code provided (e.g., "join <code>")
3. Note the WhatsApp number (format: `whatsapp:+14155238886`)

#### Step 4: Configure in App
1. Open the Birthday Reminder App
2. Go to **Settings**
3. Fill in:
   - **Your Name**: How you want to appear in messages
   - **Twilio Account SID**: From step 2
   - **Twilio Auth Token**: From step 2
   - **Twilio WhatsApp Number**: From step 3 (include `whatsapp:` prefix)
4. Click **Save Settings**

## Usage Guide

### Adding Contacts

1. Go to the **Contacts** page
2. Click **Add Contact**
3. Fill in:
   - **Name**: Full name of the person
   - **Birthdate**: Their birthday (YYYY-MM-DD format)
   - **WhatsApp Number**: Their WhatsApp number (include country code)
4. Click **Add Contact**

### Managing the Scheduler

#### Start Automatic Birthday Checks
1. Go to **Dashboard**
2. The scheduler status will show if it's running
3. Configure the daily check time (default: 9:00 AM)
4. The system will automatically check for birthdays and send messages

#### Manual Operations
- **Send Test Message**: Verify your WhatsApp integration
- **Run Manual Check**: Check for today's birthdays immediately
- **Send Individual Message**: Send birthday message to specific contact

### Dashboard Overview

The dashboard shows:
- **Total Contacts**: Number of people in your contact list
- **Today's Birthdays**: People celebrating today
- **Upcoming Birthdays**: Next 30 days of birthdays
- **Scheduler Status**: Whether automatic checking is enabled

## API Documentation

### Contacts API

\`\`\`bash
# Get all contacts
GET /api/contacts

# Add new contact
POST /api/contacts
{
  "name": "John Doe",
  "birthdate": "1990-12-25",
  "whatsapp_number": "+1234567890"
}

# Update contact
PUT /api/contacts/{id}

# Delete contact
DELETE /api/contacts/{id}
\`\`\`

### WhatsApp API

\`\`\`bash
# Send birthday messages to today's birthdays
POST /api/whatsapp/send-birthday-messages

# Send test message
POST /api/whatsapp/send-test
{
  "test_number": "+1234567890"
}

# Send individual birthday message
POST /api/whatsapp/send-individual
{
  "contact_id": 1
}

# Check WhatsApp integration status
GET /api/whatsapp/status
\`\`\`

### Scheduler API

\`\`\`bash
# Start scheduler
POST /api/scheduler/start
{
  "hour": 9,
  "minute": 0
}

# Stop scheduler
POST /api/scheduler/stop

# Get scheduler status
GET /api/scheduler/status

# Run manual check
POST /api/scheduler/run-now
\`\`\`

## Troubleshooting

### Common Issues

#### "WhatsApp integration not configured"
- **Solution**: Add your Twilio credentials in Settings
- **Check**: Account SID, Auth Token, and WhatsApp number are correct

#### "Settings not configured"
- **Solution**: Add your name in the Settings page
- **Note**: Your name appears in birthday messages

#### Messages not sending
- **Check**: WhatsApp sandbox is active (send "join <code>" to Twilio number)
- **Verify**: Phone numbers include country codes (e.g., +1234567890)
- **Test**: Use the "Send Test Message" feature first

#### Scheduler not working
- **Check**: Scheduler is started from the Dashboard
- **Verify**: Time zone settings on your computer
- **Note**: Scheduler runs in the background - check logs for activity

#### Frontend won't connect to backend
- **Solution**: Ensure backend is running on port 5000
- **Check**: No firewall blocking localhost connections
- **Verify**: Both frontend and backend are running

### Error Messages

#### "Twilio error: 20003"
- **Meaning**: Authentication failed
- **Solution**: Check Account SID and Auth Token

#### "Twilio error: 21211"
- **Meaning**: Invalid phone number
- **Solution**: Use correct format with country code (+1234567890)

#### "Twilio error: 63016"
- **Meaning**: WhatsApp sandbox not joined
- **Solution**: Send "join <code>" message to Twilio WhatsApp number

## Production Deployment

### Option 1: Simple Local Deployment

1. **Start Both Services**:
   \`\`\`bash
   # Windows
   start.bat
   
   # Linux/Mac
   chmod +x start.sh
   ./start.sh
   \`\`\`

2. **Access Application**: Open `http://localhost:3000`

### Option 2: Separate Services

1. **Backend Service**:
   \`\`\`bash
   cd backend
   python run_scheduler.py  # Runs scheduler only
   python app.py           # Runs API server
   \`\`\`

2. **Frontend Build**:
   \`\`\`bash
   cd frontend
   npm run build
   # Serve build folder with web server
   \`\`\`

### Option 3: Docker Deployment (Advanced)

Create `docker-compose.yml` for containerized deployment:

\`\`\`yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
\`\`\`

## Security Considerations

- **Credentials**: Never commit Twilio credentials to version control
- **Environment**: Use `.env` files for sensitive configuration
- **Network**: Consider firewall rules for production deployment
- **Database**: Backup your SQLite database regularly
- **Updates**: Keep dependencies updated for security patches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages and logs
3. Verify Twilio account and WhatsApp sandbox status
4. Test with simple configurations first

## Changelog

### Version 1.0.0
- Initial release
- WhatsApp integration via Twilio
- Automatic birthday scheduling
- React frontend with modern UI
- Contact management system
- Settings configuration
- Manual message sending
- Comprehensive documentation
