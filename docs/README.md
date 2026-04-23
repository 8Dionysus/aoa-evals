# Documentation Map

This file is the human-first entrypoint for the repository's `docs/` surface.

Use it when you want to understand **which doc to open next** without guessing from filenames alone.

## Start Here

Choose the path that matches your question:

- I need one concrete source-owned proof surface first:
  - [First starter bundle](../bundles/aoa-bounded-change-quality/EVAL.md)
- I need one bounded antifragility family read backed by owner-local receipts:
  - [AoA Antifragility Posture](../bundles/aoa-antifragility-posture/EVAL.md)
- I need one repeated-window stress recovery proof surface without turning routing or memo into stronger truth:
  - [AoA Stress Recovery Window](../bundles/aoa-stress-recovery-window/EVAL.md)
  - [Stress Recovery Window Evals](STRESS_RECOVERY_WINDOW_EVALS.md)
- I need one proof surface for stats-derived re-grounding without turning stats into proof:
  - [Stats Re-Grounding Boundary Integrity](../bundles/aoa-stats-regrounding-boundary-integrity/EVAL.md)
- I need to understand what this repository means by evaluation:
  - [Eval Philosophy](EVAL_PHILOSOPHY.md)
  - [Architecture](ARCHITECTURE.md)
- I need the current proof-layer direction and next growth lanes:
  - [Roadmap](../ROADMAP.md)
- I need to pick or inspect an eval bundle by routing surface:
  - [Eval Selection](../EVAL_SELECTION.md)
  - [Eval Index](../EVAL_INDEX.md)
- I need to understand status, review posture, or canonization:
  - [Eval Rubric](EVAL_RUBRIC.md)
  - [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- I need to understand score and verdict boundaries:
  - [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
  - [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
- I need one protocol integrity verdict for an experience bundle:
  - [Experience Protocol Integrity](../bundles/aoa-experience-protocol-integrity/EVAL.md)
- I need to understand how runtime artifacts and trace surfaces become eval evidence:
  - [Trace Eval Bridge](TRACE_EVAL_BRIDGE.md)
  - [Trace Eval Bridge Chaos Wave 1](TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md)
  - [Runtime Integrity Review](RUNTIME_INTEGRITY_REVIEW.md)
  - [Eval Result Receipt Guide](EVAL_RESULT_RECEIPT_GUIDE.md)
  - [Runtime Bench Promotion Guide](RUNTIME_BENCH_PROMOTION_GUIDE.md)
  - [Self-Agent Checkpoint Eval Posture](SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md)
  - [Recurrence Proof Program](RECURRENCE_PROOF_PROGRAM.md)
- I need to understand portability, fixtures, blind spots, or baseline comparison:
  - [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
  - [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
  - [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
  - [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
  - [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
  - [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
  - [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
  - [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)
- I need release process guidance:
  - [Releasing `aoa-evals`](RELEASING.md)

## Surface Types

### Generated reader surfaces

These are reader-facing navigation artifacts derived from authoritative markdown and generated data.
Use them after you know whether you need routing convenience or source-owned bundle meaning.
They do not replace `bundles/*/EVAL.md` and `bundles/*/eval.yaml`.

- [Eval Selection](../EVAL_SELECTION.md)
  - use when you need one bounded eval choice by category, status, claim type, or nearby relation
- [Eval Index](../EVAL_INDEX.md)
  - use when you need the current public eval map
- `generated/eval_catalog.json`
  - use when a reader or router needs the full derived catalog with dependency refs, relations, and evidence metadata
- `generated/eval_catalog.min.json`
  - use when a reader or router needs the thin projection surface for routing, indexing, and compact upstream proof-lineage
- `generated/eval_capsules.json`
  - use when a local runtime needs compact eval cards derived from bounded claim, trigger boundary, blind spots, interpretation guidance, and compact lineage signals
- `generated/comparison_spine.json`
  - use when a reader or router needs the filtered comparison-only ladder with mode-specific comparison contracts
- `generated/eval_sections.full.json`
  - use when a local runtime needs bounded section expansion from source-owned eval markdown without reopening the whole bundle blindly

### Authored review and governance guides

These are human-authored guides that define bounded review, score semantics, and publication discipline.

- [Eval Rubric](EVAL_RUBRIC.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
- [Releasing `aoa-evals`](RELEASING.md)

### Portability and boundary guides

These guides explain what makes an eval bundle portable, bounded, and honest about its limits.

- [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
- [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)

### Derived bridge surfaces

These surfaces explain how neighboring runtime artifacts and trace inputs can
feed existing eval bundles without creating a second proof canon.

- [Trace Eval Bridge](TRACE_EVAL_BRIDGE.md)
- [Trace Eval Bridge Chaos Wave 1](TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md)
- [Eval Result Receipt Guide](EVAL_RESULT_RECEIPT_GUIDE.md)
- [Self-Agent Checkpoint Eval Posture](SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md)
- [Recurrence Proof Program](RECURRENCE_PROOF_PROGRAM.md)
- `../examples/artifact_to_verdict_hook.*.example.json`
- `../examples/runtime_evidence_selection.*.example.json`
- `../examples/eval_result_receipt.example.json`

## Recommended Reading Paths

### New reader path

1. [README](../README.md)
2. [First starter bundle](../bundles/aoa-bounded-change-quality/EVAL.md)
3. [EVAL_SELECTION](../EVAL_SELECTION.md)
4. [EVAL_INDEX](../EVAL_INDEX.md)
5. [Eval Philosophy](EVAL_PHILOSOPHY.md)
6. [Architecture](ARCHITECTURE.md)

## Verify Current Surfaces

Use this non-mutating check path when you need to confirm current public and adjunct surfaces:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q tests
```

### Reviewer path

1. [Eval Rubric](EVAL_RUBRIC.md)
2. [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
3. [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
4. one eval bundle plus its `notes/`
5. [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
6. [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

### Eval author path

1. [Eval Philosophy](EVAL_PHILOSOPHY.md)
2. [Architecture](ARCHITECTURE.md)
3. [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
4. [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
5. [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
6. [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
7. [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
8. [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
9. [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
10. [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
11. [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
12. [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)

## Companion Repository Surfaces

These are outside `docs/` but matter when navigating the repo:

- [README](../README.md)
- [EVAL_INDEX](../EVAL_INDEX.md)
- [EVAL_SELECTION](../EVAL_SELECTION.md)
- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
- [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)
- `../reports/same-task-baseline-proof-flow-v1.md`
- `../reports/comparison-spine-proof-flow-v1.md`
- `../reports/artifact-process-paired-proof-flow-v2.md`
- `../reports/repeated-window-proof-flow-v1.md`
- `../reports/repeated-window-proof-flow-v2.md`
- [CONTRIBUTING](../CONTRIBUTING.md)
- [Eval Template](../templates/EVAL.template.md)

## Notes

- Prefer generated reader surfaces when the question is "which eval should I inspect next?"
- Prefer one concrete `EVAL.md` bundle when the question is "where is the source-owned proof meaning for this claim?"
- Prefer `generated/eval_catalog*.json` when the question is "what is the deterministic machine-readable eval surface right now?"
- Prefer `generated/eval_capsules.json` when the question is "what is the smallest local runtime card for this eval?"
- Prefer `generated/comparison_spine.json` when the question is "which comparison surface in the current ladder should I inspect next?"
- Prefer `generated/eval_sections.full.json` when the question is "which exact eval section should I expand next?"
- Prefer authored guides when the question is "what does this repo mean by this score, verdict, or boundary?"
- Prefer boundary guides when the question is "is this bundle really portable and honest enough to publish?"
- Prefer [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md) when the question is "which artifact/process surface should I read first, and where does the bridge stop?"
- Prefer [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md) when the question is "what makes repeated windows comparable enough for a bounded movement read?"
- Prefer [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md) when the question is "how do fixture, runner, scorer, and dossier contracts stay reusable without hiding meaning?"
- Prefer [Runtime Bench Promotion Guide](RUNTIME_BENCH_PROMOTION_GUIDE.md) when the question is "how can `abyss-stack` latency, load, recovery, or context-stress artifacts travel upward without becoming a fake capability ranking?"
- Prefer [Trace Eval Bridge](TRACE_EVAL_BRIDGE.md) when the question is "how do playbook artifacts, verification artifacts, or `WitnessTrace` sidecars become bounded eval evidence?"
- Prefer [Runtime Integrity Review](RUNTIME_INTEGRITY_REVIEW.md) when the question is "how should W10 runtime continuity evidence stay candidate-only and replay-bound before any later owner handoff?"
- Prefer [Eval Result Receipt Guide](EVAL_RESULT_RECEIPT_GUIDE.md) when the question is "how can one bounded eval publication be emitted as a machine-readable receipt without turning receipts into verdict authority or repo-global scoring?"
- It also explains why `aoa-evals` keeps a local mirror of the canonical shared envelope owned by `aoa-stats`.
- Prefer [Self-Agent Checkpoint Eval Posture](SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md) when the question is "how does `AOA-P-0006` close on the eval layer without inventing a new checkpoint-only proof canon?"
- Prefer [Recurrence Proof Program](RECURRENCE_PROOF_PROGRAM.md) when the question is "how does explicit return behavior become bounded proof without replacing scope, approval, verification, or restart-fidelity surfaces?"
- Treat the docs listed here as the canonical wording layer for future public bundle authoring.

The current runtime path is:

`pick -> inspect -> expand -> object use`
