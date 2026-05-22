# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/publication-receipts/DIRECTION.md` for current operating direction, `mechanics/publication-receipts/PARTS.md` for active parts, and `mechanics/publication-receipts/PROVENANCE.md` only when legacy or former placement matters.

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

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/publication-receipts/README.md`
7. `mechanics/publication-receipts/PARTS.md`
8. the affected part `README.md`
9. `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
10. `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`
11. `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`
12. `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` for dry-review
    intake changes
13. `reports/AGENTS.md`
14. `.aoa/live_receipts/AGENTS.md`
15. affected bundle-local report and source bundle surfaces

## Local Law

- Keep receipts weaker than the bundle-local report.
- Keep the local `stats-event-envelope` mirror subordinate to `aoa-stats`.
- Keep `eval_result_receipt` payloads bounded to one eval publication.
- Keep `.aoa/live_receipts/` append-only and public-safe.
- Keep receipt-intake dry reviews visibly non-published.
- Use `supersedes` for correction instead of rewriting old publication facts.
- Keep evidence refs pointed back to source bundles and report artifacts.

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

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run receipt tests when schemas, examples, publisher behavior, or live receipt
validation changes:

```bash
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py tests/test_validate_repo.py
```

## Closeout

Report which receipt seam changed, which bundle-local report remains stronger,
whether `aoa-stats` envelope ownership stayed mirrored rather than absorbed,
whether any owner-local append happened, what validation ran, and what raw or
private receipt material was intentionally not inspected.
