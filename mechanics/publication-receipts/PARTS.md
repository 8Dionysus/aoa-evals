# Publication Receipts Parts

## Role

`PARTS.md` names the living sub-operations inside the publication receipts
mechanic.

The mechanic owns the route from reviewed bounded report to optional
publication receipt. The parts keep each authority class visible so a dry
review, payload schema, stats envelope mirror, publisher, and owner-local log
do not collapse into one false proof surface.

## Parts

| Part | Owns | Emits | Must not claim |
| --- | --- | --- | --- |
| `receipt-payload` | eval-result receipt guide, payload schema, and public example | schema-valid `eval_result_receipt` payload shape | a receipt is proof authority |
| `stats-envelope-mirror` | local mirror of the canonical `aoa-stats` event envelope | local validation support for eval receipt envelopes | ownership of `aoa-stats` event vocabulary |
| `live-publisher` | owner-local append tool for already valid receipts | append-only JSONL writes when explicitly invoked | publication from dry review or proof promotion |
| `intake-dry-review` | non-publishing report-to-receipt derivation artifact | payload preview with `not_published` posture | receipt publication, envelope creation, live-log append, or runtime acceptance |

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

Stop-lines forbid dry review from implying publication, receipt presence from
implying proof authority, or local envelope mirrors from owning `aoa-stats`.

Validation is `python scripts/validate_repo.py`,
`python scripts/validate_semantic_agents.py`, and receipt-specific tests.
