# Release Support Parts

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

These parts are release-route artifacts. They do not publish a release, approve
a PR, create a tag, replace GitHub `Repo Validation`, or strengthen any eval
claim.

## Part Contract

Inputs are bounded release scope, changelog narrative, release procedure,
repository validation posture, and local handoff or audit evidence.

Outputs are readiness audits, strategic closeout audits, PR handoff snapshots,
and release-route review artifacts.

Owner split stays explicit: root release entrypoints remain where contributors
expect them; package parts own only release-support state artifacts and do not
own bundle claims.

Stop-lines forbid treating audits or handoffs as tags, GitHub Releases, PR
approval, observed GitHub `Repo Validation`, or goal completion.

Validation is `python scripts/release_check.py`,
`python scripts/validate_repo.py`, and `python scripts/validate_semantic_agents.py`.
