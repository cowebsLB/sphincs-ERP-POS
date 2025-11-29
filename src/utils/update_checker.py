"""
Auto-update checker for GitHub releases
"""
import requests
import re
from typing import Optional, Dict, Any
from packaging import version as pkg_version
from loguru import logger


class UpdateChecker:
    """Check for updates from GitHub releases"""
    
    def __init__(self, repo_owner: str, repo_name: str, current_version: str):
        """
        Initialize update checker
        
        Args:
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
            current_version: Current application version (e.g., "1.2.3")
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = self._normalize_version(current_version)
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.latest_release: Optional[Dict[str, Any]] = None
    
    def _normalize_version(self, version: str) -> str:
        """Normalize version string (remove 'v' prefix if present)"""
        return version.lstrip('vV')
    
    def check_for_updates(self, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Check GitHub for latest release
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            Update info dict if update available, None otherwise
        """
        try:
            logger.info(f"Checking for updates: {self.repo_owner}/{self.repo_name}")
            response = requests.get(self.api_url, timeout=timeout)
            response.raise_for_status()
            
            release_data = response.json()
            self.latest_release = release_data
            
            latest_version = self._normalize_version(release_data.get('tag_name', ''))
            
            if self._is_newer_version(latest_version):
                logger.info(f"Update available: {self.current_version} -> {latest_version}")
                return {
                    'current_version': self.current_version,
                    'latest_version': latest_version,
                    'tag_name': release_data.get('tag_name', ''),
                    'name': release_data.get('name', ''),
                    'body': release_data.get('body', ''),
                    'published_at': release_data.get('published_at', ''),
                    'html_url': release_data.get('html_url', ''),
                    'assets': release_data.get('assets', []),
                }
            else:
                logger.info(f"No update available. Current: {self.current_version}, Latest: {latest_version}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check for updates: {e}")
            return None
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return None
    
    def _is_newer_version(self, latest_version: str) -> bool:
        """
        Check if latest version is newer than current version
        
        Args:
            latest_version: Latest version string
            
        Returns:
            True if latest version is newer
        """
        try:
            current = pkg_version.parse(self.current_version)
            latest = pkg_version.parse(latest_version)
            return latest > current
        except Exception as e:
            logger.error(f"Error comparing versions: {e}")
            return False
    
    def get_download_url(self, asset_name_pattern: Optional[str] = None) -> Optional[str]:
        """
        Get download URL for update installer
        
        Args:
            asset_name_pattern: Pattern to match asset name (e.g., "SphincsERP-Setup")
            
        Returns:
            Download URL or None
        """
        if not self.latest_release:
            return None
        
        assets = self.latest_release.get('assets', [])
        if not assets:
            return None
        
        if asset_name_pattern:
            # Find asset matching pattern
            for asset in assets:
                if asset_name_pattern.lower() in asset.get('name', '').lower():
                    return asset.get('browser_download_url')
        
        # Return first asset if no pattern specified
        return assets[0].get('browser_download_url') if assets else None

