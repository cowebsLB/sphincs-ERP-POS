"""
Utility script to update admin user password to numeric PIN
Run this to set a numeric PIN for POS login
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.database.models import User
from src.utils.auth import hash_password
from loguru import logger


def update_admin_pin(new_pin: str = "1234"):
    """Update admin user password to numeric PIN"""
    # Initialize database
    db_manager = get_db_manager()
    db_manager.create_tables()
    
    db = db_manager.get_session()
    try:
        # Get admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("❌ Admin user not found. Please run create_admin.py first.")
            return False
        
        # Validate PIN is numeric
        if not new_pin.isdigit():
            print(f"❌ PIN must be numeric only. '{new_pin}' is not valid.")
            return False
        
        # Update password
        admin_user.password_hash = hash_password(new_pin)
        db.commit()
        
        print("✅ Admin PIN updated successfully!")
        print(f"   Username: admin")
        print(f"   PIN: {new_pin}")
        print(f"\n📝 POS Login Credentials:")
        print(f"   Staff ID: 1")
        print(f"   PIN: {new_pin}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating admin PIN: {e}")
        db.rollback()
        print(f"❌ Failed to update admin PIN: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    pin = sys.argv[1] if len(sys.argv) > 1 else "1234"
    update_admin_pin(pin)

