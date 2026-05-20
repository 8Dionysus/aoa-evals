# 0013 Publication Receipts Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/publication-receipts/`

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

- Leave publication receipts only as a guide, schemas, example, script, and
  `.aoa/live_receipts/` card.
- Move receipt surfaces under one package directory.
- Create `mechanics/publication-receipts/` as a route package while leaving the
  guide, schemas, examples, publisher, reports, and live receipt log in place.

## Decision

Create `mechanics/publication-receipts/` for the operation:

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

The package routes receipt publication work without moving
`docs/EVAL_RESULT_RECEIPT_GUIDE.md`, `schemas/`, `examples/`,
`scripts/publish_live_receipts.py`, `reports/`, or `.aoa/live_receipts/`.

## Rationale

Publication receipts are useful because they make one bounded eval result
legible to downstream readers. They are dangerous when they look like a second
proof canon, generic telemetry truth, or global scoring layer.

A mechanics package makes the operation visible without absorbing stronger
owners. `aoa-evals` keeps eval-result payload meaning and verdict limits.
`aoa-stats` keeps the canonical shared envelope and event vocabulary. Bundle
reports remain the stronger machine-readable proof contract.

## Consequences

- Positive: receipt publication now has a package route and validator-backed
  discovery surface.
- Tradeoff: the package is intentionally a route layer, not a data move. Future
  maintainers must still read the guide, schemas, publisher, report cards, and
  live receipt card for exact local law.
- Follow-up: later validators can tighten cross-checks between reports,
  receipt payloads, `evidence_refs`, and append-only correction posture if real
  drift appears.

## Boundaries

This decision does not move `.aoa/live_receipts/`, `reports/`, `schemas/`,
`examples/`, or the receipt publisher.

It does not make receipts stronger than a bundle-local report, source
`EVAL.md`, or `eval.yaml`.

It does not authorize repo-global score construction, raw log publication,
private telemetry exposure, canonical `aoa-stats` ownership changes, or
receipt-count quality claims.

## Validation

- `mechanics/publication-receipts/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, validation, and
  next route.
- `mechanics/publication-receipts/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `README.md`,
  `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
