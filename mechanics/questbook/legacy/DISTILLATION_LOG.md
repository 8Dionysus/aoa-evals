# Questbook Distillation Log

## Role

This log accounts for questbook lineage that has been distilled into active
parts.

It is not a changelog, generated output, or active work queue.

## Entries

### 2026-05-20 - Root quest schemas distilled into questbook parts

Former root schemas:

- `schemas/quest.schema.json`
- `schemas/quest_dispatch.schema.json`

Active parts:

- `mechanics/questbook/parts/source-record-contract/`
- `mechanics/questbook/parts/dispatch-reader/`

Reason:

The schemas are not generic shared proof-infra contracts. They constrain the
quest obligation loop: source quest records, lifecycle state, generated
dispatch readers, and return routes. Moving them behind `questbook` keeps the
active route convex while generated readers remain root-derived companions.

Validation route:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
