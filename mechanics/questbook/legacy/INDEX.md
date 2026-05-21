# Questbook Legacy Index

## Role

This index maps old questbook path vocabulary to the current active route.

It is not an active quest source list and not a retirement queue.

## Path Map

| Former or overloaded path | Current active route | Posture |
| --- | --- | --- |
| `schemas/quest.schema.json` | `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json` | historical root schema placement |
| `schemas/quest_dispatch.schema.json` | `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json` | historical root schema placement |
| `quests/AOA-EV-Q-*.yaml` | `quests/<lane>/<state>/AOA-EV-Q-*.yaml` | historical top-level source path vocabulary |
| `quests/AOE-Q-AGON-*.md` and `quests/agon/captured/AOE-Q-AGON-*.md` | `mechanics/agon/PROVENANCE.md` | former Agon markdown note lineage |

## Stop-Lines

- Do not recreate root schema aliases.
- Do not recreate top-level quest source files.
- Do not turn former Agon markdown notes into eval bundles or active quest
  lifecycle records.
- Do not use legacy lookup as proof authority.

## Validation

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
