"""
Settings View - Application settings and configuration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QGroupBox, QMessageBox, QTabWidget
)
from loguru import logger
from src.config.settings import get_settings
from src.gui.audit_trail_view import AuditTrailView
from src.gui.location_management import LocationManagementView
from src.gui.permissions_management import PermissionsManagementView
from src.gui.cloud_sync_view import CloudSyncView
from src.gui.notification_preferences_widget import NotificationPreferencesWidget


class SettingsView(QWidget):
    """Settings View"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup settings UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Settings")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addSpacing(24)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F3F4F6;
                color: #374151;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2563EB;
                font-weight: 600;
            }
        """)
        
        # Settings tab
        settings_widget = self.create_settings_widget()
        self.tabs.addTab(settings_widget, "Settings")
        
        # Audit Trail tab
        audit_view = AuditTrailView(self.user_id)
        self.tabs.addTab(audit_view, "Audit Trail")
        
        # Location Management tab
        location_view = LocationManagementView(self.user_id)
        self.tabs.addTab(location_view, "Locations")
        
        # Permissions Management tab
        permissions_view = PermissionsManagementView(self.user_id)
        self.tabs.addTab(permissions_view, "Permissions")
        
        # Cloud Sync tab
        cloud_sync_view = CloudSyncView(self.user_id)
        self.tabs.addTab(cloud_sync_view, "Cloud Sync")
        
        notification_prefs = NotificationPreferencesWidget(self.user_id)
        self.tabs.addTab(notification_prefs, "Notifications")
        
        # Integrations tab
        from src.gui.integrations_view import IntegrationsView
        integrations_view = IntegrationsView(self.user_id)
        self.tabs.addTab(integrations_view, "Integrations")
        
        # 2FA Setup tab (only for admin roles)
        from src.gui.two_factor_setup import TwoFactorSetupDialog
        # Note: 2FA setup is accessed via a button, not a tab
        
        layout.addWidget(self.tabs)
    
    def create_settings_widget(self) -> QWidget:
        """Create settings widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Settings groups
        # Database Settings
        db_group = QGroupBox("Database Settings")
        db_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: 600;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        db_layout = QFormLayout(db_group)
        db_layout.setSpacing(12)
        
        self.db_host_input = QLineEdit()
        self.db_host_input.setPlaceholderText("localhost")
        db_layout.addRow("Host:", self.db_host_input)
        
        self.db_port_input = QLineEdit()
        self.db_port_input.setPlaceholderText("5432")
        db_layout.addRow("Port:", self.db_port_input)
        
        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("database_name")
        db_layout.addRow("Database Name:", self.db_name_input)
        
        layout.addWidget(db_group)
        layout.addSpacing(16)
        
        # Update Settings
        update_group = QGroupBox("Update Settings")
        update_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: 600;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        update_layout = QFormLayout(update_group)
        update_layout.setSpacing(12)
        
        self.github_repo_input = QLineEdit()
        self.github_repo_input.setPlaceholderText("username/repository")
        update_layout.addRow("GitHub Repository:", self.github_repo_input)
        
        self.auto_check_input = QLineEdit()
        self.auto_check_input.setPlaceholderText("true/false")
        update_layout.addRow("Auto Check Updates:", self.auto_check_input)
        
        layout.addWidget(update_group)
        layout.addSpacing(24)
        
        # Save button
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        save_btn.clicked.connect(self.handle_save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        return widget
    
    def load_settings(self):
        """Load settings from config"""
        try:
            settings = get_settings()
            
            # Database settings
            self.db_host_input.setText(settings.get('Database', 'cloud_db_url', ''))
            self.db_port_input.setText(str(settings.get_int('Database', 'port', 5432)))
            self.db_name_input.setText(settings.get('Database', 'cloud_db_type', ''))
            
            # Update settings
            repo_owner = settings.get('Updates', 'github_repo_owner', '')
            repo_name = settings.get('Updates', 'github_repo_name', '')
            if repo_owner and repo_name:
                self.github_repo_input.setText(f"{repo_owner}/{repo_name}")
            else:
                self.github_repo_input.setText('')
            self.auto_check_input.setText(str(settings.get_bool('Updates', 'check_on_startup', True)))
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def handle_save(self):
        """Handle save settings button click"""
        try:
            settings = get_settings()
            
            # Update database settings
            settings.set('Database', 'cloud_db_url', self.db_host_input.text().strip())
            try:
                port = int(self.db_port_input.text().strip() or '5432')
                settings.set('Database', 'port', str(port))
            except ValueError:
                pass
            settings.set('Database', 'cloud_db_type', self.db_name_input.text().strip())
            
            # Update update settings
            repo_text = self.github_repo_input.text().strip()
            if '/' in repo_text:
                parts = repo_text.split('/', 1)
                settings.set('Updates', 'github_repo_owner', parts[0])
                if len(parts) > 1:
                    settings.set('Updates', 'github_repo_name', parts[1])
            else:
                settings.set('Updates', 'github_repo_owner', '')
                settings.set('Updates', 'github_repo_name', '')
            
            auto_check = self.auto_check_input.text().strip().lower() == 'true'
            settings.set('Updates', 'check_on_startup', str(auto_check).lower())
            
            settings.save()
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            logger.info("Settings saved")
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{str(e)}")

