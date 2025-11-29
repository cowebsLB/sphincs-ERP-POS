"""
Audit Logger - Log all system changes for audit trail
"""

from datetime import datetime
from loguru import logger
from src.database.connection import get_db_session
from src.database.models import AuditLog
from typing import Optional, Dict, Any


def log_audit_event(
    staff_id: Optional[int],
    action: str,
    table_name: str,
    record_id: Optional[int] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """
    Log an audit event
    
    Args:
        staff_id: ID of staff member performing the action
        action: Action type (create, update, delete, login, logout, etc.)
        table_name: Name of the table being modified
        record_id: ID of the record being modified
        old_values: Dictionary of old values (for updates)
        new_values: Dictionary of new values (for creates/updates)
        ip_address: IP address of the user
        user_agent: User agent string
    """
    try:
        db = get_db_session()
        
        audit_log = AuditLog(
            staff_id=staff_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(audit_log)
        db.commit()
        db.close()
        
        logger.debug(f"Audit log created: {action} on {table_name} by staff {staff_id}")
        
    except Exception as e:
        logger.error(f"Error creating audit log: {e}")


def get_client_ip() -> Optional[str]:
    """Get client IP address (simplified - would need request context in web app)"""
    # For desktop app, return None or get from system
    return None


def get_user_agent() -> Optional[str]:
    """Get user agent string"""
    # For desktop app, return application identifier
    return "Sphincs ERP Desktop Client"

