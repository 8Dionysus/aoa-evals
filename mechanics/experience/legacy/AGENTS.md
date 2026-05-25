# AGENTS.md

## Applies to

`mechanics/experience/legacy/`.

## Role

This district preserves Experience provenance behind the active
`mechanics/experience/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Experience wave, law, bridge, support, and version placement. |
| input | Old Experience path, raw wave packet, bridge note, support note, version note, or historical lookup question. |
| output | Active Experience parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/experience/` owns current Experience proof work; this legacy district owns archive-local lookup and lineage accounting. |
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

- Start from active Experience parts before using legacy.
- Place current Experience proof work in the active parent or owning part.
- Treat raw wave, law, bridge, support, and version files as historical input
  that maps back to active topology.
- Add raw or historical material with an active route, an index row, and
  distillation accounting.

## Validation

After changing legacy maps, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which Experience legacy source was mapped, which active parent or part
owns the current route, which archive accounting changed, and which checks ran.
