# Proof Infra / Reportable Contracts Part

## Role

`reportable-contracts/` owns the shared reportable proof contract surfaces for
`aoa-evals`.

It routes bundle report pressure to shared runner, scorer, and schema surfaces
that keep reportable proof artifacts readable while bundle-local interpretation
stays stronger.

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
cite their own `evals/<family>/<eval>/reports/summary.schema.json` and
`evals/<family>/<eval>/reports/example-report.json`. The bundle-local
`evals/<family>/<eval>/EVAL.md` remains the interpretation boundary.

## Inputs

- a source proof bundle with a bounded claim;
- a bundle-local `evals/<family>/<eval>/fixtures/contract.json` when shared fixture
  support is used;
- a bundle-local `evals/<family>/<eval>/runners/contract.json` that names this part
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

This part supplies reusable report contracts. Stronger meaning routes through:

| Meaning pressure | Stronger route |
| --- | --- |
| bounded claim and object under evaluation | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| report interpretation | bundle-local report schemas, examples, and reviewed reports |
| comparison semantics | `mechanics/comparison-spine/` |
| audit candidate-evidence interpretation | `mechanics/audit/` and bundle-local review |
| receipt publication | `mechanics/publication-receipts/` after a reviewed report exists |
| sibling owner truth | the owning sibling repository |

## Stop-Lines

| Pressure | Route |
| --- | --- |
| Repo-global score pressure | bounded claim review in the source bundle; the scorer helper stays a breakdown payload. |
| Shared runner authority pressure | bundle-local interpretation boundary and reviewed report route. |
| Weak report pressure | evidence or schema fit under the source bundle route. |
| Root `runners/`, `scorers/`, or `schemas` alias pressure | route-card-only root districts plus active part-local paths. |
| Bundle-local report schema or reviewed report pressure | the source bundle. |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
