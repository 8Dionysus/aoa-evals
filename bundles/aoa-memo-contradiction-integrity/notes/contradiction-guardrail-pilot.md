# Contradiction Guardrail Pilot

This bundle is the second narrow downstream pilot for
`repo:aoa-memo/examples/memory_eval_guardrail_pack.example.json`.

It treats memo contradiction handling as supportable only when the consumer
preserves, at minimum:

- visible lifecycle `review_state` and `current_recall` posture
- explicit separation between superseded, withdrawn, and still-open tension
- visible contradiction refs, replacement refs, or audit walkback when the
  case needs them

This pilot intentionally does not absorb recall precision, permission leakage,
over-promotion, or hallucinated merge checks.

Its current materialized draft proof flow runs through
`fixtures/memo-contradiction-guardrail-v1/README.md`,
`bundles/aoa-memo-contradiction-integrity/fixtures/contract.json`,
`bundles/aoa-memo-contradiction-integrity/runners/contract.json`, and the
schema-backed companion report in
`bundles/aoa-memo-contradiction-integrity/reports/example-report.json`.

Selected audit trails or provenance-thread timelines may travel as evidence
sidecars. They do not replace the source-owned memo guardrail pack.
