# ERP UI/UX Phase 2 - Global Visual Refresh

Back to [Documentation Index](../INDEX.md), [ERP UI/UX Roadmap](uiux-roadmap.md), and [ERP Worklog](worklog.md).

## Goal

Establish a single, consistent, high-contrast visual baseline across ERP modules without breaking existing workflows.

## What Was Implemented

- Introduced a global ERP stylesheet (`ERP_APP_BASE_STYLE`) in `src/gui/design_system.py`.
- Applied the global style at app bootstrap in `src/erp_main.py`.
- Covered core widget families:
  - `QWidget`, `QMainWindow`, `QFrame`, `QLabel`, `QGroupBox`
  - Inputs (`QLineEdit`, `QComboBox`, text editors, date/spin controls)
  - Data views (`QTableWidget`, `QTableView`, `QTreeWidget`, `QTreeView`)
  - Tabs, menus, tooltips, and scrollbars
  - Default button states (normal, hover, pressed, disabled)

## Design Direction

- Light enterprise shell with dark, readable text.
- Crisp surfaces and clear borders for forms and data grids.
- Focus states and selection states that are visible and consistent.
- Preserved module-level overrides where intentional, while preventing unreadable fallback colors.

## Accessibility-Driven Rules

- All text defaults to dark foreground on light surfaces.
- Table headers and rows use explicit foreground colors.
- Selection colors maintain readable foreground/background contrast.
- Tooltips and menus remain legible against surrounding context.

## Files

- `src/gui/design_system.py`
- `src/erp_main.py`
- `src/gui/retail_ecommerce_view.py` (module-level contrast hardening from hotfix)

## Validation Plan

- Compile checks for touched Python files.
- Launch smoke test for ERP.
- Manual visual verification across table-heavy modules:
  - Product Management
  - Inventory Management
  - Supplier Management
  - Customer Management
  - Retail & E-Commerce

## Next Improvements (Optional)

- Standardize all legacy per-module `setStyleSheet` blocks to design-system constants.
- Add shared status-chip helpers (success, warning, error, info).
- Add compact-density mode for data-entry heavy operators.
