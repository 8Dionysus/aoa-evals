# aoa-evals

Public library of portable evaluation bundles for agents and agent-shaped workflows.

`aoa-evals` is the proof layer in the AoA public surface. Where `aoa-techniques` stores reusable practice and `aoa-skills` stores bounded execution bundles, `aoa-evals` stores **evaluation bundles** that make claims about quality, boundaries, regressions, artifact output, and repeated-window movement reproducible, reviewable, and portable.

An eval here is not a random benchmark and not a pile of project-local tests. It is a bounded proof surface with clear claim limits, explicit scoring or verdict logic, defined fixtures or cases, known blind spots, and portable execution guidance.

## Start here

Use the shortest route by need:

- first concrete source-owned proof surface: `bundles/aoa-bounded-change-quality/EVAL.md`
- docs map: `docs/README.md`
- repeated-window stress recovery proof surface: `bundles/aoa-stress-recovery-window/EVAL.md` and `docs/STRESS_RECOVERY_WINDOW_EVALS.md`
- proof posture and limits: `docs/EVAL_PHILOSOPHY.md`
- architecture: `docs/ARCHITECTURE.md`
- current eval surface and chooser: `EVAL_INDEX.md` and `EVAL_SELECTION.md`
- authoring template: `templates/EVAL.template.md`

## Route by need

- score semantics, verdict boundaries, and review posture: `docs/SCORE_SEMANTICS_GUIDE.md`, `docs/VERDICT_INTERPRETATION_GUIDE.md`, `docs/EVAL_RUBRIC.md`, and `docs/EVAL_REVIEW_GUIDE.md`
- derived reader surfaces: `generated/eval_catalog.min.json`, `generated/eval_capsules.json`, and `generated/eval_sections.full.json`
- regression, peer comparison, and repeated-window reading: `docs/COMPARISON_SPINE_GUIDE.md`, `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`, and `generated/comparison_spine.json`
- bounded stress recovery longitudinal reading: `docs/STRESS_RECOVERY_WINDOW_EVALS.md` and `bundles/aoa-stress-recovery-window/EVAL.md`
- artifact-side versus process-side reading: `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- runtime-artifact to verdict bridge: `docs/TRACE_EVAL_BRIDGE.md`, `docs/EVAL_RESULT_RECEIPT_GUIDE.md`, and `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- local shared-envelope mirror and eval publication seam:
  `docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- portability, fixtures, and baseline-boundary guides: `docs/FIXTURE_SURFACE_GUIDE.md`, `docs/BLIND_SPOT_DISCLOSURE_GUIDE.md`, `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md`, and `docs/BASELINE_COMPARISON_GUIDE.md`
- shared proof infra and portable report surfaces: `docs/SHARED_PROOF_INFRA_GUIDE.md`, `fixtures/`, `runners/`, `scorers/`, `reports/`, and `schemas/`
- adjunct progression, self-agent, and recurrence seams: `docs/PROGRESSION_EVIDENCE_MODEL.md`, `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`, and `docs/RECURRENCE_PROOF_PROGRAM.md`
- selection and release surfaces: `EVAL_SELECTION.md` and `docs/RELEASING.md`

## What belongs here

Good candidates:

- portable eval bundles for agent behavior
- bounded workflow evaluations
- boundary and authority adherence evals
- artifact-quality evals
- regression and comparison evals
- longitudinal movement evals
- scorers, rubrics, and verdict schemas
- shared fixture and runner contracts
- schema-backed report examples

Bad candidates:

- random tests with no portable evaluation contract
- raw project-local QA that was not generalized
- secret-bearing fixtures or logs
- massive uncurated run dumps
- techniques that belong in `aoa-techniques`
- skills that belong in `aoa-skills`
- undocumented scoring logic
- metrics with no interpretation boundary
- claims stronger than the evidence actually supports

## Core distinction

- `aoa-techniques` owns practice meaning
- `aoa-skills` owns bounded workflow meaning
- `aoa-evals` owns bounded proof meaning

In short:

`practice canon -> workflow canon -> proof canon`

The current public runtime path remains:

`pick -> inspect -> expand -> object use`

## What this repository does not try to do

`aoa-evals` does not provide a final or total measure of intelligence.
It does not reduce agent quality to one number.
It does not treat any single eval as the whole truth.

This repository prefers explicit limits over false objectivity.

## Local validation

Install local dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the minimum repository check:

```bash
python scripts/validate_repo.py
```

Run the current full non-mutating proof-surface battery when you need parity across authored, generated, and adjunct surfaces:

```bash
python scripts/build_catalog.py --check
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q tests
```

Refresh the derived reader catalogs only when you intentionally need to rewrite them:

```bash
python scripts/build_catalog.py
```

If local sibling repositories are not checked out beside this repo, some dependency-target existence checks stay in the looser local path. Use the documented environment variables when you need the stricter federated path.

## Go elsewhere when...

- you need reusable practice meaning: `aoa-techniques`
- you need the bounded workflows under evaluation: `aoa-skills`
- you need routing and dispatch: `aoa-routing`
- you need role posture or handoff context: `aoa-agents`
- you need scenario-level composition: `aoa-playbooks`

## License

Apache-2.0
