# Reviewed Candidate Adoption Pilot

This bundle is the first narrow downstream pilot for the reviewed-candidate
memo gap that remained after the base writeback-act lane landed.

It treats reviewed-candidate adoption as supportable only when the proof flow
preserves, at minimum:

- an explicit runtime writeback mapping for claim, pattern, or bridge
  candidates
- a reviewed anchor that keeps the adoption step inspectable
- an adopted memo object on the object-facing recall family
- a live receipt that points back to the adopted object and reviewed anchor
- recall visibility that preserves candidate posture instead of smoothing it
  into settled truth

This pilot intentionally does not absorb contradiction handling,
confirmed-decision writeback, promotion readiness, future scar readiness,
retention readiness, live-ledger claims, permission leakage, or graph-lift
completion checks.

Its current materialized draft proof flow runs through
`fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`,
`bundles/aoa-memo-reviewed-candidate-adoption-integrity/fixtures/contract.json`,
`bundles/aoa-memo-reviewed-candidate-adoption-integrity/runners/contract.json`,
and the schema-backed companion reports under `reports/`.

The current draft is allowed to fail honestly.
The point of the pilot is to expose the remaining gap without rewriting the
already-landed recall, contradiction, or base writeback-act lanes.
