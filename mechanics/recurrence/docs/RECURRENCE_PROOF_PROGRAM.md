# Recurrence Proof Program for `aoa-evals`

## Role

Use this guide as the mechanic-wide route map for recurrence-aware proof work
inside `aoa-evals`.

It helps an agent choose the right recurrence part, source proof bundle,
bounded review route, or stronger-owner handoff when return, memory, recursor,
stats, beacon, or overclaim pressure appears.

| Pressure | Owner route |
| --- | --- |
| recurrence control-plane proof | recurrence part or source proof bundle |
| source proof meaning | bundle-local `evals/**/EVAL.md` and `eval.yaml` |
| concrete fixture, runner, scorer, manifest, hook, or test payload | owning recurrence part or bundle route |
| runtime return, memory canon, stats truth, or recursor activation | stronger owner before eval-side proof adoption |

## Mechanic-wide Scope

Use this guide to keep recurrence-aware proof work split across the active
recurrence parts and nearby source bundles without collapsing return, memory,
recursor, stats, beacon, and overclaim questions into one mega-bundle.

The mechanic-wide route is:

`recurrence pressure -> active recurrence part or source bundle -> bounded review -> report, decision packet, or owner handoff`

Concrete fixtures, schemas, runners, scorers, manifests, hooks, and tests stay
under the owning recurrence part or bundle route.

## Source Surfaces

- `mechanics/recurrence/README.md`
- `mechanics/recurrence/DIRECTION.md`
- `mechanics/recurrence/PARTS.md`
- `mechanics/recurrence/parts/`
- `evals/workflow/aoa-return-anchor-integrity/EVAL.md`
- `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`
- `mechanics/EVIDENCE_CLUSTERS.md`

## Stronger Owner Split

`aoa-evals` owns bounded claim wording, verdict logic, report interpretation,
bundle distinctness, and anti-overclaim posture. `Agents-of-Abyss` owns
recurrence doctrine. Runtime owners own return execution and artifact
contracts. `aoa-memo` owns checkpoint memory objects and memory canon.
`aoa-stats`, `aoa-routing`, `aoa-playbooks`, KAG, and Agon owners keep their
own truth.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| global recurrence completeness or hidden continuity | keep the claim at the bounded recurrence proof question |
| recursor activation or runtime owner mutation | route to the runtime or role owner before eval-side adoption |
| portable proof by beacon or manifest | keep beacon and manifest evidence below bundle-local review |
| stats, generated projections, recurrence hooks, or owner refs as source truth | route to the source owner and cite them as evidence sidecars only |
| broad capability score from multiple recurrence families | keep claim families split by active part or source bundle |

## Purpose

This note defines how recurrence lands inside `aoa-evals` without creating a
new proof empire.

`aoa-evals` may read return-aware artifacts and selected runtime return
evidence as bounded proof inputs.
It remains the owner of:

- bounded claim wording
- verdict logic
- report interpretation
- bundle distinctness
- anti-overclaim posture

Stronger owner routes stay outside this proof program:

| Concern | Stronger owner |
| --- | --- |
| recurrence doctrine | `Agents-of-Abyss` |
| return policy | `abyss-stack` |
| runtime artifact contracts | `aoa-agents` |
| scenario composition | `aoa-playbooks` |
| checkpoint memory objects | `aoa-memo` |
| navigation hints | `aoa-routing` |

## Core rule

When a route loses its axis, source boundary, active phase, expected artifact,
or verification posture, smooth continuation should not be rewarded by default.

The eval-side question is smaller and stricter:

> when the route returned, did it return to a real anchor and re-enter honestly?

That question is evaluable.
It is narrower than general capability, narrower than final-answer quality, and
narrower than broad safety claims.

## Distinct claim families

Recurrence-aware proof in `aoa-evals` should stay split across nearby jobs
rather than collapsing into one mega-bundle.

### `aoa-return-anchor-integrity`

This is the first proposed return-specific bundle.

It checks whether a return-capable route:

- named a real `return_reason`
- pointed to a valid anchor rather than atmosphere
- rebuilt context from bounded anchor surfaces rather than hidden raw continuity
- re-entered with an honest note or stopped honestly
- stayed inside a bounded loop discipline

This bundle stays on anchor fidelity and honest re-entry.
Its current materialized draft proof flow runs through
`mechanics/recurrence/parts/anchor-return/fixtures/return-anchor-v1/README.md`,
`evals/workflow/aoa-return-anchor-integrity/fixtures/contract.json`,
`evals/workflow/aoa-return-anchor-integrity/runners/contract.json`, and the
schema-backed companion report in
`evals/workflow/aoa-return-anchor-integrity/reports/example-report.json`.

Keep adjacent questions on their own routes:

| Adjacent question | Route |
| --- | --- |
| final-answer grading | evaluation surface that owns answer quality |
| broad long-horizon competence | `aoa-long-horizon-depth` or another explicit bundle |
| approval classification | `aoa-approval-boundary-adherence` |
| general scope drift diagnosis | `aoa-scope-drift-detection` |
| runtime benchmark ranking | runtime or comparison owner before eval-side adoption |

### `aoa-long-horizon-depth`

This existing draft bundle remains the inquiry-specific restart-fidelity
surface.

Its current materialized draft proof flow runs through
`mechanics/checkpoint/parts/restartable-inquiry/fixtures/long-horizon-restart-v1/README.md`,
`evals/workflow/aoa-long-horizon-depth/fixtures/contract.json`,
`evals/workflow/aoa-long-horizon-depth/runners/contract.json`, and the schema-backed
companion report in
`evals/workflow/aoa-long-horizon-depth/reports/example-report.json`.

Use it when the main question is:

- checkpoint completeness
- contradiction preservation across relaunch
- `memory_delta` versus `canon_delta` separation
- resistance to false continuity in checkpoint-based inquiry

Use `aoa-long-horizon-depth` for that narrower restart-fidelity job.

### `aoa-scope-drift-detection`

Use this when the return route silently widened, narrowed, or reshaped the task
after re-entry.

A return may have a valid anchor and still come back into the wrong task
surface.
That is scope drift, not anchor integrity.

### `aoa-verification-honesty`

Use this when the route returns and then overclaims what it verified.

A return may be real while the post-return report still fakes verification.
That is verification honesty, not anchor integrity.

### `aoa-approval-boundary-adherence`

Use this when the route returns across mutation, approval, or authority
boundaries.

A return may be well-anchored and still cross an action boundary incorrectly.
That is approval posture, not anchor integrity.

### `aoa-eval-integrity-check`

Use the meta-eval as the sidecar whenever public wording around return begins
to inflate.

It should guard against:

- treating return as proof of broad safety
- treating one clean re-entry as proof of general competence
- blurring `aoa-return-anchor-integrity` together with
  `aoa-long-horizon-depth`
- turning runtime return evidence into a capability leaderboard

## Bridge posture

### `AOA-P-0008 long-horizon-model-tier-orchestra`

Keep `aoa-tool-trajectory-discipline` as the primary route-quality anchor for
the first model-tier path.

When the route emits an explicit return decision and return-aware runtime
sidecar, `aoa-return-anchor-integrity` may travel as an adjacent diagnostic
surface.
Keep the primary tool-path or verification read as the owning route.

### `AOA-P-0009 restartable-inquiry-loop`

Keep `aoa-long-horizon-depth` as the primary inquiry restart-fidelity anchor.
Its current draft proof flow is anchored in
`mechanics/checkpoint/parts/restartable-inquiry/fixtures/long-horizon-restart-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.

When the restart route also emits explicit return decisions, anchor refs, or
bounded re-entry notes, `aoa-return-anchor-integrity` may travel as an adjacent
diagnostic surface.
It remains narrower than checkpoint-and-relaunch reading.

### `abyss-stack` runtime wrapper

Selected return events, policy notes, and summary-only runtime evidence may
travel upward through `runtime_evidence_selection`.
They remain evidence sidecars unless and until bundle meaning is explicit.

## Minimum evidence posture

A strong return-aware bounded case should expose, at minimum:

- one explicit return decision or equivalent return event
- one named return reason
- one or more anchor refs
- the bounded surfaces used for context rebuild
- one re-entry note or one safe-stop note
- enough case evidence to show whether raw hidden continuity was still required

Optional helpful sidecars:

- `verification_result`
- `route_decision`
- `bounded_plan`
- `inquiry_checkpoint`
- selected runtime return event summaries
- integrity sidecars that state what not to overread

## Future Candidates

The proof program may later split further into distinct surfaces such as:

- return loop ceiling discipline
- safe-stop honesty
- anchor provenance preservation

Name those as separate public defaults only after case families show that the
split is real and useful.

## External Routes

| Pressure | Route |
| --- | --- |
| return read as a global intelligence score | keep the verdict to the bounded bundle claim |
| model ranking by re-entry prose | use a comparison or benchmark owner that explicitly owns ranking |
| existing workflow, boundary, or restart bundle replacement | keep the existing bundle as the owning proof route |
| runtime governance | route to the runtime owner before eval-side proof use |
| raw runtime logs as public proof | select public-safe candidate evidence, then review through the bundle |

## Boundary to preserve

`aoa-evals` owns bounded proof meaning for recurrence evidence.
The route home stays with the owner that creates or governs the returning
runtime, memory, routing, stats, scenario, or role surface.

## Validation

Use `mechanics/recurrence/AGENTS.md#validation` for executable validation
commands. This mechanic-wide guide names the recurrence proof program; the
route card owns command execution.
