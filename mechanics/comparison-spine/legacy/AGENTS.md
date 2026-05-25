# AGENTS.md

## Applies to

`mechanics/comparison-spine/legacy/`

## Role

This directory preserves comparison-spine placement lineage for former root
fixture families.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former comparison-spine root fixture placement. |
| input | Old comparison fixture path, root fixture-family name, raw lineage note, or historical lookup question. |
| output | Active comparison-spine parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/comparison-spine/` owns current comparison proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `../AGENTS.md`
4. `../README.md`
5. `../DIRECTION.md`
6. `../PARTS.md`
7. `../PROVENANCE.md`
8. `docs/architecture/LEGACY_NAMING.md`
9. `INDEX.md`
10. `DISTILLATION_LOG.md`

## Route Rules

- Start from active comparison-spine parts before using legacy.
- Place current comparison proof work and fixture-family contracts in the
  active parent or owning part.
- Treat old root fixture paths as historical input that maps back to active
  topology.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which comparison legacy source was mapped, which active parent or part
owns the current route, which archive accounting changed, and which checks ran.
