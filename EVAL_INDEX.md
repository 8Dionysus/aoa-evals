# EVAL_INDEX

This file is the repository-wide map of public eval bundles.

## Starter eval bundles

| name | category | status | summary |
|---|---|---|---|
| aoa-bounded-change-quality | workflow | bounded | Checks whether a non-trivial agent change stays scoped, explicitly verified, and clearly reported without silent task expansion. |
| aoa-verification-honesty | workflow | bounded | Checks whether an agent truthfully reports which verification steps on a bounded change task were executed, skipped, or blocked. |
| aoa-scope-drift-detection | boundary | bounded | Checks whether an agent keeps requested scope aligned with executed scope on bounded change tasks, or explicitly discloses deviation. |
| aoa-ambiguity-handling | stress | bounded | Checks whether an agent handles incomplete, conflicting, or underspecified task meaning on bounded change tasks without silently choosing an unearned path. |
| aoa-approval-boundary-adherence | boundary | bounded | Checks whether an agent correctly distinguishes safe action, explicit-approval-required action, and out-of-bounds action. |
| aoa-trace-outcome-separation | workflow | bounded | Checks whether bounded change workflows remain reviewable when final outcome and execution-path quality are judged separately before any combined reading. |
| aoa-tool-trajectory-discipline | workflow | bounded | Checks whether an agent uses tools in a disciplined, reviewable way on bounded tasks where the tool path itself is part of the bounded claim. |
| aoa-regression-same-task | regression | draft | Compares a candidate against a frozen baseline on the same bounded task family to detect material regression without claiming general growth. |
| aoa-artifact-review-rubric | artifact | bounded | Checks whether a produced artifact on a bounded change task is reviewably strong on the visible task surface without treating polish as proof of workflow discipline. |
| aoa-output-vs-process-gap | comparative | draft | Compares artifact-side and process-side readings on the same bounded cases to show when polished output outruns workflow discipline, process outruns artifact strength, or the two stay aligned. |
| aoa-eval-integrity-check | capability | draft | Checks whether current public starter bundles stay coherent across manifest contract, verdict wording, evidence coverage, and public selection surfaces. |
| aoa-longitudinal-growth-snapshot | longitudinal | draft | Checks whether ordered, comparable windows on the same bounded workflow surface show modest directional movement without upgrading that movement into broad capability growth. |

## Planned starter bundles

No additional planned starter bundles are currently named publicly.

## Bundle Distinctness Notes

- `aoa-bounded-change-quality` is the composite workflow starter:
  it can observe multiple nearby failure modes together and should not be treated as the precise diagnostic surface for any one of them.
- `aoa-verification-honesty` is the current diagnostic workflow starter for verification truthfulness:
  did the agent claim checks it did not run, overstate coverage, or hide missing verification?
- `aoa-scope-drift-detection` is the current diagnostic boundary starter for scope alignment:
  did the agent silently widen, narrow, or reshape the requested task surface?
- `aoa-ambiguity-handling` is the current diagnostic stress starter for task-meaning ambiguity:
  did the agent ask, bound assumptions, or explicitly branch when requirements were incomplete or conflicting?
- `aoa-approval-boundary-adherence` is the current diagnostic boundary starter for authority ambiguity:
  did the agent classify safe, approval-gated, and out-of-bounds actions correctly without treating uncertainty as permission?
- `aoa-trace-outcome-separation` is the current bounded trace-aware workflow starter:
  are final outcome and execution path being judged separately before any combined reading?
- `aoa-tool-trajectory-discipline` is the current bounded narrower tool-path workflow starter:
  did tool use stay disciplined on cases where the tool path itself matters to the claim?
- `aoa-regression-same-task` is the current regression starter:
  did the candidate materially regress against a frozen baseline on the same bounded task family?
- `aoa-artifact-review-rubric` is the current bounded artifact starter:
  did the produced artifact itself look strong on the visible task surface without implying a strong workflow?
- `aoa-output-vs-process-gap` is the current artifact/process bridge starter:
  is polished output outrunning process discipline, is process outrunning artifact strength, or are the two broadly aligned?
- `aoa-eval-integrity-check` is the current capability starter for eval-bundle coherence:
  do the public starter bundles remain coherent across manifest contract, evidence coverage, and public routing surfaces?
- `aoa-longitudinal-growth-snapshot` is the current longitudinal starter:
  do ordered comparable windows on the same bounded workflow surface show modest directional movement without turning that movement into broad capability growth?
- `aoa-artifact-review-rubric` should stay on artifact quality:
  it should not drift into workflow-proof claims already covered by workflow starters.
- `aoa-output-vs-process-gap` should compare polished outputs against process discipline:
  it should not duplicate the trace/outcome split or the artifact-review surface.
- `aoa-eval-integrity-check` should inspect starter-bundle coherence:
  it should not be read as a direct agent-behavior starter bundle or as proof of canonical readiness.
- `aoa-longitudinal-growth-snapshot` should stay on repeated-window bounded workflow movement:
  it should not be read as a same-task regression surface or as proof of broad capability growth.

## Planned public states

| status | meaning |
|---|---|
| `draft` | The eval idea exists and is documented, but the bundle is not yet stable enough for strong portable claims. |
| `bounded` | The eval has a repeatable execution path, clear boundaries, and a reviewable verdict surface. |
| `portable` | The eval can be reused outside its birth context without losing its main meaning. |
| `baseline` | The eval is stable enough to serve as a comparison surface across changes. |
| `canonical` | The eval is recommended by default for its bounded claim class. |
| `deprecated` | The eval is historically preserved but no longer preferred as the main proof surface. |

## Category notes

- `capability` checks whether a bounded ability is present.
- `workflow` checks multi-step behavior rather than isolated answers.
- `boundary` checks scope, authority, safety, or approval adherence.
- `artifact` checks the quality of produced outputs.
- `regression` checks whether a change made behavior worse.
- `comparative` compares variants, versions, or modes.
- `longitudinal` checks change over time.
- `stress` probes edge conditions, ambiguity, or adversarial surfaces.

## Notes

- `draft` means the bundle shape is being established and the public claim should remain modest.
- `bounded` means the bundle now has a repeatable bounded review path, explicit failure-versus-readout support notes, and a stronger public example readout.
- the current bounded one-run starter tranche now spans composite workflow, diagnostic workflow, boundary, stress, trace/path, and artifact surfaces.
- starter bundles are meant to define the public proof surface, not to maximize repo size quickly.
- future versions may record additional metadata such as scoring surface, baseline mode, portability notes, and known blind spots directly in index-derived artifacts.
