# Memo Guardrail Pilot

This bundle is the first narrow downstream pilot for
`repo:aoa-memo/examples/memory_eval_guardrail_pack.example.json`.

It treats memo recall as supportable only when the consumer preserves, at
minimum:

- a smallest-surface-first precision posture
- visible provenance-thread or stronger-source posture
- visible lifecycle and staleness posture

This pilot intentionally does not absorb contradiction handling, permission
leakage, over-promotion, or hallucinated merge checks.

Selected runtime or routing traces may travel as evidence sidecars.
They do not replace the source-owned memo guardrail pack.
