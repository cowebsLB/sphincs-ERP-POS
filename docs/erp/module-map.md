# ERP Module Map

Back to [Documentation Index](../INDEX.md), [ERP UI/UX Roadmap](uiux-roadmap.md), [ERP UI/UX Baseline Audit](uiux-audit-baseline.md), [ERP UI/UX Phase 1 Shell Refresh](uiux-phase1-shell-refresh.md), and [ERP Worklog](worklog.md).

## Core ERP Shell

- Entry point: `src/erp_main.py`
- Main dashboard window: `src/gui/erp_dashboard.py`
- Navigation sidebar: `src/gui/sidebar.py`
- Settings container: `src/gui/settings_view.py`

## Primary ERP Modules

- Products: `src/gui/product_management.py`
- Inventory: `src/gui/inventory_management.py`
- Customers: `src/gui/customer_management.py`
- Staff: `src/gui/staff_management.py`
- Sales: `src/gui/sales_management.py`
- Financial: `src/gui/financial_management.py`
- Reports: `src/gui/sales_reports.py`
- Operations Hub: `src/gui/operations_hub.py`

## Supporting Services

- DB models: `src/database/models.py`
- DB connection/session: `src/database/connection.py`
- Notifications center: `src/utils/notification_center.py`
- Notification preferences: `src/utils/notification_preferences.py`

## UX Prioritization Order

1. `erp_dashboard.py`
2. `sidebar.py`
3. `settings_view.py`
4. Module-by-module rollout using shared patterns
