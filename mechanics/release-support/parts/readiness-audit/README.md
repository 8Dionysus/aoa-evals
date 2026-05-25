# Release Support / Readiness Audit Part

## Role

This part owns the local release-prep readiness audit artifact.

## Source Surfaces

- `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- `mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py`
- `CHANGELOG.md`
- `docs/operations/RELEASING.md`
- `scripts/release_check.py`

The artifact says whether the accumulated strategic refactor is locally ready
for release-prep review after local gates. It routes publication state to live
owners: current git branch/merge state, GitHub PR approval and Repo Validation,
tags, GitHub Releases, live eval-result receipt publication, sibling mutation
evidence, and current goal review.

## Inputs

- bounded accumulated release-prep scope;
- `CHANGELOG.md` narrative anchor and release-support route law;
- local verification snapshot from generated checks, validators, package tests,
  full pytest, release check, whitespace check, and sibling canary when relevant;
- source evidence refs for design, decisions, quests, mechanics, reports,
  generated readers, receipt dry-review, and sibling-boundary surfaces;
- publication-state fields that route branch, PR, GitHub `Repo Validation`,
  merge, tag, release, and final completion review to live owner evidence.

## Outputs

- `release_support_readiness_audit` JSON report;
- requirement-by-requirement local release-prep readiness claims;
- `publication_boundary` fields for release, tag, GitHub Release, PR, GitHub
  `Repo Validation`, live receipt, sibling mutation, and goal completion, with
  `goal_completion_status` as `not_complete`;
- validator and test failures when readiness language becomes publication,
  approval, or completion language.

## Stronger Owner Split

This part owns the local readiness audit for release-prep review.

Root release entrypoints own their own lanes: `CHANGELOG.md` is the public
release narrative, `docs/operations/RELEASING.md` is the procedure, `scripts/release_check.py`
is the local release gate, and GitHub `Repo Validation` is the remote landing
gate.

Bundle-local proof objects, reports, schemas, and review docs remain stronger
than readiness audit claims.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| readiness audit treated as tag, GitHub Release, PR approval, observed GitHub `Repo Validation`, or goal completion | current git, GitHub, tag/release, and goal-audit evidence |
| green local release audit used to grow eval verdict or bundle status | bundle-local proof review |
| skipped checks or unresolved sibling compatibility | explicit verification snapshot and owner handoff |
| live eval-result receipt publication, runtime acceptance, or sibling mutation claim | receipt, runtime, or sibling-owner evidence |
| root release entrypoint movement | root or GitHub-native lane |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
## Next Route

Use this part when updating release-prep readiness evidence or its validator
contract. Keep `CHANGELOG.md`, `docs/operations/RELEASING.md`, `scripts/release_check.py`,
and `.github/workflows/repo-validation.yml` in their root or GitHub-native
lanes.
