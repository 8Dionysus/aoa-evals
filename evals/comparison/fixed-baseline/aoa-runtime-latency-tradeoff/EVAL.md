---
name: aoa-runtime-latency-tradeoff
category: comparative
status: draft
summary: Checks whether a runtime comparison preserves a bounded latency and resource-use
  tradeoff claim without overreading it as reasoning quality, agent behavior, or cross-host
  performance.
object_under_evaluation: runtime latency and resource-use tradeoff under matched fixture
  conditions
claim_type: comparative
baseline_mode: fixed-baseline
report_format: comparative-summary
technique_dependencies: []
skill_dependencies: []
comparison_surface:
  shared_family_path: mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md
  paired_readout_path: mechanics/comparison-spine/parts/fixed-baseline/reports/runtime-latency-tradeoff-proof-flow-v1.md
  integrity_sidecar: aoa-eval-integrity-check
  anchor_surface: aoa-local-text-contract-fit
  baseline_target_label: sanitized local runtime baseline variant
  selection_question: Do you need a fixed-baseline route for runtime latency and resource-use
    tradeoffs under matched fixture conditions?
---

# aoa-runtime-latency-tradeoff

## Intent

Use this eval to check whether a local runtime variant comparison can support
a bounded latency and resource-use tradeoff claim under matched fixture
conditions.

This draft bundle exists because runtime benchmark pressure can be valuable
without being safe to publish raw. It turns a selected, sanitized runtime
candidate into a reviewable fixed-baseline proof route.

The goal is not to crown a runtime, model, host, or agent.
The goal is to test one bounded claim:

under matched host class, preset, fixture, timeout, and metric semantics, one
local runtime variant may show lower chosen latency while carrying a visible
resource-use cost.

This bundle remains diagnostic until bundle-local review accepts specific
public-safe evidence.

## Object under evaluation

This eval checks runtime latency and resource-use tradeoff under matched
fixture conditions.

Primary surfaces under evaluation:
- the named baseline runtime variant and candidate runtime variant
- latency metric semantics, such as p95 first-token latency, kept stable across
  the comparison
- resource-use metric semantics, such as visible accelerator memory pressure,
  kept separate from latency
- matched fixture, preset, timeout, retry, and host-class assumptions
- whether the comparative summary preserves the tradeoff instead of flattening
  it into a winner story

Nearby surfaces intentionally excluded:
- reasoning quality
- agent behavior quality
- global model ranking
- host or hardware leaderboard claims
- runtime health outside the named comparison window
- raw private benchmark artifact publication

## Bounded claim

This eval is designed to support a claim like:

under these matched fixture conditions, the candidate runtime variant shows a
lower chosen latency reading than the named baseline while using more of the
tracked resource budget.

The claim must stay a runtime tradeoff claim only.

This eval does **not** support claims such as:
- the candidate reasons better
- the agent behaves better end to end
- the candidate is globally faster across hosts
- the model, backend, or quantization is generally best
- the private runtime evidence is now public proof by itself

## Trigger boundary

Use this eval when:
- a runtime candidate compares local runtime variants under matched fixture conditions
- the claim is about latency and resource use rather than reasoning quality
- selected raw runtime artifacts need a public-safe eval route before review
- an owner wants to preserve a tradeoff lesson without copying private logs,
  rendered configs, host fingerprints, or raw device samples

Do not use this eval when:
- `aoa-local-text-contract-fit` is the real question because output-shape
  contract fit, not runtime tradeoff, is under review
- `aoa-regression-same-task` is sufficient because the comparison is a workflow
  regression claim rather than runtime metric hygiene
- raw runtime evidence has not been reduced to a selected public-safe candidate
  packet
- the pressure is still only a quest obligation
- the result is meant to rank reasoning quality, agent quality, hosts, or
  hardware tiers

## Inputs

- named baseline runtime variant
- named candidate runtime variant
- public-safe selected evidence packet or sanitized candidate ref
- matched fixture family and case identifiers
- latency metric definition and aggregation window
- resource-use metric definition
- environment invariants and environment deltas stated at review level
- bundle-local reviewer judgment

Candidate evidence refs:
- private-runtime-candidate:sanitized-local-runtime-latency-tradeoff

Quest refs:
- no quest refs named

## Fixtures and case surface

The initial fixture contract lives at `fixtures/contract.json`.

A strong public-safe fixture family should include:
- repeatable prompts or requests shared by baseline and candidate
- stable preset, timeout, retry, and warmup posture
- metric labels that remain comparable across both sides
- enough case-level notes to distinguish latency movement from resource cost
- a replacement rule for local repos that need different prompts without
  changing the comparison meaning

Fixture families should avoid:
- secret-bearing prompts or rendered configs
- raw private log paths
- host fingerprints or exact hardware identity
- one flattering prompt treated as a general runtime result
- latency-only summaries that hide resource deltas

## Scoring or verdict logic

This draft uses a comparative verdict with per-case comparison notes.

Canonical comparative readings:
- `baseline stronger`
- `candidate stronger`
- `mixed tradeoff signal`
- `noisy variation`
- `not reviewable`

For this bundle, `candidate stronger` should be rare. Lower latency with higher
resource use is usually a `mixed tradeoff signal` unless the accepted review
contract explicitly says the resource cost remains inside the allowed budget.

Per-case review should ask:
- did both variants run under the same fixture and preset assumptions?
- is the latency metric defined the same way on both sides?
- is the resource-use metric visible and separated from latency?
- is the difference larger than noisy variation for the named metric?
- does the summary preserve the tradeoff rather than implying general quality?

## Baseline or comparison mode

This draft uses `fixed-baseline`.

The baseline target label is `sanitized local runtime baseline variant`.
The comparison surface is anchored near `aoa-local-text-contract-fit` because
runtime tradeoff evidence is useful only after local text-lane contract-fit
pressure stays distinct from speed pressure.

The fixed baseline is acceptable only when:
- baseline and candidate use the same public-safe fixture family
- metric semantics are stable across both variants
- host-class, preset, timeout, and retry posture are named at review level
- environment deltas are visible and do not silently change the proof job
- resource use remains a first-class reading, not an appendix

## Execution contract

A careful run should:
1. reduce raw runtime evidence into a selected public-safe packet
2. name the baseline target and candidate target
3. confirm matched fixture, preset, timeout, retry, and metric semantics
4. capture latency and resource-use readings separately
5. write per-case comparative notes before the bundle-level verdict
6. reject or defer evidence that leaks private runtime artifacts
7. publish only a bounded comparative summary after bundle-local review

Do not treat scaffold creation as runtime evidence acceptance.

## Outputs

- one bundle-level comparative verdict
- per-case baseline and candidate notes
- named baseline target
- latency movement summary
- resource-use movement summary
- noisy-variation notes where the difference is too thin
- evidence acceptance or rejection notes after review
- optional schema-backed report at `reports/example-report.json`

## Failure modes

- duplicate bundle for an existing proof surface
- runtime evidence accepted before bundle-local review
- vague quest pressure promoted too early
- scaffold text mistaken for proof
- latency improvement summarized as reasoning improvement
- resource cost hidden behind a winner label
- private paths, raw logs, rendered configs, or device samples copied into the
  public bundle
- host-specific evidence overread as a cross-host leaderboard

## Blind spots

This eval does not prove:
- reasoning quality ranking
- better agent behavior
- cross-host leaderboard placement
- general runtime health
- public proof status for private runtime artifacts
- that the named resource tradeoff is acceptable for a specific deployment

## Interpretation guidance

Treat any future positive result as support for one bounded runtime tradeoff
claim.

Do not treat a positive result as:
- evidence acceptance without bundle-local review
- a runtime health verdict
- a public starter recommendation
- proof that neighboring evals are unnecessary
- proof that speed repaired an output-contract, workflow, or reasoning miss

## Verification

- confirm the bounded claim is explicit
- confirm existing eval routes were inspected first
- confirm candidate evidence stayed candidate-only
- confirm origin need and integrity check evidence resolve publicly
- confirm the public bundle contains no raw private paths, rendered configs,
  host fingerprints, or raw device samples
- confirm latency and resource-use readings remain separate in every report
- run the proof-object validation lane before promotion

Source refs:
- mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md
- mechanics/proof-object/parts/eval-authoring/docs/EVAL_BIRTH_PROTOCOL.md

## Technique traceability

- none yet

## Skill traceability

- none yet

## Adaptation points

- local fixtures
- local runners
- bundle-local report schema
- candidate evidence review packets
