# Origin Need

`aoa-bounded-change-quality` already exposed verification truthfulness as one nearby failure mode,
but it remained a `composite` workflow surface.

That made it useful for answering:
- did the bounded workflow hold together?

It did **not** isolate the narrower root-cause question:
- did the agent truthfully report which verification steps were executed, skipped, or blocked?

`aoa-verification-honesty` exists to separate that diagnostic question from nearby surfaces such as:
- scope drift
- summary dishonesty outside verification claims
- broader workflow-quality collapse

If the main question is requested-scope vs executed-scope alignment,
that should use `aoa-scope-drift-detection` instead.

This bundle is intentionally narrower than the composite starter.
It should make verification overstatement visible
without pretending to answer the full workflow question by itself.
