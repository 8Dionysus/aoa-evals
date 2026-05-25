# AGENTS.md

## Applies to

`mechanics/rpg/legacy/`.

## Role

This directory preserves provenance for former root progression and unlock
proof placement.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former RPG progression and unlock proof placement. |
| input | Old RPG path, progression residue, unlock proof source, raw lineage note, or historical lookup question. |
| output | Active RPG parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/rpg/` owns current RPG proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/rpg/AGENTS.md`
4. `mechanics/rpg/README.md`
5. `mechanics/rpg/DIRECTION.md`
6. `mechanics/rpg/PARTS.md`
7. `mechanics/rpg/PROVENANCE.md`
8. `docs/architecture/LEGACY_NAMING.md`
9. `mechanics/rpg/legacy/INDEX.md`

## Route Rules

- Start from active RPG parts before using legacy.
- Place current RPG progression and unlock proof work in the active parent or
  owning part.
- Treat former root paths as historical input that maps back to active
  topology.
- Keep former paths mapped to active parts.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which RPG legacy source was mapped, which active parent or part owns the
current route, which archive accounting changed, and which checks ran.
