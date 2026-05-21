# AGENTS.md

## Applies to

`mechanics/proof-loop/legacy/` provenance and lineage files.

## Role

This directory preserves old proof-loop root report placement behind the active
`proof-loop` mechanic.

It is not the route-smoke report owner, not a proof bundle, not a generated
reader, not a receipt publisher, and not a place for new proof-loop work.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/proof-loop/AGENTS.md`
3. `mechanics/proof-loop/README.md`
4. `mechanics/proof-loop/PARTS.md`
5. `mechanics/proof-loop/PROVENANCE.md`
6. `docs/LEGACY_NAMING.md`

## Boundaries

- Start from active proof-loop parts before reading legacy.
- Keep old `reports/` paths as lookup lineage, not active report placement.
- Do not recreate proof-loop route-smoke reports under root `reports/`.
- Do not add new route-smoke artifacts here.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
