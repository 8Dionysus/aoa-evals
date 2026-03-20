# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-evals`.

## Purpose

`aoa-evals` is the bounded proof canon of AoA.

It stores portable evaluation bundles for bounded claims about workflow quality, boundaries, regressions, artifact quality, comparative behavior, and related reviewable surfaces.

This repository is for bounded proof surfaces, not for universal scores or broad claims of intelligence.

## Owns

This repository is the source of truth for:

- eval bundle wording
- bounded claim framing
- verdict-shape wording
- review posture and caveats at the eval layer
- eval metadata and generated catalogs/capsules
- repository-level doctrine about what an eval does and does not prove

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- the bounded execution workflows under evaluation in `aoa-skills`
- routing and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- higher-level scenario composition in `aoa-playbooks`
- memory objects or recall surfaces in `aoa-memo`
- private benchmark data, hidden operational telemetry, or private infrastructure detail

## Core rule

Only contribute evals that make bounded, reviewable claims.

If a claim cannot be stated clearly enough to say what it does not prove, it does not belong here yet.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/EVAL_PHILOSOPHY.md`
4. the target `bundles/*/EVAL.md`
5. any manifest, catalog, capsule, or summary surface tied to that bundle

If the task changes a claim, inspect the upstream skill or technique surfaces the eval depends on.

## Primary objects

The most important objects in this repository are:

- `bundles/*/EVAL.md`
- `bundles/*/eval.yaml` or the current manifest source
- generated eval catalogs
- generated eval capsules
- philosophy, architecture, and starter-bundle docs referenced by the README

## Allowed changes

Safe, normal contributions include:

- tightening a bounded claim
- improving category, verdict-shape, or caveat wording
- clarifying evaluation context and blind spots
- fixing metadata drift between source files and generated outputs
- improving dependency references to skills or techniques
- adding a new eval when the claim is clearly bounded and reviewable

## Changes requiring extra care

Use extra caution when:

- changing what the eval claims to prove
- changing category or verdict shape
- changing dependency structure
- changing generated catalog or capsule shape
- changing wording that prevents overclaiming
- changing starter bundles or selection surfaces that public readers may interpret as doctrine

## Hard NO

Do not contribute:

- broad intelligence claims disguised as bounded evals
- score theater without clear claim boundaries
- hidden private datasets with no public framing
- vague pass/fail wording with no review posture
- evals that depend on secret context not present in the repository
- metadata-only surfaces that imply stronger proof than the underlying bundle supports

Do not:

- rewrite upstream skill or technique meaning here
- store routing meaning here
- store memory meaning here
- use polished wording to conceal uncertainty

## Typical claim shapes

Good evals here usually support one or more bounded claim shapes:

- capability within a bounded class of tasks
- workflow quality across a bounded process
- boundary adherence
- artifact quality on a visible task surface
- regression against a frozen or comparable baseline
- comparative difference under matched conditions
- longitudinal movement over repeated bounded windows

## Public hygiene

Assume everything here is public, inspectable, and challengeable.

Write for portability:

- make the object under evaluation explicit
- keep the claim type narrow
- say what the eval does not prove
- keep verdict language reviewable
- avoid private assumptions unless they are clearly marked and sanitized

## Contribution doctrine

Use this flow:

`PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what eval is being added or changed
- what bounded claim it supports
- what it does not prove
- which upstream skills or techniques it depends on

### DIFF

Keep the change focused.

Do not mix unrelated benchmark cleanup into an eval change unless it is necessary for repository integrity.

### VERIFY

Confirm that:

- the claim remains bounded
- the verdict shape still matches the claim
- caveats and blind spots remain visible
- dependencies still point to the right upstream surfaces
- the public reading of the eval is not stronger than the evidence it carries

If metadata or generated surfaces changed, regenerate and validate them.

### REPORT

Summarize:

- what changed
- whether claim meaning changed or only metadata changed
- whether category or verdict shape changed
- whether dependencies changed
- any remaining caveats or follow-up work

## Validation

Run the validation commands documented in `README.md`.

If catalogs, capsules, or other generated eval surfaces changed, regenerate and validate them before finishing.

Run tests or checks for touched surfaces when available. Do not claim checks you did not run.

## Cross-repo neighbors

Use these neighboring repositories when the task crosses boundaries:

- `aoa-techniques` for upstream reusable practice
- `aoa-skills` for the bounded workflows under evaluation
- `aoa-routing` for smallest-next-object navigation
- `aoa-agents` for role/evaluation posture context
- `aoa-playbooks` for scenario-level composition context
- `Agents-of-Abyss` for ecosystem-level map and boundary doctrine

## Output expectations

When reporting back after a change, include:

- which eval bundles changed
- whether claim meaning changed or only metadata changed
- whether category, verdict shape, or caveats changed
- whether dependencies changed
- what validation was run
- any public interpretation risks or downstream follow-up

## Default editing posture

Prefer the smallest reviewable change.
Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.