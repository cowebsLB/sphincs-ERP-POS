"""
Predictive Analytics - Inventory forecasting and demand prediction
"""

from loguru import logger
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
from src.database.connection import get_db_session
from src.database.models import Order, OrderItem, Product, Inventory, Ingredient


class PredictiveAnalytics:
    """Predictive analytics for inventory and sales forecasting"""
    
    def __init__(self):
        self.db = None
    
    def predict_inventory_demand(self, ingredient_id: int, days_ahead: int = 30) -> Dict:
        """
        Predict inventory demand for an ingredient
        
        Args:
            ingredient_id: ID of the ingredient
            days_ahead: Number of days to predict ahead
            
        Returns:
            Dictionary with predictions:
                - predicted_usage: float
                - current_stock: float
                - days_until_out_of_stock: int
                - recommended_order_quantity: float
                - confidence_level: str
        """
        try:
            db = get_db_session()
            
            # Get historical usage (last 90 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            # Get orders with items that use this ingredient
            orders = db.query(Order).filter(
                Order.order_datetime >= start_date,
                Order.order_datetime <= end_date
            ).all()
            
            # Calculate historical usage
            total_usage = 0.0
            usage_by_day = defaultdict(float)
            
            for order in orders:
                order_items = db.query(OrderItem).filter(
                    OrderItem.order_id == order.order_id
                ).all()
                
                for item in order_items:
                    if item.product:
                        # Check if product uses this ingredient (simplified - would need Recipe model)
                        # For now, estimate based on product sales
                        # In real implementation, would check Recipe model
                        total_usage += item.quantity * 0.1  # Placeholder multiplier
                        
                        day_key = order.order_datetime.date()
                        usage_by_day[day_key] += item.quantity * 0.1
            
            # Calculate average daily usage
            if len(usage_by_day) > 0:
                avg_daily_usage = total_usage / len(usage_by_day)
            else:
                avg_daily_usage = 0.0
            
            # Get current stock
            inventory = db.query(Inventory).filter(
                Inventory.ingredient_id == ingredient_id,
                Inventory.status == 'active'
            ).first()
            
            current_stock = inventory.quantity if inventory else 0.0
            
            # Predict future usage
            predicted_usage = avg_daily_usage * days_ahead
            
            # Calculate days until out of stock
            if avg_daily_usage > 0:
                days_until_out = int(current_stock / avg_daily_usage)
            else:
                days_until_out = 999
            
            # Recommended order quantity (with safety buffer)
            safety_buffer = 1.5  # 50% buffer
            recommended_order = max(0, (predicted_usage * safety_buffer) - current_stock)
            
            # Confidence level based on data availability
            if len(usage_by_day) >= 30:
                confidence = "High"
            elif len(usage_by_day) >= 14:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            db.close()
            
            return {
                'predicted_usage': round(predicted_usage, 2),
                'current_stock': round(current_stock, 2),
                'days_until_out_of_stock': days_until_out,
                'recommended_order_quantity': round(recommended_order, 2),
                'confidence_level': confidence,
                'avg_daily_usage': round(avg_daily_usage, 2)
            }
            
        except Exception as e:
            logger.error(f"Error predicting inventory demand: {e}")
            return {
                'predicted_usage': 0.0,
                'current_stock': 0.0,
                'days_until_out_of_stock': 0,
                'recommended_order_quantity': 0.0,
                'confidence_level': "Error",
                'avg_daily_usage': 0.0
            }
    
    def predict_sales_trend(self, product_id: int, days_ahead: int = 30) -> Dict:
        """
        Predict sales trend for a product
        
        Args:
            product_id: ID of the product
            days_ahead: Number of days to predict ahead
            
        Returns:
            Dictionary with predictions:
                - predicted_sales: int
                - predicted_revenue: float
                - trend: str (increasing/decreasing/stable)
                - confidence_level: str
        """
        try:
            db = get_db_session()
            
            # Get historical sales (last 90 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            # Split into periods for trend analysis
            period1_start = start_date
            period1_end = start_date + timedelta(days=45)
            period2_start = period1_end
            period2_end = end_date
            
            # Period 1 sales
            period1_orders = db.query(OrderItem).join(Order).filter(
                OrderItem.product_id == product_id,
                Order.order_datetime >= period1_start,
                Order.order_datetime < period1_end
            ).all()
            period1_qty = sum(item.quantity for item in period1_orders)
            period1_revenue = sum(item.total_price for item in period1_orders)
            
            # Period 2 sales
            period2_orders = db.query(OrderItem).join(Order).filter(
                OrderItem.product_id == product_id,
                Order.order_datetime >= period2_start,
                Order.order_datetime <= period2_end
            ).all()
            period2_qty = sum(item.quantity for item in period2_orders)
            period2_revenue = sum(item.total_price for item in period2_orders)
            
            # Calculate trend
            if period1_qty > 0:
                qty_change = ((period2_qty - period1_qty) / period1_qty) * 100
            else:
                qty_change = 0 if period2_qty == 0 else 100
            
            if abs(qty_change) < 5:
                trend = "Stable"
            elif qty_change > 0:
                trend = "Increasing"
            else:
                trend = "Decreasing"
            
            # Predict future sales (simple linear projection)
            avg_daily_qty = (period1_qty + period2_qty) / 90
            predicted_sales = int(avg_daily_qty * days_ahead)
            
            product = db.query(Product).filter(Product.product_id == product_id).first()
            avg_price = product.price if product else 0.0
            predicted_revenue = predicted_sales * avg_price
            
            # Confidence based on data consistency
            if period1_qty > 0 and period2_qty > 0:
                variance = abs(qty_change)
                if variance < 20:
                    confidence = "High"
                elif variance < 50:
                    confidence = "Medium"
                else:
                    confidence = "Low"
            else:
                confidence = "Low"
            
            db.close()
            
            return {
                'predicted_sales': predicted_sales,
                'predicted_revenue': round(predicted_revenue, 2),
                'trend': trend,
                'trend_percentage': round(qty_change, 1),
                'confidence_level': confidence,
                'avg_daily_sales': round(avg_daily_qty, 2)
            }
            
        except Exception as e:
            logger.error(f"Error predicting sales trend: {e}")
            return {
                'predicted_sales': 0,
                'predicted_revenue': 0.0,
                'trend': "Unknown",
                'trend_percentage': 0.0,
                'confidence_level': "Error",
                'avg_daily_sales': 0.0
            }
    
    def get_low_stock_alerts_predictive(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get predictive low stock alerts
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of dictionaries with alert information
        """
        try:
            db = get_db_session()
            ingredients = db.query(Ingredient).all()
            
            alerts = []
            for ingredient in ingredients:
                prediction = self.predict_inventory_demand(ingredient.ingredient_id, days_ahead)
                
                if prediction['days_until_out_of_stock'] < days_ahead:
                    alerts.append({
                        'ingredient_id': ingredient.ingredient_id,
                        'ingredient_name': ingredient.name,
                        'current_stock': prediction['current_stock'],
                        'predicted_usage': prediction['predicted_usage'],
                        'days_until_out': prediction['days_until_out_of_stock'],
                        'recommended_order': prediction['recommended_order_quantity'],
                        'confidence': prediction['confidence_level']
                    })
            
            db.close()
            return sorted(alerts, key=lambda x: x['days_until_out'])
            
        except Exception as e:
            logger.error(f"Error getting predictive alerts: {e}")
            return []

