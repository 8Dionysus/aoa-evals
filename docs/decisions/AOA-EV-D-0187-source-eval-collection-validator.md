# Source Eval Collection Validator

- Decision ID: AOA-EV-D-0187
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_collection.py`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-object, proof-infra, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After authored record, artifact, evidence, reference, and comparison checks
moved into focused validators, `scripts/validators/source_eval_contracts.py`
still survived as a broad facade. It discovered source eval bundles, assembled
catalog records, exposed compatibility aliases, and re-exported catalog,
capsule, and comparison-spine projection builder helpers.

That shape kept an old validator bucket alive after the owner boundaries were
already visible.

## Decision

Source eval bundle discovery and accepted catalog-record collection live in
`scripts/validators/source_eval_collection.py`.

The module owns:

- source eval bundle directory discovery;
- single-bundle validation orchestration across focused source eval validators;
- accepted `EvalBundleRecord` collection for repo validation and generated
  builders; and
- source-fast formatting for collection failures.

Catalog, capsule, and comparison-spine projections route through direct
`eval_catalog_contract.py`, `eval_capsule_contract.py`, and
`eval_comparison_spine_contract.py` modules.

`scripts/validators/source_eval_contracts.py` is removed after callers move to
the collection module, focused source eval validators, or direct projection
builders.

## Rationale

Collection is a source/topology concern: it decides which authored source eval
records are coherent enough to become inputs for projections.

Projection builders are generated-surface concerns: they derive read models
from accepted records. They should not be hidden behind a validator facade.

Removing the facade prevents old compatibility aliases from becoming the place
where future source eval rules quietly accumulate again.

## Consequences

- Positive: source eval record collection has one owner and one failure route.
- Positive: projection-builder dependencies are explicit and direct.
- Positive: `source_eval_contracts.py` is deleted instead of preserved as a
  compatibility layer.
- Tradeoff: callers that used broad aliases now import the focused owner they
  actually need.

## Current Applicability

As of 2026-06-04:

- Still valid: source eval bundles must satisfy authored record, comparison,
  evidence, artifact, and reference checks before catalog records are accepted.
- Changed: bundle discovery and record collection moved into
  `source_eval_collection.py`; projection builder adapters moved out of
  validator space and into direct `eval_*_contract.py` calls.
- Supersedes: the aggregate/projection-adapter shape left by AOA-EV-D-0151 and
  AOA-EV-D-0178.

## Boundaries

This decision does not let `source_eval_collection.py` own authored record
schema semantics, evidence policy, dependency refs, comparison-surface meaning,
or artifact contracts; those remain with focused source eval validators.

It does not make collection own generated freshness, report-index freshness,
runtime outcomes, trace/eval grading, release packaging, or sibling truth.

It does not introduce compatibility aliases for the removed facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
