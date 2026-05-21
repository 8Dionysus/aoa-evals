# AGENTS.md

## Role

`schemas/` is a route-card-only compatibility surface for schema contract
paths.

Active schema payloads route to mechanic-local owners:

- Quest source and dispatch schemas live under `mechanics/questbook/parts/`.
- Eval frontmatter and manifest schemas live under
  `mechanics/proof-object/parts/eval-contracts/`.
- Shared fixture, runner, and report-summary contract schemas live under
  `mechanics/proof-infra/parts/reportable-contracts/schemas/`.

## Rules

Schema edits are proof contract edits. Preserve `$schema`, stable identifier posture, required fields, enums, and descriptions that keep verdict interpretation bounded.

Weak reports route to report, scorer, runner, or bundle-local contract repair;
schema permissiveness should keep the proof contract bounded.

Pair schema changes with examples, validator updates, and docs that explain interpretation limits.

Active root schema aliases route through each mechanic `PROVENANCE.md`; the
owning legacy archive explains itself after that bridge.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
