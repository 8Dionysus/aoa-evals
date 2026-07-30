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
bundle-local reportable proof artifacts readable and checkable. It also owns
reusable experiment-control shapes when several proof objects need the same
reproducibility and honest run-status boundary.

## Source Surfaces

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/docs/ACTIVE_ORGAN_EXPERIMENT_CONTRACTS.md`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/active-organ-model-prompt-provider-hardware-pin.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/active-organ-memory-experiment-manifest.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/active-organ-memory-run-status-receipt.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/examples/active_organ_experiment_contracts.negative-examples.json`
- `mechanics/proof-infra/parts/reportable-contracts/scripts/validate_active_organ_experiment_contracts.py`
- `mechanics/proof-infra/parts/reportable-contracts/tests/test_active_organ_experiment_contracts.py`

Each bundle-local runner contract cites the primary active paths through
`runner_surface_path` and `report_schema_path`. A bundle with several genuine
execution lanes records the rest through `additional_runner_surface_paths` and
`additional_report_schema_paths`; it does not invent lane-specific schema
keys. Optional `validation_command_templates` keep environment-bound commands
explicit without turning them into evidence of execution.
`scorer_helper_paths` retains shared scoring helpers. Bundle-local reports
still cite their own schemas and example report, while the bundle-local
`evals/<family>/<eval>/EVAL.md` remains the interpretation boundary.

## Inputs

- a source proof bundle with a bounded claim;
- a bundle-local `evals/<family>/<eval>/fixtures/contract.json` when shared fixture
  support is used;
- a bundle-local `evals/<family>/<eval>/runners/contract.json` that names this part
  through `runner_surface_path`;
- optional `scorer_helper_paths` for shared bounded breakdown payloads;
- a bundle-local report schema and example report.
- a preregistered active-organ A/B/C experiment that needs exact model,
  prompt-template, provider, runtime, and host pins;
- run evidence that must distinguish complete, partial, invalid, aborted, and
  blocked execution before bundle-local verdict review;
- a consuming source bundle such as
  `evals/comparison/fixed-baseline/aoa-memo-active-organ-offline-replay/`
  that keeps experiment execution, comparative interpretation, and effect
  authority separate.

## Outputs

- a part-local runner surface for reportable proof discipline;
- a part-local shared scorer helper for repeatable bounded breakdown payloads;
- shared schemas for fixture contracts, runner contracts, and generic summary
  report shape;
- C21-C23 experiment pin, immutable manifest, and run-status receipt contracts
  with reference examples, a canonical C22 normalized self-digest, and
  executable negative mutations;
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
| memory semantics, recall, intervention, lifecycle, or forgetting | `aoa-memo` |
| route admission and orchestration | `aoa-sdk` |
| runtime delivery evidence | `abyss-stack` |
| host capability and resource/storage facts | `abyss-machine` |
| measurement grammar | `aoa-stats` |
| active-organ verdict or benefit | source bundle, admitted evidence, and bundle-local verdict logic |
| production or policy authority | sole operator and named effect owner |

## Stop-Lines

| Pressure | Route |
| --- | --- |
| Repo-global score pressure | bounded claim review in the source bundle; the scorer helper stays a breakdown payload. |
| Shared runner authority pressure | bundle-local interpretation boundary and reviewed report route. |
| Weak report pressure | evidence or schema fit under the source bundle route. |
| Root `runners/`, `scorers/`, or `schemas` alias pressure | route-card-only root districts plus active part-local paths. |
| Bundle-local report schema or reviewed report pressure | the source bundle. |
| Green run-status pressure to claim benefit | source bundle comparison and verdict review; C23 remains execution status only. |
| Schema-valid but post-freeze C22 mutation | recompute the normalized self-digest and fail closed before any run enters comparison. |
| Experiment-control pressure to change memory or production policy | owning sibling contract and operator/effect-owner route. |
| A scored run needs a materially changed pin, manifest, or status meaning | new immutable version or superseding receipt; never coerce the old artifact. |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
