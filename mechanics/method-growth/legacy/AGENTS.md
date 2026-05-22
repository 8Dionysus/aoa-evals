# AGENTS.md

## Applies to

`mechanics/method-growth/legacy/`.

## Role

This district preserves Method Growth provenance behind the active
`mechanics/method-growth/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Method Growth path and fixture-family placement. |
| input | Old Method Growth path, fixture-family residue, raw lineage note, or historical lookup question. |
| output | Active Method Growth parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/method-growth/` owns current Method Growth proof work; this legacy district owns archive-local lookup and lineage accounting. |
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
8. `docs/LEGACY_NAMING.md`
9. `INDEX.md`
10. `DISTILLATION_LOG.md`

## Route Rules

- Start from active Method Growth parts before using legacy.
- Place current Method Growth proof work and fixture-family contracts in the
  active parent or owning part.
- Treat former root paths as historical input that maps back to active
  topology.
- Keep old paths mapped to current parts and validators.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which old path or name was mapped and which active part owns it now.
