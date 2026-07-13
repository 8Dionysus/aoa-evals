# Questbook Source Validator Boundary

- Decision ID: AOA-EV-D-0170
- Status: Superseded
- Superseded by: AOA-EV-D-0208-questbook-source-aggregate-removal
- Date: 2026-06-04
- Owner surface: `scripts/validators/questbook_source.py`, `mechanics/questbook/parts/source-record-contract/README.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model
- Mechanic parents: questbook, cross-parent
- Guard families: source/topology, projection/generated, trace/eval
- Posture: active rationale

## Context

`scripts/validators/questbook.py` still carried Questbook route-card checks,
part owner-split checks, source quest record schema checks, lifecycle posture,
active/closed Questbook listing rules, orchestrator-proof source constraints,
and the handoff into generated reader parity.

Earlier splits moved RPG progression bridge checks and generated quest reader
parity into focused modules. The remaining source-record checks were still large
enough to keep `questbook.py` as a historical mixed validator.

## Decision

Questbook source record, schema, and lifecycle validation lives in
`scripts/validators/questbook_source.py`.

The module owns:

- quest source record discovery and duplicate/foundation id checks;
- quest and dispatch schema envelope checks;
- `quests/LIFECYCLE.md` state matrix checks;
- active and closed quest listing posture in `QUESTBOOK.md`;
- source-record repo/id/public_safe/path-shape checks;
- source-record owner constraints for orchestrator proof, progression evidence,
  and unlock proof bridge quests; and
- the source-to-generated handoff into Questbook projection parity.

Historical compatibility adapters were removed later by AOA-EV-D-0193; source
callers import `questbook_source.py` directly.

## Rationale

Quest route cards and Questbook part contracts are one boundary. Source quest
records and lifecycle state posture are a tighter source-record boundary. Keeping
them in one validator made Questbook look like a place to accumulate every
historical obligation connected to a quest.

The source validator can call the projection validator because source records
must remain synchronized with generated readers. That call is a handoff, not a
transfer of meaning: generated readers remain projections, and source quest
records remain the authored truth.

## Consequences

- Positive: `questbook_source.py` owns source-record behavior directly rather
  than hiding it behind a Questbook facade.
- Positive: Questbook source-record checks have their own validator, inventory
  entry, mechanics ledger row, and decision rationale.
- Tradeoff: `questbook_source.py` still calls the projection validator during
  source-fast validation to keep generated readers synchronized.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook source records must remain schema-backed, lifecycle
  aligned, and reflected in the public obligation index.
- Changed: source-record, schema-envelope, lifecycle, active/closed listing, and
  source owner-constraint logic first moved out of `questbook.py`; the later
  active route split them again into `questbook_schema_lifecycle.py`,
  `questbook_source_records.py`, and `questbook_obligation_index.py`.
- Superseded by: AOA-EV-D-0208 removes the `questbook_source.py` aggregate.
- Further changed by: AOA-EV-D-0193 removes the remaining `questbook.py`
  compatibility facade; AOA-EV-D-0197 removes the projection aggregate.

## Boundaries

This decision does not make a Questbook source validator the owner of generated
quest reader meaning, live task assignment, runtime dispatch, proof-surface
promotion, owner acceptance, final quest state movement, RPG progression
semantics, or sibling orchestrator ownership.

Generated reader parity routes to
`scripts/validators/questbook_projection_parity.py`; projection builders route
to `scripts/validators/questbook_projection_records.py`; strict sibling
orchestrator refs route to `scripts/validators/questbook_orchestrator_refs.py`.
Questbook-linked RPG progression/unlock support routes to
`scripts/validators/questbook_progression.py`. Active source schema/lifecycle,
source-record, and obligation-index checks route to
`scripts/validators/questbook_schema_lifecycle.py`,
`scripts/validators/questbook_source_records.py`, and
`scripts/validators/questbook_obligation_index.py`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
