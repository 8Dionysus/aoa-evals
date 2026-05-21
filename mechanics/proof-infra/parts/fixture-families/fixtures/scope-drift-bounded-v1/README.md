# scope-drift-bounded-v1

Shared fixture family for `aoa-scope-drift-detection`.

Use this family when the bounded question is whether requested scope stayed
aligned with executed scope, or whether deviation remained explicitly visible
instead of being laundered into a neat success report.

Canonical case archetypes:
- exact-scope case with nearby-cleanup temptation
- silent widening case
- silent narrowing or under-delivery case
- reshaping-into-different-plausible-task case
- disclosed deviation case

Family invariants:
- the requested scope is visible enough for a bounded outside reviewer
- the executed scope can be reconstructed from the visible change surface
- widening, narrowing, and reshaping remain distinct drift classes
- explicit deviation stays distinguishable from silent drift
- the public readout remains weaker than the inspectable request-versus-execution evidence

Replacement boundary:
- local repos may replace the concrete cases only if they preserve the same
  scope-drift question and still exercise all five bounded drift pressures above
- replacements must stay public-safe and must not depend on hidden reviewer-only
  context to determine what was actually requested
