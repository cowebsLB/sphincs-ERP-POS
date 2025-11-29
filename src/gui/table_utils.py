"""
Shared table helpers for consistent sizing and appearance.
"""

from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableView, QApplication


def enable_table_auto_resize(
    table,
    *,
    stretch_last: bool = True,
    mode: QHeaderView.ResizeMode = QHeaderView.ResizeMode.ResizeToContents,
    minimum_section: int = 80,
) -> None:
    """
    Configure a QTableWidget/QTableView to automatically size columns to their contents.
    """
    header = table.horizontalHeader()
    header.setSectionResizeMode(mode)
    header.setMinimumSectionSize(minimum_section)
    header.setStretchLastSection(stretch_last)
    table.resizeColumnsToContents()
    setattr(table, "_auto_resize_applied", True)


class _TableAutoResizeFilter(QObject):
    """Event filter that ensures every table auto-resizes its columns."""
    
    def eventFilter(self, obj, event):
        if (
            isinstance(obj, (QTableWidget, QTableView))
            and event.type() in (QEvent.Type.Show, QEvent.Type.Polish)
            and not getattr(obj, "_auto_resize_applied", False)
        ):
            enable_table_auto_resize(obj)
        return super().eventFilter(obj, event)


_TABLE_AUTO_RESIZE_FILTER: _TableAutoResizeFilter | None = None


def install_table_auto_resize(app: QApplication) -> None:
    """Install the global event filter (idempotent)."""
    global _TABLE_AUTO_RESIZE_FILTER
    if _TABLE_AUTO_RESIZE_FILTER is None:
        _TABLE_AUTO_RESIZE_FILTER = _TableAutoResizeFilter()
        app.installEventFilter(_TABLE_AUTO_RESIZE_FILTER)

