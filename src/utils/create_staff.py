"""
Utility script to create a staff member linked to admin user
Run this to create a staff record for POS login
"""
import sys
from pathlib import Path
from datetime import date

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.database.models import Staff, User
from loguru import logger


def create_admin_staff():
    """Create staff record linked to admin user"""
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
        
        # Check if staff already exists for this user
        existing_staff = db.query(Staff).filter(Staff.user_id == admin_user.user_id).first()
        if existing_staff:
            print(f"✅ Staff record already exists!")
            print(f"   Staff ID: {existing_staff.staff_id}")
            print(f"   Name: {existing_staff.first_name} {existing_staff.last_name}")
            print(f"   Employee ID: {existing_staff.employee_id}")
            return True
        
        # Create staff record
        staff = Staff(
            employee_id="EMP001",
            first_name="Admin",
            last_name="User",
            email=admin_user.email,
            hire_date=date.today(),
            department="management",
            position="Administrator",
            employment_type="full_time",
            status="active",
            user_id=admin_user.user_id
        )
        
        db.add(staff)
        db.commit()
        db.refresh(staff)
        
        print("✅ Staff record created successfully!")
        print(f"   Staff ID: {staff.staff_id}")
        print(f"   Name: {staff.first_name} {staff.last_name}")
        print(f"   Employee ID: {staff.employee_id}")
        print(f"\n📝 POS Login Credentials:")
        print(f"   Staff ID: {staff.staff_id}")
        print(f"   Password: admin123 (same as admin user)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating staff: {e}")
        db.rollback()
        print(f"❌ Failed to create staff: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_staff()

