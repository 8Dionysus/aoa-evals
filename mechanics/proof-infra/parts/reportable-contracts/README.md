# Reportable Contracts

## Role

`reportable-contracts/` owns the shared reportable proof contract surfaces for
`aoa-evals`.

It is a part of `proof-infra`, not a parent mechanic. It is not a bundle, a
repo-global score, a hidden runner implementation, or a report verdict.

## Owned Operation

`bundle report need -> shared reportable proof contract -> bundle-local runner contract -> schema-backed report artifact -> generated proof_artifacts`

The bundle owns the bounded claim and report interpretation. This part owns the
shared runner surface, shared scorer helper, and shared schemas that make
bundle-local reportable proof artifacts readable and checkable.

## Source Surfaces

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json`

Each bundle-local runner contract cites the active paths through
`runner_surface_path` and `scorer_helper_paths`. Bundle-local reports still
cite their own `bundles/<bundle>/reports/summary.schema.json` and
`bundles/<bundle>/reports/example-report.json`. The bundle-local
`bundles/<bundle>/EVAL.md` remains the interpretation boundary.

## Inputs

- a source proof bundle with a bounded claim;
- a bundle-local `bundles/<bundle>/fixtures/contract.json` when shared fixture
  support is used;
- a bundle-local `bundles/<bundle>/runners/contract.json` that names this part
  through `runner_surface_path`;
- optional `scorer_helper_paths` for shared bounded breakdown payloads;
- a bundle-local report schema and example report.

## Outputs

- a part-local runner surface for reportable proof discipline;
- a part-local shared scorer helper for repeatable bounded breakdown payloads;
- shared schemas for fixture contracts, runner contracts, and generic summary
  report shape;
- generated catalog `proof_artifacts` derived from bundle-local contracts.

## Stronger Owner Split

This part is weaker than:

- `bundles/*/EVAL.md` and `bundles/*/eval.yaml`;
- bundle-local report schemas, examples, and reviewed reports;
- comparison-spine semantics;
- audit candidate-evidence interpretation;
- publication receipts;
- sibling owner truth.

## Stop-Lines

- Do not turn the scorer helper into a repo-global score.
- Do not make the shared runner surface stronger than bundle-local
  interpretation.
- Do not weaken shared schemas to pass a weak report.
- Do not recreate root `runners/`, `scorers/`, or `schemas/` active payload
  aliases.
- Do not use this part to absorb bundle-local report schemas or reviewed
  report artifacts.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py tests/test_build_catalog.py tests/test_validate_repo.py
```
