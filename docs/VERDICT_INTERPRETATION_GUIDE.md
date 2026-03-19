# Verdict Interpretation Guide

This guide defines how to read the main verdict classes used in `aoa-evals`.

Use it when a bundle already has a verdict surface,
but you still need to decide what that verdict supports and what it still does not support.

See also:
- [Documentation Map](README.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Canonical verdicts

| verdict | meaning | does not mean |
|---|---|---|
| `supports bounded claim` | The observed evidence supports the exact stated claim on this bounded eval surface. | General capability, universal safety, or stable behavior outside the named boundary. |
| `mixed support` | The surface contains meaningful support and meaningful counter-evidence, or the evidence is too split or unstable for a cleaner reading. | A soft pass, a polite fail, or permission to over-read the strongest case. |
| `does not support bounded claim` | The current evidence does not support the stated claim on this eval surface. | Proof that the agent can never succeed, or proof that all nearby claims are false. |

These verdicts should stay tied to the explicit bounded claim in the bundle.

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
One run should not be mistaken for a durable ranking or baseline.

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
- style-only movement is not mistaken for substantive change

Use repeated runs to support bounded statements such as:
- version B did not look worse than version A on this surface
- this policy change reduced visible scope drift on the same case family
- this diagnostic bundle became more stable across comparable runs

Do not use repeated runs to imply:
- permanent progress
- universal superiority
- cross-surface equivalence

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

## Claim language

Prefer language like:
- under these conditions, this bounded claim is supported
- on this fixture family, the result supports a modest workflow-quality claim
- on this authority surface, the agent classified actions with reasonable caution
- compared with the named baseline, this surface did not look worse

Avoid language like:
- the agent is good
- the workflow is safe
- this proves reliability
- this bundle shows real intelligence
- the score speaks for itself

## Public summary discipline

A public summary should say:
- the bounded claim
- the verdict
- what evidence mainly drove that verdict
- what remains uncertain
- what the result still does not prove

A public summary should not:
- upgrade `mixed support` into a pass
- hide a blocking failed case behind a clean average
- imply a broader claim than the bundle states
- confuse outcome quality with root-cause diagnosis

## Final note

Verdicts are not decorations.

They are the shortest truthful answer the bundle can currently support.

If the truth is mixed, say mixed.
If the truth is bounded, keep it bounded.
