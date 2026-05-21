# Scorers Route

This directory is the compatibility route card for historical shared scorer
helper paths.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root scorer helper routing |
| entry | open when an old root scorer path appears or a shared scorer helper needs an owner |
| input | scorer helper, report helper, transition-note helper, integrity-risk helper, or old root scorer reference |
| output | proof-infra reportable-contract scorer route or owning mechanic helper route |
| owner | `scorers/AGENTS.md` for route law; proof-infra reportable-contracts for the active shared helper |
| next route | `mechanics/proof-infra/parts/reportable-contracts/scorers/` |
| validation | `scorers/AGENTS.md` and proof-infra route checks |

The active shared scorer helper now lives at:

`mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`

The current helper is intentionally small:
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py` builds repeatable breakdown payloads for workflow, artifact, comparative, and integrity reports
- it now also provides shared transition-note and integrity-risk payload helpers for repeated-window and sidecar reports

Use [AGENTS.md](AGENTS.md) for scorer helper rules and old-path lineage.
