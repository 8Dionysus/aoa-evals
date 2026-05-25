# 0013 Publication Receipts Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/publication-receipts/`

## Index Metadata

- Surface classes: mechanic package, report/release/receipt
- Mechanic parents: publication-receipts
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

`aoa-evals` already has an eval-result receipt guide, receipt payload schema,
local stats envelope mirror, public example, live publisher, owner-local live
receipt route card, and tests. The pressure is no longer whether receipts
exist. The pressure is whether future agents can change the seam without
turning a publication sidecar into proof authority.

The active operation is narrow: a reviewed bounded report can emit an optional
eval-result receipt inside a `stats-event-envelope`, and an owner-local log may
record the publication. The bundle-local report and source proof object remain
stronger.

## Options Considered

- Leave publication receipts only as root guide, schemas, example, script, and
  `.aoa/live_receipts/` card.
- Move every receipt surface under one package directory without naming parts.
- Create `mechanics/publication-receipts/` as a route package and keep its
  authored receipt artifacts under named `parts/`, while leaving the owner-local
  live receipt log in `.aoa/live_receipts/`.

## Decision

Create `mechanics/publication-receipts/` for the operation:

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

The package routes receipt publication work through part-local homes:

- `parts/receipt-payload/` for the guide, payload schema, and public example;
- `parts/stats-envelope-mirror/` for the local `aoa-stats` envelope mirror;
- `parts/live-publisher/` for the owner-local append tool;
- `parts/intake-dry-review/` for the non-publishing intake review artifact.

The package still does not move `.aoa/live_receipts/`.

## Rationale

Publication receipts are useful because they make one bounded eval result
legible to downstream readers. They are dangerous when they look like a second
proof canon, generic telemetry truth, or global scoring layer.

A mechanics package makes the operation visible without absorbing stronger
owners. `aoa-evals` keeps eval-result payload meaning and verdict limits.
`aoa-stats` keeps the canonical shared envelope and event vocabulary. Bundle
reports remain the stronger machine-readable proof contract.

## Consequences

- Positive: receipt publication now has a package route, part-local source
  surfaces, and validator-backed discovery surface.
- Tradeoff: `.aoa/live_receipts/` remains outside the package parts. Future
  maintainers must still respect the live receipt card for append-only local
  memory.
- Follow-up: later validators can tighten cross-checks between reports,
  receipt payloads, `evidence_refs`, and append-only correction posture if real
  drift appears.

## Boundaries

This decision does not move `.aoa/live_receipts/`.

It does move the receipt payload guide/schema/example, local envelope mirror,
publisher script, and dry-review artifact into package-local parts because
those surfaces are publication-receipt mechanics rather than general root
district source truth.

It does not make receipts stronger than a bundle-local report, source
`EVAL.md`, or `eval.yaml`.

It does not authorize repo-global score construction, raw log publication,
private telemetry exposure, canonical `aoa-stats` ownership changes, or
receipt-count quality claims.

## Validation

- `mechanics/publication-receipts/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, validation, and
  next route.
- `mechanics/publication-receipts/PARTS.md` names the part topology.
- `mechanics/publication-receipts/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `README.md`,
  `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/publication-receipts/` owns the route from reviewed
  bounded report to optional eval-result receipt, stats-envelope sidecar,
  owner-local live log, and downstream derived reader.
- Clarified: the receipt guide now routes proof-canon, report replacement,
  repo-global score, live-log, and derived-summary pressure to owners instead
  of framing the seam through prohibition-only prose.
- Source surfaces updated:
  - `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
  - `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`
  - `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
  - `scripts/validate_repo.py`
- Validation: root repository validation, semantic AGENTS validation, receipt
  targeted tests, generated surface checks, and full pytest stayed green.

## Review Log

### 2026-05-24 - Receipt guide pressure routes clarified

- Previous assumption: receipt safety needed repeated negative statements about
  proof canon, report replacement, and receipt misuse.
- New reality: an agent follows the seam more reliably when each pressure points
  to the owner route that can carry it.
- Reason: publication receipts are downstream read models; role, input, output,
  owner, next route, tool, and validation are the durable operating facts.
- Source surfaces updated: receipt guide, public example interpretation bound,
  dry-review boundary strings, and validator tokens.
- Validation: root repository validation, semantic AGENTS validation, receipt
  targeted tests, generated surface checks, and full pytest stayed green.
