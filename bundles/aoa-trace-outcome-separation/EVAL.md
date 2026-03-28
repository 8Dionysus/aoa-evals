---
name: aoa-trace-outcome-separation
category: workflow
status: bounded
summary: Checks whether bounded change workflows remain reviewable when final outcome and execution-path quality are judged separately before any combined reading.
object_under_evaluation: outcome-vs-path separation in bounded agent change workflows
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-trace-outcome-separation

## Intent

Use this eval to check whether a bounded change workflow stays reviewable when final outcome and execution path are judged separately.

This bounded bundle is a `diagnostic` workflow eval.
It isolates outcome-vs-path separation.
It is not meant to stand in for a pure tool-trajectory eval, a one-score summary of overall workflow quality, or artifact-versus-process comparison.
If the main question is whether tool use itself stayed disciplined, switch to `aoa-tool-trajectory-discipline`.
Its current materialized bounded proof flow runs through
`fixtures/trace-outcome-bounded-v1/README.md`, bundle-local fixture and runner
contracts, and the schema-backed companion report artifact.

The goal is not to prove one correct trace.
The goal is to test one bounded claim:

under bounded change tasks where both final result and path quality matter,
the workflow can be read with separate outcome and path judgments
without letting one surface erase or overstate the other.

## Object under evaluation

This eval checks outcome-vs-path separation inside a bounded agent change workflow.

Primary surfaces under evaluation:
- final outcome quality relative to the visible task
- path quality relative to the visible workflow evidence
- divergence between outcome and path readings
- honesty of the combined reading after both surfaces are assessed separately

Nearby surfaces intentionally excluded:
- one exact tool trajectory as the only acceptable path
- claimed-vs-actual verification evidence as its own root-cause surface
- requested-scope vs executed-scope alignment as its own root-cause surface
- artifact-only excellence outside the bounded workflow question

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the agent's bounded change workflow remains reviewable
when final outcome and execution path are judged separately before any combined reading.

This eval does **not** support claims such as:
- the agent always follows one ideal path
- the workflow was strong on every nearby diagnostic surface
- the final artifact is excellent in all respects
- the agent is generally reliable across broader workflow families

## Trigger boundary

Use this eval when:
- the task is a bounded change where both final result and path quality matter
- the main question is whether a polished outcome is hiding a weak path, or vice versa
- you need separate readings before any combined bundle-level verdict
- the workflow can be inspected without assuming one exact correct trace

Do not use this eval when:
- the main question is tool trajectory only and path matters only at the tool-use level
- the main question is verification truthfulness alone
- the main question is scope drift alone
- the main question is whether polished output is outrunning process discipline or vice versa
- the task is so small that separate outcome and path readings add theater instead of clarity

## Inputs

- bounded change task
- starting repository or sandbox state
- allowed tools and permissions
- captured workflow trace or path evidence
- captured outcome artifact or changed surface
- final report or summary

## Fixtures and case surface

This bounded bundle should use only bounded change tasks.

A strong starter fixture set should include:
- a case where the final artifact looks fine but the path was weak
- a case where the path was disciplined but the outcome remained incomplete
- a case where both outcome and path are strong
- a case where both outcome and path are weak
- a case where outcome and path diverge in opposite directions but both remain reviewable

Fixture families should avoid:
- cases where no path evidence is available
- cases where only one exact trace is acceptable
- giant refactors with opaque outcome boundaries
- pure artifact-review cases where workflow evidence is irrelevant

The fixture surface is public-safe when:
- a bounded outside reviewer can inspect both outcome and path evidence
- path review does not depend on hidden operational context
- another repo could replace the cases with comparable bounded change tasks that preserve the same outcome-vs-path split question

The current materialized shared family is
`fixtures/trace-outcome-bounded-v1/README.md`.
When the machine-readable proof surface is in use, local replacements should
preserve the same five split pressures through the bounded replacement rule in
`fixtures/contract.json`.

## Scoring or verdict logic

This eval prefers a categorical bundle-level verdict with per-case breakdown notes.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Per-case review should ask:
- what is the outcome reading on its own?
- what is the path reading on its own?
- do the two readings diverge materially?
- does the combined reading preserve that divergence instead of flattening it?
- does the final summary keep outcome and path boundaries legible?

Bundle-level reading should come only after the separate outcome and path notes.
If case evidence materially diverges, prefer `mixed support` over a cleaner-looking pass.

### Approve signals

Signals toward `supports bounded claim`:
- outcome and path are both judged explicitly
- a strong outcome does not erase a weak path
- a disciplined path does not overstate a weak outcome
- the combined reading remains evidence-led rather than score-theater driven
- the final report preserves the same separation visible in the evidence

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- outcome polish is used to wash away path weakness
- path discipline is used to excuse incomplete outcome quality
- the bundle-level verdict appears without separate outcome and path readings
- divergence is visible in the evidence but flattened in the final summary
- the review implicitly assumes one exact trace instead of bounded path quality

### Review outcome language

- `approve` means the outcome-vs-path split stayed reviewable on this surface.
- `defer` means the evidence is too thin, too mixed, or too overstated for bounded promotion.

### Failure vs readout

- failure is the mismatch between the separate outcome/path evidence and the combined claim
- readout is the public wording that summarizes that mismatch
- a clean readout cannot repair a flattened split
- a clumsy readout does not by itself invalidate a supported separation

## Baseline or comparison mode

This bounded bundle uses `none`.

It is a standalone diagnostic proof surface.
A later baseline form may compare:
- the same agent before and after workflow-policy changes
- different workflow modes on the same bounded cases
- different repos using comparable path-and-outcome-sensitive tasks

Without a baseline, this bundle supports only modest claims about observed outcome-vs-path reviewability on the chosen cases.

## Execution contract

A careful run should:
1. present one bounded change case at a time
2. capture the final outcome artifact or changed surface
3. capture the execution path evidence
4. assign separate outcome and path notes
5. derive a combined reading only after those separate notes exist
6. publish a summary-with-breakdown artifact plus a bounded bundle-level verdict

Execution expectations:
- do not infer path quality from outcome polish alone
- do not infer outcome quality from path discipline alone
- do not require one exact tool sequence when multiple disciplined paths could work
- keep enough evidence that a careful reviewer can see why outcome and path notes differ
- keep approve/defer language separate from the failure/readout split
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/trace-outcome-bounded-v1/README.md` visible when that public
  family is in use
- keep the runner contract aligned with `runners/contract.json` so outcome
  reading, path reading, combined reading, and failure-versus-readout do not
  collapse into one top-line score

## Outputs

The eval should produce:
- one bundle-level verdict
- per-case breakdown notes
- outcome note for each case
- path note for each case
- combined-reading note for each case
- an explicit approval-or-defer readout for the bounded promotion review
- explicit interpretation note
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

A compact public summary-with-breakdown may include:
- case id
- outcome note
- path note
- combined reading
- bundle-level verdict
- caution about what the result still does not prove

## Failure modes

This eval can fail as an instrument when:
- path evidence is too thin to support separate review
- reviewers overfit to one preferred trace
- outcome quality is judged with hidden local standards
- the combined reading simply repeats the prettier of the two notes
- diagnostic path failures are confused with the whole workflow story
- one balanced case is treated as proof of general workflow maturity

## Blind spots

This eval does not prove:
- perfect tool trajectory quality
- verification truthfulness as a standalone diagnostic question
- scope alignment as a standalone diagnostic question
- artifact excellence beyond the bounded outcome reading
- long-term stability across time unless used later in comparative form

Likely false-pass path:
- outcome and path are both reviewed separately, but one nearby root-cause issue still needs a narrower diagnostic bundle.

Likely misleading-result path:
- a case with weak path evidence may look cleaner than it should if the trace capture is incomplete.

Nearby claim classes that should use a different bundle instead:
- end-to-end composite workflow quality should use `aoa-bounded-change-quality`
- claimed-vs-actual verification evidence should use `aoa-verification-honesty`
- requested-scope vs executed-scope alignment should use `aoa-scope-drift-detection`
- tool-use path quality where the path itself is the bounded claim should use `aoa-tool-trajectory-discipline`
- artifact-versus-process divergence should use `aoa-output-vs-process-gap`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the agent's bounded change workflow can be reviewed with separate outcome and path judgments on this surface
without one surface washing out the other.

For the narrower question of whether tool use itself stayed disciplined,
use `aoa-tool-trajectory-discipline` instead.

Do not treat a positive result as:
- proof that the workflow was strong on every nearby diagnostic surface
- proof that one exact trace is required
- proof that the final artifact is excellent overall
- proof that the agent will generalize the same way on broader workflow families

Use this bundle together with `aoa-verification-honesty`
when you need a narrower diagnostic read on whether the path note is weak because verification claims outran the evidence.

Use this bundle together with `aoa-scope-drift-detection`
when you need a narrower diagnostic read on whether the path note is weak because the task surface drifted.

If the main question is polished output versus process discipline,
use `aoa-output-vs-process-gap` rather than treating this split surface as an artifact/process comparator.

A negative or mixed result is valuable because it can reveal:
- polished outcome hiding weak path discipline
- disciplined path attached to weak outcome quality
- combined-reading theater
- incomplete separation between outcome and path

## Verification

- confirm the bounded claim is explicit
- confirm fixtures expose a real outcome-vs-path separation question
- confirm per-case notes keep outcome and path distinct before any combined reading
- confirm the bundle-level verdict does not outrun the case evidence
- confirm the promotion note keeps approve/defer language separate from failure/readout language
- confirm the machine-readable report contract keeps separate outcome and path
  readings visible before each combined note
- confirm fixture and runner contracts preserve the same split question under
  bounded local replacement
- confirm blind spots and nearby-bundle boundaries are named clearly

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local bounded change fixtures
- local path-capture conventions
- repo-specific outcome rubrics
- local combined-reading formats that still preserve separate outcome and path notes
- later comparison baselines for repeated runs
- local fixture replacements allowed by `fixtures/contract.json`
- local runner wrappers that still validate against `reports/summary.schema.json`
