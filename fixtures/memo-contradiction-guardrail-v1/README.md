# memo-contradiction-guardrail-v1

Shared fixture family for `aoa-memo-contradiction-integrity`.

Use this family when the bounded question is whether a memo consumer can use
lifecycle-aware object recall paths without flattening superseded, retracted,
or still-open contradictory memory into one smooth current story.

Canonical case archetypes:
- preferred-current claim with explicit contradiction refs
- superseded claim with visible replacement and historical posture
- retracted claim with withdrawn posture and audit walkback
- still-open tension case with no fake resolution
- smoothing-pressure case that should escalate to provenance or audit trace

Family invariants:
- the explicit read path stays visible as object inspect, capsule, expand,
  audit walkback, or provenance-thread walkback
- lifecycle `review_state` and `current_recall` posture remain inspectable per
  case
- superseded, withdrawn, and still-open contradictory states stay
  distinguishable rather than collapsing into generic staleness
- contradiction refs, replacement refs, and audit trace linkage remain
  reviewable when present
- lifecycle posture stays weaker than proof or final contradiction resolution

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  contradiction-integrity question and still exercise all five bounded
  pressures above
- replacements must stay public-safe and must not depend on hidden
  reconciliation logic, secret-bearing traces, or runtime-only conflict
  resolution
