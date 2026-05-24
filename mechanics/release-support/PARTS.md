# Release Support / Part Index

`mechanics/release-support/` owns the release-publication proof route as a
mechanic, not as a flat list of root reports.

The package keeps root release entrypoints visible where contributors expect
them:

- `CHANGELOG.md` remains the public release narrative.
- `docs/RELEASING.md` remains the public release procedure.
- `scripts/release_check.py` remains the root local release gate.
- `.github/workflows/repo-validation.yml` remains the GitHub-native landing
  gate.

The mechanic-owned state artifacts live in parts:

- [Readiness Audit](parts/readiness-audit/README.md)
- [Strategic Closeout](parts/strategic-closeout/README.md)
- [PR Handoff](parts/pr-handoff/README.md)

Read these parts as release-support route artifacts. Live publication state is
owned by current git, GitHub, tag, and release evidence; eval claim strength is
owned by bundle-local proof surfaces.

## Part Contract

| Field | Route |
| --- | --- |
| Inputs | bounded release scope, changelog narrative, release procedure, repository validation posture, local handoff or audit evidence |
| Outputs | readiness audit, strategic closeout audit, PR handoff snapshot, or release-route review artifact |
| Owner split | root release entrypoints remain where contributors expect them; package parts own release-support state artifacts; bundle claims stay with source proof surfaces |
| Stop-lines | route tag, GitHub Release, PR approval, observed GitHub `Repo Validation`, merge, and goal completion checks to live owner evidence |
| Validation | parent `AGENTS.md` and `parts/AGENTS.md` command lanes |

Validation routes through [AGENTS](AGENTS.md#validation), including release
check, repo validation, and semantic AGENTS lanes.
