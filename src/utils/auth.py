"""
Authentication and password management
"""
import bcrypt
from sqlalchemy.orm import Session
from typing import Optional
from loguru import logger
from src.database.models import Staff, Role
from src.database.connection import get_db_session


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    # Encode password to bytes
    password_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string (decode from bytes)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    try:
        # Encode both to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        # Verify password
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a staff member by username and password
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        Dictionary with staff/user data if authenticated, None otherwise
    """
    db = get_db_session()
    try:
        staff = db.query(Staff).filter(Staff.username == username).first()
        
        if not staff:
            logger.warning(f"Authentication failed: User '{username}' not found")
            return None
        
        if staff.status != 'active':
            logger.warning(f"Authentication failed: User '{username}' is not active (status: {staff.status})")
            return None
        
        if not verify_password(password, staff.password_hash):
            logger.warning(f"Authentication failed: Invalid password for user '{username}'")
            return None
        
        # Get role name
        role_name = "staff"  # default
        if staff.role:
            role_name = staff.role.role_name
        
        # Access all attributes while session is open
        user_data = {
            'user_id': staff.staff_id,  # Use staff_id as user_id for compatibility
            'staff_id': staff.staff_id,
            'username': staff.username,
            'email': staff.email,
            'role': role_name,
            'role_id': staff.role_id,
            'first_name': staff.first_name,
            'last_name': staff.last_name,
            'is_active': staff.status == 'active',
            'created_at': staff.created_at
        }
        
        logger.info(f"User '{username}' authenticated successfully")
        return user_data
        
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def authenticate_staff_by_id(staff_id: int, password: str) -> Optional[dict]:
    """
    Authenticate staff by staff ID number and password
    
    Args:
        staff_id: Staff ID number (integer)
        password: Plain text password
        
    Returns:
        Dictionary with staff data if authenticated, None otherwise
    """
    db = get_db_session()
    try:
        # Find staff by staff_id
        staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        
        if not staff:
            logger.warning(f"Authentication failed: Staff ID '{staff_id}' not found")
            return None
        
        if staff.status != 'active':
            logger.warning(f"Authentication failed: Staff ID '{staff_id}' is not active (status: {staff.status})")
            return None
        
        # Verify password
        if not verify_password(password, staff.password_hash):
            logger.warning(f"Authentication failed: Invalid password for staff ID '{staff_id}'")
            return None
        
        # Get role name
        role_name = "staff"  # default
        if staff.role:
            role_name = staff.role.role_name
        
        # Access all attributes while session is open
        staff_data = {
            'staff_id': staff.staff_id,
            'first_name': staff.first_name,
            'last_name': staff.last_name,
            'username': staff.username,
            'email': staff.email,
            'phone': staff.phone,
            'user_id': staff.staff_id,  # Use staff_id as user_id for compatibility
            'role': role_name,
            'role_id': staff.role_id,
            'is_active': staff.status == 'active'
        }
        
        logger.info(f"Staff ID '{staff_id}' authenticated successfully")
        return staff_data
        
    except Exception as e:
        logger.error(f"Error during staff authentication: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def create_staff(username: str, password: str, email: Optional[str] = None, 
                 role_id: int = None, first_name: str = "User", 
                 last_name: str = "Account", is_active: bool = True) -> Optional[Staff]:
    """
    Create a new staff account
    
    Args:
        username: Username
        password: Plain text password
        email: Email address (optional)
        role_id: Role ID (if None, will use first available role)
        first_name: First name
        last_name: Last name
        is_active: Whether staff is active
        
    Returns:
        Created Staff object or None if creation failed
    """
    db = get_db_session()
    try:
        # Check if username already exists
        existing = db.query(Staff).filter(Staff.username == username).first()
        if existing:
            logger.warning(f"Staff creation failed: Username '{username}' already exists")
            return None
        
        # Get role_id if not provided
        if role_id is None:
            role = db.query(Role).first()
            if not role:
                logger.error("No roles found. Please create roles first.")
                return None
            role_id = role.role_id
        
        # Create new staff
        from datetime import date
        staff = Staff(
            username=username,
            password_hash=hash_password(password),
            email=email,
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            hire_date=date.today(),
            status="active" if is_active else "inactive"
        )
        
        db.add(staff)
        db.commit()
        db.refresh(staff)
        
        logger.info(f"Staff '{username}' created successfully")
        return staff
        
    except Exception as e:
        logger.error(f"Error creating staff: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def get_staff_by_id(staff_id: int) -> Optional[Staff]:
    """Get staff by ID"""
    db = get_db_session()
    try:
        return db.query(Staff).filter(Staff.staff_id == staff_id).first()
    finally:
        db.close()

