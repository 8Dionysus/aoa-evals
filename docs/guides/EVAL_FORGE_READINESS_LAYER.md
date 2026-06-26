# Eval Forge Readiness Layer

This guide is the session entrypoint for OS Abyss eval work.

It is not a verdict surface, not a scoring guide, and not proof adoption. It
shows the smallest reliable route for an agent to discover existing evals,
reject noise, create local candidate pressure when needed, and keep
`aoa-evals` as the central proof authority.

## Operating Card

| Field | Route |
| --- | --- |
| role | session-ready Eval Forge front door |
| input | eval pressure, local `evals/` port pressure, session trace pressure, MCP write-side pressure, validator/test/script route pressure |
| output | readiness gate packet, existing eval route, local intake/suite/report route, candidate-only session packet route, or owner review stop line |
| owner | `aoa-evals` owns proof doctrine and this readiness layer; local repos own local pressure; `abyss-stack` owns the runnable MCP package; `.aoa` owns raw/session evidence |
| first command | `python scripts/check_eval_forge_readiness.py --json` |
| session packet | `python scripts/aoa_eval_session_start.py --json` |
| validation | this guide's [Verification](#verification) section |

## Fast Path

Run these from the `aoa-evals` repo before designing a new eval:

```bash
python scripts/check_eval_forge_readiness.py --json
python scripts/aoa_eval_session_start.py --json
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
python scripts/check_eval_support_registry.py --json
python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets
```

If the readiness check reports warnings, read the warning owner. Warnings are
intentional when live `.aoa` catch-up is waiting for a quiet window, the MCP
federation mirror is stale but source checkout is selected, dirty repositories
are classified before edits, or unsafe write-capable scripts are forbidden as
direct eval application.

Errors block the forge route until the named owner surface is repaired.

## Route Order

1. Check existing central evals and generated catalog routes.
2. Check the target repo's `evals/PORT.yaml`, `intake/`, `suites/`, and
   `reports/`.
3. Check validator/test/script support classification before running a support
   command as eval evidence.
4. Check session or runtime candidate packets only after validating the
   candidate-only packet contract.
5. Use Eval Forge to choose an archetype or worksheet.
6. Write local intake/suite/report pressure only through the repo-local owner
   surface or dry-run-first MCP write tools.
7. Route central adoption through `aoa-evals` owner review.

Do not start from keyword search. A kept candidate needs expected route,
observed break, consequence, owner surface, and repeatability path.

## Local Port Flow

Use local ports for pressure born inside a repo:

```bash
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --local-port-repo <repo_id> --json
```

Active ports can carry intake packets, suite notes, and report notes. Skeleton
ports stay dormant until real pressure appears. A local port does not own
verdicts, scoring, regression truth, or proof doctrine.

## Session Mining Flow

Manual session mining is candidate-only.

The current seed review is:

```text
mechanics/audit/parts/candidate-readers/reports/session-mining/2026-06-25-aoa-eval-control.manual-review.md
```

It reviewed 20 bounded episodes and imported five candidate packets:

- `session:aoa-eval-criteria-before-mining`
- `session:aoa-eval-goal-shrink-completion-overclaim`
- `session:aoa-eval-keyword-mining-blindspot`
- `session:aoa-eval-session-front-door-actionability-gap`
- `session:aoa-eval-working-process-fossilized-as-doctrine`

Rejected and deferred rows are part of the evidence. They prevent future agents
from turning transition-only, emotion-only, or keyword-only hits into fake
candidates.

## MCP Write Side

`aoa-evals-mcp` may write only repo-local eval-port files:

- `evals/intake/*.eval_need.json`
- `evals/suites/*.suite.md`
- `evals/reports/*.report.md`
- `evals/PORT.yaml` `skeleton` to `active` activation when the same gated write
  adds first pressure

Every local write response must include an audit receipt that says whether the
call was a dry-run, whether the target stayed inside `evals/`, whether schema
validation passed, whether `PORT.yaml` activation was needed/applied, and that
proof authority, promotion, verdict, scoring, and central mutation remain
false.

Future central bundle creation, evidence acceptance, verdict computation,
regression scoring, receipt publication, non-stdio exposure, or writes outside
repo-local `evals/` ports require a new decision.

## Validator, Test, And Script Classes

Agents should read `check_eval_support_registry.py --json` before treating a
command as eval support.

The readiness layer distinguishes:

- safe direct support: deterministic validators and tests that constrain stable
  contracts;
- candidate-only support: runtime/session/memory evidence that needs owner
  review;
- component-only support: helper validators reached only through the owning
  command;
- forbidden support: write-capable scripts without a safe direct eval-apply
  route;
- generated/read-model support: parity and freshness checks below proof
  acceptance.

## Freshness And Drift

Freshness is a gate, not a background concern. The readiness layer tracks:

- generated dashboard age;
- stale MCP federation mirrors;
- `.aoa` live catch-up state;
- support registry unsafe writers;
- component-only validators;
- active local port pressure;
- dirty repositories and branch drift.

The source checkout remains stronger than a stale mirror. Raw/session evidence
remains stronger than `.aoa` search output. Authored source remains stronger
than generated dashboards.

## Verification

Use this command as the single readiness gate:

```bash
python scripts/check_eval_forge_readiness.py --json
```

Use the full verification set before closeout:

```bash
python scripts/aoa_eval_session_start.py --json
python scripts/check_eval_forge_readiness.py --json
python scripts/check_eval_freshness_sentinel.py --json
python scripts/build_eval_readiness_dashboard.py --check
python scripts/check_eval_support_registry.py --json
python scripts/check_eval_candidate_queue_lifecycle.py --json
python scripts/validate_eval_candidate_packets.py --schema-only
python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run `aoa-evals-mcp` checks from `abyss-stack` when MCP write-side behavior
changes:

```bash
python mcp/services/aoa-evals-mcp/scripts/validate_evals_mcp.py
python -m pytest -q mcp/services/aoa-evals-mcp/tests
```
