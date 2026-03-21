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
- `aoa-bounded-change-quality` is the current bounded composite workflow starter:
  use it when you want one end-to-end workflow signal for a bounded non-trivial change task.
- `aoa-verification-honesty` is the current bounded diagnostic workflow starter:
  use it when the main question is whether claimed verification matched executed, skipped, or blocked checks.
- `aoa-scope-drift-detection` is the current bounded diagnostic boundary starter for scope alignment:
  use it when the main question is whether requested scope still matched executed scope.
- `aoa-ambiguity-handling` is the current bounded diagnostic stress starter:
  use it when the main question is incomplete, conflicting, or underspecified task meaning.
- `aoa-approval-boundary-adherence` is the current bounded diagnostic boundary starter:
  use it when the main question is approval, authority, or permission classification.
- `aoa-trace-outcome-separation` is the current bounded trace-aware workflow starter:
  use it when the main question is whether final outcome and path should stay separate before any combined reading.
- `aoa-tool-trajectory-discipline` is the current bounded tool-path workflow starter:
  use it when tool-use path quality matters as its own bounded surface.
- `aoa-regression-same-task` is the current baseline same-task regression starter:
  use it when you need a frozen-baseline comparison rather than a one-run judgment.
- `aoa-artifact-review-rubric` is the current bounded artifact starter:
  use it when the main question is the produced artifact itself.
- `aoa-output-vs-process-gap` is the current draft artifact/process bridge starter:
  use it when the main question is whether polished output is outrunning process discipline or vice versa.
- `aoa-eval-integrity-check` is the current bounded capability sidecar for eval-bundle coherence:
  use it when the main question is whether a public starter bundle is overstating what it proves or drifting out of alignment with its public contract.
- `aoa-longitudinal-growth-snapshot` is the current draft longitudinal starter:
  use it when the main question is ordered repeated-window movement on the same bounded workflow surface.

See also:
- [EVAL_INDEX](EVAL_INDEX.md)
- [Documentation Map](docs/README.md)

## Pick by question

### I need one bounded end-to-end workflow signal for a non-trivial change task
- `aoa-bounded-change-quality`

### I need to know whether an agent respected approval, authority, or risk boundaries
- `aoa-approval-boundary-adherence`

### I need to isolate whether the agent faked or overstated verification
- `aoa-verification-honesty`

### I need to isolate whether the agent silently widened, narrowed, or reshaped the task
- `aoa-scope-drift-detection`

### I need to evaluate incomplete or conflicting task meaning rather than authority ambiguity
- `aoa-ambiguity-handling`

### I need to split final outcome judgment from path judgment without assuming one correct trace
- `aoa-trace-outcome-separation`

### I need to judge tool-use path quality only where the tool path itself matters
- `aoa-tool-trajectory-discipline`

### I need to compare a candidate against a frozen baseline on the same bounded task family
- `aoa-regression-same-task`

### I need to judge the produced artifact itself
- `aoa-artifact-review-rubric`

### I need to know whether polished output is outrunning process discipline
- `aoa-output-vs-process-gap`

### I need to check whether a public starter bundle is coherent as an eval surface
- `aoa-eval-integrity-check`

### I need to read repeated-window movement on the same bounded workflow surface
- `aoa-longitudinal-growth-snapshot`

## Pick by category

| category | use when | starter bundles |
|---|---|---|
| `workflow` | You care about multi-step execution quality, verification truthfulness, outcome-vs-path separation, or tool-path quality where path matters. | `aoa-bounded-change-quality`, `aoa-verification-honesty`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline` |
| `boundary` | You care about authority, approval, permission adherence, or requested-scope alignment. | `aoa-scope-drift-detection`, `aoa-approval-boundary-adherence` |
| `stress` | You care about incomplete, conflicting, or underspecified task meaning. | `aoa-ambiguity-handling` |
| `regression` | You care about frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| `artifact` | You care about the produced artifact itself rather than the workflow that produced it. | `aoa-artifact-review-rubric` |
| `comparative` | You care about cross-surface divergence such as polished output versus process discipline. | `aoa-output-vs-process-gap` |
| `capability` | You care about whether a bounded eval ability or review surface is present, such as integrity checking of public eval bundles. | `aoa-eval-integrity-check` |
| `longitudinal` | You care about ordered repeated-window movement on the same bounded surface rather than one-run or one-baseline comparison. | `aoa-longitudinal-growth-snapshot` |

## Pick by public maturity

Current starter posture is still intentionally modest, but the bounded one-run tranche now covers the core starter surfaces.

### If you need a stable public default now
There is no `canonical` eval yet.

### If you need a bounded comparison surface
Prefer `aoa-regression-same-task` when you need the first public `baseline` same-task comparison surface.
Use `aoa-output-vs-process-gap` when you need artifact-side versus process-side peer comparison on the same bounded cases.
Use `aoa-longitudinal-growth-snapshot` when you need ordered repeated-window movement on the same bounded workflow surface.
Other comparative and growth surfaces remain modest draft work.
Use `aoa-eval-integrity-check` as the bounded sidecar when a public maturity wave risks semantic overreach, bundle blur, or baseline/growth-by-association drift.

### If you need a bounded one-run starter now
Prefer `aoa-bounded-change-quality`, `aoa-verification-honesty`, `aoa-scope-drift-detection`, `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, or `aoa-artifact-review-rubric`.
These bundles now have explicit bounded review notes and stronger example readouts, but they still do not support portable, baseline, or canonical claims.

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
| same-task regression comparison | You want a frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| artifact review | You want to judge the produced artifact itself on the visible task surface. | `aoa-artifact-review-rubric` |
| output-vs-process divergence | You want to compare artifact-side and process-side readings on the same bounded cases. | `aoa-output-vs-process-gap` |
| eval-bundle integrity | You want to inspect whether a public starter bundle remains coherent across its manifest, evidence, and public routing surfaces. | `aoa-eval-integrity-check` |
| bounded longitudinal movement | You want to inspect ordered repeated-window movement on one named bounded workflow surface. | `aoa-longitudinal-growth-snapshot` |

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
- `aoa-verification-honesty` isolates verification evidence only; it is not the main eval for overall workflow quality or scope diagnosis.
- `aoa-scope-drift-detection` isolates requested-scope vs executed-scope alignment only; it is not the main eval for overall workflow quality or verification truthfulness.
- `aoa-ambiguity-handling` isolates task-meaning ambiguity only; it is not the main eval for permission or authority classification.
- `aoa-approval-boundary-adherence` is about authority ambiguity, not about all forms of task ambiguity.
- `aoa-trace-outcome-separation` is now a bounded one-run split surface; it keeps outcome and path distinct before a combined reading and is not a substitute for narrower root-cause diagnostics.
- `aoa-tool-trajectory-discipline` is now a bounded one-run tool-path surface; it applies only where tool path materially matters and should not be used to grade process for its own sake.
- `aoa-regression-same-task` is now the first public `baseline` surface; it is a frozen-baseline comparison surface and should not be treated as proof of general capability growth.
- `aoa-artifact-review-rubric` is now a bounded one-run artifact surface; it stays on artifact quality only and does not imply strong workflow discipline.
- `aoa-output-vs-process-gap` remains a draft bridge surface; it now participates in the first materialized artifact/process paired proof flow, but it still does not replace standalone artifact review, standalone workflow review, trace/path separation, or the public baseline regression surface.
- `aoa-eval-integrity-check` is now a bounded meta-eval for public starter-bundle coherence and semantic anti-theater review; it does not replace direct agent-behavior evaluation or promotion review.
- `aoa-longitudinal-growth-snapshot` is a repeated-window movement surface; it does not replace one-run workflow reading or frozen same-task regression.
- As the corpus grows, later generated surfaces may add filters by status, object under evaluation, baseline mode, and verdict shape.
- Prefer `baseline` or `canonical` bundles for stronger comparison claims once the public corpus reaches that stage.
