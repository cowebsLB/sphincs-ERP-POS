"""
Loyalty Points Utility - Award and manage loyalty points
"""

from loguru import logger
from datetime import date
from src.database.connection import get_db_session
from src.database.models import Customer, Order, LoyaltyProgram
from src.utils.notification_center import NotificationCenter


def award_loyalty_points(order_id: int) -> dict:
    """
    Award loyalty points to customer based on order
    
    Args:
        order_id: Order ID
        
    Returns:
        Dictionary with success status and points awarded
    """
    db = get_db_session()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order or not order.customer_id:
            return {'success': False, 'message': 'Order not found or no customer associated'}
        
        # Get active loyalty program
        loyalty_program = db.query(LoyaltyProgram).filter(
            LoyaltyProgram.is_active == True,
            LoyaltyProgram.start_date <= date.today(),
            (LoyaltyProgram.end_date.is_(None)) | (LoyaltyProgram.end_date >= date.today())
        ).first()
        
        if not loyalty_program:
            return {'success': False, 'message': 'No active loyalty program'}
        
        # Calculate points (points_per_currency * order_total)
        points_to_award = int(order.total_amount * loyalty_program.points_per_currency)
        
        if points_to_award <= 0:
            return {'success': False, 'message': 'No points to award for this order'}
        
        # Award points to customer
        customer = db.query(Customer).filter(Customer.customer_id == order.customer_id).first()
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        customer.loyalty_points += points_to_award
        db.commit()
        
        NotificationCenter.instance().emit_notification(
            module="Sales",
            title="Loyalty points awarded",
            message=f"{points_to_award} point(s) awarded to {customer.first_name} {customer.last_name}",
            severity="info",
            source_type="loyalty_order",
            source_id=order_id,
            payload={
                "customer_id": customer.customer_id,
                "points_added": points_to_award,
                "order_id": order_id,
            },
        )
        
        logger.info(f"Awarded {points_to_award} loyalty points to customer {order.customer_id} for order {order_id}")
        
        return {
            'success': True,
            'points_awarded': points_to_award,
            'total_points': customer.loyalty_points,
            'message': f'Awarded {points_to_award} loyalty points'
        }
        
    except Exception as e:
        logger.error(f"Error awarding loyalty points: {e}")
        db.rollback()
        return {'success': False, 'message': f'Error awarding points: {str(e)}'}
    finally:
        db.close()


def get_customer_loyalty_info(customer_id: int) -> dict:
    """
    Get customer loyalty information
    
    Args:
        customer_id: Customer ID
        
    Returns:
        Dictionary with loyalty information
    """
    db = get_db_session()
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        # Get active loyalty program
        loyalty_program = db.query(LoyaltyProgram).filter(
            LoyaltyProgram.is_active == True,
            LoyaltyProgram.start_date <= date.today(),
            (LoyaltyProgram.end_date.is_(None)) | (LoyaltyProgram.end_date >= date.today())
        ).first()
        
        return {
            'success': True,
            'points': customer.loyalty_points,
            'points_per_currency': loyalty_program.points_per_currency if loyalty_program else 0,
            'program_name': loyalty_program.program_name if loyalty_program else None
        }
        
    except Exception as e:
        logger.error(f"Error getting loyalty info: {e}")
        return {'success': False, 'message': f'Error: {str(e)}'}
    finally:
        db.close()

