# Local Eval-Port Decision Matrix

## Role

This matrix tells a fresh agent how repo-local `evals/` ports influence Eval
Forge routing.

Repo-local ports own pressure evidence, intake, suites, reports, and local
fixtures. `aoa-evals` owns central proof doctrine, verdicts, scoring,
regression meaning, and central bundle adoption.

## Live Inventory Boundary

Workspace counts, active-port membership, and current pressure are live read
models, not durable content for this matrix. Inspect them through the local-port
inventory route in `docs/guides/LOCAL_EVAL_PORT_STANDARD.md` and the Eval Forge
operating path. This document keeps only the stable routing distinctions.

## Decision Matrix

| Inventory Route Key | Meaning | Eval Forge Route | Stop-Line |
| --- | --- | --- | --- |
| `missing_no_pressure` | no local port and no current pressure | stop unless current work creates bounded pressure | do not create a port just for symmetry |
| `valid_skeleton_keep_dormant` | valid dormant port with no active pressure | no-op or record current pressure only if new evidence exists | do not invent intake |
| `active_intake_select_then_apply_or_design` | local intake/report pressure exists | `local-intake-pressure-packet`, then select/design review | check central/local duplicates first |
| `active_suite_note_review_or_execution_contract_design` | suite note exists but execution state is `absent` | design/review sidecar | `.suite.md` alone is not runnable |
| `active_suite_contract_invalid_repair` | sidecar schema, path, symlink, argv, or authority guard fails | repair contract | no invocation from invalid state |
| `active_suite_contract_stale_review` | tracked source digest changed | review change and refresh approved hash | no invocation from stale state |
| `active_suite_apply_or_regression_check` | execution state is source-contract-`ready` | owner or `aoa-eval-apply` JIT-revalidates, invokes typed exact argv, and captures environment/receipt | inventory/Forge/readiness never execute; ready is not runtime reproducibility and the suite result is not central verdict |
| `active_reports_only_suite_extraction_or_review` | reports exist without runnable suite | owner review; possibly extract suite | reports are not proof |
| `invalid_active_repair` | active port shape is invalid | repair port shape first | no eval adoption before validator passes |
| `invalid_port_repair` | invalid local port | repair schema/topology | no central adoption from invalid local state |
| `central_overlap_apply_existing_first` | central route likely already exists | inspect/apply central source bundle first | no duplicate local or central draft |

## Operating Route

Use `docs/guides/LOCAL_EVAL_PORT_STANDARD.md` for local-port inspection and
validation, and `EVAL_FORGE_OPERATING_PATH.md` for the owner-routing flow.

## Promotion Boundary

Local ports can produce candidate pressure, deterministic support, and owner
review packets. They do not create central `aoa-evals` proof by location. A
central proof bundle or verdict requires separate owner acceptance and source
bundle validation.

## Execution Boundary

The execution state vocabulary is exactly `absent`, `invalid`, `stale`, and
`ready`, aggregated as `invalid > stale > ready > absent`. Inventory, Eval
Forge, readiness, dashboard, session-start, promotion review, generated
readers, and MCP are inspect-only. MCP also cannot write `.suite.json` under
AOA-EV-D-0241. Only the selected repo owner or `aoa-eval-apply` may invoke a
ready contract's exact argv.
The contract owner is resolved from PORT and Git common-dir/origin identity,
not a named worktree basename. Owner/apply must revalidate immediately before
execution and preserve environment plus receipt metadata.
Every consumer first normalizes the inventory envelope. V1/unknown packets map
suite execution to `absent`, regardless of injected fields or old route keys;
only v2 may reach `active_suite_apply_or_regression_check`.
