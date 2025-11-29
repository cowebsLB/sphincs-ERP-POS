"""
Procurement Automation - Auto-generate purchase orders when stock hits threshold
"""

from loguru import logger
from datetime import date
from src.database.connection import get_db_session
from src.database.models import Inventory, Ingredient, PurchaseOrder, POItem, Supplier, Staff


def check_and_generate_pos(user_id: int) -> list:
    """
    Check inventory levels and auto-generate purchase orders for items below reorder level
    
    Args:
        user_id: ID of staff member creating the POs
        
    Returns:
        List of created purchase order IDs
    """
    try:
        db = get_db_session()
        created_pos = []
        
        # Find inventory items below reorder level
        low_stock_items = db.query(Inventory).filter(
            Inventory.quantity <= Inventory.reorder_level,
            Inventory.status == 'active'
        ).all()
        
        if not low_stock_items:
            db.close()
            return []
        
        # Group by supplier
        supplier_items = {}
        for item in low_stock_items:
            ingredient = item.ingredient
            supplier_id = ingredient.supplier_id if ingredient.supplier_id else None
            
            if supplier_id:
                if supplier_id not in supplier_items:
                    supplier_items[supplier_id] = []
                supplier_items[supplier_id].append(item)
        
        # Create purchase orders for each supplier
        for supplier_id, items in supplier_items.items():
            supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
            if not supplier or supplier.status != 'active':
                continue
            
            # Create PO
            po = PurchaseOrder(
                supplier_id=supplier_id,
                staff_id=user_id,
                order_date=date.today(),
                status='pending'
            )
            db.add(po)
            db.flush()  # Get PO ID
            
            # Add items to PO
            for item in items:
                # Calculate quantity needed (reorder level * 2 as default)
                quantity_needed = item.reorder_level * 2
                
                # Get current cost per unit
                unit_price = item.ingredient.cost_per_unit or 0.0
                
                po_item = POItem(
                    po_id=po.po_id,
                    ingredient_id=item.ingredient_id,
                    quantity=quantity_needed,
                    unit_price=unit_price
                )
                db.add(po_item)
            
            created_pos.append(po.po_id)
            logger.info(f"Auto-generated PO #{po.po_id} for supplier {supplier.name}")
        
        db.commit()
        db.close()
        
        return created_pos
        
    except Exception as e:
        logger.error(f"Error auto-generating POs: {e}")
        db.rollback()
        db.close()
        return []


def get_low_stock_items() -> list:
    """
    Get list of inventory items that are below reorder level
    
    Returns:
        List of inventory items with low stock
    """
    try:
        db = get_db_session()
        low_stock = db.query(Inventory).filter(
            Inventory.quantity <= Inventory.reorder_level,
            Inventory.status == 'active'
        ).all()
        
        result = []
        for item in low_stock:
            result.append({
                'inventory_id': item.inventory_id,
                'ingredient_name': item.ingredient.name,
                'current_quantity': item.quantity,
                'reorder_level': item.reorder_level,
                'unit': item.unit,
                'supplier': item.ingredient.supplier.name if item.ingredient.supplier else None
            })
        
        db.close()
        return result
        
    except Exception as e:
        logger.error(f"Error getting low stock items: {e}")
        return []

