"""
Utility script to create an admin staff account.
Run this once to bootstrap login access.
"""
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.database.models import Role, Staff
from src.utils.auth import create_staff
from src.utils.create_roles import create_default_roles


def _resolve_admin_role_id(db) -> Optional[int]:
    """Return an admin-capable role id if available."""
    role = (
        db.query(Role)
        .filter(Role.role_name.in_(["admin", "sysadmin", "erp_admin"]))
        .order_by(Role.role_name.asc())
        .first()
    )
    return role.role_id if role else None


def create_admin_user() -> bool:
    """Create default admin account if it does not exist."""
    db_manager = get_db_manager()
    db_manager.create_tables()

    db = db_manager.get_session()
    try:
        existing = db.query(Staff).filter(Staff.username == "admin").first()
        if existing:
            print("Admin account already exists.")
            print(f"Username: {existing.username}")
            print(f"Staff ID: {existing.staff_id}")
            return True

        role_id = _resolve_admin_role_id(db)
    finally:
        db.close()

    if role_id is None:
        create_default_roles()
        db = db_manager.get_session()
        try:
            role_id = _resolve_admin_role_id(db)
        finally:
            db.close()

    if role_id is None:
        print("Failed to find or create an admin-capable role.")
        return False

    admin = create_staff(
        username="admin",
        password="admin123",
        email="admin@sphincs.local",
        role_id=role_id,
        first_name="Admin",
        last_name="User",
        is_active=True,
    )

    if not admin:
        print("Failed to create admin account.")
        return False

    print("Admin account created successfully.")
    print("Username: admin")
    print("Password: admin123")
    print("WARNING: Change the default password after first login.")
    return True


if __name__ == "__main__":
    create_admin_user()

