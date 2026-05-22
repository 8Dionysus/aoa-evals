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

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root schema contract paths |
| input | schema lookup, old root schema reference, or proof contract edit |
| output | mechanic-local schema owner route |
| owner | questbook, proof-object eval-contracts, or proof-infra reportable-contracts part |
| next route | owning mechanic part schema directory |
| tools | examples, validator updates, docs, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Route Rules

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
