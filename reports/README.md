# Shared Reports

This directory stores top-level public report artifacts that are shared across more than one bundle.

Bundle-local report contracts should live under:
- `bundles/<name>/reports/summary.schema.json`
- `bundles/<name>/reports/example-report.json`

Real bundle-local run artifacts should also stay under the owning bundle, using
`bundles/<name>/reports/*.report.json`, and must validate against that bundle's
local report schema.

Top-level report artifacts here should only capture cross-bundle readouts such as:
- paired proof flows
- shared readout dossiers
- reusable public comparison guidance

Shared machine-readable publication receipts that span more than one bundle do
not live under `reports/`.
Keep those shared receipt seams in `schemas/` and `examples/` so bundle-local
report artifacts remain the stronger proof contract.

Current shared receipt surfaces:
- canonical shared envelope: `repo:aoa-stats/schemas/stats-event-envelope.schema.json`
- `schemas/stats-event-envelope.schema.json`
- `schemas/eval-result-receipt.schema.json`
- `examples/eval_result_receipt.example.json`

The local `schemas/stats-event-envelope.schema.json` file is a mirror of the
canonical `aoa-stats` envelope so `aoa-evals` can validate its own example and
publication seam without claiming ownership of the whole shared event family.

Current shared dossiers:
- `artifact-process-paired-proof-flow-v1.md` for artifact/process bridge reading
- `artifact-process-paired-proof-flow-v2.md` for second-family artifact/process bridge reading
- `reports/proof-loop-local-route-smoke-v1.md` for the first bounded
  proof-loop route-smoke report
- `bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
  for the first schema-backed bundle-local proof-loop report
- `reports/eval-result-receipt-intake-dry-review-v1.json` for the first
  receipt-intake dry review; it contains a payload preview only, with
  `receipt_status` kept `not_published` and no live receipt append
- `reports/proof-release-readiness-audit-v1.json` for local proof-release
  readiness review of the accumulated strategic refactor diff; it is not a tag,
  GitHub Release, GitHub `Repo Validation`, PR approval, or goal completion
- `reports/strategic-closeout-audit-v1.json` for requirement-by-requirement
  strategic closeout review of the local refactor; it states handoff readiness
  while keeping goal completion, PR, GitHub `Repo Validation`, tag, GitHub
  Release, live receipt publication, runtime acceptance, and sibling mutation
  open
- `reports/release-prep-pr-handoff-v1.json` for the pre-PR owner landing
  handoff snapshot: it prepares candidate branch, commit, PR title/body, changed
  surface groups, validation, and landing steps while recording that, at
  snapshot time, branch creation, commit, push, PR, GitHub `Repo Validation`,
  merge, tag, GitHub Release, live receipt publication, runtime acceptance,
  sibling mutation, and goal completion were still open; once a branch or PR
  exists, current git and GitHub state supersedes the snapshot for live status
- `same-task-baseline-proof-flow-v1.md` for frozen same-task baseline reading
- `repeated-window-proof-flow-v1.md` for repeated-window longitudinal reading
- `repeated-window-proof-flow-v2.md` for cautious repeated-window transition reading

Current generated report reader:
- `generated/eval_report_index.min.json` routes to real bundle-local
  `*.report.json` artifacts; it is not receipt authority and does not replace
  the source reports.

Shared dossier naming discipline:
- keep the primary bundle-local dossier path in `paired_readout_path`
- record any additional shared dossiers in `additional_paired_readout_paths`
- keep top-level dossiers weaker than bundle-local interpretation guidance
