# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/publication-receipts/DIRECTION.md`, `mechanics/publication-receipts/PARTS.md`, and `mechanics/publication-receipts/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/publication-receipts/` and publication receipt route guidance.

## Role

This package routes eval-result receipt publication work.

It routes receipt payloads, stats-envelope mirror pressure, live publisher
behavior, and intake dry review back to bundle-local reports, `aoa-stats`
ownership, and append-only publication boundaries.

## Operating Card

| Field | Route |
| --- | --- |
| role | eval-result receipt route for publication payloads and dry-review seams |
| input | eval-result receipt payload, stats-event-envelope mirror, live publisher change, intake dry-review artifact, or `.aoa/live_receipts/` boundary question |
| output | payload/schema route, publisher test route, dry-review handoff, append-only publication route, or stronger-owner handoff |
| owner | bundle-local report owns verdict meaning; publication-receipts owns receipt shape and local publication route |
| next route | `mechanics/publication-receipts/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, affected bundle-local report, and `.aoa/live_receipts/AGENTS.md` when append behavior moves |
| tools | root validator, semantic AGENTS validator, receipt tests, publisher tests |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| bundle-local verdict meaning | affected bundle-local report and source bundle |
| eval-result receipt payload | `mechanics/publication-receipts/parts/receipt-payload/` |
| canonical stats envelope meaning | `aoa-stats`; local mirror stays under `stats-envelope-mirror` |
| live append behavior | `mechanics/publication-receipts/parts/live-publisher/` and `.aoa/live_receipts/AGENTS.md` |
| intake dry review | `mechanics/publication-receipts/parts/intake-dry-review/` |
| report index or release posture | report/release owner route before claim strengthening |

## Local Law

- Keep receipts weaker than the bundle-local report.
- Keep the local `stats-event-envelope` mirror subordinate to `aoa-stats`.
- Keep `eval_result_receipt` payloads bounded to one eval publication.
- Keep `.aoa/live_receipts/` append-only and public-safe.
- Keep receipt-intake dry reviews visibly non-published.
- Use `supersedes` for correction instead of rewriting old publication facts.
- Keep evidence refs pointed back to source bundles and report artifacts.

Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

## Route Rules

- Inspect raw live JSONL only when the live publication route requires it.
- Publish only public-safe, reduced receipt material.
- Treat receipt count as publication evidence, with proof quality staying in
  bundle-local review.
- Keep receipts below report review.
- Keep dry-review payload previews outside the publishable receipt envelope.
- Route canonical `aoa-stats` schema ownership through `aoa-stats`.
- Keep receipt strength bounded by the bundle-local verdict boundary.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run the narrow package route checks:

Run receipt tests when schemas, examples, publisher behavior, or live receipt
validation changes:

## Closeout

Report which receipt seam changed, which bundle-local report remains stronger,
whether `aoa-stats` envelope ownership stayed mirrored rather than absorbed,
whether any owner-local append happened, what validation ran, and what raw or
private receipt material stayed outside scope.
