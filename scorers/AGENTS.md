# AGENTS.md

## Role

`scorers/` is a compatibility route card for shared bounded helpers for
reportable proof artifacts.

## Current surface

Active scorer payload:

- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for shared bounded scorer helpers |
| input | scorer helper lookup, old root scorer reference, or bounded report helper support need |
| output | proof-infra reportable-contract scorer route |
| owner | `mechanics/proof-infra/parts/reportable-contracts/` |
| next route | `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py` |
| tools | root validator and semantic AGENTS validator |
| validation | this card's `Validation` section |

## Route Rules

Shared helpers may format or normalize bounded breakdowns, but they must remain reviewable enough for outside inspection.
Bundle-local meaning in EVAL.md stays stronger than scorer helper output.
Generic score output requires explicit bundle-level interpretation.
Preserve helper support for transition-note and integrity-risk payloads when editing repeated-window or sidecar-related logic.
Active root scorer helper aliases route through proof-infra provenance and the
active part-local surface.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
