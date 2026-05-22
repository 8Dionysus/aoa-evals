# Reports Route

`reports/` is the compatibility route card for former top-level shared report
artifacts.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root report path routing |
| entry | open when an old root report path appears or a report artifact needs a stronger owner |
| input | report artifact, dossier, receipt preview, generated report reader ref, or old root report path |
| output | owning bundle report, mechanic report family, receipt dry review, or generated reader route |
| owner | `reports/AGENTS.md` for route law; owning bundle or mechanic part for report meaning |
| next route | bundle-local `reports/`, `mechanics/*/parts/*/reports/`, or `generated/eval_report_index.min.json` |
| validation | `reports/AGENTS.md` and the owning route card |

Active root reports payloads route to the owning bundle or mechanic part.

Use [AGENTS.md](AGENTS.md) for report safety, proof-strength, and route-card
rules. This README is the route map.

Current top-level shared dossiers:

- none

## Report Route Families

| Report family | Owning surface | Route note |
| --- | --- | --- |
| Bundle-local reports | `evals/<family>/<eval>/reports/` | Source report schemas, examples, and `*.report.json` artifacts stay with the bundle whose claim they support. |
| Proof-loop reports | `mechanics/proof-loop/parts/route-smoke/reports/` and bundle-local proof-loop reports | Route-smoke report artifacts stay mechanic-owned; schema-backed bundle-local reports stay under their eval bundle. |
| Comparison-spine reports | `mechanics/comparison-spine/parts/*/reports/` | Shared dossiers are comparison-spine state/readout artifacts and stay weaker than bundle-local interpretation. |
| Publication receipt reports | `mechanics/publication-receipts/parts/*/reports/` | Receipt previews and dry reviews stay below reviewed report meaning; `receipt-intake` dry review keeps `receipt_status` as `not_published`. |
| Release-support reports | `mechanics/release-support/parts/*/reports/` | Readiness, closeout, and PR handoff reports support landing posture without strengthening eval claims. |
| Generated report reader | `generated/eval_report_index.min.json` | Derived report lookup points back to source report artifacts and owning proof surfaces. |

Current report anchors:

- route-smoke report:
  `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
- first schema-backed bundle-local proof-loop report:
  `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
- receipt-intake dry review:
  `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
