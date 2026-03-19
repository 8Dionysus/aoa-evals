# Architecture

## Purpose

`aoa-evals` is a public repository of portable evaluation bundles for agents and agent-shaped workflows.

It is the proof layer in the AOA public surface.

- `aoa-techniques` answers: what reusable engineering or evaluation practice exists, what are its invariants, and why is it valid?
- `aoa-skills` answers: how should an agent apply one or more techniques in a bounded workflow?
- `aoa-evals` answers: what bounded claims about agent quality, behavior, boundaries, regressions, or growth can be checked reproducibly?

## Conceptual model

### Techniques

A technique is a minimal reproducible unit of engineering practice.

Techniques may inform evaluation design, scoring discipline, rollout posture, or interpretation,
but they are not themselves eval bundles.

### Skills

A skill is an agent-facing execution bundle.

Skills may be one object under evaluation, but they are not themselves proof surfaces.

### Eval bundles

An eval bundle is a portable proof surface.

It packages:
- a bounded evaluation claim
- the object under evaluation
- fixture or case surface
- scoring or verdict logic
- execution guidance
- baseline or comparison mode
- report expectations
- blind spots and interpretation limits

An eval bundle may rely on one technique, several techniques, one skill, several skills, or none of them directly.
Its primary responsibility is not execution and not technique canonization.
Its primary responsibility is reproducible bounded proof.

## Layering

### Layer 1: origin need

An eval is usually born from a real quality question such as:
- a repeated failure mode
- a repeated claim that needs proof
- a regression that needs visibility
- a workflow that needs bounded comparison
- an artifact class that needs review discipline

### Layer 2: bounded eval design

The observed need is shaped into:
- a clear claim
- a bounded scope
- a fixture surface
- a scoring or verdict model
- a repeatable execution path
- an interpretation boundary

### Layer 3: portable eval bundle

The bounded design becomes a public-safe reusable eval bundle inside `aoa-evals`.

### Layer 4: local adaptation

A project-local overlay may add:
- repo-specific fixtures
- local runners
- local report sinks
- environment assumptions
- private operational context

These local adaptations should remain outside the public core unless they become general enough to publish safely.

## Design rules

1. eval bundles should make bounded claims, not total claims
2. proof matters more than impression
3. reproducibility matters more than anecdotal success
4. comparison surfaces matter more than isolated wins
5. blind spots must be named explicitly
6. raw run volume should not replace clear interpretation
7. markdown should remain the human-reviewable meaning surface
8. structured outputs should remain derived, bounded, and inspectable
9. compact public report artifacts are preferred over massive uncurated dumps
10. local project-specific evals should not silently masquerade as portable public defaults

## Eval categories

### Capability evals

Check whether an agent can perform a bounded class of tasks.

### Workflow evals

Check multi-step behavior rather than isolated outputs.

### Boundary evals

Check scope, authority, approval, safety, rollback thinking, or policy adherence.

### Artifact evals

Check the quality of produced outputs such as code, diffs, plans, reports, or documentation.

### Regression evals

Check whether a changed model, skill surface, or orchestration made behavior worse.

### Comparative evals

Compare:
- versions
- agents
- modes
- policies
- contexts

### Longitudinal evals

Track change across time rather than one run.

### Stress evals

Probe ambiguity, conflict, incomplete information, misleading cues, or adversarial edge conditions.

## Build philosophy

Eval bundles should be reviewable public artifacts.

They may rely on shared runners, scorers, fixtures, or schemas,
but a reviewer should still be able to understand:
- what is being claimed
- what is being measured
- how the verdict is reached
- where the bundle may mislead

Portable proof surfaces are preferred over opaque benchmark theater.

## Maturity direction

An eval bundle should eventually record:
- its own maturity state
- its object class
- its baseline mode
- its scoring surface
- its report contract
- known blind spots
- optional provenance or portability notes

A likely public maturity path is:
- `draft`
- `bounded`
- `portable`
- `baseline`
- `canonical`
- `deprecated`

## Long-term direction

This repository should eventually support:
- portable public proof surfaces
- bounded comparison across agent changes
- regression visibility without metric theater
- compact trustworthy report contracts
- reusable evaluation discipline across projects
- growth tracking without inflated claims
