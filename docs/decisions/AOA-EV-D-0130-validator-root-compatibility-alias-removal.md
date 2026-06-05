# Validator Root Compatibility Alias Removal

- Decision ID: AOA-EV-D-0130
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validate_repo.py`, `scripts/validators/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: proof-object, proof-infra, publication-receipts, audit, boundary-bridge, cross-parent
- Guard families: source/topology, projection/generated, release/nightly
- Posture: active rationale

## Context

Several focused validator modules were split out of `scripts/validate_repo.py`.
The first landing preserved compatibility aliases in the root entrypoint so
tests could continue importing old `*_NAME` and `*_REQUIRED_TOKENS` constants.

That compatibility layer became stale surface area. It kept historical owner
knowledge visible in the root file after the focused modules already owned it.

## Decision

`scripts/validate_repo.py` no longer re-exports compatibility aliases for the
focused validator modules.

Tests and fixtures import constants from their owner modules directly:

- `scripts/validators/audit.py`
- `scripts/validators/boundary_bridge.py`
- focused decision-index validator modules
- `scripts/validators/docs_routes.py`
- `scripts/validators/docs_topology.py`
- `scripts/validators/eval_bundles.py`
- `scripts/validators/generated_parity.py`
- `scripts/validators/mechanics.py`
- `scripts/validators/proof_infra.py`
- `scripts/validators/proof_loop.py`
- `scripts/validators/proof_object.py`
- `scripts/validators/phase_alpha_matrix.py`
- focused Questbook helper modules
- `scripts/validators/questbook_projection.py`
- `scripts/validators/questbook_progression.py`
- `scripts/validators/questbook_routes.py`
- `scripts/validators/questbook_source.py`
- `scripts/validators/report_index.py`
- `scripts/validators/root_authority.py`
- `scripts/validators/runtime_candidates.py`
- `scripts/validators/source_doctrine.py`
- `scripts/validators/titan.py`

Root validation may still call focused validator functions or read a module
constant directly for an unsplit live gate, but it must not recreate a
top-level compatibility alias solely for old import convenience.

## Rationale

Validator modules are owner organs, not hidden appendices of the root
validator. If tests keep importing owner constants through `validate_repo.py`,
the root file remains a historical script pile even after behavior moves out.

Direct owner imports make the boundary visible in the tests and remove one
source of future alias drift.

## Consequences

- Positive: root compatibility alias assignments and broad owner-module
  re-export imports were removed.
- Positive: tests now name the focused validator owner for these constants.
- Positive: future splits should update tests and imports during the same
  change instead of preserving old root aliases.
- Tradeoff: older external imports of these constants from `scripts/validate_repo.py`
  are intentionally not preserved.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: focused validator constants are imported from focused modules, not
  re-exported by root.
- Refined by: AOA-EV-D-0193 removes the remaining Questbook compatibility
  facade and keeps Questbook callers on focused modules.
- Refined by: AOA-EV-D-0218 removes the decision-index validator aggregate and
  keeps decision-index callers on focused modules.
- Refined by: AOA-EV-D-0219 removes the Questbook helper aggregate and keeps
  Questbook callers on focused helper modules.

## Boundaries

This decision does not remove the `scripts/validate_repo.py` command.

It does not force unsplit live gates to move before their owner boundary is
clear.

It does not create compatibility aliases in another file.

## Validation

- `python -m pytest -q tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py tests/test_route_residue.py tests/test_quest_and_reader_surfaces.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
