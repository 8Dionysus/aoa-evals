# Questbook Legacy Index

## Role

This index maps old questbook path vocabulary to the current active route.

It returns schema, quest-source, and former Agon note questions to their active
owners.

## Path Map

| Former or overloaded path | Current active route | Posture |
| --- | --- | --- |
| `schemas/quest.schema.json` | `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json` | historical root schema placement |
| `schemas/quest_dispatch.schema.json` | `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json` | historical root schema placement |
| `quests/AOA-EV-Q-*.yaml` | `quests/<lane>/<state>/AOA-EV-Q-*.yaml` | historical top-level source path vocabulary |
| `quests/AOE-Q-AGON-*.md` and `quests/agon/captured/AOE-Q-AGON-*.md` | `mechanics/agon/PROVENANCE.md` | former Agon markdown note lineage |

## Current Route Expectations

| Pressure | Route |
| --- | --- |
| root quest schema alias | current questbook part schema route |
| top-level quest source vocabulary | `quests/<lane>/<state>/` source record route |
| former Agon markdown note | `mechanics/agon/PROVENANCE.md` lineage bridge |
| proof authority question | source quest record, source eval bundle, and owning review route |

## Validation

Use [AGENTS.md](AGENTS.md#validation).
