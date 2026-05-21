# 0065 Growth-cycle Diagnosis-gate Contract

## Status

Accepted.

## Context

`mechanics/growth-cycle/` is deliberately narrow. The active eval-side
operation is `diagnosis-gate` for `aoa-diagnosis-cause-discipline`; repair,
progression, closeout, harvest, quest promotion, and owner followthrough remain
outside the package until separate evidence proves active parts.

The package README and `PARTS.md` already preserve this route, but the
`diagnosis-gate` part README still used a thin `Boundary` section instead of
explicit `Stronger Owner Split` and `Stop-Lines`.

## Decision

Require `mechanics/growth-cycle/parts/diagnosis-gate/README.md` to expose:

- an eval-backed thin support route statement when it has no part-local
  payload subdirectories;
- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

`diagnosis-gate` remains a cause-hypothesis discipline part. It does not become
a repair parent, owner-fit proof route, final object-quality proof, broad growth
score, reviewed-closeout chain, donor-harvest approval, quest-promotion
gate, memory canon, runtime activation, or owner-local landing authority.
The explicit broad growth score stop-line is part of this contract.

## Consequences

- Future Growth Cycle edits must keep diagnosis before repair as a proof
  boundary, not a broad growth claim.
- Repair proof remains under `mechanics/antifragility/parts/repair-proof/`.
- Repeated-window movement remains under
  `mechanics/comparison-spine/parts/longitudinal-window/`.
- RPG progression and unlock proof remains under
  `mechanics/rpg/parts/progression-unlocks/`.
- Closeout, harvest, quest promotion, and owner followthrough remain
  obligations or ingress pressure until separate eval-side operations exist.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k growth_cycle_diagnosis_gate
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q
```
