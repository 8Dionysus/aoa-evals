# Source Eval Artifact Aggregate Removal

- Decision ID: AOA-EV-D-0199
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused source eval report, fixture, and runner artifact validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-infra, proof-object
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0159 moved bundle-local artifact checks out of the broad source eval
contract validator. The resulting `scripts/validators/source_eval_artifacts.py`
module still mixed three distinct artifact boundaries:

- report schema/example/actual-report validation, including comparative mode
  pins and longitudinal overclaim guards;
- fixture contract validation and repo-relative fixture-family refs; and
- runner contract validation and repo-relative runner/report/scorer refs.

Those checks all protect bundle-local support artifacts, but they do not share
one owner surface.

## Decision

`scripts/validators/source_eval_artifacts.py` is removed.

Bundle-local source eval artifact validation now routes through focused modules:

- `source_eval_report_artifacts.py` owns report schemas, examples, actual
  reports, comparative-summary mode pins, and longitudinal report claim
  boundaries.
- `source_eval_fixture_contracts.py` owns fixture contract schema validation and
  fixture-family refs.
- `source_eval_runner_contracts.py` owns runner contract schema validation and
  runner/report/scorer refs.
- `source_eval_artifact_common.py` is helper-only shared materialized-comparison
  and repo-relative path logic.

`source_eval_collection.py` calls the focused validators directly during bundle
validation.

## Rationale

Report artifacts, fixture contracts, and runner contracts fail for different
reasons and route to different repair surfaces. Keeping them in one artifact
module made future support-artifact pressure look like a single historical
bucket.

The split keeps source bundle support checks close to their artifact class while
preserving the rule that generated projections only build from coherent source
bundles.

## Consequences

- Positive: no source eval artifact aggregate validator remains.
- Positive: report, fixture, and runner artifact failures now name their
  concrete owner module.
- Positive: common repo-relative helper logic is helper-only and has no proof
  meaning authority.
- Tradeoff: `source_eval_collection.py` imports three focused artifact
  validators because it is the source bundle validation orchestrator.

## Current Applicability

As of 2026-06-04:

- Still valid: bundle-local support artifacts must validate before catalog
  records are accepted for generated projections.
- Changed: source eval artifact behavior no longer lives in
  `source_eval_artifacts.py`; it is split across
  `source_eval_report_artifacts.py`, `source_eval_fixture_contracts.py`, and
  `source_eval_runner_contracts.py`.
- Supersedes: the remaining aggregate shape left by AOA-EV-D-0159.
- Refined by: AOA-EV-D-0226 splits report comparative-mode and longitudinal
  report helpers out of `source_eval_report_artifacts.py`.

## Boundaries

This decision does not let source eval artifact validators define `EVAL.md`
source meaning, manifest dependency semantics, public chooser posture, generated
freshness, release packaging, runtime policy, trace grading, or eval outcome
quality.

It does not create a replacement source eval artifact aggregate under another
name.

## Validation

- `python -m py_compile scripts/validators/source_eval_artifact_common.py scripts/validators/source_eval_report_artifacts.py scripts/validators/source_eval_fixture_contracts.py scripts/validators/source_eval_runner_contracts.py scripts/validators/source_eval_collection.py tests/test_report_schema_contracts.py`
- `python -m pytest -q tests/test_report_schema_contracts.py tests/test_build_catalog.py tests/test_validate_repo.py tests/test_eval_source_topology.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
