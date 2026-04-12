# Eval Selection

This file is the repository-wide chooser for public eval bundles.

Use it when you need one bounded evaluation surface now,
rather than reading the full `EVAL_INDEX.md` first.

This surface prefers:
- bounded selection
- explicit claim classes
- modest public states
- honest uncertainty

Current starter posture:
- `aoa-bounded-change-quality` is the current portable composite workflow anchor:
  use it when you want one end-to-end workflow signal for a bounded non-trivial change task.
- `aoa-verification-honesty` is the current portable diagnostic workflow starter:
  use it when the main question is whether claimed verification matched executed, skipped, or blocked checks.
- `aoa-scope-drift-detection` is the current bounded diagnostic boundary starter for scope alignment:
  use it when the main question is whether requested scope still matched executed scope.
  Its materialized bounded proof flow now uses `fixtures/scope-drift-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
- `aoa-ambiguity-handling` is the current bounded diagnostic stress starter:
  use it when the main question is incomplete, conflicting, or underspecified task meaning.
  Its materialized bounded proof flow now uses `fixtures/ambiguity-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
- `aoa-approval-boundary-adherence` is the current bounded diagnostic boundary starter:
  use it when the main question is approval, authority, or permission classification.
  Its materialized bounded proof flow now uses `fixtures/approval-boundary-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
- `aoa-trace-outcome-separation` is the current bounded trace-aware workflow starter:
  use it when the main question is whether final outcome and path should stay separate before any combined reading.
  Its materialized bounded proof flow now uses `fixtures/trace-outcome-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
- `aoa-tool-trajectory-discipline` is the current bounded tool-path workflow starter:
  use it when tool-use path quality matters as its own bounded surface.
  Its materialized bounded proof flow now uses `fixtures/tool-trajectory-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
- `aoa-antifragility-posture` is the current draft stress-family antifragility starter:
  use it when the main question is whether one owner-local surface handled one named stressor family through bounded degraded continuation, source-owned receipts, and explicit anti-widening posture.
- `aoa-stress-recovery-window` is the current draft longitudinal stress-recovery starter:
  use it when the main question is whether ordered windows on one named stressor family show healthier handling without letting proof, stats, routing, or memo outrank owner evidence.
  Its current materialized proof flow uses a shared stress-recovery window family, runner contract, schema-backed report, and paired readout, but the bundle remains draft.
- `aoa-candidate-lineage-integrity` is the current draft growth-refinery lineage starter:
  use it when the main question is whether one bounded lineage chain stays coherent across checkpoint carry, reviewed candidate, seed staging, and owner evidence.
- `aoa-owner-fit-routing-quality` is the current draft growth-refinery routing starter:
  use it when the main question is whether a reviewed growth candidate is routed to the right owner layer with an honest nearest-wrong target and no derivative-repo first-authoring drift.
- `aoa-diagnosis-cause-discipline` is the current draft growth-refinery diagnosis starter:
  use it when the main question is whether a diagnosis or self-diagnosis move kept symptoms, probable causes, owner ambiguity, unknowns, and repair proof separate.
- `aoa-repair-boundedness` is the current draft growth-refinery repair starter:
  use it when the main question is whether a repair or reanchor move stayed bounded, preserved owner boundaries, and left a reviewable trail.
- `aoa-continuity-anchor-integrity` is the current draft self-agency continuity anchor starter:
  use it when the main question is whether a continuity route still keeps one inspectable anchor chain instead of drifting into memo, stats, or chat residue.
- `aoa-reflective-revision-boundedness` is the current draft self-agency continuity revision starter:
  use it when the main question is whether reflective revision stayed inside one named revision window instead of widening by convenience.
- `aoa-self-reanchor-correctness` is the current draft self-agency continuity reanchor starter:
  use it when the main question is whether reanchor returned to the last valid artifact rather than to remembered continuity.
- `aoa-witness-trace-integrity` is the current draft witness workflow starter:
  use it when the main question is whether a bounded run left a reviewable witness trace before any downstream memo or compost use.
  Its current draft proof flow is already materialized through a shared witness case family, bundle-local runner contract, and schema-backed report example.
- `aoa-regression-same-task` is the current baseline same-task regression starter:
  use it when you need a frozen-baseline comparison rather than a one-run judgment.
  Its current materialized proof flow uses a shared frozen case family, runner contract, schema-backed report, and shared baseline dossier.
- `aoa-artifact-review-rubric` is the current portable artifact anchor:
  use it when the main question is the produced artifact itself.
- `aoa-compost-provenance-preservation` is the current draft compost artifact starter:
  use it when the main question is whether a witness-derived note or principle candidate preserved provenance and review posture.
  Its current draft proof flow is already materialized through a shared compost case family, bundle-local runner contract, and schema-backed report example.
- `aoa-output-vs-process-gap` is the current draft artifact/process bridge starter:
  use it when the main question is whether polished output is outrunning process discipline or vice versa after the standalone artifact and workflow surfaces are already legible and matched conditions are explicit.
- `aoa-eval-integrity-check` is the current bounded integrity sidecar meta-eval for eval-bundle coherence:
  use it when the main question is whether a public starter bundle is overstating what it proves or drifting out of alignment with its public contract, especially across the comparison spine, not when you need a direct agent-behavior eval.
- `aoa-longitudinal-growth-snapshot` is the current draft longitudinal starter:
  use it when the main question is ordered repeated-window movement on the same bounded workflow surface.
  Its current materialized proof flow uses a shared repeated-window family, runner contract, schema-backed report, and shared dossiers, but the bundle remains draft.

See also:
- [EVAL_INDEX](EVAL_INDEX.md)
- [Documentation Map](docs/README.md)

## Quick split for nearby workflow and diagnostic questions

- Need one bounded end-to-end workflow signal, not a root-cause diagnosis? Start with `aoa-bounded-change-quality`.
- Need claimed-vs-actual verification evidence? Switch to `aoa-verification-honesty`.
- Need requested-scope versus executed-scope alignment? Switch to `aoa-scope-drift-detection`.
- Need incomplete or conflicting task meaning rather than permission classification? Switch to `aoa-ambiguity-handling`.
- Need final outcome and execution path kept separate before any combined reading? Use `aoa-trace-outcome-separation`.
- Need to judge the tool path itself on path-sensitive tasks? Use `aoa-tool-trajectory-discipline`.
- Need to know whether a growth-refinery lineage chain itself stayed coherent? Use `aoa-candidate-lineage-integrity`.
- Need to know whether a reviewed growth candidate is routed to the right owner layer? Use `aoa-owner-fit-routing-quality`.
- Need to know whether a diagnosis preserved cause discipline without overclaiming? Use `aoa-diagnosis-cause-discipline`.
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
  Use this when the question is bounded degraded continuation plus source-owned receipt posture on one named stressor family, not broad repo quality or repeated-window movement.

### I need to read repeated-window stress recovery on one named family without letting derived layers outrank owner evidence
- `aoa-stress-recovery-window`
  Use this when the question is repeated-window recovery posture for one named stressor family, not one-run owner-local posture and not federation-wide resilience.

### I need to know whether a growth-refinery lineage chain stays internally coherent
- `aoa-candidate-lineage-integrity`
  Use this when the question is chain coherence across checkpoint carry, reviewed candidate, seed staging, and owner evidence rather than owner choice or final object quality.

### I need to know whether a reviewed growth candidate is routed to the right owner layer
- `aoa-owner-fit-routing-quality`
  Use this when the question is owner hypothesis, owner shape, nearest-wrong-target quality, and derivative-repo exclusion rather than chain integrity or final object quality.

### I need to know whether a diagnosis named causes without overclaiming
- `aoa-diagnosis-cause-discipline`
  Use this when the question is whether symptoms, probable causes, owner ambiguity, unknowns, confidence limits, and repair handoff language stayed separate before repair, not whether the repair worked or owner fit is correct.

### I need to know whether a repair or reanchor move stayed bounded
- `aoa-repair-boundedness`
  Use this when the question is whether a follow-through correction preserved owner boundaries, reduced ambiguity, and stayed reviewable rather than widening scope under repair language.

### I need to know whether a continuity route still has one inspectable anchor chain
- `aoa-continuity-anchor-integrity`
  Use this when the question is whether `continuity_ref`, `revision_window_ref`, `reanchor_ref`, and `anchor_artifact_ref` still form one honest chain rather than dissolving into memo, stats, or chat residue.

### I need to know whether reflective revision stayed inside one named revision window
- `aoa-reflective-revision-boundedness`
  Use this when the question is whether reflective revision kept explicit stop-lines and stayed inside the named window rather than widening by convenience.

### I need to know whether reanchor returned to the last valid artifact
- `aoa-self-reanchor-correctness`
  Use this when the question is whether a route returned to the last valid artifact with explicit return posture rather than narrating continuity from memory.

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
  Do not use this bridge surface as a replacement for standalone artifact review, standalone workflow review, or frozen-baseline comparison.
  Read the side-by-side note as matched-condition evidence, not as stylistic explanation alone.

### I need to check whether a public starter bundle is coherent as an eval surface
- `aoa-eval-integrity-check`
  This is a bounded integrity sidecar meta-eval; do not use it as a direct agent-behavior starter.

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
| `boundary` | You care about authority, approval, permission adherence, requested-scope alignment, owner-fit routing boundaries, or whether a continuity route reanchored to the right artifact. | `aoa-scope-drift-detection`, `aoa-approval-boundary-adherence`, `aoa-owner-fit-routing-quality`, `aoa-self-reanchor-correctness` |
| `stress` | You care about incomplete, conflicting, or underspecified task meaning, or about one bounded owner-local stressor family and whether degraded continuation stayed reviewable, source-owned, and weaker than the normal path. | `aoa-ambiguity-handling`, `aoa-antifragility-posture` |
| `regression` | You care about frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| `artifact` | You care about the produced artifact itself or about provenance-preserving compost artifacts derived from witness-facing inputs. | `aoa-artifact-review-rubric`, `aoa-compost-provenance-preservation` |
| `comparative` | You care about cross-surface divergence such as polished output versus process discipline. | `aoa-output-vs-process-gap` |
| `capability` | You care about whether a bounded eval-side review surface is present, such as integrity checking of public eval bundles, growth-refinery lineage coherence, or continuity-anchor integrity as distinct bounded abilities. | `aoa-eval-integrity-check`, `aoa-candidate-lineage-integrity`, `aoa-continuity-anchor-integrity` |
| `longitudinal` | You care about ordered repeated-window movement on the same bounded surface, or about repeated-window stress recovery posture on one named stressor family rather than one-run or one-baseline comparison. | `aoa-longitudinal-growth-snapshot`, `aoa-stress-recovery-window` |

Guardrails:
- `workflow` here spans both composite and narrower surfaces; if you need a root-cause read, switch from `aoa-bounded-change-quality` to the narrower neighbor.
- `comparative` here is a bridge surface; it does not replace standalone artifact/workflow reading or the public baseline regression surface.
- `capability` here means a bounded eval-surface meta-review, not a direct runtime-quality judgment of the agent.

## Pick by public maturity

Current starter posture is still intentionally modest, but the portable-and-bounded one-run tranche now covers the core starter surfaces.

### If you need a stable public default now
There is no `canonical` eval yet.

### If you need a bounded comparison surface
Prefer `aoa-regression-same-task` when you need the first public `baseline` same-task comparison surface.
Use `aoa-output-vs-process-gap` when you need artifact-side versus process-side peer comparison on the same bounded cases after the standalone artifact and workflow surfaces are already readable.
Use `aoa-longitudinal-growth-snapshot` when you need ordered repeated-window movement on the same bounded workflow surface.
Use `aoa-stress-recovery-window` when the repeated-window question is specifically owner-first stress recovery posture for one named stressor family.
`aoa-regression-same-task`, `aoa-longitudinal-growth-snapshot`, and `aoa-stress-recovery-window` now ship materialized proof artifacts, but only `aoa-regression-same-task` is the public baseline surface.
Other comparative and growth surfaces remain modest draft work.
Use `aoa-eval-integrity-check` as the bounded sidecar when a public maturity wave risks semantic overreach, bundle blur, or baseline/growth-by-association drift.

### If you need a bounded one-run starter now
Prefer `aoa-scope-drift-detection`, `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, or `aoa-eval-integrity-check`.
These bounded diagnostics now have explicit bounded review notes, and `aoa-scope-drift-detection`, `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`, `aoa-trace-outcome-separation`, plus `aoa-tool-trajectory-discipline` now also have materialized schema-backed proof flows, but this tranche still does not support portable, baseline, or canonical claims.

### If you need a portable one-run starter now
Prefer `aoa-bounded-change-quality` when the question is composite workflow discipline on one bounded non-trivial change task.
Prefer `aoa-verification-honesty` when the question is claimed-vs-actual verification evidence on one bounded change surface.
Prefer `aoa-artifact-review-rubric` when the question is the produced artifact itself on the visible task surface.
These bundles now support portable reuse across bounded local adaptation, but they still do not imply baseline or canonical status.

### If you need an early public proof sketch beyond that bounded tranche
Use `draft` bundles carefully and read their boundaries, blind spots, and interpretation notes before drawing conclusions.

### If you need a narrow diagnostic surface rather than a composite signal
Verification truthfulness, scope alignment, task-meaning ambiguity, and authority or approval classification currently have public diagnostic starters.
Trace-aware split and tool-path workflow starters are also public, but they should not be mistaken for one-root-cause diagnostics.

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

If the bundle does not answer those questions clearly,
pick a narrower eval or defer strong conclusions.

## Notes

- This chooser is intentionally bounded and modest.
- `aoa-bounded-change-quality` can observe scope drift or fake verification, but it does not isolate those failure classes precisely.
- when the question is one failure class rather than one end-to-end workflow signal, switch from `aoa-bounded-change-quality` to the narrower neighbor immediately rather than over-reading the composite bundle.
- `aoa-bounded-change-quality` is now the portable one-run workflow anchor; portability here means bounded reuse, not baseline comparison or canonical default status.
- `aoa-verification-honesty` isolates verification evidence only; it is not the main eval for overall workflow quality or scope diagnosis.
- `aoa-verification-honesty` now ships a portable one-run proof surface; it remains the narrower diagnostic workflow read rather than the composite workflow anchor and does not imply baseline or canonical status.
- `aoa-scope-drift-detection` now ships a materialized bounded proof surface; it still isolates requested-scope vs executed-scope alignment only and is not the main eval for overall workflow quality or verification truthfulness.
- `aoa-ambiguity-handling` now ships a materialized bounded proof surface; it still isolates task-meaning ambiguity only and is not the main eval for permission or authority classification.
- `aoa-approval-boundary-adherence` now ships a materialized bounded proof surface; it still isolates authority ambiguity only and is not the main eval for incomplete or conflicting task meaning.
- `aoa-trace-outcome-separation` now ships a materialized bounded proof surface; it still isolates separate outcome/path reading only and is not the narrower tool-path eval.
- `aoa-approval-boundary-adherence` is about authority ambiguity, not about all forms of task ambiguity.
- `aoa-ambiguity-handling` isolates task-meaning ambiguity only; it is not the main eval for permission or authority classification.
- `aoa-trace-outcome-separation` is now a bounded one-run split surface; it keeps outcome and path distinct before a combined reading and is not a substitute for narrower root-cause diagnostics.
- `aoa-tool-trajectory-discipline` now ships a materialized bounded proof surface; it still isolates path-sensitive tool use only and is not a generic workflow or outcome-vs-path score.
- `aoa-tool-trajectory-discipline` is now a bounded one-run tool-path surface; it applies only where tool path materially matters and should not be used to grade process for its own sake or to replace the broader outcome-versus-path split.
- `aoa-antifragility-posture` is a draft first-wave stress-family surface; it stays on one owner-local receipt family and should not be over-read as broad resilience, repeated-window improvement, or stats authority.
- `aoa-stress-recovery-window` is a draft fourth-wave longitudinal stress surface; it stays on one named stressor family and should not be over-read as federation-wide resilience or live health authority.
- `aoa-candidate-lineage-integrity` is a draft growth-refinery capability surface; it stays on structural lineage coherence and should not be over-read as owner-fit proof, final object quality, or permission to skip owner-local evidence.
- `aoa-owner-fit-routing-quality` is a draft growth-refinery boundary surface; it stays on reviewed owner choice and nearest-wrong-target quality and should not be over-read as lineage proof, final object quality, or derivative-repo first-authoring permission.
- `aoa-diagnosis-cause-discipline` is a draft growth-refinery workflow surface; it stays on diagnosis-cause discipline and should not be over-read as repair success, final cause truth, final object quality, or owner-fit proof.
- `aoa-repair-boundedness` is a draft growth-refinery workflow surface; it stays on bounded repair and reanchor quality and should not be over-read as permanent stability, final owner proof, or retroactive validation of the first route.
- `aoa-long-horizon-depth` is now a materialized draft recurrence workflow surface; it stays on checkpoint-based restart fidelity and does not imply final-answer quality, broad long-horizon capability, or starter status.
- `aoa-memo-recall-integrity` is now a materialized draft memo workflow surface; it stays on inspect/capsule/expand recall integrity and does not imply contradiction coverage, permission safety, or starter status.
- `aoa-memo-contradiction-integrity` is now a materialized draft memo workflow surface; it stays on lifecycle-aware contradiction visibility and does not imply contradiction resolution, permission safety, promotion discipline, or starter status.
- `aoa-witness-trace-integrity` is a materialized draft witness workflow surface; it checks whether a public witness artifact stayed reviewable enough for bounded downstream use and does not claim runtime telemetry completeness or outcome quality.
- `aoa-regression-same-task` is now the first public `baseline` surface; it is a frozen-baseline comparison surface and should not be treated as proof of general capability growth.
- `aoa-artifact-review-rubric` is now the portable one-run artifact anchor; it stays on artifact quality only and does not imply strong workflow discipline or replace the bridge surface.
- `aoa-compost-provenance-preservation` is a materialized draft compost artifact surface; it checks provenance and review-state preservation on witness-derived artifacts and does not imply canon-readiness or replace general artifact review.
- `aoa-output-vs-process-gap` remains a draft bridge surface; it now participates in the first materialized artifact/process paired proof flow, but it still does not replace standalone artifact review, standalone workflow review, trace/path separation, or the public baseline regression surface.
- `aoa-output-vs-process-gap` now also carries a second matched family and paired dossier, but it still stays draft and does not inherit stronger status by association.
- `aoa-eval-integrity-check` is now a bounded integrity sidecar meta-eval for public starter-bundle coherence and semantic anti-theater review across the comparison spine; it does not replace direct agent-behavior evaluation, promotion review, or proof of canonical readiness.
- `aoa-longitudinal-growth-snapshot` is a repeated-window movement surface; it does not replace one-run workflow reading or frozen same-task regression, and its `context_note` plus `transition_note` should stay visible before any top-line movement story.
- `aoa-stress-recovery-window` is a repeated-window stress recovery surface; it does not replace one-run owner-local antifragility reading, frozen same-task regression, or owner-owned health truth.
- `generated/comparison_spine.json` is now the minimal filtered reader surface for the comparison ladder.
- As the corpus grows, later generated surfaces may add filters by status, object under evaluation, baseline mode, and verdict shape.
- Prefer `baseline` or `canonical` bundles for stronger comparison claims once the public corpus reaches that stage.
