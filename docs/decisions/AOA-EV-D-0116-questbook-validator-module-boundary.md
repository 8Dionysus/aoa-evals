# Questbook Validator Module Boundary

- Decision ID: AOA-EV-D-0116
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/questbook.py`, `scripts/validate_repo.py`, `mechanics/questbook/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, root/topology, generated/readout
- Mechanic parents: questbook, rpg, cross-parent
- Guard families: questbook/source, generated/report/receipt/runtime
- Posture: active rationale

## Context

The validator, test, and script refactor made validation lanes visible, but
`scripts/validate_repo.py` still carried historical domain rules directly.
Questbook validation was a coherent boundary inside that monolith: it checked
quest source records, quest lifecycle route law, generated quest catalog and
dispatch parity, orchestrator proof anchors, and RPG unlock proof bridge
surfaces.

That pressure is not a reason to delete the checks. It is a reason to name the
boundary they protect.

## Options Considered

- Keep questbook validation inside `scripts/validate_repo.py` until a larger
  source/topology split.
- Move questbook checks into a broad `source_topology` module with unrelated
  route-card contracts.
- Move questbook checks into `scripts/validators/questbook.py` and keep
  `scripts/validate_repo.py` as the compatibility entrypoint and orchestrator.

## Decision

Questbook source, projection, and unlock proof bridge checks live in
`scripts/validators/questbook.py`.

`scripts/validate_repo.py` remains the repo-wide validator entrypoint and
re-exports the questbook helper functions used by existing builders and tests.

The new module is classified in validator inventory, script inventory, and the
residual root-authored surface ledger so it cannot become a hidden standalone
gate.

## Rationale

Questbook checks sit at the boundary between source records and generated
dispatch readers. Keeping them in a named module makes the owner route explicit:
source meaning stays with `QUESTBOOK.md`, `quests/`, and `mechanics/questbook/`;
generated readers prove projection parity; RPG unlock proof bridge surfaces keep
their own bounded progression evidence posture.

This preserves the local proof canon without creating a generic
`validate_everything.py` replacement.

## Consequences

- Positive: one more coherent domain moved out of the root validator.
- Positive: questbook projection parity is named without promoting generated
  readers into source meaning.
- Tradeoff: `scripts/validate_repo.py` keeps compatibility re-exports until
  callers move to direct module imports.
- Follow-up: continue extracting the next coherent domain from
  `scripts/validate_repo.py`, especially repo-wide evidence/readout surfaces.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the single repo-wide
  validation entrypoint.
- Changed: questbook source/projection checks now have a focused validator
  module under `scripts/validators/`.
- Superseded by: none.

## Boundaries

This decision does not change eval bundle meaning, quest state semantics,
orchestrator capability truth, RPG runtime activation policy, or generated
reader authority.

It does not make questbook validation a separate release command. Lane command
authority remains in `docs/validation/validation_lanes.json`.

## Validation

- `python -m pytest -q tests/test_quest_and_reader_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
