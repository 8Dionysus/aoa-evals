# Mechanic Parent Direction Validator Boundary

- Decision ID: AOA-EV-D-0177
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanic_parent_direction.py`, `docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/mechanic_parents.py` protected several parent-level
questions at once: active parent allowlist, route-card coverage, current
direction contracts, parent-level guidance docs, lower-parts index command
hygiene, and old flat mechanic path bans.

The current-direction checks are a distinct boundary. They validate the parent
`DIRECTION.md` contract, README/AGENTS entry route, stale route wording,
direction decision record, proof topology references, legacy naming posture, and
roadmap routing. Those checks should not be owned by the same body that owns
allowlist and guidance-doc policy.

## Decision

Mechanic parent current-direction validation lives in
`scripts/validators/mechanic_parent_direction.py`.

The module owns:

- parent `DIRECTION.md` required tokens;
- parent README direction-entry route checks;
- parent AGENTS direction-entry route checks;
- stale negative route-language guards for active mechanic parent route cards;
- direction decision token checks;
- proof-topology, legacy-naming, roadmap, mechanics README, and mechanics
  AGENTS route references for current direction.

`scripts/validators/mechanic_parent_common.py` owns only shared token lookup and
markdown command parsing. Historical aggregate imports were removed later by
AOA-EV-D-0194.

## Rationale

Parent direction is the current operating contour of a mechanic. It is not the
same as the parent allowlist, parent-level guidance-doc admission, lower parts
index command hygiene, or legacy path bans.

Splitting direction checks prevents `mechanic_parents.py` from becoming a
historical catch-all for every parent-level concern while preserving the
existing aggregate validation route used by `mechanics_routes.py`.

## Consequences

- Positive: direction contracts now have a focused validator, inventory row,
  mechanics ledger row, and decision rationale.
- Positive: tests and route orchestration import the focused direction
  validator directly.
- Tradeoff: mechanic route orchestration imports direction alongside sibling
  mechanic-parent validators.

## Current Applicability

As of 2026-06-04:

- Still valid: every active mechanic parent must expose current direction and
  route README/AGENTS entry surfaces through that direction.
- Changed: direction contract checks moved out of `mechanic_parents.py` and
  into `mechanic_parent_direction.py`.
- Superseded by: AOA-EV-D-0194 removes the remaining `mechanic_parents.py`
  aggregate validator.

## Boundaries

This decision does not let `mechanic_parent_direction.py` own mechanic parent
allowlists, parent-level guidance docs, lower parts index command hygiene,
legacy archive meaning, part payload meaning, generated parity, release artifact
freeze, runtime policy, or trace/eval grading.

Those route to `mechanic_parent_allowlist.py`,
`mechanic_parent_guidance.py`, `mechanic_parent_index.py`, focused mechanic
legacy/provenance validators, focused mechanic part validators, or stronger
runtime and eval surfaces.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
