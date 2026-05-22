# Release Support Direction

Release Support in `aoa-evals` should make release preparation reviewable
without making release publication strengthen any eval claim.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest release-support route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active release-support part map.
- `parts/`: readiness-audit, strategic-closeout, and PR-handoff support.
- `PROVENANCE.md`: controlled bridge from active route to old proof-release placement.
- `legacy/`: lineage only; not release status.
- root release surfaces: `CHANGELOG.md`, `docs/RELEASING.md`, CI workflows,
  and release scripts.

## Current contour

- Keep local release readiness, strategic closeout, and PR handoff distinct.
- Keep GitHub PR, CI, merge, tag, and release status current-state owned, not
  report-snapshot owned.
- Keep validation claims bounded to what each command actually proves.
- Keep release narrative from strengthening proof claims.

## Growth rule

Add release-support parts only when a repeated release operation needs a
reviewable artifact and validator coverage. Do not use release-support as a
parking place for ordinary changelog edits.

## Stop-lines

- Do not claim tag, GitHub Release, PR approval, Repo Validation, publication,
  or goal completion from a local snapshot.
- Do not promote bundles or accept runtime evidence through release wording.

## Validation

Use the validation lane in [mechanics/release-support/AGENTS.md](AGENTS.md#validation).
