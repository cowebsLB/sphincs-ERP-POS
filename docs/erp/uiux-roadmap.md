# ERP UI/UX Roadmap

Back to [Documentation Index](../INDEX.md), [ERP Worklog](worklog.md), [ERP UI/UX Baseline Audit](uiux-audit-baseline.md), and [ERP UI/UX Phase 1 Shell Refresh](uiux-phase1-shell-refresh.md).

## Goal

Improve ERP usability and visual quality without breaking existing business logic.

## Focus Areas

1. Information architecture

- Clean navigation grouping and naming.
- Reduce duplicate destinations and dead-end views.

1. Dashboard clarity

- Improve hierarchy for KPIs, alerts, and quick actions.
- Prioritize actionable data over decorative blocks.

1. Shared design system

- Standardize spacing, typography, button variants, and card/table patterns.
- Reduce one-off styling per module.

1. Workflow quality

- Improve add/edit dialogs for data-heavy modules.
- Reduce clicks for top daily ERP tasks.

## Delivery Phases

1. Audit and baseline

- Capture screenshots and friction points.
- Define objective UX acceptance checks.

1. Foundation pass

- Introduce reusable style tokens/components.
- Apply to dashboard, sidebar, and settings first.

1. Module rollout

- Apply patterns to Product, Inventory, Customer, Staff, Sales, and Finance views.
- Keep behavior unchanged unless explicitly planned.

1. Final polish

- Alignment pass, edge-case states, and accessibility/readability checks.

## Acceptance Checks

- Navigation labels are consistent and predictable.
- Key daily actions are reachable in 2 clicks or less.
- Table-heavy screens keep readability at common desktop sizes.
- No regressions in existing tests and critical import checks.
