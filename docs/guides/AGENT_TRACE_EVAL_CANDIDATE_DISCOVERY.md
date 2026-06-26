# Agent Trace Eval Candidate Discovery Guide

This guide helps a reviewer discover candidate eval pressure in agent sessions,
traces, and repo work before a proof bundle exists.

It is not a mining report, not reviewed proof, and not a promotion mechanism.
It defines the signs that make a session worth manual review and the gates that
separate useful eval candidates from noise.

See also:
- [Documentation Map](../README.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Boundary Route Checklist](BOUNDARY_ROUTE_CHECKLIST.md)
- [Local Eval Port Standard](LOCAL_EVAL_PORT_STANDARD.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | pre-bundle discovery guide for trace/session eval candidates |
| input | agent trace, Codex session segment, failed landing, user correction loop, stale route claim, runtime mismatch, validation miss, or local eval pressure |
| output | keep, reject, defer, duplicate, local-intake, central-design, trigger-skill, or runtime-owner route |
| owner | this guide owns discovery criteria; `.aoa` owns raw/session evidence; local repos own local `evals/` pressure; `aoa-evals` owns proof doctrine and central bundles |
| next route | `.aoa` evidence pointer, repo-local `evals/` port, `aoa-skills` trigger design, `abyss-stack` runtime owner, `aoa-evals-mcp` access-plane check, or central `aoa-evals` bundle design |
| validation | [docs/AGENTS.md#validation](../AGENTS.md#validation) |

## Session Front Door

For new OS Abyss eval work, the fast path is:

1. start with the session-start route packet from `scripts/aoa_eval_session_start.py`
2. inspect active repo routes and freshness blockers from that packet
3. validate the candidate packet contract with `scripts/validate_eval_candidate_packets.py`
4. check candidate queue lifecycle with `scripts/check_eval_candidate_queue_lifecycle.py`
5. route concrete candidates through `mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py`
6. dry-run local-to-central review with `scripts/review_eval_promotion_path.py`
7. only then write any real mined candidate packet or central draft proposal

This keeps each session operational: the agent sees current tools, active local
pressure, candidate-only boundaries, promotion gates, freshness blockers, and
stop-lines before it starts designing new evals.

Eval Forge is the quick design route for a kept candidate. It can select an
archetype and emit a worksheet, but it remains non-proof and cannot promote
candidate packets or create central bundles.

The promotion dry-run is a gate review, not promotion. It walks one active
local pressure item through local owner review, central overlap check, source
bundle draft, fixture/runner/report contract review, human acceptance,
catalog/report regeneration, and release/advisory validation. It must keep
`promotion_allowed=false` and `mcp_promotion_allowed=false`.

## Research Grounding

Refresh these sources before a major mining wave. They were checked for this
guide on 2026-06-25.

| Source | Adopted here | Rejected for OS Abyss |
| --- | --- | --- |
| [OpenAI agent evals](https://developers.openai.com/api/docs/guides/agent-evals) | Start from traces while behavior is still being debugged; trace-level review should inspect model calls, tool calls, guardrails, handoffs, routing changes, and regressions before datasets harden the check. | Hosted trace graders and eval runs are evidence inputs, not central proof acceptance. |
| [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Use objective, dataset, metric, run/compare, and continuous-growth structure; keep human feedback in the calibration loop. | Do not bind durable OS Abyss proof control to deprecated hosted Evals platform semantics. |
| [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) | A useful agent trace records the whole workflow plus spans for agent runs, generations, tool calls, guardrails, handoffs, and sensitive-data boundaries. | Do not judge path-sensitive behavior from final text alone. |
| [LangSmith trajectory evals](https://docs.langchain.com/langsmith/trajectory-evals) | Use exact, subset, superset, or unordered tool-call trajectory matching when route behavior is the claim. | Do not use judge-only mining for deterministic route-law violations. |
| [LangSmith evaluation approaches](https://docs.langchain.com/langsmith/evaluation-approaches) | Keep final response, single-step, and trajectory evals separate so the evaluator matches the failure shape. | Do not flatten every agent failure into one broad rubric. |
| [LangChain Agent Evaluation Readiness Checklist](https://www.langchain.com/blog/agent-evaluation-readiness-checklist) | Review real traces before building infrastructure, define unambiguous success criteria, assign ownership, separate capability/regression evals, and derive custom evaluators from observed failures. | Do not build automation before labels, criteria, and owner gates exist. |
| [Anthropic agent evals guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Avoid brittle path checks unless the path itself matters; read transcripts to distinguish genuine agent failure from grader, harness, or ambiguous-task failure. | Do not treat every deviation from one expected path as failure. |
| [Hamel Husain evals FAQ](https://hamel.dev/blog/posts/evals-faq/) and [error-analysis note](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html) | Error analysis decides what evals to write; use open notes, first-failure focus, axial coding into a failure taxonomy, and real traces rather than generic metrics. | Do not start from keyword search or generic metrics. |
| [Label Studio production agent evaluation](https://labelstud.io/blog/how-to-evaluate-ai-agents-in-production/) | Final outputs can hide bad trajectories; human-readable trace structure is needed to catch wrong reasoning, hallucinated tool calls, missing side effects, and domain-specific misses. | Do not let output-only grading hide tool/action failures. |
| [EDDOps process model](https://arxiv.org/html/2411.13768v3) | Treat the system pipeline as the object of diagnosis, classify failing execution traces, and find the earliest critical decision that caused the cascade. | Do not blame the last visible symptom when an earlier route break caused the failure. |
| [Inspect AI](https://inspect.aisi.org.uk/) and [Inspect sandboxing](https://inspect.aisi.org.uk/sandboxing.html) | Future runnable agent evals should be expressible as tasks with datasets, agents/solvers, tools, scorers, logs, and isolation/sandboxing where side effects matter. | Do not run write-capable support scripts as eval application without check/dry-run or sandbox route. |

## Core Rule

Do not search for eval candidates by looking for the word `eval`.

A useful candidate exists only when the reviewer can name all of these:

1. expected route: what the agent should have done in this repo or OS layer
2. observed break: what the trace shows instead
3. consequence: what became riskier, wrong, slower, stale, or misleading
4. owner: which source surface or runtime owner can judge the expected route
5. repeatability path: how this could become a check, trajectory eval, local
   intake packet, trigger-skill case, or central proof bundle

If any one of those is missing, the item is not yet a kept candidate. It is
either rejected or deferred for missing evidence.

## Strong Candidate Signs

These signs justify manual review. They do not prove that an eval should be
built.

| Sign | What to look for | Likely route |
| --- | --- | --- |
| user correction after agent claimed progress | user rejects a route, says the task was misunderstood, or points to a concrete missed obligation | session candidate; first-failure note |
| expected-route mismatch | agent changes docs, generated output, memory, or runtime before inspecting the owner route that should govern the task | boundary or route eval |
| generated/readmodel overreach | generated, MCP, dashboard, index, or summary output is treated as proof authority | proof-topology or generated-parity eval |
| final-output/trajectory split | final answer looks acceptable, but the trace shows skipped checks, wrong tool use, missing side effect, or unsafe mutation order | trajectory eval |
| freshness miss | agent relies on stale docs, old branch state, old web source, old runtime status, or unrefreshed sibling repo when freshness matters | freshness sentinel or route canary |
| hidden-state contradiction | agent says a check passed, repo is clean, landing is done, or capability exists while live state says otherwise | runtime/readiness eval |
| owner-boundary breach | local repo pressure is promoted into central proof, `.aoa` raw evidence becomes truth, or MCP access becomes verdict | owner-boundary eval |
| goal shrink | user asked for deep research or full DoD, but the agent converts it into a shallow plan, dashboard, or prose-only artifact | planning/DoD eval |
| wrong automation | agent automates classification before human criteria or labels exist, or writes current process accidents into durable doctrine | candidate-lifecycle eval |
| repeated correction loop | the same user correction class repeats across turns or repos, especially after the agent says it understands | trigger-skill or regression eval |
| tool/action misuse | mutation happens before inspect, destructive command is proposed, dry-run is skipped, or tool choice hides the evidence needed for review | action-policy eval |
| memory/context contamination | prior summary, generated index, or retrieved context overrides the current source route or user correction | memory-boundary eval |
| grader/harness ambiguity | an eval fails because the grader, fixture, harness, or task statement is wrong or too rigid | eval-integrity check |

## Reject Or Defer Signals

Reject or defer aggressively. The point is to create a clean candidate set, not
a pile of interesting annoyance.

| Signal | Route |
| --- | --- |
| keyword-only hit such as `eval`, `test`, `landing`, or `done` with no route break | reject |
| pure style preference with no source route, consequence, or repeatability path | reject |
| user anger with no trace evidence beyond the emotion | defer until the concrete route break is found |
| no identifiable owner surface | defer with missing-owner reason |
| expected route cannot be stated without inventing doctrine | reject or route to research first |
| one-off local typo or copy nit with no recurrence or boundary meaning | reject |
| existing validator, test, or eval already covers the behavior | duplicate and route to the existing surface |
| private, secret-bearing, or overly broad raw session evidence cannot be safely bounded | defer for privacy/sanitization route |
| evidence exists only in a generated summary and raw or source refs are unavailable | defer; summaries are pointers |
| candidate would require an LLM judge but no human labels or rubric exist | defer for rubric/calibration |
| proposed eval would fossilize a temporary workflow accident | reject unless owner route says the pattern is durable |

## Candidate Admission Gates

A kept candidate should pass these gates before it becomes an intake packet or
bundle design input:

| Gate | Keep condition |
| --- | --- |
| evidence boundedness | source refs point to a bounded session span, trace, file diff, command output, or validation result |
| expected-route clarity | the expected route can be linked to an `AGENTS.md`, guide, validator, local `PORT.yaml`, decision, or runtime contract |
| first-failure clarity | the earliest meaningful route break can be named separately from downstream noise |
| consequence | the break matters for correctness, proof authority, safety, freshness, cost, user trust, or OS growth |
| owner | local repo, central `aoa-evals`, `.aoa`, `aoa-skills`, `abyss-stack`, or MCP access-plane owner is explicit |
| repeatability | there is a plausible future check: deterministic rule, trace trajectory grader, local intake, skill trigger, smoke, or human review rubric |
| duplicate check | nearby validators, tests, eval bundles, and local `evals/` surfaces were checked or marked unknown |
| privacy/freshness | raw evidence handling and source freshness are safe enough for the next route |

## Failure Families For Open Coding

Use these labels as a starting vocabulary during manual review. Change the
taxonomy after real reviewed traces show better categories.

| Family | Meaning |
| --- | --- |
| intent/perception | agent misses what the user actually asked, especially after a correction |
| route/planning | agent chooses the wrong owner surface, shrinks the task, or skips the needed source route |
| memory/context | stale memory, summary, or retrieved context overrides current evidence |
| tool/action | wrong tool, wrong mutation order, missing dry-run, skipped inspection, unsafe side effect |
| proof/readout | source proof, generated readmodel, report, or MCP packet is interpreted too strongly |
| freshness/runtime | live state, sibling drift, current branch, or runtime status is not rechecked when needed |
| validation/grader | test, validator, grader, fixture, or harness gives false confidence or false failure |
| collaboration/trigger | agent should ask, stop, select a skill, or switch route but continues blindly |
| lifecycle/promotion | candidate, local intake, draft, baseline, or canonical posture is promoted too early |

## Evaluator Fit

Do not force every candidate into a central `aoa-evals` bundle.

| Candidate shape | Better fit |
| --- | --- |
| exact file/schema/topology condition | deterministic validator or unit test |
| stable boundary between two components | contract test |
| invariant across many route states | property/invariant test |
| agent chose wrong tool, route, handoff, or mutation order | trajectory eval |
| final answer good but path unsafe or incomplete | trajectory eval with side-effect expectations |
| subjective quality or ambiguous collaboration behavior | human review first, then calibrated LLM judge if useful |
| local repo pressure not yet reusable | repo-local `evals/intake/` packet |
| missing skill trigger or wrong skill trigger | `aoa-skills` trigger design case |
| runtime/MCP state mismatch | `abyss-stack` or MCP owner smoke/check |
| proof authority or public-readout risk | central `aoa-evals` proof bundle or guide update |

## Packet Fields

When a candidate survives the gates, record it with neutral evidence fields.
Avoid process/person fields unless an owning review surface explicitly requires
them.

| Field | Meaning |
| --- | --- |
| `source_ref` | bounded trace/session/file/command reference |
| `task_pressure` | what the user or system needed at that moment |
| `expected_route` | owner-backed behavior expected from the agent |
| `actual_trajectory` | what the agent actually did |
| `first_failure` | earliest meaningful break, before downstream cascade |
| `consequence` | why this matters |
| `owner_surface_refs` | docs, validators, route cards, ports, or runtime contracts that can judge it |
| `freshness_refs` | dates, branch/runtime state, source freshness, or sibling status needed to interpret it |
| `privacy_boundary` | what may be quoted, summarized, redacted, or kept local |
| `existing_surface_check` | checked existing eval/test/validator or marked unknown |
| `evaluator_fit` | validator, contract test, property test, trajectory eval, human rubric, local intake, skill trigger, or runtime smoke |
| `candidate_state` | observed, needs_owner_review, duplicate_existing_eval, local_only, central_draft, rejected, deferred, or accepted |
| `candidate_state_reason` | one concrete reason for the state |
| `next_step` | smallest owner-respecting action |

## Manual Mining Implication

`.aoa` indexes, session summaries, and search hits are pointer generators only.
They are not reviewed truth.

Manual mining should read bounded source evidence and write open notes about the
first failure before grouping cases into a taxonomy. Search can help build a
queue, but the keep/reject decision must come from reading the trace or segment
against the gates above.

Useful pointer signals include:

- user correction immediately after an assistant completion or status claim
- repeated "what next" or "is that all" loops after a supposed closeout
- failed validation or dirty worktree after a success claim
- landing, release, or runtime work without the expected live check
- source/generation mismatch after a generated reader update
- high-turn loops around the same owner-boundary problem
- session segments where the agent changes durable docs before research or
  route inspection

Pointer signals are not candidates by themselves.

## Automation Boundary

Before a reviewed taxonomy exists, automation may only propose review queues and
surface missing evidence. It must not auto-promote, auto-reject, or write
durable proof claims.

After enough manually reviewed cases exist, automation may help with:

- grouping open notes into provisional failure families
- detecting duplicates against existing evals and validators
- finding stale source refs or missing owner refs
- suggesting evaluator fit
- preparing local intake drafts for human review

Automation still stays below source owners, review notes, and bundle-local proof.

## OS Abyss Owner Map

| Surface | Role in discovery |
| --- | --- |
| `.aoa` | raw/session evidence and freshness pointers only |
| local repo `evals/` | repo-owned pressure, intake packets, local suites, and reports |
| `aoa-evals` | proof doctrine, central bundles, shared guide criteria, generated proof readers |
| `aoa-evals-mcp` | access plane; it can expose packets or status but must not create proof truth |
| `aoa-skills` | trigger and workflow behavior that can become skill-level eval pressure |
| `abyss-stack` | runtime, MCP, observability, and live host checks |
| generated/readmodel surfaces | derived selectors; weaker than authored source and reviewed evidence |

## First Use Path

1. Build a small review queue from pointer signals, not eval keywords.
2. Read bounded source evidence manually.
3. For each possible case, fill the admission gates and packet fields.
4. Reject and defer aggressively with one concrete reason.
5. Open-code kept cases, then group them into a failure taxonomy.
6. Route recurring, owner-clear cases to local intake, trigger design, runtime
   owner checks, or central bundle design.
7. Update this guide only after real reviewed evidence shows a better criterion.

The exit condition is a small set of high-signal candidates whose expected
route, observed break, consequence, owner, and repeatability path are all
inspectable.
