# QUESTBOOK integration - aoa-evals

## Purpose

This note shows how `QUESTBOOK.md` fits into `aoa-evals` as the public tracked surface for deferred proof obligations.

## Role split

- eval bundles remain the source of eval meaning
- indexes and selection docs remain public navigation and proof surfaces
- `QUESTBOOK.md` holds deferred obligations that survive the current bounded diff
- proof/regression/verdict-bridge boundaries stay explicit and reviewable
- caution notes, blind spots, and repeated-window discipline should become reusable only when they recur enough to deserve stable IDs

## Good anchors in this repo

Use stable anchors such as:
- `EVAL_INDEX.md`
- `docs/COMPARISON_SPINE_GUIDE.md`
- `docs/TRACE_EVAL_BRIDGE.md`
- `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`

## Initial posture

A good eval quest normally points to:
- a missing proof surface
- a regression or comparison seam
- a trace-to-verdict bridge debt
- a repeated caution pattern that wants canon instead of duplicated prose

## Example-only surfaces

The generated quest catalog and dispatch examples are versioned example-only surfaces.
They support review and validation, but they are not live portable verdict authority.

## Manual-first pilot lane

- `AOA-EV-Q-0002` closed one source/proof review lane by anchoring the surviving proof question in `EVAL_INDEX.md` and `docs/COMPARISON_SPINE_GUIDE.md`.
- No live routing consumer, dispatch input, or quest builder was introduced for this pass.
- The result is bounded proof alignment, not a new verdict authority layer.
