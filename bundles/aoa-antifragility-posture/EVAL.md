---
name: aoa-antifragility-posture
category: stress
status: draft
summary: Checks whether one owner-local surface handles a named stressor family through bounded degraded continuation, source-owned receipts, and split-axis readout without stealing source ownership.
object_under_evaluation: owner-local antifragility posture for one surface and stressor family
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies:
  - AOA-T-0097
  - AOA-T-0098
skill_dependencies: []
---

# aoa-antifragility-posture

## Intent

Use this eval to read one bounded antifragility family without letting proof surfaces steal source ownership.

This bundle is a `diagnostic` stress eval.
It checks whether one named owner-local surface handled one named stressor family through:
- bounded degraded continuation
- source-owned receipt emission
- explicit anti-widening posture
- split-axis readout

It is not a repo-global resilience score and not a general quality verdict.

## Object under evaluation

This eval checks the antifragility posture of one owner-local surface under one named stressor family.

The current first-wave exemplar is:
- repo: `ATM10-Agent`
- surface: `hybrid-query`
- stressor family: retrieval succeeds while the KAG stage fails or returns no useful expansion

Included nearby surfaces:
- source-owned stressor receipts
- linked owner-local run artifacts
- optional adaptation deltas
- optional bounded eval evidence that stays subordinate to the owner-local receipt

Excluded nearby surfaces:
- repo-global quality claims
- broad runtime availability claims
- derived stats ownership

## Bounded claim

This eval is designed to support a modest claim like:

under these conditions, one owner-local surface handled one named stressor family in a bounded, reviewable way,
emitted source-owned evidence,
and stayed weaker than the normal path without silently widening action authority.

This eval does **not** support claims such as:
- the whole repo is resilient
- the system is generally antifragile
- the derived stats layer now owns the event meaning
- the operator burden is solved globally

## Trigger boundary

Use this eval when:
- one repo has a named stressor family with source-owned receipts
- degraded continuation or explicit safe stop is part of the observed posture
- you need split-axis reading instead of one prestige score
- the main question is antifragility posture on one bounded family, not general workflow quality

Do not use this eval when:
- no trustworthy source-owned receipt exists yet
- the question is broad project quality rather than one bounded stressor family
- the main need is a repeated-window movement read rather than one bounded family snapshot
- the source of truth is already drifting away from the owner repo

## Inputs

- source-owned stressor receipts
- owner-local run artifacts for the same events
- optional adaptation deltas that cite prior receipts
- optional bounded proof artifacts

The minimum first-wave path is one receipt family plus the linked owner-local artifacts.

## Fixtures and case surface

This bundle is intentionally documentation-first in wave one.

Good case families for it include:
- one degraded hybrid retrieval family
- one routing fallback family
- one runtime containment family

The current example case surface stays small:
- one repo
- one surface
- one named stressor family
- one bounded review window

What this surface excludes:
- giant blended incident timelines
- unbounded log dumps
- dashboard-only summaries with no owner-local evidence

## Scoring or verdict logic

This bundle prefers split-axis categorical readout over one total score.

Primary axes:
- containment
- fallback fidelity
- false-action prevention
- recovery latency
- adaptation gain
- operator burden
- trust calibration

Axis status values:
- `pass`
- `warn`
- `fail`
- `na`

Success means:
- source-owned evidence exists
- degraded continuation stayed weaker than the normal path
- mutation widening stayed blocked or explicitly absent
- the readout keeps separate axes visible

Ambiguous result means:
- evidence is thin
- some axes are visible but repeated-window or adaptation claims are not yet justified

## Baseline or comparison mode

This bundle uses `none`.

Without a baseline, it supports only a modest family-level posture read.
It can say whether one bounded surface looked antifragility-aware on the observed evidence.
It cannot say whether the system improved over time without a repeated-window comparison surface.

## Execution contract

A careful run should:
1. collect the source-owned receipt set
2. link the matching owner-local artifacts
3. note any cited adaptation deltas
4. score the split axes with explicit caution where evidence is thin
5. publish one compact report

If shipping a machine-readable report, use:
- `reports/summary.schema.json` for the bundle-local report contract
- `reports/example-report.json` for the example readout
- `schemas/antifragility_eval_report_v1.json` for the repo-level schema surface

## Outputs

The eval should produce:
- one compact family-level readout
- split axis statuses
- explicit blind spots
- one short verdict summary

Wave-one support artifacts include:
- `notes/origin-need.md`
- `notes/portable-review.md`
- `checks/eval-integrity-check.md`
- `examples/example-report.md`
- `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:
- receipt volume is mistaken for proof quality
- derived stats are treated as the primary evidence source
- one axis score is over-read as a sovereign antifragility score
- adaptation gain is claimed before repeated evidence exists
- the bundle quietly starts judging broad repo health

## Blind spots

This eval does not prove:
- global project quality
- universal resilience
- repeated-window improvement
- unrelated workflow or artifact quality

Likely false-pass risk:
- a repo emits receipts but still degrades unsafely on adjacent surfaces outside the observed family

Likely false-fail risk:
- one family has thin evidence even though broader local posture may be healthier

## Interpretation guidance

Read this bundle as one bounded family snapshot.

- `pass` on one axis is not general resilience
- `warn` may reflect honest thin evidence rather than bad behavior
- `na` on adaptation gain is healthy when no repeated-window evidence exists yet
- the bundle is strongest when it stays downstream from owner-local receipts instead of replacing them

Do not treat a positive result as:
- proof that the whole repo is resilient
- permission for derived stats or eval layers to take source ownership
- justification for automatic recovery or mutation widening
- repeated-window improvement evidence when only one bounded family snapshot was reviewed

## Verification

Verify the bundle by confirming that:
- the report example validates against the schema
- the example keeps split axes visible
- the bundle wording stays downstream from source-owned receipts
- blind spots remain explicit and bounded

## Technique traceability

- `AOA-T-0097` from `8Dionysus/aoa-techniques` at `techniques/system-recovery/degrade-reground-recover/TECHNIQUE.md`
- `AOA-T-0098` from `8Dionysus/aoa-techniques` at `techniques/validation-patterns/receipt-first-failure-analysis/TECHNIQUE.md`

## Skill traceability

No direct skill dependency in wave one.

## Adaptation points

Projects may vary:
- receipt schema details
- which stressor families exist
- which owner-local artifacts are authoritative
- whether later repeated-window proof is available

What should stay invariant:
- source-owned evidence first
- split-axis readout
- no sovereign antifragility score
- no ownership drift away from the owner repo
