# AGENTS.md

## Guidance for `schemas/`

`schemas/` is a compatibility route card for schema contract placement, not an
active root schema payload district.

Mechanic-owned schemas live with their owning part. Quest source and dispatch
schemas live under `mechanics/questbook/parts/`, not this root district.
Eval frontmatter and manifest schemas live under
`mechanics/proof-object/parts/bundle-contracts/`, not this root district.
Shared fixture, runner, and report-summary contract schemas live under
`mechanics/proof-infra/parts/reportable-contracts/schemas/`, not this root
district.

No active root schema payload should live here.

Schema edits are proof contract edits. Preserve `$schema`, stable identifier posture, required fields, enums, and descriptions that keep verdict interpretation bounded.

Do not make schemas more permissive to pass a weak report. Fix the report, scorer, runner, or bundle-local contract.

Pair schema changes with examples, validator updates, and docs that explain interpretation limits.

Do not recreate active root schema aliases here. Use each mechanic
`PROVENANCE.md` for old root path lineage; the owning legacy archive explains
itself after that bridge.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
