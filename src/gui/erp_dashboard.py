"""
ERP Dashboard - Main interface for Sphincs ERP
"""

from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QGridLayout, QListWidget, QListWidgetItem,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QIcon
from pathlib import Path
from loguru import logger
from typing import Optional
from src.gui.sidebar import Sidebar
from src.gui.notification_tray import NotificationTrayManager
from src.utils.notification_center import NotificationCenter
from src.utils.notification_worker import NotificationWorker
from src.utils.notification_preferences import (
    get_notification_preferences,
    filter_notifications_for_user,
    should_display_notification,
    snooze_channels,
    clear_snooze,
)


class SummaryCard(QFrame):
    """Summary card widget for dashboard metrics"""
    
    def __init__(self, title: str, value: str, icon: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.value_label = None
        self.setup_ui(title, value, icon)
    
    def setup_ui(self, title: str, value: str, icon: Optional[str]):
        """Setup card UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            font-weight: 500;
        """)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("""
            color: #111827;
            font-size: 32px;
            font-weight: 700;
        """)
        layout.addWidget(self.value_label)
        
        layout.addStretch()
    
    def set_value(self, value: str):
        """Update the value displayed in the card"""
        if self.value_label:
            self.value_label.setText(value)


class QuickActionButton(QPushButton):
    """Quick action button for dashboard"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(44)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                min-height: 44px;
            }
            QPushButton:hover {
                background-color: #3B82F6;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)


class ERPDashboard(QMainWindow):
    """Main ERP Dashboard window"""
    
    # Signals
    navigate_to = pyqtSignal(str)  # Emits section name when navigation clicked
    logout_requested = pyqtSignal()  # Emits when user requests logout
    
    def __init__(self, username: str, role: str, user_id: int, parent=None):
        super().__init__(parent)
        self.username = username
        self.role = role
        self.user_id = user_id
        self.current_view = "Dashboard"
        self.inventory_alert_count = 0
        self.notification_list: Optional[QListWidget] = None
        self.notification_section_widget: Optional[QWidget] = None
        self.notification_tray: Optional[NotificationTrayManager] = None
        self.notification_worker: Optional[NotificationWorker] = None
        self.notification_center = NotificationCenter.instance()
        self.notification_preferences = {}
        
        self.setWindowTitle(f"Sphincs ERP - Dashboard")
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent.parent / "sphincs_icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self.setup_ui()
        self.setup_notifications()
        self.load_dashboard_data()
        
        # Maximize window on startup
        self.showMaximized()
        
        logger.info(f"ERP Dashboard initialized for user: {username} ({role})")
    
    def setup_ui(self):
        """Setup dashboard UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar navigation
        self.sidebar = Sidebar()
        self.sidebar.navigation_clicked.connect(self.handle_navigation)
        self.sidebar.logout_requested.connect(self.handle_logout)
        self.sidebar.set_user_info(self.username, self.role)
        main_layout.addWidget(self.sidebar)
        
        # Content area (scrollable) - stored as instance variable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #0F172A;
                border: none;
            }
        """)
        
        # Initial dashboard content
        self.show_dashboard_view()
        
        main_layout.addWidget(self.scroll_area)
    
    def refresh_notification_preferences(self):
        """Load latest notification preferences for the user."""
        try:
            self.notification_preferences = get_notification_preferences(self.user_id)
        except Exception as exc:
            logger.error(f"Failed to load notification preferences: {exc}")
            self.notification_preferences = {}
    
    def setup_notifications(self):
        """Initialize notification services, tray, and worker."""
        self.notification_center.notification_created.connect(self.handle_notification_created)
        self.notification_center.notification_updated.connect(self.refresh_notification_list)
        self.refresh_notification_preferences()
        
        if QSystemTrayIcon.isSystemTrayAvailable():
            icon = self.windowIcon()
            if icon.isNull():
                icon = QIcon()
            self.notification_tray = NotificationTrayManager(icon, self)
            self.notification_tray.open_requested.connect(self.restore_from_tray)
            self.notification_tray.view_notifications_requested.connect(self.show_notifications_from_tray)
            self.notification_tray.sync_requested.connect(self.handle_sync_data)
            self.notification_tray.exit_requested.connect(self.close)
            self.notification_tray.show()
            unread = self.notification_center.get_unread_count()
            self.notification_tray.set_unread_count(unread)
        else:
            logger.warning("System tray not available on this system.")
        
        try:
            self.notification_worker = NotificationWorker(parent=self)
            self.notification_worker.start()
        except Exception as exc:
            logger.error(f"Failed to start notification worker: {exc}")
    
    def create_navigation_bar(self) -> QFrame:
        """Create top navigation bar"""
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #E5E7EB;
                padding: 6px 16px 6px 16px;
            }
        """)
        nav_frame.setFixedHeight(56)
        
        layout = QHBoxLayout(nav_frame)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 4, 24, 4)
        
        # App name
        app_label = QLabel("Sphincs ERP")
        app_label.setStyleSheet("""
            color: #2563EB;
            font-size: 20px;
            font-weight: 700;
        """)
        layout.addWidget(app_label)
        
        layout.addSpacing(32)
        
        # Navigation buttons
        nav_items = ["Dashboard", "Products", "Inventory", "Suppliers", "Customers", "Staff", "Sales", "Reports", "Settings"]
        self.nav_buttons = {}
        
        for item in nav_items:
            btn = QPushButton(item)
            btn.setFlat(True)
            if item == "Dashboard":
                btn.setStyleSheet("""
                    QPushButton {
                        color: #2563EB;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        background-color: #DBEAFE;
                    }
                    QPushButton:hover {
                        background-color: #BFDBFE;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #374151;
                        font-size: 14px;
                        font-weight: 500;
                        padding: 8px 16px;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background-color: #F3F4F6;
                        color: #2563EB;
                    }
                """)
            btn.clicked.connect(lambda checked, name=item: self.handle_navigation(name))
            self.nav_buttons[item] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # User info
        user_label = QLabel(f"{self.username} ({self.role})")
        user_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            margin-bottom: 8px;
            margin-top: 8px;
        """)
        layout.addWidget(user_label)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                color: #EF4444;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 16px;
                border-radius: 6px;
                margin-top: 8px;
            }
            QPushButton:hover {
                background-color: #FEE2E2;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return nav_frame
    
    def create_welcome_section(self) -> QWidget:
        """Create welcome section"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        welcome_label = QLabel(f"Welcome back, {self.username}!")
        welcome_label.setStyleSheet("""
            color: #111827;
            font-size: 28px;
            font-weight: 700;
        """)
        layout.addWidget(welcome_label)
        
        date_label = QLabel(self.get_current_date())
        date_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
        """)
        layout.addWidget(date_label)
        
        return widget
    
    def create_summary_section(self) -> QWidget:
        """Create today's summary section"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Today's Summary")
        title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Summary cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)
        
        self.summary_cards = {
            'sales': SummaryCard("Sales", "$0.00"),
            'orders': SummaryCard("Orders", "0"),
            'staff': SummaryCard("Staff", "0/0"),
            'alerts': SummaryCard("Alerts", "0")
        }
        
        cards_layout.addWidget(self.summary_cards['sales'], 0, 0)
        cards_layout.addWidget(self.summary_cards['orders'], 0, 1)
        cards_layout.addWidget(self.summary_cards['staff'], 0, 2)
        cards_layout.addWidget(self.summary_cards['alerts'], 0, 3)
        
        layout.addLayout(cards_layout)
        
        return widget
    
    def create_quick_actions_section(self) -> QWidget:
        """Create quick actions section"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Quick Actions")
        title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        actions = [
            ("New Product", self.handle_new_product),
            ("Add Staff", self.handle_add_staff),
            ("View Reports", self.handle_view_reports),
            ("Sync Data", self.handle_sync_data)
        ]
        
        for action_text, handler in actions:
            btn = QuickActionButton(action_text)
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        return widget
    
    def create_notifications_section(self) -> QWidget:
        """Create notifications center section"""
        widget = QWidget()
        widget.setObjectName("notificationsSection")
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        title = QLabel("Alerts & Notifications")
        title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        snooze_btn = QPushButton("Snooze")
        snooze_btn.setFixedHeight(32)
        snooze_btn.setMenu(self.build_snooze_menu())
        header_layout.addWidget(snooze_btn)
        self.snooze_menu_button = snooze_btn
        
        mark_btn = QPushButton("Mark All Read")
        mark_btn.setFixedHeight(32)
        mark_btn.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                color: #111827;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
        """)
        mark_btn.clicked.connect(self.mark_all_notifications_read)
        header_layout.addWidget(mark_btn)
        
        layout.addLayout(header_layout)
        
        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.notification_list = QListWidget()
        self.notification_list.setObjectName("notificationList")
        self.notification_list.setStyleSheet("""
            QListWidget#notificationList {
                border: none;
                background-color: transparent;
            }
            QListWidget#notificationList::item {
                padding: 12px 16px;
                border-bottom: 1px solid #F3F4F6;
            }
        """)
        self.notification_list.setWordWrap(True)
        container_layout.addWidget(self.notification_list)
        
        layout.addWidget(container)
        self.notification_section_widget = widget
        self.refresh_notification_list()
        
        return widget
    
    def build_snooze_menu(self) -> QMenu:
        menu = QMenu(self)
        for label, minutes in [("15 minutes", 15), ("30 minutes", 30), ("1 hour", 60), ("4 hours", 240)]:
            action = menu.addAction(f"Snooze {label}")
            action.triggered.connect(lambda _, m=minutes: self.snooze_notifications(m))
        menu.addSeparator()
        clear_action = menu.addAction("Clear snooze")
        clear_action.triggered.connect(self.clear_snooze_notifications)
        return menu
    
    def create_recent_activity_section(self) -> QWidget:
        """Create recent activity section"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Recent Activity")
        title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Activity list
        activity_frame = QFrame()
        activity_frame.setFrameShape(QFrame.Shape.StyledPanel)
        activity_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setSpacing(8)
        activity_layout.setContentsMargins(16, 16, 16, 16)
        
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidgetItem {
                padding: 8px 0;
                border-bottom: 1px solid #F3F4F6;
            }
            QListWidgetItem:last {
                border-bottom: none;
            }
        """)
        self.activity_list.setMaximumHeight(300)
        
        activity_layout.addWidget(self.activity_list)
        layout.addWidget(activity_frame)
        
        return widget
    
    def load_dashboard_data(self):
        """Load dashboard data from database"""
        logger.info("Loading dashboard data...")
        
        try:
            from src.utils.dashboard_analytics import (
                get_today_sales, get_today_orders,
                get_active_staff_count, get_inventory_alerts,
                get_recent_activities
            )
            
            # Load real data
            today_sales = get_today_sales()
            today_orders = get_today_orders()
            active_staff, total_staff = get_active_staff_count()
            alerts = get_inventory_alerts()
            self.inventory_alert_count = alerts
            
            # Update summary cards
            self.summary_cards['sales'].set_value(f"${today_sales:,.2f}")
            self.summary_cards['orders'].set_value(str(today_orders))
            self.summary_cards['staff'].set_value(f"{active_staff}/{total_staff}")
            self.update_alert_summary()
            
            # Load recent activities
            self.activity_list.clear()
            activities = get_recent_activities(limit=10)
            
            if activities:
                for activity in activities:
                    time_str = activity['time'].strftime("%H:%M")
                    message = f"[{time_str}] {activity['icon']} {activity['message']}"
                    item = QListWidgetItem(message)
                    item.setForeground(QColor("#6B7280"))
                    self.activity_list.addItem(item)
            else:
                item = QListWidgetItem("No recent activity")
                item.setForeground(QColor("#6B7280"))
                self.activity_list.addItem(item)
                
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            # Fallback to placeholder data
            self.summary_cards['sales'].set_value("$0.00")
            self.summary_cards['orders'].set_value("0")
            self.summary_cards['staff'].set_value("0/0")
            self.inventory_alert_count = 0
            self.update_alert_summary()
    
    def update_alert_summary(self):
        """Update alerts summary card and tray badge."""
        unread = self.notification_center.get_unread_count()
        total_alerts = (self.inventory_alert_count or 0) + unread
        if 'alerts' in self.summary_cards:
            self.summary_cards['alerts'].set_value(str(total_alerts))
        if self.notification_tray:
            self.notification_tray.set_unread_count(unread)
    
    def mark_all_notifications_read(self):
        """Mark all notifications as read."""
        updated = self.notification_center.mark_all_as_read()
        if updated:
            logger.info("Marked %s notifications as read", updated)
        self.refresh_notification_list()
    
    def snooze_notifications(self, minutes: int):
        """Snooze all channels for the given minutes."""
        try:
            snooze_channels(self.user_id, minutes)
            logger.info("Snoozed alerts for %s minutes", minutes)
        except Exception as exc:
            logger.error(f"Failed to snooze alerts: {exc}")
        finally:
            self.refresh_notification_preferences()
            self.refresh_notification_list()
    
    def clear_snooze_notifications(self):
        """Clear snooze for all channels."""
        try:
            clear_snooze(self.user_id)
            logger.info("Cleared notification snooze")
        except Exception as exc:
            logger.error(f"Failed to clear snooze: {exc}")
        finally:
            self.refresh_notification_preferences()
            self.refresh_notification_list()
    
    def refresh_notification_list(self, *_):
        """Refresh notification list widget."""
        records = self.notification_center.get_recent_notifications(limit=15)
        filtered = filter_notifications_for_user(
            records,
            self.user_id,
            target="desktop",
            preferences=self.notification_preferences,
        )
        if self.notification_list:
            self.notification_list.clear()
            for data in filtered:
                self._add_notification_item(data, append_bottom=True)
        self.update_alert_summary()
    
    def handle_notification_created(self, data: dict):
        """Handle new notification events."""
        logger.debug(f"Notification received: {data}")
        if not should_display_notification(
            data,
            staff_id=self.user_id,
            target="desktop",
            preferences=self.notification_preferences,
        ):
            return
        if self.notification_list:
            self._add_notification_item(data, append_bottom=False)
        if self.notification_tray:
            self.notification_tray.show_notification(
                data.get("title", "Notification"),
                data.get("message", ""),
                data.get("severity", "info"),
            )
        self.update_alert_summary()
    
    def _add_notification_item(self, data: dict, append_bottom: bool = False):
        """Utility to render notification list items."""
        if not self.notification_list:
            return
        
        text = self._format_notification_text(data)
        item = QListWidgetItem(text)
        severity = data.get("severity", "info")
        color = {
            "critical": "#DC2626",
            "warning": "#B45309",
            "info": "#1E3A8A",
        }.get(severity, "#1E3A8A")
        item.setForeground(QColor(color))
        item.setData(Qt.ItemDataRole.UserRole, data)
        
        if append_bottom:
            self.notification_list.addItem(item)
        else:
            self.notification_list.insertItem(0, item)
            self.notification_list.scrollToTop()
        
        # Keep list length reasonable
        max_items = 20
        while self.notification_list.count() > max_items:
            self.notification_list.takeItem(self.notification_list.count() - 1)
    
    def _format_notification_text(self, data: dict) -> str:
        timestamp = self._parse_timestamp(data.get("triggered_at"))
        timestamp_str = timestamp.strftime("%b %d %H:%M") if timestamp else ""
        title = data.get("title", "Alert")
        message = data.get("message", "")
        if timestamp_str:
            return f"[{timestamp_str}] {title} — {message}"
        return f"{title} — {message}"
    
    @staticmethod
    def _parse_timestamp(value) -> Optional[datetime]:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return None
    
    def restore_from_tray(self):
        """Restore window when tray icon activated."""
        if self.isMinimized():
            self.showNormal()
        self.raise_()
        self.activateWindow()
    
    def show_notifications_from_tray(self):
        """Navigate to dashboard and focus notifications section."""
        self.handle_navigation("Dashboard")
        QTimer.singleShot(400, self.scroll_to_notifications)
    
    def scroll_to_notifications(self):
        """Scroll dashboard to notifications area."""
        if self.notification_section_widget:
            self.scroll_area.ensureWidgetVisible(self.notification_section_widget, 0, 0)
    
    def closeEvent(self, event):
        """Stop background worker and hide tray."""
        if self.notification_worker:
            self.notification_worker.stop()
            self.notification_worker.wait(2000)
            self.notification_worker = None
        if self.notification_tray:
            self.notification_tray.hide()
        super().closeEvent(event)
    
    def get_current_date(self) -> str:
        """Get formatted current date"""
        from datetime import datetime
        return datetime.now().strftime("%A, %B %d, %Y")
    
    def handle_navigation(self, section: str):
        """Handle navigation button clicks"""
        logger.info(f"Navigation to: {section}")
        self.navigate_to.emit(section)
        self.current_view = section
        
        # Sidebar handles its own button states, no need to update styles here
        
        # Switch view based on section
        if section == "Dashboard":
            self.show_dashboard_view()
        elif section == "Products":
            self.show_products_view()
        elif section == "Inventory":
            self.show_inventory_view()
        elif section == "Suppliers":
            self.show_suppliers_view()
        elif section == "Customers":
            self.show_customers_view()
        elif section == "Staff":
            self.show_staff_view()
        elif section == "Attendance":
            self.show_attendance_view()
        elif section == "Shift Scheduling":
            self.show_shift_view()
        elif section == "Payroll":
            self.show_payroll_view()
        elif section == "Performance":
            self.show_performance_view()
        elif section == "Sales":
            self.show_sales_view()
        elif section == "Financial":
            self.show_financial_view()
        elif section == "Reports":
            self.show_reports_view()
        elif section == "Operations":
            self.show_operations_view()
        elif section == "Retail & E-Commerce":
            self.show_retail_ecommerce_view()
        elif section == "Healthcare":
            self.show_healthcare_view()
        elif section == "Education":
            self.show_education_view()
        elif section == "Manufacturing":
            self.show_manufacturing_view()
        elif section == "Logistics":
            self.show_logistics_view()
        elif section == "Mobile":
            self.show_mobile_view()
        elif section == "Settings":
            self.show_settings_view()
        else:
            # Other sections - show placeholder
            self.show_placeholder_view(section)
    
    def show_dashboard_view(self):
        """Show dashboard view"""
        self.refresh_notification_preferences()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(32, 32, 32, 32)
        
        # Welcome section
        welcome_section = self.create_welcome_section()
        content_layout.addWidget(welcome_section)
        
        # Today's Summary
        summary_section = self.create_summary_section()
        content_layout.addWidget(summary_section)
        
        # Quick Actions
        actions_section = self.create_quick_actions_section()
        content_layout.addWidget(actions_section)
        
        # Notifications section
        notifications_section = self.create_notifications_section()
        content_layout.addWidget(notifications_section)
        
        # Recent Activity
        activity_section = self.create_recent_activity_section()
        content_layout.addWidget(activity_section)
        
        content_layout.addStretch()
        
        self.scroll_area.setWidget(content_widget)
    
    def show_staff_view(self):
        """Show staff management view"""
        from src.gui.staff_management import StaffManagementView
        staff_view = StaffManagementView(self.user_id)
        self.scroll_area.setWidget(staff_view)
    
    def show_attendance_view(self):
        """Show attendance management"""
        from src.gui.attendance_management import AttendanceManagementView
        attendance_view = AttendanceManagementView(self.user_id)
        self.scroll_area.setWidget(attendance_view)
    
    def show_shift_view(self):
        """Show shift scheduling"""
        from src.gui.shift_scheduling import ShiftSchedulingView
        shift_view = ShiftSchedulingView(self.user_id)
        self.scroll_area.setWidget(shift_view)
    
    def show_payroll_view(self):
        """Show payroll management"""
        from src.gui.payroll_management import PayrollManagementView
        payroll_view = PayrollManagementView(self.user_id)
        self.scroll_area.setWidget(payroll_view)
    
    def show_performance_view(self):
        """Show staff performance reports"""
        from src.gui.staff_performance_reports import StaffPerformanceReportsView
        performance_view = StaffPerformanceReportsView(self.user_id)
        self.scroll_area.setWidget(performance_view)
    
    def show_products_view(self):
        """Show product management view"""
        from src.gui.product_management import ProductManagementView
        products_view = ProductManagementView(self.user_id)
        self.scroll_area.setWidget(products_view)
    
    def show_inventory_view(self):
        """Show inventory management view"""
        from src.gui.inventory_management import InventoryManagementView
        inventory_view = InventoryManagementView(self.user_id)
        self.scroll_area.setWidget(inventory_view)
    
    def show_suppliers_view(self):
        """Show supplier management view"""
        from src.gui.supplier_management import SupplierManagementView
        suppliers_view = SupplierManagementView(self.user_id)
        self.scroll_area.setWidget(suppliers_view)
    
    def show_customers_view(self):
        """Show customer management view"""
        from src.gui.customer_management import CustomerManagementView
        customers_view = CustomerManagementView(self.user_id)
        self.scroll_area.setWidget(customers_view)
    
    def show_sales_view(self):
        """Show sales management view"""
        from src.gui.sales_management import SalesManagementView
        sales_view = SalesManagementView(self.user_id)
        self.scroll_area.setWidget(sales_view)
    
    def show_financial_view(self):
        """Show financial management view"""
        from src.gui.financial_management import FinancialManagementView
        financial_view = FinancialManagementView(self.user_id)
        self.scroll_area.setWidget(financial_view)
    
    def show_operations_view(self):
        """Show advanced operations hub"""
        from src.gui.operations_hub import AdvancedOperationsView
        operations_view = AdvancedOperationsView(self.user_id)
        self.scroll_area.setWidget(operations_view)
    
    def show_retail_ecommerce_view(self):
        """Show retail & e-commerce view"""
        from src.gui.retail_ecommerce_view import RetailECommerceView
        retail_view = RetailECommerceView(self.user_id)
        self.scroll_area.setWidget(retail_view)
    
    def show_healthcare_view(self):
        """Show healthcare management view"""
        from src.gui.healthcare_view import HealthcareView
        healthcare_view = HealthcareView(self.user_id)
        self.scroll_area.setWidget(healthcare_view)
    
    def show_education_view(self):
        """Show education & training view"""
        from src.gui.education_view import EducationView
        education_view = EducationView(self.user_id)
        self.scroll_area.setWidget(education_view)
    
    def show_manufacturing_view(self):
        """Show manufacturing management view"""
        from src.gui.manufacturing_view import ManufacturingView
        manufacturing_view = ManufacturingView(self.user_id)
        self.scroll_area.setWidget(manufacturing_view)
    
    def show_logistics_view(self):
        """Show logistics & fleet management view"""
        from src.gui.logistics_view import LogisticsView
        logistics_view = LogisticsView(self.user_id)
        self.scroll_area.setWidget(logistics_view)
    
    def show_reports_view(self):
        """Show reports view (same as sales for now)"""
        from src.gui.sales_reports import SalesReportsView
        reports_view = SalesReportsView(self.user_id)
        self.scroll_area.setWidget(reports_view)
    
    def show_mobile_view(self):
        """Show mobile companion view"""
        from src.gui.mobile_view import MobileView
        mobile_view = MobileView(self.user_id)
        self.scroll_area.setWidget(mobile_view)
    
    def show_settings_view(self):
        """Show settings view"""
        from src.gui.settings_view import SettingsView
        settings_view = SettingsView(self.user_id)
        self.scroll_area.setWidget(settings_view)
    
    def show_placeholder_view(self, section: str):
        """Show placeholder view for unimplemented sections"""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(32, 32, 32, 32)
        
        label = QLabel(f"{section} - Coming Soon")
        label.setStyleSheet("""
            color: #6B7280;
            font-size: 18px;
            font-weight: 500;
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        self.scroll_area.setWidget(content_widget)
    
    def handle_logout(self):
        """Handle logout"""
        logger.info("Logout requested")
        self.logout_requested.emit()
        self.close()
    
    def handle_new_product(self):
        """Handle new product action"""
        logger.info("New product action")
        # Navigate to Products and trigger add dialog
        self.handle_navigation("Products")
        # Get the products view and trigger add
        QTimer.singleShot(200, self._trigger_add_product)
    
    def _trigger_add_product(self):
        """Trigger add product dialog after navigation"""
        try:
            # Find the products view in the scroll area
            widget = self.scroll_area.widget()
            if widget and hasattr(widget, 'handle_add_product'):
                widget.handle_add_product()
        except Exception as e:
            logger.error(f"Error triggering add product: {e}")
    
    def handle_add_staff(self):
        """Handle add staff action"""
        logger.info("Add staff action")
        # Navigate to Staff and trigger add dialog
        self.handle_navigation("Staff")
        # Get the staff view and trigger add
        QTimer.singleShot(200, self._trigger_add_staff)
    
    def _trigger_add_staff(self):
        """Trigger add staff dialog after navigation"""
        try:
            # Find the staff view in the scroll area
            widget = self.scroll_area.widget()
            if widget and hasattr(widget, 'handle_add_staff'):
                widget.handle_add_staff()
        except Exception as e:
            logger.error(f"Error triggering add staff: {e}")
    
    def handle_view_reports(self):
        """Handle view reports action"""
        logger.info("View reports action")
        self.handle_navigation("Reports")
    
    def handle_sync_data(self):
        """Handle sync data action"""
        logger.info("Sync data action")
        from PyQt6.QtWidgets import QMessageBox
        try:
            from src.utils.cloud_sync import get_cloud_sync_manager
            manager = get_cloud_sync_manager()
            status = manager.get_sync_status()
            
            if not status.get('enabled'):
                QMessageBox.information(self, "Sync", 
                    "Cloud sync is not configured. Please configure it in Settings > Cloud Sync.")
                return
            
            # Trigger sync
            result = manager.sync_orders()
            if result.get('success'):
                QMessageBox.information(self, "Sync Complete", 
                    f"Data synchronized successfully.\n{result.get('message', '')}")
            else:
                QMessageBox.warning(self, "Sync Warning", 
                    f"Sync completed with warnings:\n{result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"Error syncing data: {e}")
            QMessageBox.critical(self, "Sync Error", 
                f"Failed to sync data:\n{str(e)}")
    
