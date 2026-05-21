# Proof Object Legacy

## Role

This directory preserves old proof-object template and schema placement behind
the active mechanic.

Do not use it as a bundle source, template source, schema source, or generated
reader.

## Route

Active route first:

1. `mechanics/proof-object/README.md`
2. `mechanics/proof-object/PARTS.md`
3. `mechanics/proof-object/PROVENANCE.md`
4. `legacy/INDEX.md`

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Required Route

Open `../PROVENANCE.md` before using this directory. Use `INDEX.md` for
old-path lookup, `DISTILLATION_LOG.md` for raw-to-active accounting, and
`raw/README.md` for raw lineage. Legacy is not active topology and not a
new-work entrypoint.
