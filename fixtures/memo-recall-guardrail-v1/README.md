# memo-recall-guardrail-v1

Shared fixture family for `aoa-memo-recall-integrity`.

Use this family when the bounded question is whether a memo consumer can use
explicit inspect/capsule/expand recall paths without hiding precision,
provenance, or staleness posture.

Canonical case archetypes:
- inspect-beats-expand precision case
- provenance-thread-visible capsule case
- stale-or-withdrawn lifecycle honesty case
- thin-grounding stronger-source escalation case
- compact-surface false-authority pressure case

Family invariants:
- the explicit read path stays visible as inspect, capsule, expand, or
  stronger-source escalation
- provenance-thread or stronger-source posture remains inspectable per case
- stale, superseded, or retracted memory remains visibly non-current
- compact memo surfaces stay weaker than proof or canon claims
- stronger-source escalation remains available when memo grounding is thin

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  recall-integrity question and still exercise all five bounded pressures above
- replacements must stay public-safe and must not depend on hidden search,
  ranking, or private runtime recall behavior
