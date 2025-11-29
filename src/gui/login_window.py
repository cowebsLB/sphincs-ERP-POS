"""
Login window for authentication
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
from typing import Optional
from loguru import logger
from src.utils.auth import authenticate_user
from src.database.models import Staff
from src.config.settings import get_settings
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False
    logger.warning("keyring not available, passwords will be stored in config (less secure)")


class LoginWindow(QDialog):
    """Login dialog window"""
    
    # Signal emitted when login is successful (emits user object with attributes)
    login_successful = pyqtSignal(object)  # Changed from User to object to avoid SQLAlchemy issues
    
    def __init__(self, app_name: str = "Sphincs", parent=None):
        """
        Initialize login window
        
        Args:
            app_name: Application name (ERP or POS)
            parent: Parent widget
        """
        super().__init__(parent)
        self.app_name = app_name
        self.settings = get_settings()
        self.setup_ui()
        self.setup_connections()
        self.load_saved_credentials()
        
        # Focus on username field (or password if username is pre-filled)
        if self.username_input.text():
            QTimer.singleShot(100, self.password_input.setFocus)
        else:
            QTimer.singleShot(100, self.username_input.setFocus)
    
    def setup_ui(self):
        """Setup login window UI"""
        self.setWindowTitle(f"{self.app_name} - Login")
        # Container: 400px width (within 360-440px range), auto height (min 350px)
        self.setFixedWidth(400)
        self.setMinimumHeight(350)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)  # We'll control spacing manually
        layout.setContentsMargins(40, 40, 40, 40)
        
        # App name/title
        title_label = QLabel(self.app_name)
        title_font = QFont("Segoe UI", 24, QFont.Weight.DemiBold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2563EB; margin-bottom: 8px;")
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Sign in to continue")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #6B7280; margin-bottom: 28px;")
        layout.addWidget(subtitle_label)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(36)  # 36px height
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                font-size: 16px;
                background-color: white;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
                outline: none;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Spacing: 20px between username and password
        layout.addSpacing(20)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(36)  # 36px height
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                font-size: 16px;
                background-color: white;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
                outline: none;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Remember me checkbox - 16px spacing from password field
        layout.addSpacing(16)
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("color: #374151; font-size: 14px;")
        layout.addWidget(self.remember_checkbox)
        
        # Status label (for error messages)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #EF4444; font-size: 12px; min-height: 20px; margin-top: 8px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Spacing: 24px before login button
        layout.addSpacing(24)
        
        # Login button - full width, 44px height
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(44)  # 44px, slightly larger than inputs
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding-top: 16px;
                padding-bottom: 16px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: 600;
                min-height: 44px;
            }
            QPushButton:hover {
                background-color: #3B82F6;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
            QPushButton:disabled {
                background-color: #E5E7EB;
                color: #9CA3AF;
            }
        """)
        layout.addWidget(self.login_button)
        
        # Online/Offline status - 24px spacing from button to prevent overlap
        layout.addSpacing(24)
        self.status_indicator = QLabel("● Online")
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_indicator.setStyleSheet("color: #10B981; font-size: 12px; margin-top: 4px;")
        layout.addWidget(self.status_indicator)
        
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click"""
        # Strip whitespace from username to prevent accidental spaces
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Clear previous error
        self.status_label.setText("")
        
        # Validate inputs
        if not username:
            self.show_error("Please enter your username")
            self.username_input.setFocus()
            return
        
        if not password:
            self.show_error("Please enter your password")
            self.password_input.setFocus()
            return
        
        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        
        # Authenticate user
        user_data = authenticate_user(username, password)
        
        if user_data:
            logger.info(f"Login successful for user: {username}")
            # Save or clear credentials based on "Remember me" checkbox
            self.save_credentials(username, password)
            # Create a simple object to hold user data
            from types import SimpleNamespace
            user_obj = SimpleNamespace(**user_data)
            self.login_successful.emit(user_obj)
            self.accept()
        else:
            self.show_error("Invalid username or password")
            self.password_input.clear()
            self.password_input.setFocus()
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
    
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #EF4444; font-size: 12px; min-height: 20px;")
    
    def load_saved_credentials(self):
        """Load saved credentials if "Remember me" was checked previously"""
        try:
            # Check if remember me was enabled
            remember_me = self.settings.get_bool('Login', 'remember_me', False)
            if not remember_me:
                return
            
            # Load username
            saved_username = self.settings.get('Login', 'username', '')
            if saved_username:
                self.username_input.setText(saved_username)
                self.remember_checkbox.setChecked(True)
            
            # Load password (securely)
            saved_password = self._get_saved_password(saved_username)
            if saved_password:
                self.password_input.setText(saved_password)
                
        except Exception as e:
            logger.error(f"Error loading saved credentials: {e}")
    
    def save_credentials(self, username: str, password: str):
        """Save or clear credentials based on 'Remember me' checkbox"""
        try:
            if self.remember_checkbox.isChecked():
                # Save credentials
                self.settings.set('Login', 'remember_me', 'true')
                self.settings.set('Login', 'username', username)
                self._save_password(username, password)
                logger.info(f"Credentials saved for user: {username}")
            else:
                # Clear saved credentials
                self.settings.set('Login', 'remember_me', 'false')
                self.settings.set('Login', 'username', '')
                self._clear_saved_password(username)
                logger.info("Saved credentials cleared")
        except Exception as e:
            logger.error(f"Error saving credentials: {e}")
    
    def _save_password(self, username: str, password: str):
        """Save password securely"""
        if KEYRING_AVAILABLE:
            try:
                keyring.set_password(f"{self.app_name}_Login", username, password)
            except Exception as e:
                logger.error(f"Error saving password to keyring: {e}")
                # Fallback to config (less secure)
                self.settings.set('Login', 'password', password)
        else:
            # Fallback: store in config (less secure, but better than nothing)
            logger.warning("Using config file for password storage (keyring not available)")
            self.settings.set('Login', 'password', password)
    
    def _get_saved_password(self, username: str) -> str:
        """Get saved password securely"""
        if KEYRING_AVAILABLE:
            try:
                password = keyring.get_password(f"{self.app_name}_Login", username)
                return password or ""
            except Exception as e:
                logger.error(f"Error getting password from keyring: {e}")
                # Fallback to config
                return self.settings.get('Login', 'password', '')
        else:
            # Fallback: get from config
            return self.settings.get('Login', 'password', '')
    
    def _clear_saved_password(self, username: str):
        """Clear saved password"""
        if KEYRING_AVAILABLE:
            try:
                keyring.delete_password(f"{self.app_name}_Login", username)
            except Exception as e:
                logger.error(f"Error clearing password from keyring: {e}")
        
        # Also clear from config if it exists
        try:
            self.settings.set('Login', 'password', '')
        except:
            pass
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

