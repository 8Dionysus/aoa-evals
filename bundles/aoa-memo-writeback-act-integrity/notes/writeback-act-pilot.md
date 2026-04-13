# Writeback Act Pilot

This bundle is the first narrow downstream pilot for the reviewed-closeout
writeback gap that landed in
`docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`.

It treats the writeback act as supportable only when the proof flow preserves,
at minimum:

- a visible runtime closure boundary
- a reviewed source anchor for adoption
- an adopted memo object with provenance and recall posture
- a receipt-facing publication surface that keeps the act inspectable later

This pilot intentionally does not absorb contradiction handling,
reviewed-candidate promotion, future scar readiness, retention readiness,
live-ledger claims, permission leakage, or hallucinated merge checks.

Its current materialized draft proof flow runs through
`fixtures/memo-writeback-act-guardrail-v1/README.md`,
`bundles/aoa-memo-writeback-act-integrity/fixtures/contract.json`,
`bundles/aoa-memo-writeback-act-integrity/runners/contract.json`, and the
schema-backed companion report in
`bundles/aoa-memo-writeback-act-integrity/reports/example-report.json`.

Selected runtime traces may travel as evidence sidecars.
They do not replace the source-owned memo writeback boundary or the reviewed
source anchors that keep the act honest.
