# Eval Review Guide

This guide defines the bounded review contract for public maturity decisions in `aoa-evals`.

Use it when an eval bundle already looks useful and reusable,
but the repo still needs one explicit decision about whether the bundle is ready for:

- `draft -> bounded`
- promotion to `baseline`
- `baseline -> canonical`

This guide is review-first.
Promotion authority routes through explicit review; frontmatter metadata,
generated catalog fields, and validator results remain supporting evidence.

See also:
- [Documentation Map](../README.md)
- [Eval Rubric](EVAL_RUBRIC.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | bounded maturity review guide for public eval bundles |
| input | bounded-promotion pressure, baseline pressure, canonical pressure, metadata evidence, support-note evidence, portability evidence, canonical-readiness evidence, or interpretation-risk pressure |
| output | approve/defer outcome, remaining-gap route, review-evidence route, promotion route, or integrity-sidecar route |
| owner | this guide owns docs-level maturity review discipline; bundle-local `EVAL.md`, `eval.yaml`, `support_note`, `portable_review`, and `canonical_readiness` own concrete review evidence |
| next route | affected bundle, [Eval Rubric](EVAL_RUBRIC.md), [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md), [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md), [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md), or comparison guide |
| validation | [docs/AGENTS.md#validation](../AGENTS.md#validation) |

## Outcomes

### For `draft -> bounded`

Bounded review should end in one of two outcomes only:

- `approve for bounded promotion`
- `defer for now`

Use `approve for bounded promotion` when the eval already reads as a repeatable bounded proof surface with:
- a clear execution path
- a reviewable verdict surface
- example reporting that keeps the public readout honest
- visible failure-vs-readout distinctions
- nearby-bundle boundaries that stay crisp

Use `defer for now` when one remaining gap blocks bounded status: failure
classes collapse, interpretation limits stay unexposed, or support material
needs a reviewable evidence trail.

### For promotion to `baseline`

Baseline review should end in one of two outcomes only:

- `approve for baseline`
- `defer for now`

Use `approve for baseline` when the eval already reads as a stable comparison surface within its bounded scope.

Use `defer for now` when stability, local shape, or interpretation still needs
baseline-grade support before comparison use.

Record that public approval trail in `portable_review`.
Baseline approval notes route through that evidence kind.

When a wave materially deepens pairing, shared infra, longitudinal reading, or canonical candidacy,
carry `aoa-eval-integrity-check` or an equivalent bounded integrity packet as a sidecar.

## Review Pressure Routes

| Pressure | Route |
| --- | --- |
| frontmatter metadata wants to promote a bundle | explicit maturity review with bundle-local evidence |
| generated catalog fields look stronger than review notes | review the bundle source and keep generated readers derived |
| baseline approval needs a public trail | record the trail in `portable_review` |
| bounded approval hides failure-vs-readout ambiguity | defer with the smallest concrete remaining gap |
| canonical pressure lacks default-use rationale | defer until `canonical_readiness` states the bounded default-use case |
| comparison, longitudinal, shared-infra, or canonical pressure widens a public reading | carry `aoa-eval-integrity-check` or equivalent bounded integrity sidecar |

## Bounded Review Axes

| axis | approve signal | defer signal |
|---|---|---|
| execution path clarity | A reviewer can see how the bundle is meant to run and where the bounded read comes from. | The run path still needs explicit reconstruction evidence. |
| verdict and readout discipline | Bundle-level verdicts, per-case notes, and example reports stay legible and bounded. | Public readout still jumps too quickly from thin evidence to strong conclusions. |
| failure-vs-readout separation | Failure signals are named directly and stay distinct from the summary language used to report them. | Failure signals blur into summary wording or polished readouts cover them. |
| nearby-bundle distinctness | The bundle clearly says which nearby question belongs here and which routes elsewhere. | The bundle still blurs into composite, diagnostic, artifact, or boundary neighbors. |
| support evidence | Starter evidence, example report, and support notes make the bounded claim inspectable after publication. | Key bounded-claim support still needs explicit review evidence. |

### For `baseline -> canonical`

Canonical review should end in one of two outcomes only:

- `approve for canonical promotion`
- `defer for now`

Use `approve for canonical promotion` when the eval already reads as the natural default proof surface within its bounded scope.

Use `defer for now` when the eval is strong, but still reads as an optional companion, a context-shaped comparator, or an under-validated default.

## Baseline Review Axes

| axis | approve signal | defer signal |
|---|---|---|
| repeatability | Runs are stable enough that comparison meaningfully tells us something bounded and non-trivial. | Run-to-run or environment-to-environment movement is still too large for stable comparison. |
| baseline clarity | The bundle clearly states what it compares against and what kind of claim that comparison can support. | The comparison target is muddy, shifting, or easy to over-interpret. |
| fixture discipline | The fixture surface is clearly bounded and representative enough for the stated claim. | Fixtures still look too ad hoc, too narrow, or too entangled with one local context. |
| verdict semantics | Scores or verdicts are explained with a bounded interpretation route. | The bundle still relies on opaque numbers, vague labels, or hidden judgment. |
| blind-spot disclosure | The bundle honestly names unsupported readings and routes them elsewhere. | The bundle still reads as stronger or broader than its actual surface supports. |
| practical reuse | The bundle can be run outside its birth context with bounded adaptation. | Real use still depends too much on one project's private environment, tooling, or habits. |

## Canonical Review Axes

| axis | approve signal | defer signal |
|---|---|---|
| default-use rationale | The bundle clearly reads as the default proof surface for its bounded claim class. | The default-use rationale is weak or missing. |
| comparison trustworthiness | The bundle has demonstrated stable enough meaning across review cycles, comparisons, or contexts. | Meaning still shifts too much across contexts or review passes. |
| interpretation honesty | Scores, verdicts, and summaries already resist false certainty and inflated claims. | The bundle still invites benchmark theater, false ranking, or over-broad conclusions. |
| portability beyond origin | The eval has shown useful life beyond its birth context or initial local need. | Evidence still comes mostly from one origin, or portability remains too thin. |
| stronger validation than baseline floor | The bundle has more than mere structural completeness; reviews, integrity checks, or repeated use reinforce its strength. | Evidence still looks too close to the minimum baseline floor. |
| fresh public-safety recheck | The current public bundle remains safe, bounded, and suitable for broader recommendation. | Public-safety, local leakage, or interpretation risks remain unresolved. |

## Metadata Supports Explicit Review

Stage 1 metadata supports review and routes the reviewer toward the evidence to inspect.

- `maturity_score` can hint that a bundle is approaching baseline or canonical strength.
- `repeatability` can show whether the result surface is stable enough for disciplined comparison.
- `portability_level` can show whether the bundle still carries strong local shape.
- `validation_strength` can show whether reinforcement moved beyond structural completeness.
- `blind_spot_disclosure` can show whether the bundle names its own limits.
- `export_ready` only concerns Stage 1 structured catalog publication safety.

Promotion decisions stay with explicit human review.

## Tracked Review Evidence

Promotion-shaped reviews should leave a small public trail:

- bundles operating at `bounded` posture should carry a `support_note` that records the bounded review outcome, failure-versus-readout distinction, and interpretation boundary
- bundles already operating at `portable`, `baseline`, or `canonical` posture should carry `portable_review`; for baseline promotion this is the public review trail
- bundles seeking or holding `canonical` posture should carry `canonical_readiness`
- bundles using `comparative-summary` should carry a `support_note` that names the comparison contract and its interpretation limits
- bundles claiming reusable proof artifacts should ship schema-backed report examples and runner/fixture contracts before those artifacts are treated as part of the public proof surface

These notes keep the public reasoning inspectable after the decision.

## Review Notes

Review should stay bounded and concrete.

- Review the bundle as published today.
- Name one recommendation only: approve now or defer for now.
- If deferred, name the smallest concrete remaining gap and the route that closes it.
- If approved, make the bundle's comparison or default-use rationale explicit enough that later reviewers can read it from the review trail.
- Name the exact boundary of the approved claim.
- If the bundle uses scores, say the interpretation boundary where those scores stop.
- If the bundle uses categorical verdicts, say what uncertainty remains after the verdict.

## Deferral Routes

Common deferral routes include:

- fixture surface needs broader or less local evidence
- score semantics need clearer interpretation bounds
- verdict logic needs explicit judgment evidence
- blind spots need bundle-shaped disclosure
- bundle remains better as a companion than as a default proof surface
- repeated use reveals unstable meaning
- report summaries need weaker claim language

## Recording review outcomes

A bundle-level review note should remain the authoritative place to record:
- outcome
- boundary of the approved or deferred claim
- smallest remaining gap if deferred
- default-use rationale if approved
- any caution about score or verdict interpretation
