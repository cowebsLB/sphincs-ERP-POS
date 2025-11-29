"""
Collapsible Sidebar Navigation Component
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QIcon
from loguru import logger


class Sidebar(QWidget):
    """Collapsible sidebar navigation"""
    
    # Signal emitted when a navigation item is clicked
    navigation_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        self.nav_structure = [
            {
                "group": "Overview",
                "icon": "🏠",
                "items": [
                    {"name": "Dashboard", "icon": "📊"}
                ]
            },
            {
                "group": "Sales & CRM",
                "icon": "🛍️",
                "items": [
                    {"name": "Products", "icon": "📦"},
                    {"name": "Customers", "icon": "👥"},
                    {"name": "Sales", "icon": "💰"},
                    {"name": "Reports", "icon": "📈"}
                ]
            },
            {
                "group": "Inventory & Supply",
                "icon": "📦",
                "items": [
                    {"name": "Inventory", "icon": "📋"},
                    {"name": "Suppliers", "icon": "🏢"}
                ]
            },
            {
                "group": "Staff & HR",
                "icon": "👥",
                "items": [
                    {"name": "Staff", "icon": "👤"},
                    {"name": "Attendance", "icon": "🕒"},
                    {"name": "Shift Scheduling", "icon": "📅"},
                    {"name": "Payroll", "icon": "💵"},
                    {"name": "Performance", "icon": "⭐"}
                ]
            },
            {
                "group": "Finance & Ops",
                "icon": "💼",
                "items": [
                    {"name": "Financial", "icon": "💵"},
                    {"name": "Operations", "icon": "🛠️"}
                ]
            },
            {
                "group": "Industry Solutions",
                "icon": "🏭",
                "items": [
                    {"name": "Retail & E-Commerce", "icon": "🛒"},
                    {"name": "Healthcare", "icon": "🏥"},
                    {"name": "Education", "icon": "🎓"},
                    {"name": "Manufacturing", "icon": "🏭"},
                    {"name": "Logistics", "icon": "🚚"}
                ]
            },
            {
                "group": "Platform",
                "icon": "⚙️",
                "items": [
                    {"name": "Mobile", "icon": "📱"},
                    {"name": "Settings", "icon": "⚙️"}
                ]
            }
        ]
        self.group_meta = {grp["group"]: grp for grp in self.nav_structure}
        
        self.group_buttons = {}
        self.group_contents = {}
        self.nav_buttons = {}
        self.setObjectName("sidebar")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI"""
        self.setFixedWidth(240)  # Expanded width
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #F1F5F9;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 0px;
            }
            QScrollBar::handle:vertical {
                background: transparent;
                min-height: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: transparent;
                height: 0px;
            }
            QScrollBar::handle:horizontal {
                background: transparent;
                min-width: 0px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QPushButton#navButton {
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 10px;
                color: #0F172A;
                font-size: 14px;
                font-weight: 500;
                background-color: #FFFFFF;
            }
            QPushButton#navButton:hover {
                background-color: #E2E8F0;
                color: #0F172A;
            }
            QPushButton#navButton:checked {
                background-color: #E0E7FF;
                color: #1E3A8A;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header with collapse/expand and logout buttons
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Collapse/Expand button (hamburger menu) - on the left
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(32, 32)
        self.toggle_btn.setToolTip("Collapse/Expand Sidebar")
        # Override general button styles for this specific button
        self.toggle_btn.setStyleSheet("""
            QPushButton#toggle_btn {
                background-color: transparent;
                border: 1px solid #374151;
                border-radius: 6px;
                font-size: 20px;
                font-weight: bold;
                color: #D1D5DB;
                text-align: center;
                padding: 0px;
            }
            QPushButton#toggle_btn:hover {
                background-color: #374151;
                color: white;
            }
        """)
        self.toggle_btn.setObjectName("toggle_btn")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        header_layout.addWidget(self.toggle_btn)
        
        # Logout button - in header
        self.logout_btn = QPushButton("⇱")
        self.logout_btn.setFixedSize(32, 32)
        self.logout_btn.setToolTip("Logout")
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.setProperty("icon", "⇱")
        self.logout_btn.setProperty("text", "Logout")
        self.logout_btn.setCheckable(False)
        # Override general button styles for this specific button
        self.logout_btn.setStyleSheet("""
            QPushButton#logout_btn {
                background-color: transparent;
                border: 1px solid #EF4444;
                border-radius: 6px;
                font-size: 18px;
                font-weight: bold;
                color: #EF4444;
                text-align: center;
                padding: 0px;
            }
            QPushButton#logout_btn:hover {
                background-color: #EF4444;
                color: white;
            }
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_btn)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addSpacing(8)
        
        # Scrollable navigation container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide vertical scrollbar
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)  # Remove frame for cleaner look
        scroll_content = QWidget()
        self.nav_layout = QVBoxLayout(scroll_content)
        self.nav_layout.setSpacing(6)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation groups
        for group in self.nav_structure:
            group_name = group["group"]
            group_icon = group["icon"]
            header_btn = QPushButton()
            header_btn.setCheckable(True)
            header_btn.setChecked(True)
            header_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            header_btn.setObjectName("groupHeader")
            header_btn.setToolTip(group_name)
            header_btn.clicked.connect(lambda checked, name=group_name: self.toggle_group(name))
            header_btn.setStyleSheet("""
                QPushButton#groupHeader {
                    background-color: transparent;
                    color: #9CA3AF;
                    font-size: 13px;
                    font-weight: 600;
                    text-align: left;
                    padding: 6px 8px;
                    border-radius: 6px;
                }
                QPushButton#groupHeader:hover {
                    background-color: #374151;
                    color: white;
                }
            """)
            self.group_buttons[group_name] = header_btn
            self.nav_layout.addWidget(header_btn)
            
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(4)
            content_layout.setContentsMargins(8, 0, 0, 8)
            
            for item in group["items"]:
                item_name = item["name"]
                item_icon = item["icon"]
                btn = QPushButton(f"{item['icon']} {item['name']}")
                btn.setCheckable(True)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setProperty("icon_str", str(item_icon))
                btn.setProperty("text_str", str(item_name))
                btn.setToolTip(item_name)
                if item_name == "Dashboard":
                    btn.setChecked(True)
                btn.clicked.connect(lambda checked, name=item_name: self.on_nav_clicked(name))
                self.nav_buttons[item_name] = btn
                btn.setObjectName("navButton")
                content_layout.addWidget(btn)
            
            self.group_contents[group_name] = content_widget
            self.nav_layout.addWidget(content_widget)
            self.nav_layout.addSpacing(4)
        
        self.nav_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area, stretch=1)
        
        self.update_group_headers()
        
        layout.addStretch()
        
        # User info at bottom
        self.user_frame = QFrame()
        self.user_frame.setMinimumHeight(60)
        self.user_frame.setStyleSheet("""
            QFrame {
                background-color: #374151;
                border-radius: 8px;
            }
        """)
        user_layout = QVBoxLayout(self.user_frame)
        user_layout.setSpacing(4)
        user_layout.setContentsMargins(12, 8, 12, 8)
        
        self.user_name_label = QLabel("Admin")
        self.user_name_label.setWordWrap(True)
        self.user_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.user_name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 0px;
                margin: 0px;
                background-color: transparent;
            }
        """)
        user_layout.addWidget(self.user_name_label)
        
        self.user_role_label = QLabel("Administrator")
        self.user_role_label.setWordWrap(True)
        self.user_role_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.user_role_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 12px;
                padding: 0px;
                margin: 0px;
                background-color: transparent;
            }
        """)
        user_layout.addWidget(self.user_role_label)
        
        layout.addWidget(self.user_frame)
    
    # Signal for logout
    logout_requested = pyqtSignal()
    
    def handle_logout(self):
        """Handle logout button click"""
        self.logout_requested.emit()
    
    def toggle_sidebar(self):
        """Toggle sidebar collapsed/expanded state"""
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            # Collapse: show only icons
            self.setFixedWidth(80)
            
            # Update buttons to show only icons
            for btn in self.nav_buttons.values():
                icon_str = btn.property("icon_str")
                text_str = btn.property("text_str")
                if icon_str:
                    btn.setText(str(icon_str))
                if text_str:
                    btn.setToolTip(str(text_str))
            
            # Logout button stays as icon in header (no change needed)
            
            # Hide user info
            self.user_frame.hide()
        else:
            # Expand: show icons + text
            self.setFixedWidth(240)
            
            # Update buttons to show icon + text
            for btn in self.nav_buttons.values():
                icon_str = btn.property("icon_str")
                text_str = btn.property("text_str")
                if icon_str and text_str:
                    btn.setText(f"{icon_str} {text_str}")
                elif text_str:
                    btn.setText(str(text_str))
                btn.setToolTip("")
            
            # Logout button stays as icon in header (no change needed)
            
            # Show user info
            self.user_frame.show()
        
        self.update_group_headers()
    
    def on_nav_clicked(self, section: str):
        """Handle navigation button click"""
        # Uncheck all buttons
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
        
        # Check clicked button
        if section in self.nav_buttons:
            self.nav_buttons[section].setChecked(True)
        self.ensure_group_visible(section)
        
        # Emit signal
        self.navigation_clicked.emit(section)
    
    def set_active_section(self, section: str):
        """Set active navigation section"""
        # Uncheck all buttons
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
        
        # Check specified section
        if section in self.nav_buttons:
            self.nav_buttons[section].setChecked(True)
        self.ensure_group_visible(section)
    
    def set_user_info(self, username: str, role: str):
        """Set user information in sidebar"""
        self.user_name_label.setText(username)
        self.user_role_label.setText(role)
    
    
    def toggle_group(self, group_name: str):
        """Toggle visibility of a navigation group"""
        header = self.group_buttons.get(group_name)
        content = self.group_contents.get(group_name)
        if not header or not content:
            return
        expanded = header.isChecked()
        content.setVisible(expanded)
        self.update_group_header_text(group_name)
    
    def update_group_headers(self):
        """Refresh header labels for all groups"""
        for group_name in self.group_buttons.keys():
            self.update_group_header_text(group_name)
    
    def update_group_header_text(self, group_name: str):
        header = self.group_buttons.get(group_name)
        content = self.group_contents.get(group_name)
        meta = self.group_meta.get(group_name, {})
        if not header or content is None:
            return
        icon = meta.get("icon", "")
        if self.is_collapsed:
            header.setText(icon)
        else:
            expanded = content.isVisible()
            arrow = "▾" if expanded else "▸"
            header.setText(f"{arrow} {icon}  {group_name}")
        header.setToolTip(group_name)
    
    def ensure_group_visible(self, section: str):
        """Ensure the group for the given section is expanded"""
        for group_name, group in self.group_meta.items():
            if any(item["name"] == section for item in group["items"]):
                header = self.group_buttons.get(group_name)
                content = self.group_contents.get(group_name)
                if header and content and not content.isVisible():
                    header.setChecked(True)
                    content.setVisible(True)
                    self.update_group_header_text(group_name)
                break

