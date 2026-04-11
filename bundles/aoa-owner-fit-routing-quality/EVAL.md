---
name: aoa-owner-fit-routing-quality
category: boundary
status: draft
summary: Checks whether a reviewed growth-refinery candidate is routed to the right owner layer with one clear owner hypothesis, honest nearest-wrong-target reasoning, and no first-authoring drift into derivative repos.
object_under_evaluation: reviewed owner-fit routing quality for growth-refinery candidates
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-owner-fit-routing-quality

## Intent

Use this eval to judge whether a reviewed growth-refinery candidate is being
routed to the right owner layer for bounded reasons.

This draft bundle is a `boundary` proof surface.
It does not replace lineage integrity, and it does not replace final owner
proof.

## Object under evaluation

This eval checks reviewed owner-fit routing quality for growth-refinery
candidates.

Primary surfaces under evaluation:

- chosen `owner_hypothesis`
- chosen `owner_shape`
- rejected `nearest_wrong_target`
- bounded evidence that explains the chosen owner layer

Nearby surfaces intentionally excluded:

- final planted object quality
- broad long-term usefulness
- derivative repos acting as first-authoring homes

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the reviewed candidate is routed to one bounded owner layer with one clear
owner hypothesis, one honest nearest-wrong target, and one reviewable reason
set.

This eval does not support claims such as:

- the final planted object is high quality
- the owner choice will remain optimal forever
- derivative repos may absorb first-authoring meaning

## Trigger boundary

Use this eval when:

- the candidate is already reviewed
- the main question is owner choice rather than chain integrity
- nearby owner layers are plausible enough to cause drift
- nearest-wrong-target reasoning matters to the rollout

Do not use this eval when:

- the main question is lineage-chain integrity
- the main question is final object quality
- no reviewed candidate exists yet

## Inputs

- one reviewed candidate
- bounded evidence refs
- chosen owner hypothesis
- chosen owner shape
- rejected nearest-wrong target
- route doctrine for derivative-repo exclusions

## Fixtures and case surface

Strong bounded cases should include:

- one clearly correct owner target
- one ambiguous candidate that still resolves cleanly
- one case where `aoa-routing` or `aoa-kag` looks tempting but should stay
  derivative

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit routing notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- one clear owner target exists
- nearest-wrong target is plausible, not perfunctory
- routing does not drift first-authoring meaning into `aoa-routing` or
  `aoa-kag`
- explanation quality stays specific and bounded

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone owner-fit read for one reviewed candidate family.
It does not compare routes over time, and it does not assign a score.

## Execution contract

A careful run should:

1. gather the reviewed candidate dossier
2. inspect chosen owner and nearest-wrong target
3. verify derivative repos remain derivative
4. publish one bounded routing-quality read

## Outputs

The eval should produce:

- one bounded verdict
- one owner-fit note per reviewed candidate
- one explicit nearest-wrong-target note

## Failure modes

Main ways this eval can fail as an instrument:

- owner-fit is inferred from thin rhetoric instead of bounded evidence
- derivative repos become stealth first-authoring homes
- final object quality is inferred from a clean routing note

## Blind spots

This eval does not prove:

- final planted object quality
- long-term adoption or usefulness
- lineage-chain integrity by itself

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the owner-fit reasoning is reviewably strong on this candidate surface.

Do not treat a positive result as:

- proof of final object quality
- proof that the chosen owner will never need revision
- permission to skip later proof on the final owner object

## Verification

- review one clearly correct owner case
- review one ambiguous case with a real nearest-wrong target
- confirm derivative-repo drift is rejected explicitly

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol

## Adaptation points

- add owner-local doctrine fixtures after the proving run
- keep owner-fit proof weaker than final owner-object proof
