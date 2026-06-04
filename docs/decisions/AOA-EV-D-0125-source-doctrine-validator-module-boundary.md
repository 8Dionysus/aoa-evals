# Source Doctrine Validator Module Boundary

- Decision ID: AOA-EV-D-0125
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/source_doctrine.py`, `evals/`, `docs/guides/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, source/topology, comparison/readout, report/readout
- Mechanic parents: proof-object, comparison-spine, proof-infra, audit, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

Several authored-source doctrine checks still lived directly in
`scripts/validate_repo.py`:

- comparison doctrine and selection/index parity;
- artifact/process separation guide and bundle wording;
- repeated-window discipline guide and longitudinal bundle wording;
- integrity risk taxonomy schema/example wording for
  `aoa-eval-integrity-check`.

These checks align source bundles and guides. They are not generated parity,
runtime policy, receipt publication, release evidence, or broad audit reports.

## Options Considered

- Keep the checks in `scripts/validate_repo.py`.
- Fold them into comparison-spine, audit, or proof-infra validator modules.
- Move guide and source-bundle doctrine checks into
  `scripts/validators/source_doctrine.py` while keeping bundle shape and
  generated projection checks in their existing lanes.

## Decision

Source doctrine validation lives in `scripts/validators/source_doctrine.py`.

`scripts/validate_repo.py` keeps compatibility wrappers for
`validate_comparison_doctrine_surfaces`,
`validate_artifact_process_doctrine_surfaces`,
`validate_repeated_window_doctrine_surfaces`, and
`validate_integrity_taxonomy_surfaces`.

The module owns authored guide, selection/index, source bundle wording, and
integrity taxonomy alignment checks.

## Rationale

Source doctrine is a boundary around authored meaning. It asks whether a guide,
selection route, index route, bundle wording, and schema/example vocabulary are
aligned.

It should stay separate from generated validators because generated readers
must not define source meaning. It should also stay separate from runtime and
audit validators because these checks do not inspect a live run, receipt, trace,
or approval decision.

## Consequences

- Positive: source guide and bundle doctrine checks leave the root validator.
- Positive: comparison/readout doctrine remains below authored source meaning
  and outside generated parity.
- Tradeoff: wrappers remain in `scripts/validate_repo.py` because tests still
  call the root functions.
- Follow-up: source bundle contract checks can move later if the split keeps
  bundle topology, guide doctrine, and generated projections distinct.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: guide and source-bundle doctrine checks now have a focused validator
  module.
- Superseded by: none.

## Boundaries

This decision does not move bundle parsing, bundle schema validation, generated
catalog parity, runtime integrity review, receipt publication, or release
evidence into source-doctrine.

It does not make comparison, repeated-window, or integrity taxonomy guides
stronger than bundle-local source truth.

## Validation

- `python -m pytest -q tests/test_comparison_surface_contracts.py tests/test_validate_repo.py tests/test_report_schema_contracts.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
