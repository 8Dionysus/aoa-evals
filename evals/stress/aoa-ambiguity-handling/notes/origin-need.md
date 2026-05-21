# Origin Need

`aoa-bounded-change-quality` already exposed ambiguity as one nearby failure mode,
but it remained a `composite` workflow surface.

That made it useful for answering:
- did the bounded workflow hold together?

It did **not** isolate the narrower root-cause question:
- did the agent handle incomplete, conflicting, or underspecified task meaning honestly,
  or did it silently choose one interpretation and present it as the original ask?

`aoa-approval-boundary-adherence` also does a different job.
It isolates authority and approval ambiguity,
not general task-meaning ambiguity.

`aoa-ambiguity-handling` exists to separate that task-meaning question from nearby surfaces such as:
- authority ambiguity
- later scope drift after execution begins
- broader workflow-quality collapse

This bundle is intentionally narrower than the composite workflow starter
and distinct from the approval-boundary starter.
It should make silent interpretation collapse visible
without pretending to answer the whole workflow question by itself.
