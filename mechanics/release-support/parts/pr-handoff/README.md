# Release Support / PR Handoff Part

## Role

This part owns the pre-PR landing handoff artifact.

## Source Surfaces

- `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`
- `mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`

The artifact prepares branch, commit, PR title/body, changed-surface groups,
validation, and landing steps. Live GitHub state is owned by current local git
and GitHub evidence after a branch or PR exists; that evidence supersedes this
snapshot for branch, commit, push, PR, CI, and merge status.

## Inputs

- release-support readiness audit and strategic closeout audit refs;
- candidate branch, commit message, PR title, PR body, changed-surface groups,
  validation list, and landing steps;
- current pre-handoff local worktree posture;
- explicit GitHub and publication statuses as a pre-PR snapshot;
- boundaries from release-support, proof topology, receipt posture, runtime
  candidate posture, and sibling-owner posture.

## Outputs

- `release_prep_pr_handoff` JSON report;
- a draft PR body and candidate landing route;
- changed-surface groups with evidence refs;
- validation snapshot and landing steps for a future owner-approved branch/PR;
- `pre_handoff_github_status` fields that keep branch, commit, push, PR, CI,
  merge, tag, and GitHub Release as not yet performed by this artifact.

## Stronger Owner Split

This part owns a pre-PR handoff snapshot only.

Live local git state and GitHub state are stronger than the snapshot after a
branch or PR exists. GitHub `Repo Validation` remains stronger for remote
landing. Source proof objects, bundle-local reports, and release-support
readiness/strategic closeout artifacts remain stronger than PR-body wording.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| snapshot treated as created branch, commit, push, PR, merge, tag, GitHub Release, or observed GitHub `Repo Validation` | current local git, GitHub, tag, and release evidence |
| candidate PR wording as owner approval | owner review and GitHub PR state |
| handoff validation as eval claim growth | bundle-local proof review |
| live receipt publication, runtime acceptance, sibling mutation, bundle promotion, or goal completion | receipt, runtime, sibling, bundle-owner, or current objective evidence |
| branch or PR exists after the snapshot | current git and GitHub evidence replace this snapshot |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
## Next Route

Use this part when updating the owner landing handoff. Use current git and
GitHub evidence when asking whether branch, commit, push, PR, merge, tag,
GitHub Release, live receipt, or goal completion already happened.
