"""
Settings View - Application settings and configuration

Documentation:
- docs/INDEX.md
- docs/erp/uiux-roadmap.md
- docs/erp/uiux-audit-baseline.md
- docs/erp/uiux-phase1-shell-refresh.md
- docs/erp/worklog.md
"""

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from loguru import logger

from src.config.settings import get_settings
from src.gui.audit_trail_view import AuditTrailView
from src.gui.cloud_sync_view import CloudSyncView
from src.gui.design_system import (
    GROUP_BOX_STYLE,
    INPUT_STYLE,
    PRIMARY_BUTTON_STYLE,
    TAB_WIDGET_STYLE,
    apply_muted_text,
    apply_page_title,
)
from src.gui.location_management import LocationManagementView
from src.gui.notification_preferences_widget import NotificationPreferencesWidget
from src.gui.permissions_management import PermissionsManagementView


class SettingsView(QWidget):
    """Settings View."""

    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup settings UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 28, 28, 28)

        title = QLabel("Settings")
        apply_page_title(title)
        layout.addWidget(title)

        subtitle = QLabel(
            "Configure database connection, updates, permissions, locations, and integrations."
        )
        subtitle.setWordWrap(True)
        apply_muted_text(subtitle, size=13)
        layout.addWidget(subtitle)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(TAB_WIDGET_STYLE)

        self.tabs.addTab(self.create_settings_widget(), "General")
        self.tabs.addTab(AuditTrailView(self.user_id), "Audit Trail")
        self.tabs.addTab(LocationManagementView(self.user_id), "Locations")
        self.tabs.addTab(PermissionsManagementView(self.user_id), "Permissions")
        self.tabs.addTab(CloudSyncView(self.user_id), "Cloud Sync")
        self.tabs.addTab(NotificationPreferencesWidget(self.user_id), "Notifications")

        from src.gui.integrations_view import IntegrationsView

        self.tabs.addTab(IntegrationsView(self.user_id), "Integrations")
        layout.addWidget(self.tabs)

    def create_settings_widget(self) -> QWidget:
        """Create base settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        db_group = QGroupBox("Database")
        db_group.setStyleSheet(GROUP_BOX_STYLE)
        db_layout = QFormLayout(db_group)
        db_layout.setSpacing(10)

        self.db_host_input = QLineEdit()
        self.db_host_input.setPlaceholderText("postgresql://host/db or cloud URL")
        self.db_host_input.setStyleSheet(INPUT_STYLE)
        db_layout.addRow("Cloud DB URL:", self.db_host_input)

        self.db_port_input = QLineEdit()
        self.db_port_input.setPlaceholderText("5432")
        self.db_port_input.setStyleSheet(INPUT_STYLE)
        db_layout.addRow("Port:", self.db_port_input)

        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("postgresql")
        self.db_name_input.setStyleSheet(INPUT_STYLE)
        db_layout.addRow("Provider:", self.db_name_input)
        layout.addWidget(db_group)

        update_group = QGroupBox("Updates")
        update_group.setStyleSheet(GROUP_BOX_STYLE)
        update_layout = QFormLayout(update_group)
        update_layout.setSpacing(10)

        self.github_repo_input = QLineEdit()
        self.github_repo_input.setPlaceholderText("owner/repository")
        self.github_repo_input.setStyleSheet(INPUT_STYLE)
        update_layout.addRow("Repository:", self.github_repo_input)

        self.auto_check_combo = QComboBox()
        self.auto_check_combo.addItem("Enabled", True)
        self.auto_check_combo.addItem("Disabled", False)
        self.auto_check_combo.setStyleSheet(INPUT_STYLE)
        update_layout.addRow("Check on startup:", self.auto_check_combo)
        layout.addWidget(update_group)

        button_row = QHBoxLayout()
        button_row.addStretch()

        save_button = QPushButton("Save Settings")
        save_button.setStyleSheet(PRIMARY_BUTTON_STYLE)
        save_button.clicked.connect(self.handle_save)
        button_row.addWidget(save_button)
        layout.addLayout(button_row)
        layout.addStretch()

        return widget

    def load_settings(self):
        """Load settings from config."""
        try:
            settings = get_settings()
            self.db_host_input.setText(settings.get("Database", "cloud_db_url", ""))
            self.db_port_input.setText(str(settings.get_int("Database", "port", 5432)))
            self.db_name_input.setText(settings.get("Database", "cloud_db_type", ""))

            repo_owner = settings.get("Updates", "github_repo_owner", "")
            repo_name = settings.get("Updates", "github_repo_name", "")
            self.github_repo_input.setText(
                f"{repo_owner}/{repo_name}" if repo_owner and repo_name else ""
            )

            auto_check = settings.get_bool("Updates", "check_on_startup", True)
            self.auto_check_combo.setCurrentIndex(0 if auto_check else 1)
        except Exception as exc:
            logger.error(f"Error loading settings: {exc}")

    def handle_save(self):
        """Handle save settings button click."""
        try:
            settings = get_settings()

            settings.set("Database", "cloud_db_url", self.db_host_input.text().strip())
            try:
                port = int(self.db_port_input.text().strip() or "5432")
                settings.set("Database", "port", str(port))
            except ValueError:
                logger.warning("Invalid port value, keeping existing port")
            settings.set("Database", "cloud_db_type", self.db_name_input.text().strip())

            repo_text = self.github_repo_input.text().strip()
            if "/" in repo_text:
                owner, name = repo_text.split("/", 1)
                settings.set("Updates", "github_repo_owner", owner)
                settings.set("Updates", "github_repo_name", name)
            else:
                settings.set("Updates", "github_repo_owner", "")
                settings.set("Updates", "github_repo_name", "")

            auto_check = bool(self.auto_check_combo.currentData())
            settings.set("Updates", "check_on_startup", str(auto_check).lower())
            settings.save()

            QMessageBox.information(self, "Success", "Settings saved successfully.")
            logger.info("Settings saved")
        except Exception as exc:
            logger.error(f"Error saving settings: {exc}")
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{exc}")
