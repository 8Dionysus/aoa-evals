# Release Support Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/release-support/` owns the operation that prepares and checks one
bounded `aoa-evals` release publication.

Changelog, GitHub workflow, generated catalog, and source proof bundle owners
keep their own authority. This package keeps release readiness, audit, PR
handoff, release-check posture, and publication checks bounded to one
`aoa-evals` release.

## Owned Operation

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

This package routes release proof publication work. Source proof meaning stays
in `evals/**/EVAL.md`, `evals/**/eval.yaml`, reports, schemas, and authored
guides. Release publication carries those surfaces; it does not make them
stronger.

In shorter form: release publication does not strengthen eval claims.

## Source Surfaces

- `docs/RELEASING.md`
- `CHANGELOG.md`
- `scripts/release_check.py`
- `.github/workflows/repo-validation.yml`
- `.github/AGENTS.md`
- `README.md` current release line
- `docs/AGENTS_ROOT_REFERENCE.md`
- `mechanics/release-support/PARTS.md`
- `mechanics/release-support/parts/README.md`
- `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- `mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py`
- `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json`
- `mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py`
- `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json`
- `mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- generated catalog check routed through `AGENTS.md#validation`
- repository validation routed through `AGENTS.md#validation`
- full local test gate routed through `AGENTS.md#validation`
- latest sibling canary route routed through `AGENTS.md#validation`

## Inputs

- one bounded release scope
- the matching `CHANGELOG.md` section that anchors the public release narrative
- changed source proof bundles, docs, schemas, mechanics, generated surfaces, or
  support artifacts
- release audit output from `scripts/release_check.py`
- optional latest-sibling canary output when current sibling compatibility is
  part of the release claim
- GitHub `Repo Validation` result when landing through PR

## Outputs

- reviewable release-prep diff
- optional readiness audit such as
  `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`
- strategic closeout audit when the long-goal handoff needs requirement-by-
  requirement review
- PR handoff snapshot when owner landing needs a prepared branch/PR route
- refreshed generated catalogs when source inputs changed
- local release audit result
- PR body or release handoff that names changed surfaces, validation, skipped
  checks, and remaining risk
- Git tag and GitHub release notes only after the release-prep change lands on
  `main`

## Stronger Owner Split

The release route packages and publishes proof surfaces. It does not decide
whether a proof claim is true.

Bundle-local proof objects remain stronger than release notes. `CHANGELOG.md`
is the human public release narrative, not proof authority. GitHub `Repo
Validation` is a landing gate, not a substitute for bundle-local review. The
Git tag records a published state; it does not promote draft, baseline, or
canonical status by itself.

Sibling repositories keep their own stronger truth. Latest-sibling canary
results may prove compatibility posture for release review, but they do not
transfer sibling authority into `aoa-evals`.

## Parts

Use [PARTS](PARTS.md) before editing package-owned release artifacts.

- [Readiness Audit](parts/readiness-audit/README.md) owns the local
  release-prep readiness artifact.
- [Strategic Closeout](parts/strategic-closeout/README.md) owns the
  long-goal handoff audit artifact.
- [PR Handoff](parts/pr-handoff/README.md) owns the pre-PR owner landing
  snapshot.

Root release entrypoints stay root- or GitHub-native when they are contributor
entrypoints or execution gates: `CHANGELOG.md`, `docs/RELEASING.md`,
`scripts/release_check.py`, and `.github/workflows/repo-validation.yml`.

## Readiness Audit

`mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` is a local readiness audit for
the accumulated strategic refactor diff.

It may say the diff is ready for release-prep review after local gates pass. It
must also say that no tag, GitHub Release, PR approval, GitHub `Repo
Validation`, eval result receipt, sibling mutation, or long-goal completion has
occurred.

## Strategic Closeout Audit

`mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` is a wider local handoff audit for
the accumulated strategic refactor plan.

It may say the local refactor is ready for owner/landing review. It must also
say that the long goal is not complete until a current objective audit proves
the mechanics-refactor definition of done and the requested GitHub landing
route completes: commit, push, PR, GitHub `Repo Validation`, merge,
fast-forward `main`, and clean worktree. PR landing is required for this
operator route, but it cannot substitute for the objective audit.

## Release Prep PR Handoff

`mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` is the pre-PR owner landing handoff
snapshot for the accumulated strategic refactor.

It may prepare a candidate branch, commit message, PR title, PR body, changed
surface groups, validation list, and landing steps. It must also say that at
snapshot time no branch, commit, push, PR had occurred: no branch, commit, push,
PR, GitHub `Repo Validation`, merge, tag, GitHub Release, live receipt, runtime
acceptance, sibling mutation, or goal completion had occurred. After a branch or
PR exists, current git and GitHub state supersedes the snapshot for live status.

## Boundaries

- Do not batch unrelated proof changes into one release because the audit is
  green.
- Do not let `scripts/release_check.py` replace bundle-local review.
- Do not publish a tag or GitHub release from this package route alone.
- Do not treat a readiness audit as a published release.
- Do not turn release notes into eval verdict authority.
- Do not use `CHANGELOG.md` to rewrite source proof meaning.
- Do not weaken validation to make a release pass.
- Do not claim current sibling compatibility unless the relevant canary or CI
  path was run.
- Do not use repo-prefixed release titles when the repo's human-facing release
  convention expects a plain tag such as `v0.3.3`.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- preparing a release section in `CHANGELOG.md`;
- changing `docs/RELEASING.md`;
- changing `scripts/release_check.py`;
- changing `.github/workflows/repo-validation.yml`;
- changing the part-local readiness, strategic closeout, or PR handoff
  artifacts;
- creating a PR intended to become a release-prep branch;
- creating or correcting a GitHub Release for `aoa-evals`.
