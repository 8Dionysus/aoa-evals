# Mechanic Part Validator Boundary

- Decision ID: AOA-EV-D-0147
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanic_parts.py`, mechanic part contract guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

Mechanic part contracts protect part README shape, source-surface refs, payload
inventory, parent `PARTS.md` synchronization, lower parts index route posture,
and validation command reachability.

Before this split, those checks lived inside `scripts/validate_repo.py` beside
repo-wide orchestration, generated projection checks, legacy bridge checks, and
root topology checks. That made the root validator remember part-local contract
law and decision-token matrices directly.

## Decision

Mechanic part validation lives in `scripts/validators/mechanic_parts.py`.

The module owns:

- parent `PARTS.md` part-contract token checks;
- part README contract checks;
- part payload inventory checks;
- part source-surface ref and Source Surfaces section checks;
- parent `PARTS.md` synchronization checks;
- parent `PARTS.md` and `parts/README.md` index/route heading role checks;
- part validation command reachability and ownership checks.

`scripts/validate_repo.py` delegates to the module through
`validate_mechanic_part_surfaces`. Tests for moved behavior import
`validators/mechanic_parts.py` directly instead of using root compatibility
wrappers.

## Rationale

Mechanic part contracts are mechanic-local boundaries. They decide whether a
part has a readable route, enough source refs, explicit payload ownership, and
reachable validation evidence.

They do not define source eval meaning, generated read-model parity, release
artifact freeze, runtime policy, trace/eval grading, or sibling truth. Keeping
them in a focused module prevents the root validator from accumulating one more
historical gate family.

## Consequences

- Positive: `validate_repo.py` no longer exports mechanic part contract,
  PARTS sync, index-role, or validation command wrappers.
- Positive: part-contract tests now call the owning module directly.
- Positive: script and validator inventories name mechanic part contracts as a
  distinct source-fast surface.
- Follow-up: remaining parent direction, legacy/provenance, and allowlist
  mechanics checks should split only when their owner boundary is equally
  coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parts must keep contract, payload, source-ref, index,
  and validation-route evidence explicit.
- Changed: mechanic part checks moved from `scripts/validate_repo.py` to
  `scripts/validators/mechanic_parts.py`.
- Superseded by: none.

## Boundaries

This decision does not let part validators define part payload meaning. Payload
meaning stays with the owning mechanic part and its source surfaces.

It does not turn part validation commands into release artifact freeze or
runtime policy enforcement.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanic_parts.py`
- `python -m pytest -q tests/test_index_surface_roles.py tests/test_mechanic_part_contracts.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py`
