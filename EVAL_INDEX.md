# Eval Bundle Index

This file is the repository-wide agent-facing index of public eval bundles.

## Operating Card

| Field | Route |
|---|---|
| role | repository-wide agent-facing index of public eval bundles |
| input | public bundle inventory question, eval layer/status map question, category lookup, or starter-surface audit |
| output | bundle-local source route, layer route, generated reader route, or validation route |
| owner | `EVAL_INDEX.md` owns public starter-table and layer-index wording; bundle-local source files own claim meaning |
| next route | `EVAL_SELECTION.md`, selected `evals/**/EVAL.md`, `eval.yaml`, `generated/README.md`, or comparison/mechanic support routes |
| tools | generated catalog/readers, comparison spine reader, report index, and eval source validator |
| validation | [evals/AGENTS.md#validation](evals/AGENTS.md#validation) and root [AGENTS.md#verify](AGENTS.md#verify) |

## Starter eval bundles

| name | category | status | summary |
|---|---|---|---|
| aoa-bounded-change-quality | workflow | portable | Checks whether a non-trivial agent change holds together as one bounded end-to-end workflow signal, with precise diagnostic questions routed to narrower surfaces. |
| aoa-verification-honesty | workflow | portable | Checks whether an agent truthfully reports which verification steps on a bounded change task were executed, skipped, or blocked. |
| aoa-scope-drift-detection | boundary | bounded | Checks whether an agent keeps requested scope aligned with executed scope on bounded change tasks, or explicitly discloses deviation. |
| aoa-ambiguity-handling | stress | bounded | Checks whether an agent handles incomplete, conflicting, or underspecified task meaning on bounded change tasks with earned ask, branch, or bounded-assumption behavior visible. |
| aoa-approval-boundary-adherence | boundary | bounded | Checks whether an agent correctly distinguishes safe action, explicit-approval-required action, and out-of-bounds action. |
| aoa-trace-outcome-separation | workflow | bounded | Checks whether bounded change workflows remain reviewable when final outcome and execution-path quality stay separately readable before any combined reading; tool-path grading routes to its own bounded surface. |
| aoa-tool-trajectory-discipline | workflow | bounded | Checks whether an agent uses tools in a disciplined, reviewable way on bounded tasks where the tool path itself is the bounded claim. |
| aoa-antifragility-posture | stress | draft | Checks whether one owner-local surface handles a named stressor family through bounded degraded continuation, source-owned receipts, and split-axis readout while source ownership stays visible below proof and stats layers. |
| aoa-stress-recovery-window | longitudinal | draft | Checks whether ordered windows on one named stressor family show healthier handling with owner evidence outranking proof, stats, routing, and memo. |
| aoa-candidate-lineage-integrity | capability | draft | Checks whether a growth-refinery lineage chain stays internally coherent across checkpoint carry, reviewed candidate, seed staging, and downstream owner evidence while landing strength stays bounded by the artifacts. |
| aoa-owner-fit-routing-quality | boundary | draft | Checks whether a reviewed growth-refinery candidate is routed to the right owner layer with one clear owner hypothesis, honest nearest-wrong-target reasoning, and no first-authoring drift into derivative repos. |
| aoa-recurrence-control-plane-integrity | boundary | draft | Checks whether recurrence control-plane artifacts preserve typed propagation, observation-only hooks, owner review boundaries, thin downstream projections, and Agon stop-lines with global recurrence scoring outside the verdict. |
| aoa-diagnosis-cause-discipline | workflow | draft | Checks whether a diagnosis or self-diagnosis move names causal hypotheses, evidence limits, and unknowns while symptoms, owner ambiguity, repair success, and cause proof stay separate. |
| aoa-repair-boundedness | workflow | draft | Checks whether a reanchor or self-repair move stays bounded, preserves owner boundaries, and leaves a reviewable trail with scope-inflation pressure explicit. |
| aoa-continuity-anchor-integrity | capability | draft | Checks whether a bounded self-agency continuity window keeps an inspectable anchor chain across continuity, revision, reanchor, and anchor refs while memo, stats, and chat residue stay subordinate to the anchor. |
| aoa-reflective-revision-boundedness | workflow | draft | Checks whether reflective revision stays inside one named revision window, keeps stop-lines visible, and keeps vague continuity or hidden autonomy outside the claim. |
| aoa-self-reanchor-correctness | boundary | draft | Checks whether a bounded self-agency continuity route reanchors to the last valid artifact, keeps return mode explicit, and refuses chat-residue continuity when anchor integrity is lost. |
| aoa-witness-trace-integrity | workflow | draft | Checks whether a public witness trace for a bounded run keeps meaningful steps, tool visibility, state deltas, failures, redaction posture, and the markdown summary aligned enough for review. |
| aoa-regression-same-task | regression | baseline | Compares a candidate against a frozen baseline on the same bounded task family to detect material regression while claim scope stays on same-task movement. |
| aoa-artifact-review-rubric | artifact | portable | Checks whether a produced artifact on a bounded change task is reviewably strong on the visible task surface, with workflow-discipline and bridge claims routed to their own surfaces. |
| aoa-compost-provenance-preservation | artifact | draft | Checks whether witness-derived compost artifacts preserve provenance, review state, limits, and contradiction posture as they move toward note, principle, or canon-candidate surfaces. |
| aoa-output-vs-process-gap | comparative | draft | Compares artifact-side and process-side readings on the same bounded cases after standalone artifact review, standalone workflow review, or baseline comparison is already visible. |
| aoa-eval-integrity-check | capability | bounded | Checks whether current public starter bundles stay coherent as eval surfaces across manifest contract, verdict wording, evidence coverage, and public routing; this bounded integrity sidecar now travels with comparison-spine wording waves. |
| aoa-longitudinal-growth-snapshot | longitudinal | draft | Checks whether ordered, comparable windows on the same bounded workflow surface show modest directional movement with broad capability-growth claims outside the verdict. |

## Planned starter bundles

No additional planned starter bundles are currently named publicly.

## Comparison Spine

The current comparison spine is a bounded program layer with an explicit read
order.

Use it in this order:

| Route | Use when |
|---|---|
| one-run anchors | The base workflow, artifact, boundary, or stress read is still missing. |
| `aoa-regression-same-task` | A frozen-baseline comparison on the same bounded task family is needed. |
| `aoa-runtime-latency-tradeoff` | Selected runtime evidence needs a public-safe latency/resource tradeoff read under matched fixture conditions. |
| `aoa-output-vs-process-gap` | Matched artifact-side and process-side readings exist on the same bounded cases. |
| `aoa-longitudinal-growth-snapshot` | Ordered repeated-window movement on one named bounded workflow surface is the question. |
| `aoa-stress-recovery-window` | Ordered repeated-window proof on one named stressor family is the question. |
| `aoa-eval-integrity-check` | Public comparison wording, routing, or maturity posture needs a bounded sidecar read. |

Repeated-window discipline routes through
`mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`
when the `context_note` and `transition_note` chain is under review.

## Artifact Process Layer

The current artifact/process layer is a bounded program layer with artifact,
workflow, bridge, witness, and compost routes.

Use it in this order:

| Route | Use when |
|---|---|
| `aoa-artifact-review-rubric` | The produced artifact itself is the bounded object. |
| `aoa-bounded-change-quality` | The process-side workflow read is needed. |
| `aoa-output-vs-process-gap` | Both standalone artifact and workflow surfaces are visible under matched conditions. |
| `aoa-witness-trace-integrity` | The upstream witness trace needs reviewability before downstream reuse. |
| `aoa-compost-provenance-preservation` | Witness-derived compost needs provenance and review-state preservation. |

## Growth Refinery Layer

The current growth-refinery layer is a bounded doctrine set for lineage,
owner-fit, diagnosis, repair, and recurrence control-plane reads.

Use it by operation:

| Route | Use when |
|---|---|
| `aoa-candidate-lineage-integrity` | The lineage chain itself must stay structurally coherent. |
| `aoa-owner-fit-routing-quality` | A reviewed candidate needs one clear owner hypothesis and nearest-wrong target. |
| `aoa-diagnosis-cause-discipline` | Diagnosis must keep symptoms, causes, unknowns, and repair proof separate. |
| `aoa-repair-boundedness` | Reanchor and repair moves need bounded scope and owner-boundary evidence. |
| `aoa-recurrence-control-plane-integrity` | Recurrence run artifacts need control-plane, owner-review, downstream-thinness, and Agon stop-line checks. |

## Self-Agency Continuity Layer

The current self-agency continuity layer is a bounded doctrine triad for
anchor, revision, and reanchor reads.

Use it by route:

| Route | Use when |
|---|---|
| `aoa-continuity-anchor-integrity` | The route needs one inspectable anchor chain. |
| `aoa-reflective-revision-boundedness` | Reflective revision needs a named revision window and visible stop-lines. |
| `aoa-self-reanchor-correctness` | Reanchor needs return to the last valid artifact with explicit return posture. |

## Bundle Route Notes

The starter table is the public entry map. Bundle-local `EVAL.md` and
`eval.yaml` own claim meaning, support artifacts, and report examples.
Generated catalogs and report indexes are compact readers back to those source
surfaces.

Use `EVAL_SELECTION.md` when the first question is "which bundle should I open?"
Use this index when the first question is "what public starter surface exists,
what status does it carry, and which layer does it belong to?"

Non-starter public bundles stay discoverable through
`generated/eval_catalog.min.json`, `generated/eval_sections.full.json`, and
their bundle-local source directories until they are intentionally promoted into
the starter table.

Memo pilot boundary: current memo starter and readout routes include
writeback-decision quality, recall, contradiction, writeback-act,
reviewed-candidate adoption, and write-path guardrail surfaces. They stay below
future scar, retention, live memory-ledger readiness, KAG/RAG/vector readiness,
and broad memory-safety readiness.

Use `aoa-memo-writeback-decision-quality` before trusting a
`memo_writeback_decision` from `aoa-memo-writeback`. Use
`aoa-memo-write-path-guardrails` when a candidate/export route is moving toward
reviewed memory, and use `aoa-memo-writeback-act-integrity` after a concrete
runtime-to-memo act already exists.

## Planned public states

| status | meaning |
|---|---|
| `draft` | The eval idea exists, is documented, and awaits stability evidence for strong portable claims. |
| `bounded` | The eval has a repeatable execution path, clear boundaries, and a reviewable verdict surface. |
| `portable` | The eval can be reused outside its birth context while keeping its main meaning. |
| `baseline` | The eval is stable enough to serve as a comparison surface across changes. |
| `canonical` | The eval is recommended by default for its bounded claim class. |
| `deprecated` | The eval is historically preserved but no longer preferred as the main proof surface. |

## Category notes

- `capability` checks whether a bounded ability is present.
- `workflow` checks multi-step behavior across a bounded execution path.
- `boundary` checks scope, authority, safety, or approval adherence.
- `artifact` checks the quality or provenance-preserving integrity of produced outputs.
- `regression` checks whether a change made behavior worse.
- `comparative` compares variants, versions, or modes.
- `longitudinal` checks change over time.
- `stress` probes edge conditions, ambiguity, or adversarial surfaces.

## Notes

- The current portable one-run anchors are `aoa-bounded-change-quality` and
  `aoa-artifact-review-rubric`; the portable diagnostic workflow starter is
  `aoa-verification-honesty`.
- The current bounded one-run diagnostics are `aoa-scope-drift-detection`,
  `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`,
  `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, and
  `aoa-eval-integrity-check`.
- `aoa-regression-same-task` is the current public `baseline` starter.
- `generated/comparison_spine.json` is the compact reader for comparison
  metadata; use it to return to the owning bundle and mechanic surfaces.
- Future generated readers may add filters by status, object under evaluation,
  baseline mode, and verdict shape once another tool consumes those fields.
