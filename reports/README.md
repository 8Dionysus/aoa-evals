# Shared Reports Route Card

This is a compatibility route card for former top-level shared report artifacts.
No active root reports payload should live here.

Historically this directory stored top-level public report artifacts that were
shared across more than one bundle. Active reports now need a narrower owner:
bundle-local reports stay with their bundle, and mechanic-owned reports stay
with the mechanic part that owns the operation.

Bundle-local report contracts should live under:
- `bundles/<name>/reports/summary.schema.json`
- `bundles/<name>/reports/example-report.json`

Real bundle-local run artifacts should also stay under the owning bundle, using
`bundles/<name>/reports/*.report.json`, and must validate against that bundle's
local report schema.

Top-level report artifacts may return here only through an explicit topology
decision and validator allowlist update. Until then, this root directory remains
route-card-only.

Shared machine-readable publication receipts that span more than one bundle do
not live under `reports/`.
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
- `bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
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
  `*.report.json` artifacts; it is not receipt authority and does not replace
  the source reports.

Shared dossier naming discipline for comparison-spine paired readouts:
- keep the primary bundle-local dossier path in `paired_readout_path`
- record any additional shared dossiers in `additional_paired_readout_paths`
- keep top-level dossiers weaker than bundle-local interpretation guidance
