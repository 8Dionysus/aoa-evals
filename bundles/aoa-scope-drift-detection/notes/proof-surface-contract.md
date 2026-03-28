# Proof Surface Contract

This note records the machine-readable proof surface for
`aoa-scope-drift-detection`.

The bounded bundle remains narrow:
- it is about requested-scope versus executed-scope alignment
- it is not a composite workflow grade
- it is not a verification-honesty or ambiguity-handling replacement

The materialized proof flow keeps these surfaces explicit:
- shared case-family pressure in `fixtures/scope-drift-bounded-v1/README.md`
- bounded local replacement rules in `fixtures/contract.json`
- reportable runner inputs in `runners/contract.json`
- schema-backed scope-drift readout in `reports/summary.schema.json`
- a concrete companion example in `reports/example-report.json`

The machine-readable surface should preserve:
- requested scope and executed scope as separate review objects
- explicit drift classes for aligned, widening, narrowing, and reshaping
- explicit-versus-silent deviation as a real readout surface
- failure-versus-readout separation on every case
