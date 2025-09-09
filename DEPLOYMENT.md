# Deployment Guide

This guide covers different deployment options for the Birthday Reminder App.

## Local Development Deployment

### Quick Start (Recommended)
\`\`\`bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
\`\`\`

### Manual Start
\`\`\`bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Scheduler (Optional)
cd backend
python run_scheduler.py
\`\`\`

## Production Deployment

### Option 1: Docker Compose (Recommended)

1. **Prerequisites**:
   - Docker and Docker Compose installed
   - 2GB RAM minimum
   - Ports 3000 and 5000 available

2. **Deploy**:
   \`\`\`bash
   # Build and start services
   docker-compose up -d --build
   
   # Check status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   \`\`\`

3. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

4. **Stop**:
   \`\`\`bash
   docker-compose down
   \`\`\`

### Option 2: Systemd Service (Linux)

1. **Create service file** `/etc/systemd/system/birthday-reminder.service`:
   \`\`\`ini
   [Unit]
   Description=Birthday Reminder App
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/birthday-reminder
   ExecStart=/usr/bin/python3 /opt/birthday-reminder/backend/start_service.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   \`\`\`

2. **Enable and start**:
   \`\`\`bash
   sudo systemctl daemon-reload
   sudo systemctl enable birthday-reminder
   sudo systemctl start birthday-reminder
   \`\`\`

### Option 3: Windows Service

1. **Install NSSM** (Non-Sucking Service Manager)
2. **Create service**:
   \`\`\`cmd
   nssm install BirthdayReminder
   nssm set BirthdayReminder Application "C:\Python39\python.exe"
   nssm set BirthdayReminder AppParameters "C:\BirthdayApp\backend\start_service.py"
   nssm set BirthdayReminder AppDirectory "C:\BirthdayApp\backend"
   nssm start BirthdayReminder
   \`\`\`

### Option 4: Cloud Deployment

#### Heroku
\`\`\`bash
# Install Heroku CLI
# Create Procfile in root:
echo "web: cd backend && python app.py" > Procfile
echo "worker: cd backend && python run_scheduler.py" >> Procfile

# Deploy
heroku create birthday-reminder-app
git push heroku main
\`\`\`

#### DigitalOcean App Platform
\`\`\`yaml
# .do/app.yaml
name: birthday-reminder
services:
- name: backend
  source_dir: backend
  github:
    repo: your-username/birthday-reminder
    branch: main
  run_command: python start_service.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  
- name: frontend
  source_dir: frontend
  github:
    repo: your-username/birthday-reminder
    branch: main
  build_command: npm run build
  run_command: npx serve -s build
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
\`\`\`

## Environment Configuration

### Production Environment Variables

Create `.env` file in backend directory:
\`\`\`env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///data/birthday_app.db

# Twilio Configuration (Optional - can be set via UI)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Scheduler Configuration
SCHEDULER_HOUR=9
SCHEDULER_MINUTE=0
\`\`\`

### Security Considerations

1. **Change Default Secret Key**:
   \`\`\`python
   import secrets
   print(secrets.token_hex(32))
   \`\`\`

2. **Use HTTPS in Production**:
   - Configure reverse proxy (nginx/Apache)
   - Obtain SSL certificate (Let's Encrypt)

3. **Database Security**:
   - Regular backups
   - Proper file permissions
   - Consider PostgreSQL for production

4. **Firewall Configuration**:
   \`\`\`bash
   # Allow only necessary ports
   ufw allow 22    # SSH
   ufw allow 80    # HTTP
   ufw allow 443   # HTTPS
   ufw enable
   \`\`\`

## Monitoring and Maintenance

### Health Checks

\`\`\`bash
# Backend health
curl http://localhost:5000/api/whatsapp/status

# Frontend health
curl http://localhost:3000

# Scheduler status
curl http://localhost:5000/api/scheduler/status
\`\`\`

### Log Monitoring

\`\`\`bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs
journalctl -u birthday-reminder -f

# Application logs
tail -f backend/birthday_scheduler.log
\`\`\`

### Backup Strategy

\`\`\`bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp backend/birthday_app.db "backups/birthday_app_$DATE.db"
find backups/ -name "*.db" -mtime +30 -delete
\`\`\`

### Updates

\`\`\`bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Or for manual deployment
cd backend && pip install -r requirements.txt
cd ../frontend && npm install && npm run build
\`\`\`

## Troubleshooting Production Issues

### Common Problems

1. **Port conflicts**:
   \`\`\`bash
   netstat -tulpn | grep :5000
   lsof -i :3000
   \`\`\`

2. **Permission issues**:
   \`\`\`bash
   chown -R www-data:www-data /opt/birthday-reminder
   chmod +x backend/start_service.py
   \`\`\`

3. **Memory issues**:
   \`\`\`bash
   free -h
   docker stats
   \`\`\`

4. **Database corruption**:
   \`\`\`bash
   sqlite3 birthday_app.db ".backup backup.db"
   \`\`\`

### Performance Optimization

1. **Enable gzip compression**
2. **Use CDN for static assets**
3. **Implement caching**
4. **Monitor resource usage**
5. **Set up log rotation**

## Scaling Considerations

For high-volume deployments:

1. **Database**: Migrate to PostgreSQL
2. **Queue System**: Add Redis/Celery for message processing
3. **Load Balancing**: Multiple backend instances
4. **Monitoring**: Prometheus + Grafana
5. **Error Tracking**: Sentry integration
