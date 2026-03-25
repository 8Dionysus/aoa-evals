# RUNTIME BENCH PROMOTION GUIDE

This guide defines how `abyss-stack` runtime benchmark artifacts may become bounded evidence surfaces in `aoa-evals`.

Use it when a runtime benchmark looks useful, but you still need to decide whether it should stay local, travel as a selected sidecar, or begin to harden into a portable proof surface.

See also:
- [Documentation Map](README.md)
- [Trace Eval Bridge](TRACE_EVAL_BRIDGE.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)

## Core rule
`aoa-evals` may read selected runtime benchmark evidence from `abyss-stack`.

It remains the owner of:
- bounded claim wording
- comparison semantics
- verdict logic
- interpretation guidance
- portability review

It does not ingest:
- raw uncurated dumps
- secret-bearing rendered config
- host-private material that cannot travel safely
- vague leaderboard claims

## Promotion target classes
Use one of these target classes:
- `local-only` — useful inside `abyss-stack`, not ready to travel
- `evidence-sidecar` — selected runtime evidence can accompany another bounded eval surface
- `bundle-candidate` — the runtime claim is stable enough to begin authoring or extending a portable comparative bundle

## What runtime evidence may honestly support
Good bounded claim shapes:
- under matched host and fixture conditions, variant B lowers p95 first-token latency relative to variant A
- under matched restart conditions, backend X recovers more reliably than backend Y
- under matched context-stress cases, this profile remains stable up to N tokens before visible failure

Bad claim shapes:
- model X is smarter
- backend Y is the best
- this latency win proves better agent quality
- this proves general reasoning growth

## Promotion floor
Before promotion, keep explicit:
- source manifest refs
- manifest schema ref
- benchmark family
- comparison mode
- environment invariants
- environment deltas
- selected evidence only
- do-not-overread notes
- human review required

If those surfaces are missing, the evidence is still local-shaped.

## Comparison hygiene
### `fixed-baseline`
Use when one candidate run is being compared against one frozen baseline run on the same bounded runtime surface.

Keep stable:
- host class
- benchmark family
- fixture family
- metric semantics
- timeout and retry posture

### `peer-compare`
Use when two variants are compared side by side under matched conditions, and neither side is the default truth source.

Keep explicit:
- what is matched
- what changed
- what stays noisy
- why the read is not a ranking claim

### `longitudinal-window`
Use when ordered named windows stay on one bounded runtime surface.

Keep explicit:
- named windows
- one stable benchmark family
- one stable fixture family or replacement contract
- environment notes that affect comparability

If the proof job changed between windows, do not call the sequence a clean movement story.

## What stays out of `aoa-evals`
Do not promote:
- raw dumps
- secret-bearing rendered config
- private host fingerprints
- dashboards with no bounded claim text
- one flattering prompt or one lucky run
- metrics with no interpretation boundary

## Promotion reading discipline
Treat promoted runtime evidence as support for bounded runtime posture only.

Do not read it as:
- a global model ranking
- a capability ranking
- proof of reasoning quality
- proof that an agent workflow improved unless another bounded eval surface says so

## Hook surface
Use `../schemas/runtime-evidence-selection.schema.json` as the machine-readable selection contract.

Use `../examples/runtime_evidence_selection.workhorse-local.example.json` as the first bounded example.

## Boundary to preserve
Runtime posture can become evidence.

It does not become proof canon until `aoa-evals` gives it bounded meaning.
