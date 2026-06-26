# Session Mining Criteria And Reject Taxonomy

## Role

This document defines the first manual review layer before `.aoa` session
evidence becomes an eval candidate packet or Eval Forge worksheet.

The first phase is deliberately manual. Keyword search is a locator at most. A
candidate is kept only after a reviewer confirms route pressure, owner surface,
consequence, repeatability, and proof boundary.

## Keep Gates

A candidate can move to Eval Forge only when all core gates are named:

| Gate | Review Question |
| --- | --- |
| Expected route | What should the agent or system have done? |
| Observed break or pressure | What actually happened, or what proof pressure appeared? |
| First failure | Where is the first meaningful failure before downstream noise? |
| Consequence | Why does this matter for correctness, proof, safety, freshness, cost, trust, or OS growth? |
| Owner surface | Which repo, skill, runtime, local port, or central proof surface can judge this? |
| Repeatability path | Can this become a route check, suite, rubric, worksheet, or negative example? |
| Bounded refs | Are source/session/file/command refs narrow enough for review? |
| Privacy/freshness | Is private/raw evidence kept with the owner, and is freshness stated? |
| Existing-surface check | Was central/local/support overlap checked before new design? |

## Positive Signs Without The Word Eval

Trigger review when one or more of these signs appear, even if nobody says
`eval`:

- the agent closes a goal before satisfying the stated DoD or evidence depth;
- a validator, test, support script, or local suite should have been selected
  before new design;
- local pressure, central proof authority, MCP access, and `.aoa` session
  evidence are being mixed;
- the user repeatedly corrects the same route behavior;
- the first tool or owner surface is wrong for the pressure;
- freshness, mirror state, dirty repo state, or runtime availability changes
  the trustworthiness of evidence;
- a skill should have triggered from route signs, but the agent waited for a
  keyword;
- a report, dashboard, generated reader, receipt, or candidate packet starts to
  read like proof;
- a local port has active intake, suite, or report pressure that could become a
  deterministic check or owner-review packet.

## Negative Signs

Reject or defer when the evidence is only:

- a transition message such as "go on", "landing", or "what next" with no
  independent route break;
- anger, urgency, or emotional pressure without a concrete owner-route failure;
- the word `eval`, `test`, `done`, or `landing` without consequence and owner
  route;
- an exact duplicate of a stronger kept packet;
- stale or private raw context with no reviewable refs;
- a broad desire for quality without a bounded object under evaluation;
- a normal unit-test request with no eval-routing pressure;
- a source-of-truth lookup that belongs to source mapping, not eval routing.

## Reject Taxonomy

| Code | Reject When | Action |
| --- | --- | --- |
| `keyword_only` | only weak words such as eval/test/done/landing appear | do not packetize; require route pressure |
| `emotion_only` | frustration is present but no concrete failure can be named | use it to focus review, not as candidate evidence |
| `transition_only` | message only continues work or asks status | keep out of queue |
| `duplicate_existing_candidate` | a stronger packet already covers the failure class | reference the stronger packet |
| `ownerless` | no repo, skill, runtime, port, or proof owner can judge it | defer until owner surface is found |
| `private_raw_only` | evidence cannot be reduced to bounded refs | stop; do not copy raw private text |
| `no_consequence` | failure has no correctness/proof/runtime/user-cost impact | reject as noise |
| `no_repeatability_path` | no plausible check, rubric, suite, or worksheet can use it | defer or reject |
| `existing_surface_first` | central/local/support surface likely already handles it | inspect/apply existing route before new design |
| `automation_premature` | labels, reject reasons, and owner gates are not stable | keep manual; do not build miner automation yet |

## Manual Review Protocol

1. Start from the readiness packet and current `.aoa` freshness status.
2. Select a bounded session span by human review, not by keyword hits alone.
3. Record neutral refs only: session id, task/segment/event range, file path,
   command, packet id, and freshness note.
4. Fill the keep gates before deciding the candidate state.
5. Check central catalog, repo-local port inventory, and support registry before
   proposing any new eval design.
6. Assign one state: `needs_owner_review`, `observed`,
   `duplicate_existing_eval`, `deferred`, or `rejected`.
7. Preserve rejected rows in the manual report when they protect future agents
   from re-adding queue noise.
8. Validate any packetized candidate with
   `python scripts/validate_eval_candidate_packets.py <path>`.

## Minimal Candidate Packet Contract

A kept packet needs:

- stable packet id and source kind;
- bounded source refs and freshness refs;
- trigger class or proposed archetype fit;
- task pressure, expected route, actual route or observed break;
- first failure and consequence;
- owner surface refs;
- privacy boundary;
- positive or next-step route;
- explicit non-promotion rule.

The packet is not a verdict, score, baseline, or central proof object.

## Archetype Routing Hints

| Pressure Class | First Archetype |
| --- | --- |
| criteria missing before mining | `human-review-rubric` |
| goal shrink or completion overclaim | `trace-trajectory-eval` |
| missed trigger without keyword | `aoa-skills-trigger-eval` |
| runtime/MCP/front-door actionability gap | `abyss-stack-runtime-mcp-smoke` |
| active local intake | `local-intake-pressure-packet` |
| active local suite/regression surface | `local-runnable-suite` |
| possible central proof bundle | `central-proof-bundle-draft` only after owner acceptance |

## Automation Stop-Line

Do not automate broad session mining until this layer has enough reviewed
positive cases, negative cases, duplicate accounting, and owner decisions to
calibrate a miner. The first useful automation is a guardrail that preserves
candidate-only posture, not a miner that creates more queue pressure.

