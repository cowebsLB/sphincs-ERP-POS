"""
Receipt Printing Utility - Generate and print receipts
"""

from loguru import logger
from datetime import datetime
from typing import Optional
from src.database.connection import get_db_session
from src.database.models import Order, OrderItem, Product, Staff, Customer


def generate_receipt_text(order_id: int) -> str:
    """
    Generate receipt text for an order
    
    Args:
        order_id: Order ID
        
    Returns:
        Receipt text as string
    """
    db = get_db_session()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return f"Order {order_id} not found"
        
        # Build receipt
        receipt_lines = []
        receipt_lines.append("=" * 50)
        receipt_lines.append("SPHINCS ERP+POS")
        receipt_lines.append("=" * 50)
        receipt_lines.append(f"Order #: {order.order_id}")
        receipt_lines.append(f"Date: {order.order_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if order.staff:
            receipt_lines.append(f"Staff: {order.staff.first_name} {order.staff.last_name}")
        
        if order.customer:
            receipt_lines.append(f"Customer: {order.customer.first_name} {order.customer.last_name}")
        
        if order.table_number:
            receipt_lines.append(f"Table: {order.table_number}")
        
        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Item':<25} {'Qty':>5} {'Price':>10} {'Total':>10}")
        receipt_lines.append("-" * 50)
        
        # Order items
        items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        subtotal = 0.0
        
        for item in items:
            product_name = item.product.name if item.product else "Unknown"
            qty = item.quantity
            unit_price = float(item.unit_price)
            total_price = float(item.total_price)
            subtotal += total_price
            
            # Truncate long names
            if len(product_name) > 23:
                product_name = product_name[:20] + "..."
            
            receipt_lines.append(
                f"{product_name:<25} {qty:>5} ${unit_price:>9.2f} ${total_price:>9.2f}"
            )
        
        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Subtotal:':<40} ${subtotal:>9.2f}")
        
        # Tax (assuming 10%)
        tax = subtotal * 0.10
        receipt_lines.append(f"{'Tax (10%):':<40} ${tax:>9.2f}")
        
        total = subtotal + tax
        receipt_lines.append(f"{'TOTAL:':<40} ${total:>9.2f}")
        
        if order.payment_method:
            receipt_lines.append(f"Payment: {order.payment_method.upper()}")
        
        receipt_lines.append("=" * 50)
        receipt_lines.append("Thank you for your business!")
        receipt_lines.append("=" * 50)
        
        return "\n".join(receipt_lines)
        
    except Exception as e:
        logger.error(f"Error generating receipt: {e}")
        return f"Error generating receipt: {str(e)}"
    finally:
        db.close()


def print_receipt(order_id: int, printer_name: Optional[str] = None) -> bool:
    """
    Print receipt to printer or file
    
    Args:
        order_id: Order ID
        printer_name: Optional printer name (if None, saves to file)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        receipt_text = generate_receipt_text(order_id)
        
        if printer_name:
            # TODO: Implement actual printer integration
            # For now, just log
            logger.info(f"Printing receipt for order {order_id} to {printer_name}")
            logger.debug(f"Receipt content:\n{receipt_text}")
            return True
        else:
            # Save to file
            from pathlib import Path
            receipts_dir = Path.home() / "Documents" / "Sphincs Receipts"
            receipts_dir.mkdir(parents=True, exist_ok=True)
            
            receipt_file = receipts_dir / f"receipt_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            receipt_file.write_text(receipt_text, encoding='utf-8')
            
            logger.info(f"Receipt saved to: {receipt_file}")
            return True
            
    except Exception as e:
        logger.error(f"Error printing receipt: {e}")
        return False

