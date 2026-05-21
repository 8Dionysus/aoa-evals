# 0008 Boundary Bridge Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/boundary-bridge/`

## Context

The first refactor slice exposed sibling reference drift in `aoa-memo` paths.
That drift was repaired locally, and `docs/decisions/0003-sibling-proof-reference-compatibility.md`
recorded the boundary: sibling refs are proof inputs, not transfers of sibling
authority.

The repository already has `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py` and
`mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`, and the current latest-sibling canary
passes against local sibling checkouts. The remaining gap is a durable
compatibility map and package route so future drift does not return as
one-off path archaeology.

## Options Considered

- Leave sibling reference handling as validator implementation detail.
- Create a package only after the next failure.
- Create `boundary-bridge` now, because there is already a repaired failure, a
  canary matrix, a runner, and current sibling checkout evidence.

## Decision

Create `mechanics/boundary-bridge/` with package-local parts for sibling proof
reference compatibility and latest-sibling canary checking:

- `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`

The package owns the route:

`repo-qualified ref -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary -> bundle-local review`

It does not move existing refs or edit sibling repositories.

## Rationale

This makes sibling proof references convex: a future agent can tell whether a
ref is current, legacy, rejected, or unresolved before deciding whether it may
support local proof review.

It also keeps the sibling canary in the right place. The canary proves current
checkout compatibility under configured roots; it does not prove sibling owner
acceptance or local proof promotion.

## Consequences

- Positive: sibling path drift now has a package route, compatibility map, and
  validator-backed discovery surface.
- Tradeoff: another package exists before a machine-readable compatibility
  ledger. That ledger should wait until repeated drift proves the docs and
  canary matrix are insufficient.
- Follow-up: Phase 6 legacy containment can use this package when old sibling
  paths need accepted-input mappings.

## Boundaries

This decision does not authorize editing sibling repositories.

It does not make path existence proof authority, sibling owner acceptance,
generated-reader truth, bundle promotion, or runtime verdict meaning.

It does not replace bundle-local review.

## Validation

- `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md` names the compatibility map and posture
  vocabulary.
- `mechanics/boundary-bridge/README.md` names source surfaces, inputs,
  outputs, stronger-owner split, boundaries, legacy posture, validation, and
  next route.
- `mechanics/boundary-bridge/PARTS.md` names the compatibility-map and
  latest-sibling-canary parts.
- `mechanics/boundary-bridge/AGENTS.md` names local editing law.
- `python scripts/validate_repo.py`
- `python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json`
- `python scripts/validate_semantic_agents.py`
