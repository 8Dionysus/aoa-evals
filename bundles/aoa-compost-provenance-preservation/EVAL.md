---
name: aoa-compost-provenance-preservation
category: artifact
status: draft
summary: Checks whether witness-derived compost artifacts preserve provenance, review state, limits, and contradiction posture as they move from raw input toward note, principle, or canon-candidate surfaces.
object_under_evaluation: provenance-preserving compost artifacts derived from witness-facing inputs
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-compost-provenance-preservation

## Intent

Use this eval to check whether witness-derived compost artifacts keep their provenance alive as they are distilled.

This draft bundle is a `diagnostic` artifact eval.
It checks whether a compost note,
principle candidate,
or canon-facing candidate preserves source refs,
review state,
limits,
and contradiction posture.
It is not meant to prove philosophical truth,
and it is not a replacement for general artifact-quality review.

The goal is not to prove that a composted insight is final.
The goal is to test one bounded claim:

under these conditions,
witness-derived compost artifacts can be distilled without severing provenance,
without hiding review state,
and without turning note or principle candidates into premature canon.

## Object under evaluation

This eval checks provenance-preserving compost artifacts derived from witness-facing inputs.

Primary surfaces under evaluation:
- retention of source refs back to the witness-facing input
- visibility of review status and current limits
- honesty about what changed from raw input to note or principle candidate
- preservation of contradiction,
  stale,
  or demotion posture
- refusal to treat every compost artifact as canon-ready

Nearby surfaces intentionally excluded:
- direct quality of the original run
- general artifact polish outside provenance discipline
- philosophical validity of the principle itself
- executable ToS platform behavior

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
a witness-derived compost artifact can move from raw input toward note,
synthesis,
or principle candidate
without losing provenance,
review posture,
or the ability to stay partial,
contested,
or later demoted.

This eval does **not** support claims such as:
- the resulting principle is canonically true
- the note is complete enough to replace its sources
- ToS now owns the operational route that produced the witness
- contradiction or decay handling is solved for all future compost artifacts

## Trigger boundary

Use this eval when:
- a public witness or summary is being distilled into a compost artifact
- provenance and review posture are part of the real question
- the main risk is premature abstraction or canon inflation
- a note or principle candidate may otherwise look cleaner than its evidence allows

Do not use this eval when:
- no witness-facing input is available
- the artifact is not part of a compost route
- the main question is generic artifact quality rather than provenance preservation
- the route is already claiming full canonization beyond this pilot contract

## Inputs

- one witness-facing input such as `WitnessTrace` or `witness_summary_md`
- one compost note,
  synthesis note,
  or principle candidate
- visible source refs
- visible review-state and limit notes
- visible promotion boundary for anything approaching canon

## Fixtures and case surface

A strong starter fixture set should include:
- a raw witness-derived input becoming a note
- a note becoming a principle candidate while keeping visible source refs
- a case where review state stays provisional and visible
- a case where contradiction or staleness remains possible after distillation
- a case where a tempting canon-like summary must be held back

Fixture families should avoid:
- notes that sever their route from the witness-facing input
- canon-like artifacts with no visible review or provenance posture
- highly polished summaries that no longer show their limits
- cases that depend on hidden private source references

## Scoring or verdict logic

This eval prefers a bundle-level verdict with an explicit breakdown.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:
- `source_ref_retention`
- `review_state_visibility`
- `limit_honesty`
- `promotion_boundary`
- `contradiction_and_decay_posture`

Per-artifact review should ask:
- can a reviewer still trace the compost artifact back to the witness-facing input?
- are review state and current limits visible?
- does the artifact say what remains partial or provisional?
- does a principle candidate keep its source refs rather than replacing them?
- do contradiction,
  stale,
  or demotion paths remain possible?

### Approve signals

Signals toward `supports bounded claim`:
- source refs remain visible and specific
- review state stays explicit
- principle candidates keep visible dependence on their upstream note or witness
- contradictions,
  decay,
  or demotion remain possible
- canon-facing language stays gated behind explicit review

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- a note or principle candidate severs its source refs
- review posture disappears behind polished synthesis
- limits are no longer named
- canon-like phrasing appears without a clear gate
- contradiction,
  stale posture,
  or later demotion becomes structurally impossible

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded proof surface for provenance-preserving compost.
A later stronger form may compare:
- different compost routes on the same witness input
- the same compost artifact before and after review
- note versus principle candidate behavior across repeated pilot runs

Without that later comparison form,
this bundle supports only modest claims about current provenance preservation on the chosen cases.

## Execution contract

A careful run should:
1. choose one witness-facing input and one downstream compost artifact
2. inspect source refs,
   review state,
   and current limits directly
3. confirm whether the artifact preserved provenance through distillation
4. confirm whether contradiction and decay posture remain possible
5. confirm whether promotion stopped honestly before canon when evidence stayed partial
6. publish a summary-with-breakdown artifact with an explicit interpretation boundary

Execution expectations:
- do not reward abstraction that severed provenance
- do not treat polished synthesis as proof of canon-readiness
- do not move operational ownership into ToS while reviewing the artifact
- do not erase decay or demotion posture in the name of clarity

## Outputs

The eval should produce:
- one bundle-level verdict
- one breakdown across the provenance-preservation axes
- one note on the most material preservation or severance point
- one explicit interpretation boundary

A compact public summary-with-breakdown may include:
- artifact id
- verdict
- breakdown by provenance-preservation axis
- main source-ref note
- main promotion-boundary note

## Failure modes

This eval can fail as an instrument when:
- reviewers reward polished synthesis more than provenance retention
- source refs exist only nominally and are not actually useful
- review state is copied mechanically without shaping interpretation
- contradiction or demotion posture is ignored because the artifact looks clean
- the bundle is over-read as proof of canonization

## Blind spots

This eval does not prove:
- philosophical correctness of the resulting idea
- final canon readiness
- quality of the original run that produced the witness
- general artifact quality outside provenance discipline
- long-term ToS growth policy beyond this pilot wave

Likely false-pass path:
- the artifact keeps token source refs,
  but review state and limits are so vague that a reader still overreads it as settled truth.

Likely misleading-result path:
- a careful provisional note can look modest or incomplete
  precisely because it preserved contradiction,
  decay,
  and review posture honestly.

Nearby claim classes that should use a different bundle instead:
- general produced-artifact quality should use `aoa-artifact-review-rubric`
- witness trace honesty should use `aoa-witness-trace-integrity`
- broader ToS doctrinal review should use the manual `Tree-of-Sophia` review route

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the compost artifact preserved provenance and review posture well enough for bounded reuse.

Do not treat a positive result as:
- proof that the resulting principle is canon
- proof that all contradictions have been resolved
- proof that operational ownership moved into ToS
- proof that later growth seeds are already implemented

A mixed or negative result is valuable because it can reveal:
- provenance severance
- hidden review posture
- premature canon language
- limits erased by polished synthesis
- contradiction or decay routes being closed too early

## Verification

- confirm the bounded claim is explicit
- confirm the witness-facing input and downstream artifact are both inspected
- confirm source refs remain visible and specific
- confirm review state and current limits remain explicit
- confirm principle or canon-facing language stays gated honestly
- confirm contradiction,
  stale,
  or demotion posture remains possible

## Technique traceability

Technique linkage is intentionally deferred for this starter bundle.
The current pilot is doctrinal and playbook-led rather than driven by a reusable compost technique canon.

## Skill traceability

Skill linkage is intentionally deferred for this starter bundle.
The current pilot route lives first in `aoa-playbooks/witness-to-compost-pilot`
and in ToS compost doctrine rather than in a standalone skill bundle.

## Adaptation points

Project overlays may add:
- local compost note shapes
- local review-state vocabularies
- local promotion gates for principle candidates
- local decay or staleness rules
- later comparison forms once the provenance-preserving compost route stabilizes
