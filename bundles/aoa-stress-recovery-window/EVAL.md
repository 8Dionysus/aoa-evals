---
name: aoa-stress-recovery-window
category: longitudinal
status: draft
summary: Checks whether a named stressor family shows healthier handling across an ordered bounded window without letting proof, stats, routing, or memo outrank owner evidence.
object_under_evaluation: ordered stress recovery posture on one named owner surface and adjacent evidence family
claim_type: longitudinal
baseline_mode: longitudinal-window
report_format: comparative-summary
comparison_surface:
  shared_family_path: fixtures/stress-recovery-window-bounded-v1/README.md
  paired_readout_path: reports/stress-recovery-window-proof-flow-v1.md
  integrity_sidecar: aoa-eval-integrity-check
  selection_question: Do you need ordered repeated-window proof for one named stress recovery family?
  anchor_surface: aoa-antifragility-posture
  window_family_label: stress-recovery-window-bounded-v1 bounded stress recovery sequence
technique_dependencies:
  - AOA-T-0097
  - AOA-T-0098
skill_dependencies: []
---

# aoa-stress-recovery-window

## Intent

Use this eval to check whether ordered windows around one named stressor family show healthier handling without upgrading that movement into federation-wide resilience.

This starter bundle is a `diagnostic` longitudinal eval.
It is downstream of owner receipts, wave-3 handoff and regrounding objects, and bounded eval evidence.
Its goal is to test one modest claim:

across ordered comparable windows on one named stress recovery family,
the system can show healthier containment, route discipline, re-entry posture, and evidence continuity
without letting proof, stats, routing, or memo seize ownership of the event meaning.

## Object under evaluation

This eval checks ordered stress recovery posture on one named owner surface and adjacent evidence family.

Primary surfaces under evaluation:

- source-owned stressor receipts for one family
- stress handoff envelopes
- playbook stress lanes and re-entry gates
- projection-health receipts and regrounding tickets
- bounded route hints and memo context that stay weaker than owner evidence

Nearby surfaces intentionally excluded:

- repo-global health or uptime claims
- broad resilience claims across unrelated stressor families
- route hints treated as stronger than the owner receipts they cite
- memo context treated as present-tense health proof

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
ordered windows on one named stressor family show healthier recovery posture
because the system stayed evidence-linked, bounded, and honest about re-entry,
without turning downstream derived layers into stronger truth than the owner evidence.

This eval does **not** support claims such as:

- the whole federation is healthy
- all future re-entry attempts will be safe
- one route hint or one memo object proves present-tense recovery
- a repeated stress window replaces first-wave owner-local antifragility reading

## Trigger boundary

Use this eval when:

- you have ordered windows on the same named stressor family
- the main question is repeated-window recovery posture rather than one-run family reading
- owner receipts and adjacent wave-3 objects are explicit enough to follow
- you need split-axis proof rather than a prestige scalar

Do not use this eval when:

- no trustworthy owner receipt family exists yet
- the windows are too inconsistent to compare honestly
- the main need is first-wave bounded antifragility reading rather than repeated-window movement
- the only signals available are route hints or memo context without stronger evidence

## Inputs

- ordered named windows
- one bounded owner surface or tightly related surface family
- one public input manifest for the chosen window family
- source-owned stressor receipts and owner-local artifacts
- wave-3 handoff, playbook, and KAG objects for the same family when available
- optional route hints and memo context that remain secondary

Because `baseline_mode` is `longitudinal-window`, this bundle also requires:

- ordered windows
- one public report or summary artifact per window family read
- context notes that affect comparability

## Fixtures and case surface

This bundle stays report-led and bounded.

A strong v1 window family includes:

- one named owner surface
- one named stressor family
- repeated windows that keep the same owner and adjacent evidence family in play
- a visible recovery lesson about containment, route posture, re-entry, or regrounding

The current exemplar keeps the surface narrow:

- owner repo: `ATM10-Agent`
- owner surface: `hybrid-query`
- stressor family: `hybrid-query-kag-unhealthy`
- adjacent layers: `aoa-agents`, `aoa-playbooks`, `aoa-kag`, `aoa-routing`, and `aoa-memo`

This surface excludes:

- floating incident timelines with no named window contract
- health claims that are not anchored to owner receipts
- route-only or memo-only evidence chains

The current shared family is `fixtures/stress-recovery-window-bounded-v1/README.md`.

## Scoring or verdict logic

This bundle prefers split-axis categorical readout plus one bounded bundle posture.

Primary axes:

- `handoff_fidelity`
- `route_discipline`
- `reentry_quality`
- `regrounding_effectiveness`
- `evidence_continuity`
- `false_promotion_prevention`
- `operator_burden`
- `trust_calibration`

Axis status values:

- `pass`
- `warn`
- `fail`
- `na`

The evidence hierarchy should stay explicit:

1. owner receipts and owner-local artifacts
2. wave-3 handoff, lane, gate, projection-health, and regrounding objects
3. bounded eval report interpretation
4. derived stats summary and route hints as secondary shaping context
5. memo context only as reviewed recall

Success means the windows support healthier bounded recovery posture without false promotion.
Regression means later windows widen, hide uncertainty, or break evidence continuity.
Ambiguous results should remain `mixed` or `suppressed`.

## Baseline or comparison mode

This starter bundle uses `longitudinal-window`.

Its machine-readable comparison surface is anchored in `aoa-antifragility-posture`,
uses the shared family `fixtures/stress-recovery-window-bounded-v1/README.md`,
publishes through `reports/stress-recovery-window-proof-flow-v1.md`,
and keeps `aoa-eval-integrity-check` as the integrity sidecar whenever public stress wording or maturity posture changes materially.

In this surface:

- the windows must be ordered and named
- the same bounded stress family must stay visible across the window
- the same owner surface or tightly related surface family must remain in scope
- style-only movement should not look like recovery growth
- missing owner evidence should force cautious or suppressed readout

If the sequence loses comparability or owner evidence thins out,
prefer `mixed` or `suppressed` over a cleaner story.

## Execution contract

A careful run should:

1. define the ordered window and the named stressor family
2. collect source-owned owner receipts and owner-local artifacts
3. gather the relevant wave-3 handoff, playbook, and KAG objects
4. interpret route hints and memo context only after the stronger evidence is visible
5. publish one comparative-summary artifact with a bounded longitudinal posture

When shipping a machine-readable report, validate it against:

- `reports/summary.schema.json`

This bundle also ships:

- the bundle-local fixture contract at `fixtures/contract.json`
- the bundle-local runner contract at `runners/contract.json`
- the shared window family note at `fixtures/stress-recovery-window-bounded-v1/README.md`
- the paired readout at `reports/stress-recovery-window-proof-flow-v1.md`

## Outputs

The eval should produce:

- one bundle-level longitudinal posture
- split-axis status and rationale
- explicit blind spots and evidence gaps
- an optional machine-readable report at `reports/example-report.json`

For this starter bundle, the public support artifacts are:

- `notes/origin-need.md`
- `notes/window-contract.md`
- `notes/baseline-readiness.md`
- `checks/eval-integrity-check.md`
- `examples/example-report.md`

## Failure modes

Main ways this eval can fail as an instrument:

- route hints outrank owner evidence
- memo context quietly acts like present-tense proof
- later windows look healthier only because the reporting became cleaner
- quarantine exit or ticket creation is over-read as healthy re-entry
- thin owner evidence is glossed over instead of being suppressed

## Blind spots

This eval does not prove:

- long-horizon health across unrelated stressor families
- repo-global readiness for mutation
- that future KAG projection families will follow the same re-entry discipline
- that operator burden is solved outside the named window

## Interpretation guidance

Treat this bundle as repeated-window proof for one bounded stress family, not as a total resilience measure.

Use it together with `aoa-antifragility-posture` when you need both:

- one owner-local family read
- one ordered repeated-window read for the same family

- healthier route posture or memo recall is not the same as owner-surface health
- suppressed or mixed outcomes may be the most honest longitudinal result when owner evidence stays thin
- a healthier window still remains weaker than the gate or quarantine objects it cites

Do not treat a positive result as:
- proof that the whole federation is resilient
- permission to bypass owner receipts, playbook gates, or KAG quarantine posture
- justification for direct mutation widening
- present-tense health proof just because route, stats, and memo layers now align

## Verification

- confirm the named stress family and ordered windows are explicit
- confirm the evidence chain stays owner-first
- confirm route and memo layers stay weaker than owner evidence
- confirm the report stays longitudinal rather than incident-global
- confirm the output does not imply stronger conclusions than the bundle supports

## Technique traceability

- `AOA-T-0097` from `aoa-techniques`: degrade, reground, recover
- `AOA-T-0098` from `aoa-techniques`: receipt-first failure analysis

## Skill traceability

This bundle does not directly depend on a specific runtime skill surface.

## Adaptation points

Project overlays may add:

- local repeated-window fixture families
- local runner guidance
- local source-owned stressor families
- stricter suppression rules for thin evidence
