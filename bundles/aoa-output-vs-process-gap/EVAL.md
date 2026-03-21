---
name: aoa-output-vs-process-gap
category: comparative
status: draft
summary: Compares artifact-side and process-side readings on the same bounded cases to show when polished output outruns workflow discipline, process outruns artifact strength, or the two stay aligned.
object_under_evaluation: artifact-versus-process divergence on the same bounded change cases
claim_type: comparative
baseline_mode: peer-compare
report_format: comparative-summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-output-vs-process-gap

## Intent

Use this eval to compare artifact-side and process-side readings on the same bounded change cases.

This draft bundle is a `comparative` bridge eval.
It compares polished output against workflow discipline.
It is not meant to replace the underlying artifact or workflow bundles,
and it is not a root-cause diagnostic surface by itself.

The goal is not to declare one side "the real truth."
The goal is to test one bounded claim:

on the same bounded cases,
the repository can show whether output polish materially outruns workflow discipline,
process discipline materially outruns artifact strength,
or the two stay broadly aligned.

## Object under evaluation

This eval checks artifact-versus-process divergence on the same bounded change cases.

Primary surfaces under evaluation:
- artifact-side reading from `aoa-artifact-review-rubric`
- process-side reading from `aoa-bounded-change-quality`
- divergence pattern between the two readings
- honesty of the comparative summary after both surfaces are reviewed separately

Nearby surfaces intentionally excluded:
- full root-cause diagnosis
- one-run workflow judgment by itself
- one-run artifact judgment by itself
- outcome-versus-path separation as a substitute for artifact/process comparison

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
artifact-side and process-side readings on the same bounded cases
can be compared honestly enough to show whether one materially outruns the other
or whether the two stay broadly aligned.

This eval does **not** support claims such as:
- one side is always more important than the other
- the stronger-looking side proves general capability
- the comparison explains the root cause of every divergence
- the result generalizes automatically to broader task families

## Trigger boundary

Use this eval when:
- the same bounded cases can be reviewed on both artifact and workflow surfaces
- the main question is whether polished output is outrunning process discipline or vice versa
- style-polished output could otherwise be mistaken for strong workflow evidence
- you need a bridge surface rather than a standalone artifact or workflow judgment

Do not use this eval when:
- the main question is the artifact itself rather than the gap
- the main question is end-to-end workflow quality rather than the gap
- the main question is outcome-versus-path separation
- the same bounded case family is not available on both sides of the comparison

## Inputs

- one bounded case family shared by both surfaces
- artifact-side readings from `aoa-artifact-review-rubric`
- process-side readings from `aoa-bounded-change-quality`
- visible case evidence needed to justify both readings
- comparative summary contract

## Fixtures and case surface

This draft bundle should use the same bounded case family for both artifact and process readings.

A strong starter fixture set should include:
- a case where the artifact is strong and the process is weak
- a case where the process is strong and the artifact is modest
- a case where both surfaces are strong
- a case where both surfaces are weak
- a style-polished case where artifact impression risks outrunning process evidence

Fixture families should avoid:
- cases where only one side can be reviewed meaningfully
- heterogeneous case soups that blur the shared comparison surface
- cases where hidden local taste dominates artifact reading
- cases where process review depends on path evidence not available to bounded outside reviewers

The fixture surface is public-safe when:
- a bounded outside reviewer can inspect both readings on the same cases
- the shared case family remains visible and stable enough for peer comparison
- another repo could replace the cases with comparable bounded change tasks and preserve the same comparison posture

## Scoring or verdict logic

This eval prefers comparative per-case notes plus a comparative bundle-level verdict.

Canonical comparative readings for v1:
- `artifact outruns process`
- `process outruns artifact`
- `artifact and process are broadly aligned`
- `mixed comparison signal`

Per-case review should ask:
- what is the artifact-side reading on this case?
- what is the process-side reading on this case?
- does one side materially outrun the other?
- is the divergence real, or is it mostly style or presentation drift?
- does the final comparative summary preserve the same bounded difference visible in the evidence?

Bundle-level reading should stay downstream of per-case comparison notes.
If case evidence materially diverges, prefer `mixed comparison signal` over a cleaner-looking winner.
Use `mixed comparison signal` when the side-by-side read is genuinely split
or when the evidence is too noise-limited to justify a stronger winner.

### Approve signals

Signals toward a clean comparative reading:
- both artifact-side and process-side notes are assigned before the gap reading
- matched conditions stay visible enough that the two side readings remain truly side-by-side
- style-only polish is not mistaken for strong process discipline
- modest artifacts are not auto-downgraded when the process side is clearly stronger
- aligned cases remain aligned instead of being forced into a winner-takes-all read

### Degrade signals

Signals toward `mixed comparison signal`:
- the comparison quietly upgrades polished output into workflow proof
- the comparison quietly upgrades disciplined workflow into artifact excellence
- trace/path divergence is treated as if it were the same thing as artifact/process divergence
- matched conditions drift enough that the side-by-side read stops being trustworthy
- the comparative summary names a winner where the evidence is actually mixed or noisy

## Baseline or comparison mode

This starter bundle uses `peer-compare`.

In v1, the peer surfaces are:
- artifact side: `aoa-artifact-review-rubric`
- process side: `aoa-bounded-change-quality`

Neither side is the default truth source.
The point is the bounded divergence or alignment between them on the same cases.

`aoa-trace-outcome-separation` is a nearby follow-up reader,
but it is not the default paired process surface in v1.

Matched conditions should stay explicit:
- the same bounded case family
- the same evaluated run family
- the same review frame before any gap summary is assigned

## Execution contract

A careful run should:
1. choose one bounded case family shared by both sides
2. assign artifact-side readings with `aoa-artifact-review-rubric`
3. assign process-side readings with `aoa-bounded-change-quality`
4. derive a per-case gap reading only after both side readings exist
5. derive a bundle-level comparative verdict from the per-case comparison notes
6. publish a comparative-summary artifact with explicit interpretation limits

Execution expectations:
- do not let one side silently stand in for the other
- do not use trace/path separation as if it were the same comparative question
- do not force every case into a winner when alignment or mixed evidence is more truthful
- keep enough side-by-side evidence that a careful reviewer can see why each gap reading was assigned

## Outputs

The eval should produce:
- one bundle-level comparative verdict
- per-case comparison notes
- artifact-side reading for each case
- process-side reading for each case
- gap reading for each case
- explicit interpretation note

A compact public comparative-summary may include:
- case id
- artifact-side reading
- process-side reading
- gap reading
- bundle-level verdict
- caution about what the result still does not prove

## Failure modes

This eval can fail as an instrument when:
- the two sides are not actually reading the same bounded case family
- hidden house-style preference dominates the artifact side
- process-side evidence is too thin for a fair peer comparison
- matched conditions are named loosely enough that the side-by-side read becomes performative
- trace/path divergence is mistaken for artifact/process divergence
- the summary turns the bridge into a winner-takes-all scoreboard
- one vivid divergent case is treated as the whole story

## Blind spots

This eval does not prove:
- root-cause diagnosis for why one side outran the other
- one-run artifact quality by itself
- one-run workflow quality by itself
- outcome-versus-path separation as its own question
- stable cross-family ranking unless used later in a stronger comparative form

Likely false-pass path:
- artifact and process look aligned on the chosen cases, but both are only modest on a broader unseen surface.

Likely misleading-result path:
- style polish can still distort the artifact side if reviewers stop reading the process evidence carefully.

Nearby claim classes that should use a different bundle instead:
- produced artifact quality should use `aoa-artifact-review-rubric`
- end-to-end workflow quality should use `aoa-bounded-change-quality`
- outcome-versus-path separation should use `aoa-trace-outcome-separation`

## Interpretation guidance

Treat a positive comparative result as support for one bounded claim:
on this shared case family,
artifact-side and process-side readings can be compared honestly enough to show divergence or alignment.

Do not treat a positive comparative result as:
- proof that one side matters more in all contexts
- proof that the stronger-looking side explains the whole story
- proof of general capability growth or decline
- proof that trace/path separation no longer matters

Use this bundle together with `aoa-trace-outcome-separation`
when you need a follow-up read on whether the process side looks weak because path and outcome diverged internally.

Do not treat this bridge as a baseline-default comparator.
It remains a draft side-by-side surface even when the paired workflow or artifact starters are stronger individually.

A negative or mixed result is valuable because it can reveal:
- polished output outrunning workflow discipline
- disciplined process outrunning artifact strength
- false winner-takes-all summaries
- comparison noise that should stay bounded

## Verification

- confirm the bounded claim is explicit
- confirm the same bounded case family is used on both sides
- confirm artifact-side and process-side readings exist before any gap reading
- confirm matched conditions stay explicit enough for a real side-by-side interpretation
- confirm the bundle-level verdict does not outrun the comparison evidence
- confirm blind spots and nearby-bundle boundaries are named clearly

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local shared case families
- local comparative summary formats that still preserve both side readings
- repo-specific artifact or workflow rubrics
- follow-up readers for why one side outran the other
- later stronger peer-comparison discipline
