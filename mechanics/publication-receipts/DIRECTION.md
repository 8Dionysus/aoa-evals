# Publication Receipts Direction

Publication Receipts in `aoa-evals` should record optional bounded eval-result
publication after review without strengthening the claim being published.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest receipt route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active publication-receipts part map.
- `parts/`: receipt payload, stats-envelope mirror, live publisher, and intake
  dry-review support.
- `PROVENANCE.md`: controlled bridge from active route to old receipt placement.
- `legacy/`: lineage only; not a live log.
- `.aoa/live_receipts/`: owner-local live receipt log, not authored source.

## Current contour

- Keep receipts optional and subordinate to reviewed bundle-local reports.
- Keep stats envelope mirroring local to validation; `aoa-stats` owns the
  canonical envelope.
- Keep live publishing explicit and separate from dry review.
- Keep receipt intake from becoming proof acceptance.

## Growth rule

Add receipt parts only when a repeated publication operation needs a schema,
publisher, dry review, mirror, or validation route. Do not create receipt
surface for unreviewed reports.

## Stop-lines

- Do not treat receipts as stronger than reports or source bundles.
- Do not publish live receipts from dry-review work.
- Do not turn receipt events into telemetry dashboards or repo-global scores.

## Validation

Use the validation lane in [mechanics/publication-receipts/AGENTS.md](AGENTS.md#validation).
