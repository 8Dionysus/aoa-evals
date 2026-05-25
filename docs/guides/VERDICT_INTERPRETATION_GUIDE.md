# Verdict Interpretation Guide

This guide defines how to read the main verdict classes used in `aoa-evals`.

Use it when a bundle already has a verdict surface and the reviewer needs to
decide which bounded reading the verdict supports, which route stays outside
the verdict, and where stronger interpretation should go next.

See also:
- [Documentation Map](../README.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | verdict interpretation guide for bounded eval result surfaces |
| input | bundle verdict, per-case evidence, one-run pressure, repeated-run pressure, longitudinal pressure, composite/diagnostic pressure, claim-language pressure, or public-summary pressure |
| output | supported reading, boundary route, stronger-interpretation route, claim-language route, or public-summary correction route |
| owner | this guide owns docs-level verdict reading discipline; bundle-local `EVAL.md`, `eval.yaml`, reports, and review notes own concrete verdict evidence |
| next route | affected bundle, [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md), [Eval Review Guide](EVAL_REVIEW_GUIDE.md), comparison guide, repeated-window guide, or diagnostic bundle owner |
| validation | [docs/AGENTS.md#validation](../AGENTS.md#validation) |

## Canonical Verdict Routes

| verdict | supported reading | boundary route |
|---|---|---|
| `supports bounded claim` | The observed evidence supports the exact stated claim on this bounded eval surface. | Route broader capability, universal safety, and stable-behavior readings to the owner surface that can support them. |
| `mixed support` | The surface contains meaningful support and meaningful counter-evidence, or the evidence is too split or unstable for a cleaner reading. | Keep the tension visible; route strongest-case enthusiasm and hidden-pass pressure back to case evidence. |
| `does not support bounded claim` | The current evidence leaves the stated claim unsupported on this eval surface. | Keep the failure local to this claim; use nearby bundle review before rejecting other claim classes. |

These verdicts stay tied to the explicit bounded claim in the bundle.

## When to use `mixed support`

Prefer `mixed support` when:
- cases materially split between success and failure
- the evidence is real but too inconsistent for a clean pass
- instrumentation or review quality leaves important uncertainty
- the fixture surface is too thin for the stronger reading
- the bundle summary would otherwise look cleaner than the case evidence deserves

`mixed support` is a truth-preserving verdict.
Use it when the surface is genuinely mixed.

## One-run interpretation

One run can support a bounded claim.
Durable ranking or baseline pressure needs the repeated-run or comparison
route below.

One-run results are strongest when:
- the claim is narrow
- the fixtures are reviewable
- the verdict logic is explicit
- the summary says what still remains uncertain

One-run results are weak evidence for:
- growth across time
- comparison between models or modes
- stable ranking claims
- claims that require repeatability

## Repeated-run and comparison interpretation

Comparison becomes stronger only when:
- the fixture surface is stable or replaced by contract
- the verdict or score semantics stay the same
- the object under evaluation stays comparable
- environment changes are named
- style-only movement routes separately from substantive change

Use repeated runs to support bounded statements such as:
- version B preserved the named-baseline behavior on this surface
- this policy change reduced visible scope drift on the same case family
- this diagnostic bundle became more stable across comparable runs

Route these stronger readings elsewhere:

| Pressure | Route |
| --- | --- |
| permanent progress | longitudinal review with named windows and context drift |
| universal superiority | broader comparison surface with explicit baseline semantics |
| cross-surface equivalence | owner review across the affected bundle surfaces |

## Longitudinal interpretation

Use longitudinal readings only when:
- windows are ordered and named
- the same bounded surface is being read across windows
- context drift is disclosed
- style-only movement routes separately from substantive change

Canonical longitudinal readings should stay modest:

| reading | supported reading | boundary route |
|---|---|---|
| `bounded improvement signal` | Later windows look reviewably stronger on the same bounded surface. | Route general capability growth or durable improvement claims to a broader owner surface. |
| `mixed or unstable movement` | The sequence shows real movement, but it splits, drifts, or becomes too unstable for a cleaner directional claim. | Preserve the unstable readout instead of smoothing it into a pass or hidden growth story. |
| `no clear directional movement` | The sequence looks flat, too small, or too style-shaped for a stronger trend reading. | Keep room for local change that remains outside this surface's capture. |
| `bounded regression signal` | Later windows lost a reviewable strength on the same bounded surface. | Route universal decline claims away from this bounded surface. |

## Composite vs diagnostic bundles

| bundle shape | positive verdict means | negative or mixed verdict means | common misuse |
|---|---|---|---|
| `composite` | The end-to-end bounded workflow held together well enough on this surface. | Something in the bounded workflow surface broke or remained too uncertain. | Treating the bundle as a root-cause diagnosis of one failure class. |
| `diagnostic` | The isolated failure class or bounded question looked strong enough on this surface. | The isolated surface showed weakness, contradiction, or unresolved ambiguity. | Treating the diagnostic result as a full workflow judgment. |

Composite bundles answer:
- did the bounded workflow hold together?

Diagnostic bundles answer:
- did this specific bounded surface hold?

Use both shapes together when stronger interpretation needs both.

## Claim Language Routes

| Claim pressure | Route |
| --- | --- |
| bounded support under named conditions | "under these conditions, this bounded claim is supported" |
| fixture-family support | "on this fixture family, the result supports a modest workflow-quality claim" |
| authority-surface behavior | "on this authority surface, the agent classified actions with reasonable caution" |
| named-baseline comparison | "compared with the named baseline, this surface preserved the bounded behavior" |
| broad quality, safety, reliability, intelligence, or score-sovereignty language | route back to bundle claim, score semantics, and stronger owner review before publication |

## Public summary discipline

A public summary should say:
- the bounded claim
- the verdict
- what evidence mainly drove that verdict
- what remains uncertain
- unsupported readings that route elsewhere

Public-summary pressure routes:

| Pressure | Route |
| --- | --- |
| `mixed support` starts reading like a pass | restore the mixed evidence and uncertainty |
| a clean average hides a blocking failed case | surface the failed case beside the summary |
| summary implies a broader claim than the bundle states | narrow the summary to the bundle claim |
| outcome quality starts reading as root-cause diagnosis | route to diagnostic bundle or reviewer analysis |

## Final note

They are the shortest truthful answer the bundle can currently support.

If the truth is mixed, say mixed.
If the truth is bounded, keep it bounded.
