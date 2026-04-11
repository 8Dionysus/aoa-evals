---
name: aoa-candidate-lineage-integrity
category: capability
status: draft
summary: Checks whether a growth-refinery lineage chain stays internally coherent across checkpoint carry, reviewed candidate, seed staging, and downstream owner evidence without inferring stronger landing than the artifacts support.
object_under_evaluation: growth-refinery lineage-chain coherence across checkpoint, reviewed harvest, seed staging, and owner evidence surfaces
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-candidate-lineage-integrity

## Intent

Use this eval to check whether one bounded growth-refinery lineage remains
internally coherent and reviewable.

This draft bundle is a `capability` proof surface.
It does not decide owner fit, and it does not grade final object quality.

## Object under evaluation

This eval checks growth-refinery lineage-chain coherence across checkpoint,
reviewed harvest, seed staging, and owner evidence surfaces.

Primary surfaces under evaluation:

- provisional `cluster_ref` carry
- reviewed `candidate_ref` identity
- staged `seed_ref`
- downstream `object_ref` when it exists
- dropped or superseded branch markers

Nearby surfaces intentionally excluded:

- owner-fit doctrine by itself
- final planted object quality
- broad route health or growth scores

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the bounded lineage chain
`cluster_ref -> candidate_ref -> seed_ref -> object_ref`
stays internally consistent and reviewable enough for downstream proof and
stats to read honestly.

This eval does not support claims such as:

- the candidate belongs in one specific owner repo
- the final planted object is high quality
- owner receipts may be replaced by lineage structure alone

## Trigger boundary

Use this eval when:

- lineage artifacts span more than one owner layer
- the main question is chain integrity rather than owner choice
- dropped or superseded branches must stay visible
- proof or stats would overread the chain without a bounded integrity pass

Do not use this eval when:

- the main question is owner-fit routing quality
- the main question is final planted object quality
- only one layer exists and there is no real lineage chain to test

## Inputs

- one bounded lineage bundle
- checkpoint carry artifact or example
- reviewed candidate artifact or receipt
- staged seed artifact or receipt when present
- downstream owner object ref when present
- explicit drop or supersession markers when present

## Fixtures and case surface

Start with synthetic lineage bundles and one real reviewed lineage later.

Strong bounded cases should include:

- one clean forward lineage
- one dropped branch
- one superseded branch
- one case where a required stage is missing and the chain should fail

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit integrity notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- no stage appears before its prerequisite
- `candidate_ref` does not appear before reviewed harvest
- `seed_ref` does not appear before seed staging
- `object_ref` does not appear before owner landing
- dropped and superseded paths stay explicit
- `nearest_wrong_target` and owner-shaping context do not disappear without
  explanation

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone integrity check for one bounded lineage bundle.
It does not compare one lineage against another, and it does not assign a
growth score.

## Execution contract

A careful run should:

1. collect the bounded lineage bundle
2. verify stage order and required field presence
3. inspect dropped and superseded paths for honest representation
4. publish a bounded integrity read with explicit claim limits

## Outputs

The eval should produce:

- one bounded verdict
- one concise integrity note per reviewed lineage
- explicit missing-stage or overclaim flags

## Failure modes

Main ways this eval can fail as an instrument:

- structural coherence is mistaken for owner-fit proof
- final object quality is inferred from a clean lineage chain
- dropped or superseded branches disappear from the public read

## Blind spots

This eval does not prove:

- correct owner selection by itself
- final planted object quality
- that owner receipts are unnecessary

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the lineage chain is structurally coherent enough to review honestly.

Do not treat a positive result as:

- proof of final owner quality
- proof of correct owner-fit routing
- permission to skip owner-local evidence

## Verification

- review one clean chain and one failure-shaped chain
- confirm dropped and superseded branches stay visible
- confirm claim limits remain explicit in the report

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol

## Adaptation points

- add a real reviewed lineage family once the proving run exists
- keep later fixtures subordinate to owner receipts and proof
