# 0057 Publication Receipts Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/publication-receipts/parts/`

## Index Metadata

- Surface classes: mechanic part, validation guard, report/release/receipt
- Mechanic parents: publication-receipts
- Guard families: part and payload, generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

`publication-receipts` owns the optional eval-result receipt route:

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

The parent README and `PARTS.md` already named that operation. The remaining
risk was part-level thinness. `receipt-payload`, `stats-envelope-mirror`,
`live-publisher`, and `intake-dry-review` could be read as independent
mechanics or as equally strong publication surfaces. That would recreate the
same naming failure the mechanics refactor is meant to prevent.

## Decision

Make the four publication receipt part README files carry explicit part-level
contracts:

- `mechanics/publication-receipts/parts/receipt-payload/README.md`;
- `mechanics/publication-receipts/parts/stats-envelope-mirror/README.md`;
- `mechanics/publication-receipts/parts/live-publisher/README.md`;
- `mechanics/publication-receipts/parts/intake-dry-review/README.md`.

Each part must expose part-level contracts with inputs, outputs,
`stronger owner split`, stop-lines, and validation.

## Rationale

The active parent is `publication-receipts`. Payloads, envelope mirrors,
publishers, and dry reviews are forms inside that parent, not new parent
mechanics.

The source bundle and reviewed report remain stronger than every receipt
surface. `aoa-stats` remains stronger for canonical stats envelope ownership.
`.aoa/live_receipts/` remains owner-local append memory, not proof authority.
The dry-review artifact stays `not_published`.

## Consequences

- Positive: future receipt work starts from part contracts instead of path
  archaeology.
- Positive: `python scripts/validate_repo.py` now catches drift in the four
  high-risk publication receipt part README files.
- Positive: receipt-payload, stats-envelope-mirror, live-publisher, and
  intake-dry-review stay visibly inside the `publication-receipts` parent.
- Tradeoff: publication receipt wording is stricter where overclaiming is easy.

## Boundaries

This decision does not publish a real eval-result receipt, create a stats event
envelope, append `.aoa/live_receipts/`, create a receipt-payload parent,
create a live-publisher parent, create a dry-review parent, promote a bundle,
accept runtime evidence, close a quest, claim a GitHub Release, or complete the
strategic goal.

It does not transfer canonical `aoa-stats` envelope authority into
`aoa-evals`.

## Validation

- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py -k publication_receipts_part_readmes`
