# Quest Source Records

`quests/` is the source quest record district for `aoa-evals` proof
obligations.

A quest is an obligation-return source record: a missing proof surface,
regression gap, verdict-bridge debt, repeated blind spot, proof-pressure
ingress, or owner handoff that still needs a bounded next route.

Open this surface for lane/state source layout, lifecycle routing, and the
split between source records, the human questbook index, generated dispatch
readers, questbook mechanic support, and eval proof meaning.

## Operating Card

| Field | Route |
| --- | --- |
| role | source quest record route map |
| entry | open when deferred proof pressure, regression debt, verdict-bridge debt, or owner handoff needs a durable source record |
| input | proof obligation, lifecycle state, owner route, evidence gap, or generated quest reader ref |
| output | lane/state source record, `QUESTBOOK.md` open-obligation entry, generated quest reader route, or source eval package route |
| owner | `quests/AGENTS.md` for editing law; `quests/LIFECYCLE.md` for state meaning; quest schema for record shape |
| next route | `quests/<lane>/<state>/`, `QUESTBOOK.md`, `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, or source eval packages under `evals/` |
| validation | `quests/AGENTS.md` and the owning questbook mechanic route |

## Current Source Layout

The current source layout is lane/state based:

`quests/<lane>/<state>/<quest-id>.yaml`

- `quests/<lane>/<state>/AOA-EV-Q-*.yaml` are schema-backed source quest
  records.
- Active source records use schema-backed YAML. Former Agon markdown quest
  notes are preserved behind `mechanics/agon/PROVENANCE.md`.

Old top-level quest paths are legacy path vocabulary. Active aliases stay out
of the tree so source IDs stay stable and generated readers expose the current
source path.

## Surface Roles

- `quests/<lane>/<state>/*.yaml`: source quest records.
- `quests/LIFECYCLE.md`: lifecycle contract for state meaning, return posture,
  open-index visibility, and proof-loop defer or handoff endings.
- `QUESTBOOK.md`: human index of open proof, regression, and verdict-bridge
  obligations.
- `generated/quest_catalog.min.json`: derived catalog reader.
- `generated/quest_dispatch.min.json`: derived dispatch reader.
- `generated/quest_catalog.min.example.json` and
  `generated/quest_dispatch.min.example.json`: example mirrors.
- `mechanics/questbook/`: operation package for source-record contracts,
  lifecycle support, and generated dispatch readers.
- `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`:
  source quest record schema.
- `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`:
  generated dispatch schema.
- `evals/**/EVAL.md` and `evals/**/eval.yaml`: source proof meaning when an
  obligation matures into bounded eval work.

Generated quest readers derive from source quest records. Live portable verdict
authority remains with reviewed proof surfaces and bundle-local eval meaning.

## Lanes

Candidate lanes:

- `proof`
- `trace`
- `orchestrator`
- `unlock`
- `runtime`
- `closeout`
- `agon`
- `harvest`
- `questbook`

Allowed lifecycle states are defined by `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`:

- `captured`
- `triaged`
- `ready`
- `active`
- `blocked`
- `reanchor`
- `done`
- `dropped`

The state directory must match the record's `state` field. This lets path,
source metadata, and generated readers reinforce the same lifecycle claim.

Use `quests/LIFECYCLE.md` before changing a quest state. It defines which
states remain open in `QUESTBOOK.md`, which states are closed provenance, and
which return posture applies when a proof-loop route defers or hands off.

## Change Routes

| Change pressure | Source route |
| --- | --- |
| Record shape or path | `quests/AGENTS.md`, then `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json` |
| State meaning or open-index visibility | `quests/LIFECYCLE.md` and `QUESTBOOK.md` |
| Generated quest lookup | `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, and the catalog builder |
| Broad repo direction | `ROADMAP.md` |
| Durable rationale | `docs/decisions/` |
| Matured proof work | source eval packages under `evals/` |

## Verify

Use [AGENTS](AGENTS.md#validation) for executable validation commands.
