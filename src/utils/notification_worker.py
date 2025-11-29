"""
Background worker thread that periodically scans the database
for conditions that should trigger notifications.
"""

from datetime import date, datetime, timedelta

from PyQt6.QtCore import QThread
from loguru import logger
from sqlalchemy.orm import joinedload

from src.database.connection import get_db_session
from src.database.models import (
    Inventory,
    InventoryExpiry,
    MaintenanceTask,
    Notification,
    Order,
    QualityAudit,
    SafetyIncident,
)
from src.utils.notification_center import NotificationCenter


class NotificationWorker(QThread):
    """QThread that polls the database and emits alerts."""
    
    def __init__(self, poll_seconds: int = 60, parent=None):
        super().__init__(parent)
        self.poll_seconds = max(15, poll_seconds)
        self._running = False
        self.center = NotificationCenter.instance()
    
    def stop(self):
        """Request the worker to stop."""
        self._running = False
    
    def run(self):
        """Main loop."""
        self._running = True
        logger.info("Notification worker started (interval=%ss)", self.poll_seconds)
        
        while self._running:
            try:
                self.check_inventory_levels()
                self.check_expiry_records()
                self.check_operations_tasks()
                self.check_pending_orders()
            except Exception as exc:
                logger.error(f"Notification worker cycle failed: {exc}")
            
            # Sleep in smaller chunks so stop() is responsive
            elapsed = 0
            while self._running and elapsed < self.poll_seconds:
                self.msleep(200)
                elapsed += 0.2
        
        logger.info("Notification worker stopped")
    
    # ------------------------------------------------------------------
    # Inventory checks
    # ------------------------------------------------------------------
    def check_inventory_levels(self):
        session = get_db_session()
        items = []
        try:
            items = (
                session.query(Inventory)
                .options(joinedload(Inventory.ingredient))
                .filter(
                    Inventory.reorder_level.isnot(None),
                    Inventory.reorder_level > 0,
                    Inventory.quantity <= Inventory.reorder_level,
                )
                .all()
            )
            for item in items:
                name = item.ingredient.name if item.ingredient else f"Inventory #{item.inventory_id}"
                message = f"{name} is at {item.quantity:g} {item.unit} (reorder level {item.reorder_level:g})."
                self.center.emit_notification(
                    module="Inventory",
                    title="Low stock alert",
                    message=message,
                    severity="warning",
                    source_type="inventory_low",
                    source_id=item.inventory_id,
                    payload={
                        "inventory_id": item.inventory_id,
                        "quantity": item.quantity,
                        "unit": item.unit,
                    },
                )
        finally:
            session.close()
        
        active_ids = {item.inventory_id for item in items}
        self._resolve_cleared_sources("inventory_low", active_ids)
    
    def check_expiry_records(self):
        session = get_db_session()
        today = date.today()
        try:
            records = (
                session.query(InventoryExpiry)
                .options(joinedload(InventoryExpiry.inventory).joinedload(Inventory.ingredient))
                .filter(InventoryExpiry.is_expired == False)  # noqa: E712
                .all()
            )
            for record in records:
                days_before = record.alert_days_before or 0
                warn_date = today + timedelta(days=days_before)
                if record.expiry_date <= today:
                    severity = "critical"
                    title = "Expired ingredient"
                elif record.expiry_date <= warn_date:
                    severity = "warning"
                    title = "Ingredient expiring soon"
                else:
                    continue
                
                ingredient = None
                if record.inventory and record.inventory.ingredient:
                    ingredient = record.inventory.ingredient.name
                
                message = f"{ingredient or 'Batch'} expires on {record.expiry_date.isoformat()}."
                data = self.center.emit_notification(
                    module="Inventory",
                    title=title,
                    message=message,
                    severity=severity,
                    source_type="inventory_expiry",
                    source_id=record.expiry_id,
                    payload={
                        "expiry_id": record.expiry_id,
                        "inventory_id": record.inventory_id,
                        "expiry_date": record.expiry_date.isoformat(),
                    },
                )
                
                # Mark DB flag when already expired
                if severity == "critical" and not record.is_expired:
                    record.is_expired = True
                    session.commit()
        finally:
            session.close()
    
    # ------------------------------------------------------------------
    # Operations hub checks
    # ------------------------------------------------------------------
    def check_operations_tasks(self):
        today = date.today()
        
        # Maintenance tasks overdue
        session = get_db_session()
        tasks = []
        try:
            tasks = (
                session.query(MaintenanceTask)
                .filter(
                    MaintenanceTask.status.in_(["open", "in_progress"]),
                    MaintenanceTask.scheduled_date.isnot(None),
                    MaintenanceTask.scheduled_date < today,
                )
                .all()
            )
            for task in tasks:
                self.center.emit_notification(
                    module="Operations",
                    title="Maintenance task overdue",
                    message=f"Task #{task.task_id} is past due for asset {task.asset_id or 'N/A'}.",
                    severity="warning",
                    source_type="maintenance_task",
                    source_id=task.task_id,
                )
        finally:
            session.close()
        self._resolve_cleared_sources("maintenance_task", {task.task_id for task in tasks})
        
        # Quality audits that need follow-up
        session = get_db_session()
        audits = []
        try:
            audits = (
                session.query(QualityAudit)
                .filter(
                    QualityAudit.status.in_(["open", "in_progress"]),
                    QualityAudit.follow_up_date.isnot(None),
                    QualityAudit.follow_up_date <= today,
                )
                .all()
            )
            for audit in audits:
                self.center.emit_notification(
                    module="Operations",
                    title="Quality audit follow-up",
                    message=f"Audit #{audit.audit_id} requires attention.",
                    severity="info",
                    source_type="quality_audit",
                    source_id=audit.audit_id,
                )
        finally:
            session.close()
        self._resolve_cleared_sources("quality_audit", {audit.audit_id for audit in audits})
        
        # Safety incidents still open
        session = get_db_session()
        incidents = []
        try:
            incidents = (
                session.query(SafetyIncident)
                .filter(SafetyIncident.status.in_(["open", "investigating"]))
                .all()
            )
            for incident in incidents:
                severity = (
                    "critical" if incident.severity in ("major", "critical") else "warning"
                )
                self.center.emit_notification(
                    module="Safety",
                    title="Open safety incident",
                    message=f"Incident #{incident.incident_id} ({incident.severity}) pending.",
                    severity=severity,
                    source_type="safety_incident",
                    source_id=incident.incident_id,
                )
        finally:
            session.close()
        self._resolve_cleared_sources("safety_incident", {incident.incident_id for incident in incidents})
    
    # ------------------------------------------------------------------
    # Sales / POS checks
    # ------------------------------------------------------------------
    def check_pending_orders(self):
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=5)
        session = get_db_session()
        active_ids = set()
        try:
            pending_orders = (
                session.query(Order)
                .filter(
                    Order.order_status == "pending",
                    Order.order_datetime >= cutoff,
                )
                .all()
            )
            for order in pending_orders:
                self.center.emit_notification(
                    module="Sales",
                    title="New POS order",
                    message=f"Order #{order.order_id} is waiting for processing.",
                    severity="info",
                    source_type="pos_order",
                    source_id=order.order_id,
                    payload={
                        "order_id": order.order_id,
                        "total": order.total_amount,
                        "type": order.order_type,
                    },
                )
            active_ids = {order.order_id for order in pending_orders}
        finally:
            session.close()
        
        self._resolve_cleared_sources("pos_order", active_ids)
    
    def _resolve_cleared_sources(self, source_type: str, active_ids):
        """Automatically mark alerts resolved when their source no longer matches."""
        session = get_db_session()
        try:
            stale = (
                session.query(Notification.source_id)
                .filter(
                    Notification.source_type == source_type,
                    Notification.is_read == False,  # noqa: E712
                )
                .all()
            )
        finally:
            session.close()
        
        for (source_id,) in stale:
            if source_id not in active_ids:
                self.center.resolve_for_source(source_type, source_id)


