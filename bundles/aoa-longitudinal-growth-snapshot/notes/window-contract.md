# Window Contract

Use this bundle only when the window sequence is:
- ordered
- named
- comparable on the same bounded workflow surface
- backed by one public report or summary artifact per window

Each window should preserve:
- the same anchor workflow surface
- comparable case meaning or declared replacement logic
- comparable verdict interpretation
- the same bounded workflow surface even when fixtures rotate within the declared window rules
- the same shared family `fixtures/repeated-window-bounded-v1/README.md`

Each window should disclose:
- reviewer changes if they materially affect reading
- environment or policy changes if they materially affect comparability
- case-family drift if it exists at all
- one `context_note` that acts as the comparability disclosure for that window
- one `transition_note` that explains the bounded movement relative to the previous named window

Treat style-only or report-only movement as:
- `no clear directional movement`
- or `mixed or unstable movement`

unless the bounded workflow evidence itself also moved.

Keep the current materialized repeated-window proof flow aligned with:
- `fixtures/repeated-window-bounded-v1/README.md`
- `reports/example-report.json`
- `reports/repeated-window-proof-flow-v1.md`
- `reports/repeated-window-proof-flow-v2.md`
- `aoa-eval-integrity-check` as the integrity sidecar whenever public movement wording, routing, or maturity posture changes materially

