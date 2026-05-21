# Reports Route

This is a compatibility route card for former top-level shared report artifacts.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root report path routing |
| entry | open when an old root report path appears or a report artifact needs a stronger owner |
| input | report artifact, dossier, receipt preview, generated report reader reference, or old root report path |
| output | bundle-local report, proof-loop report, comparison-spine report, release-support report, or publication-receipt part |
| owner | `reports/AGENTS.md` for route law; owning bundle or mechanic part for report meaning |
| next route | bundle-local `reports/`, `mechanics/*/parts/*/reports/`, or `generated/eval_report_index.min.json` |
| validation | `reports/AGENTS.md` and the owning route card |

Active root reports payloads route to the owning bundle or mechanic part.

Historically this directory stored top-level public report artifacts that were
shared across more than one bundle. Active reports now need a narrower owner:
bundle-local reports stay with their bundle, and mechanic-owned reports stay
with the mechanic part that owns the operation.

Bundle-local report contracts live under:
- `evals/<family>/<eval>/reports/summary.schema.json`
- `evals/<family>/<eval>/reports/example-report.json`

Real bundle-local run artifacts also stay under the owning bundle as
`evals/<family>/<eval>/reports/*.report.json`.

Use [AGENTS.md](AGENTS.md) for report safety, proof-strength, and route-card
rules. This README is the route map.

Shared machine-readable publication receipts that span more than one bundle
route through publication-receipts parts.
Keep those shared receipt seams under
`mechanics/publication-receipts/parts/` so bundle-local report artifacts remain
the stronger proof contract.

Current publication receipt surfaces:
- canonical shared envelope: `repo:aoa-stats/schemas/stats-event-envelope.schema.json`
- `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`

The local `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json` file is a mirror of the
canonical `aoa-stats` envelope so `aoa-evals` can validate its own example and
publication seam without claiming ownership of the whole shared event family.
The non-publishing receipt-intake dry review now lives with the same mechanic at
`mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`.
It contains a payload preview only, keeps `receipt_status` as `not_published`,
and performs no live receipt append.

Current top-level shared dossiers:

- none

Proof-loop reports no longer live in this root report district. They are
mechanic-owned route artifacts or bundle-local reports:

- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
  for the first bounded proof-loop route-smoke report
- `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
  for the first schema-backed bundle-local proof-loop report

Comparison-spine shared dossiers no longer live in this root report district.
They are mechanic-owned state/readout artifacts:

- `mechanics/comparison-spine/parts/spine-overview/reports/comparison-spine-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md`

Release-support reports no longer live in this root report district. They are
mechanic-owned state artifacts:

- `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`
- `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`

Current generated report reader:
- `generated/eval_report_index.min.json` routes to real bundle-local
  `*.report.json` artifacts; receipt authority and source report meaning stay
  with their owning surfaces.
