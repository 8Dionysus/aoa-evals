# Eval Forge Route Review 2026-06-26

> Current applicability (2026-07-10): this report preserves the reviewed
> 2026-06-26 route snapshot. Under AOA-EV-D-0245, its `.suite.md`-only rows
> have execution state `absent` and route to sidecar design/review, not
> `local-runnable-suite`, until a validated sidecar becomes
> source-contract-`ready`. That state does not prove runtime reproducibility;
> owner/apply still JIT-revalidates and captures environment plus receipt.

## Boundary

This is a part-local route-review report for Eval Forge.

It is not a central eval bundle, verdict, score, baseline, receipt, or proof
promotion. It records that several real candidate classes and active local-port
pressure items can pass through the design router while preserving owner
boundaries.

## Readiness Evidence

The session-start, readiness, local-port inventory, and candidate-packet
validation routes were exercised through their owning entrypoints.

Observed:

- session-start schema: `os_abyss_eval_session_start_v1`;
- Eval Forge readiness schema: `os_abyss_eval_forge_readiness_check_v1`;
- overall readiness status: `warning`;
- `.aoa` freshness blocker: `run_live_catchup`;
- candidate packets: 5 valid;
- local ports: 15 valid, 4 active, 11 skeleton, 0 invalid;
- support registry: 595 surfaces, 466 safe to apply directly, 4 unsafe
  side-effect scripts;
- candidate queue: 10 entries, including 5 session packets and 4 local port
  pressure entries.

The freshness blocker is intentional route evidence. It prevents treating
session output as current proof while still allowing bounded candidate review.

## External Grounding

The review used current external patterns as design input:

| Source | Adopted For Eval Forge |
| --- | --- |
| Anthropic agent eval guidance | agent evals need task, trial, grader, transcript/outcome thinking |
| Inspect AI | runnable eval shape maps to dataset, solver/agent, scorer, tools, and logs |
| LangSmith AgentEvals | trajectory and tool-call behavior need separate route-level evaluation |
| Google ADK | trajectory/tool-use and final-response evaluation are different dimensions |
| Langfuse | manual trace review comes before scalable online/offline eval automation |
| LangChain readiness checklist | outcome should not be over-constrained by brittle exact paths when multiple valid routes exist |
| OpenAI deprecations | durable OS Abyss workflow must not depend on the hosted Evals platform that is being retired in 2026 |

These are not OS Abyss proof authorities.

## Session Candidate Routes

Candidate packets were inspected through the Eval Forge candidate route.

| Packet | Decision | Archetype | Owner Route | Next Route |
| --- | --- | --- | --- | --- |
| `session:aoa-eval-criteria-before-mining` | keep | `human-review-rubric` | domain owner | owner-review worksheet and manual rubric before automation |
| `session:aoa-eval-goal-shrink-completion-overclaim` | keep | `trace-trajectory-eval` | `aoa-evals + .aoa candidate evidence` | trajectory review for premature completion and DoD shrink |
| `session:aoa-eval-keyword-mining-blindspot` | keep | `aoa-skills-trigger-eval` | `aoa-skills` | trigger design case for route signs without keyword dependency |
| `session:aoa-eval-session-front-door-actionability-gap` | keep | `abyss-stack-runtime-mcp-smoke` | `abyss-stack` | runtime/MCP/front-door smoke before central proof |
| `session:aoa-eval-working-process-fossilized-as-doctrine` | keep | `human-review-rubric` | domain owner | review temporary workflow correction before doctrine |

All routes reported `proof_authority: false` and `promotion_allowed: false` in
the worksheet payload.

## Local Port Routes

Local ports were inspected through the Eval Forge owner-routing path after the
workspace inventory had been built.

| Repo | Decision | Archetype | Route Key | Owner Boundary |
| --- | --- | --- | --- | --- |
| `aoa-skills` | keep | `local-runnable-suite` | `active_suite_apply_or_regression_check` | repo-local suite; central proof stays in `aoa-evals` |
| `aoa-memo` | keep | `local-intake-pressure-packet` | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap first |
| `aoa-routing` | keep | `local-intake-pressure-packet` | `active_intake_select_then_apply_or_design` | inspect local intake and central overlap first |
| `connectors/aoa-4pda-connector` | keep | `local-runnable-suite` | `active_suite_apply_or_regression_check` | connector-local suite; central proof stays in `aoa-evals` |

## Worksheet Artifact

The worksheet was produced through the Eval Forge candidate route and written
to the part-local example surface below.

Output:

- path:
  `mechanics/proof-object/parts/eval-authoring/examples/aoa_eval_criteria_before_mining.eval_design_worksheet.example.json`;
- worksheet schema validation: valid;
- selected archetype: `human-review-rubric`;
- `proof_authority: false`;
- `promotion_allowed: false`;
- no source bundle was created.

## Owner-Review Outputs Added

- `docs/EVAL_FORGE_OPERATING_PATH.md`;
- `docs/SESSION_MINING_CRITERIA.md`;
- `docs/LOCAL_PORT_DECISION_MATRIX.md`;
- this route-review report;
- schema-valid worksheet example for `aoa-eval-criteria-before-mining`.

## Gaps

Owner-review needed:

- accept or revise the manual mining criteria before broad mining;
- decide whether each kept packet becomes a local suite, central draft, trigger
  case, runtime smoke, or reject.

Automation later:

- build any session miner only after enough accepted positive and negative
  examples exist;
- prefer guardrails against overclaim before broad automatic candidate creation.

Proof promotion later:

- no kept packet is central proof;
- no local suite/report is central verdict or regression truth;
- central bundle creation requires explicit human owner acceptance and source
  bundle validation.

Rejected/noise:

- keyword-only, emotion-only, transition-only, duplicate, ownerless, private
  raw-only, no-consequence, and no-repeatability cases stay out of packetized
  candidate queues.
