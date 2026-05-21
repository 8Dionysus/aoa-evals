# Stress Recovery Window Evals

## Purpose

Wave 4 adds a repeated-window proof surface for explicit stress handling across owner repos and adjacent AoA layers.

The point is not to prove that the whole federation is healthy.
The point is to answer a narrower question:

**Given a named stressor family and a bounded window, did handoffs, playbook gates, route posture, and KAG regrounding combine into a healthier handling pattern?**

## Why This Belongs In `aoa-evals`

`aoa-evals` already owns bounded, reproducible, regression-aware proof surfaces.
Wave 4 extends that posture to stress handling that spans multiple explicit objects:

- source-owned stressor receipts
- agent stress handoff envelopes
- playbook stress lanes and re-entry gates
- projection-health receipts and regrounding tickets
- derived route hints
- optional memo context as tertiary evidence

This remains proof, not workflow ownership.

## Input Discipline

Preferred evidence order:

1. source-owned receipts and owner-local artifacts
2. wave-3 handoff, lane, gate, projection-health, and regrounding objects
3. route hints that cite those owner or derived inputs
4. memo objects only as reviewed context, never as primary evidence

The bundle should suppress or narrow its verdict when owner evidence is too thin.

## Suggested Axes

Wave 4 uses split axes that match the objects now in play:

- `handoff_fidelity`
- `route_discipline`
- `reentry_quality`
- `regrounding_effectiveness`
- `evidence_continuity`
- `false_promotion_prevention`
- `operator_burden`
- `trust_calibration`

The bundle may add repo-local axes later, but should not hide these behind one total score.

## Scope Discipline

A healthy report for this bundle stays bounded by:

- one named stressor family
- one explicit window
- one owner surface or tightly related surface family
- a clear list of repos actually involved

Do not turn repeated-window evaluation into a floating federation-wide vibe check.

## Output Posture

The wave-4 landing publishes:

- one bundle at `bundles/aoa-stress-recovery-window/`
- one schema-backed report
- one small input manifest example
- one narrow example report
- repo-native catalog discoverability alongside the existing starter eval families

This surface complements `aoa-antifragility-posture`.
It does not replace the first-wave family read.

## Guardrails

- do not let route hints become stronger evidence than the owner receipts they cite
- do not let memo pattern objects stand in for current-run truth
- do not score regrounding success if the evidence only proves that a ticket exists
- do not treat KAG quarantine exit as healthy re-entry without explicit conditions
- do not collapse all movement into a single number
