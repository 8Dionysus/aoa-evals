# Questbook Schema Parts

- Decision ID: AOA-EV-D-0047
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/questbook/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part, quest/lane
- Mechanic parents: questbook
- Guard families: part and payload
- Posture: active rationale

## Context

Questbook already owned a real proof-side operation:

`source quest record -> human open-obligation index -> generated quest reader -> deferred return or reviewed promotion`

The operation was split across root districts:

- source records under `quests/<lane>/<state>/`
- lifecycle guidance under `quests/LIFECYCLE.md`
- human index in `QUESTBOOK.md`
- generated readers under `generated/`
- validation in `scripts/validate_repo.py` and `scripts/build_catalog.py`
- schemas under root `schemas/`

The root schema placement made the quest contract look like generic proof
infrastructure even though the schemas only make sense inside the questbook
loop.

## Options Considered

- Leave the schemas in root `schemas/` as generic contracts.
- Move both schemas into a single generic `questbook/schemas/` directory.
- Split the schemas into active questbook parts.

## Decision

Move the quest source schema to:

`mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`

Move the quest dispatch schema to:

`mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`

Add `mechanics/questbook/PARTS.md`, `PROVENANCE.md`, and legacy index/log
surfaces so active parts come first and former root placement remains
traceable.

Generated quest readers remain in root `generated/` because they are repo-wide
derived readers. Source quest records remain under `quests/` because that is
the active source district.

## Rationale

This keeps topology convex. The source-record contract and dispatch-reader
contract are not standalone mechanics and not generic proof-infra. They are
parts of the AoA-aligned `questbook` mechanic.

The split also keeps generated projection weaker than source quest records. A
future agent can now tell which part owns schema changes without treating the
root schema directory as a mixed bag of unrelated mechanics.

## Consequences

- Positive: quest schemas now sit behind the active mechanic that owns their
  operation.
- Positive: old root schema paths are preserved as legacy path vocabulary, not
  active topology.
- Positive: `questbook` now has part and provenance surfaces matching the
  active mechanics pattern.
- Tradeoff: validation constants and test fixtures must use longer part-local
  paths.

## Boundaries

This decision does not move source quest records out of `quests/`.

It does not move generated quest readers out of root `generated/`.

It does not make quests eval bundles, roadmap direction, proof verdicts, or
owner acceptance.

It does not authorize root schema aliases or top-level quest source aliases.

## Validation

- `mechanics/questbook/PARTS.md` names active parts, stop-lines, and validation.
- `mechanics/questbook/PROVENANCE.md` bridges former root schema placement
  questions into the owning legacy archive.
- `scripts/validate_repo.py` and `scripts/build_catalog.py` use the part-local
  schema paths.
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
