"""
Configuration management for Sphincs ERP + POS
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import configparser


class Settings:
    """Application settings manager"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize settings manager
        
        Args:
            config_dir: Directory for config files (default: user's AppData)
        """
        if config_dir is None:
            # Windows: %APPDATA%\Sphincs ERP+POS
            appdata = os.getenv('APPDATA', os.path.expanduser('~'))
            self.config_dir = Path(appdata) / "Sphincs ERP+POS"
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.ini"
        self.config = configparser.ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration"""
        # Application settings
        self.config['Application'] = {
            'version': '1.0.0',
            'app_name': 'Sphincs ERP+POS',
            'language': 'en',
        }
        
        # Database settings
        db_path = self.config_dir / "sphincs.db"
        self.config['Database'] = {
            'local_db_path': str(db_path),
            'cloud_db_url': '',
            'cloud_db_type': 'postgresql',  # postgresql or mysql
            'sync_enabled': 'false',
        }
        
        # Update settings
        self.config['Updates'] = {
            'enabled': 'true',
            'check_on_startup': 'true',
            'check_interval_hours': '24',
            'auto_download': 'false',
            'auto_install': 'false',
            'update_channel': 'stable',  # stable, beta, alpha
        }
        
        # UI settings
        self.config['UI'] = {
            'theme': 'light',
            'dpi_scaling': 'true',
            'touch_mode': 'false',
        }
        
        # Hardware settings
        self.config['Hardware'] = {
            'printer_name': '',
            'printer_type': 'escpos',
            'barcode_scanner_enabled': 'false',
            'cash_drawer_enabled': 'false',
        }
        
        self.save()
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section: str, key: str, value: Any):
        """Set configuration value"""
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save()
    
    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value"""
        return self.config.getfloat(section, key, fallback=fallback)


# Global settings instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def save_settings(settings_dict: Dict[str, Any]) -> None:
    """
    Save settings dictionary to config file
    
    Args:
        settings_dict: Dictionary with section names as keys and dict of settings as values
    """
    settings = get_settings()
    
    for section, values in settings_dict.items():
        for key, value in values.items():
            settings.set(section, key, value)
    
    settings.save()

