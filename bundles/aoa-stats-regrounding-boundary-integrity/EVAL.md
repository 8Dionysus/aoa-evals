---
name: aoa-stats-regrounding-boundary-integrity
category: boundary
status: draft
summary: Checks whether stats-derived re-grounding signals preserve the split between stats observability, SDK policy, routing advisory hints, and bounded eval proof verdicts.
object_under_evaluation: stats-driven re-grounding consumer boundary across aoa-stats, aoa-sdk, aoa-routing, and aoa-evals
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-stats-regrounding-boundary-integrity

## Intent

Use this eval when a consumer starts reading `aoa-stats` surface profiles or
source coverage as a trigger to re-ground before risky work.

This bundle checks the boundary of that pattern. It asks whether stats remains
derived observability, SDK owns policy application, routing remains advisory,
and evals remains bounded proof.

## Object under evaluation

This eval checks the stats-driven re-grounding consumer boundary across
`aoa-stats`, `aoa-sdk`, `aoa-routing`, and `aoa-evals`.

Primary surfaces under evaluation:

- `aoa-stats/generated/summary_surface_catalog.min.json`
- `aoa-stats/generated/source_coverage_summary.min.json`
- SDK-facing re-grounding signal or policy output
- `aoa-routing/generated/stats_regrounding_hints.min.json`
- this eval bundle's verdict wording and report shape

Nearby surfaces intentionally excluded:

- owner-local receipt truth
- final owner object quality
- route approval
- proof verdicts for the underlying owner work
- broad health or readiness scoring for the federation

## Bounded claim

This eval can support a claim like:

for this bounded consumer path, stats-derived surface profile and coverage
signals correctly prompt re-grounding in owner-local truth, SDK applies the
policy decision, routing provides only advisory next-read hints, and evals does
not convert the stats signal into proof of owner truth.

It does not support claims such as:

- a stats summary proves the owner repo is healthy
- a routing hint approves a route
- an SDK re-grounding decision is an eval verdict
- an eval verdict replaces owner-local receipts
- coverage breadth proves source truth or project health

## Trigger boundary

Use this eval when:

- a consumer reads `source_coverage_summary` as a risk signal
- a consumer reads a catalog entry as a `surface_profile`
- routing exposes stats re-grounding hints
- SDK policy decides between clear, recommended, or required re-grounding
- the report might accidentally upgrade a derived signal into proof

Do not use this eval when:

- the main question is whether a specific owner artifact is correct
- the main question is general stats schema validity
- the main question is final route quality
- no consumer-side action or policy is being claimed

## Inputs

A careful run may include:

- one stats summary-surface catalog entry for the target surface
- one source-coverage summary with thin-signal flags
- one SDK re-grounding signal or surface-detection report
- one routing stats-regrounding advisory hint payload
- one owner-local source reference used for re-grounding
- the final consumer report wording

Missing consumer-path pieces are `not_observed`, not passes.

## Fixtures and case surface

The shared fixture family is
`fixtures/stats-regrounding-boundary-v1/README.md`.

Seed cases should cover:

- healthy coverage plus low-risk profile
- thin coverage plus high-risk profile
- routing advisory hint present but non-authoritative
- SDK policy requiring re-grounding before mutation
- negative overclaim where stats is treated as proof or routing authority

Replacement fixtures must preserve the same split-model question.

## Scoring or verdict logic

The scorer emits one axis result for each rubric axis:

- stats signal integrity
- coverage thinness handling
- SDK policy ownership
- routing advisory boundary
- eval verdict boundary
- owner-truth re-grounding target
- anti-overclaim report posture

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`
- `insufficient evidence`

Any authority transfer from owner truth into stats, routing, or SDK should
degrade the result. Any eval wording that treats the stats signal as proof
should fail the eval boundary axis.

## Baseline or comparison mode

This draft bundle uses `none`.

It is a standalone boundary read for one consumer path. A later baseline form
may compare re-grounding policy revisions over time, but that comparison is not
part of the current claim.

## Execution contract

A careful run should:

1. select one stats surface profile and source-coverage payload
2. capture the SDK policy decision that consumes those stats inputs
3. capture any routing advisory hint exposed for the same surface
4. name the owner-local truth target used for re-grounding
5. score each axis separately
6. keep missing axes separate from failed axes
7. write a compact summary-with-breakdown report
8. stop before owner-route approval or proof promotion

The scorer is a proof helper. It does not outrank this EVAL.md claim boundary.

## Outputs

The eval should produce:

- one bundle-level verdict
- per-axis status and evidence note
- a list of stats signals observed
- a list of owner-truth targets inspected or still missing
- limitations for missing consumer-path pieces
- anti-overclaim notes
- advisory followthrough suggestions

The bundle-local companion report contract lives at
`reports/summary.schema.json`, with an example at
`reports/example-report.json`.

## Failure modes

This eval can fail as an instrument when:

- the supplied path omits the SDK policy decision
- the report treats a thin-signal flag as proof of owner failure
- routing advice is described as route approval
- eval wording turns coverage breadth into project health
- owner-local truth targets are not named
- missing axes are counted as passes

## Blind spots

This eval does not prove:

- the owner-local artifact is correct
- the stats builder is complete across all future owner repos
- the routing layer chose the best route
- the SDK policy is optimal for every workflow
- project health, capability, or self-agency

Likely false-pass path:

- a consumer report uses cautious wording but never actually follows the
  owner-truth action it names.

Likely misleading-result path:

- the supplied example covers only one high-risk stats surface and is read as a
  general guarantee for all summaries.

## Interpretation guidance

Treat a positive result as support for one bounded claim: the supplied
consumer path preserved stats, SDK, routing, and eval ownership while using
stats-derived signals to re-ground.

Do not treat a positive result as:

- proof that the underlying owner work is correct
- permission to skip owner-local receipts
- permission to promote a route
- a general score for `aoa-stats`
- a broad federation health verdict

Pair this bundle with `aoa-owner-fit-routing-quality`,
`aoa-recurrence-control-plane-integrity`, or `aoa-verification-honesty` when
the main question moves into route fit, recurrence projection integrity, or
claimed-versus-actual verification.

## Verification

- confirm the bounded claim is explicit
- confirm stats remains derived observability
- confirm SDK owns the policy decision
- confirm routing hints are advisory only
- confirm eval wording does not become owner truth
- confirm owner-local re-grounding targets are named
- confirm missing axes remain `not_observed`
- confirm generated catalogs refresh after bundle changes

## Technique traceability

No source-owned technique dependency is claimed yet.

Future technique extraction, if any, should land in `aoa-techniques` before it
is referenced here.

## Skill traceability

No agent-facing skill dependency is claimed yet.

This bundle may be used beside change or contract-test skills, but it does not
define or activate those skills.

## Adaptation points

Project overlays may add:

- concrete SDK policy traces
- routing advisory payloads from local generated surfaces
- stats coverage snapshots from live refresh
- owner-local receipt references
- stricter report-schema extensions
- comparison baselines for policy revisions
