# Score Semantics Guide

This guide defines the canonical meaning of scores, rubric axes, per-case notes,
and bundle-level verdicts in `aoa-evals`.

Use it when an eval bundle already has a result surface,
but you still need to decide what that result actually means and how far it can be read.

See also:
- [Documentation Map](README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)

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
| `rubric axis` | One named review dimension used to structure judgment. An axis is not the whole claim. |
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
- a clean score must not erase a material failed case
- a bundle-level verdict must not silently contradict per-case evidence
- a rubric axis must stay interpretable from observed evidence
- if aggregate output hides a meaningful disagreement, prefer `mixed support`

## Rubric axes

Rubric axes should:
- name one bounded review dimension each
- stay legible to a human reviewer
- avoid heavy overlap with nearby axes
- avoid pretending to be the whole claim

Rubric axes should not:
- duplicate the final verdict in slightly different words
- average unrelated failure modes into false objectivity
- replace explicit blind-spot disclosure
- create the illusion of precision without clearer meaning

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

Do not let one impressive case stand in for the bundle.

## Score shapes

| shape | normal use | caution |
|---|---|---|
| `categorical` | Best default for most draft and bounded bundles. | Must still name evidence and interpretation limits. |
| `pass-fail` | Useful when the claim surface is crisp and blocking failures are clear. | Easy to over-read if failure modes vary widely. |
| `comparative` | Useful when the bundle is explicitly baseline-shaped. | Not valid without stable comparison semantics. |
| `scalar-with-interpretation` | Acceptable when thresholds, ranges, and gaming risks are explicit. | Never let the number become the whole meaning. |
| `mixed` | Useful when a bundle genuinely needs both structured axes and a bounded verdict. | Do not use mixed shape to hide unclear semantics. |

## When not to collapse into one score

Do not collapse the result into one number when:
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
- what it does not capture
- whether it is per-case or bundle-level
- whether it supports standalone or comparative reading
- what nearby bundle should be used for a narrower diagnosis if needed

A score without an interpretation bound is not a strong public surface.

## Composite and diagnostic bundles

Score semantics should match bundle shape.

Composite bundles:
- may observe several nearby failure classes together
- should resist flattening those classes into one overconfident score
- usually benefit from per-case notes plus a bounded bundle-level verdict

Diagnostic bundles:
- should isolate one failure class or bounded review question
- should say what they intentionally do not evaluate
- should treat blocking contradictions seriously rather than smoothing them away

## Final note

In `aoa-evals`, a score is never the point.

The point is a bounded, reviewable claim supported by legible evidence.

If a score helps that, keep it.
If it hides that, weaken it.
