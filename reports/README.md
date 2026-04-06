# Shared Reports

This directory stores top-level public report artifacts that are shared across more than one bundle.

Bundle-local report contracts should live under:
- `bundles/<name>/reports/summary.schema.json`
- `bundles/<name>/reports/example-report.json`

Top-level report artifacts here should only capture cross-bundle readouts such as:
- paired proof flows
- shared readout dossiers
- reusable public comparison guidance

Shared machine-readable publication receipts that span more than one bundle do
not live under `reports/`.
Keep those shared receipt seams in `schemas/` and `examples/` so bundle-local
report artifacts remain the stronger proof contract.

Current shared receipt surfaces:
- `schemas/stats-event-envelope.schema.json`
- `schemas/eval-result-receipt.schema.json`
- `examples/eval_result_receipt.example.json`

Current shared dossiers:
- `artifact-process-paired-proof-flow-v1.md` for artifact/process bridge reading
- `artifact-process-paired-proof-flow-v2.md` for second-family artifact/process bridge reading
- `same-task-baseline-proof-flow-v1.md` for frozen same-task baseline reading
- `repeated-window-proof-flow-v1.md` for repeated-window longitudinal reading
- `repeated-window-proof-flow-v2.md` for cautious repeated-window transition reading

Shared dossier naming discipline:
- keep the primary bundle-local dossier path in `paired_readout_path`
- record any additional shared dossiers in `additional_paired_readout_paths`
- keep top-level dossiers weaker than bundle-local interpretation guidance
