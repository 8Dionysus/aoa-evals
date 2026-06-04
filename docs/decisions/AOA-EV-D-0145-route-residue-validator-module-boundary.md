# Route Residue Validator Module Boundary

- Decision ID: AOA-EV-D-0145
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/route_residue.py`, route residue guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, projection/generated
- Posture: active rationale

## Context

The route residue guard family protects the boundary between route-card-only
root districts, active mechanic parents, generated/readout references, source
eval bundles, repo config, decision records, and mechanic payloads.

Before this split, `scripts/validate_repo.py` held the full residue scanner:
generated/readout JSON walking, active mechanic route-card checks,
root-authored doc checks, decision-route checks, repo-config checks,
source-bundle checks, mechanic-payload checks, structured manifest route checks,
and all decision-token matrices.

That was too much root memory. The root entrypoint remembered every residue
mode instead of delegating to one boundary organ.

## Decision

Route residue validation lives in `scripts/validators/route_residue.py`.

The module owns the generated/readout, active mechanic, root-authored,
decision, repo-config, source-bundle, mechanic-payload, and structured
manifest route-residue checks. It imports active mechanic parent topology from
`scripts/validators/mechanics.py` and root route-card-only district topology
from `scripts/validators/root_route_cards.py`.

`scripts/validate_repo.py` delegates through the module and injects only the
shared token lookup context.

## Rationale

Route residue is one coherent boundary: it prevents stale root payload homes
and legacy mechanic parent paths from becoming current authority. It is not
source proof meaning, generated parity ownership, release packaging, or runtime
policy enforcement.

Moving the family as a unit removes historical gate clutter from the root
entrypoint while preserving the guard as a hard source-fast check.

## Consequences

- Positive: route-residue behavior now has one focused module and one test
  import path.
- Positive: `validate_repo.py` no longer exports residue constants or wrapper
  validators.
- Positive: mechanic parent topology is read from `validators/mechanics.py`
  rather than copied into root.
- Follow-up: remaining root-owned mechanics topology helpers can be split next
  when their owner boundary is equally coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: route-card-only districts and legacy mechanic parent paths must
  not be used as current authority.
- Changed: route residue validation moved from `scripts/validate_repo.py` to
  `scripts/validators/route_residue.py`.
- Superseded by: none.

## Boundaries

This decision does not make generated validators define source meaning.

It does not promote route residue checks to runtime policy enforcement,
capability authorization, release artifact freeze, or trace/eval outcome
grading.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/route_residue.py tests/test_generated_route_residue.py tests/test_route_residue.py`
- `python -m pytest -q tests/test_generated_route_residue.py tests/test_route_residue.py`
