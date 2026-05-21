# AGENTS.md

## Applies to

`mechanics/audit/legacy/` provenance and lineage files.

## Role

This directory preserves old audit/runtime-evidence placement and naming
history behind the active `audit` mechanic.

It is not the active packet contract, not the generated-reader source, not a
runtime owner surface, and not a place for new audit work.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/audit/AGENTS.md`
3. `mechanics/audit/README.md`
4. `mechanics/audit/PARTS.md`
5. `mechanics/audit/PROVENANCE.md`
6. `docs/LEGACY_NAMING.md`

## Boundaries

- Start from active audit parts before reading legacy.
- Keep `runtime-evidence` as evidence-class vocabulary, not parent topology.
- Do not recreate old root schemas, examples, generated readers, or
  `mechanics/runtime-evidence/`.
- Do not add new candidate packets here.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
