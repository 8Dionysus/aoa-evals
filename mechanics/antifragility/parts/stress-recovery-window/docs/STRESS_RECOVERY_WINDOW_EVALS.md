# Stress Recovery Window Evals

## Purpose

This part supports a repeated-window proof surface for explicit stress handling
across owner repos and adjacent AoA layers.

It answers a narrow question:

**Given a named stressor family and a bounded window, did handoffs, playbook gates, route posture, and KAG regrounding combine into a healthier handling pattern?**

## Why This Belongs In `aoa-evals`

`aoa-evals` already owns bounded, reproducible, regression-aware proof surfaces.
This bundle applies that posture to stress handling that spans multiple
explicit objects:

- source-owned stressor receipts
- agent stress handoff envelopes
- playbook stress lanes and re-entry gates
- projection-health receipts and regrounding tickets
- derived route hints
- optional memo context as tertiary evidence

This remains a proof surface. Workflow ownership stays with the owner route
that produced the stress handling evidence.

## Input Discipline

Preferred evidence order:

1. source-owned receipts and owner-local artifacts
2. explicit handoff, lane, gate, projection-health, and regrounding objects
3. route hints that cite those owner or derived inputs
4. memo objects as reviewed context after owner evidence

The bundle should suppress or narrow its verdict when owner evidence is too thin.

## Report Axes

The report contract uses split axes that match the objects in play:

- `handoff_fidelity`
- `route_discipline`
- `reentry_quality`
- `regrounding_effectiveness`
- `evidence_continuity`
- `false_promotion_prevention`
- `operator_burden`
- `trust_calibration`

The bundle may add repo-local axes later; split-axis evidence remains visible.

## Scope Discipline

A healthy report for this bundle stays bounded by:

- one named stressor family
- one explicit window
- one owner surface or tightly related surface family
- a clear list of repos actually involved

Federation-wide vibe-check pressure routes back to named owner evidence,
explicit windows, and the bounded eval question.

## Output Posture

The active source bundle publishes:

- one bundle at `evals/comparison/longitudinal-window/aoa-stress-recovery-window/`
- one schema-backed report
- one small input manifest example
- one narrow example report
- repo-native catalog discoverability alongside the existing starter eval families

This surface complements `aoa-antifragility-posture`.
The first-wave family read remains the posture-review route.

## Guardrails

| Pressure | Route |
| --- | --- |
| route hints outranking owner receipts | owner receipt route before route-hint interpretation |
| memo pattern objects standing in for current-run truth | owner evidence route before memo context |
| regrounding success from ticket existence alone | regrounding evidence route with outcome conditions |
| KAG quarantine exit as healthy re-entry | KAG condition route plus explicit re-entry evidence |
| single-number movement pressure | split-axis stress-recovery readout route |
