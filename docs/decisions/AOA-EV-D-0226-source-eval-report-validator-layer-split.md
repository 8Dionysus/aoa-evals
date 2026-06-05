# Source Eval Report Validator Layer Split

- Decision ID: AOA-EV-D-0226
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused source eval report artifact modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-object, proof-infra, comparison-spine
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0199 removed the broad source eval artifact aggregate. The remaining
`scripts/validators/source_eval_report_artifacts.py` module still mixed report
artifact existence and schema validation with two narrower rules:

- comparative-summary `comparison_mode` pinning against manifest
  `baseline_mode`; and
- longitudinal report claim-boundary, limitation, window id, window order, and
  transition-note checks.

Those rules are report-adjacent, but they fail for different reasons than
schema/example/actual-report existence and manifest drift.

## Decision

Keep `scripts/validators/source_eval_report_artifacts.py` as the blocking
bundle-local report artifact validator.

Split report support rules into helper modules:

- `scripts/validators/source_eval_report_modes.py` owns comparative report
  `comparison_mode` pinning.
- `scripts/validators/source_eval_report_longitudinal.py` owns longitudinal
  report claim-boundary and window-shape checks.
- `scripts/validators/source_eval_report_artifacts.py` owns schema/example
  presence, inline schema validation, actual report validation, and manifest
  drift.

Tests import the longitudinal helper directly for overclaim grammar. No
replacement report aggregate facade is added.

## Rationale

Report artifact existence and schema conformance are source artifact checks.
Comparative mode pinning is a manifest/report consistency rule. Longitudinal
overclaim and window-shape checks are comparison-spine posture rules.

Keeping them in one module made future report policy pressure land in a single
bucket. The split keeps each rule small while preserving the blocking report
artifact entrypoint used by source bundle validation.

## Consequences

- Positive: source report artifact validation is smaller and focused on report
  artifact surfaces.
- Positive: comparative mode and longitudinal claim-boundary helpers are
  non-blocking support surfaces in the inventories.
- Positive: tests no longer import longitudinal grammar through the broad
  report artifact validator.
- Tradeoff: the report artifact validator imports two helper modules.

## Boundaries

This split does not let report helpers define fixture contracts, runner
contracts, `EVAL.md` source meaning, manifest dependency semantics, generated
freshness, release packaging, runtime policy, trace grading, or eval outcome
quality.

It does not create a replacement source eval report aggregate.

## Validation

- `python -m py_compile scripts/validators/source_eval_report_artifacts.py scripts/validators/source_eval_report_longitudinal.py scripts/validators/source_eval_report_modes.py tests/test_report_schema_contracts.py`
- `python -m pytest -q tests/test_report_schema_contracts.py -k "report or longitudinal or comparative"`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
