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

Current snapshot on 2026-06-26:

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
| `aoa-skills` | active | 1 suite, 5 reports | `active_suite_apply_or_regression_check` | run or inspect local trigger/regression suite before new design |
| `aoa-memo` | active | 1 intake, 1 report | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap before design |
| `aoa-routing` | active | 1 intake, 2 reports | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap before design |
| `connectors/aoa-4pda-connector` | active | 1 suite, 1 report | `active_suite_apply_or_regression_check` | run or inspect connector-local suite before central adoption |

## Deep Local Port Check: aoa-skills

`aoa-skills/evals/PORT.yaml` says:

- `schema_version: local_eval_port_v1`;
- `owner_repo: aoa-skills`;
- `status: active`;
- `proof_owner_repo: aoa-evals`;
- local role is repo-local eval pressure, fixtures, suites, and reports;
- central boundary forbids local verdict, scoring, regression, or proof
  doctrine authority.

The active suite is:

- `evals/suites/aoa-eval-trigger-corpus.suite.md`

The active reports include:

- `aoa-eval-session-mining.report.md`;
- `aoa-eval-runtime-adoption-20260621.report.md`;
- `aoa-eval-battle-path-20260621.report.md`;
- `aoa-eval-prompt-trigger-harness-20260625.report.md`;
- `aoa-eval-self-awareness-contract-lane.report.md`.

Implication: for `aoa-eval` trigger pressure, the first route is local apply or
regression review in `aoa-skills`, not a new central bundle.

## Decision Matrix

| Inventory Route Key | Meaning | Eval Forge Route | Stop-Line |
| --- | --- | --- | --- |
| `missing_no_pressure` | no local port and no current pressure | stop unless current work creates bounded pressure | do not create a port just for symmetry |
| `valid_skeleton_keep_dormant` | valid dormant port with no active pressure | no-op or record current pressure only if new evidence exists | do not invent intake |
| `active_intake_select_then_apply_or_design` | local intake/report pressure exists | `local-intake-pressure-packet`, then select/design review | check central/local duplicates first |
| `active_suite_apply_or_regression_check` | local suite can run as deterministic support | `local-runnable-suite`, then local apply/regression check | suite result is not central verdict |
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

