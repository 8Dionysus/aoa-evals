# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/antifragility/DIRECTION.md` for current operating direction, `mechanics/antifragility/PARTS.md` for active parts, and `mechanics/antifragility/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/antifragility/` and its active parts.

## Role

This package routes antifragility proof work on the eval side.

It does not own AoA antifragility doctrine, owner-local cleanup, runtime repair,
playbook choreography, memory truth, stats truth, or generated verdict
authority.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/antifragility/README.md`
7. `mechanics/antifragility/PARTS.md`
8. `mechanics/antifragility/PROVENANCE.md` only when old placement matters

## Boundaries

- Keep source proof bundles under `evals/`.
- Keep comparison readout discipline under `mechanics/comparison-spine/`.
- Keep runtime-chaos selected evidence under `mechanics/audit/` until a
  bundle-local review accepts it.
- Keep repair proof bounded; do not turn repair into parent topology or final
  owner proof.
- Do not create new antifragility parts from one document, one report, one
  schema, one example, or one repair story.
- Do not absorb `aoa-diagnosis-cause-discipline` into this package unless a
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
