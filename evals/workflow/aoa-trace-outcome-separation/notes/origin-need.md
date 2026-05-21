# Origin Need

`aoa-bounded-change-quality` already exposed outcome quality and path quality as nearby workflow concerns,
but it remained a `composite` workflow surface.

That made it useful for answering:
- did the bounded workflow hold together?

It did **not** isolate the narrower review question:
- when outcome quality and path quality diverge,
  can the workflow still be read honestly without letting one surface flatten the other?

`aoa-verification-honesty` and `aoa-scope-drift-detection` each do narrower jobs.
They can explain why a path note is weak,
but they do not provide the split surface that keeps outcome and path legible before any combined reading.

`aoa-trace-outcome-separation` exists to separate that split-reading question from nearby surfaces such as:
- pure verification truthfulness
- pure scope alignment
- pure tool-trajectory judgment
- broader composite workflow quality

This bundle is intentionally narrower than the composite workflow starter
but broader than any single root-cause diagnostic.
It should make outcome-vs-path divergence visible
without pretending there is one ideal trace for every case.
