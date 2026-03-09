# ERP UI/UX Baseline Audit

Back to [Documentation Index](../INDEX.md), [ERP UI/UX Roadmap](uiux-roadmap.md), and [ERP Worklog](worklog.md).

## Scope

Initial static audit of the ERP shell and core navigation surfaces:

- `src/erp_main.py`
- `src/gui/erp_dashboard.py`
- `src/gui/sidebar.py`
- `src/gui/settings_view.py`

## Findings

1. Styling is duplicated across modules.

- Large inline `setStyleSheet` blocks repeat colors, spacing, and component patterns.
- This increases drift and slows consistent UI updates.

1. No shared UI token layer is enforced.

- Colors, sizes, and paddings are hardcoded in many files.
- Dashboard, sidebar, and settings use similar components but separate style definitions.

1. Navigation text/icon rendering has encoding artifacts.

- Sidebar labels/icons include mojibake characters in the source.
- This can degrade perceived quality and maintainability.

1. Visual hierarchy is inconsistent.

- Header scale, card density, and spacing differ between views.
- Important data and actions do not always stand out predictably.

1. Readability/performance risk in large UI modules.

- ERP shell files are large and mix layout, behavior, and style concerns.
- This makes rapid UX iteration harder.

## Priority Fix List (ERP Phase 1)

1. Create shared style tokens and reusable widget style helpers.
2. Refactor dashboard/sidebars/settings to consume shared styles.
3. Normalize top-level page structure:

- Header
- Primary actions
- Summary
- Detailed content

1. Replace broken icon text with stable assets or unicode-safe strings.
2. Introduce small UI helper components for repeated card/table/button patterns.

## Acceptance Criteria for Phase 1

- Dashboard, sidebar, and settings share one style system.
- Navigation and labels render cleanly with no encoding artifacts.
- Primary actions and KPI cards follow one hierarchy pattern.
- Existing behavior remains stable while visual consistency improves.
