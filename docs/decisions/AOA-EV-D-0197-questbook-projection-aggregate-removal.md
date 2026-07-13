# Questbook Projection Aggregate Removal

- Decision ID: AOA-EV-D-0197
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused Questbook projection, parity, and orchestrator reference validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/read-model, source/topology, capability/permission
- Mechanic parents: questbook, cross-parent
- Guard families: projection/generated, source/topology, capability/permission
- Posture: active rationale

## Context

AOA-EV-D-0163 moved generated Questbook projection checks out of the old
Questbook facade, and AOA-EV-D-0193 removed that facade. The remaining
`scripts/validators/questbook_projection.py` module still mixed three different
boundaries:

- source record discovery, projection-readiness checks, and expected reader
  entry builders;
- generated catalog/dispatch live/example parity checks; and
- strict sibling `aoa-agents` orchestrator-class reference resolution.

Those checks are related by handoff, but they do not share one owner surface.
Keeping them in one module made generated parity look like it also owned source
record shape and sibling capability references.

## Decision

`scripts/validators/questbook_projection.py` is removed.

Questbook projection validation now routes through focused modules:

- `questbook_projection_records.py` owns quest source discovery, projection
  readiness, and expected catalog/dispatch record builders.
- `questbook_projection_parity.py` owns generated catalog/dispatch live/example
  parity and dispatch schema checks.
- `questbook_orchestrator_refs.py` owns strict sibling orchestrator-class
  reference shape and resolution.

`validate_repo.py` orchestrates the source-to-generated handoff by passing the
focused source-record result into generated parity. `build_catalog.py` imports
the projection record builder directly. Tests import the focused module that
owns the exercised behavior.

## Rationale

Generated readers are projections, not source authority. A builder that derives
expected catalog records from source YAML is not the same boundary as a parity
validator that checks frozen generated files, and neither of them owns the
sibling `aoa-agents` capability catalog.

Splitting the module makes each failure route explicit: fix source records,
rebuild generated readers, or repair strict sibling refs. It also removes the
last Questbook projection-shaped aggregate after the facade removal.

## Consequences

- Positive: no Questbook projection aggregate/facade validator remains.
- Positive: generated parity, projection builders, and strict sibling refs now
  have separate inventory rows, mechanics ledger rows, and import paths.
- Positive: the source-to-generated handoff stays explicit without absorbing
  generated parity or sibling capability meaning into source-record checks.
- Tradeoff: Questbook source validation imports three focused modules instead
  of one broader projection module.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook generated readers must remain exact projections of
  source quest records and schema-backed dispatch rules.
- Changed: the projection aggregate no longer exists; active behavior is split
  across `questbook_projection_records.py`, `questbook_projection_parity.py`,
  and `questbook_orchestrator_refs.py`.
- Further changed by: AOA-EV-D-0208 removes the `questbook_source.py`
  aggregate and moves the active handoff into `validate_repo.py`.
- Supersedes: the remaining aggregate shape left by AOA-EV-D-0163 and
  AOA-EV-D-0193.

## Boundaries

This decision does not make generated quest readers the source of quest meaning,
live task assignment, runtime dispatch, proof-surface promotion, owner
acceptance, final quest state movement, or sibling orchestrator ownership.

It does not create a replacement Questbook projection aggregate under another
name.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
