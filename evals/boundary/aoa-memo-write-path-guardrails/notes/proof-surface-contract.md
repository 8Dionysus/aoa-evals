# Proof Surface Contract

This note records the machine-readable proof surface for
`aoa-memo-write-path-guardrails`.

The draft bundle remains narrow:

- it is about candidate-to-reviewed-memory write-path guardrails
- it is not recall precision
- it is not contradiction handling
- it is not final source-truth judgment
- it is not role authorization outside memo operation mode
- it is not KAG, RAG, graph, vector, or retrieval correctness
- it is not general memory poisoning resistance

The materialized proof flow keeps these surfaces explicit:

- write-path guardrail doctrine in `aoa-memo`
- bounded local replacement rules in `fixtures/contract.json`
- reportable runner inputs in `runners/contract.json`
- schema-backed write-path readout in `reports/summary.schema.json`
- a concrete companion example in `reports/example-report.json`
- a current pilot readout in
  `reports/current-write-path-guardrail-pilot.report.json`
- neighboring memo evals for recall, contradiction, writeback act, and
  reviewed-candidate adoption

The machine-readable surface should preserve:

- source trust classification
- ingestion risk marking
- derivation lineage
- action-safety separation
- durable landing gate behavior
- MCP and local memo port authority split
