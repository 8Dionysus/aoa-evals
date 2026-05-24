# Architecture

## Role

`docs/ARCHITECTURE.md` explains the technical proof model of `aoa-evals`.

Use this file for the proof model. Use `DESIGN.md` for repository shape,
`docs/PROOF_TOPOLOGY.md` for authority classes, `ROADMAP.md` for sequencing,
`docs/decisions/` for rationale, generated catalogs for compact projections,
and `mechanics/EVIDENCE_CLUSTERS.md` before creating or moving mechanic
packages.

## Operating Card

| Field | Route |
| --- | --- |
| role | technical proof model for portable eval bundles, mechanic operation support, and generated reader boundaries |
| input | proof-model question, agent-eval vocabulary, bundle anatomy, mechanic parent pressure, local adaptation pressure, or generated-reader pressure |
| output | proof-layer route, owner split, bundle/mechanic/generated boundary, and design-rule route |
| owner | this document for the technical proof model; `DESIGN.md` for repository form; `docs/PROOF_TOPOLOGY.md` for authority classes |
| next route | source eval package, `docs/PROOF_TOPOLOGY.md`, `mechanics/EVIDENCE_CLUSTERS.md`, `mechanics/README.md`, generated builder, or `docs/decisions/` |
| tools | nearest `AGENTS.md`, root validator, semantic AGENTS validator, and generated-reader builders when derived surfaces move |
| validation | `docs/AGENTS.md#validation` and the focused architecture proof-model route in `docs/decisions/0093-architecture-proof-model-contract.md` |

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
while eval bundles carry the portable proof claim.

### Skills

A skill is an agent-facing execution bundle.

Skills may be one object under evaluation. Their execution meaning stays with
the skill owner; `aoa-evals` reviews only the bounded proof claim it can
support.

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
Its primary responsibility is reproducible bounded proof. Execution and
technique canonization stay with the owning skill and technique layers.

### Agent eval vocabulary

Modern agent eval language maps into `aoa-evals` through owner routes:

| Agent-eval term | Local proof route |
| --- | --- |
| task or case | bundle fixture/case surface and bundle-local fixture contract |
| trial or run | runner output, report artifact, or receipt preview under its owning bundle or mechanic |
| grader | scoring or verdict logic in `EVAL.md`, `eval.yaml`, report schema, or bounded scorer helper |
| transcript or trajectory | selected evidence, trace fixture, or audit candidate packet before bundle-local review |
| outcome | bounded report verdict or comparative readout under the bundle interpretation boundary |
| harness or scaffold | bundle-local runner contract, shared runner surface, or stronger execution owner such as `aoa-skills` or `aoa-agents` |

Use this vocabulary as route translation. The owner surfaces above keep the
proof authority.

### Mechanics

A mechanic is a recurring proof-layer operation with its own inputs, outputs,
stronger-owner split, stop-lines, and validation.

Mechanics organize reusable proof machinery around source eval packages:
authoring contracts, comparison spines, shared proof infrastructure, receipt
sidecars, quest obligations, audit intake, boundary bridges, and AoA-aligned
proof support such as Agon, recurrence, checkpoint, Experience,
antifragility, method-growth, RPG, growth-cycle, and distillation.

Legacy inside a mechanic is provenance behind the active route. Active work
starts from the parent route, part contracts, and validators; `PROVENANCE.md`
is the single controlled bridge into the owning legacy archive. Archive details
stay inside that archive.

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

### Layer 5: proof operation support

Once several bundles or support artifacts repeat the same proof operation, the
support machinery may live under `mechanics/<parent>/parts/<part>/`.

The parent name must come from one of two routes:

- AoA-aligned mechanics keep the center mechanic name when local proof support
  materializes that operation.
- Evals-native mechanics are allowed only when `aoa-evals` itself owns the
  proof-organ operation.

An evals-native parent may keep a stronger-owner subject name only when the
local proof operation is explicit and the stronger owner split is visible. The
`titan` parent is this owner-named evals-native case: `aoa-evals` owns seed
boundary proof shape, while `aoa-agents` keeps Titan role, bearer, summon, and
incarnation law.

Artifact forms such as canaries, reports, receipts, schemas, runners, scorers,
generated readers, and verdict models become parts or payloads under the
owning parent. Parent names come from the recurring operation and owner split.

## Design Rule Routes

| Pressure | Route |
| --- | --- |
| broad or total claim pressure | shape one bounded claim with scope, evidence, verdict logic, and blind spots |
| impression pressure | route to reviewable proof evidence |
| anecdotal success pressure | route to a reproducible execution or review path |
| isolated win pressure | add comparison posture when comparison is claimed |
| hidden-limit pressure | name blind spots as part of the proof contract |
| raw run volume pressure | route through clear interpretation and report boundaries |
| human meaning pressure | keep markdown as the human-reviewable meaning surface |
| structured-output pressure | keep structured outputs derived, bounded, and inspectable |
| large dump pressure | prefer compact public report artifacts |
| project-local pressure | keep local adaptations public-safe before promoting them as portable defaults |
| artifact-form pressure | require cross-root evidence before naming a mechanic parent |
| legacy pressure | preserve lineage through active owner routes and provenance bridges |

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

When a bundle starts to act as a reusable proof instrument rather than a prose-only starter,
it should materialize that claim through bounded artifacts such as:
- shared fixture contracts
- shared scorer helpers
- bundle-local runner contracts
- schema-backed report examples

These artifacts remain subordinate to the authored markdown and manifest surfaces.

## Derived reader surfaces

`generated/eval_catalog.json` and `generated/eval_catalog.min.json` are deterministic
reader surfaces derived from:
- `evals/**/EVAL.md`
- `evals/**/eval.yaml`

They exist to support routing, navigation, and read-heavy consumers.
They route readers back to authored bundle meaning in markdown and manifest
files.

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
- regression visibility with bounded comparison semantics
- compact trustworthy report contracts
- reusable evaluation discipline across projects
- growth tracking with explicit claim limits
