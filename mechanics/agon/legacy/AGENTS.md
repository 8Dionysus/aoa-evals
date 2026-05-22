# AGENTS.md

## Applies to

`mechanics/agon/legacy/`.

## Role

This district preserves Agon wave landing provenance and former root-path
evidence behind the active `mechanics/agon/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Agon wave, landing, and root-path placements. |
| input | Old Agon path, wave file, landing note, raw provenance question, or accepted historical vocabulary. |
| output | Active Agon parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/agon/` owns current Agon proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/README.md`
3. `mechanics/EVIDENCE_CLUSTERS.md`
4. `mechanics/agon/README.md`
5. `mechanics/agon/PARTS.md`
6. `mechanics/agon/PROVENANCE.md`
7. `mechanics/agon/legacy/INDEX.md`
8. `mechanics/agon/legacy/DISTILLATION_LOG.md`

## Route Rules

- Start from active Agon parts before using legacy.
- Place current Agon proof work in the active parent or owning part.
- Treat wave files as historical input that maps back to active topology.
- Preserve raw provenance until an explicit decision and validator-backed
  replacement name the stronger source.

## Validation

Run the root mechanics checks after changing legacy maps:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which legacy source was mapped, which active part owns the current route,
and whether any old docs-root reference remains accepted input.
