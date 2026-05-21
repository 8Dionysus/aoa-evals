---
name: aoa-repair-boundedness
category: workflow
status: draft
summary: Checks whether a reanchor or self-repair move stays bounded, preserves owner boundaries, and leaves a reviewable trail instead of smearing scope inflation across layers.
object_under_evaluation: bounded repair and reanchor quality on growth-refinery follow-through moves
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-repair-boundedness

## Intent

Use this eval to judge whether a self-repair or reanchor move preserved
boundedness and did not quietly widen authority or scope.

This draft bundle is a `workflow` proof surface.
It does not replace final proof on the repaired owner object.

## Object under evaluation

This eval checks bounded repair and reanchor quality on growth-refinery
follow-through moves.

Primary surfaces under evaluation:

- repair target seam
- explicit owner-boundary preservation
- bounded ambiguity reduction
- reviewable artifact trail left by the repair move

Nearby surfaces intentionally excluded:

- final planted object quality
- permanent stability of the repaired object
- broad route-health stories

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the repair or reanchor move stayed bounded, preserved ownership boundaries,
and reduced ambiguity without smearing scope inflation across layers.

This eval does not support claims such as:

- the repaired object will stay stable forever
- the repair move replaces later proof on the final owner object
- any widening disguised as repair is acceptable because the result improved

## Trigger boundary

Use this eval when:

- a misroute, diagnosis, or repair move changed the follow-through path
- the main question is whether the repair stayed bounded
- scope or authority drift is a plausible failure mode
- a reviewable artifact trail exists

Do not use this eval when:

- the main question is first-owner routing quality
- the main question is final object quality
- there is no concrete repair or reanchor move to inspect

## Inputs

- one repair or reanchor artifact trail
- one named target seam
- owner-boundary notes
- ambiguity before and after the repair move
- downstream follow-through artifact refs

## Fixtures and case surface

Strong bounded cases should include:

- one honest bounded repair
- one scope-inflating repair that should fail
- one reanchor move that correctly narrows owner ambiguity

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit repair notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- the repair move states its target seam clearly
- ownership boundaries remain explicit
- ambiguity is reduced rather than smeared across layers
- the artifact trail remains reviewable enough for follow-up proof

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone bounded-repair read.
It does not compare repairs over time, and it does not assign a growth score.

## Execution contract

A careful run should:

1. gather the repair or reanchor artifact trail
2. inspect the named target seam
3. verify owner-boundary preservation
4. confirm the move reduced ambiguity without widening scope
5. publish one bounded repair-quality read

## Outputs

The eval should produce:

- one bounded verdict
- one repair note per reviewed move
- one explicit ambiguity-reduction note

## Failure modes

Main ways this eval can fail as an instrument:

- scope inflation hides behind successful-looking repair prose
- owner boundaries smear across adjacent layers
- a reviewable trail is missing but the bundle still reads as strong

## Blind spots

This eval does not prove:

- permanent stability of the repaired object
- final owner-object quality
- that the first routing choice was correct

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the repair or reanchor move stayed reviewably bounded on this surface.

Do not treat a positive result as:

- proof of final object quality
- proof that no further proof is needed
- permission to widen future repair scope silently

## Verification

- review one honest bounded repair
- review one widening-shaped failure
- confirm the artifact trail remains reviewable

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol

## Adaptation points

- add real repair-trail fixtures after the proving run
- keep this bundle weaker than final owner proof
