"""
Utility functions for the birthday reminder app
"""

import re
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def validate_phone_number(phone_number):
    """Validate and format phone number"""
    if not phone_number:
        return False, "Phone number is required"
    
    # Remove whatsapp: prefix if present
    clean_number = phone_number.replace("whatsapp:", "").strip()
    
    # Check if it's a valid phone number format
    # Allow +, digits, spaces, dashes, and parentheses
    pattern = r'^[\+]?[1-9][\d\s\-$$$$]{7,15}$'
    
    if not re.match(pattern, clean_number):
        return False, "Invalid phone number format"
    
    return True, clean_number

def format_whatsapp_number(phone_number):
    """Format phone number for WhatsApp"""
    # Remove any existing whatsapp: prefix
    if phone_number.startswith("whatsapp:"):
        phone_number = phone_number.replace("whatsapp:", "")
    
    # Remove any spaces, dashes, or parentheses, keep + and digits
    cleaned = re.sub(r'[^\d\+]', '', phone_number)
    
    # Ensure it starts with +
    if not cleaned.startswith('+'):
        # Assume US number if no country code
        if len(cleaned) == 10:
            cleaned = '+1' + cleaned
        else:
            cleaned = '+' + cleaned
    
    return cleaned

def calculate_age(birthdate):
    """Calculate age from birthdate"""
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    
    today = date.today()
    age = today.year - birthdate.year
    
    # Adjust if birthday hasn't occurred this year
    if today < date(today.year, birthdate.month, birthdate.day):
        age -= 1
    
    return age

def get_next_birthday(birthdate):
    """Get the next birthday date for a given birthdate"""
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    
    today = date.today()
    this_year_birthday = date(today.year, birthdate.month, birthdate.day)
    
    if this_year_birthday >= today:
        return this_year_birthday
    else:
        return date(today.year + 1, birthdate.month, birthdate.day)

def days_until_birthday(birthdate):
    """Calculate days until next birthday"""
    next_birthday = get_next_birthday(birthdate)
    today = date.today()
    return (next_birthday - today).days

def is_birthday_today(birthdate):
    """Check if today is the person's birthday"""
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    
    today = date.today()
    return (today.month == birthdate.month and today.day == birthdate.day)

def log_whatsapp_activity(contact_name, phone_number, success, message, message_type="birthday"):
    """Log WhatsApp activity for debugging and monitoring"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"WhatsApp {message_type.upper()} - {status}: {contact_name} ({phone_number}) - {message}")

def sanitize_input(text, max_length=100):
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove any potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', str(text))
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()
