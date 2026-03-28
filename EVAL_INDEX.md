# EVAL_INDEX

This file is the repository-wide map of public eval bundles.

## Starter eval bundles

| name | category | status | summary |
|---|---|---|---|
| aoa-bounded-change-quality | workflow | portable | Checks whether a non-trivial agent change holds together as one bounded end-to-end workflow signal without treating that composite read as a precise diagnostic surface. |
| aoa-verification-honesty | workflow | portable | Checks whether an agent truthfully reports which verification steps on a bounded change task were executed, skipped, or blocked. |
| aoa-scope-drift-detection | boundary | bounded | Checks whether an agent keeps requested scope aligned with executed scope on bounded change tasks, or explicitly discloses deviation. |
| aoa-ambiguity-handling | stress | bounded | Checks whether an agent handles incomplete, conflicting, or underspecified task meaning on bounded change tasks without silently choosing an unearned path. |
| aoa-approval-boundary-adherence | boundary | bounded | Checks whether an agent correctly distinguishes safe action, explicit-approval-required action, and out-of-bounds action. |
| aoa-trace-outcome-separation | workflow | bounded | Checks whether bounded change workflows remain reviewable when final outcome and execution-path quality stay separately readable before any combined reading, rather than grading the tool path itself. |
| aoa-tool-trajectory-discipline | workflow | bounded | Checks whether an agent uses tools in a disciplined, reviewable way on bounded tasks where the tool path itself is part of the bounded claim, rather than acting as a general outcome-versus-path splitter. |
| aoa-witness-trace-integrity | workflow | draft | Checks whether a public witness trace for a bounded run keeps meaningful steps, tool visibility, state deltas, failures, redaction posture, and the markdown summary aligned enough for review. |
| aoa-regression-same-task | regression | baseline | Compares a candidate against a frozen baseline on the same bounded task family to detect material regression without claiming general growth. |
| aoa-artifact-review-rubric | artifact | portable | Checks whether a produced artifact on a bounded change task is reviewably strong on the visible task surface without treating artifact quality as proof of workflow discipline or as an artifact/process bridge. |
| aoa-compost-provenance-preservation | artifact | draft | Checks whether witness-derived compost artifacts preserve provenance, review state, limits, and contradiction posture as they move toward note, principle, or canon-candidate surfaces. |
| aoa-output-vs-process-gap | comparative | draft | Compares artifact-side and process-side readings on the same bounded cases as a bridge surface, not as a replacement for standalone artifact review, standalone workflow review, or baseline comparison. |
| aoa-eval-integrity-check | capability | bounded | Checks whether current public starter bundles stay coherent as eval surfaces across manifest contract, verdict wording, evidence coverage, and public routing; this bounded integrity sidecar now travels with comparison-spine wording waves. |
| aoa-longitudinal-growth-snapshot | longitudinal | draft | Checks whether ordered, comparable windows on the same bounded workflow surface show modest directional movement without upgrading that movement into broad capability growth. |

## Planned starter bundles

No additional planned starter bundles are currently named publicly.

## Comparison Spine

The current comparison spine is a bounded program layer, not a loose pile of comparison bundles.

Read it as:
- one-run anchor surfaces before any comparison layer
- `aoa-regression-same-task` for the frozen-baseline default
- `aoa-output-vs-process-gap` for matched peer comparison on the same bounded cases
- `aoa-longitudinal-growth-snapshot` for ordered repeated-window movement on one named bounded workflow surface
- `aoa-eval-integrity-check` as the bounded integrity sidecar whenever public wording, routing, or maturity posture could otherwise overstate the comparison read

Public discipline:
- `aoa-regression-same-task` remains the only default public `baseline` surface
- `aoa-output-vs-process-gap` remains draft and should not inherit baseline status by association
- `aoa-longitudinal-growth-snapshot` remains draft and should not inherit growth claims by association
- `aoa-eval-integrity-check` remains the comparison-spine sidecar, not a replacement for direct comparison evidence

## Artifact Process Layer

The current artifact/process layer is also a bounded program layer rather than three unrelated starter bundles.

Read it as:
- `aoa-artifact-review-rubric` for the artifact-side reading
- `aoa-bounded-change-quality` for the process-side reading
- `aoa-output-vs-process-gap` only after both standalone readings exist
- `aoa-witness-trace-integrity` as adjacent upstream witness context when needed
- `aoa-compost-provenance-preservation` as adjacent downstream compost context when needed

Public discipline:
- artifact polish does not prove workflow discipline
- workflow discipline does not prove artifact excellence
- witness integrity does not replace workflow discipline
- compost provenance does not replace artifact review

## Bundle Distinctness Notes

- `aoa-bounded-change-quality` is the current portable composite workflow anchor:
  it answers whether one bounded change workflow held together end to end and can observe multiple nearby failure modes together.
  It should not be treated as the precise diagnostic surface for verification truthfulness, scope drift, or task-meaning ambiguity.
- `aoa-verification-honesty` is the current portable diagnostic workflow starter for verification truthfulness:
  did the agent claim checks it did not run, overstate coverage, or hide missing verification?
  Its materialized one-run proof flow now anchors on `fixtures/verification-honesty-v1/README.md`, a bundle-local runner contract, a schema-backed report example, and a portable review that preserves its narrower diagnostic boundary.
- `aoa-scope-drift-detection` is the current diagnostic boundary starter for scope alignment:
  did the agent silently widen, narrow, or reshape the requested task surface?
  Its materialized bounded proof flow now anchors on `fixtures/scope-drift-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example while staying narrower than workflow, verification, or ambiguity reads.
- `aoa-ambiguity-handling` is the current diagnostic stress starter for task-meaning ambiguity:
  did the agent ask, bound assumptions, or explicitly branch when requirements were incomplete or conflicting?
  Its materialized bounded proof flow now anchors on `fixtures/ambiguity-bounded-v1/README.md`, a bundle-local runner contract, and a schema-backed report example while staying narrower than authority, scope, or workflow reads.
- `aoa-approval-boundary-adherence` is the current diagnostic boundary starter for authority ambiguity:
  did the agent classify safe, approval-gated, and out-of-bounds actions correctly without treating uncertainty as permission?
- `aoa-trace-outcome-separation` is the current bounded trace-aware workflow starter:
  are final outcome and execution path being judged separately before any combined reading?
  Use it when the main question is the split itself, not when the tool path must be graded as its own bounded surface.
- `aoa-tool-trajectory-discipline` is the current bounded narrower tool-path workflow starter:
  did tool use stay disciplined on cases where the tool path itself matters to the claim?
  It should not be read as the general outcome-versus-path split surface.
- `aoa-witness-trace-integrity` is the current draft witness workflow starter:
  did a bounded run leave a reviewable witness trace with meaningful steps, visible tool use, explicit external effects, preserved failures, and an honest markdown summary?
  Its materialized draft proof flow now anchors on `fixtures/witness-trace-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
  It should not be read as proof of outcome quality, as a substitute for future runtime instrumentation, or as the default process-side read in the artifact/process layer.
- `aoa-regression-same-task` is the current baseline regression starter:
  did the candidate materially regress against a frozen baseline on the same bounded task family?
  Its current machine-readable comparison surface is anchored in `aoa-bounded-change-quality` and its materialized proof flow runs through `fixtures/frozen-same-task-v1/README.md`, `reports/example-report.json`, and `reports/same-task-baseline-proof-flow-v1.md`.
- `aoa-artifact-review-rubric` is the current portable artifact anchor:
  did the produced artifact itself look strong on the visible task surface without implying a strong workflow?
  Start here when the question is artifact quality itself; do not skip straight to the bridge surface.
  Its shared paired families now include `fixtures/bounded-change-paired-v1/README.md` and `fixtures/bounded-change-paired-v2/README.md`, but the bundle remains the standalone artifact-side read rather than the bridge.
- `aoa-compost-provenance-preservation` is the current draft compost artifact starter:
  did a witness-derived note, synthesis, or principle candidate preserve provenance, review state, current limits, and demotion posture?
  Its materialized draft proof flow now anchors on `fixtures/compost-provenance-v1/README.md`, a bundle-local runner contract, and a schema-backed report example.
  It should not be read as proof of canon-readiness, as a replacement for general artifact review, or as the default artifact-side read in the artifact/process layer.
- `aoa-output-vs-process-gap` is the current artifact/process bridge starter:
  is polished output outrunning process discipline, is process outrunning artifact strength, or are the two broadly aligned?
  It should be read after the standalone artifact and workflow surfaces, not as a replacement for them, and not as a baseline-by-association surface.
  Its materialized bridge now spans `fixtures/bounded-change-paired-v1/README.md`, `fixtures/bounded-change-paired-v2/README.md`, `reports/artifact-process-paired-proof-flow-v1.md`, and `reports/artifact-process-paired-proof-flow-v2.md`, but the bundle remains draft.
- `aoa-eval-integrity-check` is the current bounded integrity sidecar starter:
  do the public starter bundles remain coherent across manifest contract, evidence coverage, public routing, and semantic anti-theater risks, especially across the comparison spine?
  It is a meta-eval for public starter bundles, not a direct agent-behavior starter and not proof of canonical readiness.
- `aoa-longitudinal-growth-snapshot` is the current longitudinal starter:
  do ordered comparable windows on the same bounded workflow surface show modest directional movement without turning that movement into broad capability growth?
  Its current machine-readable comparison surface is anchored in `aoa-bounded-change-quality` and its materialized proof flow runs through `fixtures/repeated-window-bounded-v1/README.md`, `reports/example-report.json`, `reports/repeated-window-proof-flow-v1.md`, and `reports/repeated-window-proof-flow-v2.md`, but the bundle remains draft.
- `aoa-artifact-review-rubric` should stay on artifact quality:
  it should not drift into workflow-proof claims already covered by workflow starters.
- `aoa-witness-trace-integrity` should stay on public witness reviewability:
  it should not drift into outcome grading, hidden-runtime completeness, or compost quality claims.
- `aoa-compost-provenance-preservation` should stay on provenance-preserving compost artifacts:
  it should not drift into philosophical proof, canon-readiness, or general artifact grading detached from provenance.
- `aoa-output-vs-process-gap` should compare polished outputs against process discipline:
  it should not duplicate the trace/outcome split or the artifact-review surface.
- `aoa-eval-integrity-check` should inspect starter-bundle coherence and semantic overreach:
  it should not be read as a direct agent-behavior starter bundle or as proof of canonical readiness.
- `aoa-long-horizon-depth` should stay on checkpoint-based restart fidelity:
  it should not drift into final-answer grading, runtime-instrumentation completeness, or general philosophical depth claims.
- `aoa-return-anchor-integrity` should stay on return-anchor fidelity and honest re-entry:
  it should not drift into final-answer grading, checkpoint-only restart fidelity, scope diagnosis, approval classification, or post-return verification claims.
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
- `artifact` checks the quality or provenance-preserving integrity of produced outputs.
- `regression` checks whether a change made behavior worse.
- `comparative` compares variants, versions, or modes.
- `longitudinal` checks change over time.
- `stress` probes edge conditions, ambiguity, or adversarial surfaces.

## Notes

- `draft` means the bundle shape is being established and the public claim should remain modest.
- `bounded` means the bundle now has a repeatable bounded review path, explicit failure-versus-readout support notes, and a stronger public example readout.
- the current portable one-run anchors are `aoa-bounded-change-quality` and `aoa-artifact-review-rubric`, and the current portable diagnostic workflow starter is `aoa-verification-honesty`.
- the current bounded one-run diagnostics remain `aoa-scope-drift-detection`, `aoa-ambiguity-handling`, `aoa-approval-boundary-adherence`, `aoa-trace-outcome-separation`, `aoa-tool-trajectory-discipline`, and `aoa-eval-integrity-check`.
- `aoa-scope-drift-detection` now also has a materialized bounded proof flow in `fixtures/scope-drift-bounded-v1/README.md`, bundle-local fixture and runner contracts, and schema-backed report artifacts while staying `bounded` and `local-shaped`.
- `aoa-ambiguity-handling` now also has a materialized bounded proof flow in `fixtures/ambiguity-bounded-v1/README.md`, bundle-local fixture and runner contracts, and schema-backed report artifacts while staying `bounded` and `local-shaped`.
- the witness/compost pilot pair now has materialized draft proof surfaces in `aoa-witness-trace-integrity` and `aoa-compost-provenance-preservation`.
- checkpoint-based restart fidelity now has its first draft public bundle in `aoa-long-horizon-depth`, but it is not part of the current starter set.
- return-aware anchor fidelity now has its first materialized draft public bundle in `aoa-return-anchor-integrity`, anchored by `fixtures/return-anchor-v1/README.md`, bundle-local fixture and runner contracts, and schema-backed report artifacts, but it is not part of the current starter set.
- the first materialized paired proof flow now sits across `aoa-artifact-review-rubric`, `aoa-bounded-change-quality`, and `aoa-output-vs-process-gap` using shared fixtures, runner contracts, and schema-backed report examples.
- the artifact/process layer now also carries a second matched family and second paired dossier so the bridge can deepen without changing `peer_surfaces` or promoting by association.
- the comparison spine now also has materialized proof flows for `aoa-regression-same-task`, `aoa-output-vs-process-gap`, and `aoa-longitudinal-growth-snapshot` through shared fixture families, runner contracts, schema-backed report examples, and the shared read-order artifact `reports/comparison-spine-proof-flow-v1.md`.
- the repeated-window layer now also carries a second shared dossier with explicit transition-note discipline so comparability stays visible before any top-line movement story.
- the current first public `baseline` starter is `aoa-regression-same-task`; other comparative and longitudinal starters remain draft.
- `aoa-eval-integrity-check` is now bounded as the public integrity sidecar for semantic overreach and public-surface drift.
- starter bundles are meant to define the public proof surface, not to maximize repo size quickly.
- the comparison spine now also ships machine-readable comparison metadata through `generated/comparison_spine.json`.
- future versions may record additional metadata such as scoring surface, baseline mode, portability notes, and known blind spots directly in index-derived artifacts.
