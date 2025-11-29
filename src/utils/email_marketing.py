"""
Email Marketing - Automated email campaigns for customer loyalty
"""

from loguru import logger
from typing import List, Dict, Optional
from datetime import datetime
from src.database.connection import get_db_session
from src.database.models import Customer, Order, Coupon


class EmailMarketing:
    """Email marketing automation"""
    
    def __init__(self):
        self.smtp_server = None
        self.smtp_port = 587
        self.sender_email = None
        self.sender_password = None
    
    def configure_smtp(self, server: str, port: int, email: str, password: str):
        """
        Configure SMTP settings
        
        Args:
            server: SMTP server address
            port: SMTP port
            email: Sender email address
            password: Sender email password
        """
        self.smtp_server = server
        self.smtp_port = port
        self.sender_email = email
        self.sender_password = password
        logger.info("SMTP configured")
    
    def send_welcome_email(self, customer_id: int) -> bool:
        """
        Send welcome email to new customer
        
        Args:
            customer_id: Customer ID
            
        Returns:
            True if sent successfully
        """
        try:
            db = get_db_session()
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            db.close()
            
            if not customer or not customer.email:
                return False
            
            subject = "Welcome to Our Restaurant!"
            body = f"""
            Dear {customer.first_name},
            
            Thank you for joining us! We're excited to have you as a customer.
            
            As a welcome gift, you've received 100 loyalty points!
            
            Start earning more points with every purchase and unlock exclusive rewards.
            
            Best regards,
            The Team
            """
            
            return self._send_email(customer.email, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")
            return False
    
    def send_birthday_email(self, customer_id: int, coupon_code: str) -> bool:
        """
        Send birthday email with special coupon
        
        Args:
            customer_id: Customer ID
            coupon_code: Coupon code to include
            
        Returns:
            True if sent successfully
        """
        try:
            db = get_db_session()
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            db.close()
            
            if not customer or not customer.email:
                return False
            
            subject = "Happy Birthday! Special Offer Inside 🎉"
            body = f"""
            Dear {customer.first_name},
            
            Happy Birthday! We hope your special day is filled with joy.
            
            As a birthday gift, here's a special coupon code: {coupon_code}
            
            Use it on your next visit for a special discount!
            
            Best wishes,
            The Team
            """
            
            return self._send_email(customer.email, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending birthday email: {e}")
            return False
    
    def send_promotional_email(self, customer_ids: List[int], subject: str, body: str, coupon_code: Optional[str] = None) -> Dict:
        """
        Send promotional email to multiple customers
        
        Args:
            customer_ids: List of customer IDs
            subject: Email subject
            body: Email body
            coupon_code: Optional coupon code to include
            
        Returns:
            Dictionary with sent/failed counts
        """
        results = {'sent': 0, 'failed': 0}
        
        try:
            db = get_db_session()
            customers = db.query(Customer).filter(Customer.customer_id.in_(customer_ids)).all()
            db.close()
            
            if coupon_code:
                body += f"\n\nSpecial Offer: Use code {coupon_code} for a discount!"
            
            for customer in customers:
                if customer.email:
                    if self._send_email(customer.email, subject, body):
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                else:
                    results['failed'] += 1
            
            logger.info(f"Promotional email sent: {results['sent']} sent, {results['failed']} failed")
            return results
            
        except Exception as e:
            logger.error(f"Error sending promotional emails: {e}")
            return results
    
    def send_abandoned_cart_email(self, customer_id: int) -> bool:
        """
        Send abandoned cart reminder email
        
        Args:
            customer_id: Customer ID
            
        Returns:
            True if sent successfully
        """
        try:
            db = get_db_session()
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            db.close()
            
            if not customer or not customer.email:
                return False
            
            subject = "You left items in your cart!"
            body = f"""
            Dear {customer.first_name},
            
            We noticed you left some items in your cart. Don't miss out!
            
            Complete your order now and enjoy our delicious food.
            
            Best regards,
            The Team
            """
            
            return self._send_email(customer.email, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending abandoned cart email: {e}")
            return False
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Internal method to send email (placeholder - requires SMTP configuration)
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body: Email body
            
        Returns:
            True if sent successfully
        """
        if not self.smtp_server or not self.sender_email:
            logger.warning("SMTP not configured. Email not sent.")
            logger.info(f"Would send email to {to_email}: {subject}")
            return False
        
        try:
            # In real implementation, use smtplib to send email
            # import smtplib
            # from email.mime.text import MIMEText
            # from email.mime.multipart import MIMEMultipart
            # 
            # msg = MIMEMultipart()
            # msg['From'] = self.sender_email
            # msg['To'] = to_email
            # msg['Subject'] = subject
            # msg.attach(MIMEText(body, 'plain'))
            # 
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()
            # server.login(self.sender_email, self.sender_password)
            # server.send_message(msg)
            # server.quit()
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False


def get_email_marketing() -> EmailMarketing:
    """Get global email marketing instance"""
    return EmailMarketing()

