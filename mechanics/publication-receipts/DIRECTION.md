# Publication Receipts Direction

Publication Receipts in `aoa-evals` should record optional bounded eval-result
publication after review without strengthening the claim being published.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest receipt route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active publication-receipts part map.
- `parts/`: receipt payload, stats-envelope mirror, live publisher, and intake
  dry-review support.
- `PROVENANCE.md`: controlled bridge from active route to old receipt placement.
- `legacy/`: archive-local route for old receipt placement after
  `PROVENANCE.md`; live log routing stays under `.aoa/live_receipts/`.
- `.aoa/live_receipts/`: owner-local live receipt log; authored source routing
  stays with the package and its parts.

## Current contour

- Keep receipts optional and subordinate to reviewed bundle-local reports.
- Keep stats envelope mirroring local to validation; `aoa-stats` owns the
  canonical envelope.
- Keep live publishing explicit and separate from dry review.
- Keep receipt intake from becoming proof acceptance.

## Growth rule

Add receipt parts only when a repeated publication operation needs a schema,
publisher, dry review, mirror, or validation route. Unreviewed report pressure
routes back to bundle-local review before any receipt surface grows.

## Stop-lines

| Pressure | Route |
| --- | --- |
| receipts read as stronger than reports or source bundles | return proof meaning to the reviewed report and source bundle |
| dry-review work reads as live publication | route to intake dry review until a real receipt envelope exists |
| receipt events read as telemetry dashboards or repo-global scores | route dashboard vocabulary and scoring claims to their stronger owners |

## Validation

Use the validation lane in [mechanics/publication-receipts/AGENTS.md](AGENTS.md#validation).
