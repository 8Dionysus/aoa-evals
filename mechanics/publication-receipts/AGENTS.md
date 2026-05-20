# AGENTS.md

## Applies to

`mechanics/publication-receipts/` and publication receipt route guidance.

## Role

This package routes eval-result receipt publication work.

It does not own bundle meaning, bundle-local report interpretation, the
canonical `stats-event-envelope`, `.aoa/live_receipts/` as verdict authority,
or any repo-global score.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/publication-receipts/README.md`
7. `docs/EVAL_RESULT_RECEIPT_GUIDE.md`
8. `schemas/eval-result-receipt.schema.json`
9. `schemas/stats-event-envelope.schema.json`
10. `reports/eval-result-receipt-intake-dry-review-v1.json` for dry-review
    intake changes
11. `reports/AGENTS.md`
12. `.aoa/live_receipts/AGENTS.md`
13. affected bundle-local report and source bundle surfaces

## Local Law

- Keep receipts weaker than the bundle-local report.
- Keep the local `stats-event-envelope` mirror subordinate to `aoa-stats`.
- Keep `eval_result_receipt` payloads bounded to one eval publication.
- Keep `.aoa/live_receipts/` append-only and public-safe.
- Keep receipt-intake dry reviews visibly non-published.
- Use `supersedes` for correction instead of rewriting old publication facts.
- Keep evidence refs pointed back to source bundles and report artifacts.

## Boundaries

- Do not read raw live JSONL log content for a docs-only route change.
- Do not publish secrets, private telemetry, hidden benchmark data, or
  unreduced operator traces.
- Do not turn receipt count into proof quality.
- Do not let a receipt replace report review.
- Do not let a dry-review payload preview become a publishable receipt
  envelope.
- Do not edit canonical `aoa-stats` schema ownership from this repo.
- Do not strengthen a receipt beyond the bundle-local verdict boundary.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run receipt tests when schemas, examples, publisher behavior, or live receipt
validation changes:

```bash
python -m pytest -q tests/test_publish_live_receipts.py tests/test_live_receipt_log.py tests/test_validate_repo.py
```

## Closeout

Report which receipt seam changed, which bundle-local report remains stronger,
whether `aoa-stats` envelope ownership stayed mirrored rather than absorbed,
whether any owner-local append happened, what validation ran, and what raw or
private receipt material was intentionally not inspected.
