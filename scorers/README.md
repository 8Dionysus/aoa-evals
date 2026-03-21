# Shared Scorers

This directory stores shared bounded helpers for reportable proof artifacts.

Shared scorer helpers here should:
- format or normalize bounded breakdowns
- stay readable enough for outside review
- never outrank bundle-local meaning in `EVAL.md`
- avoid turning bounded proof into one generic score

The current helper is intentionally small:
- `bounded_rubric_breakdown.py` builds repeatable breakdown payloads for workflow, artifact, comparative, and integrity reports
