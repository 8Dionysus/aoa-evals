# Proof Surface Contract

This note records the machine-readable proof surface for
`aoa-memo-contradiction-integrity`.

The draft bundle remains narrow:

- it is about lifecycle-aware contradiction visibility on memo object recall
- it is not contradiction resolution
- it is not permission inference from memo fields
- it is not canon-promotion review
- it is not merge-hallucination review

The materialized proof flow keeps these surfaces explicit:

- shared case-family pressure in
  `fixtures/memo-contradiction-guardrail-v1/README.md`
- bounded local replacement rules in `fixtures/contract.json`
- reportable runner inputs in `runners/contract.json`
- schema-backed contradiction readout in `reports/summary.schema.json`
- a concrete companion example in `reports/example-report.json`

The machine-readable surface should preserve:

- lifecycle visibility across preferred, historical, and withdrawn posture
- honest `current_recall` posture when contradiction remains open
- explicit contradiction and replacement linkage
- audit or provenance walkback when the contradiction needs trace-back
