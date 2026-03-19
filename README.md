# aoa-evals

Public library of portable evaluation bundles for agents and agent-shaped workflows.

`aoa-evals` is the proof layer in the AOA public surface.
Where `aoa-techniques` stores public, reusable, validated engineering techniques,
and `aoa-skills` stores bounded agent-facing workflow bundles,
`aoa-evals` stores **evaluation bundles** that make claims about agent quality,
boundaries, regressions, and growth reproducible, reviewable, and comparable.

An eval here is not a random benchmark and not a pile of project-local tests.
It is a reusable proof surface with clear evaluation boundaries,
explicit scoring or verdict logic, defined fixtures or cases,
known blind spots, and portable execution guidance.

## Start here

If you are new to this repository, follow this short path:

1. Read `docs/README.md` for the docs map.
2. Read `docs/ARCHITECTURE.md` for the high-level model.
3. Read `docs/EVAL_PHILOSOPHY.md` for the core stance on proof, limits, and growth.
4. Read `EVAL_INDEX.md` for the current eval surface.
5. Open `bundles/aoa-bounded-change-quality/EVAL.md` as the first starter eval bundle.
6. Use `templates/EVAL.template.md` when authoring a new eval.

## What belongs here

Good candidates:
- portable eval bundles for agent behavior
- bounded workflow evaluations
- boundary and authority adherence evals
- artifact-quality evals
- regression and comparison evals
- longitudinal growth evals
- scorers, rubrics, and verdict schemas
- shared fixtures and baseline surfaces
- report contracts and interpretation guides

Bad candidates:
- random tests without a portable evaluation contract
- raw project-local QA that was not generalized
- secret-bearing fixtures or logs
- massive uncurated run dumps
- techniques that should live in `aoa-techniques`
- skills that should live in `aoa-skills`
- undocumented scoring logic
- metrics with no interpretation boundary
- evaluations that imply stronger claims than they actually support

## Core distinction

### `aoa-techniques`
Stores the public canon of reusable engineering techniques.
A technique is a minimal reproducible unit of engineering practice.

### `aoa-skills`
Stores bounded agent-facing execution bundles.
A skill packages one or more techniques into a reviewable workflow.

### `aoa-evals`
Stores the public canon of portable proof surfaces.
An eval bundle defines how to check a bounded claim about agent quality,
behavior, safety, artifact output, or change over time.

In short:

`practice canon -> workflow canon -> proof canon`

## Why this repository exists

Strong agents need more than artifacts, intentions, or convincing demos.

This repository exists to answer questions such as:
- what exactly can we currently defend as true about agent quality?
- under which boundaries is that claim valid?
- what improved, what regressed, and what only changed style?
- which outputs are robust, and which are fragile?
- what does one evaluation result actually mean, and what does it not mean?

`aoa-evals` exists to reduce self-deception,
accelerate grounded growth,
and keep agent quality tied to reproducible evidence.

## Core principles

- proof over impression
- bounded claims over vague confidence theater
- portable eval bundles over project-local magic
- comparability matters
- regression visibility matters
- blind spots must be named
- artifacts matter, but are not enough
- process matters, but is not enough
- human-readable meaning stays primary
- structured outputs must remain reviewable
- evaluation should support growth without pretending to be omniscience

## Repository structure

- `docs/` — architecture, philosophy, roadmap, conventions, interpretation guides
- `generated/` — derived routing and reader catalogs
- `templates/` — templates for eval authoring and metadata
- `bundles/` — eval bundles
- `fixtures/` — shared reusable fixture sets
- `scorers/` — shared scoring and verdict helpers
- `runners/` — execution helpers and portable runner surfaces
- `schemas/` — machine-readable bundle and report contracts
- `reports/` — compact public summary artifacts
- `scripts/` — local validation, build, and reporting helpers
- `EVAL_INDEX.md` — repository-wide eval map

Local working notes such as `TODO.local.md` and `PLANS.local.md` stay gitignored in each clone.
The public planning artifact for this repository is `docs/ROADMAP.md`, which remains tracked.

A typical eval bundle contains:
- `EVAL.md`
- `eval.yaml`
- optional `fixtures/`
- optional `scorers/`
- optional `examples/`
- optional `checks/`
- optional `reports/summary.schema.json`
- optional `notes/blind-spots.md`

`EVAL.md` and `eval.yaml` remain authoritative.
`generated/eval_catalog.json` and `generated/eval_catalog.min.json` are derived reader surfaces for routing and indexing.

## Evaluation bundle shape

A strong eval bundle should make these things explicit:
- intent
- object under evaluation
- bounded claim
- what is in scope and out of scope
- fixtures or case surface
- scoring or verdict logic
- baseline or comparison mode
- execution contract
- report shape
- failure modes
- blind spots
- interpretation guidance

An eval bundle should be understandable to a human reviewer
without hidden scoring assumptions or untracked private context.

## Eval categories

- `capability` — checks whether an agent can perform a bounded class of tasks
- `workflow` — checks multi-step behavior rather than isolated answers
- `boundary` — checks scope, authority, safety, and approval adherence
- `artifact` — checks the quality of produced code, docs, plans, diffs, or reports
- `regression` — checks whether a change made behavior worse
- `comparative` — compares versions, agents, modes, or policies
- `longitudinal` — checks growth or degradation across time
- `stress` — probes ambiguity, conflict, noise, or adversarial edge conditions

## Current repository phase

This repository is in bootstrap mode.

The current goal is to establish:
- the public doctrine for bounded agent evaluation
- the eval bundle shape and metadata contracts
- the first starter eval bundles
- portable scoring and report surfaces
- baseline comparison discipline
- the path toward trustworthy regression and longitudinal evaluation

## What this repository does not try to do

`aoa-evals` does not claim to provide a final or total measure of intelligence.
It does not reduce agent quality to one number.
It does not treat any single eval as the whole truth.

This repository prefers explicit limits over false objectivity.

## Local validation

Install the local dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the full repository check:

```bash
python scripts/validate_repo.py
```

Build the derived reader catalogs:

```bash
python scripts/build_catalog.py
```

The validator checks that generated catalogs exist, stay current, and keep the min catalog as an exact projection of the full catalog.

An eval should say:
- what it can support
- what it cannot support
- what kind of evidence it provides
- where interpretation must stay cautious

## Contribution model

A good eval bundle is usually born from a real need:
- a repeated failure mode
- a repeated quality claim that needs proof
- a regression surface that needs stabilization
- a workflow that needs bounded comparison
- an artifact class that needs clearer review and scoring

In short:

`observed need -> bounded eval design -> portable bundle -> review -> public proof surface`

## Intended users

- agent builders
- solo builders
- infra engineers
- evaluation designers
- AI workflow designers
- reviewers who need bounded evidence
- teams that want portable proof surfaces for agent quality

## License

Apache-2.0
