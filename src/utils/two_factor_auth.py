"""
Two-Factor Authentication (2FA) - TOTP-based 2FA for admin roles
"""

try:
    import pyotp
    import qrcode
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    pyotp = None
    qrcode = None

from io import BytesIO
from loguru import logger
from typing import Optional, Tuple
from src.database.connection import get_db_session
from src.database.models import Staff


class TwoFactorAuth:
    """Two-Factor Authentication manager"""
    
    def __init__(self):
        self.issuer_name = "Sphincs ERP"
    
    def generate_secret(self, username: str) -> str:
        """
        Generate a secret key for a user
        
        Args:
            username: Username of the user
            
        Returns:
            Secret key string
        """
        if not PYOTP_AVAILABLE:
            raise ImportError("pyotp is not installed. Install it with: pip install pyotp qrcode[pil]")
        return pyotp.random_base32()
    
    def get_provisioning_uri(self, username: str, secret: str) -> str:
        """
        Get provisioning URI for QR code generation
        
        Args:
            username: Username
            secret: Secret key
            
        Returns:
            Provisioning URI
        """
        if not PYOTP_AVAILABLE:
            raise ImportError("pyotp is not installed. Install it with: pip install pyotp qrcode[pil]")
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=self.issuer_name
        )
    
    def generate_qr_code(self, uri: str) -> BytesIO:
        """
        Generate QR code image from URI
        
        Args:
            uri: Provisioning URI
            
        Returns:
            BytesIO object containing PNG image
        """
        if not PYOTP_AVAILABLE:
            raise ImportError("qrcode is not installed. Install it with: pip install pyotp qrcode[pil]")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes
    
    def verify_token(self, secret: str, token: str) -> bool:
        """
        Verify a TOTP token
        
        Args:
            secret: User's secret key
            token: Token to verify
            
        Returns:
            True if token is valid, False otherwise
        """
        if not PYOTP_AVAILABLE:
            raise ImportError("pyotp is not installed. Install it with: pip install pyotp qrcode[pil]")
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)  # Allow 1 time step tolerance
        except Exception as e:
            logger.error(f"Error verifying 2FA token: {e}")
            return False
    
    def get_current_token(self, secret: str) -> str:
        """
        Get current TOTP token (for testing)
        
        Args:
            secret: User's secret key
            
        Returns:
            Current token
        """
        if not PYOTP_AVAILABLE:
            raise ImportError("pyotp is not installed. Install it with: pip install pyotp qrcode[pil]")
        totp = pyotp.TOTP(secret)
        return totp.now()


def get_2fa_manager() -> TwoFactorAuth:
    """Get global 2FA manager instance"""
    return TwoFactorAuth()

