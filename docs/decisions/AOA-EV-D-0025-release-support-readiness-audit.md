# Release Support Readiness Audit

- Decision ID: AOA-EV-D-0025
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/release-support/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: report/release/receipt, boundary/runtime/sibling
- Mechanic parents: release-support, audit
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

The strategic refactor now spans root design, agent route cards, decisions,
roadmap, quests, proof topology, legacy naming, mechanics packages, generated
readers, proof-loop reports, receipt-intake dry review, validators, and tests.

`scripts/release_check.py` is green locally, but a green local release audit is
not the same as a bounded release-prep review, GitHub `Repo Validation`, tag,
GitHub Release, or completion of the long strategic goal.

The repository needs a public-safe readiness artifact that says what is locally
ready for release-prep review and what remains explicitly outside publication.

## Options Considered

- Treat the green `release_check.py` result as sufficient: rejected because it
  hides scope, skipped publication steps, and goal-completion limits.
- Prepare a real release section, tag, or PR body immediately: rejected because
  the accumulated diff still needs a release-prep readiness audit before
  publication routing.
- Add `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json`: accepted because it
  maps requirements, evidence, local gates, and open publication conditions
  without publishing a release.

## Decision

`aoa-evals` keeps `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` as the first
release-support readiness audit for the accumulated strategic refactor diff.

The artifact may state local release-prep review readiness. It must also state
that no tag, GitHub Release, PR approval, GitHub `Repo Validation` result for an
uncommitted diff, eval result receipt, sibling mutation, or goal completion has
occurred.

Short boundary form: no tag, no GitHub Release, no PR approval, no goal completion.

## Rationale

The release route is where a large proof-layer refactor is most likely to
overclaim. A readiness audit makes the difference visible:

- local checks can be green;
- changed surfaces can be reviewable;
- generated readers can be current;
- sibling compatibility can have canary evidence;
- and publication can still remain open.

That distinction protects bundle-local proof meaning and keeps release
publication weaker than source proof objects.

## Consequences

- Positive: future agents get a concrete release-prep handoff surface instead
  of inferring readiness from scattered checks.
- Tradeoff: the audit is one more report surface to validate and keep
  subordinate to `CHANGELOG.md`, `docs/operations/RELEASING.md`, and the actual PR/CI
  route.
- Follow-up: a later landing slice can turn this readiness audit into a PR
  handoff, but only after rerunning the required gates and preserving skipped
  publication boundaries.

## Boundaries

Do not infer that a release was published.
Do not infer that a tag or GitHub Release exists.
Do not infer that GitHub `Repo Validation` has approved this uncommitted diff.
Do not infer that the long strategic goal is complete.
Do not use this audit to strengthen any eval verdict, bundle status, sibling
truth, receipt, or runtime evidence.

## Validation

The route is protected by `scripts/validate_repo.py`, targeted tests for
release-readiness overclaim boundaries, `python scripts/release_check.py`, and
the generated/sibling/full-test battery before any later publication route.
