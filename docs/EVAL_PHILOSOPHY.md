# Eval Philosophy

## Why this repository exists

Strong agents create artifacts.
Stronger agents create convincing artifacts.
Quality requires evidence beyond artifact strength and persuasion.

`aoa-evals` exists because growth without evaluation tends to drift toward narrative, taste, or self-deception.

This repository is for bounded proof.

It asks:
- what exactly do we think is true about agent quality?
- what evidence supports that claim?
- under which boundaries is the claim valid?
- what would count as regression?
- what would count as mere style change?
- what remains unknown even after the eval runs?

## Operating Card

| Field | Route |
| --- | --- |
| role | epistemic posture guide for bounded proof |
| input | proof claim, confidence pressure, metric pressure, memory evidence, artifact/process evidence, comparison pressure, blind spot, portability question, or growth claim |
| output | proof distinction, owner route, interpretation boundary, or bundle-local review pressure |
| owner | this guide for evaluation posture; source eval bundles for proof meaning; `docs/PROOF_TOPOLOGY.md` for authority classes |
| next route | source eval bundle, `docs/EVAL_REVIEW_GUIDE.md`, `docs/SCORE_SEMANTICS_GUIDE.md`, `docs/VERDICT_INTERPRETATION_GUIDE.md`, `docs/PROOF_TOPOLOGY.md`, or owning mechanic |
| tools | nearest `AGENTS.md`, root validator, semantic AGENTS validator, generated-reader checks when derived surfaces move |
| validation | `docs/AGENTS.md#validation` |

## Core stance

Evaluation is a bounded, reproducible way of learning something defensible
about quality.
Truth remains broader than one eval run.

Good evals reduce self-deception.
Bad evals create false confidence theater.

This repository prefers explicit limits over inflated certainty.

## Core distinction routes

| Pressure | Route |
| --- | --- |
| artifact looks convincing | ask for bounded proof evidence |
| process looks clean | ask for outcome evidence and interpretation boundary |
| metric looks authoritative | read it as a proxy, lens, and bounded signal |
| memory looks relevant | cite it as recall context and route proof authority to source evidence |
| single run looks strong | compare states across time, variants, or baselines |
| blind spot feels inconvenient | name it as part of the proof contract |
| project-local success looks portable | run the portability boundary before public proof claims |
| growth story looks tempting | keep comparison disciplined and claims bounded |

## What an eval should do

A strong eval should:
- make a bounded claim explicit
- say what is in scope and out of scope
- use a repeatable execution path
- produce a reviewable verdict or report
- help compare states across time or variants
- make regressions visible
- name its blind spots

A strong eval keeps its measurement boundary explicit.

## Adjacent routes

When nearby work looks eval-shaped, route the pressure to the owner surface
before it becomes a proof claim:

| Pressure | Owner route |
| --- | --- |
| random test pressure | test suite, bundle-local check, or fixture integrity route |
| one-off project script pressure | project-local tooling, or a mechanic part only after the operation recurs |
| giant run dump pressure | selected evidence, compact report, or audit candidate packet |
| vague confidence score pressure | score semantics, interpretation boundary, and bundle-local verdict logic |
| total-capability number pressure | bounded report or comparison surface with blind spots attached |
| general-intelligence proof pressure | route away from `aoa-evals` unless a bounded local claim is explicit |
| human-judgment replacement pressure | Eval Review Guide, reviewer decision, and recorded interpretation boundary |

## On memory

Memory is not proof.

Reviewed `aoa-memo` memory can provide recall context only when the eval cites
object ids, provenance, lifecycle, and generated read models.
It can help a reviewer find prior decisions, source refs, and session context,
while proof authority still needs fixtures, selected evidence, scoring or
verdict logic, bundle-local reports, or mechanic-owned proof interpretation.

`aoa-evals` has route_only memory posture until a local memo port exists.
Session evidence routes through `.aoa` or source proof artifacts before any
later `aoa-memo` reviewed intake.
Durable memory, local memo candidates, and export packets route through reviewed
owner surfaces rather than hidden eval-side paths.
Treat `aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs as
access-plane evidence for inspection and review; proof authority and durable
write authority stay with their owner surfaces.

## Artifacts, processes, and proof

Artifacts matter.
Processes matter.
Bounded proof needs both artifact evidence and process evidence.

A beautiful report may hide shallow reasoning.
A clean workflow may still produce fragile outcomes.
A passed test may still miss the real failure surface.

This repository exists to turn artifacts and processes into bounded proof surfaces rather than vague reassurance.

## On metrics

Metrics are useful when bounded.
Metrics are dangerous when treated as reality.

A metric should always be understood as:
- a proxy
- a lens
- a bounded signal

Read every metric as one bounded signal inside a review.

If a metric is used, the bundle should say:
- why this metric exists
- what it captures
- what it misses
- how easily it can be gamed
- how it should be interpreted

## On comparison

Single-run success is interesting.
Comparison is more valuable.

This repository values:
- before vs after
- agent A vs agent B
- mode X vs mode Y
- policy surface 1 vs policy surface 2
- same task over time

Growth becomes more defensible when comparison is disciplined.

## On blind spots

Every eval has blind spots.

They are part of the truth contract.

Strong claims require named blind spots.

Common blind spots include:
- fixture overfitting
- scorer bias
- reward hacking
- style substitution for quality
- narrow task coverage
- hidden private context
- unstable environment assumptions
- false pass from shallow compliance

## On portability

Portable evals matter because project-local magic is cheap and misleading.

A public eval bundle should be understandable and runnable outside its birth context with reasonable effort.
A one-environment bundle can still be useful locally; public proof waits for a portable route.

## On regression

Regression is one of the main reasons this repository exists.

Agent systems can look stronger while becoming:
- less reliable
- less bounded
- less safe
- less honest about uncertainty
- more style-heavy and less substance-heavy

A good eval should help detect these silent losses.

## On growth

The goal of evaluation is disciplined growth.

Evaluation should help us:
- see what is real
- see what is weak
- prioritize what matters
- compare improvement honestly
- avoid lying to ourselves

This repository treats evaluation as a growth organ and proof discipline.

## Human review and structured outputs

Human-readable meaning stays primary.

Structured outputs, scores, schemas, and reports are valuable,
but they should remain legible, bounded, and reviewable.

The repository should prefer:
- human-interpretable verdicts
- compact report artifacts
- clear score semantics
- explicit interpretation notes

over opaque benchmark spectacle.

## Final contract

A public eval bundle should tell the truth in a bounded way.

Weak form:
- "the agent is good"

Bounded form:
- "under these conditions, on this surface, with these fixtures and this scoring logic, this bounded claim is supported to this degree, with these blind spots"

That is enough.
That is already powerful.
That is the kind of proof this repository exists to preserve.
