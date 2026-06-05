# RUNTIME BENCH PROMOTION GUIDE

This guide defines how `abyss-stack` runtime benchmark artifacts may become bounded evidence surfaces in `aoa-evals`.

Use it when a runtime benchmark looks useful, but you still need to decide whether it should stay local, travel as a selected sidecar, or begin to harden into a portable proof surface.

See also:
- [Documentation Map](../../../../../docs/README.md)
- [Trace Eval Bridge](../../artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md)
- [Portable Eval Boundary Guide](../../../../../docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Baseline Comparison Guide](../../../../../docs/guides/BASELINE_COMPARISON_GUIDE.md)

## Core rule
`aoa-evals` may read selected runtime benchmark evidence from `abyss-stack`.

It remains the owner of:
- bounded claim wording
- comparison semantics
- verdict logic
- interpretation guidance
- portability review

Raw dumps, secret-bearing rendered config, host-private material, and vague
leaderboard claims stay with the runtime or source owner until curated into a
public-safe packet.

## Promotion target classes
Use one of these target classes:
- `local-only` — useful inside `abyss-stack`, stays local until travel-ready
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
- memory-context boundary when the packet reads memo recall, contradiction, or
  writeback context
- overread-routing notes
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
- where ranking pressure routes

### `longitudinal-window`
Use when ordered named windows stay on one bounded runtime surface.

Keep explicit:
- named windows
- one stable benchmark family
- one stable fixture family or replacement contract
- environment notes that affect comparability

If the proof job changed between windows, route the sequence through replacement
contract review before telling a movement story.

## Owner Route For Weak Evidence

| Evidence pressure | Route |
| --- | --- |
| raw dumps | runtime owner selection first |
| secret-bearing rendered config | source owner sanitization first |
| private host fingerprints | operator-owned reduction first |
| dashboards missing bounded claim text | benchmark owner writes the bounded claim first |
| one flattering prompt or one lucky run | repeatable fixture or comparison owner review |
| metrics missing an interpretation boundary | eval interpretation review before promotion |

## Promotion reading discipline
Treat promoted runtime evidence as support for bounded runtime posture only.

Route broader readings this way:

| Reading pressure | Route |
| --- | --- |
| global model ranking | comparison owner and explicit ranking contract |
| capability ranking | bounded capability eval owner |
| proof of reasoning quality | reasoning-quality eval surface with its own evidence |
| agent workflow improvement | workflow eval surface that names the improved behavior |

## Hook surface
Use `../schemas/runtime-evidence-selection.schema.json` as the machine-readable selection contract.

Use `../examples/runtime_evidence_selection.workhorse-local.example.json` as the first bounded example.
Use `../examples/runtime_evidence_selection.return-anchor-integrity.example.json`
when selected `runtime_return_event` summaries and return-policy notes need to
travel upward as a bounded evidence sidecar for `aoa-return-anchor-integrity`.
Use `../examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json`
when selected runtime memo-export packets need to travel upward as a bounded
evidence sidecar for `aoa-memo-recall-integrity` on the Phase Alpha rerun seam.
Use `../examples/runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json`
and `../examples/runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json`
when selected runtime memo-export packets need to stay contradiction-visible
without turning lifecycle context into source truth.
Use `../examples/runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json`
when selected Phase Alpha runtime closure packets need to travel upward as a
bounded evidence sidecar for `aoa-memo-writeback-act-integrity` on the
runtime-to-memo writeback seam.
Use `../examples/runtime_evidence_selection.runtime-chaos-window.example.json`
when curated chaos-wave receipts and reviewed closeout examples should travel
upward only as example-backed sidecar evidence for `aoa-stress-recovery-window`.

## Boundary to preserve
Runtime posture can become evidence after bounded selection.

Proof-canon pressure routes through `aoa-evals` bounded meaning review. Until
that review happens, runtime evidence-selection packets stay candidate surfaces
with owner-review refs.

Memo-context packets also keep `memory_context_boundary` visible. That boundary
routes provenance, freshness, retention, and permission pressure to `aoa-memo`
and forbids reading selected memory context as tool authorization, durable
writeback approval, source truth, private/stale-context proof, or a local memo
port.
