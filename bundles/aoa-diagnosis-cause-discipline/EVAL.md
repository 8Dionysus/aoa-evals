---
name: aoa-diagnosis-cause-discipline
category: workflow
status: draft
summary: Checks whether a diagnosis or self-diagnosis move names causal hypotheses, evidence limits, and unknowns without confusing symptoms, owner ambiguity, or repair success with cause proof.
object_under_evaluation: diagnosis and cause-hypothesis discipline on growth-refinery follow-through moves
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-diagnosis-cause-discipline

## Intent

Use this eval to judge whether a diagnosis or self-diagnosis move preserved
cause discipline before repair.

This draft bundle is a `workflow` proof surface.
It does not prove repair success, owner fit, or final object quality.

## Object under evaluation

This eval checks diagnosis and cause-hypothesis discipline on
growth-refinery follow-through moves.

Primary surfaces under evaluation:

- symptom refs
- probable cause hypotheses
- owner ambiguity notes
- explicit unknowns and confidence limits
- repair handoff language

Nearby surfaces intentionally excluded:

- repair boundedness by itself
- final planted object quality
- owner-fit routing quality by itself
- proof that the named cause is ultimately correct

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the diagnosis named plausible causal hypotheses and evidence limits without
collapsing symptoms, owner ambiguity, repair success, or later cleanup into
cause proof.

This eval does not support claims such as:

- the named cause is definitely correct
- the repair worked because the diagnosis was tidy
- owner ambiguity can be treated as a cause without evidence

## Trigger boundary

Use this eval when:

- a diagnosis or self-diagnosis artifact exists before repair
- the main question is whether causal hypotheses stayed honest
- symptom evidence and probable cause evidence can be inspected separately
- unknowns or confidence limits matter to the follow-through path

Do not use this eval when:

- the main question is whether the repair stayed bounded
- the main question is whether the chosen owner layer was correct
- no diagnosis or self-diagnosis artifact exists

## Inputs

- one diagnosis or self-diagnosis artifact
- symptom refs
- probable cause hypotheses
- confidence and unknowns
- owner ambiguity notes when present
- one repair or follow-through handoff

## Fixtures and case surface

Strong bounded cases should include:

- one honest cause-hypothesis diagnosis
- one symptom-as-cause failure
- one repair-success-overclaim failure

## Scoring or verdict logic

This eval prefers a categorical verdict with explicit diagnosis notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Key review checks:

- symptoms stay separated from probable causes
- unknowns and confidence limits remain visible
- owner ambiguity is not flattened into cause language
- repair handoff does not prove the diagnosis true
- evidence limits are not stronger than the reviewed artifact supports

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone cause-discipline read for one diagnosis family.
It does not compare diagnoses over time, and it does not assign a growth score.

## Execution contract

A careful run should:

1. gather the diagnosis or self-diagnosis artifact
2. separate symptom refs from probable cause hypotheses
3. inspect owner ambiguity, unknowns, and confidence limits
4. check whether repair handoff language overclaims cause proof
5. publish one bounded cause-discipline read

## Outputs

The eval should produce:

- one bounded verdict
- one diagnosis note per reviewed artifact
- one explicit claim-limit note

## Failure modes

Main ways this eval can fail as an instrument:

- tidy diagnosis prose hides a symptom-as-cause jump
- repair success is treated as proof that the cause was correct
- owner ambiguity is mislabeled as a cause without evidence

## Blind spots

This eval does not prove:

- the cause is ultimately correct
- the repair worked
- the final object is high quality
- the chosen owner route is correct

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the diagnosis kept symptom, cause, owner ambiguity, and unknowns reviewably
separate on this surface.

Do not treat a positive result as:

- proof of repair success
- proof of final object quality
- proof that no later cause revision is needed

## Verification

- review one honest cause-hypothesis diagnosis
- review one symptom-as-cause failure
- review one repair-success-overclaim failure

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-change-protocol

## Adaptation points

- add real diagnosis fixtures after the proving run
- keep this bundle weaker than repair proof and owner proof
