# Proof Surface Contract

This note records the machine-readable proof surface for
`aoa-witness-trace-integrity`.

The draft bundle remains narrow:
- it is about public witness reviewability on bounded runs
- it is not a runtime-instrumentation completeness claim
- it is not an outcome-quality grade

The materialized proof flow keeps these surfaces explicit:
- shared case-family pressure in `fixtures/witness-trace-v1/README.md`
- bounded local replacement rules in `fixtures/contract.json`
- reportable runner inputs in `runners/contract.json`
- schema-backed witness readout in `reports/summary.schema.json`
- a concrete companion example in `reports/example-report.json`

The machine-readable surface should preserve:
- meaningful-step visibility
- tool visibility where tools materially shaped the run
- explicit `state_delta` notes for external effects
- preserved partial-failure paths
- reviewable redaction posture
- a markdown summary that stays weaker than the trace
