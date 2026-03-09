# ERP UI/UX Phase 1 - Shell Refresh

Back to [Documentation Index](../INDEX.md), [ERP UI/UX Roadmap](uiux-roadmap.md), [ERP UI/UX Baseline Audit](uiux-audit-baseline.md), and [ERP Worklog](worklog.md).

## Scope

Foundation visual/system pass for the ERP shell:

- Sidebar navigation
- Settings shell
- Dashboard shell/components
- Shared design tokens and style snippets

## Implemented

1. Shared design system module

- Added reusable color tokens and style snippets in `src/gui/design_system.py`.
- Centralized common styles: cards, tabs, inputs, buttons, list widgets, sidebar shell.

1. Sidebar refresh

- Rebuilt sidebar styling with a cleaner structure and consistent spacing.
- Replaced broken icon text artifacts with stable ASCII abbreviations.
- Preserved navigation behavior and signal API.

1. Settings refresh

- Reworked settings header/subtitle hierarchy.
- Unified tab/group/input/button styles via design system tokens.
- Replaced free-text update toggle with explicit enabled/disabled combo.

1. Dashboard shell improvements

- Applied shared styles to key dashboard surfaces.
- Improved welcome/summary wording and quick-action layout density.
- Centered dashboard content column for better readability on wide screens.
- Standardized notification/activity card and list styling.

## Non-goals in this phase

- Deep per-module visual redesign beyond dashboard/sidebar/settings.
- Business logic changes outside minimal UX-supportive adjustments.
- Data model or backend contract changes.

## Validation

- `flake8 --select F821,F824,F811` on touched ERP shell files: pass.
- Targeted GUI import tests: pass.
- `test_all_features.py` subset for GUI/config paths: pass.

## Next

Phase 2 should rollout design-system usage into:

1. Product management
2. Inventory management
3. Customer and staff management
4. Sales and financial modules
