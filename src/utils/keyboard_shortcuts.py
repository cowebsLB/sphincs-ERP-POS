"""
Keyboard Shortcuts Manager - Global keyboard shortcuts for power users
"""

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from loguru import logger


class KeyboardShortcutsManager(QObject):
    """Manages global keyboard shortcuts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcuts = {}
        self.parent_window = parent
    
    def register_shortcut(self, key_sequence: str, callback, description: str = ""):
        """
        Register a keyboard shortcut
        
        Args:
            key_sequence: Key sequence string (e.g., "Ctrl+N", "F5")
            callback: Function to call when shortcut is triggered
            description: Optional description of what the shortcut does
        """
        try:
            shortcut = QShortcut(QKeySequence(key_sequence), self.parent_window)
            shortcut.activated.connect(callback)
            self.shortcuts[key_sequence] = {
                'shortcut': shortcut,
                'callback': callback,
                'description': description
            }
            logger.debug(f"Registered shortcut: {key_sequence} - {description}")
        except Exception as e:
            logger.error(f"Error registering shortcut {key_sequence}: {e}")
    
    def setup_default_shortcuts(self, dashboard):
        """Setup default keyboard shortcuts for the ERP dashboard"""
        # Navigation shortcuts
        self.register_shortcut("Ctrl+1", lambda: dashboard.handle_navigation("Dashboard"), "Go to Dashboard")
        self.register_shortcut("Ctrl+2", lambda: dashboard.handle_navigation("Products"), "Go to Products")
        self.register_shortcut("Ctrl+3", lambda: dashboard.handle_navigation("Inventory"), "Go to Inventory")
        self.register_shortcut("Ctrl+4", lambda: dashboard.handle_navigation("Suppliers"), "Go to Suppliers")
        self.register_shortcut("Ctrl+5", lambda: dashboard.handle_navigation("Customers"), "Go to Customers")
        self.register_shortcut("Ctrl+6", lambda: dashboard.handle_navigation("Staff"), "Go to Staff")
        self.register_shortcut("Ctrl+7", lambda: dashboard.handle_navigation("Sales"), "Go to Sales")
        self.register_shortcut("Ctrl+8", lambda: dashboard.handle_navigation("Financial"), "Go to Financial")
        self.register_shortcut("Ctrl+9", lambda: dashboard.handle_navigation("Reports"), "Go to Reports")
        self.register_shortcut("Ctrl+0", lambda: dashboard.handle_navigation("Settings"), "Go to Settings")
        
        # Common actions
        self.register_shortcut("Ctrl+N", lambda: self._trigger_add_action(dashboard), "Add New Item")
        self.register_shortcut("Ctrl+S", lambda: self._trigger_save_action(dashboard), "Save")
        self.register_shortcut("Ctrl+F", lambda: self._trigger_search_action(dashboard), "Search")
        self.register_shortcut("Ctrl+E", lambda: self._trigger_edit_action(dashboard), "Edit Selected")
        self.register_shortcut("Delete", lambda: self._trigger_delete_action(dashboard), "Delete Selected")
        self.register_shortcut("F5", lambda: self._trigger_refresh_action(dashboard), "Refresh")
        self.register_shortcut("Ctrl+W", lambda: self._trigger_close_tab(dashboard), "Close Tab")
        
        # Theme toggle
        self.register_shortcut("Ctrl+T", lambda: self._toggle_theme(dashboard), "Toggle Theme")
        
        logger.info("Keyboard shortcuts registered")
    
    def _trigger_add_action(self, dashboard):
        """Trigger add action based on current view"""
        try:
            # Try to find and trigger add button in current view
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                # Look for common add button patterns
                for child in scroll_widget.findChildren(type(scroll_widget)):
                    if hasattr(child, 'clicked') and hasattr(child, 'text'):
                        if 'Add' in child.text() or 'New' in child.text():
                            child.click()
                            return
        except Exception as e:
            logger.debug(f"Could not trigger add action: {e}")
    
    def _trigger_save_action(self, dashboard):
        """Trigger save action"""
        try:
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                for child in scroll_widget.findChildren(type(scroll_widget)):
                    if hasattr(child, 'clicked') and hasattr(child, 'text'):
                        if 'Save' in child.text():
                            child.click()
                            return
        except Exception as e:
            logger.debug(f"Could not trigger save action: {e}")
    
    def _trigger_search_action(self, dashboard):
        """Focus search field"""
        try:
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                from PyQt6.QtWidgets import QLineEdit
                search_fields = scroll_widget.findChildren(QLineEdit)
                for field in search_fields:
                    if 'search' in field.objectName().lower() or 'Search' in field.placeholderText():
                        field.setFocus()
                        return
        except Exception as e:
            logger.debug(f"Could not trigger search action: {e}")
    
    def _trigger_edit_action(self, dashboard):
        """Trigger edit action"""
        try:
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                for child in scroll_widget.findChildren(type(scroll_widget)):
                    if hasattr(child, 'clicked') and hasattr(child, 'text'):
                        if 'Edit' in child.text():
                            child.click()
                            return
        except Exception as e:
            logger.debug(f"Could not trigger edit action: {e}")
    
    def _trigger_delete_action(self, dashboard):
        """Trigger delete action"""
        try:
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                for child in scroll_widget.findChildren(type(scroll_widget)):
                    if hasattr(child, 'clicked') and hasattr(child, 'text'):
                        if 'Delete' in child.text():
                            child.click()
                            return
        except Exception as e:
            logger.debug(f"Could not trigger delete action: {e}")
    
    def _trigger_refresh_action(self, dashboard):
        """Trigger refresh/reload"""
        try:
            # Try to reload current view
            current_view = getattr(dashboard, 'current_view', None)
            if current_view:
                dashboard.handle_navigation(current_view)
        except Exception as e:
            logger.debug(f"Could not trigger refresh action: {e}")
    
    def _trigger_close_tab(self, dashboard):
        """Close current tab if in tabbed view"""
        try:
            scroll_widget = dashboard.scroll_area.widget()
            if scroll_widget:
                from PyQt6.QtWidgets import QTabWidget
                tabs = scroll_widget.findChildren(QTabWidget)
                if tabs:
                    current_index = tabs[0].currentIndex()
                    if current_index >= 0:
                        tabs[0].removeTab(current_index)
        except Exception as e:
            logger.debug(f"Could not close tab: {e}")
    
    def _toggle_theme(self, dashboard):
        """Toggle theme"""
        try:
            if hasattr(dashboard, 'sidebar') and hasattr(dashboard.sidebar, 'theme_btn'):
                dashboard.sidebar.theme_btn.click()
        except Exception as e:
            logger.debug(f"Could not toggle theme: {e}")
    
    def get_shortcuts_help(self) -> dict:
        """Get all registered shortcuts for help display"""
        return {
            key: info['description'] 
            for key, info in self.shortcuts.items()
        }

