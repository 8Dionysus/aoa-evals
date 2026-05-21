---
name: aoa-self-reanchor-correctness
category: boundary
status: draft
summary: Checks whether a bounded self-agency continuity route reanchors to the last valid artifact, keeps return mode explicit, and refuses chat-residue continuity when anchor integrity is lost.
object_under_evaluation: reanchor correctness on bounded self-agency continuity routes
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
  - aoa-bounded-context-map
---

# aoa-self-reanchor-correctness

## Intent

Use this eval to judge whether a bounded continuity route returned to the last
valid artifact rather than widening scope or pretending that conversational
continuity is enough.

This draft bundle is a `boundary` proof surface.
It does not prove anchor integrity by itself, and it does not prove the whole
route stayed healthy.

## Object under evaluation

This eval checks reanchor correctness on bounded self-agency continuity routes.

Primary surfaces under evaluation:

- `reanchor_ref`
- `anchor_artifact_ref`
- explicit return mode
- reason for reanchor
- post-reanchor continuity wording

Nearby surfaces intentionally excluded:

- whether the earlier revision window was bounded
- the full anchor chain by itself
- final owner-object quality
- broad autonomy or selfhood claims

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the route reanchored to the last valid artifact, kept return posture explicit,
and refused chat-residue continuity once boundedness or anchor clarity was
lost.

This eval does not support claims such as:

- reanchor guarantees future success
- any return to an older artifact is automatically correct
- downstream memo or stats surfaces may stand in for the return anchor

## Trigger boundary

Use this eval when:

- a route actually issued or should have issued a `reanchor_ref`
- the main question is whether return posture chose the right anchor class
- chat residue or vague continuity is a plausible failure mode
- explicit return mode matters to the route

Do not use this eval when:

- there is no reanchor decision or trigger to inspect
- the main question is whether the continuity chain existed at all
- the main question is whether revision stayed bounded before reanchor

## Inputs

- one reanchor decision
- one named anchor artifact
- one anchor trace or continuity window
- return-mode notes
- any downstream continuity, memo, or stats wording after reanchor

## Fixtures and case surface

Strong bounded cases should include:

- one correct reanchor to the last valid artifact
- one stale-anchor failure
- one chat-residue-continuity failure

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit reanchor notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- the return target is a named inspectable artifact
- reanchor naming is explicit rather than implied
- the chosen anchor is the last valid one still supported by the route
- downstream continuity wording does not smuggle in chat-residue return

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone reanchor-correctness read.
It does not compare reanchors over time, and it does not assign a continuity
or autonomy score.

## Execution contract

A careful run should:

1. gather the reanchor decision and named anchor artifact
2. inspect why the route needed return
3. verify the chosen anchor is inspectable and still valid
4. check whether post-reanchor wording overreads chat continuity
5. publish one bounded reanchor-correctness read

## Outputs

The eval should produce:

- one bounded verdict
- one reanchor note per reviewed route
- one explicit claim-limit note

## Failure modes

Main ways this eval can fail as an instrument:

- the route returns to a stale or weak artifact
- reanchor is implied but never named
- post-reanchor wording quietly treats remembered context as enough

## Blind spots

This eval does not prove:

- the whole anchor chain was intact before reanchor
- reflective revision was bounded
- the final owner object is high quality

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the route returned to the last valid artifact on this surface.

Do not treat a positive result as:

- proof of autonomy
- proof that the route is now healthy forever
- permission to let memo or stats stand in for reanchor truth

## Verification

- review one correct reanchor
- review one stale-anchor failure
- review one chat-residue-continuity failure

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol
- aoa-bounded-context-map

## Adaptation points

- add real reanchor fixtures after the first reviewed continuity run
- keep this bundle weaker than final owner proof and route-health claims
