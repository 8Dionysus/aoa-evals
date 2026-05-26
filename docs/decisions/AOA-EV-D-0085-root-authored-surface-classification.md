# Root-authored Surface Classification

- Decision ID: AOA-EV-D-0085
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: root/topology
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

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

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/EVIDENCE_CLUSTERS.md` owns the residual
  root-authored surface classification ledger for top-level `docs/`,
  `scripts/`, and `tests/` files.
- Clarified: the former `docs/VIA_NEGATIVA_CHECKLIST.md` root guide now routes
  through `docs/guides/BOUNDARY_ROUTE_CHECKLIST.md`, so the file name and content name
  the agent action directly.
- Source surfaces updated:
  - `docs/guides/BOUNDARY_ROUTE_CHECKLIST.md`
  - `docs/README.md`
  - `mechanics/EVIDENCE_CLUSTERS.md`
  - `scripts/validate_repo.py`
- Validation: root-authored classification tests, root repository validation,
  and semantic AGENTS validation stayed green.

## Review Log

### 2026-05-24 - Boundary checklist renamed to route action

- Previous assumption: a via-negativa checklist was an acceptable
  root-authored guide name for bounded-proof safety.
- New reality: low-context agents need the file name and first screen to say
  which route action the guide owns.
- Reason: boundary pressure is handled through owner routes, source proof
  review, and validation rather than a free-standing negative checklist.
- Source surfaces updated: checklist file name/content, docs map link,
  root-authored classification ledger, and validator allowlist.
- Validation: root-authored classification tests, root repository validation,
  and semantic AGENTS validation stayed green.

### 2026-05-24 - Portable boundary guide route language clarified

- Previous assumption: portability guidance could rely on shorthand such as
  hidden-context warnings and universality disclaimers.
- New reality: low-context agents need the guide to name the review criteria:
  replacement contract, public setup route, bounded portable meaning, and
  travel-together proof surfaces.
- Reason: `docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md` is a root-owned guide; its
  first-pass route should expose the proof route before local-shaped deferral.
- Source surfaces updated: `docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k portable_eval_boundary`
  and `python scripts/validate_repo.py`.
