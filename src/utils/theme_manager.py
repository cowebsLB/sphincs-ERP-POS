"""
Theme Manager - Dark/Light mode support
"""

from PyQt6.QtCore import QObject, pyqtSignal
from loguru import logger
from src.config.settings import get_settings


class ThemeManager(QObject):
    """Manages application theme (dark/light mode)"""
    
    theme_changed = pyqtSignal(str)  # Emits 'dark' or 'light'
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = get_settings()
        self._current_theme = self.settings.get('UI', 'theme', fallback='light')
    
    @property
    def current_theme(self) -> str:
        """Get current theme"""
        return self._current_theme
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        new_theme = 'dark' if self._current_theme == 'light' else 'light'
        self.set_theme(new_theme)
    
    def set_theme(self, theme: str):
        """Set theme (dark or light)"""
        if theme not in ['dark', 'light']:
            logger.warning(f"Invalid theme: {theme}, defaulting to light")
            theme = 'light'
        
        self._current_theme = theme
        self.settings.set('UI', 'theme', theme)
        self.theme_changed.emit(theme)
        logger.info(f"Theme changed to: {theme}")
    
    def get_stylesheet(self, component: str = 'main') -> str:
        """Get stylesheet for current theme"""
        if self._current_theme == 'dark':
            return self._get_dark_stylesheet(component)
        else:
            return self._get_light_stylesheet(component)
    
    def _get_light_stylesheet(self, component: str) -> str:
        """Light theme stylesheet"""
        if component == 'sidebar':
            return """
                QWidget {
                    background-color: #1F2937;
                }
                QPushButton {
                    text-align: left;
                    padding: 12px 16px;
                    border: none;
                    border-radius: 8px;
                    color: #D1D5DB;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #374151;
                    color: white;
                }
                QPushButton:checked {
                    background-color: #2563EB;
                    color: white;
                }
            """
        elif component == 'main':
            return """
                QWidget {
                    background-color: #F3F4F6;
                    color: #111827;
                }
                QLabel {
                    color: #111827;
                }
            """
        return ""
    
    def _get_dark_stylesheet(self, component: str) -> str:
        """Dark theme stylesheet"""
        if component == 'sidebar':
            return """
                QWidget {
                    background-color: #111827;
                }
                QPushButton {
                    text-align: left;
                    padding: 12px 16px;
                    border: none;
                    border-radius: 8px;
                    color: #9CA3AF;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1F2937;
                    color: white;
                }
                QPushButton:checked {
                    background-color: #3B82F6;
                    color: white;
                }
            """
        elif component == 'main':
            return """
                QWidget {
                    background-color: #0F172A;
                    color: #F1F5F9;
                }
                QLabel {
                    color: #F1F5F9;
                }
                QTableWidget {
                    background-color: #1E293B;
                    color: #F1F5F9;
                    border: 1px solid #334155;
                    gridline-color: #334155;
                }
                QTableWidget::item {
                    color: #F1F5F9;
                }
                QHeaderView::section {
                    background-color: #1E293B;
                    color: #F1F5F9;
                    border: none;
                    border-bottom: 2px solid #334155;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #1E293B;
                    color: #F1F5F9;
                    border: 1px solid #334155;
                }
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #2563EB;
                }
            """
        return ""


# Global theme manager instance
_theme_manager_instance = None


def get_theme_manager() -> ThemeManager:
    """Get global theme manager instance"""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance

