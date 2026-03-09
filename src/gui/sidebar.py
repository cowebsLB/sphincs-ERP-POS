"""
Collapsible Sidebar Navigation Component

Documentation:
- docs/INDEX.md
- docs/erp/uiux-roadmap.md
- docs/erp/uiux-audit-baseline.md
- docs/erp/uiux-phase1-shell-refresh.md
- docs/erp/module-map.md
- docs/erp/worklog.md
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from src.gui.design_system import (
    SIDEBAR_DANGER_ICON_BUTTON_STYLE,
    SIDEBAR_ICON_BUTTON_STYLE,
    SIDEBAR_ROOT_STYLE,
    SIDEBAR_USER_CARD_STYLE,
)


class Sidebar(QWidget):
    """Collapsible sidebar navigation."""

    navigation_clicked = pyqtSignal(str)
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.expanded_width = 276
        self.collapsed_width = 84
        self.is_collapsed = False
        self.nav_structure = [
            {
                "group": "Overview",
                "icon": "OV",
                "items": [
                    {"name": "Dashboard", "icon": "DB"},
                ],
            },
            {
                "group": "Sales & CRM",
                "icon": "SC",
                "items": [
                    {"name": "Products", "icon": "PR"},
                    {"name": "Customers", "icon": "CU"},
                    {"name": "Sales", "icon": "SA"},
                    {"name": "Reports", "icon": "RP"},
                ],
            },
            {
                "group": "Inventory & Supply",
                "icon": "IS",
                "items": [
                    {"name": "Inventory", "icon": "IV"},
                    {"name": "Suppliers", "icon": "SU"},
                ],
            },
            {
                "group": "Staff & HR",
                "icon": "HR",
                "items": [
                    {"name": "Staff", "icon": "ST"},
                    {"name": "Attendance", "icon": "AT"},
                    {"name": "Shift Scheduling", "icon": "SH"},
                    {"name": "Payroll", "icon": "PY"},
                    {"name": "Performance", "icon": "PF"},
                ],
            },
            {
                "group": "Finance & Ops",
                "icon": "FO",
                "items": [
                    {"name": "Financial", "icon": "FN"},
                    {"name": "Operations", "icon": "OP"},
                ],
            },
            {
                "group": "Industry Solutions",
                "icon": "IN",
                "items": [
                    {"name": "Retail & E-Commerce", "icon": "RE"},
                    {"name": "Healthcare", "icon": "HC"},
                    {"name": "Education", "icon": "ED"},
                    {"name": "Manufacturing", "icon": "MF"},
                    {"name": "Logistics", "icon": "LG"},
                ],
            },
            {
                "group": "Platform",
                "icon": "PL",
                "items": [
                    {"name": "Mobile", "icon": "MB"},
                    {"name": "Settings", "icon": "SG"},
                ],
            },
        ]
        self.group_meta = {grp["group"]: grp for grp in self.nav_structure}

        self.group_buttons = {}
        self.group_contents = {}
        self.nav_buttons = {}
        self.setObjectName("sidebar")
        self.setup_ui()

    def setup_ui(self):
        """Setup sidebar UI."""
        self.setFixedWidth(self.expanded_width)
        self.setStyleSheet(SIDEBAR_ROOT_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.toggle_btn = QPushButton("MENU")
        self.toggle_btn.setFixedSize(56, 32)
        self.toggle_btn.setToolTip("Collapse/Expand Sidebar")
        self.toggle_btn.setStyleSheet(SIDEBAR_ICON_BUTTON_STYLE)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        header_layout.addWidget(self.toggle_btn)

        self.logout_btn = QPushButton("OUT")
        self.logout_btn.setFixedSize(44, 32)
        self.logout_btn.setToolTip("Logout")
        self.logout_btn.setStyleSheet(SIDEBAR_DANGER_ICON_BUTTON_STYLE)
        self.logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_btn)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()

        self.nav_layout = QVBoxLayout(scroll_content)
        self.nav_layout.setSpacing(4)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)

        for group in self.nav_structure:
            group_name = group["group"]
            group_icon = group["icon"]

            header_btn = QPushButton()
            header_btn.setCheckable(True)
            header_btn.setChecked(True)
            header_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            header_btn.setObjectName("groupHeader")
            header_btn.setToolTip(group_name)
            header_btn.clicked.connect(lambda _, name=group_name: self.toggle_group(name))
            self.group_buttons[group_name] = header_btn
            self.nav_layout.addWidget(header_btn)

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(4)
            content_layout.setContentsMargins(8, 0, 0, 8)

            for item in group["items"]:
                item_name = item["name"]
                item_icon = item["icon"]

                btn = QPushButton(f"{item_icon}  {item_name}")
                btn.setCheckable(True)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setProperty("icon_str", item_icon)
                btn.setProperty("text_str", item_name)
                btn.setProperty("collapsed", False)
                btn.setToolTip(item_name)
                btn.setObjectName("navButton")
                if item_name == "Dashboard":
                    btn.setChecked(True)
                btn.clicked.connect(lambda _, name=item_name: self.on_nav_clicked(name))
                self.nav_buttons[item_name] = btn
                content_layout.addWidget(btn)

            self.group_contents[group_name] = content_widget
            self.nav_layout.addWidget(content_widget)
            self.nav_layout.addSpacing(4)

            # Group icon is stored in metadata and used in header rendering.
            self.group_meta[group_name]["icon"] = group_icon

        self.nav_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area, stretch=1)

        self.user_frame = QFrame()
        self.user_frame.setMinimumHeight(66)
        self.user_frame.setStyleSheet(SIDEBAR_USER_CARD_STYLE)
        user_layout = QVBoxLayout(self.user_frame)
        user_layout.setSpacing(2)
        user_layout.setContentsMargins(10, 8, 10, 8)

        self.user_name_label = QLabel("Admin")
        self.user_name_label.setStyleSheet(
            "color: #F8FAFC; font-size: 13px; font-weight: 700; background-color: transparent;"
        )
        user_layout.addWidget(self.user_name_label)

        self.user_role_label = QLabel("Administrator")
        self.user_role_label.setStyleSheet(
            "color: #94A3B8; font-size: 11px; font-weight: 500; background-color: transparent;"
        )
        user_layout.addWidget(self.user_role_label)
        layout.addWidget(self.user_frame)

        self.update_group_headers()
        self._apply_collapsed_visual_state()

    def handle_logout(self):
        """Handle logout button click."""
        self.logout_requested.emit()

    def toggle_sidebar(self):
        """Toggle sidebar collapsed/expanded state."""
        self.is_collapsed = not self.is_collapsed
        self.setFixedWidth(self.collapsed_width if self.is_collapsed else self.expanded_width)

        if self.is_collapsed:
            self.toggle_btn.setText("||")
            self.logout_btn.setText("X")
            self.toggle_btn.setFixedSize(36, 32)
            self.logout_btn.setFixedSize(36, 32)
            self.user_frame.hide()
            for btn in self.nav_buttons.values():
                icon_str = btn.property("icon_str")
                btn.setText(str(icon_str) if icon_str else "")
                btn.setToolTip(str(btn.property("text_str") or ""))
        else:
            self.toggle_btn.setText("MENU")
            self.logout_btn.setText("OUT")
            self.toggle_btn.setFixedSize(56, 32)
            self.logout_btn.setFixedSize(44, 32)
            self.user_frame.show()
            for btn in self.nav_buttons.values():
                icon_str = str(btn.property("icon_str") or "")
                text_str = str(btn.property("text_str") or "")
                btn.setText(f"{icon_str}  {text_str}".strip())
                btn.setToolTip("")

        self.update_group_headers()
        self._apply_collapsed_visual_state()

    def on_nav_clicked(self, section: str):
        """Handle navigation button click."""
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
        if section in self.nav_buttons:
            self.nav_buttons[section].setChecked(True)
        self.ensure_group_visible(section)
        self.navigation_clicked.emit(section)

    def set_active_section(self, section: str):
        """Set active navigation section."""
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
        if section in self.nav_buttons:
            self.nav_buttons[section].setChecked(True)
        self.ensure_group_visible(section)

    def set_user_info(self, username: str, role: str):
        """Set user information in sidebar."""
        self.user_name_label.setText(username)
        self.user_role_label.setText(role)

    def toggle_group(self, group_name: str):
        """Toggle visibility of a navigation group."""
        header = self.group_buttons.get(group_name)
        content = self.group_contents.get(group_name)
        if not header or not content:
            return
        expanded = header.isChecked()
        content.setVisible(expanded)
        self.update_group_header_text(group_name)

    def update_group_headers(self):
        """Refresh header labels for all groups."""
        for group_name in self.group_buttons.keys():
            self.update_group_header_text(group_name)

    def update_group_header_text(self, group_name: str):
        """Update a single group header based on expansion/collapse state."""
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
            arrow = "v" if expanded else ">"
            header.setText(f"{arrow} {icon}  {group_name}")
        header.setToolTip(group_name)

    def _apply_collapsed_visual_state(self):
        """Apply visual state updates for collapsed vs expanded sidebar."""
        for header in self.group_buttons.values():
            header.setVisible(not self.is_collapsed)
        for btn in self.nav_buttons.values():
            btn.setProperty("collapsed", self.is_collapsed)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def ensure_group_visible(self, section: str):
        """Ensure the group for the given section is expanded."""
        for group_name, group in self.group_meta.items():
            if any(item["name"] == section for item in group["items"]):
                header = self.group_buttons.get(group_name)
                content = self.group_contents.get(group_name)
                if header and content and not content.isVisible():
                    header.setChecked(True)
                    content.setVisible(True)
                    self.update_group_header_text(group_name)
                break
