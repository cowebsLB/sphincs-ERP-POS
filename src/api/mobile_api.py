"""
Mobile Companion App API - REST API for mobile app integration.
"""

from datetime import datetime, timezone
from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS
from loguru import logger

from src.database.connection import get_db_session
from src.database.models import Attendance, Inventory, Notification, Order, Product
from src.utils.notification_center import NotificationCenter
from src.utils.notification_preferences import filter_notifications_for_user


def _utc_now_naive() -> datetime:
    """Return current UTC timestamp as naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class MobileAPI:
    """REST API for mobile companion app."""

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api_key = None
        self.setup_routes()

    @staticmethod
    def _error(message: str, status: int = 400):
        return jsonify({"success": False, "error": message}), status

    def _internal_error(self, context: str, exc: Exception):
        logger.exception(f"{context}: {exc}")
        return self._error("Internal server error", 500)

    def require_auth(self, f):
        """Decorator for API key authentication."""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.api_key:
                provided_key = request.headers.get("X-API-Key")
                if not provided_key or provided_key != self.api_key:
                    return self._error("Unauthorized", 401)
            return f(*args, **kwargs)

        return decorated_function

    def setup_routes(self):
        """Setup API routes."""

        @self.app.route("/api/mobile/health", methods=["GET"])
        def health_check():
            return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

        @self.app.route("/api/mobile/orders", methods=["GET"])
        @self.require_auth
        def get_orders():
            try:
                limit = request.args.get("limit", 50, type=int)
                limit = max(1, min(limit, 200))
                status = request.args.get("status")

                with get_db_session() as db:
                    query = db.query(Order).order_by(Order.order_datetime.desc())
                    if status:
                        query = query.filter(Order.order_status == status)
                    orders = query.limit(limit).all()

                    orders_data = [
                        {
                            "order_id": order.order_id,
                            "order_number": f"ORD{order.order_id:06d}",
                            "customer_name": (
                                f"{order.customer.first_name} {order.customer.last_name}"
                                if order.customer
                                else "Walk-in"
                            ),
                            "total_amount": order.total_amount,
                            "status": order.order_status,
                            "order_type": order.order_type,
                            "datetime": order.order_datetime.isoformat(),
                            "items": [
                                {
                                    "product_name": item.product.name,
                                    "quantity": item.quantity,
                                    "price": item.unit_price,
                                }
                                for item in order.order_items
                            ],
                        }
                        for order in orders
                    ]

                return jsonify({"success": True, "orders": orders_data})
            except Exception as exc:
                return self._internal_error("Error fetching orders", exc)

        @self.app.route("/api/mobile/orders/<int:order_id>", methods=["GET"])
        @self.require_auth
        def get_order(order_id):
            try:
                with get_db_session() as db:
                    order = db.query(Order).filter(Order.order_id == order_id).first()
                    if not order:
                        return self._error("Order not found", 404)

                    order_data = {
                        "order_id": order.order_id,
                        "order_number": f"ORD{order.order_id:06d}",
                        "customer": {
                            "name": (
                                f"{order.customer.first_name} {order.customer.last_name}"
                                if order.customer
                                else "Walk-in"
                            ),
                            "phone": order.customer.phone if order.customer else None,
                            "email": order.customer.email if order.customer else None,
                        },
                        "total_amount": order.total_amount,
                        "status": order.order_status,
                        "order_type": order.order_type,
                        "table_number": order.table_number,
                        "datetime": order.order_datetime.isoformat(),
                        "payment_method": order.payment_method,
                        "items": [
                            {
                                "product_name": item.product.name,
                                "quantity": item.quantity,
                                "unit_price": item.unit_price,
                                "total_price": item.total_price,
                            }
                            for item in order.order_items
                        ],
                    }

                return jsonify({"success": True, "order": order_data})
            except Exception as exc:
                return self._internal_error("Error fetching order", exc)

        @self.app.route("/api/mobile/orders/<int:order_id>/status", methods=["PUT"])
        @self.require_auth
        def update_order_status(order_id):
            try:
                data = request.get_json(silent=True) or {}
                new_status = data.get("status")
                if not new_status:
                    return self._error("Status is required", 400)

                with get_db_session() as db:
                    order = db.query(Order).filter(Order.order_id == order_id).first()
                    if not order:
                        return self._error("Order not found", 404)

                    order.order_status = new_status
                    db.commit()

                return jsonify({"success": True, "message": "Order status updated"})
            except Exception as exc:
                return self._internal_error("Error updating order status", exc)

        @self.app.route("/api/mobile/products", methods=["GET"])
        @self.require_auth
        def get_products():
            try:
                category = request.args.get("category")
                active_only = request.args.get("active_only", "true").lower() == "true"

                with get_db_session() as db:
                    query = db.query(Product)
                    if active_only:
                        query = query.filter(Product.is_active.is_(True))
                    if category:
                        query = query.join(Product.category).filter(Product.category.has(name=category))
                    products = query.all()

                    products_data = [
                        {
                            "product_id": product.product_id,
                            "name": product.name,
                            "category": product.category.name if product.category else None,
                            "price": product.price,
                            "description": product.description,
                            "image_url": product.image_url,
                        }
                        for product in products
                    ]

                return jsonify({"success": True, "products": products_data})
            except Exception as exc:
                return self._internal_error("Error fetching products", exc)

        @self.app.route("/api/mobile/dashboard", methods=["GET"])
        @self.require_auth
        def get_dashboard():
            try:
                from src.utils.dashboard_analytics import (
                    get_active_staff_count,
                    get_inventory_alerts,
                    get_today_orders,
                    get_today_sales,
                )

                today_sales = get_today_sales()
                today_orders = get_today_orders()
                active_staff, total_staff = get_active_staff_count()
                alerts = get_inventory_alerts()

                return jsonify(
                    {
                        "success": True,
                        "dashboard": {
                            "today_sales": today_sales,
                            "today_orders": today_orders,
                            "active_staff": active_staff,
                            "total_staff": total_staff,
                            "inventory_alerts": alerts,
                            "timestamp": datetime.now().isoformat(),
                        },
                    }
                )
            except Exception as exc:
                return self._internal_error("Error fetching dashboard", exc)

        @self.app.route("/api/mobile/inventory/alerts", methods=["GET"])
        @self.require_auth
        def get_inventory_alerts_route():
            try:
                with get_db_session() as db:
                    low_stock = (
                        db.query(Inventory)
                        .filter(
                            Inventory.quantity <= Inventory.reorder_level,
                            Inventory.status == "active",
                        )
                        .all()
                    )

                    alerts_data = [
                        {
                            "ingredient_id": inv.ingredient_id,
                            "ingredient_name": inv.ingredient.name,
                            "current_stock": inv.quantity,
                            "reorder_level": inv.reorder_level,
                            "unit": inv.unit,
                        }
                        for inv in low_stock
                    ]

                return jsonify({"success": True, "alerts": alerts_data})
            except Exception as exc:
                return self._internal_error("Error fetching inventory alerts", exc)

        @self.app.route("/api/mobile/notifications", methods=["GET"])
        @self.require_auth
        def get_notifications_feed():
            try:
                staff_id = request.args.get("staff_id", type=int)
                if not staff_id:
                    return self._error("staff_id is required", 400)

                limit = request.args.get("limit", 50, type=int)
                limit = max(1, min(limit, 200))
                since = request.args.get("since")

                with get_db_session() as db:
                    query = db.query(Notification).order_by(Notification.triggered_at.desc())
                    if since:
                        try:
                            since_dt = datetime.fromisoformat(since)
                        except ValueError:
                            return self._error("Invalid since format. Use ISO 8601.", 400)
                        query = query.filter(Notification.triggered_at >= since_dt)

                    records = query.limit(limit).all()
                    notifications = [
                        {
                            "id": record.notification_id,
                            "module": record.module,
                            "title": record.title,
                            "message": record.message,
                            "severity": record.severity,
                            "triggered_at": (
                                record.triggered_at.isoformat() if record.triggered_at else None
                            ),
                            "is_read": record.is_read,
                        }
                        for record in records
                    ]

                filtered = filter_notifications_for_user(
                    notifications,
                    staff_id,
                    target="mobile",
                )
                unread_count = sum(1 for item in filtered if not item.get("is_read"))
                return jsonify(
                    {
                        "success": True,
                        "notifications": filtered,
                        "unread": unread_count,
                    }
                )
            except Exception as exc:
                return self._internal_error("Error fetching notifications", exc)

        @self.app.route("/api/mobile/notifications/read", methods=["POST"])
        @self.require_auth
        def acknowledge_notifications():
            try:
                data = request.get_json(silent=True) or {}
                ids = data.get("ids", [])
                if not isinstance(ids, list) or not ids:
                    return self._error("ids list required", 400)

                ids = [int(nid) for nid in ids if str(nid).isdigit()]
                if not ids:
                    return self._error("ids list required", 400)

                with get_db_session() as db:
                    updated = (
                        db.query(Notification)
                        .filter(Notification.notification_id.in_(ids))
                        .update(
                            {
                                Notification.is_read: True,
                                Notification.read_at: _utc_now_naive(),
                            },
                            synchronize_session=False,
                        )
                    )
                    db.commit()

                NotificationCenter.instance().notification_updated.emit({"refresh": True})
                return jsonify({"success": True, "updated": updated})
            except Exception as exc:
                return self._internal_error("Error marking notifications read", exc)

        @self.app.route("/api/mobile/staff/clock-in", methods=["POST"])
        @self.require_auth
        def clock_in():
            try:
                data = request.get_json(silent=True) or {}
                staff_id = data.get("staff_id")
                if not staff_id:
                    return self._error("Staff ID is required", 400)

                now = datetime.now()
                today = now.date()

                with get_db_session() as db:
                    attendance = (
                        db.query(Attendance)
                        .filter(
                            Attendance.staff_id == staff_id,
                            Attendance.attendance_date == today,
                        )
                        .first()
                    )

                    if attendance and attendance.clock_in:
                        return self._error("Already clocked in today", 400)

                    if not attendance:
                        attendance = Attendance(
                            staff_id=staff_id,
                            attendance_date=today,
                            clock_in=now,
                            status="present",
                        )
                        db.add(attendance)
                    else:
                        attendance.clock_in = now
                        attendance.status = "present"

                    db.commit()

                return jsonify({"success": True, "message": "Clocked in successfully"})
            except Exception as exc:
                return self._internal_error("Error clocking in", exc)

        @self.app.route("/api/mobile/staff/clock-out", methods=["POST"])
        @self.require_auth
        def clock_out():
            try:
                data = request.get_json(silent=True) or {}
                staff_id = data.get("staff_id")
                if not staff_id:
                    return self._error("Staff ID is required", 400)

                now = datetime.now()
                today = now.date()

                with get_db_session() as db:
                    attendance = (
                        db.query(Attendance)
                        .filter(
                            Attendance.staff_id == staff_id,
                            Attendance.attendance_date == today,
                        )
                        .first()
                    )

                    if not attendance or not attendance.clock_in:
                        return self._error("Not clocked in", 400)
                    if attendance.clock_out:
                        return self._error("Already clocked out today", 400)

                    attendance.clock_out = now

                    if isinstance(attendance.clock_in, datetime):
                        clock_in_dt = attendance.clock_in
                    else:
                        clock_in_dt = datetime.combine(today, attendance.clock_in)

                    total_hours = (now - clock_in_dt).total_seconds() / 3600
                    attendance.total_hours = total_hours
                    db.commit()

                return jsonify(
                    {
                        "success": True,
                        "message": "Clocked out successfully",
                        "total_hours": total_hours,
                    }
                )
            except Exception as exc:
                return self._internal_error("Error clocking out", exc)

    def run(self, host="0.0.0.0", port=5000, debug=False, api_key=None):
        """Run the API server."""
        self.api_key = api_key
        if self.api_key:
            logger.info("Mobile API authentication enabled (X-API-Key required)")
        logger.info(f"Starting Mobile API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def get_mobile_api() -> MobileAPI:
    """Get mobile API instance."""
    return MobileAPI()

