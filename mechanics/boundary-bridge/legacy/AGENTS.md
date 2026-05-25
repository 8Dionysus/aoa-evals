# AGENTS.md

## Applies to

`mechanics/boundary-bridge/legacy/`

## Role

This directory maps former boundary-bridge path vocabulary to active routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former boundary-bridge and sibling-proof-reference placement. |
| input | Old boundary-bridge path, sibling-proof-ref name, compatibility note, canary, proof anchor, or historical lookup question. |
| output | Active boundary-bridge parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/boundary-bridge/` owns current boundary-bridge proof work; this legacy district owns archive-local lookup and lineage accounting. |
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

- Start from active boundary-bridge parts before using legacy.
- Place current compatibility maps, canaries, proof anchors, and matrix payloads
  in the active parent or owning part.
- Treat `mechanics/sibling-proof-refs/` as historical vocabulary that maps back
  to active boundary-bridge topology.
- Keep sibling-owner acceptance tied to active proof and owner handoff surfaces.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which old boundary-bridge source was mapped, which active part owns the
current route, which archive accounting changed, and which checks ran.
