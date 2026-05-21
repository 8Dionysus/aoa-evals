# 0058 Release Support Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/release-support/parts/`

## Context

`release-support` owns the release-publication proof route:

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

The parent README and `PARTS.md` already keep release publication weaker than
bundle-local proof meaning. The remaining risk was that the three active part
README files were too thin for long-running work. A future agent could read
`readiness-audit`, `strategic-closeout`, or `pr-handoff` as release approval,
GitHub state, or goal completion rather than release-support artifacts with
strict claim limits.

## Decision

Make the three release-support part README files carry explicit part-level contracts:

- `mechanics/release-support/parts/readiness-audit/README.md`;
- `mechanics/release-support/parts/strategic-closeout/README.md`;
- `mechanics/release-support/parts/pr-handoff/README.md`.

Each part must expose inputs, outputs, `stronger owner split`, stop-lines, and
validation.

## Rationale

The active parent is `release-support`. Readiness audits, strategic closeout
audits, and PR handoff snapshots are forms inside that parent, not independent
parent mechanics and not remote publication evidence.

Root release entrypoints keep their own lanes. `CHANGELOG.md` carries the
public narrative, `docs/RELEASING.md` carries the procedure,
`scripts/release_check.py` carries the local audit gate, and GitHub `Repo
Validation` carries the remote landing gate.

The long goal remains stronger than any local closeout artifact: completion
requires landed state, observed GitHub validation, clean `main`, and
owner-visible final audit. The current part artifacts must keep `not_complete`
where completion has not happened.

## Consequences

- Positive: future release-support work starts from local part contracts instead
  of interpreting JSON report names as authority.
- Positive: `python scripts/validate_repo.py` now catches drift in the three
  release-support part README files.
- Positive: readiness, closeout, and handoff stay visibly inside
  `release-support`.
- Tradeoff: release-support wording is stricter where false completion would be
  tempting.

## Boundaries

This decision does not create a branch, commit, push, PR, merge, tag, GitHub
Release, live receipt, runtime acceptance, sibling mutation, bundle promotion,
or goal completion.

It does not make `CHANGELOG.md`, release notes, Git tags,
`scripts/release_check.py`, readiness audits, closeout audits, or PR handoff
snapshots stronger than source proof objects and bundle-local reports.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/release_check.py`
- `python -m pytest -q tests/test_validate_repo.py -k release_support_part_readmes`
