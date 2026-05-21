# Root-authored Surface Classification

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Context

The mechanics refactor moved many active payloads out of root districts and into
mechanic-owned parts. Some root districts are now route-card-only, but `docs/`,
`scripts/`, and `tests/` remain legitimate root-authored districts.

That creates a subtler failure mode: a future change can leave a mechanic-owned
payload in `docs/`, `scripts/`, or `tests/` and still look plausible because
those roots are not empty by design.

## Options Considered

- Leave residual root-authored files implicit.
- Make `docs/`, `scripts/`, and `tests/` route-card-only too.
- Add a residual classification ledger and validator allowlist for top-level
  root-authored surfaces that may remain in those districts.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` owns the Residual Root-authored Surface Classification
ledger.

Every top-level file under `docs/`, `scripts/`, and `tests/` must either appear
in that ledger as root-owned, or be moved to the owner that actually owns it.
Each row must state the root-owned role, the mechanic-owned payload boundary,
and the validation guard.

An unclassified root-authored surface is rejected by `scripts/validate_repo.py`.

## Rationale

The root-district reconnaissance ledger answers which districts exist and what
their posture is. This decision adds the next layer for the non-empty root
districts: the current files are not accidental residue.

This protects the goal's active topology without pretending that all useful
guidance, builders, validators, and repository-wide tests belong inside
mechanics.

## Consequences

- Positive: residual root-authored files become reviewable instead of ambient.
- Positive: mechanic-owned payload cannot quietly return to `docs/`, `scripts/`,
  or `tests/` without updating the ledger and validator.
- Positive: root-owned guides, builders, and tests remain legitimate where they
  are stronger than any one mechanic package.
- Tradeoff: new top-level files in those districts must update the ledger and
  validator allowlist in the same slice.

## Boundaries

The ledger is not a move plan and does not make every root-authored surface a
mechanic. It classifies what remains root-owned.

It does not replace route-card-only guards for `config`, `examples`, `fixtures`,
`manifests`, `reports`, `schemas`, `runners`, `scorers`, or `templates`.

It does not move source bundles, generated readers, quest records, or
bundle-local report tests into mechanics unless a separate evidence-backed
owner route proves the move.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k root_authored_surface_classification
python scripts/validate_repo.py
```
