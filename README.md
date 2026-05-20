# aoa-evals

Public library of portable evaluation bundles for agents and agent-shaped workflows.

`aoa-evals` is the proof layer in the AoA public surface. Where `aoa-techniques` stores reusable practice and `aoa-skills` stores bounded execution bundles, `aoa-evals` stores **evaluation bundles** that make claims about quality, boundaries, regressions, artifact output, and repeated-window movement reproducible, reviewable, and portable.

An eval here is not a random benchmark and not a pile of project-local tests. It is a bounded proof surface with clear claim limits, explicit scoring or verdict logic, defined fixtures or cases, known blind spots, and portable execution guidance.

> Current release: `v0.3.3`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- first concrete source-owned proof surface: `bundles/aoa-bounded-change-quality/EVAL.md`
- system form: `DESIGN.md`
- agent-facing guidance form: `DESIGN.AGENTS.md`
- proof topology and authority classes: `docs/PROOF_TOPOLOGY.md`
- legacy and accepted-input naming: `docs/LEGACY_NAMING.md`
- agent lane district: `.agents/AGENTS.md` and `.agents/spark/AGENTS.md`
- active proof operations atlas: `mechanics/README.md`
- active proof-loop route: `mechanics/proof-loop/README.md`
- first proof-loop route-smoke report:
  `reports/proof-loop-local-route-smoke-v1.md`
- first bundle-local proof-loop report:
  `bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
- first receipt-intake dry review:
  `reports/eval-result-receipt-intake-dry-review-v1.json`
- proof-release readiness audit:
  `reports/proof-release-readiness-audit-v1.json`
- strategic closeout audit:
  `reports/strategic-closeout-audit-v1.json`
- release-prep PR handoff:
  `reports/release-prep-pr-handoff-v1.json`
- docs map: `docs/README.md`
- current direction: `ROADMAP.md`
- proof obligations: `QUESTBOOK.md` and lane/state source records routed by
  `quests/README.md` and `quests/LIFECYCLE.md`
- repeated-window stress recovery proof surface: `bundles/aoa-stress-recovery-window/EVAL.md` and `docs/STRESS_RECOVERY_WINDOW_EVALS.md`
- self-agency continuity proof surfaces: `bundles/aoa-continuity-anchor-integrity/EVAL.md`, `bundles/aoa-reflective-revision-boundedness/EVAL.md`, and `bundles/aoa-self-reanchor-correctness/EVAL.md`
- proof posture and limits: `docs/EVAL_PHILOSOPHY.md`
- architecture: `docs/ARCHITECTURE.md`
- durable decisions: `docs/decisions/`
- current eval surface and chooser: `EVAL_INDEX.md` and `EVAL_SELECTION.md`
- Titan incarnation boundary canaries: `docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan-canaries/README.md`, and `evals/titan_*_canary.yaml`
- Agon pre-protocol proof alignment: `mechanics/agon-proof/README.md`,
  `docs/AGON_EVAL_PREBINDING_MODEL.md`, and
  `docs/AGON_EVAL_OWNER_HANDOFFS.md`
- authoring template: `templates/EVAL.template.md`

## Route by need

- score semantics, verdict boundaries, and review posture: `docs/SCORE_SEMANTICS_GUIDE.md`, `docs/VERDICT_INTERPRETATION_GUIDE.md`, `docs/EVAL_RUBRIC.md`, and `docs/EVAL_REVIEW_GUIDE.md`
- derived reader surfaces: `generated/eval_catalog.min.json`,
  `generated/eval_capsules.json`, `generated/eval_sections.full.json`, and
  `generated/eval_report_index.min.json`
- proof topology before mechanics or file movement: `docs/PROOF_TOPOLOGY.md`
- legacy, historical, accepted-input, generated-projection, and candidate-only
  names: `docs/LEGACY_NAMING.md`
- proof-object and bundle lifecycle operation:
  `mechanics/proof-object/README.md`
- comparison spine operation:
  `mechanics/comparison-spine/README.md`
- shared proof infrastructure operation:
  `mechanics/proof-infra/README.md`
- active proof-loop operation: `mechanics/proof-loop/README.md`
- quest obligation operation: `mechanics/questbook/README.md`
- runtime candidate evidence operation: `mechanics/runtime-evidence/README.md`
- sibling proof-reference compatibility: `docs/SIBLING_PROOF_REFS.md` and `mechanics/sibling-proof-refs/README.md`
- maintained Spark fast-loop lane: `.agents/spark/AGENTS.md` and
  `.agents/spark/SWARM.md`
- regression, peer comparison, and repeated-window reading:
  `docs/COMPARISON_SPINE_GUIDE.md`,
  `mechanics/comparison-spine/README.md`,
  `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`, and
  `generated/comparison_spine.json`
- bounded stress recovery longitudinal reading: `docs/STRESS_RECOVERY_WINDOW_EVALS.md` and `bundles/aoa-stress-recovery-window/EVAL.md`
- stats-driven re-grounding boundary proof: `bundles/aoa-stats-regrounding-boundary-integrity/EVAL.md`
- bounded self-agency continuity reading: `bundles/aoa-continuity-anchor-integrity/EVAL.md`, `bundles/aoa-reflective-revision-boundedness/EVAL.md`, and `bundles/aoa-self-reanchor-correctness/EVAL.md`
- via negativa pruning checklist: `docs/VIA_NEGATIVA_CHECKLIST.md`
- artifact-side versus process-side reading: `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- runtime-artifact to verdict bridge: `docs/TRACE_EVAL_BRIDGE.md`, `docs/TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md`, `docs/EVAL_RESULT_RECEIPT_GUIDE.md`, and `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- Titan incarnation proof seeds: `docs/TITAN_INCARNATION_CANARIES.md`,
  `mechanics/titan-canaries/README.md`,
  `evals/titan_incarnation_spine_canary.yaml`,
  `evals/titan_named_summon_no_generic_shadow_canary.yaml`,
  `evals/titan_forge_gate_payload_canary.yaml`,
  `evals/titan_delta_gate_payload_canary.yaml`,
  `evals/titan_memory_source_ref_canary.yaml`, and
  `evals/titan_lineage_non_erasure_canary.yaml`
- Agon pre-protocol proof alignment:
  `mechanics/agon-proof/README.md`, `docs/AGON_COURT_PREBINDING.md`,
  `docs/AGON_EVAL_PREBINDING_MODEL.md`,
  `docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`,
  `config/agon_eval_prebindings.seed.json`, and
  `generated/agon_eval_prebinding_registry.min.json`
- local shared-envelope mirror and eval publication seam:
  `docs/EVAL_RESULT_RECEIPT_GUIDE.md`,
  `reports/eval-result-receipt-intake-dry-review-v1.json`, and
  `mechanics/publication-receipts/README.md`
- portability, fixtures, and baseline-boundary guides: `docs/FIXTURE_SURFACE_GUIDE.md`, `docs/BLIND_SPOT_DISCLOSURE_GUIDE.md`, `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md`, and `docs/BASELINE_COMPARISON_GUIDE.md`
- shared proof infra and portable report surfaces:
  `docs/SHARED_PROOF_INFRA_GUIDE.md`,
  `mechanics/proof-infra/README.md`, `fixtures/`, `runners/`, `scorers/`,
  `reports/`, and `schemas/`
- adjunct progression, self-agent, and recurrence seams: `docs/PROGRESSION_EVIDENCE_MODEL.md`, `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`, and `docs/RECURRENCE_PROOF_PROGRAM.md`
- selection and release surfaces: `EVAL_SELECTION.md`, `docs/RELEASING.md`,
  `reports/proof-release-readiness-audit-v1.json`,
  `reports/strategic-closeout-audit-v1.json`, and
  `reports/release-prep-pr-handoff-v1.json`, and
  `mechanics/proof-release/README.md`

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
python scripts/generate_eval_report_index.py --check
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q tests
```

Refresh the derived reader catalogs only when you intentionally need to rewrite them:

```bash
python scripts/build_catalog.py
python scripts/generate_eval_report_index.py
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
