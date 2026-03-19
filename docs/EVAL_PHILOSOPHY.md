# Eval Philosophy

## Why this repository exists

Strong agents create artifacts.
Stronger agents create convincing artifacts.
Neither fact alone proves quality.

`aoa-evals` exists because growth without evaluation tends to drift toward narrative, taste, or self-deception.

This repository is for bounded proof.

It asks:
- what exactly do we think is true about agent quality?
- what evidence supports that claim?
- under which boundaries is the claim valid?
- what would count as regression?
- what would count as mere style change?
- what remains unknown even after the eval runs?

## Core stance

Evaluation is not the same thing as truth.

An eval is a bounded, reproducible way of learning something defensible about quality.

Good evals reduce self-deception.
Bad evals create false confidence theater.

This repository prefers explicit limits over inflated certainty.

## What an eval should do

A strong eval should:
- make a bounded claim explicit
- say what is in scope and out of scope
- use a repeatable execution path
- produce a reviewable verdict or report
- help compare states across time or variants
- make regressions visible
- name its blind spots

A strong eval should not pretend to measure everything.

## What an eval is not

An eval is not:
- a random test
- a one-off project script
- a giant run dump
- a vague confidence score with no interpretation contract
- a single number standing in for total capability
- proof of general intelligence
- a replacement for human judgment in all cases

## Artifacts, processes, and proof

Artifacts matter.
Processes matter.
Neither is enough by itself.

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

Never as the whole truth of quality.

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

Blind spots are not embarrassing leftovers.
They are part of the truth contract.

A bundle that cannot name its blind spots is not ready to make strong claims.

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
If it cannot survive outside one narrow environment, it may still be useful locally,
but it is not yet a good public proof surface.

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

The goal of evaluation is not humiliation and not performance theater.

The goal is disciplined growth.

Evaluation should help us:
- see what is real
- see what is weak
- prioritize what matters
- compare improvement honestly
- avoid lying to ourselves

This repository treats evaluation as a growth organ, not a punishment ritual.

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

Not:
- "the agent is good"

But something closer to:
- "under these conditions, on this surface, with these fixtures and this scoring logic, this bounded claim is supported to this degree, with these blind spots"

That is enough.
That is already powerful.
That is the kind of proof this repository exists to preserve.
