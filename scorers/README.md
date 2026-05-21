# Scorers Route

This directory is a compatibility route card for shared bounded helpers.

The active shared scorer helper now lives at:

`mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`

The current helper is intentionally small:
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py` builds repeatable breakdown payloads for workflow, artifact, comparative, and integrity reports
- it now also provides shared transition-note and integrity-risk payload helpers for repeated-window and sidecar reports

Use [AGENTS.md](AGENTS.md) for scorer helper rules and old-path lineage.
