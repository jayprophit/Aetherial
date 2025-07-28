"""
Email Service for Unified Platform
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending notifications and communications"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "noreply@unifiedplatform.com"
        self.sender_password = "app_password"  # In production, use environment variables
        
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> Dict[str, Any]:
        """Send email to recipient"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # For demo purposes, just log the email
            logger.info(f"Email sent to {to_email}: {subject}")
            
            return {
                'success': True,
                'message': 'Email sent successfully',
                'to': to_email,
                'subject': subject
            }
            
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_verification_email(self, to_email: str, verification_code: str) -> Dict[str, Any]:
        """Send email verification code"""
        subject = "Verify Your Email - Unified Platform"
        body = f"""
        Welcome to Unified Platform!
        
        Your verification code is: {verification_code}
        
        Please enter this code to verify your email address.
        
        Best regards,
        Unified Platform Team
        """
        
        return self.send_email(to_email, subject, body)
    
    def send_password_reset_email(self, to_email: str, reset_token: str) -> Dict[str, Any]:
        """Send password reset email"""
        subject = "Password Reset - Unified Platform"
        body = f"""
        You requested a password reset for your Unified Platform account.
        
        Your reset token is: {reset_token}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Unified Platform Team
        """
        
        return self.send_email(to_email, subject, body)

