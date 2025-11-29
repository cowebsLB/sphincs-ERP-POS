"""
Logging configuration for Sphincs ERP + POS
"""
import logging
import sys
import io
from pathlib import Path
from typing import Optional
from datetime import datetime
from loguru import logger


def setup_logger(app_name: str = "Sphincs", log_dir: Optional[Path] = None):
    """
    Setup application logger
    
    Args:
        app_name: Application name (ERP or POS)
        log_dir: Directory for log files (default: config directory)
    """
    from src.config.settings import get_settings
    
    settings = get_settings()
    
    if log_dir is None:
        log_dir = settings.config_dir / "logs"
    else:
        log_dir = Path(log_dir)
    
    # Ensure log directory exists
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        # Fallback to temp directory if config dir fails
        import tempfile
        log_dir = Path(tempfile.gettempdir()) / "Sphincs" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file with date
    log_file = log_dir / f"{app_name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Ensure log_file is a valid path
    if log_file is None or not log_file.parent.exists():
        # Last resort: use temp directory
        import tempfile
        log_file = Path(tempfile.gettempdir()) / f"{app_name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with color (only if stderr is available)
    # In windowed executables, stderr might be None or not writable
    try:
        if sys.stderr is not None and hasattr(sys.stderr, 'write'):
            logger.add(
                sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level="INFO",
                colorize=True,
            )
    except (TypeError, AttributeError, OSError, io.UnsupportedOperation):
        # stderr is not available or not writable in windowed executables
        # This is normal for PyInstaller windowed apps, so we just skip console logging
        pass
    
    # Add file handler
    try:
        logger.add(
            str(log_file),  # Convert to string for better compatibility
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )
    except (TypeError, AttributeError, OSError) as e:
        # If file logging fails, at least ensure we have a basic handler
        # This should not happen, but handle gracefully
        import tempfile
        fallback_log = Path(tempfile.gettempdir()) / f"{app_name}_fallback.log"
        try:
            logger.add(
                str(fallback_log),
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                level="DEBUG",
            )
        except Exception:
            # If even fallback fails, just continue without file logging
            pass
    
    return logger

