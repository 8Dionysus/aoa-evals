# Score Semantics Guide

This guide defines the canonical meaning of scores, rubric axes, per-case notes,
and bundle-level verdicts in `aoa-evals`.

Use it when an eval bundle already has a result surface,
but you still need to decide what that result actually means and how far it can be read.

See also:
- [Documentation Map](README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | score and verdict interpretation guide for eval result surfaces |
| input | result surface, case evidence, rubric axis, bundle-level verdict, scalar-score pressure, or collapse pressure |
| output | score interpretation bound, expanded result shape, per-case note route, bundle-level verdict route, or review gap |
| owner | this guide owns score semantics; bundle-local `EVAL.md`, `eval.yaml`, reports, and review notes own concrete claim meaning |
| next route | `docs/EVAL_REVIEW_GUIDE.md`, `docs/VERDICT_INTERPRETATION_GUIDE.md`, `docs/EVAL_RUBRIC.md`, or the affected bundle |
| validation | `docs/AGENTS.md#validation` |

## Default posture

This repository prefers:
- direct evidence over abstraction
- per-case notes over unexplained aggregate numbers
- categorical verdicts over decorative scores
- explicit interpretation bounds over tidy-looking summaries

Use a scalar score only when it has a strict interpretation contract.

## Core vocabulary

| term | meaning |
|---|---|
| `evidence` | Directly inspectable material such as traces, diffs, outputs, classifications, logs, or review notes tied to a case. |
| `signal` | A bounded pattern extracted from evidence, such as scope drift, explicit verification, or refusal quality. |
| `rubric axis` | One named review dimension used to structure judgment. An axis carries one part of the claim. |
| `per-case note` | The bounded result for one case, fixture item, or scenario. |
| `bundle-level summary` | The compact cross-case reading of what happened across the eval surface. |
| `verdict` | The bounded judgment about whether the stated claim is supported on this eval surface. |
| `score` | A scalar or ordered abstraction that compresses evidence. A score is only valid when its interpretation bound is explicit. |
| `mixed support` | A verdict meaning the current evidence neither supports a clean pass nor a clean rejection of the bounded claim. |
| `interpretation bound` | The explicit limit on how far a score or verdict may be generalized. |

## Evidence hierarchy

Higher-level summaries should remain subordinate to lower-level evidence.

Preferred order:

1. direct observed case evidence
2. per-case notes
3. rubric-axis summaries
4. bundle-level verdict
5. scalar or aggregate score

Implications:
- a clean score preserves material failed cases in the interpretation bound
- a bundle-level verdict stays consistent with per-case evidence
- a rubric axis must stay interpretable from observed evidence
- if aggregate output hides a meaningful disagreement, prefer `mixed support`

## Rubric axes

Rubric axes should:
- name one bounded review dimension each
- stay legible to a human reviewer
- avoid heavy overlap with nearby axes
- avoid pretending to be the whole claim

Route these rubric-axis pressure signals:

| Pressure | Route |
| --- | --- |
| axis repeats the final verdict in slightly different words | collapse it into the verdict or split a real evidence dimension |
| unrelated failure modes get averaged into false objectivity | keep separate axes or use `mixed support` |
| blind spots disappear into axis labels | add explicit blind-spot disclosure |
| precision appears without clearer meaning | weaken the score shape or add an interpretation bound |

Examples of good axis shapes:
- scope stayed declared and reviewable
- claimed verification matched performed verification
- action classification matched the authority boundary
- report summary matched the observed work

## Per-case vs bundle-level meaning

Per-case notes answer:
- what happened on this case?
- what evidence supports that reading?
- what failure mode or success signal was visible here?

Bundle-level summaries answer:
- what bounded claim is supported across this surface?
- how consistent was the signal?
- what uncertainty remains after aggregation?

Bundle-level verdicts should remain weaker than the strongest-looking individual case.

If cases materially diverge, prefer:
- a weaker bundle-level verdict
- explicit uncertainty notes
- or `mixed support`

One impressive case stays per-case evidence; the bundle verdict follows
cross-case support.

## Score shapes

| shape | normal use | caution |
|---|---|---|
| `categorical` | Best default for most draft and bounded bundles. | Must still name evidence and interpretation limits. |
| `pass-fail` | Useful when the claim surface is crisp and blocking failures are clear. | Easy to over-read if failure modes vary widely. |
| `comparative` | Useful when the bundle is explicitly baseline-shaped. | Not valid without stable comparison semantics. |
| `scalar-with-interpretation` | Acceptable when thresholds, ranges, and gaming risks are explicit. | Keep the number subordinate to the evidence and interpretation bound. |
| `mixed` | Useful when a bundle genuinely needs both structured axes and a bounded verdict. | Use mixed shape to expose unclear semantics before collapsing them. |

## When To Keep Results Expanded

Keep the result expanded when:
- the bundle is composite and nearby failure modes matter separately
- the bundle is diagnostic and one blocking failure should dominate interpretation
- the fixture surface is thin or still highly local-shaped
- repeatability is too weak for stable comparison
- reviewer judgment is still heavily qualitative
- style improvement could be mistaken for substantive improvement

In those cases, prefer:
- per-case notes
- rubric-axis summaries
- categorical verdicts
- explicit caution notes

## Score interpretation bound

Every score or verdict should make clear:
- what it captures
- what remains outside its capture boundary
- whether it is per-case or bundle-level
- whether it supports standalone or comparative reading
- what nearby bundle should be used for a narrower diagnosis if needed

A score with an interpretation bound becomes a reviewable public surface.

## Composite and diagnostic bundles

Score semantics should match bundle shape.

Composite bundles:
- may observe several nearby failure classes together
- should resist flattening those classes into one overconfident score
- usually benefit from per-case notes plus a bounded bundle-level verdict

Diagnostic bundles:
- should isolate one failure class or bounded review question
- should name intentionally excluded questions
- should treat blocking contradictions seriously rather than smoothing them away

## Final note

In `aoa-evals`, a score serves the bounded claim.

The point is a bounded, reviewable claim supported by legible evidence.

If a score helps that, keep it.
If it hides that, weaken it.
