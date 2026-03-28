# witness-trace-v1

Shared fixture family for `aoa-witness-trace-integrity`.

Use this family when the bounded question is whether a public witness artifact
stayed reviewable enough for downstream memo or compost use without pretending
runtime telemetry is already complete.

Canonical case archetypes:
- visible tool-use case
- explicit `state_delta` case
- partial-failure-preserved case
- redaction-required-but-reviewable case
- markdown-summary-overclaim pressure case

Family invariants:
- the public trace keeps meaningful steps visible enough to reconstruct the route
- tool use is named when it materially shaped the bounded run
- external effects are explicit as `state_delta` rather than hidden in prose
- failures leave a partial witness instead of disappearing behind polish
- redaction protects payloads without erasing route reviewability
- the markdown summary stays weaker than the trace rather than stronger

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  witness-integrity question and still exercise all five bounded trace
  pressures above
- replacements must stay public-safe for an outside reviewer and must not
  require hidden runtime-only telemetry
