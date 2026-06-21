# Local Eval Port Standard

`evals/` in a sibling repository is a local eval-pressure port, not a local
copy of `aoa-evals`.

The port lets an owner repo preserve the cases, fixtures, trace cues, suites,
reports, and proof questions that were born inside that repo while keeping
verdict, scoring, regression, and proof-doctrine authority in `aoa-evals`.

## Operating Card

| Field | Route |
| --- | --- |
| role | cross-repo standard for local eval-pressure ports |
| input | repo-local proof pressure, trace failure, local suite need, fixture family, or report route |
| output | local intake packet, local suite, local report, local draft bundle, or route to `aoa-evals` |
| owner | this guide owns the standard; sibling `evals/PORT.yaml` owns local status and boundary declaration |
| next route | sibling `evals/AGENTS.md`, `evals/intake/`, local suite/report surface, or `aoa-evals` source bundle |
| validation | `python scripts/validate_local_eval_port.py --target-root <repo>` |

## Required Shape

Every local port has this minimum shape:

```text
evals/
  AGENTS.md
  README.md
  PORT.yaml
  intake/
    README.md
  suites/
    README.md
  reports/
    README.md
```

`PORT.yaml` uses `local_eval_port_v1`:

```yaml
schema_version: local_eval_port_v1
owner_repo: aoa-memo
status: active
proof_owner_repo: aoa-evals
default_intake_schema: eval_need_v1
local_role: repo-local eval pressure, fixtures, suites, and reports
central_boundary: no verdict, scoring, regression, or proof doctrine authority
```

The first wave status values are:

- `skeleton`: the port exists and declares its boundary, but carries no active
  local intake or bundle yet;
- `active`: the port carries at least one local intake packet, local draft
  bundle, local suite note, or local report note.

## Intake

`intake/` is the pre-bundle layer. It stores proof pressure before the reviewer
knows whether the next route is an existing central eval, selected evidence, a
quest, or a new draft bundle.

Use `*.eval_need.json` for structured intake. The payload must follow the
`eval_need_v1` schema owned by
`mechanics/proof-object/parts/eval-authoring/schemas/eval-need.schema.json`.

Do not call this layer `candidates/`. A candidate is one possible state; local
eval intake also includes trace failures, fixture pressure, local suite needs,
and non-authoring-ready blind spots.

## Local Suites And Reports

`suites/` and `reports/` are local note surfaces for deterministic repo-local
proof pressure. They preserve fixture families, case lists, local review
shells, or run summaries before `aoa-evals` adopts a portable bundle.

Use these filenames:

```text
evals/suites/<slug>.suite.md
evals/reports/<slug>.report.md
```

Both files start with YAML frontmatter:

```yaml
---
schema_version: local_eval_suite_note_v1
owner_repo: aoa-memo
status: draft
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---
```

Report notes use `schema_version: local_eval_report_note_v1`. The first-wave
note statuses are `draft` and `reviewed`.

Local suite and report notes may name local cases, fixture expectations,
evidence refs, and review questions. They must not compute final verdicts,
define scoring truth, declare regression status, publish receipts, or invent
proof doctrine.

## MCP Federation And Writes

The `aoa_evals` MCP access plane may federate local ports across the workspace.
It may list ports, inspect one port, read local intake/suite/report surfaces,
and prepare route-first local write plans.

Write-side MCP in the first federation wave is limited to local port files:

- `evals/intake/*.eval_need.json`;
- `evals/suites/*.suite.md`;
- `evals/reports/*.report.md`;
- `evals/PORT.yaml` status movement from `skeleton` to `active` when the same
  gated write adds the first local pressure file.

The MCP must not create central `aoa-evals/evals/**` source bundles, compute
verdicts, define scoring, mark regression truth, publish receipts, or accept
evidence. Central adoption still routes through `aoa-evals` source bundle
review and the eval authoring scaffold.

## Local Ownership

A local port may own:

- repo-local proof questions and origin need;
- public-safe cases, fixtures, suites, examples, and report shells;
- local trace or failure references that remain below proof authority;
- local draft bundles when the claim is already narrow enough to expose
  `EVAL.md` and `eval.yaml`;
- route context that helps `aoa-evals` decide whether to adopt or normalize the
  proof surface later.

A local port must not own:

- final verdict, scoring, or regression truth;
- proof doctrine or portable claim vocabulary;
- central starter-bundle promotion;
- hidden private benchmark truth;
- live runtime enforcement or production monitoring claims.

## Bundle Boundary

If a sibling repo creates a local draft bundle, it uses the same source shape as
`aoa-evals`:

```text
evals/<claim-family>/<eval-name>/
  EVAL.md
  eval.yaml
```

The bundle stays local until `aoa-evals` explicitly adopts or normalizes it.
Local bundle reports may inform proof review, but they do not become central
verdicts by location alone.

## Tests, Validators, And Scripts

Local eval ports keep three lanes separate:

- deterministic validators protect shape, schema, owner boundaries, and route
  declarations;
- tests protect repo-local deterministic contracts and fixtures;
- semantic eval runners, trace grading, repeated runs, and model-judge scoring
  route to `aoa-evals` or the runtime/eval owner.

The local port validator is deterministic and safe for repo checks:

```bash
python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .
```

It confirms the port shape, `PORT.yaml`, `eval_need_v1` intake payloads, local
suite/report note frontmatter, local active/skeleton status, and the boundary
that central proof authority remains in `aoa-evals`.

## Workspace Inventory And Routing Read-Model

When an agent needs the OS Abyss-wide eval-port picture, use the read-only
inventory builder from `aoa-evals`:

```bash
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
```

The builder scans sibling Git repositories, validates local ports through
`scripts/validate_local_eval_port.py`, counts local intake, suites, reports,
and draft bundles, and emits route recommendations such as:

- `missing_no_pressure`;
- `valid_skeleton_keep_dormant`;
- `active_intake_select_then_apply_or_design`;
- `active_suite_apply_or_regression_check`;
- `active_reports_only_suite_extraction_or_review`;
- `invalid_active_repair` or `invalid_port_repair`;
- `central_overlap_apply_existing_first`.

The inventory excludes `aoa-evals` itself because `aoa-evals` is the central
proof owner, not a repo-local pressure port.

The read-model is advisory routing evidence. It may tell an agent which repo
needs local-port repair, selection, apply, design, or no mutation. It must not
promote local pressure, compute verdicts, accept evidence, create central
bundles, or replace direct inspection of the target repository before a write.

The inventory's producer/consumer contract lives in
`docs/architecture/local_eval_port_inventory.contract.v1.json`. `aoa-evals`
owns that contract; `aoa-evals-mcp` may consume it to keep MCP resources and
tools aligned with the central status vocabulary, summary keys, route keys, and
authority boundaries.

## Coverage Waves

The first local eval-port wave covered:

- `aoa-memo` as the first active port;
- `aoa-routing`;
- `aoa-kag`;
- `aoa-agents`;
- `aoa-stats`;
- `aoa-sdk`.

Skeleton ports are acceptable during the first wave as long as they state their
future local pressure honestly and do not carry fake bundles.

The next coverage wave extends the same contract to other owner repositories
that produce repo-local eval pressure while work is happening there:

- `8Dionysus` for public-entry and workspace-route proof pressure;
- `Agents-of-Abyss` for center and federation-boundary proof pressure;
- `Tree-of-Sophia` for ToS source, doctrine, and relation proof pressure;
- `ATM10-Agent` for companion, perception, retrieval, and safe-automation proof
  pressure;
- `Dionysus` for seed, wave, planting, and replay proof pressure;
- `aoa-skills` for skill-trigger and workflow proof pressure;
- `aoa-techniques` for technique-canon and reusable-practice proof pressure;
- `aoa-playbooks` for scenario, fallback, handoff, and real-run proof
  pressure;
- `abyss-machine` for host-machine proof pressure under the host change-ledger
  and storage-policy boundary.

The coverage wave changes where pressure may be captured; it does not move
central proof authority out of `aoa-evals`.

## Stop-Lines

Route away when:

- a local report reads like a central verdict;
- a skeleton port starts implying an active suite;
- a trace failure becomes proof without review;
- write-side MCP starts writing central bundles, verdicts, scores, regression
  truth, or receipts;
- a local eval bundle duplicates an existing central bundle without a
  route-first check;
- a sibling repo starts defining proof doctrine instead of local evidence
  shape.
