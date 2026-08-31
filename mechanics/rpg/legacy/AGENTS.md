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
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
## Route Rules

- Start from active RPG parts before using legacy.
- Place current RPG progression and unlock proof work in the active parent or
  owning part.
- Treat former root paths as historical input that maps back to active
  topology.
- Keep former paths mapped to active parts.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

## Closeout

Report which RPG legacy source was mapped, which active parent or part owns the
current route, which archive accounting changed, and which checks ran.
