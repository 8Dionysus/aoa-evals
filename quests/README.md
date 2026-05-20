# Quests

`quests/` contains source quest records for `aoa-evals` proof obligations.

Quests are not eval bundles. A quest is an obligation to return: a missing proof
surface, regression gap, verdict-bridge debt, repeated blind spot, proof-pressure
ingress, or owner handoff that has not yet matured into a bundle, decision,
mechanic, or release item.

## Current Source Layout

The current source layout is lane/state based:

`quests/<lane>/<state>/<quest-id>.*`

- `quests/<lane>/<state>/AOA-EV-Q-*.yaml` are schema-backed source quest
  records.
- `quests/agon/captured/AOE-Q-AGON-*.md` are legacy/source-compatible Agon
  alignment notes.

Old top-level quest paths are legacy path vocabulary, not active source files.
Do not reintroduce them as duplicate aliases; source IDs stay stable and
generated readers expose the current source path.

## Surface Roles

- `quests/<lane>/<state>/*.yaml`: source quest records.
- `quests/<lane>/<state>/*.md`: legacy or source-compatible notes.
- `quests/LIFECYCLE.md`: lifecycle contract for state meaning, return posture,
  open-index visibility, and proof-loop defer or handoff endings.
- `QUESTBOOK.md`: human index of open proof, regression, and verdict-bridge
  obligations.
- `generated/quest_catalog.min.json`: derived catalog reader.
- `generated/quest_dispatch.min.json`: derived dispatch reader.
- `generated/quest_catalog.min.example.json` and
  `generated/quest_dispatch.min.example.json`: example mirrors.
- `schemas/quest.schema.json`: source quest record schema.
- `schemas/quest_dispatch.schema.json`: generated dispatch schema.

Generated quest readers do not replace source quest records and do not become
live portable verdict authority.

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

Allowed lifecycle states are defined by `schemas/quest.schema.json`:

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

## Editing Rules

- Keep `id` equal to the filename stem for
  `quests/<lane>/<state>/AOA-EV-Q-*.yaml`.
- Keep `repo: aoa-evals`.
- Keep `public_safe: true`.
- Keep the state directory equal to the source record `state`.
- Keep `quests/LIFECYCLE.md` aligned with every state accepted by
  `schemas/quest.schema.json`.
- Keep closed quests out of the open-obligation list in `QUESTBOOK.md`.
- Keep active, captured, triaged, ready, blocked, and reanchor quests visible in
  `QUESTBOOK.md`.
- Route broad direction to `ROADMAP.md`.
- Route durable rationale to `docs/decisions/`.
- Route proof meaning to eval bundles.

## Verify

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
