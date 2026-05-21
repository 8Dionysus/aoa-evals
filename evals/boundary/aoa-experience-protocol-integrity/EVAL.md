---
name: aoa-experience-protocol-integrity
category: boundary
status: draft
summary: Checks whether an experience verdict bundle keeps protocol integrity explicit, bounded, and weaker than runtime or governance authority.
object_under_evaluation: experience verdict bundle
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-experience-protocol-integrity

## Intent

Use this eval when the question is whether an experience verdict bundle stays
inside its protocol contract instead of drifting into runtime authority,
governance authority, or vague proof theater.

The route keeps four things explicit:

- what the experience verdict bundle is actually evaluating
- what protocol integrity means on this surface
- what the bundle does not prove
- what evidence still has to remain weaker than owner-local truth

## Object under evaluation

This eval checks experience verdict bundles.

Primary surfaces under evaluation:

- bundle metadata and claims wording
- report schema shape
- example report wording
- protocol boundary notes

Nearby surfaces intentionally excluded:

- runtime execution authority
- governance or certification authority
- bundle-free experience claims
- broad quality claims detached from the bundle contract

## Bounded claim

This eval is designed to support a claim like:

under these conditions, an experience verdict bundle can keep protocol
integrity explicit, stay bounded to its own contract, and avoid implying
runtime or governance authority.

This eval does not support claims such as:

- the bundle proves the underlying experience was good
- the bundle owns runtime truth
- the bundle can certify future protocol behavior
- the bundle replaces owner-local evidence or review

## Trigger boundary

Use this eval when:

- a new experience verdict bundle needs a bounded integrity read
- protocol wording could otherwise drift into overclaim
- the report surface needs a compact verdict contract

Do not use this eval when:

- the task is only about artifact style
- the task is only about runtime behavior
- the task is a broader comparison between artifact and process surfaces

## Inputs

- the bundle `eval.yaml`
- the bundle `EVAL.md`
- the bundle report schema
- the bundle example report
- any boundary note or fixture contract file

## Fixtures and case surface

A strong starter case set should include:

- one clean bounded packet that stays within protocol wording
- one packet where boundary language weakens
- one packet where runtime or governance authority is implied by mistake

Fixture families should avoid:

- private operational payloads
- hidden telemetry
- broad claims without bounded evidence

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit boundary notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- protocol integrity is named clearly
- the bundle does not imply authority it does not own
- the report wording stays below runtime or governance truth
- blind spots remain visible

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded integrity read for one bundle family.

## Execution contract

A careful run should:

1. inspect the bundle metadata and source docs
2. inspect the report schema and example report
3. check the boundary notes and fixture contract
4. publish one bounded verdict with explicit limits

## Outputs

The eval should produce:

- one bounded verdict
- one boundary note for each reviewed case
- one explicit claim-limit note

## Failure modes

Main ways this eval can fail as an instrument:

- protocol wording expands into authority wording
- the report example becomes stronger than the bundle contract
- boundary notes disappear behind polished phrasing

## Blind spots

This eval does not prove:

- the underlying experience was successful
- the bundle is broadly reusable across all protocol families
- the bundle can substitute for runtime, governance, or owner-local review

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the bundle kept protocol integrity explicit on this surface.

Do not treat a positive result as:

- proof of runtime authority
- proof of governance authority
- proof that the underlying experience itself was successful
- a substitute for owner-local review

## Verification

- review the bundle metadata and report schema
- review one clean packet
- review one boundary-leak packet
- review one authority-overreach packet

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol

## Adaptation points

- add real experience verdict cases after the first reviewed run
- keep the protocol contract weaker than runtime or governance surfaces
- reuse the same claim boundary if another experience bundle needs a sibling
  integrity read
