"""
Sphincs POS - Main Entry Point
Point of Sale Application
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from loguru import logger

from src.config.settings import get_settings
from src.utils.logger import setup_logger
from src.gui.splash_screen import SplashScreen
from src.gui.pos_window import POSWindow
from src.database.connection import get_db_manager
from src import __version__
from src.gui.table_utils import install_table_auto_resize


def main():
    """Main entry point for Sphincs POS"""
    # Setup logging
    app_logger = setup_logger("SphincsPOS")
    logger.info("Starting Sphincs POS...")
    
    # PyQt6 has high DPI scaling enabled by default
    # No need to set these attributes (they were removed in PyQt6)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Sphincs POS")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("Sphincs")
    install_table_auto_resize(app)
    
    # Set application icon (use POS-style icon if available, otherwise main icon)
    icon_path = project_root / "sphincs_icon_pos.ico"
    if not icon_path.exists():
        icon_path = project_root / "sphincs_icon.ico"
    splash_icon_pixmap = None
    if icon_path.exists():
        icon = QIcon(str(icon_path))
        app.setWindowIcon(icon)
        # Convert QIcon to QPixmap for splash screen
        splash_icon_pixmap = icon.pixmap(128, 128)  # Use 128x128 size for splash
    
    # Get settings
    settings = get_settings()
    
    # Create and show splash screen
    splash = SplashScreen(
        app_name="Sphincs POS",
        app_version=__version__,
        app_icon=splash_icon_pixmap
    )
    splash.show()
    
    # Process events to show splash screen
    app.processEvents()
    
    # Simulate initialization tasks
    def initialize_app():
        """Initialize application components"""
        splash.update_status("Loading configuration...")
        app.processEvents()
        
        # Initialize database
        splash.update_status("Connecting to database...")
        app.processEvents()
        try:
            db_manager = get_db_manager()
            db_manager.create_tables()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            splash.update_status("Database error - check logs")
            app.processEvents()
        
        # Wait for update check to complete (if enabled)
        if settings.get_bool('Updates', 'check_on_startup', True):
            # Give update check time to complete
            QTimer.singleShot(2000, finish_initialization)
        else:
            finish_initialization()
    
    def finish_initialization():
        """Finish initialization and show main window"""
        splash.update_status("Ready!")
        app.processEvents()
        
        # Keep splash screen visible for a moment
        QTimer.singleShot(1500, lambda: show_main_window())
        
        logger.info("Sphincs POS initialized successfully")
    
    # Store main window in outer scope so it doesn't get garbage collected
    main_window = None
    
    def show_main_window():
        """Show main POS window (with integrated login)"""
        nonlocal main_window
        
        # Close splash screen
        splash.close()
        
        # Create and show POS window (login is integrated)
        main_window = POSWindow()
        
        # Connect logout signal to show login again
        def on_logout():
            """Handle logout - return to login screen"""
            logger.info("Logout - returning to login screen")
            main_window.show_login_screen()
        
        main_window.logout_requested.connect(on_logout)
        main_window.show()
        
        logger.info("POS Window displayed")
    
    # Start initialization after short delay
    QTimer.singleShot(500, initialize_app)
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

