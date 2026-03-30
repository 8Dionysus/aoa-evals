# Portable Eval Boundary Guide

This guide defines the portability requirements for evaluation bundles within the `aoa-evals` bounded proof canon, ensuring they represent bounded claims about workflow quality suitable for the public proof surface.

Use this guide when a bundle demonstrates utility in a specific context but requires verification that it survives as a public proof surface rather than remaining a local testing artifact.

See also:
- [Documentation Map](README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Core question

A portable eval is not merely one that can be copied.

A portable eval is one that can be moved into another bounded context
without losing the main meaning of its claim, verdict logic, and interpretation.

The question is not:
- can another repo run these files somehow?

The real question is:
- does the bundle still tell the truth in a bounded way after reasonable adaptation?

## What portability does not mean

Portability does not mean:
- zero adaptation
- zero environment assumptions
- universal use
- total generality
- identical scores across all contexts
- immunity to judgment

Portability means the bundle's core proof contract survives bounded adaptation.

## Signs of good portability

A bundle is closer to portable when:
- the bounded claim remains clear outside the origin project
- the fixture surface can be recreated or replaced without changing the claim class
- the scorer or verdict logic does not depend on hidden reviewer intuition
- public readers can understand how the result should be interpreted
- local environment details remain subordinate to the proof surface
- the bundle names what it still cannot prove

## Signs of false portability

A bundle is not truly portable when:
- it only works because one project's naming, folder layout, or secret context is silently assumed
- the fixtures depend on private data that cannot be replaced cleanly
- the scorer uses local taste disguised as objective logic
- the verdict only makes sense to the original authors
- the bundle's claim becomes vague or inflated once removed from the origin context
- public readers would over-read the result because the interpretation boundary is missing

## The portability test

Before calling a bundle portable, ask:

1. Could a careful outsider understand the bounded claim?
2. Could they tell what the eval measures and what it does not measure?
3. Could they run or adapt the bundle without hidden private knowledge?
4. Would the verdict still mean roughly the same thing after bounded adaptation?
5. Would the bundle still resist false certainty outside the birth project?

If several answers are no, the bundle is still local-shaped.

## Fixture portability

Portable fixtures should prefer one of these shapes:
- public static fixtures
- curated fixture families with public replacement rules
- generated fixtures with stable generation boundaries
- mixed surfaces where the replacement contract is explicit

Fixture portability gets weaker when:
- the data is private
- the cases encode one local workflow too specifically
- the fixture set is too tiny to support the stated claim
- the bundle never explains how another context should substitute comparable material

## Scorer portability

Portable scorers should:
- be legible
- be bounded
- expose their categories or thresholds
- explain score semantics
- name failure modes and gaming risks

A scorer is less portable when:
- its judgments depend mostly on tacit taste
- a score exists with no explanation
- thresholds are cargo-culted from one origin context
- different reviewers would interpret the same score in radically different ways

## Verdict portability

Portable verdicts should survive movement better than raw numbers.

Good verdict styles include:
- bounded categorical verdicts
- pass / fail with interpretation notes
- scalar scores only when accompanied by strict interpretation guidance
- comparative verdicts that name what changed and how cautiously to read the change

Verdicts become less portable when:
- they imply a universal ranking
- they hide uncertainty
- they flatten several different failures into one number
- they invite readers to conclude far more than the eval supports

## Environment portability

Portable bundles may still require bounded environment setup,
but they should not depend on:
- private infrastructure
- unpublished services
- secret tool policies
- undocumented local scripts
- hidden scoring sinks

If local infrastructure is necessary,
the bundle should publish the proof contract and adaptation points clearly enough
that another environment could recreate the same bounded surface.

## Adaptation points

A portable bundle should distinguish:
- invariant core
- replaceable fixtures
- replaceable runner details
- local report sinks
- optional local scoring refinements

If everything is treated as invariant, the bundle is usually too local.
If everything is treated as replaceable, the claim is usually too vague.

## Public publication threshold

A bundle is usually ready for public portable posture when:
- the bounded claim is stable
- the object under evaluation is explicit
- the fixtures are either public or replaceable by contract
- scoring or verdict logic is reviewable
- blind spots are named
- a bounded outsider could reproduce the main meaning of the result

That is enough.
Full universality is not required.

## Final note

Do not confuse portability with scale.

A small honest eval bundle that travels well is more valuable
than a grand benchmark surface that collapses outside one project.

Portable truth beats local spectacle.
