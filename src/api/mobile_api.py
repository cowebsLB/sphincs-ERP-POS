"""
Mobile Companion App API - REST API for mobile app integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
from loguru import logger
from datetime import datetime, date
from typing import Dict, List, Optional
from src.database.connection import get_db_session
from src.database.models import (
    Order, OrderItem, Product, Staff, Customer, Inventory, Ingredient,
    Attendance, ShiftSchedule, Location, Notification
)
from src.utils.notification_preferences import filter_notifications_for_user
from src.utils.notification_center import NotificationCenter


class MobileAPI:
    """REST API for mobile companion app"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for mobile apps
        self.api_key = None  # For API authentication
        self.setup_routes()
    
    def require_auth(self, f):
        """Decorator for API key authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.api_key:
                provided_key = request.headers.get('X-API-Key')
                if not provided_key or provided_key != self.api_key:
                    return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return decorated_function
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/mobile/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})
        
        @self.app.route('/api/mobile/orders', methods=['GET'])
        def get_orders():
            """Get recent orders"""
            try:
                limit = request.args.get('limit', 50, type=int)
                status = request.args.get('status', None)
                
                db = get_db_session()
                query = db.query(Order).order_by(Order.order_datetime.desc())
                
                if status:
                    query = query.filter(Order.order_status == status)
                
                orders = query.limit(limit).all()
                
                orders_data = [{
                    'order_id': order.order_id,
                    'order_number': f"ORD{order.order_id:06d}",
                    'customer_name': f"{order.customer.first_name} {order.customer.last_name}" if order.customer else "Walk-in",
                    'total_amount': order.total_amount,
                    'status': order.order_status,
                    'order_type': order.order_type,
                    'datetime': order.order_datetime.isoformat(),
                    'items': [{
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.unit_price
                    } for item in order.order_items]
                } for order in orders]
                
                db.close()
                return jsonify({'success': True, 'orders': orders_data})
                
            except Exception as e:
                logger.error(f"Error fetching orders: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/orders/<int:order_id>', methods=['GET'])
        def get_order(order_id):
            """Get specific order details"""
            try:
                db = get_db_session()
                order = db.query(Order).filter(Order.order_id == order_id).first()
                
                if not order:
                    return jsonify({'success': False, 'error': 'Order not found'}), 404
                
                order_data = {
                    'order_id': order.order_id,
                    'order_number': f"ORD{order.order_id:06d}",
                    'customer': {
                        'name': f"{order.customer.first_name} {order.customer.last_name}" if order.customer else "Walk-in",
                        'phone': order.customer.phone if order.customer else None,
                        'email': order.customer.email if order.customer else None
                    },
                    'total_amount': order.total_amount,
                    'status': order.order_status,
                    'order_type': order.order_type,
                    'table_number': order.table_number,
                    'datetime': order.order_datetime.isoformat(),
                    'payment_method': order.payment_method,
                    'items': [{
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'unit_price': item.unit_price,
                        'total_price': item.total_price
                    } for item in order.order_items]
                }
                
                db.close()
                return jsonify({'success': True, 'order': order_data})
                
            except Exception as e:
                logger.error(f"Error fetching order: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/orders/<int:order_id>/status', methods=['PUT'])
        def update_order_status(order_id):
            """Update order status"""
            try:
                data = request.get_json()
                new_status = data.get('status')
                
                if not new_status:
                    return jsonify({'success': False, 'error': 'Status is required'}), 400
                
                db = get_db_session()
                order = db.query(Order).filter(Order.order_id == order_id).first()
                
                if not order:
                    return jsonify({'success': False, 'error': 'Order not found'}), 404
                
                order.order_status = new_status
                db.commit()
                db.close()
                
                return jsonify({'success': True, 'message': 'Order status updated'})
                
            except Exception as e:
                logger.error(f"Error updating order status: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/products', methods=['GET'])
        def get_products():
            """Get products/menu items"""
            try:
                category = request.args.get('category', None)
                active_only = request.args.get('active_only', 'true').lower() == 'true'
                
                db = get_db_session()
                query = db.query(Product)
                
                if active_only:
                    query = query.filter(Product.is_active == True)
                
                if category:
                    query = query.join(Product.category).filter(Product.category.has(name=category))
                
                products = query.all()
                
                products_data = [{
                    'product_id': product.product_id,
                    'name': product.name,
                    'category': product.category.name if product.category else None,
                    'price': product.price,
                    'description': product.description,
                    'image_url': product.image_url
                } for product in products]
                
                db.close()
                return jsonify({'success': True, 'products': products_data})
                
            except Exception as e:
                logger.error(f"Error fetching products: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/dashboard', methods=['GET'])
        def get_dashboard():
            """Get dashboard statistics"""
            try:
                from src.utils.dashboard_analytics import (
                    get_today_sales, get_today_orders,
                    get_active_staff_count, get_inventory_alerts
                )
                
                today_sales = get_today_sales()
                today_orders = get_today_orders()
                active_staff, total_staff = get_active_staff_count()
                alerts = get_inventory_alerts()
                
                dashboard_data = {
                    'today_sales': today_sales,
                    'today_orders': today_orders,
                    'active_staff': active_staff,
                    'total_staff': total_staff,
                    'inventory_alerts': alerts,
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify({'success': True, 'dashboard': dashboard_data})
                
            except Exception as e:
                logger.error(f"Error fetching dashboard: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/inventory/alerts', methods=['GET'])
        def get_inventory_alerts():
            """Get inventory alerts"""
            try:
                db = get_db_session()
                from src.database.models import Inventory
                
                # Get low stock items
                low_stock = db.query(Inventory).filter(
                    Inventory.quantity <= Inventory.reorder_level,
                    Inventory.status == 'active'
                ).all()
                
                alerts_data = [{
                    'ingredient_id': inv.ingredient_id,
                    'ingredient_name': inv.ingredient.name,
                    'current_stock': inv.quantity,
                    'reorder_level': inv.reorder_level,
                    'unit': inv.unit
                } for inv in low_stock]
                
                db.close()
                return jsonify({'success': True, 'alerts': alerts_data})
                
            except Exception as e:
                logger.error(f"Error fetching inventory alerts: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/notifications', methods=['GET'])
        def get_notifications_feed():
            """Return notifications filtered by user preferences."""
            try:
                staff_id = request.args.get('staff_id', type=int)
                if not staff_id:
                    return jsonify({'success': False, 'error': 'staff_id is required'}), 400
                limit = request.args.get('limit', 50, type=int)
                since = request.args.get('since')
                
                db = get_db_session()
                query = db.query(Notification).order_by(Notification.triggered_at.desc())
                if since:
                    try:
                        since_dt = datetime.fromisoformat(since)
                        query = query.filter(Notification.triggered_at >= since_dt)
                    except ValueError:
                        pass
                records = query.limit(limit).all()
                notifications = [{
                    'id': record.notification_id,
                    'module': record.module,
                    'title': record.title,
                    'message': record.message,
                    'severity': record.severity,
                    'triggered_at': record.triggered_at.isoformat() if record.triggered_at else None,
                    'is_read': record.is_read,
                } for record in records]
                db.close()
                
                filtered = filter_notifications_for_user(
                    notifications,
                    staff_id,
                    target="mobile",
                )
                unread_count = sum(1 for item in filtered if not item.get('is_read'))
                return jsonify({'success': True, 'notifications': filtered, 'unread': unread_count})
            except Exception as e:
                logger.error(f"Error fetching notifications: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/notifications/read', methods=['POST'])
        def acknowledge_notifications():
            """Mark notifications as read."""
            try:
                data = request.get_json() or {}
                ids = data.get('ids', [])
                if not ids:
                    return jsonify({'success': False, 'error': 'ids list required'}), 400
                db = get_db_session()
                updated = (
                    db.query(Notification)
                    .filter(Notification.notification_id.in_(ids))
                    .update(
                        {
                            Notification.is_read: True,
                            Notification.read_at: datetime.utcnow(),
                        },
                        synchronize_session=False,
                    )
                )
                db.commit()
                db.close()
                NotificationCenter.instance().notification_updated.emit({"refresh": True})
                return jsonify({'success': True, 'updated': updated})
            except Exception as e:
                logger.error(f"Error marking notifications read: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/staff/clock-in', methods=['POST'])
        def clock_in():
            """Staff clock in"""
            try:
                data = request.get_json()
                staff_id = data.get('staff_id')
                
                if not staff_id:
                    return jsonify({'success': False, 'error': 'Staff ID is required'}), 400
                
                from src.database.models import Attendance
                db = get_db_session()
                
                today = datetime.now().date()
                attendance = db.query(Attendance).filter(
                    Attendance.staff_id == staff_id,
                    Attendance.attendance_date == today
                ).first()
                
                if attendance and attendance.clock_in:
                    return jsonify({'success': False, 'error': 'Already clocked in today'}), 400
                
                if not attendance:
                    attendance = Attendance(
                        staff_id=staff_id,
                        attendance_date=today,
                        clock_in=datetime.now().time(),
                        status='present'
                    )
                    db.add(attendance)
                else:
                    attendance.clock_in = datetime.now().time()
                    attendance.status = 'present'
                
                db.commit()
                db.close()
                
                return jsonify({'success': True, 'message': 'Clocked in successfully'})
                
            except Exception as e:
                logger.error(f"Error clocking in: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/mobile/staff/clock-out', methods=['POST'])
        def clock_out():
            """Staff clock out"""
            try:
                data = request.get_json()
                staff_id = data.get('staff_id')
                
                if not staff_id:
                    return jsonify({'success': False, 'error': 'Staff ID is required'}), 400
                
                from src.database.models import Attendance
                from datetime import timedelta
                db = get_db_session()
                
                today = datetime.now().date()
                attendance = db.query(Attendance).filter(
                    Attendance.staff_id == staff_id,
                    Attendance.attendance_date == today
                ).first()
                
                if not attendance or not attendance.clock_in:
                    return jsonify({'success': False, 'error': 'Not clocked in'}), 400
                
                if attendance.clock_out:
                    return jsonify({'success': False, 'error': 'Already clocked out today'}), 400
                
                clock_out_time = datetime.now().time()
                attendance.clock_out = clock_out_time
                
                # Calculate total hours
                clock_in_dt = datetime.combine(today, attendance.clock_in)
                clock_out_dt = datetime.combine(today, clock_out_time)
                total_hours = (clock_out_dt - clock_in_dt).total_seconds() / 3600
                attendance.total_hours = total_hours
                
                db.commit()
                db.close()
                
                return jsonify({
                    'success': True,
                    'message': 'Clocked out successfully',
                    'total_hours': total_hours
                })
                
            except Exception as e:
                logger.error(f"Error clocking out: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the API server"""
        logger.info(f"Starting Mobile API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def get_mobile_api() -> MobileAPI:
    """Get mobile API instance"""
    return MobileAPI()

