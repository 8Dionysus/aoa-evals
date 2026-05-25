# 0028 Repo Validation aoa-memo Pin Refresh

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `.github/workflows/repo-validation.yml`

## Index Metadata

- Surface classes: proof topology
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

GitHub `Repo Validation` failed after the strategic refactor branch was pushed.
The local latest-sibling canary passed against the current sibling checkout, but
the GitHub workflow still pinned `aoa-memo` to an older commit. That older
checkout did not contain the current `aoa-memo` surfaces referenced by
`aoa-evals` examples, reports, and generated readers.

The failure was useful: it showed that the strict pinned CI lane was doing its
job, but its `aoa-memo` ref no longer matched the sibling proof references this
repo now validates.

## Options Considered

- Weaken or bypass the failing path checks: rejected because the check caught
  real dependency drift.
- Mutate `aoa-memo` or add compatibility aliases there: rejected because
  `aoa-evals` owns this landing route, and sibling mutation was outside scope.
- Refresh only the pinned `aoa-memo` checkout in `Repo Validation`: accepted
  because it keeps CI strict while aligning the pinned lane with current
  sibling truth.

## Decision

Refresh the `aoa-memo` checkout ref in `.github/workflows/repo-validation.yml`
to `97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f`.

This is a pinned CI-lane update, not a latest-sibling canary substitution. The
latest-sibling canary remains the read of current local sibling checkouts; GitHub
`Repo Validation` remains the strict public landing gate using pinned sibling
refs.

## Rationale

The local proof-reference repair already points at current `aoa-memo` topology.
Updating the CI pin preserves the intended invariant: if `aoa-evals` cites a
sibling proof surface, the public workflow should be able to resolve that
surface without weakening validation or editing the sibling owner.

## Consequences

- Positive: `Repo Validation` can test the same `aoa-memo` topology the local
  latest-sibling canary already proved.
- Positive: the workflow stays deterministic because it still uses a pinned
  commit.
- Tradeoff: future sibling path movement can fail CI again until the pinned lane
  is reviewed and refreshed.
- Follow-up: when proof refs into `aoa-memo` move again, verify the sibling
  checkout, refresh the workflow pin intentionally, and keep the decision trail
  visible.

## Boundaries

This decision does not mutate `aoa-memo`.
It does not make `aoa-evals` the owner of memo meaning.
It does not weaken path validation or convert latest-sibling canary output into
GitHub approval.
It does not mark the PR, release, or long goal complete.

## Validation

- GitHub failure logs showed missing `aoa-memo` paths under `.deps/aoa-memo`.
- Local `aoa-memo` `main` and `origin/main` both resolved to
  `97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f`.
- `scripts/validate_repo.py` now checks the pinned workflow ref.
- The landing route must rerun local release validation and GitHub
  `Repo Validation` after this change.
