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
shells, or run summaries before `aoa-evals` adopts a portable bundle. A suite
note is not an execution contract and must not be reported as runnable by its
presence alone.

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

## Local Suite Execution Sidecars

A local suite with reviewed execution intent adds a source sidecar next to its
note:

```text
evals/suites/<slug>.suite.md
evals/suites/<slug>.suite.json
```

The JSON sidecar uses `local_eval_suite_execution_v1`, validated by
`mechanics/proof-object/parts/eval-authoring/schemas/local-eval-suite-execution.schema.json`.
It carries:

- the matching suite id, owner repo, and `.suite.md` reference;
- `runner.kind: python_pytest`, a shell-free `runner.argv` array, and a
  repo-relative `runner.cwd`;
- a repo-relative existing `entrypoint_ref`;
- a bounded timeout and explicit accepted success exit codes;
- one or more repo-relative tracked sources with `kind: file|tree` and SHA256;
- `auto_run_allowed: false`, `proof_authority: false`, and
  `promotion_allowed: false`;
- `readiness_scope: source-contract-ready`,
  `runtime_reproducibility_proven: false`, and required JIT revalidation,
  environment capture, and execution receipt flags;
- the exact owner-local, non-proof authority boundary.

`python_pytest` has one exact semantic grammar:

```text
python|python3 [-B] -m pytest [reviewed allowlisted flags] <cwd-relative-entrypoint-arg>
```

`entrypoint_ref` remains the canonical repo-relative source ref. The final argv
token occurs once and must be its traversal-free path relative to `runner.cwd`;
resolving that token from the declared cwd must reach exactly `entrypoint_ref`.
For example, `cwd: tests` with `entrypoint_ref: tests/memory_guardrail.py`
requires final argv `memory_guardrail.py`, not `tests/memory_guardrail.py`.
The reviewed flag set is
`-q`, `--quiet`, `-x`, `--exitfirst`, `--strict-markers`, `--strict-config`,
`--disable-warnings`, bounded `--maxfail=N`, `--tb=...`, `--color=...`, and
`-r...`; the only plugin option is the fixed pair `-p no:cacheprovider`.
Optional `-B` may appear only before `-m pytest`. Other Python interpreter
flags, `-c`, another `-m` target, arbitrary
executables, Node, `env`, `command`, BusyBox, and shell wrappers are invalid.
Absolute paths, `..` traversal, backslash path forms, symlink components, and
shell metacharacters are also invalid. The entrypoint must be covered by a
tracked file or tree.

Each `*.suite.json` discovery entry must be a regular UTF-8 JSON file. A
directory, FIFO, socket, device, undecodable byte stream, or other non-regular
entry is `invalid`; inventory records the issue instead of attempting to read
or execute it.

Owner identity is canonical-repository identity, not checkout-directory
identity. `PORT.yaml`, suite/report notes, and sidecars must agree. In a Git
checkout the validator resolves the Git common-dir repository name and the
`origin` repository name when available; conflicting identities are invalid.
A named worktree such as `aoa-skills-executable-eval-pilot-20260710` therefore
still resolves to `aoa-skills`. A non-Git fixture falls back to the target-root
basename.
An identity conflict is surfaced before central-owner exclusion, so a spoofed
`origin=aoa-evals` cannot disappear from inventory as if it were the genuine
central proof owner.

File SHA256 is the digest of file bytes. Tree SHA256 is deterministic: walk
all descendants in sorted repo-relative POSIX order, reject symlinks and
non-regular entries, and hash `dir\0<relative>\n` for directories plus
`file\0<relative>\0<file-sha256>\n` for files. Use
`scripts/validate_local_eval_port.py` helpers to produce the canonical digest.

The execution state vocabulary is exactly:

- `absent`: no `.suite.json` sidecar exists; a `.suite.md` note remains
  non-runnable pressure;
- `invalid`: schema, canonical owner, path, symlink, typed runner grammar,
  entrypoint, tracked source, runtime-boundary flag, or authority checks fail;
- `stale`: structure is valid but at least one current source digest differs
  from its reviewed SHA256;
- `ready`: every source-contract and tracked-source check passes. This means
  `source-contract-ready`, not pinned-runtime-ready.

Multiple sidecars aggregate with `invalid > stale > ready > absent` priority.

Inventory, Eval Forge, readiness, dashboard, session-start, promotion review,
generated readers, and MCP inspect and route this state only. They never run
`runner.argv`. A `ready` sidecar does not pin the interpreter, platform,
installed plugins, or dependency graph; a requirements range or source hash
cannot prove runtime reproducibility. Only the selected repo owner or
`aoa-eval-apply` may proceed, and it must immediately re-run validation, confirm
the sidecar and tracked hashes are still ready, invoke the exact argv/cwd/
timeout/exit-code contract, capture interpreter/dependency/platform metadata,
and write an execution receipt linked to the sidecar digest and observed source
hashes. That receipt records an execution; it is not central proof acceptance.
The argv allowlist blocks argv-selected plugins, except the fixed
`no:cacheprovider` disable. It does not prove which ambient pytest plugins,
config files, or environment variables were active; environment capture must
record them.

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

`evals/suites/*.suite.json` is intentionally not in the AOA-EV-D-0241 write
allowlist. MCP may read a validated sidecar through inventory/detail surfaces,
but it must not create, replace, refresh hashes in, or execute one without a
separate decision.

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
suite/report note frontmatter, suite execution schema/path/hash state, local
active/skeleton status, and the boundary that central proof authority remains
in `aoa-evals`.

## Workspace Inventory And Routing Read-Model

When an agent needs the OS Abyss-wide eval-port picture, use the read-only
inventory builder from `aoa-evals`:

```bash
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
```

The builder scans sibling Git repositories with a valid working-tree marker
(`.git/HEAD` or a worktree-style `.git` file), validates local ports through
`scripts/validate_local_eval_port.py`, counts local intake, suites, reports,
and draft bundles, and emits route recommendations such as:

- `missing_no_pressure`;
- `valid_skeleton_keep_dormant`;
- `active_intake_select_then_apply_or_design`;
- `active_suite_note_review_or_execution_contract_design`;
- `active_suite_contract_invalid_repair`;
- `active_suite_contract_stale_review`;
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

The current inventory producer/consumer contract lives in
`docs/architecture/local_eval_port_inventory.contract.v2.json`. V1 remains a
compatibility input while stack MCP consumers dual-read v1 and v2. A v1 entry
must map suite execution to `absent`; consumers must never infer runnable from
`suite_notes` or trust an injected v2-shaped field. Forge, dashboard,
promotion/session surfaces, generated readers, and MCP normalize v1/unknown
input before routing; an old runnable route becomes sidecar design. V2 adds the
execution state, aggregate priority, sidecar counts, and inspect-only invocation
boundary.

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
- a `.suite.md` note is treated as runnable without a ready sidecar;
- a named Git worktree basename overrides the canonical PORT/common-dir/origin
  owner identity;
- a sidecar uses an untyped or non-`python_pytest` dispatcher grammar;
- `ready` is described as pinned or reproducible runtime evidence;
- owner/apply executes without JIT revalidation, environment capture, and an
  execution receipt;
- an invalid or stale sidecar reaches owner/apply;
- inventory, Eval Forge, readiness, dashboard, session-start, promotion review,
  generated readers, or MCP executes `runner.argv`;
- a trace failure becomes proof without review;
- write-side MCP starts writing central bundles, verdicts, scores, regression
  truth, or receipts;
- a local eval bundle duplicates an existing central bundle without a
  route-first check;
- a sibling repo starts defining proof doctrine instead of local evidence
  shape.
