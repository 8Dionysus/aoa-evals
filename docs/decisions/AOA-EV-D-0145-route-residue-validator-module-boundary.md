# Route Residue Validator Module Boundary

- Decision ID: AOA-EV-D-0145
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused route residue guard family modules

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

The module owns the route residue guard family and initially owned the
generated/readout, active mechanic, root-authored, decision, repo-config,
source-bundle, mechanic-payload, and structured manifest route-residue checks.
It imports active mechanic parent topology from `scripts/validators/mechanics.py`
and root route-card-only district topology from
`scripts/validators/root_route_cards.py`.

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

## Review Log

### 2026-06-04 - Generated and mechanic-payload residue split

- Previous assumption: `route_residue.py` owned every route residue domain as
  implementation logic.
- New reality: generated/readout residue lives in
  `scripts/validators/route_residue_generated.py`; mechanic-payload and
  structured manifest route-field residue lives in
  `scripts/validators/route_residue_mechanic_payload.py`; shared context and
  token normalization live in `scripts/validators/route_residue_common.py`.
- Reason: generated read models and mechanic payload files are different owner
  surfaces with different failure routes and allowances.
- Source surfaces updated: `scripts/validators/route_residue.py`,
  `scripts/validators/route_residue_generated.py`,
  `scripts/validators/route_residue_mechanic_payload.py`,
  `scripts/validators/route_residue_common.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Current Applicability

As of 2026-06-04:

- Still valid: route-card-only districts and legacy mechanic parent paths must
  not be used as current authority.
- Changed: route residue validation moved from `scripts/validate_repo.py` to
  `scripts/validators/route_residue.py`; generated/readout and mechanic-payload
  residue logic later moved to focused route-residue domain validators.
- Changed: AOA-EV-D-0192 removes the remaining `route_residue.py` aggregate
  facade.
- Superseded by: AOA-EV-D-0167 for route-residue domain boundaries and
  AOA-EV-D-0192 for facade removal.

## Boundaries

This decision does not make generated validators define source meaning.

It no longer makes `route_residue.py` the implementation owner of any residue
domain; focused `route_residue_*.py` modules own their domains.

It does not promote route residue checks to runtime policy enforcement,
capability authorization, release artifact freeze, or trace/eval outcome
grading.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
