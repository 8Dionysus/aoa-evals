# Publication Receipts / Part Index

## Role

`PARTS.md` names the living sub-operations inside the publication receipts
mechanic.

The mechanic owns the route from reviewed bounded report to optional
publication receipt. The parts keep each authority class visible so dry review,
payload schema, stats envelope mirror, publisher, and owner-local log pressure
routes to the surface that can carry it.

## Parts

| Part | Owns | Emits | Route pressure |
| --- | --- | --- | --- |
| `receipt-payload` | eval-result receipt guide, payload schema, and public example | schema-valid `eval_result_receipt` payload shape | proof authority routes back to the bundle-local report and source bundle |
| `stats-envelope-mirror` | local mirror of the canonical `aoa-stats` event envelope | local validation support for eval receipt envelopes | canonical event vocabulary routes to `aoa-stats` |
| `live-publisher` | owner-local append tool for already valid receipts | append-only JSONL writes when explicitly invoked | dry-review publication and proof promotion route through review and receipt boundaries |
| `intake-dry-review` | non-publishing report-to-receipt derivation artifact | payload preview with `not_published` posture | receipt publication, envelope creation, live-log append, and runtime acceptance route to their owning parts |

## Boundary

`.aoa/live_receipts/` remains the owner-local live receipt log path. It is
routed by this mechanic but is not moved into `parts/` because live receipt
memory is a local append surface, not authored package source.

Bundle-local reports and source proof bundles remain stronger than every part
listed here.

## Part Contract

Inputs are reviewed bounded report facts, receipt payload fields, stats envelope
mirror constraints, and explicit live-publish intent when publication is
actually requested.

Outputs are schema-valid payload shapes, dry-review previews, optional
append-only live receipt writes, and downstream-readable receipt envelopes.

Owner split stays explicit: bundles and reports own verdict meaning;
`aoa-stats` owns canonical stats event vocabulary; this mechanic owns only the
eval-result receipt sidecar route.

Stop-lines route dry-review publication pressure, receipt proof-authority
pressure, and local envelope ownership pressure back to their owners.

Validation routes through [AGENTS](AGENTS.md#validation), including repo,
semantic AGENTS, and receipt-specific test lanes.
