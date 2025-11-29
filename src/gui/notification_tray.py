"""
System tray manager for Sphincs ERP notifications.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon


class NotificationTrayManager(QObject):
    """Handles tray icon, context menu, and toast notifications."""
    
    open_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    sync_requested = pyqtSignal()
    view_notifications_requested = pyqtSignal()
    
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(parent)
        self.tray_icon = QSystemTrayIcon(icon, parent)
        self.tray_icon.setToolTip("Sphincs ERP")
        self.unread_count = 0
        
        self.menu = QMenu()
        self.menu.setToolTipsVisible(True)
        
        self._build_menu()
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self._handle_activation)
    
    def _build_menu(self):
        open_action = QAction("Open ERP", self.menu)
        open_action.triggered.connect(self.open_requested)
        self.menu.addAction(open_action)
        
        view_action = QAction("View Notifications", self.menu)
        view_action.triggered.connect(self.view_notifications_requested)
        self.menu.addAction(view_action)
        
        sync_action = QAction("Sync Now", self.menu)
        sync_action.triggered.connect(self.sync_requested)
        self.menu.addAction(sync_action)
        
        self.menu.addSeparator()
        
        exit_action = QAction("Exit", self.menu)
        exit_action.triggered.connect(self.exit_requested)
        self.menu.addAction(exit_action)
    
    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def show(self):
        if not self.tray_icon.isVisible():
            self.tray_icon.show()
    
    def hide(self):
        self.tray_icon.hide()
    
    def show_notification(self, title: str, message: str, severity: str = "info"):
        icon = {
            "info": QSystemTrayIcon.MessageIcon.Information,
            "warning": QSystemTrayIcon.MessageIcon.Warning,
            "critical": QSystemTrayIcon.MessageIcon.Critical,
        }.get(severity, QSystemTrayIcon.MessageIcon.Information)
        
        self.tray_icon.showMessage(title, message, icon, 8000)
    
    def set_unread_count(self, count: int):
        self.unread_count = max(0, count)
        tooltip = "Sphincs ERP"
        if self.unread_count:
            tooltip = f"Sphincs ERP • {self.unread_count} alert(s)"
        self.tray_icon.setToolTip(tooltip)
    
    # ------------------------------------------------------------------
    # Internal callbacks
    # ------------------------------------------------------------------
    def _handle_activation(self, reason: QSystemTrayIcon.ActivationReason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.open_requested.emit()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            self.view_notifications_requested.emit()


