# Questbook Projection Validator Boundary

- Decision ID: AOA-EV-D-0163
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused Questbook projection validators, `mechanics/questbook/parts/dispatch-reader/README.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/read-model, source/topology
- Mechanic parents: questbook, cross-parent
- Guard families: projection/generated, source/topology
- Posture: active rationale

## Context

`scripts/validators/questbook.py` still carried Questbook route checks, source
record checks, generated catalog/dispatch builders, generated parity checks, and
the strict sibling orchestrator-class bridge.

That kept two owner surfaces in one validator:

- Questbook source/route contract: source quest records, route cards, lifecycle
  posture, and part owner-split contracts; and
- generated Questbook reader contract: catalog/dispatch projection parity and
  optional strict sibling orchestrator reference compatibility.

The generated reader is important, but it must not become the authority for
quest meaning or live task assignment.

## Decision

Questbook generated projection validation lives in
`scripts/validators/questbook_projection.py`.

The module owns:

- quest source discovery and foundation quest presence for projection builds;
- source-record schema validation needed before generating reader entries;
- expected generated quest catalog and dispatch entry construction;
- generated catalog/example parity;
- generated dispatch/example parity and dispatch schema checks; and
- strict sibling orchestrator-class reference checks when
  `AOA_EVALS_STRICT_SIBLING_COMPAT` is enabled.

Focused source-record validation owns source records, schema/lifecycle
validation owns lifecycle posture, and `scripts/validate_repo.py` calls
generated parity for the source-to-generated handoff. Historical compatibility
adapters were removed later by AOA-EV-D-0193.

## Rationale

Generated Questbook files are read models. They should be traceable to source
quest records and schema-backed build logic, but they should not define source
meaning. Moving projection logic into its own validator makes the rebuild-parity
boundary explicit and stops the source/route validator from becoming a broad
historical gate.

The strict orchestrator bridge also belongs here because it checks whether a
projected quest reference can resolve to a sibling generated catalog in strict
mode. It does not move orchestrator-class ownership into aoa-evals.

## Consequences

- Positive: `questbook_projection.py` owns generated reader parity directly
  while focused source validators own source records and lifecycle posture and
  `questbook_routes.py` owns route cards and part contracts.
- Positive: generated catalog/dispatch parity has a dedicated validator,
  inventory entry, mechanics ledger row, and decision rationale.
- Tradeoff: the source-fast route still calls generated parity because source
  quest records and generated readers must stay synchronized.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook generated readers must remain exact projections of
  source quest records and schema-backed dispatch rules.
- Changed: generated projection logic moved out of `questbook.py` and into
  `questbook_projection.py`; source-record and lifecycle logic later moved to
  `questbook_source.py` under AOA-EV-D-0170, then split again under
  AOA-EV-D-0208.
- Superseded by: AOA-EV-D-0193 removes the remaining `questbook.py`
  compatibility facade.
- Further changed by: AOA-EV-D-0197 removes `questbook_projection.py`; active
  projection behavior now routes to `questbook_projection_records.py`,
  `questbook_projection_parity.py`, and `questbook_orchestrator_refs.py`.
  AOA-EV-D-0208 moves the active source-to-generated handoff into
  `validate_repo.py`.

## Boundaries

This decision does not make generated quest readers the source of quest meaning,
live task assignment, runtime dispatch, proof-surface promotion, owner
acceptance, final quest state movement, or sibling orchestrator ownership.

It does not move Questbook route cards, source-record lifecycle posture, part
owner-split contracts, or RPG progression/unlock bridge checks into the focused
projection modules. Source-record lifecycle posture routes to
`scripts/validators/questbook_schema_lifecycle.py` and source-record posture
routes to `scripts/validators/questbook_source_records.py`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
