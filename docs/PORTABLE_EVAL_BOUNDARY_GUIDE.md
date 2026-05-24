# Portable Eval Boundary Guide

This guide defines the portability route for evaluation bundles within the
`aoa-evals` bounded proof canon. It gives agents the route for moving public
proof claims while local context, copied files, and broad benchmark pressure
stay bounded by the bundle's contract.

Use this guide when a bundle demonstrates utility in a specific context and now
needs review as a public proof surface.

See also:
- [Documentation Map](README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | portability boundary guide for eval bundles that may leave their origin context |
| input | bundle claim, fixtures, runner or harness assumptions, scorer/verdict logic, report shape, and public interpretation pressure |
| output | portable posture, local-shaped posture, bounded adaptation route, or reviewer deferral |
| owner | bundle-local `EVAL.md` and `eval.yaml` own the proof claim; this guide owns portability criteria |
| next route | [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md), [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md), [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md), [Eval Review Guide](EVAL_REVIEW_GUIDE.md), or the affected bundle |
| validation | [docs/AGENTS.md#validation](AGENTS.md#validation) and the affected bundle route |

## Core question

A portable eval is one whose claim, verdict logic, fixture replacement story,
and interpretation boundary survive a move into another bounded context.

Ask one core question:

| Question | Review route |
| --- | --- |
| Does the bundle still tell the same bounded truth after reasonable adaptation? | inspect the invariant claim, replaceable inputs, harness assumptions, and interpretation boundary together |

## Portability Boundary Routes

Use these routes when a portability pressure appears:

| Pressure | Route |
| --- | --- |
| copied files look runnable | check whether the claim, verdict logic, and interpretation boundary still travel |
| adaptation is required | distinguish invariant core from replaceable fixtures, runner details, and local report sinks |
| environment assumptions appear | publish the setup boundary and adaptation points needed to recreate the proof surface |
| a wider audience wants to reuse the bundle | keep the public claim bounded to the proof contract that survived review |
| scores move across contexts | read score movement through score semantics and verdict interpretation, not raw number continuity |
| reviewer judgment remains part of the surface | expose the judgment rule, failure modes, and gaming risks |

## Signs of good portability

A bundle is closer to portable when:
- the bounded claim remains clear outside the origin project
- the fixture surface has a replacement contract that preserves the claim class
- the scorer or verdict logic exposes the reviewer judgment it depends on
- public readers can understand how the result should be interpreted
- local environment details remain subordinate to the proof surface
- the bundle names its remaining proof limits

## Local-Shaped Pressure Routes

When these pressures appear, route the bundle back to local-shaped review before
public portable posture:

| Pressure | Route |
| --- | --- |
| one project's naming, folder layout, or secret context carries the result | publish replacement rules or keep the bundle local-shaped |
| private data carries the fixtures | replace it with public or contract-backed fixture material |
| local taste drives the scorer | make the judgment rule reviewable or keep the scorer qualitative and bounded |
| only the original authors can read the verdict | rewrite the verdict boundary through the bundle and verdict guide |
| the claim inflates after leaving the origin context | narrow the claim before publication or defer portability |
| public readers can over-read the result | strengthen the interpretation boundary before the bundle is promoted |

## The portability test

Before calling a bundle portable, ask:

1. Could a careful outsider understand the bounded claim?
2. Could they tell what the eval measures and what proof limits remain?
3. Could they run or adapt the bundle with public setup and replacement rules?
4. Would the verdict still mean roughly the same thing after bounded adaptation?
5. Would the bundle still resist false certainty outside the birth project?

Several weak answers keep the bundle local-shaped.

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
with public boundaries for:
- infrastructure assumptions
- service availability
- tool policies
- script entrypoints
- scoring sinks

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
The target is bounded portable meaning; universal coverage belongs outside the
portability claim.

## Final note

Portability means durable bounded meaning at a new site.

Prefer a small honest eval bundle whose claim, fixture contract, verdict logic,
and interpretation boundary travel together.

Portable truth beats local spectacle.
