---
name: aoa-continuity-anchor-integrity
category: capability
status: draft
summary: Checks whether a bounded self-agency continuity window keeps an inspectable anchor chain across continuity, revision, reanchor, and anchor refs without letting memo, stats, or chat residue become continuity truth.
object_under_evaluation: anchor-chain integrity on bounded self-agency continuity windows
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
  - aoa-bounded-context-map
---

# aoa-continuity-anchor-integrity

## Intent

Use this eval to judge whether a bounded self-agency continuity route keeps one
inspectable anchor chain rather than narrating continuity from residue.

This draft bundle is a `capability` proof surface.
It does not prove autonomy, final object quality, or long-term route health.

## Object under evaluation

This eval checks anchor-chain integrity on bounded self-agency continuity
windows.

Primary surfaces under evaluation:

- `continuity_ref`
- `revision_window_ref`
- `reanchor_ref`
- `anchor_artifact_ref`
- explicit return mode and anchor-trace wording

Nearby surfaces intentionally excluded:

- memo writeback quality by itself
- derived stats quality by itself
- final owner-object quality
- broad self-agency claims

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the continuity route kept one inspectable anchor chain across continuity,
revision, reanchor, and anchor refs without letting chat residue, memo, or
stats replace the anchor.

This eval does not support claims such as:

- the route is autonomous
- the route is permanently stable
- any downstream summary proves anchor integrity by association

## Trigger boundary

Use this eval when:

- a continuity window is already named
- the main question is whether anchor continuity stayed inspectable
- explicit reanchor and return posture matter to the route
- memo or stats drift is a plausible failure mode

Do not use this eval when:

- there is no named continuity chain
- the main question is bounded revision quality rather than chain integrity
- the main question is whether reanchor chose the right return target

## Inputs

- one continuity window artifact
- one anchor trace
- one named anchor artifact
- any explicit reanchor decision
- memo or stats citations when present

## Fixtures and case surface

Strong bounded cases should include:

- one clean continuity chain
- one missing-anchor failure
- one chat-residue-overreach failure

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit anchor notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- the anchor chain is complete and inspectable
- reanchor remains explicit when the route needed return
- memo or stats citations stay weaker than the anchor artifact
- continuity language does not float free from named artifacts

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone anchor-integrity read.
It does not compare continuity windows over time, and it does not assign a
self-agency score.

## Execution contract

A careful run should:

1. gather the named continuity window and anchor trace
2. inspect continuity, revision, reanchor, and anchor refs separately
3. confirm the anchor artifact is inspectable
4. check whether any memo or stats surface is overread as anchor truth
5. publish one bounded anchor-integrity read

## Outputs

The eval should produce:

- one bounded verdict
- one anchor-chain note per reviewed route
- one explicit claim-limit note

## Failure modes

Main ways this eval can fail as an instrument:

- continuity prose hides a missing anchor link
- reanchor is implied but not named
- downstream memo or stats wording is treated as stronger than the anchor

## Blind spots

This eval does not prove:

- reflective revision stayed bounded
- reanchor chose the right last valid artifact
- the final owner artifact is good

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the route kept an inspectable anchor chain on this surface.

Do not treat a positive result as:

- proof of autonomy
- proof of permanent route health
- proof that memo or stats may speak more strongly than the anchor

## Verification

- review one clean anchor chain
- review one missing-anchor failure
- review one memo-or-chat-overreach failure

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol
- aoa-bounded-context-map

## Adaptation points

- add real continuity-chain fixtures after the first reviewed run
- keep this bundle weaker than bounded revision and reanchor proof
