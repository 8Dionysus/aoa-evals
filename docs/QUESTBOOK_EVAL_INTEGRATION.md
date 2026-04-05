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

## Installed quest-harvest posture

`aoa-quest-harvest` may assist this repo only as a post-session installed skill after a reviewed run, closure, or pause.

- it is not used inside an active route
- it does not define orchestrator identity
- it does not replace eval bundle meaning, playbook route canon, or memo ownership
- one anecdotal repeat is not enough to promote a proof pattern

Its allowed verdicts are:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Generated quest surfaces

The live generated quest catalog and dispatch surfaces are repo-local review and validation projections.
The matching example files remain versioned example-only surfaces and example mirrors.
Neither pair is a live portable verdict authority, and both surfaces are explicitly not live portable verdict authority for public proof claims.
Neither pair replaces eval bundle meaning.

Example-only progression surfaces may cite upstream read-only refs such as `AOA-SK-Q-0003`.
Those references stay source-owned upstream and do not widen this rollout into `aoa-skills`.

## Manual-first pilot lane

- `AOA-EV-Q-0002` closed one source/proof review lane by anchoring the surviving proof question in `EVAL_INDEX.md` and `docs/COMPARISON_SPINE_GUIDE.md`.
- No live routing consumer, dispatch input, or quest builder was introduced for this pass.
- The result is bounded proof alignment, not a new verdict authority layer.
