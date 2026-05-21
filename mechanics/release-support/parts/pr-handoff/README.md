# Release Support / PR Handoff Part

## Role

This part owns the pre-PR landing handoff artifact.

## Source Surfaces

- `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`
- `mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`

The artifact prepares branch, commit, PR title/body, changed-surface groups,
validation, and landing steps. It is not live GitHub state. After a branch or
PR exists, current git and GitHub evidence supersedes this snapshot for branch,
commit, push, PR, CI, and merge status.

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

Current local git state and GitHub state are stronger than the snapshot after a
branch or PR exists. GitHub `Repo Validation` remains stronger for remote
landing. Source proof objects, bundle-local reports, and release-support
readiness/strategic closeout artifacts remain stronger than PR-body wording.

## Stop-Lines

- Do not treat this artifact as a created branch, commit, push, PR, merge, tag,
  GitHub Release, or observed GitHub `Repo Validation`.
- Do not treat candidate PR wording as owner approval.
- Do not use handoff validation as proof that eval claims grew stronger.
- Do not claim live receipt publication, runtime acceptance, sibling mutation,
  bundle promotion, or goal completion.
- Do not keep using this snapshot as live status after a branch or PR exists.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
## Next Route

Use this part when updating the owner landing handoff. Do not use it to infer
that a branch, commit, push, PR, merge, tag, GitHub Release, live receipt, or
goal completion already happened.
