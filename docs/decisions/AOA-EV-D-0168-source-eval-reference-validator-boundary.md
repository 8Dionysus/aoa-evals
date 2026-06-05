# Source Eval Reference Validator Boundary

- Decision ID: AOA-EV-D-0168
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_references.py`, source eval dependency, relation, and tree-location guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-object
- Guard families: source/topology
- Posture: active rationale

## Context

After the source eval artifact and evidence splits,
`scripts/validators/source_eval_contracts.py` still carried reference checks
beside `EVAL.md` parsing and manifest/frontmatter schema validation:

- technique dependency normalization and drift checks;
- skill dependency normalization and drift checks;
- dependency target reachability against sibling repo roots;
- cross-eval relation integrity; and
- source eval claim-family tree location.

Those checks protect references out of the source eval bundle. They are
source-fast, but they are not the same boundary as parsing the proof object,
validating schema shape, evidence sufficiency, or bundle-local artifact shape.

## Decision

Source eval dependency, relation, and tree-location validation lives in
`scripts/validators/source_eval_references.py`.

The module owns:

- ordered technique and skill dependency drift checks between frontmatter and
  `eval.yaml`;
- dependency target reachability for configured `AOA_TECHNIQUES_ROOT` and
  `AOA_SKILLS_ROOT`;
- cross-eval relation self-target, missing-target, and duplicate checks; and
- claim-family source tree location checks.

`scripts/validators/source_eval_contracts.py` remains the source eval
proof-object orchestrator. It keeps compatibility adapters for existing helper
names and delegates reference checks to `source_eval_references.py` during
bundle validation.

## Rationale

Dependency refs and relation targets are authority edges. They should be
validated as source contracts, but they should not make the proof-object parser
own sibling repo reachability or cross-bundle topology.

The split keeps four adjacent source-fast questions separate:

- `source_eval_contracts.py`: is the source proof object structurally coherent?
- `source_eval_references.py`: do dependency, relation, and tree-location refs
  resolve through the right authority?
- `source_eval_evidence.py`: is the authored evidence/review posture sufficient?
- `source_eval_report_artifacts.py`: are materialized report artifacts coherent?
- `source_eval_fixture_contracts.py`: are fixture contracts coherent?
- `source_eval_runner_contracts.py`: are runner contracts coherent?

## Consequences

- Positive: reference checks have a named validator, inventory entries,
  mechanics ledger row, and decision rationale.
- Positive: `source_eval_contracts.py` focuses more tightly on source record
  parsing, schema validation, command ownership, comparison-surface shape, and
  catalog-record APIs.
- Positive: existing callers can still import reference helper names from
  `source_eval_contracts.py` through thin compatibility adapters.
- Tradeoff: `source_eval_contracts.py` still calls the reference validator
  during aggregate bundle validation because generated projections must only
  build from bundles whose reference edges are coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: source eval dependency refs, relations, and claim-family tree
  location must be coherent before catalog records are projected.
- Changed: dependency, relation, and tree-location logic moved out of
  `source_eval_contracts.py` and into `source_eval_references.py`.
- Superseded by: none.

## Boundaries

This decision does not let `source_eval_references.py` define `EVAL.md`
frontmatter parsing, manifest schema meaning, evidence policy, bundle artifact
contracts, generated reader freshness, release packaging, runtime policy, trace
grading, or eval outcome quality.

It does not move comparison-surface shape checks out of
`source_eval_contracts.py`.

## Validation

- `python -m py_compile scripts/validators/source_eval_references.py scripts/validators/source_eval_evidence.py scripts/validators/source_eval_report_artifacts.py scripts/validators/source_eval_fixture_contracts.py scripts/validators/source_eval_runner_contracts.py`
- `python -m pytest -q tests/test_build_catalog.py tests/test_validate_repo.py tests/test_eval_source_topology.py tests/test_downstream_feed_contracts.py`
