# Shared Scorers

This directory is a compatibility route card for shared bounded helpers.

The active shared scorer helper now lives at:

`mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`

Shared scorer helpers should:
- format or normalize bounded breakdowns
- stay readable enough for outside review
- never outrank bundle-local meaning in `EVAL.md`
- avoid turning bounded proof into one generic score

The current helper is intentionally small:
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py` builds repeatable breakdown payloads for workflow, artifact, comparative, and integrity reports
- it now also provides shared transition-note and integrity-risk payload helpers for repeated-window and sidecar reports

Do not recreate active root scorer helper aliases here. Route old root path
lineage through `mechanics/proof-infra/PROVENANCE.md`; the owning legacy
archive explains itself after that bridge.
