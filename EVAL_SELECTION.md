# Eval Bundle Selection Chooser

This file is the repository-wide chooser for public eval bundles.

Use it when you need one bounded evaluation surface before reading the full
`EVAL_INDEX.md`.

This surface prefers:
- bounded selection
- explicit claim classes
- modest public states
- honest uncertainty

## Current Starter Posture

| Eval | Status | Use when |
|---|---|---|
| `aoa-bounded-change-quality` | portable | You need one end-to-end workflow signal for a bounded non-trivial change task. |
| `aoa-experience-protocol-integrity` | draft | You need to read whether experience verdict protocol integrity stayed explicit and bounded. |
| `aoa-verification-honesty` | portable | You need claimed verification compared with executed, skipped, or blocked checks. |
| `aoa-scope-drift-detection` | bounded | You need requested scope compared with executed scope. |
| `aoa-ambiguity-handling` | bounded | You need incomplete, conflicting, or underspecified task meaning evaluated as the main question. |
| `aoa-approval-boundary-adherence` | bounded | You need approval, authority, or permission classification. |
| `aoa-trace-outcome-separation` | bounded | You need final outcome and execution path kept separately readable before a combined reading. |
| `aoa-tool-trajectory-discipline` | bounded | You need tool-use path quality as its own bounded surface. |
| `aoa-antifragility-posture` | draft | You need one owner-local stressor family read through bounded degraded continuation and source-owned receipts. |
| `aoa-stress-recovery-window` | draft | You need ordered windows on one named stressor family read with owner evidence first. |
| `aoa-candidate-lineage-integrity` | draft | You need one bounded lineage chain checked across checkpoint carry, reviewed candidate, seed staging, and owner evidence. |
| `aoa-owner-fit-routing-quality` | draft | You need a reviewed growth candidate routed to the right owner layer with a visible nearest-wrong target. |
| `aoa-recurrence-control-plane-integrity` | draft | You need recurrence control-plane artifacts checked for registry, graph, hooks, review, downstream-thinness, and Agon stop-line integrity. |
| `aoa-diagnosis-cause-discipline` | draft | You need symptoms, probable causes, owner ambiguity, unknowns, and repair proof kept separate. |
| `aoa-repair-boundedness` | draft | You need a repair or reanchor move checked for bounded scope, owner boundaries, and a reviewable trail. |
| `aoa-continuity-anchor-integrity` | draft | You need one inspectable continuity anchor chain. |
| `aoa-reflective-revision-boundedness` | draft | You need reflective revision checked inside one named revision window. |
| `aoa-self-reanchor-correctness` | draft | You need reanchor checked against the last valid artifact. |
| `aoa-witness-trace-integrity` | draft | You need a bounded run checked for a reviewable witness trace before memo or compost use. |
| `aoa-regression-same-task` | baseline | You need frozen-baseline comparison on the same bounded task family. |
| `aoa-artifact-review-rubric` | portable | You need the produced artifact judged on the visible task surface. |
| `aoa-compost-provenance-preservation` | draft | You need witness-derived compost checked for provenance and review posture. |
| `aoa-output-vs-process-gap` | draft | You need artifact-side and process-side readings compared on matched conditions after both standalone readings exist. |
| `aoa-eval-integrity-check` | bounded | You need public starter-bundle coherence checked across manifest, evidence, and public routing surfaces. |
| `aoa-longitudinal-growth-snapshot` | draft | You need ordered repeated-window movement on the same bounded workflow surface. |

See also:
- [EVAL_INDEX](EVAL_INDEX.md)
- [Documentation Map](docs/README.md)

## Quick split for nearby workflow and diagnostic questions

- Need one bounded end-to-end workflow signal? Start with `aoa-bounded-change-quality`.
- Need claimed-vs-actual verification evidence? Switch to `aoa-verification-honesty`.
- Need requested-scope versus executed-scope alignment? Switch to `aoa-scope-drift-detection`.
- Need incomplete or conflicting task meaning? Switch to `aoa-ambiguity-handling`.
- Need final outcome and execution path kept separate before any combined reading? Use `aoa-trace-outcome-separation`.
- Need to judge the tool path itself on path-sensitive tasks? Use `aoa-tool-trajectory-discipline`.
- Need to know whether a growth-refinery lineage chain itself stayed coherent? Use `aoa-candidate-lineage-integrity`.
- Need to know whether a reviewed growth candidate is routed to the right owner layer? Use `aoa-owner-fit-routing-quality`.
- Need to know whether recurrence control-plane artifacts stayed bounded? Use `aoa-recurrence-control-plane-integrity`.
- Need to know whether a diagnosis preserved explicit cause limits? Use `aoa-diagnosis-cause-discipline`.
- Need to know whether a repair or reanchor move stayed bounded instead of smearing scope? Use `aoa-repair-boundedness`.
- Need to know whether a continuity route still has one inspectable anchor chain? Use `aoa-continuity-anchor-integrity`.
- Need to know whether reflective revision stayed inside one named revision window? Use `aoa-reflective-revision-boundedness`.
- Need to know whether reanchor returned to the last valid artifact? Use `aoa-self-reanchor-correctness`.

## Pick by question

### I need one bounded end-to-end workflow signal for a non-trivial change task
- `aoa-bounded-change-quality`
  Use a narrower neighbor instead when the real question is claimed verification, scope alignment, task-meaning ambiguity, outcome-versus-path split, or tool-path quality itself.

### I need to know whether an agent respected approval, authority, or risk boundaries
- `aoa-approval-boundary-adherence`

### I need to isolate whether the agent faked or overstated verification
- `aoa-verification-honesty`

### I need to isolate whether the agent silently widened, narrowed, or reshaped the task
- `aoa-scope-drift-detection`

### I need to evaluate incomplete or conflicting task meaning rather than authority ambiguity
- `aoa-ambiguity-handling`

### I need to read one owner-local antifragility family without collapsing source ownership
- `aoa-antifragility-posture`
  Use this when the question is bounded degraded continuation plus source-owned receipt posture on one named stressor family.

### I need to read repeated-window stress recovery on one named family without letting derived layers outrank owner evidence
- `aoa-stress-recovery-window`
  Use this when the question is repeated-window recovery posture for one named stressor family.

### I need to know whether a growth-refinery lineage chain stays internally coherent
- `aoa-candidate-lineage-integrity`
  Use this when the question is chain coherence across checkpoint carry, reviewed candidate, seed staging, and owner evidence.

### I need to know whether a reviewed growth candidate is routed to the right owner layer
- `aoa-owner-fit-routing-quality`
  Use this when the question is owner hypothesis, owner shape, nearest-wrong-target quality, and derivative-repo exclusion.

### I need to know whether recurrence control-plane artifacts stayed bounded
- `aoa-recurrence-control-plane-integrity`
  Use this when the inspected object is the recurrence control-plane run itself: manifest scan, graph closure, hooks, beacons, review decisions, downstream projections, and Agon diagnostics. Use neighboring evals for verification honesty, candidate lineage, or return-anchor fidelity.

### I need to know whether a diagnosis named causes without overclaiming
- `aoa-diagnosis-cause-discipline`
  Use this when the question is whether symptoms, probable causes, owner ambiguity, unknowns, confidence limits, and repair handoff language stayed separate before repair.

### I need to know whether a repair or reanchor move stayed bounded
- `aoa-repair-boundedness`
  Use this when the question is whether a follow-through correction preserved owner boundaries, reduced ambiguity, and stayed reviewable.

### I need to know whether a continuity route still has one inspectable anchor chain
- `aoa-continuity-anchor-integrity`
  Use this when the question is whether `continuity_ref`, `revision_window_ref`, `reanchor_ref`, and `anchor_artifact_ref` still form one honest chain.

### I need to know whether reflective revision stayed inside one named revision window
- `aoa-reflective-revision-boundedness`
  Use this when the question is whether reflective revision kept explicit stop-lines and stayed inside the named window.

### I need to know whether reanchor returned to the last valid artifact
- `aoa-self-reanchor-correctness`
  Use this when the question is whether a route returned to the last valid artifact with explicit return posture.

### I need to split final outcome judgment from path judgment without assuming one correct trace
- `aoa-trace-outcome-separation`
  If the path itself is the bounded surface, switch to `aoa-tool-trajectory-discipline`.

### I need to judge tool-use path quality only where the tool path itself matters
- `aoa-tool-trajectory-discipline`
  If the question is whether outcome and path should stay separately readable before any combined reading, switch to `aoa-trace-outcome-separation`.

### I need to know whether a bounded run left a reviewable witness trace
- `aoa-witness-trace-integrity`
  Use this when the main question is whether meaningful steps, tool calls, external effects, failures, redaction posture, and the markdown summary stayed reviewable enough for downstream use.

### I need to compare a candidate against a frozen baseline on the same bounded task family
- `aoa-regression-same-task`

### I need to judge the produced artifact itself
- `aoa-artifact-review-rubric`
  If the question is artifact-versus-process divergence on the same cases, switch to `aoa-output-vs-process-gap` only after the standalone workflow read is already visible.

### I need to know whether a witness-derived compost artifact preserved provenance
- `aoa-compost-provenance-preservation`
  Use this when the main question is whether a note, synthesis, or principle candidate kept source refs, review state, limits, and demotion posture visible.

### I need to know whether polished output is outrunning process discipline
- `aoa-output-vs-process-gap`
  Use this bridge after standalone artifact review, standalone workflow review, or frozen-baseline comparison has made the paired surfaces visible.
  Read the side-by-side note as matched-condition evidence.

### I need to check whether a public starter bundle is coherent as an eval surface
- `aoa-eval-integrity-check`
  Use this as the bounded integrity sidecar for public starter-bundle coherence.

### I need to read repeated-window movement on the same bounded workflow surface
- `aoa-longitudinal-growth-snapshot`
  Read `context_note` as the comparability disclosure and `transition_note` as the bounded explanation of movement against the previous window.

## Pick Comparison Surface

### Do you need a frozen-baseline comparison on the same bounded task family?
- `aoa-regression-same-task`
  This remains the only current default public `baseline` comparison surface.

### Do you need a side-by-side peer compare between artifact quality and workflow discipline on the same bounded cases?
- `aoa-output-vs-process-gap`
  Read it only after the standalone artifact and workflow surfaces are already visible.

### Do you need ordered repeated-window movement on one named bounded workflow surface?
- `aoa-longitudinal-growth-snapshot`
  Keep the read modest; this remains a draft repeated-window movement surface.

### Do you need ordered repeated-window proof for one named stress recovery family?
- `aoa-stress-recovery-window`
  Keep the read owner-first; this remains a draft repeated-window stress recovery surface.

### Do you need the bounded integrity sidecar for a comparison-spine wording or maturity wave?
- `aoa-eval-integrity-check`
  Use it when public comparison wording, routing, or maturity posture risks turning the current comparison read theatrical.

## Pick by category

| category | use when | starter bundles |
|---|---|---|
| `workflow` | You care about multi-step execution quality, diagnosis-cause discipline, repair boundedness, reflective revision boundedness on continuity routes, verification truthfulness, outcome-vs-path separation, tool-path quality where path matters, or public witness-trace reviewability. | `aoa-bounded-change-quality`, `aoa-diagnosis-cause-discipline`, `aoa-repair-boundedness`, `aoa-reflective-revision-boundedness`, `aoa-verification-honesty`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, `aoa-witness-trace-integrity` |
| `boundary` | You care about authority, approval, permission adherence, requested-scope alignment, owner-fit routing boundaries, or whether a continuity route reanchored to the right artifact. | `aoa-scope-drift-detection`, `aoa-approval-boundary-adherence`, `aoa-owner-fit-routing-quality`, `aoa-self-reanchor-correctness`, `aoa-experience-protocol-integrity` |
| `stress` | You care about incomplete, conflicting, or underspecified task meaning, or about one bounded owner-local stressor family and whether degraded continuation stayed reviewable, source-owned, and weaker than the normal path. | `aoa-ambiguity-handling`, `aoa-antifragility-posture` |
| `regression` | You care about frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| `artifact` | You care about the produced artifact itself or about provenance-preserving compost artifacts derived from witness-facing inputs. | `aoa-artifact-review-rubric`, `aoa-compost-provenance-preservation` |
| `comparative` | You care about cross-surface divergence such as polished output versus process discipline. | `aoa-output-vs-process-gap` |
| `capability` | You care about whether a bounded eval-side review surface is present, such as integrity checking of public eval bundles, growth-refinery lineage coherence, or continuity-anchor integrity as distinct bounded abilities. | `aoa-eval-integrity-check`, `aoa-candidate-lineage-integrity`, `aoa-continuity-anchor-integrity` |
| `longitudinal` | You care about ordered repeated-window movement on the same bounded surface, or about repeated-window stress recovery posture on one named stressor family rather than one-run or one-baseline comparison. | `aoa-longitudinal-growth-snapshot`, `aoa-stress-recovery-window` |

Route boundaries:
- `workflow` here spans both composite and narrower surfaces; if you need a root-cause read, switch from `aoa-bounded-change-quality` to the narrower neighbor.
- `comparative` here is a bridge surface; read standalone artifact/workflow and public baseline surfaces first when those are the real question.
- `capability` here means a bounded eval-surface meta-review; use a direct runtime-quality surface when that is the real question.

## Pick by public maturity

Use maturity as a claim-strength selector before reading individual bundle
evidence.

### If you need the strongest current public default
Use the `portable` and `baseline` starters for the bounded claim they name.
`canonical` promotion remains a future state that requires broad portability,
explicit `canonical_readiness`, and a fresh public-safety recheck.

### If you need a bounded comparison surface
Prefer `aoa-regression-same-task` when you need the first public `baseline` same-task comparison surface.
Use `aoa-output-vs-process-gap` when you need artifact-side versus process-side peer comparison on the same bounded cases after the standalone artifact and workflow surfaces are already readable.
Use `aoa-longitudinal-growth-snapshot` when you need ordered repeated-window movement on the same bounded workflow surface.
Use `aoa-stress-recovery-window` when the repeated-window question is specifically owner-first stress recovery posture for one named stressor family.
Use `aoa-eval-integrity-check` as the bounded sidecar when a public maturity wave risks semantic overreach, bundle blur, or baseline/growth-by-association drift.
Follow bundle-local `EVAL.md`, `eval.yaml`, and report artifacts for the proof
path after selecting the comparison surface.

### If you need a bounded one-run starter now
Prefer `aoa-scope-drift-detection`, `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, or `aoa-eval-integrity-check`.
These bounded diagnostics give repeatable one-run reads. Keep the read inside
the status shown in `EVAL_INDEX.md` and the bundle manifest.

### If you need a portable one-run starter now
Prefer `aoa-bounded-change-quality` when the question is composite workflow discipline on one bounded non-trivial change task.
Prefer `aoa-verification-honesty` when the question is claimed-vs-actual verification evidence on one bounded change surface.
Prefer `aoa-artifact-review-rubric` when the question is the produced artifact itself on the visible task surface.
These bundles support portable reuse across bounded local adaptation. Use
`aoa-regression-same-task` when the job needs baseline comparison.

### If you need an early public proof sketch beyond that bounded tranche
Use `draft` bundles carefully and read their boundaries, blind spots, and interpretation notes before drawing conclusions.

### If you need a narrow diagnostic surface rather than a composite signal
Verification truthfulness, scope alignment, task-meaning ambiguity, and authority or approval classification currently have public diagnostic starters.
Trace-aware split and tool-path workflow starters are also public; use the narrower diagnostic starters for one-root-cause reads.

## Pick by claim style

| claim style | use when | likely bundles |
|---|---|---|
| composite workflow quality | You want to know whether a bounded change workflow held together end to end. | `aoa-bounded-change-quality` |
| verification honesty | You want to isolate claimed-vs-actual verification evidence. | `aoa-verification-honesty` |
| authority and approval boundary adherence | You want to know whether the agent classified safe, approval-gated, and out-of-bounds actions correctly. | `aoa-approval-boundary-adherence` |
| scope alignment | You want to isolate requested-scope vs executed-scope drift. | `aoa-scope-drift-detection` |
| task-meaning ambiguity handling | You want to isolate incomplete or conflicting requirements rather than permission classification. | `aoa-ambiguity-handling` |
| outcome-vs-path split | You want separate readings for final outcome and execution path before any combined workflow verdict. | `aoa-trace-outcome-separation` |
| tool trajectory discipline | You want to judge tool-use path quality only where the tool path itself matters. | `aoa-tool-trajectory-discipline` |
| witness trace integrity | You want to know whether a bounded run left a reviewable public witness trace before memo or compost reuse. | `aoa-witness-trace-integrity` |
| diagnosis-cause discipline | You want to know whether a diagnosis kept symptoms, probable causes, owner ambiguity, unknowns, and repair proof separate. | `aoa-diagnosis-cause-discipline` |
| same-task regression comparison | You want a frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| artifact review | You want to judge the produced artifact itself on the visible task surface. | `aoa-artifact-review-rubric` |
| compost provenance preservation | You want to know whether a witness-derived note or principle candidate kept provenance, review state, and demotion posture visible. | `aoa-compost-provenance-preservation` |
| output-vs-process divergence | You want to compare artifact-side and process-side readings on the same bounded cases. | `aoa-output-vs-process-gap` |
| eval-bundle integrity | You want to inspect whether a public starter bundle remains coherent across its manifest, evidence, and public routing surfaces. | `aoa-eval-integrity-check` |
| bounded longitudinal movement | You want to inspect ordered repeated-window movement on one named bounded workflow surface. | `aoa-longitudinal-growth-snapshot` |
| bounded stress recovery longitudinal read | You want to inspect ordered repeated-window recovery posture on one named stressor family without letting downstream derived layers outrank owner evidence. | `aoa-stress-recovery-window` |

## Reader guidance

When choosing an eval, ask:

1. what claim do I actually need to support?
2. do I need a one-run signal or a comparison surface?
3. am I judging workflow quality, artifact quality, safety boundaries, or regression?
4. what would this eval still fail to tell me?
5. would a pass here support a bounded claim, or tempt me into saying too much?

If the bundle answers a different question, pick a narrower eval or defer strong
conclusions.

## Source Routes

After choosing a bundle:

1. Read the bundle-local `EVAL.md` and `eval.yaml` for claim meaning,
   status, category, baseline mode, and evidence refs.
2. Use `generated/eval_catalog.min.json`, `generated/eval_sections.full.json`,
   and `generated/comparison_spine.json` only as compact readers back to source
   surfaces.
3. Use `generated/eval_report_index.min.json` when the next question is which
   report or receipt artifact exists.
4. Validate the selected path with `python scripts/validate_repo.py --eval
   <bundle-name>` or the broader repository checks named in `AGENTS.md`.

Memo pilot boundary: current memo starter and readout routes stay below future scar, retention, and live memory-ledger readiness.
