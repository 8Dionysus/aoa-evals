# Source Eval Artifact Validator Boundary

- Decision ID: AOA-EV-D-0159
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused source eval artifact validators, bundle-local source eval artifact contract guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-infra, proof-object
- Guard families: source/topology
- Posture: active rationale

## Context

After the source eval contract split, `scripts/validators/source_eval_contracts.py`
still carried bundle-local report, fixture, runner, and proof-artifact checks
beside `EVAL.md` parsing, `eval.yaml` validation, dependency drift checks,
relations, and catalog-record APIs.

That made one validator own two different source-fast boundaries:

- source proof-object record coherence; and
- materialized bundle support artifact contracts.

The artifact checks read proof-infra schemas and bundle-local support files.
They do not decide the meaning of `EVAL.md`, `eval.yaml`, dependency refs, or
generated reader freshness.

## Decision

Bundle-local source eval artifact contract validation lives in
`scripts/validators/source_eval_artifacts.py`.

The module owns:

- `evals/<family>/<eval>/reports/summary.schema.json` and
  `evals/<family>/<eval>/reports/example-report.json` pairing;
- actual `evals/<family>/<eval>/reports/*.report.json` validation against the
  bundle schema;
- comparative-summary report mode pins;
- longitudinal-window report overclaim and window-order guards;
- `evals/<family>/<eval>/fixtures/contract.json` schema validation and
  repo-relative support refs;
- `evals/<family>/<eval>/runners/contract.json` schema validation and
  repo-relative support refs;
- required materialized proof artifacts for comparative-summary bundles.

Shared source-eval schema, JSON/YAML, issue-formatting, and display helpers
live in `scripts/validators/source_eval_common.py`. That helper has no proof
meaning authority.

`scripts/validators/source_eval_contracts.py` remains the source eval
proof-object orchestrator and calls the artifact validator during record
collection.

## Rationale

Artifact contracts are authored source checks, but they are not the same owner
surface as source record parsing and dependency reachability. Separating them
keeps reports, fixtures, and runners from becoming another historical block
inside a broad source validator.

The split also makes the proof-infra boundary explicit: shared schemas can
constrain bundle-local artifact shape without letting generated readers or
runtime results define source proof meaning.

## Consequences

- Positive: `source_eval_contracts.py` no longer contains report, fixture,
  runner, or longitudinal report artifact logic.
- Positive: tests for longitudinal report overclaim behavior import the
  artifact validator directly.
- Positive: validation topology and mechanics residual ledgers classify
  artifact contracts separately from source record contracts.
- Tradeoff: `source_eval_contracts.py` still orchestrates artifact validation
  during `collect_catalog_records` because generated projections must only
  build from bundles whose support artifacts are coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: bundle-local support artifacts must validate before catalog
  records are accepted for generated projections.
- Changed: artifact contract logic moved out of `source_eval_contracts.py` and
  into `source_eval_artifacts.py`.
- Further changed by: AOA-EV-D-0199 removes `source_eval_artifacts.py`; active
  behavior now routes to `source_eval_report_artifacts.py`,
  `source_eval_fixture_contracts.py`, and `source_eval_runner_contracts.py`.
- Superseded by: AOA-EV-D-0199 for the active module shape.

## Boundaries

This decision does not let source eval artifact validators define `EVAL.md`
source meaning, manifest dependency semantics, public chooser posture, generated
freshness, release packaging, runtime policy, trace grading, or eval outcome
quality.

It checks bundle-local materialized artifact contracts only.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
