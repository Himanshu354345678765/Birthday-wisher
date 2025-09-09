"""
Message templates for birthday wishes and other notifications
"""

class MessageTemplates:
    
    BIRTHDAY_MESSAGES = [
        "🎉 Happy Birthday {name}! 🎂\n\nWishing you a wonderful day filled with happiness and joy!\n\n– from {wisher}",
        "🎈 Happy Birthday {name}! 🎉\n\nHope your special day is amazing and the year ahead brings you lots of happiness!\n\n– from {wisher}",
        "🎂 Happy Birthday {name}! 🎊\n\nMay this new year of your life be filled with joy, success, and wonderful memories!\n\n– from {wisher}",
        "🌟 Happy Birthday {name}! 🎁\n\nSending you warm wishes on your special day. May all your dreams come true!\n\n– from {wisher}",
        "🎵 Happy Birthday {name}! 🎉\n\nAnother year of wonderful memories! Wishing you health, happiness, and success!\n\n– from {wisher}"
    ]
    
    TEST_MESSAGE = "🧪 Test message from Birthday Reminder App!\n\nThis is a test to verify your WhatsApp integration is working correctly.\n\n– from {wisher}"
    
    REMINDER_MESSAGE = "📅 Birthday Reminder!\n\n{name}'s birthday is coming up on {date}. Don't forget to wish them well!\n\n– Birthday Reminder App"
    
    @classmethod
    def get_birthday_message(cls, name, wisher, template_index=0):
        """Get a formatted birthday message"""
        if template_index >= len(cls.BIRTHDAY_MESSAGES):
            template_index = 0
        
        return cls.BIRTHDAY_MESSAGES[template_index].format(name=name, wisher=wisher)
    
    @classmethod
    def get_test_message(cls, wisher):
        """Get a formatted test message"""
        return cls.TEST_MESSAGE.format(wisher=wisher)
    
    @classmethod
    def get_reminder_message(cls, name, date):
        """Get a formatted reminder message"""
        return cls.REMINDER_MESSAGE.format(name=name, date=date)
    
    @classmethod
    def get_random_birthday_message(cls, name, wisher):
        """Get a random birthday message"""
        import random
        template_index = random.randint(0, len(cls.BIRTHDAY_MESSAGES) - 1)
        return cls.get_birthday_message(name, wisher, template_index)
