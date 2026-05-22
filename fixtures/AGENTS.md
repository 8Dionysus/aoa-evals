# AGENTS.md

## Role

`fixtures/` is the public-safe compatibility route card for former root shared
fixture families.

Active fixture-family directories route to the owning mechanic part.

## Current shared families

Generic shared fixture families now live under:

- `mechanics/proof-infra/parts/fixture-families/fixtures/`

Comparison-spine fixture families now live under their active parts:

- `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/`
- `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/`

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for former root shared fixture families |
| input | shared fixture lookup, old root fixture reference, or bundle support need |
| output | owning mechanic fixture-family route |
| owner | proof-infra fixture-family part or comparison-spine part |
| next route | `mechanics/proof-infra/parts/fixture-families/fixtures/` or comparison-spine fixture parts |
| tools | root validator and semantic AGENTS validator |
| validation | this card's `Validation` section |

## Route Rules

Keep each shared family weaker than the bundle-local EVAL.md meaning it supports.
Preserve replacement guidance so another repo can keep the bounded claim surface when cases are swapped.
When a bundle points here, keep `shared_fixture_family_path` explicit and use `additional_shared_fixture_family_paths` only for real secondary reusable families.
When a bundle points to a mechanic-local fixture family, keep the part-local
path explicit and route old root path lineage through the owning mechanic.
Route new generic shared fixture families through `mechanics/proof-infra/`
first; route domain-specific families through the active owning mechanic.
Keep reusable fixture families reviewable without private context, and keep
bundle-local `EVAL.md` meaning stronger than the shared family name.
Secret-bearing logs, hidden benchmark dumps, and private telemetry stay out of
this public fixture route.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
