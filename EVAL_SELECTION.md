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
- `aoa-bounded-change-quality` is the current composite workflow starter:
  use it when you want one end-to-end workflow signal for a bounded non-trivial change task.
- `aoa-verification-honesty` is the current diagnostic workflow starter:
  use it when the main question is whether claimed verification matched executed, skipped, or blocked checks.
- `aoa-scope-drift-detection` is the current diagnostic boundary starter for scope alignment:
  use it when the main question is whether requested scope still matched executed scope.
- `aoa-ambiguity-handling` is the current diagnostic stress starter:
  use it when the main question is incomplete, conflicting, or underspecified task meaning.
- `aoa-approval-boundary-adherence` is the current diagnostic boundary starter:
  use it when the main question is approval, authority, or permission classification.
- `aoa-trace-outcome-separation` is the current trace-aware workflow starter:
  use it when the main question is whether final outcome and path should stay separate before any combined reading.
- `aoa-tool-trajectory-discipline` is the current tool-path workflow starter:
  use it when tool-use path quality matters as its own bounded surface.
- `aoa-regression-same-task` is the current same-task regression starter:
  use it when you need a frozen-baseline comparison rather than a one-run judgment.
- `aoa-artifact-review-rubric` is the current artifact starter:
  use it when the main question is the produced artifact itself.
- `aoa-output-vs-process-gap` is the current artifact/process bridge starter:
  use it when the main question is whether polished output is outrunning process discipline or vice versa.

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

## Pick by category

| category | use when | starter bundles |
|---|---|---|
| `workflow` | You care about multi-step execution quality, verification truthfulness, outcome-vs-path separation, or tool-path quality where path matters. | `aoa-bounded-change-quality`, `aoa-verification-honesty`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline` |
| `boundary` | You care about authority, approval, permission adherence, or requested-scope alignment. | `aoa-scope-drift-detection`, `aoa-approval-boundary-adherence` |
| `stress` | You care about incomplete, conflicting, or underspecified task meaning. | `aoa-ambiguity-handling` |
| `regression` | You care about frozen-baseline comparison on the same bounded task family. | `aoa-regression-same-task` |
| `artifact` | You care about the produced artifact itself rather than the workflow that produced it. | `aoa-artifact-review-rubric` |
| `comparative` | You care about cross-surface divergence such as polished output versus process discipline. | `aoa-output-vs-process-gap` |

## Pick by public maturity

Current starter posture is intentionally modest.

### If you need a stable public default now
There is no `canonical` eval yet.

### If you need a bounded comparison surface
Use `aoa-regression-same-task` when you need a frozen-baseline same-task comparison.
Use `aoa-output-vs-process-gap` when you need artifact-side versus process-side peer comparison on the same bounded cases.
Broader `baseline` surfaces are still future work.

### If you need an early public proof sketch
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
- `aoa-trace-outcome-separation` keeps outcome and path distinct before a combined reading; it is not a substitute for narrower root-cause diagnostics.
- `aoa-tool-trajectory-discipline` applies only where tool path materially matters; it should not be used to grade process for its own sake.
- `aoa-regression-same-task` is a frozen-baseline comparison surface; it should not be treated as proof of general capability growth.
- `aoa-artifact-review-rubric` stays on artifact quality only; it does not imply strong workflow discipline.
- `aoa-output-vs-process-gap` is a bridge surface; it does not replace standalone artifact review, standalone workflow review, or trace/path separation.
- As the corpus grows, later generated surfaces may add filters by status, object under evaluation, baseline mode, and verdict shape.
- Prefer `baseline` or `canonical` bundles for stronger comparison claims once the public corpus reaches that stage.
