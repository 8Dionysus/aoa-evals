# Documentation Map

This file is the human and agent entrypoint for the `docs/` surface. It helps a
reader choose the next source without guessing from filenames.

Operational edit law belongs in the nearest `AGENTS.md`. This map explains where
meaning lives and which surface to open next.

## First Route

Choose by question:

| Question | Open |
| --- | --- |
| What is this repository? | [aoa-evals Bounded Proof Canon](../README.md) |
| Where am I in the agent index chain? | [Agent Index](AGENT_INDEX.md) |
| What is the proof-system shape? | [Design](../DESIGN.md), [Agent Surface Design](../DESIGN.AGENTS.md), [Architecture](ARCHITECTURE.md) |
| Which authority class owns this artifact? | [Proof Topology](PROOF_TOPOLOGY.md) |
| Is this name active, legacy, accepted input, generated projection, or candidate vocabulary? | [Legacy Naming](LEGACY_NAMING.md) |
| Which proof operation owns this route? | [Mechanics Operation Atlas](../mechanics/README.md) |
| Why was this route chosen? | [Decision Records Index](decisions/README.md) |
| What should happen next? | [Proof Direction Roadmap](../ROADMAP.md), [Questbook Obligation Index](../QUESTBOOK.md), [Quest Source Records](../quests/README.md), [Quest Lifecycle Contract](../quests/LIFECYCLE.md) |
| Which eval should I inspect? | [Eval Bundle Selection Chooser](../EVAL_SELECTION.md), [Eval Bundle Index](../EVAL_INDEX.md) |

The first concrete source-owned proof surface remains
[First starter bundle](../evals/workflow/aoa-bounded-change-quality/EVAL.md).

Maintained agent lane routing is outside `docs/`:
[Agent District](../.agents/AGENTS.md) and
[Spark Lane](../.agents/spark/AGENTS.md).

## Surface Classes

### Source Proof Meaning

Use these when a claim, verdict, fixture, or interpretation boundary matters:

- [First starter bundle](../evals/workflow/aoa-bounded-change-quality/EVAL.md)
- [Bundle Source Index](../evals/README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Eval Rubric](EVAL_RUBRIC.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)

### Generated Reader Surfaces

These route back to authored proof sources and generated data. They make
navigation compact; they do not replace `evals/**/EVAL.md` or
`evals/**/eval.yaml`.

- [Generated Reader Index](../generated/README.md)
- [Eval Bundle Selection Chooser](../EVAL_SELECTION.md)
- [Eval Bundle Index](../EVAL_INDEX.md)
- `generated/eval_catalog.json`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`
- [Generated Eval Report Index](../generated/eval_report_index.min.json)
  (`generated/eval_report_index.min.json`)
- `generated/comparison_spine.json`

### Topology And Route Maps

Open these before moving files, strengthening artifacts, or changing route
ownership:

- [Proof Topology](PROOF_TOPOLOGY.md)
- [Agent Index](AGENT_INDEX.md)
- [Legacy Naming](LEGACY_NAMING.md)
- [Mechanics Operation Atlas](../mechanics/README.md)
- [Proof Object Mechanic](../mechanics/proof-object/README.md)
- [Proof Loop Mechanic](../mechanics/proof-loop/README.md)
- [Comparison Spine Mechanic](../mechanics/comparison-spine/README.md)
- [Proof Infra Mechanic](../mechanics/proof-infra/README.md)
- [Publication Receipts Mechanic](../mechanics/publication-receipts/README.md)
- [Release Support Mechanic](../mechanics/release-support/README.md)
- [Boundary Bridge Mechanic](../mechanics/boundary-bridge/README.md)
- [Audit Mechanic](../mechanics/audit/README.md)
- [Agon Mechanic](../mechanics/agon/README.md)
- [Titan Mechanic](../mechanics/titan/README.md)

### Portability And Boundary Guides

Use these when an eval needs to stay portable, comparable, and honest about its
limits:

- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
- [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
- [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
- [Regression Proof Surfaces](REGRESSION_PROOF_SURFACES.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)

### Bridge And Candidate Evidence Surfaces

Use these when runtime, trace, receipt, sibling, recurrence, or checkpoint
artifacts need to feed an eval without becoming stronger than bundle-local
review:

- [Trace Eval Bridge](../mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md)
- [Trace Eval Bridge Chaos Wave 1](../mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md)
- [Runtime Integrity Review](../mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md)
- [Runtime Bench Promotion Guide](../mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md)
- [Eval Result Receipt Guide](../mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md)
- [Sibling Proof References](../mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md)
- [Orchestrator Proof Anchors](../mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md)
- [Self-Agent Checkpoint Eval Posture](../mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md)
- [Recurrence Proof Program](../mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md)

## Mechanic And Evidence Anchors

These links are here for discoverability. Their owning mechanics define the
operating context.

- [Proof Loop Local Route Smoke](../mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md)
- [First Proof Loop Bundle-Local Report](../evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json)
- [Receipt Intake Dry Review](../mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json)
- [Release Support Readiness Audit](../mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json)
- [Strategic Closeout Audit](../mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json)
- [Release Prep PR Handoff](../mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json)
- `../mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json`
- `../mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json`
- `../mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`

## Recommended Reading Paths

### New Reader Path

1. [aoa-evals Bounded Proof Canon](../README.md)
2. [Agent Index](AGENT_INDEX.md)
3. [First starter bundle](../evals/workflow/aoa-bounded-change-quality/EVAL.md)
4. [Eval Bundle Selection Chooser](../EVAL_SELECTION.md)
5. [Eval Bundle Index](../EVAL_INDEX.md)
6. [Eval Philosophy](EVAL_PHILOSOPHY.md)
7. [Architecture](ARCHITECTURE.md)

### Reviewer Path

1. [Eval Rubric](EVAL_RUBRIC.md)
2. [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
3. [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
4. one eval bundle plus its `notes/`
5. [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
6. [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

### Eval Author Path

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

### Mechanics Refactor Path

1. [Proof Topology](PROOF_TOPOLOGY.md)
2. [Agent Index](AGENT_INDEX.md)
3. [Mechanics Operation Atlas](../mechanics/README.md)
4. parent `README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md`
5. local part `README.md`
6. nearest `AGENTS.md`
7. [Decision Records Index](decisions/README.md)

### Release And Handoff Path

1. [Releasing `aoa-evals`](RELEASING.md)
2. [Release Support Mechanic](../mechanics/release-support/README.md)
3. [Release Support Readiness Audit](../mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json)
4. [Strategic Closeout Audit](../mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json)
5. [Release Prep PR Handoff](../mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json)

## Selection Notes

- Prefer generated reader surfaces when the question is "which eval should I
  inspect next?"
- Prefer one concrete `EVAL.md` bundle when the question is "where is the
  source-owned proof meaning for this claim?"
- Prefer [Proof Object Mechanic](../mechanics/proof-object/README.md) for bundle
  source, manifest metadata, status posture, generated readers, and
  bundle-local review.
- Prefer [Proof Loop Mechanic](../mechanics/proof-loop/README.md) for one proof
  question moving from selection to reviewed report or receipt.
- Prefer [Publication Receipts Mechanic](../mechanics/publication-receipts/README.md)
  for optional eval-result receipts inside a stats-event-envelope.
- Prefer [Release Support Mechanic](../mechanics/release-support/README.md) for
  bounded release scope, changelog narrative, release audit, Repo Validation,
  tag, and release notes.
- Prefer [Legacy Naming](LEGACY_NAMING.md) when a name may be active topology,
  historical lineage, accepted input, generated projection, or candidate-only
  vocabulary.

The current runtime path is:

`pick -> inspect -> expand -> object use`

## Validation Route

Executable commands for docs-map or docs-owned proof-meaning changes live in
[docs/AGENTS.md#validation](AGENTS.md#validation) and the nearest owner route
card. Generated reader parity routes through
[generated/AGENTS](../generated/AGENTS.md), while mechanic-owned payload docs
route through [mechanics/AGENTS](../mechanics/AGENTS.md) and the package card.
