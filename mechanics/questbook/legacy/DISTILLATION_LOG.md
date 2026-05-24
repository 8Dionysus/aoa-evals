# Questbook Distillation Log

## Role

This log accounts for questbook lineage that has been distilled into active
parts.

It records former placement, active owner, reason, and validation route pointer.

## Entries

### 2026-05-20 - Root quest schemas distilled into questbook parts

Former root schemas:

- `schemas/quest.schema.json`
- `schemas/quest_dispatch.schema.json`

Active parts:

- `mechanics/questbook/parts/source-record-contract/`
- `mechanics/questbook/parts/dispatch-reader/`

Reason:

The schemas constrain the quest obligation loop: source quest records,
lifecycle state, generated dispatch readers, and return routes. Their current
home is `questbook`, keeping the active route convex while generated readers
remain root-derived companions.

Validation route:

Use [AGENTS.md](AGENTS.md#validation).
