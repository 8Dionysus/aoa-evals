# Shared Reports

This directory stores top-level public report artifacts that are shared across more than one bundle.

Bundle-local report contracts should live under:
- `bundles/<name>/reports/summary.schema.json`
- `bundles/<name>/reports/example-report.json`

Top-level report artifacts here should only capture cross-bundle readouts such as:
- paired proof flows
- shared readout dossiers
- reusable public comparison guidance

Current shared dossiers:
- `artifact-process-paired-proof-flow-v1.md` for artifact/process bridge reading
- `same-task-baseline-proof-flow-v1.md` for frozen same-task baseline reading
- `repeated-window-proof-flow-v1.md` for repeated-window longitudinal reading
