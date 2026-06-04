# Source Eval Contract Validator Boundary

- Decision ID: AOA-EV-D-0151
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_contracts.py`, source eval proof-object contract guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Source eval bundle-core validation protects the authored proof object inside
`evals/<kind>/<name>/`. The guarded surfaces include bundle-local `EVAL.md`,
`eval.yaml`, evidence references, dependency refs, report contracts, fixtures,
runners, proof artifacts used to build catalog records, and command ownership
inside source `EVAL.md` files.

Before this split, `scripts/validate_repo.py` owned these checks beside public
source-entry topology, generated projection parity, mechanics route checks,
runtime-adjacent audit checks, and release-support gates. That kept the root
entrypoint large enough to hide owner boundaries.

## Decision

Source eval proof-object contract validation lives in
`scripts/validators/source_eval_contracts.py`.

The module owns:

- source eval record parsing from bundle-local `EVAL.md` and `eval.yaml`;
- frontmatter, manifest, required-section, and evidence contract checks;
- dependency drift and dependency target reachability checks for technique and
  skill refs;
- comparison surface, report schema, example report, actual report, fixture,
  runner, and proof artifact contract checks;
- source `EVAL.md` executable command ownership checks;
- source eval discovery and catalog-record source APIs used by generated
  builders and tests;
- source-bundle claim-boundary checks that prevent overclaiming longitudinal
  growth from local proof artifacts.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain to the module. `scripts/build_catalog.py` and tests import the focused
module directly instead of depending on root wrappers.

## Rationale

These checks are source/topology boundaries for authored proof objects. They
decide whether a bundle is internally coherent and whether generated projections
can be rebuilt from it without letting generated readers define source meaning.

They do not define public source-entry topology, generated catalog freshness,
report-index freshness, release-artifact freeze, runtime policy, trace grading,
or eval outcome quality. Keeping this boundary focused stops the root validator
from becoming a historical collection of every source-eval proof rule.

## Consequences

- Positive: `validate_repo.py` no longer exports source eval record, catalog,
  dependency, report, fixture, runner, or proof-artifact contract helpers.
- Positive: catalog builders and tests now depend on the source eval contract
  module as the source API for authored bundle records.
- Positive: validation inventories and the residual root-authored ledger name
  this module as a focused source-fast boundary.
- Follow-up: future runtime policy, trace/eval, release, and generated parity
  checks must stay in their own owner lanes instead of expanding this module.

## Current Applicability

As of 2026-06-04:

- Still valid: bundle-local source eval proof objects must satisfy their
  manifest, markdown, evidence, dependency, report, fixture, runner, and proof
  artifact contracts before generated readers can project them, and executable
  validation commands must route to `evals/AGENTS.md` or the nearest route card.
- Changed: source eval bundle-core contract checks moved from
  `scripts/validate_repo.py` to `scripts/validators/source_eval_contracts.py`.
- Superseded by: none.

## Boundaries

This decision does not let source eval contract validators own generated reader
freshness or generated parity.

It does not own public source eval entry topology; that remains in
`scripts/validators/eval_bundles.py`.

It does not validate runtime guardrails, tool permissions, trace completeness,
grader outcomes, release packaging, or frozen artifact provenance.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/source_eval_contracts.py scripts/build_catalog.py`
- `python -m pytest -q tests/test_build_catalog.py tests/test_downstream_feed_contracts.py tests/test_validate_repo.py tests/test_runtime_evidence_surfaces.py tests/test_eval_source_topology.py tests/test_report_schema_contracts.py mechanics/proof-object/parts/eval-authoring/tests/test_scaffold_eval_bundle.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
