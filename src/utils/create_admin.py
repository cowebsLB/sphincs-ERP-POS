"""
Utility script to create admin user
Run this once to create the initial admin account
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.utils.auth import create_user
from loguru import logger


def create_admin_user():
    """Create default admin user"""
    # Initialize database
    db_manager = get_db_manager()
    db_manager.create_tables()
    
    # Create admin user
    admin = create_user(
        username="admin",
        password="admin123",  # Change this in production!
        email="admin@sphincs.local",
        role="admin",
        is_active=True
    )
    
    if admin:
        print("✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print("\n⚠️  WARNING: Change the default password in production!")
        return True
    else:
        print("❌ Failed to create admin user (may already exist)")
        return False


if __name__ == "__main__":
    create_admin_user()

