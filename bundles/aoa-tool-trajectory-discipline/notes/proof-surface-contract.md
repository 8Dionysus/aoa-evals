# Proof Surface Contract

This note records the machine-readable proof surface for
`aoa-tool-trajectory-discipline`.

The bounded bundle remains narrow:
- it is about tool-use trajectory on path-sensitive bounded tasks
- it is not the broader outcome-versus-path split bundle
- it is not a composite workflow grade

The materialized proof flow keeps these surfaces explicit:
- shared case-family pressure in `fixtures/tool-trajectory-bounded-v1/README.md`
- bounded local replacement rules in `fixtures/contract.json`
- reportable runner inputs in `runners/contract.json`
- schema-backed trajectory readout in `reports/summary.schema.json`
- a concrete companion example in `reports/example-report.json`

The machine-readable surface should preserve:
- why the path matters before the trajectory is judged
- the trajectory reading itself as a visible review object
- omission-or-churn evidence that stays weaker than overall workflow claims
- failure-versus-readout separation on every case
