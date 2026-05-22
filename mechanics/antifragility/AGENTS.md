# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/antifragility/DIRECTION.md` for current operating direction, `mechanics/antifragility/PARTS.md` for active parts, and `mechanics/antifragility/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/antifragility/` and its active parts.

## Role

This package routes antifragility proof work on the eval side.

It maps eval-side antifragility pressure to posture review, stress-recovery
window, repair-proof, comparison-spine, audit, or stronger-owner handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | antifragility proof work route on the eval side |
| input | posture signal, stress-recovery readout, repair-proof pressure, audit-selected evidence, or stronger-owner antifragility question |
| output | active part route, comparison-spine route, audit route, source bundle review, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded proof support; stronger owners keep doctrine, runtime repair, playbook choreography, memory, stats, and generated verdict authority |
| next route | `mechanics/antifragility/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, and source proof bundle |
| tools | eval-specific validator, catalog builder, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/antifragility/README.md`
7. `mechanics/antifragility/PARTS.md`
8. `mechanics/antifragility/PROVENANCE.md` only when old placement matters

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep comparison readout discipline under `mechanics/comparison-spine/`.
- Keep runtime-chaos selected evidence under `mechanics/audit/` until a
  bundle-local review accepts it.
- Keep repair proof bounded below parent topology and final owner proof.
- Create antifragility parts from a recurring proof operation with validator
  coverage.
- Route `aoa-diagnosis-cause-discipline` through its current owner until a
  later evidence pass proves an antifragility-owned operation beyond local
  repair-proof routing.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-antifragility-posture
python scripts/validate_repo.py --eval aoa-stress-recovery-window
python scripts/validate_repo.py --eval aoa-repair-boundedness
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which antifragility part changed, which bundle stayed source-owned,
which comparison or audit surface stayed in its own mechanic, and which
stronger owner boundary was preserved.
