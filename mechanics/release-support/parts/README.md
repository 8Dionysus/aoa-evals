# Release Support / Parts Route

The parts in this directory hold release-support-owned artifacts that were too
specific for root `reports/` once the mechanic became active.

Active parts:

- [Readiness Audit](readiness-audit/README.md): local release-prep readiness
  for the accumulated strategic refactor diff.
- [Strategic Closeout](strategic-closeout/README.md): requirement-by-
  requirement handoff audit for the long refactor goal.
- [PR Handoff](pr-handoff/README.md): pre-PR landing snapshot that prepares the
  owner route while current git and GitHub evidence own live branch, PR, CI,
  and merge status.

Root release entrypoints stay outside this directory when they are public or
repo-wide control surfaces: `CHANGELOG.md`, `docs/RELEASING.md`,
`scripts/release_check.py`, and `.github/workflows/repo-validation.yml`.
