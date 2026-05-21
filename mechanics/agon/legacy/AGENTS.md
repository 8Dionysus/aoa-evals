# AGENTS.md

## Applies to

`mechanics/agon/legacy/`.

## Role

Legacy preserves Agon wave landing provenance and former root-path evidence
behind the active `mechanics/agon/` package.

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/README.md`
3. `mechanics/EVIDENCE_CLUSTERS.md`
4. `mechanics/agon/README.md`
5. `mechanics/agon/PARTS.md`
6. `mechanics/agon/PROVENANCE.md`
7. `mechanics/agon/legacy/INDEX.md`
8. `mechanics/agon/legacy/DISTILLATION_LOG.md`

## Boundaries

- Start from active Agon parts before using legacy.
- Do not put new Agon work in legacy.
- Do not treat wave files as active topology.
- Do not delete raw provenance without an explicit decision and validator-backed
  replacement.

## Validation

Run the root mechanics checks after changing legacy maps:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which legacy source was mapped, which active part owns the current route,
and whether any old docs-root reference remains accepted input.
