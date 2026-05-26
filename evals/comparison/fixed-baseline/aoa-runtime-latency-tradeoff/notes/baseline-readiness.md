# Baseline Readiness

This draft uses `fixed-baseline`, so baseline discipline must be explicit.

Minimum bounded baseline conditions:
- the named baseline target remains `sanitized local runtime baseline variant`
- baseline and candidate evidence use matched fixture conditions
- comparison inputs are public-safe or sanitized before review
- host class, preset, timeout, retry, and metric semantics are stated without
  exposing private host fingerprints or raw configuration dumps
- noisy variation and style-only differences stay weaker than the verdict
- reviewer notes separate latency, resource use, and behavioral-quality claims

This note does not approve the bundle for baseline status. It records the draft readiness gates.
