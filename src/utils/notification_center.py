"""
NotificationCenter - central event bus for ERP alerts
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal, QMutex, QMutexLocker
from loguru import logger

from src.database.connection import get_db_session
from src.database.models import Notification


class NotificationCenter(QObject):
    """
    Singleton service used by all modules to create/read notifications.
    
    It persists notifications to the database, emits Qt signals so the UI/tray
    can react instantly, and provides helper methods to query or mark items
    as read.
    """
    
    notification_created = pyqtSignal(dict)
    notification_updated = pyqtSignal(dict)
    
    _instance: Optional["NotificationCenter"] = None
    _lock: QMutex = QMutex()
    
    def __init__(self):
        super().__init__()
        logger.info("NotificationCenter initialized")
    
    @classmethod
    def instance(cls) -> "NotificationCenter":
        """Return the singleton instance"""
        if cls._instance is None:
            with QMutexLocker(cls._lock):
                if cls._instance is None:
                    cls._instance = NotificationCenter()
        return cls._instance
    
    # ------------------------------------------------------------------
    # Creation helpers
    # ------------------------------------------------------------------
    def emit_notification(
        self,
        module: str,
        title: str,
        message: str,
        *,
        severity: str = "info",
        source_type: Optional[str] = None,
        source_id: Optional[int] = None,
        payload: Optional[Dict] = None,
        notified_user_id: Optional[int] = None,
        deduplicate: bool = True,
    ) -> Optional[dict]:
        """
        Persist a new notification and broadcast it.
        
        deduplicate: when True and source info is provided, skip creation if
        there is already an unread notification for the same source.
        """
        session = get_db_session()
        try:
            # Optional deduplication to avoid noisy repeats
            if deduplicate and source_type and source_id:
                existing = (
                    session.query(Notification)
                    .filter(
                        Notification.source_type == source_type,
                        Notification.source_id == source_id,
                        Notification.is_read == False,  # noqa: E712
                        Notification.module == module,
                    )
                    .first()
                )
                if existing:
                    logger.debug(
                        "Skipping duplicate notification for %s:%s",
                        source_type,
                        source_id,
                    )
                    return self._serialize(existing)
            
            notification = Notification(
                module=module,
                title=title,
                message=message,
                severity=severity,
                source_type=source_type,
                source_id=source_id,
                payload=payload,
                notified_user_id=notified_user_id,
                triggered_at=datetime.utcnow(),
            )
            session.add(notification)
            session.commit()
            session.refresh(notification)
            
            data = self._serialize(notification)
            self.notification_created.emit(data)
            return data
        except Exception as exc:
            session.rollback()
            logger.error(f"Failed to emit notification: {exc}")
            return None
        finally:
            session.close()
    
    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------
    def get_recent_notifications(self, limit: int = 20) -> List[dict]:
        session = get_db_session()
        try:
            records = (
                session.query(Notification)
                .order_by(Notification.triggered_at.desc())
                .limit(limit)
                .all()
            )
            return [self._serialize(item) for item in records]
        except Exception as exc:
            logger.error(f"Failed to load recent notifications: {exc}")
            return []
        finally:
            session.close()
    
    def get_unread_count(self) -> int:
        session = get_db_session()
        try:
            return (
                session.query(Notification)
                .filter(Notification.is_read == False)  # noqa: E712
                .count()
            )
        except Exception as exc:
            logger.error(f"Failed to count unread notifications: {exc}")
            return 0
        finally:
            session.close()
    
    def mark_as_read(self, notification_id: int) -> bool:
        session = get_db_session()
        try:
            record = (
                session.query(Notification)
                .filter(Notification.notification_id == notification_id)
                .first()
            )
            if not record:
                return False
            if record.is_read:
                return True
            
            record.is_read = True
            record.read_at = datetime.utcnow()
            session.commit()
            data = self._serialize(record)
            self.notification_updated.emit(data)
            return True
        except Exception as exc:
            session.rollback()
            logger.error(f"Failed to mark notification as read: {exc}")
            return False
        finally:
            session.close()
    
    def mark_all_as_read(self) -> int:
        session = get_db_session()
        try:
            updated = (
                session.query(Notification)
                .filter(Notification.is_read == False)  # noqa: E712
                .update(
                    {
                        Notification.is_read: True,
                        Notification.read_at: datetime.utcnow(),
                    }
                )
            )
            session.commit()
            if updated:
                self.notification_updated.emit({"refresh": True})
            return updated or 0
        except Exception as exc:
            session.rollback()
            logger.error(f"Failed to mark notifications as read: {exc}")
            return 0
        finally:
            session.close()
    
    def resolve_for_source(self, source_type: str, source_id: int) -> int:
        """
        Mark notifications tied to a source as read. Useful when an order/task
        is completed and its alert should disappear automatically.
        """
        session = get_db_session()
        try:
            updated = (
                session.query(Notification)
                .filter(
                    Notification.source_type == source_type,
                    Notification.source_id == source_id,
                    Notification.is_read == False,  # noqa: E712
                )
                .update(
                    {
                        Notification.is_read: True,
                        Notification.read_at: datetime.utcnow(),
                    }
                )
            )
            session.commit()
            if updated:
                self.notification_updated.emit({"refresh": True})
            return updated or 0
        except Exception as exc:
            session.rollback()
            logger.error(
                "Failed to resolve notifications for %s:%s - %s",
                source_type,
                source_id,
                exc,
            )
            return 0
        finally:
            session.close()
    
    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _serialize(notification: Notification) -> dict:
        return {
            "id": notification.notification_id,
            "module": notification.module,
            "title": notification.title,
            "message": notification.message,
            "severity": notification.severity,
            "source_type": notification.source_type,
            "source_id": notification.source_id,
            "payload": notification.payload or {},
            "is_read": notification.is_read,
            "read_at": notification.read_at.isoformat() if notification.read_at else None,
            "triggered_at": notification.triggered_at.isoformat() if notification.triggered_at else None,
            "notified_user_id": notification.notified_user_id,
        }


