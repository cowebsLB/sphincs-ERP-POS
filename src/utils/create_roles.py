"""
Create default roles for the ERP system
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.database.connection import get_db_session
from src.database.models import Role


def create_default_roles():
    """Create all default roles for the ERP system"""
    db = get_db_session()
    
    try:
        # Define all roles organized by category
        roles_data = [
            # System & ERP Admin Roles
            {
                'role_name': 'sysadmin',
                'description': 'System Administrator - Full system access: DB, config, backups, cloud sync, logs. God-mode.',
                'category': 'System & ERP Admin'
            },
            {
                'role_name': 'erp_admin',
                'description': 'ERP Administrator - Manages users, roles, access control, audit logs, system settings.',
                'category': 'System & ERP Admin'
            },
            {
                'role_name': 'it_support',
                'description': 'IT Support / Tech - Can troubleshoot ERP/POS issues, install updates, minor config changes.',
                'category': 'System & ERP Admin'
            },
            
            # Corporate Management Roles
            {
                'role_name': 'general_manager',
                'description': 'General Manager - Whole company oversight: finances, marketing, reports, high-level decisions.',
                'category': 'Corporate Management'
            },
            {
                'role_name': 'finance_manager',
                'description': 'Finance Manager - Reports, payroll, accounting, budgets.',
                'category': 'Corporate Management'
            },
            {
                'role_name': 'marketing_manager',
                'description': 'Marketing Manager - Campaigns, promotions, loyalty programs, social media tracking.',
                'category': 'Corporate Management'
            },
            {
                'role_name': 'hr_manager',
                'description': 'HR Manager - Staff management, recruitment, leave approvals, performance tracking.',
                'category': 'Corporate Management'
            },
            {
                'role_name': 'operations_manager',
                'description': 'Operations Manager / COO - Tracks overall operations efficiency, cross-branch KPIs.',
                'category': 'Corporate Management'
            },
            {
                'role_name': 'regional_manager',
                'description': 'Regional Manager - Watches over a specific region of branches, approves budgets, manages branch managers.',
                'category': 'Corporate Management'
            },
            
            # Branch-Level Management
            {
                'role_name': 'branch_manager',
                'description': 'Branch Manager - Overall branch operations, branch-level reports, staffing, high-level inventory decisions.',
                'category': 'Branch-Level Management'
            },
            {
                'role_name': 'floor_manager',
                'description': 'Floor Manager / Shift Manager - Front-of-house operations: table assignments, wait staff schedules, customer complaints.',
                'category': 'Branch-Level Management'
            },
            {
                'role_name': 'kitchen_manager',
                'description': 'Kitchen Manager / Head Chef - Kitchen operations, recipes, prep schedules, food quality, inventory usage.',
                'category': 'Branch-Level Management'
            },
            {
                'role_name': 'bar_manager',
                'description': 'Bar Manager / Beverage Manager - If you have a bar: drinks, stock, bartenders.',
                'category': 'Branch-Level Management'
            },
            
            # Operational / Staff Roles
            {
                'role_name': 'cashier',
                'description': 'Cashier / POS Operator - Only handles sales transactions, refunds, and receipts.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'chef',
                'description': 'Chef / Cook / Line Cook - Prepares food, updates inventory usage in the ERP.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'prep_cook',
                'description': 'Prep Cook / Kitchen Staff - Prepares ingredients, reports stock usage.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'server',
                'description': 'Server / Waiter / Waitress - Front-of-house, can see table orders and mark served items.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'barista',
                'description': 'Barista / Bartender - Drinks, POS interaction for drinks, can mark inventory usage.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'inventory_clerk',
                'description': 'Inventory Clerk / Storekeeper - Tracks stock, receives deliveries, updates ERP inventory.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'purchasing_officer',
                'description': 'Purchasing Officer / Procurement - Creates purchase orders, manages supplier communication.',
                'category': 'Operational / Staff'
            },
            {
                'role_name': 'cleaner',
                'description': 'Cleaner / Maintenance Staff - Optional, can be tracked for shift scheduling.',
                'category': 'Operational / Staff'
            },
            
            # Specialized / Optional Roles
            {
                'role_name': 'trainer',
                'description': 'Trainer - Can access training modules, onboarding guides, manuals.',
                'category': 'Specialized / Optional'
            },
            {
                'role_name': 'auditor',
                'description': 'Auditor / Inspector - Can view reports, stock, finances, compliance; cannot edit data.',
                'category': 'Specialized / Optional'
            },
            {
                'role_name': 'delivery_driver',
                'description': 'Delivery / Driver - Tracks deliveries, can update delivery status.',
                'category': 'Specialized / Optional'
            },
            {
                'role_name': 'loyalty_operator',
                'description': 'Loyalty / CRM Operator - Handles customer loyalty programs, promotions, marketing tasks.',
                'category': 'Specialized / Optional'
            },
        ]
        
        created_count = 0
        skipped_count = 0
        
        for role_data in roles_data:
            # Check if role already exists
            existing_role = db.query(Role).filter(
                Role.role_name == role_data['role_name']
            ).first()
            
            if existing_role:
                logger.debug(f"Role '{role_data['role_name']}' already exists, skipping")
                skipped_count += 1
                continue
            
            # Create new role
            role = Role(
                role_name=role_data['role_name'],
                permissions={}  # Permissions will be set via Permission model
            )
            db.add(role)
            created_count += 1
            logger.info(f"Created role: {role_data['role_name']} ({role_data['category']})")
        
        db.commit()
        logger.info(f"Role creation complete: {created_count} created, {skipped_count} skipped")
        
        return created_count, skipped_count
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating roles: {e}")
        raise
    finally:
        db.close()


def get_role_categories():
    """Get roles organized by category"""
    db = get_db_session()
    
    try:
        categories = {
            'System & ERP Admin': [],
            'Corporate Management': [],
            'Branch-Level Management': [],
            'Operational / Staff': [],
            'Specialized / Optional': []
        }
        
        # Map role names to categories
        role_category_map = {
            'sysadmin': 'System & ERP Admin',
            'erp_admin': 'System & ERP Admin',
            'it_support': 'System & ERP Admin',
            'general_manager': 'Corporate Management',
            'finance_manager': 'Corporate Management',
            'marketing_manager': 'Corporate Management',
            'hr_manager': 'Corporate Management',
            'operations_manager': 'Corporate Management',
            'regional_manager': 'Corporate Management',
            'branch_manager': 'Branch-Level Management',
            'floor_manager': 'Branch-Level Management',
            'kitchen_manager': 'Branch-Level Management',
            'bar_manager': 'Branch-Level Management',
            'cashier': 'Operational / Staff',
            'chef': 'Operational / Staff',
            'prep_cook': 'Operational / Staff',
            'server': 'Operational / Staff',
            'barista': 'Operational / Staff',
            'inventory_clerk': 'Operational / Staff',
            'purchasing_officer': 'Operational / Staff',
            'cleaner': 'Operational / Staff',
            'trainer': 'Specialized / Optional',
            'auditor': 'Specialized / Optional',
            'delivery_driver': 'Specialized / Optional',
            'loyalty_operator': 'Specialized / Optional',
        }
        
        roles = db.query(Role).all()
        for role in roles:
            category = role_category_map.get(role.role_name, 'Other')
            if category in categories:
                categories[category].append(role)
        
        return categories
        
    finally:
        db.close()


if __name__ == "__main__":
    """Run this script to create all default roles"""
    logger.info("Creating default roles...")
    created, skipped = create_default_roles()
    logger.info(f"Done! Created {created} roles, skipped {skipped} existing roles")
