# Comparison Contract

Use this draft bundle only when the baseline target and comparison surface are explicit.

- baseline target: `sanitized local runtime baseline variant`
- comparison mode: `fixed-baseline`
- latency metric semantics must be named before the verdict
- resource-use metric semantics must be named before the verdict
- noisy variation must stay weaker than a comparative verdict
- style-only or presentation-only changes must not become capability movement
- resource tradeoffs must stay separate from reasoning quality claims

Public summary discipline:
- keep the baseline target visible in every comparative report
- keep matched conditions and fixture boundaries visible before the verdict
- keep latency movement and resource movement in separate report fields
- keep candidate evidence below bundle-local review until accepted
- do not overread one runtime comparison as a broad agent-quality claim
