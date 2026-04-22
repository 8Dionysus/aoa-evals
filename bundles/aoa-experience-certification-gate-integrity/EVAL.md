---
name: aoa-experience-certification-gate-integrity
category: boundary
status: draft
summary: Checks whether an experience-derived release candidate has bounded evidence for authorized operator certification review without letting the eval certify.
object_under_evaluation: experience certification gate bundle
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-contract-test
---

# aoa-experience-certification-gate-integrity

## Intent

Use this eval when the question is whether an experience-derived
assistant/service release candidate has enough bounded evidence to proceed to
authorized operator certification review.

The route keeps four things explicit:

- the eval checks evidence sufficiency, not certification authority
- regression evidence and rollback evidence are both required
- compatibility breaks must route to recharter or explicit operator review
- Codex and `aoa-evals` must not emit a certified release verdict

## Object under evaluation

This eval checks experience certification gate bundles.

Primary surfaces under evaluation:

- evidence bundle references
- regression pack coverage
- rollback drill evidence
- compatibility or recharter signal
- operator review requirement

Nearby surfaces intentionally excluded:

- operator certification authority
- deployment ring promotion
- durable rollback execution
- stats dashboard approval

This bundle is diagnostic. It isolates the certification-gate integrity
question and does not claim to exercise the release or deployment workflow.

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a certification gate bundle can show that a release
candidate is ready for authorized operator review while keeping certification
authority outside the eval.

This eval does not support claims such as:

- the candidate is certified
- Codex can certify, approve, or promote the release
- deployment may proceed automatically
- runtime, stats, routing, memo, or SDK surfaces can replace operator review

## Trigger boundary

Use this eval when:

- a release candidate needs a bounded pre-certification evidence read
- an experience-derived patch is moving toward versioned assistant release
- regression, rollback, or compatibility evidence might be missing

Do not use this eval when:

- the task is to certify the candidate
- the task is to promote a rollout ring
- the task is to execute durable rollback
- the task is only a stats or routing summary review

## Inputs

- the candidate evidence bundle
- regression pack coverage notes
- rollback drill evidence
- compatibility or recharter note
- operator review reference or required-review marker
- the bundle report schema and example report

## Fixtures and case surface

A strong starter case set should include:

- one candidate with reviewed experience evidence, regression coverage,
  rollback evidence, and required operator review
- one candidate missing certification authority
- one candidate missing regression evidence
- one candidate missing rollback evidence
- one candidate whose compatibility break requires recharter

Fixture families should avoid:

- private operational payloads
- hidden production telemetry
- release approval language
- deployment ring state that would imply live rollout authority

## Scoring or verdict logic

This eval uses a categorical verdict with an explicit authority ceiling.

Allowed verdict classes:

- `certifiable_with_operator_review`
- `denied_authority`
- `denied_regression`
- `denied_rollback`
- `recharter_required`

The eval must not emit `certified`.

Key review checks:

- reviewed experience evidence is present
- regression evidence is present
- rollback drill evidence is present
- operator review remains required
- compatibility breakage routes to recharter or explicit review

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded integrity read for one certification-gate family.
Without a baseline, it can support a bounded readiness-for-review claim, not a
comparative quality or improvement claim.

## Execution contract

A careful run should:

1. inspect the candidate evidence bundle
2. inspect regression pack coverage
3. inspect rollback drill evidence
4. check compatibility or recharter notes
5. confirm the operator review requirement
6. publish one bounded verdict with explicit limits

The bundle-local runner contract is `runners/contract.json`.
The bundle-local report schema is `reports/summary.schema.json`.
The example report is `reports/example-report.json`.

## Outputs

The eval should produce:

- one bounded verdict
- one authority-ceiling note
- one list of missing inputs when the verdict is denied or requires recharter
- one summary of the evidence checks that were present or absent

Starter support artifacts:

- `notes/origin-need.md`
- `notes/certification-contract.md`
- `checks/eval-integrity-check.md`
- `examples/example-report.md`

## Failure modes

Main ways this eval can fail as an instrument:

- the report wording drifts into certification authority
- missing regression evidence is treated as a warning instead of a denial
- missing rollback evidence is treated as a warning instead of a denial
- compatibility breakage is hidden behind a positive verdict
- operator review becomes optional by implication

## Blind spots

This eval does not prove:

- the release candidate is certified
- the candidate is safe for deployment
- the rollout can promote rings
- runtime health will remain stable after activation
- retention watch will pass after release
- operator review can be skipped

## Interpretation guidance

Treat `certifiable_with_operator_review` as support for a bounded claim:
the evidence packet may proceed to authorized operator review.

Do not treat a positive result as:

- certification
- release approval
- deployment approval
- ring promotion
- rollback permission
- owner-local truth outside the evaluated bundle

## Verification

- review the bundle metadata and report schema
- review one clean candidate packet
- review one missing-authority packet
- review one missing-regression packet
- review one missing-rollback packet
- review one recharter-required packet
- confirm the output never contains `certified`

## Technique traceability

- AOA-T-0001

## Skill traceability

- aoa-contract-test

## Adaptation points

- add real release-candidate cases after the first reviewed run
- keep the verdict weaker than certification authority
- keep deployment watchtower evidence in a separate downstream eval when runtime
  activation is explicitly approved
