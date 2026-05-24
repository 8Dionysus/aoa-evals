# Release Support Direction

Release Support in `aoa-evals` makes release preparation reviewable while eval
claim strength stays with source proof surfaces.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest release-support route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active release-support part map.
- `parts/`: readiness-audit, strategic-closeout, and PR-handoff support.
- `PROVENANCE.md`: controlled bridge from active route to old proof-release placement.
- `legacy/`: archive-local route for old proof-release placement after
  `PROVENANCE.md`.
- root release surfaces: `CHANGELOG.md`, `docs/RELEASING.md`, CI workflows,
  and release scripts.

## Current contour

- Keep local release readiness, strategic closeout, and PR handoff distinct.
- Keep GitHub PR, CI, merge, tag, and release status current-state owned;
  report snapshots carry handoff evidence only.
- Keep validation claims bounded to what each command actually proves.
- Keep release narrative from strengthening proof claims.

## Growth rule

Add release-support parts only when a repeated release operation needs a
reviewable artifact and validator coverage. Ordinary changelog edits route to
`CHANGELOG.md`, `docs/RELEASING.md`, or `scripts/release_check.py`.

## Stop-lines

| Pressure | Route |
| --- | --- |
| tag, GitHub Release, PR approval, Repo Validation, publication, or goal completion from a local snapshot | current git, GitHub, tag/release, publication, and objective-audit evidence |
| bundle promotion or runtime acceptance through release wording | bundle-local proof review or runtime owner evidence |

## Validation

Use the validation lane in [mechanics/release-support/AGENTS.md](AGENTS.md#validation).
