# AGENTS.md

## Applies to

`mechanics/questbook/legacy/`.

## Role

This legacy bridge preserves old questbook path and placement lineage behind
the active questbook mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former questbook path, source, and placement vocabulary. |
| input | Old questbook path, quest source residue, raw file, accepted historical vocabulary, or historical lookup question. |
| output | Active questbook parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/questbook/` owns current questbook proof work; `quests/` owns quest source-card routes; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Route Rules

- Start from active questbook and `quests/` surfaces before using legacy.
- Place current quest work in the active parent, owning part, or `quests/`
  source route.
- Treat legacy path vocabulary as historical input that maps back to active
  source placement.
- Add raw files when they preserve lineage that belongs outside the active part
  and git history.
- Keep active routes first, then legacy lookup.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

## Closeout

Report which questbook legacy source was mapped, which active parent, part, or
`quests/` source route owns the current route, which archive accounting
changed, and which checks ran.
