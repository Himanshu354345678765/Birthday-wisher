# Complete Installation Guide

This guide will walk you through setting up the Birthday Reminder App from scratch.

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.7 or higher
- **Node.js**: Version 14 or higher
- **Memory**: At least 2GB RAM
- **Storage**: 500MB free space
- **Internet**: Required for Twilio WhatsApp API

## Step-by-Step Installation

### Step 1: Download and Extract

1. Download the Birthday Reminder App files
2. Extract to a folder (e.g., `C:\BirthdayApp` or `~/BirthdayApp`)
3. Open a terminal/command prompt in this folder

### Step 2: Install Python Dependencies

#### Windows:
\`\`\`cmd
cd backend
pip install -r requirements.txt
\`\`\`

#### macOS/Linux:
\`\`\`bash
cd backend
pip3 install -r requirements.txt
\`\`\`

If you get permission errors, try:
\`\`\`bash
pip3 install --user -r requirements.txt
\`\`\`

### Step 3: Install Node.js Dependencies

\`\`\`bash
cd ../frontend
npm install
\`\`\`

If you get permission errors on macOS/Linux:
\`\`\`bash
sudo npm install
\`\`\`

### Step 4: Initialize Database

\`\`\`bash
cd ../backend
python database.py
\`\`\`

You should see:
\`\`\`
Database tables created successfully!
Sample data added successfully!
\`\`\`

### Step 5: Test Backend

\`\`\`bash
python app.py
\`\`\`

You should see:
\`\`\`
* Running on http://127.0.0.1:5000
* Debug mode: on
\`\`\`

Keep this terminal open and open a new one.

### Step 6: Test Frontend

\`\`\`bash
cd frontend
npm start
\`\`\`

You should see:
\`\`\`
Local:            http://localhost:3000
\`\`\`

Your browser should automatically open to `http://localhost:3000`.

### Step 7: Configure Twilio (Required for WhatsApp)

1. **Create Twilio Account**:
   - Go to [twilio.com](https://www.twilio.com)
   - Sign up for a free account
   - Verify your email and phone number

2. **Get Credentials**:
   - Go to [Twilio Console](https://console.twilio.com/)
   - Copy your **Account SID** and **Auth Token**

3. **Enable WhatsApp Sandbox**:
   - In Twilio Console: Messaging → Try it out → Send a WhatsApp message
   - Send a WhatsApp message to +1 415 523 8886
   - Send the join code (e.g., "join <your-code>")
   - Note the WhatsApp number: `whatsapp:+14155238886`

4. **Configure in App**:
   - Open `http://localhost:3000`
   - Go to **Settings**
   - Fill in your name and Twilio credentials
   - Click **Save Settings**

### Step 8: Add Contacts and Test

1. **Add a Contact**:
   - Go to **Contacts**
   - Click **Add Contact**
   - Enter name, birthdate, and WhatsApp number
   - Click **Add Contact**

2. **Test WhatsApp**:
   - Go to **Settings**
   - Scroll to bottom and test with your own number
   - You should receive a test message

3. **Start Scheduler**:
   - Go to **Dashboard**
   - The scheduler should start automatically
   - Check that status shows "Running"

## Troubleshooting Installation

### Python Issues

#### "Python not found"
- **Windows**: Install from [python.org](https://www.python.org/downloads/)
- **macOS**: Install via Homebrew: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

#### "pip not found"
- **Windows**: Reinstall Python with "Add to PATH" checked
- **macOS/Linux**: `sudo apt install python3-pip`

#### Permission errors
- **Windows**: Run Command Prompt as Administrator
- **macOS/Linux**: Use `sudo` or `--user` flag

### Node.js Issues

#### "npm not found"
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Restart terminal after installation

#### "EACCES permission denied"
- **macOS/Linux**: `sudo npm install -g npm`
- Or configure npm to use different directory

#### Port 3000 already in use
- Kill existing process: `npx kill-port 3000`
- Or use different port: `PORT=3001 npm start`

### Database Issues

#### "Permission denied" creating database
- Check folder permissions
- Run as administrator/sudo if needed

#### "Module not found" errors
- Ensure you're in the correct directory
- Reinstall dependencies: `pip install -r requirements.txt`

### Network Issues

#### Backend not accessible
- Check if port 5000 is blocked by firewall
- Try `http://127.0.0.1:5000` instead of `localhost`

#### Frontend can't reach backend
- Ensure backend is running on port 5000
- Check proxy configuration in `package.json`

### Twilio Issues

#### "Authentication failed"
- Double-check Account SID and Auth Token
- Ensure no extra spaces in credentials

#### "Invalid phone number"
- Use international format: +1234567890
- Include country code

#### "WhatsApp sandbox not joined"
- Send "join <code>" to Twilio WhatsApp number
- Wait for confirmation message

## Alternative Installation Methods

### Using Virtual Environment (Recommended)

\`\`\`bash
# Create virtual environment
python -m venv birthday_env

# Activate it
# Windows:
birthday_env\Scripts\activate
# macOS/Linux:
source birthday_env/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Using Docker (Advanced)

\`\`\`bash
# Build and run with Docker Compose
docker-compose up --build
\`\`\`

### Portable Installation

1. Use Python portable version
2. Install dependencies to local folder
3. Create batch/shell scripts for easy startup

## Next Steps

After successful installation:

1. **Configure Settings**: Add your name and Twilio credentials
2. **Import Contacts**: Add friends and family birthdays
3. **Test Integration**: Send a test WhatsApp message
4. **Schedule Checks**: Enable automatic daily birthday checking
5. **Backup Data**: Save your `birthday_app.db` file regularly

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check terminal/console for error messages
4. Ensure Twilio account is properly configured
5. Test with simple configurations first

## Uninstallation

To remove the application:

1. Stop all running services (Ctrl+C in terminals)
2. Delete the application folder
3. Optionally remove Python packages: `pip uninstall -r requirements.txt`
4. Optionally remove Node.js packages: `npm uninstall` in frontend folder
\`\`\`

```json file="" isHidden
