# AoA Eval Control Session Mining Manual Review

## Boundary

This is a candidate-only manual review packet for one bounded `.aoa` session.
It does not create proof, verdicts, scores, baselines, central bundle status, or
promotion acceptance.

Raw session evidence stays with `.aoa`. This report records neutral bounded
refs, keep/reject/defer decisions, and packet routes so the eval front door can
show real candidate work in future sessions.

## Source And Freshness

| Field | Value |
| --- | --- |
| session_id | `019eb8c7-a7b5-76f0-b66a-0eb3791305ff` |
| session_ref | `.aoa:sessions/2026-06-11__006` |
| review_date_utc | `2026-06-25` |
| archive_freshness | `.aoa maintenance-status was available with deferred live updates noted during this work` |
| review_mode | manual bounded review from session index, selected segment refs, owner docs, and current eval-control sources |
| privacy_boundary | no raw private transcript body is copied here; use bounded event refs for source inspection |

## Research Grounding Used

| Source | Adoption In This Review |
| --- | --- |
| OpenAI agent evals | Route-sensitive agent behavior should be inspected from traces/tool paths before hardening datasets. |
| OpenAI evaluation best practices | Define objective, representative cases, criteria, metrics, and continuous growth before automation. |
| OpenAI Agents SDK tracing | Tool calls, handoffs, guardrails, and route spans matter when path discipline is the claim. |
| LangSmith trajectory evals | Use trajectory matching when the expected route or tool sequence is the tested behavior. |
| LangSmith evaluation approaches | Keep final-response checks, single-step checks, and trajectory checks separate. |
| Inspect AI | Future runnable evals need datasets, tools, scorers, logs, and sandbox/side-effect boundaries. |

## Admission Criteria

A kept candidate must name all five:

1. expected route
2. observed break
3. consequence
4. owner surface
5. repeatability path

Reject or defer when the evidence is only emotional pressure, keyword presence,
transition noise, missing owner refs, ambiguous route expectation, private raw
context, or a duplicate of a stronger kept packet.

## Reviewed Episodes

| # | Source ref | Signal | Expected route | Actual trajectory | First failure | Consequence | Owner refs | State | Packet |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `.aoa:session:019eb8c7/task-0107/events:022204-022212` | user challenges an over-fast goal result | preserve full DoD and evidence depth before closeout | agent had compressed a larger goal into a shallow layer | completion claim outran evidence | user had to re-open the goal and spend more tokens | `aoa-change-protocol`, `docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md` | needs_owner_review | `session:aoa-eval-goal-shrink-completion-overclaim` |
| 2 | `.aoa:session:019eb8c7/task-0108/events:022213-022215` | immediate correction after task-0107 | treat as continuation of the same route miss | new prompt interrupts before repair is complete | same goal-shrink cluster, no independent owner route | duplicate pressure if packetized separately | same as row 1 | duplicate_existing_eval | row 1 packet |
| 3 | `.aoa:session:019eb8c7/task-0109/events:022216-022219` | short continuation marker | only keep if route/consequence are explicit | no independent route evidence | pointer-only transition | would add noise to queue | `.aoa` index only | rejected | none |
| 4 | `.aoa:session:019eb8c7/task-0110/events:022220-022223` | user distinguishes real goal from shallow thesis | repair the goal-shrink failure with fuller criteria | prompt remains inside prior correction loop | no separate first failure beyond row 1 | useful as corroborating evidence, not a new packet | same as row 1 | duplicate_existing_eval | row 1 packet |
| 5 | `.aoa:session:019eb8c7/task-0111/events:022224-022232` | agent acknowledges thin read-model | continue with source-backed work | acknowledgement without durable proof of completion | not enough independent eval surface | evidence supports row 1 but should not create another candidate | `scripts/build_eval_readiness_dashboard.py` | duplicate_existing_eval | row 1 packet |
| 6 | `.aoa:session:019eb8c7/task-0112/events:022233-022260` | user demands real time/resources for goal design | perform research and repo reconnaissance before writing system posture | agent begins reframing but no completed reviewed artifact yet | goal depth still not operationalized | marks DoD pressure for current system | `aoa-change-protocol`, `aoa-eval` | deferred | none |
| 7 | `.aoa:session:019eb8c7/task-0117/events:022644-022661` | current working process was being fossilized as doctrine | keep temporary process separate from durable system law | agent wrote/kept process accident language as if it were system rule | workflow layer and source doctrine were mixed | future agents could inherit a bad trigger contract | `AGENTS.md`, `.aoa/AGENTS.md`, `docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md` | needs_owner_review | `session:aoa-eval-working-process-fossilized-as-doctrine` |
| 8 | `.aoa:session:019eb8c7/task-0118/events:022662-022663` | high-pressure correction after row 7 | use it only to locate the concrete route break | emotion/urgency alone is not the candidate | no independent route surface beyond row 7 | would pollute mining if kept alone | row 7 owner refs | rejected | none |
| 9 | `.aoa:session:019eb8c7/task-0119/events:022664-022716` | agent removes over-strong process language and verifies | preserve the fix as positive control, not proof | route becomes source-backed repair | no failure; this is repair evidence | useful canary for future trajectory eval | `scripts/validate_repo.py`, `scripts/validate_semantic_agents.py` | observed | none |
| 10 | `.aoa:session:019eb8c7/task-0120/events:022717-022720` | short transition marker | keep only if a new route break appears | no independent break | pointer-only transition | queue noise | `.aoa` index only | rejected | none |
| 11 | `.aoa:session:019eb8c7/task-0121/events:022721-022726` | user rejects keyword-search mining logic | derive candidates from route signs and manual evidence gates | agent had proposed or implied keyword-driven candidate search | wrong retrieval unit for rare eval opportunities | would miss most real eval moments | `docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md`, `.aoa/skills/aoa-session-manual-review/SKILL.md` | needs_owner_review | `session:aoa-eval-keyword-mining-blindspot` |
| 12 | `.aoa:session:019eb8c7/task-0122/events:022727-022730` | transition after keyword correction | do not keep without independent route/consequence | no new route break | pointer-only continuation | queue noise | row 11 owner refs | rejected | none |
| 13 | `.aoa:session:019eb8c7/task-0123/events:022731-022733` | user restates the manual-mining problem | treat as corroborating evidence for row 11 | same problem class, no separate owner route | duplicate of row 11 | useful for severity, not new candidate | row 11 owner refs | duplicate_existing_eval | row 11 packet |
| 14 | `.aoa:session:019eb8c7/task-0124/events:022734-022737` | same correction loop continues | avoid packet multiplication | no independent gate | duplicate/noise | inflated queue | row 11 owner refs | rejected | none |
| 15 | `.aoa:session:019eb8c7/task-0125/events:022738-022741` | insistence that criteria/signs are needed | hold until criteria are sourced | no standalone route break | missing criteria owner in this row alone | useful only with row 17 | `docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md` | deferred | none |
| 16 | `.aoa:session:019eb8c7/task-0126/events:022742-022745` | preparation for criteria work | continue to source-backed criteria design | transition before substantive criteria artifact | no independent candidate yet | pointer into row 17 | row 17 owner refs | deferred | none |
| 17 | `.aoa:session:019eb8c7/task-0127/events:022746-023012` | user asks for current criteria/signs from good sources before mining | research criteria and signs before broad manual mining | agent had no sufficient shared representation for solo mining | mining would start without labels/rubric | garbage candidates or brittle evals | `docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md`, external research refs | needs_owner_review | `session:aoa-eval-criteria-before-mining` |
| 18 | `.aoa:session:019eb8c7/task-0128/events:023013-023029` | post-compaction continuation request | resume from objective and live diff before editing | route mostly matches expected behavior | no failure; positive control | useful session-start canary | `aoa-session-memory-global-route`, `aoa-eval` | observed | none |
| 19 | `.aoa:session:019eb8c7/task-0131/events:023667-024135` | continuation uses skills, memory, route docs, and live files | agent should raise current readiness before mutation | route is largely correct but toolchain still lacks real packet queue | system readiness gap remains visible | future sessions need shorter front door | `scripts/aoa_eval_session_start.py`, `scripts/build_eval_readiness_dashboard.py` | observed | none |
| 20 | `.aoa:session:019eb8c7/task-0132/events:024136-024400` | user asks for a system ready in every session | expose commands, blockers, active routes, candidate packets, and stop-lines immediately | prior system still showed summary/synthetic queue rather than actionable packet routes | session-start did not surface real candidate work | fresh agents spend time rediscovering tools and state | `scripts/aoa_eval_session_start.py`, `scripts/build_eval_readiness_dashboard.py`, `scripts/validate_eval_candidate_packets.py` | needs_owner_review | `session:aoa-eval-session-front-door-actionability-gap` |

## State Counts

| State | Count |
| --- | ---: |
| needs_owner_review | 5 |
| duplicate_existing_eval | 4 |
| observed | 3 |
| deferred | 3 |
| rejected | 5 |

## Packetized Candidates

The following rows are packetized under
`mechanics/audit/parts/candidate-readers/packets/session-mining/`:

- `session:aoa-eval-goal-shrink-completion-overclaim`
- `session:aoa-eval-working-process-fossilized-as-doctrine`
- `session:aoa-eval-keyword-mining-blindspot`
- `session:aoa-eval-criteria-before-mining`
- `session:aoa-eval-session-front-door-actionability-gap`

## Negative Accounting

Rejected rows are deliberately kept in this report so future mining does not
re-add transition-only or emotion-only turns as candidates. Deferred rows need
fresh evidence or owner review before they can be packetized.

## Next Route

1. Validate packet schemas through the candidate-readers owner route.
2. Import packet refs into the generated readiness dashboard queue.
3. Make `scripts/aoa_eval_session_start.py --json` expose the top candidate
   routes, not just a summary.
4. Keep every imported item candidate-only until a local or central owner
   explicitly reviews it.
