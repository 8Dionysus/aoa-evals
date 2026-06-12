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
- `active`: the port carries at least one local intake packet or local draft
  bundle.

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

It confirms the port shape, `PORT.yaml`, `eval_need_v1` intake payloads, and
the boundary that central proof authority remains in `aoa-evals`.

## First-Wave Repos

The first local eval-port wave covers:

- `aoa-memo` as the first active port;
- `aoa-routing`;
- `aoa-kag`;
- `aoa-agents`;
- `aoa-stats`;
- `aoa-sdk`.

Skeleton ports are acceptable during the first wave as long as they state their
future local pressure honestly and do not carry fake bundles.

## Stop-Lines

Route away when:

- a local report reads like a central verdict;
- a skeleton port starts implying an active suite;
- a trace failure becomes proof without review;
- a local eval bundle duplicates an existing central bundle without a
  route-first check;
- a sibling repo starts defining proof doctrine instead of local evidence
  shape.
