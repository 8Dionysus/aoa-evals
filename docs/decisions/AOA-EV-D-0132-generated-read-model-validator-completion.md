# Generated Read-model Validator Completion

- Decision ID: AOA-EV-D-0132
- Status: Accepted
- Date: 2026-06-03
- Historical owner surface: `scripts/validators/generated_parity.py`, `generated/`
- Refined by: AOA-EV-D-0183, AOA-EV-D-0200

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, generated/readout
- Mechanic parents: proof-object, comparison-spine, questbook, cross-parent
- Guard families: projection/generated, source/topology
- Posture: active rationale

## Context

`scripts/validators/generated_parity.py` already checked generated route-card
surfaces, root generated reader listings, part-local generated directories, and
decision-index notices.

The root validator still owned catalog, min-catalog, capsule, section, and
comparison-spine projection checks. Those checks compare generated read models
against builder output and contract alignment. They do not define source eval
meaning.

## Decision

Catalog, min-catalog, capsule, section, and comparison-spine generated parity
checks live in `scripts/validators/generated_parity.py`.

`scripts/validate_repo.py` supplies a `GeneratedReadModelContext` with the
builder helpers and JSON reader that already belong to the root build/catalog
surface. The focused validator owns parity behavior, not source construction.

## Rationale

Generated validators should prove projection parity and drift, not become a
second source of eval meaning. Keeping these read-model checks in the root
validator preserved historical generated-reader behavior directly in the
entrypoint after more specialized generated surfaces had already moved.

The context boundary avoids copying builder logic into the validator module
while still moving the hard gate out of the root body.

## Consequences

- Positive: generated catalog, capsule, section, and comparison-spine parity
  checks now share the generated/read-model validator owner.
- Positive: `scripts/validate_repo.py` keeps orchestration and builder context
  but no longer owns these generated parity functions.
- Positive: generated readers remain derived from source bundle records and
  builder output.
- Follow-up: specialized generated readers with stronger local owners can keep
  their focused modules instead of folding into a broad bucket.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/build_catalog.py` remains the source builder for these
  generated read models.
- Changed: read-model parity behavior moved from `scripts/validate_repo.py` to
  `scripts/validators/generated_parity.py`.
- Refined on 2026-06-04: AOA-EV-D-0183 removed
  `scripts/validators/generated_parity.py` after moving eval read-model
  projection parity to `scripts/validators/generated_eval_readmodels.py` and
  generated route/topology checks to
  `scripts/validators/generated_route_surfaces.py`.
- Further refined on 2026-06-04: AOA-EV-D-0200 removed
  `scripts/validators/generated_eval_readmodels.py`; active generated eval
  read-model parity is split across catalog, capsule, section, and
  comparison-spine validator modules plus a helper-only common context.
- Superseded by: AOA-EV-D-0183 for the generated-parity aggregate shape;
  AOA-EV-D-0200 for the generated eval read-model aggregate shape.

## Boundaries

This decision does not promote generated catalogs, capsules, sections, or
comparison-spine readers into source truth.

It does not move report-index, runtime-candidate, phase-alpha matrix, quest, or
publication receipt specialized validators back into a generic generated
bucket.

It does not change release or generated lane command authority.

## Validation

- `python -m py_compile scripts/validators/generated_eval_readmodel_common.py scripts/validators/generated_eval_catalogs.py scripts/validators/generated_eval_capsules.py scripts/validators/generated_eval_sections.py scripts/validators/generated_eval_comparison_spine.py scripts/validators/generated_route_surfaces.py scripts/validators/evidence_readouts.py`
- `python -m pytest -q tests/test_generated_parity.py tests/test_build_catalog.py tests/test_downstream_feed_contracts.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
