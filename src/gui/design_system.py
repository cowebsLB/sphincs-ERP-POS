"""
Shared ERP design tokens and reusable Qt style snippets.

Documentation:
- docs/INDEX.md
- docs/erp/uiux-roadmap.md
- docs/erp/uiux-audit-baseline.md
- docs/erp/uiux-phase1-shell-refresh.md
- docs/erp/uiux-phase2-global-refresh.md
- docs/erp/implementation-summary-2026-03-09.md
- docs/erp/worklog.md
"""

from PyQt6.QtWidgets import QLabel


# Color tokens
BG_PAGE = "#F8FAFC"
BG_SURFACE = "#FFFFFF"
BG_SURFACE_ALT = "#F1F5F9"
TEXT_PRIMARY = "#0F172A"
TEXT_MUTED = "#475569"
TEXT_SUBTLE = "#64748B"
BORDER_SOFT = "#E2E8F0"
BORDER_STRONG = "#CBD5E1"
ACCENT = "#0EA5E9"
ACCENT_DARK = "#0284C7"
ACCENT_SOFT = "#E0F2FE"
DANGER = "#DC2626"
DANGER_SOFT = "#FEE2E2"


# Shared shell styles
ERP_APP_BASE_STYLE = f"""
QWidget {{
    background-color: {BG_PAGE};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "Noto Sans", sans-serif;
    font-size: 13px;
}}
QMainWindow {{
    background-color: {BG_PAGE};
}}
QFrame {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
}}
QLabel {{
    color: {TEXT_PRIMARY};
    background-color: transparent;
}}
QGroupBox {{
    color: {TEXT_PRIMARY};
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: {TEXT_MUTED};
}}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QDateTimeEdit, QListWidget {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_STRONG};
    border-radius: 8px;
    padding: 7px 10px;
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QDateTimeEdit:focus {{
    border: 2px solid {ACCENT};
}}
QPushButton {{
    background-color: {BG_SURFACE_ALT};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #E2E8F0;
}}
QPushButton:pressed {{
    background-color: #CBD5E1;
}}
QPushButton:disabled {{
    color: #94A3B8;
}}
QTabWidget::pane {{
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
    background-color: {BG_SURFACE};
}}
QTabBar::tab {{
    background-color: {BG_SURFACE_ALT};
    color: {TEXT_MUTED};
    padding: 9px 16px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}
QTabBar::tab:selected {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-bottom: none;
}}
QTableWidget, QTableView, QTreeWidget, QTreeView {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    alternate-background-color: {BG_SURFACE_ALT};
    gridline-color: {BORDER_SOFT};
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
}}
QTableWidget::item, QTreeWidget::item {{
    padding: 6px;
}}
QHeaderView::section {{
    background-color: {BG_SURFACE_ALT};
    color: {TEXT_PRIMARY};
    border: none;
    border-bottom: 1px solid {BORDER_SOFT};
    padding: 8px;
    font-weight: 700;
}}
QTableCornerButton::section {{
    background-color: {BG_SURFACE_ALT};
    border: none;
    border-bottom: 1px solid {BORDER_SOFT};
}}
QScrollArea {{
    border: none;
    background-color: transparent;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 4px;
}}
QScrollBar::handle:vertical {{
    background: #CBD5E1;
    min-height: 20px;
    border-radius: 5px;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #CBD5E1;
    min-width: 20px;
    border-radius: 5px;
}}
QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {{
    background: none;
    border: none;
}}
QMenu {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{
    padding: 8px 12px;
    border-radius: 6px;
}}
QMenu::item:selected {{
    background-color: {ACCENT_SOFT};
}}
QToolTip {{
    background-color: #0F172A;
    color: #F8FAFC;
    border: 1px solid #1E293B;
    padding: 6px 8px;
}}
"""

PAGE_SCROLL_STYLE = f"""
QScrollArea {{
    background-color: {BG_PAGE};
    border: none;
}}
"""

CARD_STYLE = f"""
QFrame {{
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
}}
"""

TAB_WIDGET_STYLE = f"""
QTabWidget::pane {{
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
    background-color: {BG_SURFACE};
}}
QTabBar::tab {{
    background-color: {BG_SURFACE_ALT};
    color: {TEXT_MUTED};
    padding: 10px 18px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}
QTabBar::tab:selected {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    font-weight: 600;
    border: 1px solid {BORDER_SOFT};
    border-bottom: none;
}}
"""

GROUP_BOX_STYLE = f"""
QGroupBox {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: {BG_SURFACE};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
}}
"""

INPUT_STYLE = f"""
QLineEdit, QComboBox {{
    border: 1px solid {BORDER_STRONG};
    border-radius: 8px;
    padding: 8px 10px;
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    min-height: 34px;
}}
QLineEdit:focus, QComboBox:focus {{
    border: 2px solid {ACCENT};
}}
"""

PRIMARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {ACCENT};
    color: {BG_SURFACE};
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {ACCENT_DARK};
}}
QPushButton:pressed {{
    background-color: {ACCENT_DARK};
}}
"""

SECONDARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {BG_SURFACE_ALT};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_SOFT};
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #E2E8F0;
}}
"""

DANGER_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {DANGER_SOFT};
    color: {DANGER};
    border: 1px solid {DANGER};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {DANGER};
    color: {BG_SURFACE};
}}
"""

LIST_WIDGET_STYLE = f"""
QListWidget {{
    border: none;
    background-color: transparent;
}}
QListWidget::item {{
    padding: 10px 12px;
    border-bottom: 1px solid {BORDER_SOFT};
}}
"""


# Sidebar styles
SIDEBAR_ROOT_STYLE = f"""
#sidebar {{
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}}
#sidebar QWidget {{
    background-color: transparent;
    color: #E2E8F0;
}}
#sidebar QScrollArea {{
    border: none;
    background-color: transparent;
}}
#sidebar QScrollBar:vertical {{
    width: 0px;
}}
#sidebar QPushButton#groupHeader {{
    background-color: transparent;
    color: #E2E8F0;
    font-size: 12px;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border-radius: 6px;
}}
#sidebar QPushButton#groupHeader:hover {{
    background-color: #1E293B;
    color: #F8FAFC;
}}
#sidebar QPushButton#navButton {{
    text-align: left;
    padding: 10px 12px;
    border: none;
    border-radius: 8px;
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 600;
    background-color: transparent;
}}
#sidebar QPushButton#navButton:hover {{
    background-color: #1E293B;
}}
#sidebar QPushButton#navButton:checked {{
    background-color: #0C4A6E;
    color: #E0F2FE;
}}
#sidebar QPushButton#navButton[collapsed="true"] {{
    text-align: center;
    padding: 10px 0px;
    font-size: 18px;
    font-weight: 700;
    color: #DDEAFE;
}}
#sidebar QPushButton#navButton:checked[collapsed="true"] {{
    background-color: #075985;
    color: #E0F2FE;
}}
"""

SIDEBAR_ICON_BUTTON_STYLE = """
QPushButton {
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #E2E8F0;
    font-size: 11px;
    font-weight: 700;
    padding: 0px;
}
QPushButton:hover {
    background-color: #1E293B;
}
"""

SIDEBAR_DANGER_ICON_BUTTON_STYLE = """
QPushButton {
    background-color: #111827;
    border: 1px solid #DC2626;
    border-radius: 8px;
    color: #FCA5A5;
    font-size: 11px;
    font-weight: 700;
    padding: 0px;
}
QPushButton:hover {
    background-color: #DC2626;
    color: #FFFFFF;
}
"""

SIDEBAR_USER_CARD_STYLE = """
QFrame {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 10px;
}
"""


def apply_page_title(label: QLabel):
    """Apply standard top-level page title styling."""
    label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 26px; font-weight: 700;")


def apply_section_title(label: QLabel):
    """Apply standard section title styling."""
    label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 18px; font-weight: 700;")


def apply_muted_text(label: QLabel, size: int = 13):
    """Apply standard muted text style."""
    label.setStyleSheet(f"color: {TEXT_SUBTLE}; font-size: {size}px;")
