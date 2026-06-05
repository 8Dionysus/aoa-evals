# Source Eval Domains Validator Boundary

- Decision ID: AOA-EV-D-0158
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_domains.py`, source eval dependency and doctrine validation orchestration

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-infra, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After the root topology split, `scripts/validate_repo.py` still carried
source-eval doctrine orchestration: sibling dependency roots for
`aoa-techniques` and `aoa-skills`, source eval command ownership, focused
comparison doctrine, artifact/process doctrine, repeated-window doctrine,
integrity taxonomy, and shared proof infra checks.

Those checks are source-eval validation behavior, not CLI parsing or output.

## Decision

Source eval dependency and doctrine orchestration lives in
`scripts/validators/source_eval_domains.py`.

The module owns:

- source eval dependency-root mapping from `root_context.py`;
- aggregation of source eval command ownership checks;
- aggregation of focused comparison, artifact/process, repeated-window, and
  integrity taxonomy doctrine checks;
- aggregation of shared proof-infra source checks for selected eval scopes;
- conversion of focused validator issue objects into `ValidationIssue`.

`scripts/validate_repo.py` remains the CLI entrypoint and source eval scope
runner. It asks `source_eval_domains.py` for dependency roots and doctrine
validation when source evals are present.

## Rationale

Source eval doctrine checks validate authored proof contracts and surrounding
source interpretation. They do not define generated freshness, runtime outcomes,
release packaging, or live proof acceptance.

Moving them out of the CLI keeps the root command focused on selecting eval
scope and dispatching to owner-boundary validators.

## Consequences

- Positive: `scripts/validate_repo.py` no longer imports proof-infra or source
  doctrine validators directly.
- Positive: dependency roots for source eval records have a source-eval owner
  instead of living as a CLI helper.
- Tradeoff: this module is intentionally small; it exists to keep source-eval
  doctrine orchestration separate from root command mechanics.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command and eval scope selector.
- Changed: source-eval dependency roots and doctrine aggregation moved to
  `scripts/validators/source_eval_domains.py`.
- Further changed by: AOA-EV-D-0209 removes the broad `source_doctrine.py`
  aggregate while keeping this orchestrator as the source-eval doctrine router.
- Superseded by: none.

## Boundaries

This decision does not let `source_eval_domains.py` define generated projection
freshness, runtime policy acceptance, trace/eval grading, live receipt truth,
release artifact identity, or mechanic payload meaning.

It orchestrates source-eval doctrine validators and dependency-root context
only.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/source_eval_domains.py`
- `python -m pytest -q tests/test_validate_repo.py tests/test_eval_source_topology.py tests/test_comparison_surface_contracts.py`
