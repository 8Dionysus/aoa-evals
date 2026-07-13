# Release Prep PR Handoff

- Decision ID: AOA-EV-D-0027
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/release-support/parts/pr-handoff/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: report/release/receipt
- Mechanic parents: none
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

The local strategic refactor now has a release-support readiness audit and a
strategic closeout audit. Both say the local diff is reviewable, and both keep
publication, GitHub `Repo Validation`, and goal completion open.

The next route is a landing route, but creating a branch, commit, push, PR,
merge, tag, or GitHub Release is a stronger operation than local repository
refactoring. The owner has not explicitly asked for `commit, push, merge` in
this step.

The repository therefore needs a handoff artifact that preserves the PR shape,
changed surface groups, validation list, boundaries, and landing steps without
pretending that any GitHub action has happened at handoff-preparation time.

## Options Considered

- Open a PR immediately: rejected for this step because the current request is
  to continue the goal, not an explicit commit/push/merge instruction.
- Leave the PR shape only in chat: rejected because a long-running refactor
  needs file-backed re-entry evidence.
- Add `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`: accepted because it prepares a
  concrete landing route while recording all GitHub and publication statuses as
  a pre-PR snapshot.

## Decision

`aoa-evals` keeps `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` as the first pre-PR
release-prep handoff snapshot for the accumulated strategic refactor.

The artifact may name a candidate branch, commit message, PR title, PR body,
changed surface groups, validation snapshot, and landing steps. It must mark
branch, commit, push, PR, GitHub `Repo Validation`, merge, tag, GitHub Release,
live receipt publication, runtime acceptance, sibling mutation, and goal
completion statuses as pre-handoff facts, not live-current GitHub truth.

Short boundary form: PR shape prepared; this artifact alone is not PR evidence.

## Rationale

The refactor is now large enough that the landing route should not rely on
conversation memory. A handoff artifact lets the next operator or agent inspect
the intended PR without losing the strict difference between local readiness
and remote landing evidence.

This also prevents two common failure modes: treating a green local release
check as equivalent to branch review, GitHub `Repo Validation`, merge readiness,
or goal completion; and treating an old handoff snapshot as live GitHub state
after a branch or PR exists.

## Consequences

- Positive: the next landing step has a reviewable PR title, body, validation
  list, and boundary list.
- Positive: the handoff is weaker than the actual GitHub route and its status
  block cannot be mistaken for live PR state after PR creation.
- Tradeoff: one more release-support part artifact must remain validator-covered
  and subordinate to actual branch/PR/CI evidence.
- Follow-up: if the owner asks to land, reread this handoff as a pre-PR
  snapshot, rerun the broad gates, create the branch/commit/PR, wait for GitHub
  `Repo Validation`, and only then consider merge and final completion audit.

## Boundaries

Do not infer from this artifact alone that a branch was created.
Do not infer from this artifact alone that a commit was created.
Do not infer from this artifact alone that anything was pushed.
Do not infer from this artifact alone that a PR was opened or approved.
Do not infer from this artifact alone that GitHub `Repo Validation` has approved
this diff.
Do not infer that a merge, tag, or GitHub Release exists.
Do not infer that a live eval-result receipt was published.
Do not use this handoff to promote a bundle, accept runtime evidence, mutate
sibling repositories, mutate sibling repos, or mark the goal complete.

After a branch or PR exists, current local git state and GitHub state supersede
the handoff snapshot for branch, commit, push, PR, CI, and merge status.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
