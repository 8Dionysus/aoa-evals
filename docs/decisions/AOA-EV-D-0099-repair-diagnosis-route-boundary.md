# Repair Diagnosis Route Boundary

- Decision ID: AOA-EV-D-0099

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: proof topology
- Mechanic parents: none
- Guard families: sibling and boundary
- Posture: active rationale

## Context

The mechanics refactor rejected `repair` as a parent mechanic and routed bounded
repair proof to `mechanics/antifragility/parts/repair-proof/`.

A later Growth Cycle evidence pass activated
`mechanics/growth-cycle/parts/diagnosis-gate/` for
`aoa-diagnosis-cause-discipline`. Some Antifragility wording still described
diagnosis-cause discipline as future or deferred, which could make a future
agent pull diagnosis back into Antifragility or recreate a `repair` parent.

## Decision

Keep the two routes separate and explicit:

- `aoa-repair-boundedness` routes through
  `mechanics/antifragility/parts/repair-proof/`.
- `aoa-diagnosis-cause-discipline` routes through
  `mechanics/growth-cycle/parts/diagnosis-gate/`.
- `repair` remains a wrong parent form; future Growth Cycle repair stages still
  need separate evidence and must not steal current repair-proof support.
- Diagnosis-cause discipline is not an antifragility part, and repair proof is not diagnosis proof.

## Consequences

- Antifragility can own bounded repair proof without becoming repair authority.
- Growth Cycle can own diagnosis-gate proof without claiming repair success.
- Future repair-cycle work starts from evidence, not from old deferred wording.
- Legacy may explain old route history inside `legacy/`, but active surfaces
  must route current work through the two active parts above.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_mechanic_surface_contracts.py -k repair_diagnosis_route_boundary
python scripts/validate_repo.py --eval aoa-repair-boundedness
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/validate_repo.py
```
