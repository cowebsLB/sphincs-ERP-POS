"""
Utility script to create admin staff member.
Alias wrapper around create_admin.py.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.create_admin import create_admin_user


def create_admin_staff() -> bool:
    """Backward-compatible entry point."""
    return create_admin_user()


if __name__ == "__main__":
    create_admin_staff()

