# Origin Need

`aoa-bounded-change-quality` already exposed scope drift as one nearby failure mode,
but it remained a `composite` workflow surface.

That made it useful for answering:
- did the bounded workflow hold together?

It did **not** isolate the narrower root-cause question:
- did the requested work surface still match the executed work surface,
  or was widening, narrowing, or reshaping disclosed explicitly enough to stay reviewable?

`aoa-verification-honesty` also does a different job.
It isolates whether verification claims matched executed evidence,
not whether the task surface itself drifted.

`aoa-scope-drift-detection` exists to separate that scope-alignment question from nearby surfaces such as:
- full workflow-quality collapse
- claimed-vs-actual verification evidence
- authority ambiguity

This bundle is intentionally narrower than the composite workflow starter
and distinct from the verification diagnostic starter.
It should make silent widening, narrowing, and reshaping visible
without pretending to answer the whole workflow question by itself.
