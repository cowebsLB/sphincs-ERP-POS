"""
Online Ordering Platforms Integration - UberEats, DoorDash, etc.
"""

from loguru import logger
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class OrderingPlatform(Enum):
    """Supported online ordering platforms"""
    UBER_EATS = "ubereats"
    DOORDASH = "doordash"
    GRUBHUB = "grubhub"
    POSTMATES = "postmates"
    CUSTOM = "custom"


class OnlineOrderingIntegration:
    """Integration with online ordering platforms"""
    
    def __init__(self, platform: OrderingPlatform):
        self.platform = platform
        self.api_key = None
        self.api_secret = None
        self.restaurant_id = None
        self.is_configured = False
    
    def configure(self, api_key: str, api_secret: str, restaurant_id: str):
        """
        Configure platform integration
        
        Args:
            api_key: Platform API key
            api_secret: Platform API secret
            restaurant_id: Restaurant ID on the platform
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.restaurant_id = restaurant_id
        self.is_configured = True
        logger.info(f"{self.platform.value} integration configured")
    
    def fetch_orders(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[Dict]:
        """
        Fetch orders from the platform
        
        Args:
            start_time: Start time for order fetch
            end_time: End time for order fetch
            
        Returns:
            List of order dictionaries
        """
        if not self.is_configured:
            logger.warning(f"{self.platform.value} not configured")
            return []
        
        try:
            # In real implementation, would call platform API
            # Example for UberEats:
            # import requests
            # headers = {
            #     'Authorization': f'Bearer {self.api_key}',
            #     'Content-Type': 'application/json'
            # }
            # response = requests.get(
            #     f'https://api.ubereats.com/v1/orders',
            #     headers=headers,
            #     params={
            #         'restaurant_id': self.restaurant_id,
            #         'start_time': start_time.isoformat() if start_time else None,
            #         'end_time': end_time.isoformat() if end_time else None
            #     }
            # )
            # return response.json()['orders']
            
            logger.info(f"Fetching orders from {self.platform.value}")
            return []  # Simulated - would return actual orders
            
        except Exception as e:
            logger.error(f"Error fetching orders from {self.platform.value}: {e}")
            return []
    
    def import_order(self, platform_order: Dict) -> Optional[int]:
        """
        Import an order from the platform into the local system
        
        Args:
            platform_order: Order data from platform
            
        Returns:
            Local order ID if successful, None otherwise
        """
        try:
            from src.database.connection import get_db_session
            from src.database.models import Order, OrderItem, Product, Customer
            
            db = get_db_session()
            
            # Map platform order to local order format
            # This would vary by platform
            customer_name = platform_order.get('customer_name', 'Online Order')
            customer_phone = platform_order.get('customer_phone')
            customer_email = platform_order.get('customer_email')
            
            # Find or create customer
            customer = None
            if customer_phone:
                customer = db.query(Customer).filter(Customer.phone == customer_phone).first()
            
            if not customer:
                customer = Customer(
                    first_name=customer_name.split()[0] if customer_name else "Online",
                    last_name=" ".join(customer_name.split()[1:]) if len(customer_name.split()) > 1 else "Customer",
                    phone=customer_phone,
                    email=customer_email,
                    status='active'
                )
                db.add(customer)
                db.flush()
            
            # Create order
            order = Order(
                customer_id=customer.customer_id,
                staff_id=1,  # System user
                order_type='delivery',
                order_status='pending',
                order_datetime=datetime.now(),
                total_amount=platform_order.get('total_amount', 0.0),
                payment_method='online'
            )
            db.add(order)
            db.flush()
            
            # Add order items
            for item in platform_order.get('items', []):
                product_name = item.get('name')
                product = db.query(Product).filter(Product.name == product_name).first()
                
                if product:
                    order_item = OrderItem(
                        order_id=order.order_id,
                        product_id=product.product_id,
                        quantity=item.get('quantity', 1),
                        unit_price=item.get('price', 0.0),
                        total_price=item.get('price', 0.0) * item.get('quantity', 1)
                    )
                    db.add(order_item)
            
            db.commit()
            order_id = order.order_id
            db.close()
            
            logger.info(f"Imported order {order_id} from {self.platform.value}")
            return order_id
            
        except Exception as e:
            logger.error(f"Error importing order: {e}")
            return None
    
    def update_order_status(self, platform_order_id: str, status: str) -> bool:
        """
        Update order status on the platform
        
        Args:
            platform_order_id: Order ID on the platform
            status: New status (preparing, ready, completed, etc.)
            
        Returns:
            True if successful
        """
        if not self.is_configured:
            return False
        
        try:
            # In real implementation, would call platform API to update status
            logger.info(f"Updating order {platform_order_id} status to {status} on {self.platform.value}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False
    
    def sync_menu(self, products: List[Dict]) -> bool:
        """
        Sync menu/products to the platform
        
        Args:
            products: List of product dictionaries
            
        Returns:
            True if successful
        """
        if not self.is_configured:
            return False
        
        try:
            # In real implementation, would call platform API to update menu
            logger.info(f"Syncing {len(products)} products to {self.platform.value}")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing menu: {e}")
            return False


def get_ordering_integration(platform: OrderingPlatform) -> OnlineOrderingIntegration:
    """
    Get ordering platform integration instance
    
    Args:
        platform: Ordering platform
        
    Returns:
        OnlineOrderingIntegration instance
    """
    return OnlineOrderingIntegration(platform)

