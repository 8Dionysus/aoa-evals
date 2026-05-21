# Release Support / Readiness Audit Part

## Role

This part owns the local release-prep readiness audit artifact.

## Source Surfaces

- `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- `mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py`
- `CHANGELOG.md`
- `docs/RELEASING.md`
- `scripts/release_check.py`

The artifact says whether the accumulated strategic refactor is locally ready
for release-prep review after local gates. It must keep publication open: no
tag, no GitHub Release, no PR approval, no GitHub `Repo Validation` for the
uncommitted diff, no live eval-result receipt, and no goal completion.

## Inputs

- bounded accumulated release-prep scope;
- `CHANGELOG.md` narrative anchor and release-support route law;
- local verification snapshot from generated checks, validators, package tests,
  full pytest, release check, whitespace check, and sibling canary when relevant;
- source evidence refs for design, decisions, quests, mechanics, reports,
  generated readers, receipt dry-review, and sibling-boundary surfaces;
- explicit open publication conditions that still require branch, PR, GitHub
  `Repo Validation`, merge, tag, release, and final completion review.

## Outputs

- `release_support_readiness_audit` JSON report;
- requirement-by-requirement local release-prep readiness claims;
- `publication_boundary` fields that keep release, tag, GitHub Release, PR,
  GitHub `Repo Validation`, live receipt, sibling mutation, and goal completion
  open with `goal_completion_status` as `not_complete`;
- validator and test failures when readiness language becomes publication,
  approval, or completion language.

## Stronger Owner Split

This part owns the local readiness audit for release-prep review.

Root release entrypoints own their own lanes: `CHANGELOG.md` is the public
release narrative, `docs/RELEASING.md` is the procedure, `scripts/release_check.py`
is the local release gate, and GitHub `Repo Validation` is the remote landing
gate.

Bundle-local proof objects, reports, schemas, and review docs remain stronger
than readiness audit claims.

## Stop-Lines

- Do not treat the readiness audit as a tag, GitHub Release, PR approval,
  observed GitHub `Repo Validation`, or goal completion.
- Do not use a green local release audit to strengthen any eval verdict or
  bundle status.
- Do not hide skipped checks or unresolved sibling compatibility.
- Do not claim live eval-result receipt publication, runtime acceptance, or
  sibling mutation from this artifact.
- Do not move root release entrypoints into this part.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
## Next Route

Use this part when updating release-prep readiness evidence or its validator
contract. Keep `CHANGELOG.md`, `docs/RELEASING.md`, `scripts/release_check.py`,
and `.github/workflows/repo-validation.yml` in their root or GitHub-native
lanes.
