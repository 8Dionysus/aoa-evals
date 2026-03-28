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
5. Read `docs/COMPARISON_SPINE_GUIDE.md` if your question is about regression, peer comparison, or repeated-window movement.
6. Read `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` if your question is about artifact-side versus process-side reading.
7. Read `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` if your question is about repeated-window comparability and cautious movement language.
8. Open `bundles/aoa-bounded-change-quality/EVAL.md` as the first starter eval bundle.
9. Use `templates/EVAL.template.md` when authoring a new eval.

## Quick routes

- if you need upstream reusable practice, go to [aoa-techniques](https://github.com/8Dionysus/aoa-techniques)
- if you need bounded execution workflows to evaluate, go to [aoa-skills](https://github.com/8Dionysus/aoa-skills)
- if you need the smallest next surface by task type, go to [aoa-routing](https://github.com/8Dionysus/aoa-routing)
- if you need role posture or handoff context around an evaluation target, go to [aoa-agents](https://github.com/8Dionysus/aoa-agents)
- if you need scenario-level operating context, go to [aoa-playbooks](https://github.com/8Dionysus/aoa-playbooks)
- if you need the runtime-artifact or trace-to-verdict seam, read `docs/TRACE_EVAL_BRIDGE.md`
- if you need the bounded bridge from `abyss-stack` runtime artifacts into selected proof inputs, read `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- if you need the self-agent checkpoint eval landing, read `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- if you need the recurrence-aware proof program for bounded anchor fidelity and honest re-entry, read `docs/RECURRENCE_PROOF_PROGRAM.md`
- if you need the current comparison ladder, read `docs/COMPARISON_SPINE_GUIDE.md`
- if you need the artifact/process read order, read `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- if you need cautious repeated-window reading, read `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- if you need shared fixture/runner/scorer conventions, read `docs/SHARED_PROOF_INFRA_GUIDE.md`

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
- schema-backed report examples and bundle-local runner contracts
- selected runtime benchmark evidence dossiers when they preserve bounded claim meaning

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

The current runtime path for public eval use is:

`pick -> inspect -> expand -> object use`

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
- `generated/` — derived routing catalogs, reader catalogs, and local runtime cards
- `templates/` — templates for eval authoring and metadata
- `bundles/` — eval bundles
- `fixtures/` — shared reusable fixture families and replacement contracts
- `scorers/` — shared bounded breakdown helpers
- `runners/` — portable runner contracts for schema-backed proof artifacts
- `schemas/` — machine-readable bundle and report contracts
- `examples/` — derived hook examples that bind playbook artifacts to existing eval bundles
- `reports/` — compact public summary artifacts and paired readout dossiers
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
- optional `reports/example-report.json`
- optional `runners/contract.json`
- optional `notes/blind-spots.md`

`EVAL.md` and `eval.yaml` remain authoritative.
`generated/eval_catalog.json`, `generated/eval_catalog.min.json`, and `generated/eval_capsules.json` are derived reader surfaces for routing, indexing, and local runtime lookup cards.
`generated/comparison_spine.json` is the filtered comparison-only routing and selection surface for `fixed-baseline`, `peer-compare`, and `longitudinal-window` bundles.
`generated/eval_sections.full.json` is the source-owned section payload surface for bounded expand-time reads.
`docs/TRACE_EVAL_BRIDGE.md`, `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`, `docs/RECURRENCE_PROOF_PROGRAM.md`, `examples/artifact_to_verdict_hook.*.example.json`, and `examples/runtime_evidence_selection.*.example.json` are derived bridge surfaces for runtime evidence inputs; they do not change eval bundle ownership, wording, or status.

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

This repository remains in public bootstrap,
now with the first materialized comparison wave for frozen same-task and repeated-window surfaces.
The next public hardening step is a coherent comparison spine rather than isolated comparison bundles.
The first draft memo-recall integrity pilot is now also present as a non-starter diagnostic bundle anchored to `aoa-memo` guardrail surfaces, but it remains intentionally narrower than the broader comparison and starter programs.
The witness/compost pilot pair now also has materialized draft case families,
runner contracts, and schema-backed report artifacts, while remaining weaker
than runtime instrumentation and canon claims.
The current bounded scope-alignment diagnostic now also has a materialized case
family, runner contract, and schema-backed report example without changing its
bounded status.
The first recurrence-aware proof surface now also has a materialized draft case family and runner contract in `aoa-return-anchor-integrity`, while remaining outside the starter set.

The current goal is to establish:
- the public doctrine for bounded agent evaluation
- the eval bundle shape and metadata contracts
- the first starter eval bundles
- portable scoring and report surfaces
- shared fixture families, runner contracts, and schema-backed report examples for materialized comparison flows and diagnostic pilots
- baseline comparison discipline
- artifact/process separation doctrine that stays weaker than standalone bundle meaning
- repeated-window discipline that stays weaker than broad growth claims
- the path toward trustworthy regression and longitudinal evaluation

## Read this before overclaiming

`aoa-evals` supports bounded proof surfaces, not total intelligence scores; `What this repository does not try to do` below defines what one eval result can and cannot support.

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

If `aoa-techniques` or `aoa-skills` are not checked out beside this repo,
local validation will skip dependency-target existence checks for those sibling surfaces.
CI runs the stricter path-existence check by exporting `AOA_TECHNIQUES_ROOT` and `AOA_SKILLS_ROOT`
after checking those repositories out into `.deps/`.

Build the derived reader catalogs:

```bash
python scripts/build_catalog.py
```

For CI parity, also run:

```bash
python scripts/build_catalog.py --check
```

The validator checks that generated catalogs and capsules exist, stay current, keep the min catalog as an exact projection of the full catalog, and keep capsules aligned 1:1 with the catalog surface.
It also checks that `generated/comparison_spine.json` exists, stays current, and remains aligned with the comparison entries in `generated/eval_catalog.json`.
It also checks that `generated/eval_sections.full.json` exists, stays current, and remains 1:1 aligned with the catalog and capsule surfaces.
It also checks that comparison bundles with `baseline_mode != none` ship aligned comparison-surface metadata, materialized report artifacts, runner contracts, and fixture contracts when those public surfaces are in use.

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
