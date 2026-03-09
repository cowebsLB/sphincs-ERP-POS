"""
Utility script to create a default POS staff account.
Run this to provision a cashier login quickly.
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


def _resolve_cashier_role_id(db) -> Optional[int]:
    """Return a role id suitable for POS login."""
    role = (
        db.query(Role)
        .filter(Role.role_name.in_(["cashier", "server", "erp_admin"]))
        .order_by(Role.role_name.asc())
        .first()
    )
    return role.role_id if role else None


def create_default_staff() -> bool:
    """Create default cashier account if missing."""
    db_manager = get_db_manager()
    db_manager.create_tables()

    db = db_manager.get_session()
    try:
        existing = db.query(Staff).filter(Staff.username == "cashier").first()
        if existing:
            print("Cashier account already exists.")
            print(f"Username: {existing.username}")
            print(f"Staff ID: {existing.staff_id}")
            return True

        role_id = _resolve_cashier_role_id(db)
    finally:
        db.close()

    if role_id is None:
        create_default_roles()
        db = db_manager.get_session()
        try:
            role_id = _resolve_cashier_role_id(db)
        finally:
            db.close()

    if role_id is None:
        print("Failed to find or create a POS-compatible role.")
        return False

    staff = create_staff(
        username="cashier",
        password="cashier123",
        email="cashier@sphincs.local",
        role_id=role_id,
        first_name="POS",
        last_name="Cashier",
        is_active=True,
    )

    if not staff:
        print("Failed to create cashier account.")
        return False

    print("Cashier account created successfully.")
    print("Username: cashier")
    print("Password: cashier123")
    print("WARNING: Change the default password after first login.")
    return True


if __name__ == "__main__":
    create_default_staff()

