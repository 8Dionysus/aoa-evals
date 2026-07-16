# Eval Forge Session Candidate Owner Review 2026-06-26

> Current applicability (2026-07-10): the supporting check recorded below is
> historical owner evidence, not an Eval Forge execution route. A current
> local apply requires a `ready` AOA-EV-D-0245 sidecar, and only the repo owner
> or `aoa-eval-apply` may invoke its exact argv.
>
> Current skill-route applicability (2026-07-16): the `aoa-skills` trigger
> corpus, prompt harness, and generated runtime export named below were later
> retired during capability-family consolidation. They remain historical
> evidence for this review, not current commands or owner surfaces. Current
> skill-effect review routes to the authored skill, resolved catalog/profile,
> prompt-visible host posture, and session-local manual no-skill, positive,
> negative, and coexistence comparisons. The admitted owner review is
> `aoa-skills/docs/reviews/2026-07-15-capability-family-lifecycle.md`.

## Boundary

This is an owner-review routing report for five session-derived Eval Forge
candidate packets.

It is not a central eval bundle, verdict, score, baseline, receipt, regression
claim, or proof promotion. Every decision below keeps `proof_authority: false`
and `promotion_allowed: false`; the report only records the next owner route.

## Evidence Checked

Candidate-packet validation, Eval Forge routing, the owner-local skill-trigger
harness, and the stack-owned MCP access checks were exercised through their
respective owner routes.

Existing surfaces checked before decisions:

- `mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md`;
- `mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md`;
- `mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md`;
- `mechanics/proof-object/parts/eval-authoring/reports/eval-forge/2026-06-26-eval-forge-route-review.md`;
- `mechanics/audit/parts/candidate-readers/packets/session-mining/*.eval_candidate.json`;
- `generated/eval_readiness_dashboard.json`;
- `aoa-skills/evals/suites/aoa-eval-trigger-corpus.suite.md`;
- `abyss-stack/mcp/services/aoa-evals-mcp/`.

## Decisions

| Packet | Decision | Owner Repo | Existing Surfaces Checked | Next Route | Proof Boundary |
| --- | --- | --- | --- | --- | --- |
| `session:aoa-eval-criteria-before-mining` | owner-review worksheet only | `aoa-evals` plus domain owner | session-mining criteria, reject taxonomy, worksheet schema/example, candidate packet validator | Eval Forge worksheet route | worksheet is advisory design evidence only; no broad mining automation until the owner accepts criteria and reject accounting |
| `session:aoa-eval-goal-shrink-completion-overclaim` | central proof bundle draft gate | `aoa-evals` with `.aoa` candidate evidence | central catalog/readiness dashboard, candidate packet route, trace-trajectory archetype, `aoa-change-protocol` skill route | Eval Forge candidate review | a future draft gate may be opened only after manual source-span review, central overlap check, and owner acceptance; this report creates no bundle |
| `session:aoa-eval-keyword-mining-blindspot` | skill trigger fixture/harness, applied through local `aoa-skills` suite | `aoa-skills` | `aoa-eval` source skill, `aoa-eval-trigger-corpus.suite.md`, prompt trigger fixtures, generated/runtime skill export | owner-local skill-trigger suite | local trigger coverage constrains skill routing only; it is not an `aoa-evals` verdict or central proof bundle |
| `session:aoa-eval-session-front-door-actionability-gap` | runtime/MCP smoke | `abyss-stack` | `aoa-evals` session-start/readiness, `aoa-evals-mcp` Forge access packet, MCP boundary docs, runtime status | stack-owned MCP smoke | MCP is access-plane data only; valid front-door output does not accept candidates, write worksheets, or promote proof |
| `session:aoa-eval-working-process-fossilized-as-doctrine` | owner-review worksheet only, then defer unless owner accepts a reusable route | `aoa-evals` plus affected process owner | operating path, session-mining criteria, `aoa-eval` skill boundary, candidate packet route | Eval Forge candidate review | current working process must not be fossilized into doctrine by this report; owner review decides whether it becomes a skill fixture, trajectory eval, or rejected one-off |

## Route Coverage

- Local suite/apply demonstrated by the `aoa-eval-keyword-mining-blindspot`
  route through `aoa-skills` trigger corpus and focused prompt-trigger harness.
- Skill-trigger eval demonstrated by the same packet's `trigger_design_case`
  owner route.
- Runtime/MCP smoke demonstrated by
  `aoa-eval-session-front-door-actionability-gap` through
  `aoa_evals_mcp.cli forge-access` and `validate_evals_mcp.py`.
- Human-review worksheet demonstrated by `aoa-eval-criteria-before-mining` and
  `aoa-eval-working-process-fossilized-as-doctrine`.
- Central proof bundle draft gate demonstrated by
  `aoa-eval-goal-shrink-completion-overclaim`, but the gate is not opened as a
  bundle until owner review accepts the source span and overlap check.

## Why No Automatic Proof Promotion

- All five packets are session-derived candidates with explicit
  `candidate_only`, `proof_authority: false`, and `promotion_allowed: false`
  posture.
- Forge route outputs are design guidance and worksheet payloads only.
- Local `aoa-skills` suites and `abyss-stack` MCP smokes prove only local route
  behavior.
- `.aoa` evidence remains raw/session evidence until the owner accepts a
  bounded proof object.
- Central bundle creation requires separate source bundle authoring, validation,
  and human owner acceptance.

## Remaining Owner Gaps

- Owner-review pending: accept or reject the two human-review worksheet routes.
- Proof promotion later: decide whether the goal-shrink case deserves a central
  trace-trajectory eval bundle.
- Automation later: do not broaden session mining until accepted positives,
  rejects, and collision cases exist.
- Runtime owner later: keep `abyss-stack` Forge access packet validated as an
  access plane when `aoa-evals` readiness shape changes.
- Rejected/noise: none of these five packets is rejected today, but keyword-only,
  ownerless, duplicate, no-consequence, and no-repeatability cases remain
  rejected by the criteria doc.
