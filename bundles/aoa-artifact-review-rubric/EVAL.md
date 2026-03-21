---
name: aoa-artifact-review-rubric
category: artifact
status: bounded
summary: Checks whether a produced artifact on a bounded change task is reviewably strong on the visible task surface without treating polish as proof of workflow discipline.
object_under_evaluation: produced artifact quality on bounded agent change tasks
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-artifact-review-rubric

## Intent

Use this eval to check whether a produced artifact on a bounded change task is strong on the visible task surface.

This bounded bundle is a `diagnostic` artifact eval.
It isolates artifact quality.
It is not meant to stand in for workflow discipline, path quality, or authority handling.

The goal is not to prove total engineering quality.
The goal is to test one bounded claim:

under bounded change tasks,
the produced artifact can be reviewably strong on the visible task surface
without turning artifact polish into proof of workflow discipline.

## Object under evaluation

This eval checks produced artifact quality on bounded agent change tasks.

Primary surfaces under evaluation:
- task fit to the visible request
- internal coherence and obvious defect load
- bounded completeness on the visible task surface
- reviewability and readability of the produced artifact

Nearby surfaces intentionally excluded:
- claimed-vs-actual verification evidence
- requested-scope vs executed-scope alignment
- authority or approval ambiguity
- hidden process-discipline claims
- any reading of "good artifact implies good workflow"

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the produced artifact is reviewably strong on the visible task surface
without implying that the underlying workflow was strong in every respect.

This eval does **not** support claims such as:
- the workflow was disciplined end to end
- the agent handled scope perfectly
- the verification story was honest
- the agent is generally strong across broader artifact classes
- the produced artifact is globally optimal

## Trigger boundary

Use this eval when:
- the task is a bounded change and the main question is the produced artifact itself
- the visible request is clear enough to judge task fit and bounded completeness
- readability or reviewability of the artifact matters to the claim
- you want artifact quality without importing hidden workflow judgments

Do not use this eval when:
- the main question is workflow discipline rather than artifact quality
- the main question is whether polished output is outrunning process discipline
- the main question is scope alignment, verification truthfulness, or authority handling
- the artifact cannot be reviewed without large hidden local context

## Inputs

- bounded change task
- visible request or acceptance surface
- produced artifact or changed surface
- optional artifact-review rubric notes
- final report only as supporting context, not as a substitute for artifact inspection

## Fixtures and case surface

This bounded bundle should use bounded change artifacts on the same general task family as the current workflow bundles.

A strong starter fixture set should include:
- an artifact that looks polished and is actually solid on the visible task surface
- an artifact that looks polished but has visible bounded weaknesses
- an artifact that is modest but disciplined and fit for the ask
- an artifact where readability or reviewability is the main bounded issue

For the current artifact/process paired proof flow,
this bundle can reuse `fixtures/bounded-change-paired-v1/README.md`
when the same cases also need workflow-side and bridge-side reads.

Fixture families should avoid:
- giant artifacts with unbounded review burden
- hidden house-style cases where only insiders know the expected artifact shape
- pure process questions where the artifact itself is not the review target
- authority or safety cases where artifact judgment is secondary to execution policy

The fixture surface is public-safe when:
- a bounded outside reviewer can inspect the produced artifact directly
- the visible task surface is enough to judge bounded fit and completeness
- another repo could replace the cases with comparable bounded change artifacts and preserve the same rubric surface

## Scoring or verdict logic

This eval prefers rubric-axis notes plus a bounded bundle-level verdict.
It uses a `mixed` result shape because the axis-level reading should stay visible rather than collapse into a single scalar score.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Canonical rubric axes for v1:
- task fit to the visible request
- internal coherence and obvious defect load
- bounded completeness on the visible task surface
- reviewability and readability of the produced artifact

Per-case review should ask:
- does the artifact fit the visible request?
- does it show obvious bounded defects or internal contradictions?
- is it complete enough on the visible task surface?
- is it readable and reviewable enough for bounded outside inspection?
- does the bundle-level verdict stay weaker than the strongest-looking single axis?

Bundle-level reading should stay downstream of the axis notes.
If case evidence or axis evidence materially diverges, prefer `mixed support` over a cleaner-looking pass.

### Approve signals

Signals toward `supports bounded claim`:
- the artifact fits the visible request closely
- obvious bounded defects are absent or minor
- the visible task surface is completed well enough for the bounded ask
- the artifact remains readable and reviewable to a bounded outside reviewer

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- the artifact looks polished but misses visible task requirements
- bounded defects or contradictions remain visible on inspection
- completeness is weak even though presentation looks clean
- reviewability is poor enough that the artifact is hard to trust or check
- the readout quietly upgrades polish into workflow proof

### Review outcome language

- `approve` means the artifact-side readout stayed reviewable on this surface.
- `defer` means the evidence is too thin, too mixed, or too overstated for bounded promotion.

### Failure vs readout

- failure is the mismatch between the artifact claim and the visible artifact evidence
- readout is the public wording that summarizes that mismatch
- a clean readout cannot repair missed visible requirements
- a clumsy readout does not by itself invalidate a supported artifact judgment

## Baseline or comparison mode

This bounded bundle uses `none`.

It is a standalone diagnostic proof surface.
A later comparison form may compare:
- the same agent across comparable artifact families
- alternate output styles on the same bounded cases
- artifact-side versus process-side readings on the same cases

Without a baseline, this bundle supports only modest claims about observed artifact quality on the chosen cases.
For artifact-versus-process divergence on the same cases,
use `aoa-output-vs-process-gap`.

## Execution contract

A careful run should:
1. present one bounded change case at a time
2. capture the visible request surface
3. capture the produced artifact directly
4. review the artifact against the rubric axes
5. assign a per-case note plus a bounded bundle-level verdict
6. publish a summary-with-breakdown artifact with explicit interpretation limits

Execution expectations:
- do not infer workflow strength from artifact polish alone
- do not let the final summary erase a weak rubric axis
- do not use hidden local standards as if they were part of the visible request
- keep enough evidence that a careful reviewer can see why each rubric axis was judged the way it was
- keep approve/defer language separate from the failure/readout split
- when shipping a machine-readable report, validate it against `reports/summary.schema.json`

## Outputs

The eval should produce:
- one bundle-level verdict
- per-case breakdown notes
- rubric-axis notes for each case
- artifact-strength summary
- an explicit approval-or-defer readout for the bounded promotion review
- explicit limitations note
- an optional schema-backed companion report artifact at `reports/example-report.json`

A compact public summary-with-breakdown may include:
- case id
- task-fit note
- coherence note
- completeness note
- reviewability note
- per-case note
- bundle-level verdict

## Failure modes

This eval can fail as an instrument when:
- the visible request is too thin to support bounded artifact review
- reviewers reward polish over bounded defect load
- hidden local expectations dominate the reading
- rubric axes overlap too much to stay distinct
- one beautiful artifact is treated as proof of strong workflow discipline
- summary language upgrades artifact quality into general competence claims

## Blind spots

This eval does not prove:
- overall workflow discipline
- verification truthfulness
- scope alignment
- authority handling quality
- stable strength across broader artifact families unless used later in comparative form

Likely false-pass path:
- the artifact looks strong on the visible surface, but the workflow that produced it was still weak.

Likely misleading-result path:
- a modest but fit-for-ask artifact may be underrated if reviewers over-prefer polish or house style.

Nearby claim classes that should use a different bundle instead:
- end-to-end workflow quality should use `aoa-bounded-change-quality`
- output polish versus process discipline should use `aoa-output-vs-process-gap`
- outcome-versus-path separation should use `aoa-trace-outcome-separation`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the produced artifact is reviewably strong on this visible task surface.

Do not treat a positive result as:
- proof that the workflow was disciplined
- proof that verification was honest
- proof that the agent handled authority or scope well
- proof that the artifact is globally optimal

Use this bundle together with `aoa-bounded-change-quality`
when you need both:
- an artifact-quality reading
- and an end-to-end workflow reading

Use this bundle together with `aoa-output-vs-process-gap`
when you need to know whether artifact polish is outrunning process discipline or vice versa.

For the first materialized paired proof flow,
use `reports/artifact-process-paired-proof-flow-v1.md`
so artifact and workflow reads stay independent before the bridge summary.

A negative or mixed result is valuable because it can reveal:
- polished incompleteness
- visible bounded defects
- poor reviewability
- artifact strength that is weaker than the presentation suggests

## Verification

- confirm the bounded claim is explicit
- confirm the visible request is enough to support artifact review
- confirm rubric axes stay distinct and reviewable
- confirm the bundle-level verdict does not outrun axis or case evidence
- confirm the promotion note keeps approve/defer language separate from failure/readout language
- confirm blind spots and nearby-bundle boundaries are named clearly

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local artifact-review rubrics
- local bounded artifact families
- repo-specific readability expectations
- local summary formats that still preserve axis-level evidence
- later comparison baselines for repeated runs
- local fixture replacements allowed by `fixtures/contract.json`
- local runner wrappers that still validate against `reports/summary.schema.json`
