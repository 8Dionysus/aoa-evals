# 0050 Part-local Test Placement

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/*/parts/*/tests/`

## Index Metadata

- Surface classes: mechanic part
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

The mechanics refactor moved many active docs, schemas, reports, scripts,
fixtures, and generated support surfaces behind their owning mechanic parts.
Some tests still remained in root `tests/` even after they no longer tested a
repo-wide gate. They loaded part-local scripts or asserted part-local reports:

- `proof-infra/parts/reportable-contracts` scorer helper behavior;
- `publication-receipts` live publisher, live receipt log validation, and dry
  review boundaries;
- `release-support` readiness, strategic closeout, and PR handoff artifacts;
- `boundary-bridge/parts/latest-sibling-canary` runner behavior.

Leaving those tests in root `tests/` kept an active part contract outside the
part that owned it and made root tests look like the only validation district.

## Options Considered

- Leave all tests in root `tests/` because pytest can collect them there.
- Move the entire `tests/` district into `mechanics/`.
- Move only tests that already prove a mechanic part's local contract beside
  that part.

## Decision

Part-owned tests live under the owning part:

`mechanics/<mechanic>/parts/<part>/tests/`

Root `tests/` remains the repository-wide test district for validators,
catalogs, generated readers, semantic route cards, roadmap parity, and bundle
or repo-level checks that do not have a narrower active part owner.

## Rationale

Tests are part of the proof route. If a test validates a part-local script,
schema, report, or runner, keeping the test next to that part makes the owner
split visible and prevents root `tests/` from hiding the mechanic topology.

The route also avoids moving by theme. Tests move only when the current test
already has a narrower owner. Repo-wide tests stay root-owned.

## Consequences

- Positive: mechanic parts now carry their own validation surface alongside
  docs, schemas, scripts, reports, and stop-lines.
- Positive: root `tests/` becomes a clearer repo-wide district instead of a
  mixed attic for every proof check.
- Tradeoff: focused pytest commands become longer.
- Tradeoff: full validation should use `python -m pytest -q`, not only
  `python -m pytest -q tests`, when part-local tests matter.

## Boundaries

This decision does not move source proof bundles, generated readers, root
validators, roadmap parity checks, semantic route-card checks, or bundle-level
report tests by default.

It does not create a new parent mechanic from a test name. Test files remain
validators for the part that owns the operation.

## Validation

- `docs/architecture/PROOF_TOPOLOGY.md`
- `tests/AGENTS.md`
- `mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py`
- `mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py`
- `mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py`
- `mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py`
- `python -m pytest -q`
- `python scripts/validate_repo.py`
