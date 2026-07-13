# Questbook Source Aggregate Removal

- Decision ID: AOA-EV-D-0208
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused Questbook schema, source-record, obligation-index, projection, and progression validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model, mechanics/topology, capability/permission
- Mechanic parents: questbook, rpg, cross-parent
- Guard families: source/topology, projection/generated, trace/eval, capability/permission
- Posture: active rationale

## Context

AOA-EV-D-0170 moved Questbook source behavior out of the old Questbook facade,
but the replacement `scripts/validators/questbook_source.py` kept growing into
another aggregate. It checked schema envelopes, lifecycle state matrices,
source-record discovery and owner constraints, public `QUESTBOOK.md` listing,
orchestrator alignment notes, RPG unlock bridge handoff, and generated reader
parity handoff in one file.

Those checks share a route, but they do not share one owner boundary. Keeping
them together made the source-record validator a new place for historical
Questbook-adjacent gates to accumulate.

## Options Considered

- Keep `questbook_source.py` and only reduce line count.
- Keep a compatibility facade that delegates to focused modules.
- Remove the aggregate and let `validate_repo.py` coordinate the focused
  validators directly.

## Decision

`scripts/validators/questbook_source.py` is removed.

Active Questbook source-fast validation now routes through focused modules:

- `questbook_schema_lifecycle.py` owns quest and dispatch schema envelope checks
  plus the lifecycle state matrix.
- `questbook_source_records.py` owns authored quest source-record discovery,
  source-record shape, owner constraints, strict orchestrator ref handoff, and
  expected projection entries.
- `questbook_obligation_index.py` owns public `QUESTBOOK.md` active/closed
  listing posture, integration-note tokens, and orchestrator alignment-note
  presence/tokens.
- `questbook_projection_parity.py` owns generated catalog/dispatch parity.
- `questbook_progression.py` owns the Questbook-linked RPG unlock/progression
  bridge support surface.

`scripts/validate_repo.py` coordinates these focused validators for repository
validation. It passes the source-record result into obligation-index,
progression, and generated parity checks without making any focused module own
the others' meaning.

## Rationale

The source quest record is authored truth. The generated catalog and dispatch
files are projections. The public obligation index is a reviewability surface.
The lifecycle matrix is a state contract. The RPG unlock bridge and strict
orchestrator references are cross-owner capability/support checks.

Combining those layers under a single source validator hid the failure route.
Splitting them makes the boundary actionable: repair schema/lifecycle, source
records, public listing, generated parity, or cross-owner support according to
the failing module.

## Consequences

- Positive: no Questbook source aggregate remains after the facade and
  projection aggregate removals.
- Positive: generated parity and RPG progression bridge checks are still
  blocking, but their owners remain explicit.
- Positive: tests use a local helper to exercise the full Questbook repo route
  while production validation imports focused modules directly.
- Tradeoff: `validate_repo.py` now carries a few more explicit handoff calls.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook source records, lifecycle posture, public obligation
  visibility, generated readers, and linked progression/orchestrator support
  remain source-fast gates.
- Changed: the broad `questbook_source.py` module no longer exists.
- Supersedes: AOA-EV-D-0170 for the aggregate source-validator shape.

## Boundaries

This decision does not move quest meaning into generated readers, RPG
progression, orchestrator class catalogs, runtime dispatch, live task
assignment, proof-surface promotion, owner acceptance, or final quest movement.

It also does not create a new Questbook compatibility facade. The only shared
Questbook helper behavior first lived in `questbook_common.py`; AOA-EV-D-0219
later split it into focused helper modules, and those modules must remain
helper-only.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
