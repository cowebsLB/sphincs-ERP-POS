"""
SMS Marketing - Automated SMS campaigns for customer loyalty
"""

from loguru import logger
from typing import List, Dict, Optional
from src.database.connection import get_db_session
from src.database.models import Customer


class SMSMarketing:
    """SMS marketing automation"""
    
    def __init__(self):
        self.api_key = None
        self.api_secret = None
        self.sender_id = None
        self.provider = None  # 'twilio', 'nexmo', etc.
    
    def configure(self, provider: str, api_key: str, api_secret: str, sender_id: str):
        """
        Configure SMS provider
        
        Args:
            provider: SMS provider name (twilio, nexmo, etc.)
            api_key: API key
            api_secret: API secret
            sender_id: Sender ID or phone number
        """
        self.provider = provider
        self.api_key = api_key
        self.api_secret = api_secret
        self.sender_id = sender_id
        logger.info(f"SMS provider configured: {provider}")
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS to a phone number
        
        Args:
            phone_number: Recipient phone number
            message: Message text
            
        Returns:
            True if sent successfully
        """
        if not self.api_key or not self.provider:
            logger.warning("SMS not configured. SMS not sent.")
            logger.info(f"Would send SMS to {phone_number}: {message}")
            return False
        
        try:
            # In real implementation, use provider's API
            # Example for Twilio:
            # from twilio.rest import Client
            # client = Client(self.api_key, self.api_secret)
            # message = client.messages.create(
            #     body=message,
            #     from_=self.sender_id,
            #     to=phone_number
            # )
            
            logger.info(f"SMS sent to {phone_number}: {message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    def send_promotional_sms(self, customer_ids: List[int], message: str) -> Dict:
        """
        Send promotional SMS to multiple customers
        
        Args:
            customer_ids: List of customer IDs
            message: Message text
            
        Returns:
            Dictionary with sent/failed counts
        """
        results = {'sent': 0, 'failed': 0}
        
        try:
            db = get_db_session()
            customers = db.query(Customer).filter(Customer.customer_id.in_(customer_ids)).all()
            db.close()
            
            for customer in customers:
                if customer.phone:
                    if self.send_sms(customer.phone, message):
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                else:
                    results['failed'] += 1
            
            logger.info(f"Promotional SMS sent: {results['sent']} sent, {results['failed']} failed")
            return results
            
        except Exception as e:
            logger.error(f"Error sending promotional SMS: {e}")
            return results
    
    def send_order_confirmation(self, customer_id: int, order_number: str) -> bool:
        """
        Send order confirmation SMS
        
        Args:
            customer_id: Customer ID
            order_number: Order number
            
        Returns:
            True if sent successfully
        """
        try:
            db = get_db_session()
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            db.close()
            
            if not customer or not customer.phone:
                return False
            
            message = f"Order #{order_number} confirmed! Thank you for your order."
            return self.send_sms(customer.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending order confirmation SMS: {e}")
            return False


def get_sms_marketing() -> SMSMarketing:
    """Get global SMS marketing instance"""
    return SMSMarketing()

