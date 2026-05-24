# Publication Receipts / Parts Route

`mechanics/publication-receipts/parts/` is the lower index for publication
receipt sub-operations. Use it after the parent Publication Receipts route has
selected a receipt authority class and the next agent needs the exact part,
payload home, owner route, tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for eval-result receipt payload, mirror, publishing, and dry-review parts |
| input | reviewed bounded report fact, receipt payload field, stats envelope constraint, live-publish intent, dry-review derivation, or owner-local log pressure |
| output | payload schema route, stats-envelope mirror route, live-publisher route, dry-review preview route, optional live receipt write, or downstream envelope handoff |
| owner | bundles and reports own verdict meaning; `aoa-stats` owns canonical stats vocabulary; publication-receipts owns eval-result receipt sidecar routing |
| next route | `mechanics/publication-receipts/PARTS.md`, selected part README, reviewed report, source bundle, stats owner route, and parent validation lane |
| tools | receipt schema validation, live publisher, intake dry-review checks, repo validator, and focused tests through `mechanics/publication-receipts/AGENTS.md#validation` |
| validation | `mechanics/publication-receipts/parts/AGENTS.md#validation` and `mechanics/publication-receipts/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `receipt-payload/` | bounded `eval_result_receipt` guide, schema, and public example | `receipt-payload/README.md` |
| `stats-envelope-mirror/` | local mirror of the canonical `aoa-stats` event envelope | `stats-envelope-mirror/README.md` |
| `live-publisher/` | append tool for already reviewed and schema-valid receipt envelopes | `live-publisher/README.md` |
| `intake-dry-review/` | non-publishing report-to-receipt derivation artifact | `intake-dry-review/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| proof authority or verdict meaning | reviewed report and source bundle route |
| canonical stats event vocabulary | `aoa-stats` owner route |
| live receipt append | `live-publisher/README.md` plus explicit publish intent |
| dry-review publication pressure | `intake-dry-review/README.md` plus receipt boundary review |
| `.aoa/live_receipts/` local log pressure | owner-local live receipt log route |
| runtime acceptance or bundle promotion | owning proof or runtime route before receipt publication |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| receipt payload contract changes | guide, schema, and example shape move together | `receipt-payload/README.md` |
| stats envelope mirror changes | local mirror stays aligned with `aoa-stats` vocabulary | `stats-envelope-mirror/README.md` |
| explicit live publish path changes | already valid receipt envelope can be appended by owner-local tool | `live-publisher/README.md` |
| report-to-receipt derivation needs review without publication | preview artifact carries non-publishing posture | `intake-dry-review/README.md` |
| new receipt sub-operation pressure | distinct authority class, payload home, owner split, and validation lane exist | parent `PARTS.md` update plus decision review |
