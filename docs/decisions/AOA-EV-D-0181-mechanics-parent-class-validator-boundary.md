# Mechanics Parent Class Validator Boundary

- Decision ID: AOA-EV-D-0181
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic parent registry/evidence validators, `mechanics/EVIDENCE_CLUSTERS.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After the mechanics root-surface split, `scripts/validators/mechanics.py` still
carried active parent allowlists, AoA-aligned versus evals-native class sets,
former wrong-parent routes, active parent evidence dimension ledger checks,
active parent evidence route-ref checks, and parent-class decision routing.

Those checks are mechanics parent-class law. They are not the same boundary as
root route-token presence or part-local test placement.

## Decision

Mechanics parent-class and evidence-ledger validation lives in
`scripts/validators/mechanics_parent_class.py`.

The module owns:

- active mechanic parent allowlists;
- AoA-aligned and evals-native class sets;
- former wrong-parent route mappings;
- active parent evidence dimension ledger checks;
- active parent evidence route-ref checks, including stale/generic/rationale-only
  route refs; and
- parent-class, evidence-dimension, and evidence-route-ref decision tokens.

`scripts/validators/mechanics.py` remains the compatibility and root-route
facade for existing imports and mechanics root route-token checks.

## Rationale

Parent-class law is a cross-parent topology boundary. It says which mechanic
parents are active, what class each parent belongs to, and what evidence each
parent must expose before it counts as part of the mechanics topology.

Keeping that law in the root mechanics facade made `mechanics.py` grow as a
catch-all for every mechanics topology concern. Splitting it keeps route tokens,
root-district classification, parent-class evidence, and mechanic payload
meaning apart.

## Consequences

- Positive: `mechanics.py` is now a smaller facade and root-route validator.
- Positive: parent-class/evidence failures have a focused validator, inventory
  row, mechanics ledger row, and decision rationale.
- Positive: existing callers that import parent constants from `mechanics.py`
  continue to work through compatibility aliases.
- Tradeoff: compatibility aliases remain until dependent validators can import
  the focused module directly.

## Current Applicability

As of 2026-06-04:

- Still valid: active mechanic parents must stay evidence-backed, classed, and
  free of stale/generic/rationale-only route refs.
- Changed: parent-class and evidence-ledger checks moved from `mechanics.py`
  into `mechanics_parent_class.py`.
- Further changed by: AOA-EV-D-0198 removes `mechanics_parent_class.py`; active
  behavior now routes to `mechanic_parent_registry.py`,
  `mechanic_evidence_dimensions.py`, and `mechanic_evidence_route_refs.py`.
- Superseded by: AOA-EV-D-0198 for the active module shape.

## Boundaries

This decision does not make the parent registry or evidence validators own
mechanic payload meaning, part contracts, runtime activation, generated
projections, release evidence, root-district classification, or root route-token
presence.

Those route to owning mechanic parents/parts, generated validators, release
validators, runtime/eval surfaces, `mechanics_root_districts.py`,
focused `root_authored_surface_*` validators, or the
`mechanics.py` root-route facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
