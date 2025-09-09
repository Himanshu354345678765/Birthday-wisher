from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self, account_sid=None, auth_token=None, whatsapp_number=None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.whatsapp_number = whatsapp_number
        self.client = None
        
        if account_sid and auth_token:
            try:
                self.client = Client(account_sid, auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {str(e)}")
    
    def is_configured(self):
        """Check if WhatsApp service is properly configured"""
        return all([self.account_sid, self.auth_token, self.whatsapp_number, self.client])
    
    def send_birthday_message(self, contact_name, contact_number, wisher_name):
        """Send a personalized birthday message"""
        if not self.is_configured():
            logger.error("WhatsApp service not properly configured")
            return False, "WhatsApp service not configured"
        
        try:
            # Format the birthday message
            message_body = self.format_birthday_message(contact_name, wisher_name)
            
            # Ensure the contact number is in the correct format
            formatted_number = self.format_phone_number(contact_number)
            
            # Ensure the Twilio from number is in WhatsApp channel format
            from_number = self.whatsapp_number or ""
            if not from_number.startswith("whatsapp:"):
                # Normalize any raw phone number to E.164, then prefix with whatsapp:
                normalized_from = self.format_phone_number(from_number) if from_number else from_number
                from_number = f"whatsapp:{normalized_from}" if normalized_from else from_number
            
            # Send the message
            message = self.client.messages.create(
                body=message_body,
                from_=from_number,
                to=f"whatsapp:{formatted_number}"
            )
            
            logger.info(f"Birthday message sent successfully to {contact_name} ({formatted_number}). Message SID: {message.sid}")
            return True, f"Message sent successfully (SID: {message.sid})"
            
        except TwilioException as e:
            logger.error(f"Twilio error sending message to {contact_name}: {str(e)}")
            return False, f"Twilio error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error sending message to {contact_name}: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def format_birthday_message(self, contact_name, wisher_name):
        """Format a birthday message using the business-specified template"""
        return (
            "Hi there! This is Ribbon & Balloons with Asha Traders, and today’s a super special day – it’s your Birthday! "
            "Wishing you loads of happiness, laughter, and sweet surprises. Happiest Birthday from all of us to you!"
        )
    
    def format_phone_number(self, phone_number):
        """Format phone number to ensure it works with WhatsApp"""
        # Remove any existing whatsapp: prefix
        if phone_number.startswith("whatsapp:"):
            phone_number = phone_number.replace("whatsapp:", "")
        
        # Remove any spaces, dashes, or parentheses
        cleaned_number = ''.join(filter(str.isdigit, phone_number.replace('+', '')))
        
        # Add + prefix if not present
        if not phone_number.startswith('+'):
            cleaned_number = '+' + cleaned_number
        else:
            cleaned_number = '+' + cleaned_number
            
        return cleaned_number
    
    def send_test_message(self, test_number, wisher_name):
        """Send a test message to verify WhatsApp integration"""
        if not self.is_configured():
            return False, "WhatsApp service not configured"
        
        try:
            message_body = f"🧪 Test message from Birthday Reminder App!\n\nThis is a test to verify your WhatsApp integration is working correctly.\n\n– from {wisher_name}"
            formatted_number = self.format_phone_number(test_number)
            
            # Ensure the Twilio from number is in WhatsApp channel format
            from_number = self.whatsapp_number or ""
            if not from_number.startswith("whatsapp:"):
                normalized_from = self.format_phone_number(from_number) if from_number else from_number
                from_number = f"whatsapp:{normalized_from}" if normalized_from else from_number
            
            message = self.client.messages.create(
                body=message_body,
                from_=from_number,
                to=f"whatsapp:{formatted_number}"
            )
            
            logger.info(f"Test message sent successfully to {formatted_number}. Message SID: {message.sid}")
            return True, f"Test message sent successfully (SID: {message.sid})"
            
        except TwilioException as e:
            logger.error(f"Twilio error sending test message: {str(e)}")
            return False, f"Twilio error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error sending test message: {str(e)}")
            return False, f"Unexpected error: {str(e)}"

def create_whatsapp_service(settings):
    """Factory function to create WhatsApp service from settings"""
    return WhatsAppService(
        account_sid=settings.get('twilio_account_sid'),
        auth_token=settings.get('twilio_auth_token'),
        whatsapp_number=settings.get('twilio_whatsapp_number')
    )
