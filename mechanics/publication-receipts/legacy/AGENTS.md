# AGENTS.md

## Applies to

`mechanics/publication-receipts/legacy/` provenance and lineage files.

## Role

This directory preserves old receipt root placement behind the active
`publication-receipts` mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former publication receipt, stats-envelope, publisher, live-log, and dry-review placement. |
| input | Old receipt path, stats-envelope residue, publisher script path, live-log path, dry-review report, or historical lookup question. |
| output | Active publication-receipts parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/publication-receipts/` owns current receipt payload contracts and publication support; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. root `AGENTS.md`
2. `mechanics/publication-receipts/AGENTS.md`
3. `mechanics/publication-receipts/README.md`
4. `mechanics/publication-receipts/PARTS.md`
5. `mechanics/publication-receipts/PROVENANCE.md`
6. `docs/LEGACY_NAMING.md`

## Route Rules

- Start from active publication-receipts parts before reading legacy.
- Keep old root receipt paths as lookup lineage that maps back to active
  placement.
- Place current receipt payloads, live logs, root guides, schemas, examples,
  publisher scripts, tests, and dry-review reports in the active parent or
  owning part.
- Treat stats-envelope paths as historical input unless an active owner surface
  accepts them.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which publication-receipts legacy source was mapped, which active part
owns the current route, which archive accounting changed, and which checks ran.
