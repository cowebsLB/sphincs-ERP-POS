"""
Utility script to create admin staff member
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.database.models import Staff, Role
from src.utils.auth import hash_password
from loguru import logger
from datetime import date


def create_admin_staff():
    """Create admin staff member if it doesn't exist"""
    # Initialize database
    from src.database.connection import get_db_session, DatabaseManager
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    db = get_db_session()
    try:
        # Check if admin role exists
        admin_role = db.query(Role).filter(Role.role_name == 'admin').first()
        if not admin_role:
            print("❌ Admin role not found. Please run create_roles.py first.")
            return False
        
        # Check if admin staff already exists
        existing = db.query(Staff).filter(Staff.username == 'admin').first()
        if existing:
            print("✅ Admin staff member already exists")
            print(f"   Username: {existing.username}")
            print(f"   Staff ID: {existing.staff_id}")
            return True
        
        # Create admin staff
        admin_staff = Staff(
            first_name="Admin",
            last_name="User",
            username="admin",
            password_hash=hash_password("admin"),  # Default password
            role_id=admin_role.role_id,
            email="admin@sphincs.com",
            hire_date=date.today(),
            status="active"
        )
        
        db.add(admin_staff)
        db.commit()
        
        print("✅ Admin staff member created successfully")
        print("   Username: admin")
        print("   Password: admin")
        print("   ⚠️  WARNING: Please change the default password after first login!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating admin staff: {e}")
        db.rollback()
        print(f"❌ Failed to create admin staff: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_staff()

