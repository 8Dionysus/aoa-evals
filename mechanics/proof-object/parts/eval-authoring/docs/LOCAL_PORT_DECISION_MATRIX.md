# Local Eval-Port Decision Matrix

## Role

This matrix tells a fresh agent how repo-local `evals/` ports influence Eval
Forge routing.

Repo-local ports own pressure evidence, intake, suites, reports, and local
fixtures. `aoa-evals` owns central proof doctrine, verdicts, scoring,
regression meaning, and central bundle adoption.

## Current Workspace Snapshot

Generated from:

```bash
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
```

The pressure counts below are the 2026-06-26 snapshot. Runnable posture is
interpreted by the 2026-07-10 execution-sidecar contract: suite notes without
a sidecar have execution state `absent`.

| Metric | Count |
| --- | ---: |
| repositories scanned | 15 |
| valid local ports | 15 |
| invalid local ports | 0 |
| missing ports | 0 |
| skeleton ports | 11 |
| active ports | 4 |
| stale candidates | 0 |
| repos with detected pressure | 4 |
| excluded central proof owners | 1 |

## Active Ports

| Repo | Status | Local Pressure | Route Key | First Action |
| --- | --- | --- | --- | --- |
| `aoa-skills` | active | 1 suite note, 5 reports; execution absent | `active_suite_note_review_or_execution_contract_design` | inspect the note and add/review a sidecar before owner-local apply |
| `aoa-memo` | active | 1 intake, 1 report | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap before design |
| `aoa-routing` | active | 1 intake, 2 reports | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap before design |
| `connectors/aoa-4pda-connector` | active | 1 suite note, 1 report; execution absent | `active_suite_note_review_or_execution_contract_design` | inspect the note and add/review a sidecar before owner-local apply |

## Deep Local Port Check: aoa-skills

`aoa-skills/evals/PORT.yaml` says:

- `schema_version: local_eval_port_v1`;
- `owner_repo: aoa-skills`;
- `status: active`;
- `proof_owner_repo: aoa-evals`;
- local role is repo-local eval pressure, fixtures, suites, and reports;
- central boundary forbids local verdict, scoring, regression, or proof
  doctrine authority.

The active suite note is:

- `evals/suites/aoa-eval-trigger-corpus.suite.md`

The active reports include:

- `aoa-eval-session-mining.report.md`;
- `aoa-eval-runtime-adoption-20260621.report.md`;
- `aoa-eval-battle-path-20260621.report.md`;
- `aoa-eval-prompt-trigger-harness-20260625.report.md`;
- `aoa-eval-self-awareness-contract-lane.report.md`.

Implication: the note proves local pressure exists but does not prove a runnable
suite. The first route is sidecar design/review in `aoa-skills`; only a later
source-contract-`ready` state can route typed `python_pytest` argv to the owner
or `aoa-eval-apply`. It does not prove a pinned runtime; owner/apply
JIT-revalidates and captures environment plus an execution receipt.

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

## Commands

Inspect one repo from the inventory:

```bash
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json \
  | jq '.repos[] | select(.repo_id == "aoa-skills")'
```

Validate a repo-local port from its repo root:

```bash
AOA_EVALS_ROOT=/srv/AbyssOS/aoa-evals \
python /srv/AbyssOS/aoa-evals/scripts/validate_local_eval_port.py --target-root .
```

Route a local port through Eval Forge:

```bash
python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py \
  --local-port-repo aoa-skills \
  --local-port-inventory /tmp/aoa_local_eval_ports.current.json \
  --workspace-root /srv/AbyssOS \
  --json
```

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
