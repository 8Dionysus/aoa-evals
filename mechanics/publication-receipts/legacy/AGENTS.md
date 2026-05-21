# AGENTS.md

## Applies to

`mechanics/publication-receipts/legacy/` provenance and lineage files.

## Role

This directory preserves old receipt root placement behind the active
`publication-receipts` mechanic.

It is not the receipt payload contract, not the stats-envelope mirror, not the
publisher, not the live receipt log, not a dry review, and not a place for new
publication receipt work.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/publication-receipts/AGENTS.md`
3. `mechanics/publication-receipts/README.md`
4. `mechanics/publication-receipts/PARTS.md`
5. `mechanics/publication-receipts/PROVENANCE.md`
6. `docs/LEGACY_NAMING.md`

## Boundaries

- Start from active publication-receipts parts before reading legacy.
- Keep old root receipt paths as lookup lineage, not active placement.
- Do not recreate root receipt guides, schemas, examples, publisher scripts,
  tests, or dry-review reports.
- Do not add new receipt payloads or live logs here.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
