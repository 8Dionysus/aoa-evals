# Portable Proof Beacons Part

## Role

This part owns the recurrence beacon route for
`component:evals:portable-proof-beacons`.

It keeps portable-proof pressure, progression-evidence pressure, and
anti-overclaim pressure in a recurrence-owned watch/candidate/review ladder
instead of turning `portable-proof-beacons` into a parent mechanic.

## Source Surfaces

- `mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/component.evals.portable-proof-beacons.json`
- `mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json`
- `mechanics/recurrence/parts/portable-proof-beacons/docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`
- `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md`

## Inputs

- source proof bundle changes;
- trace-eval bridge pressure and runtime candidate packet selections;
- progression evidence and unlock proof pressure;
- recurrence proof-program stop-lines;
- portable eval boundary guidance;
- hook observations from `session_stop` runtime-candidate watch surfaces.

## Outputs

- beacon statuses from `hint` through `watch`, `candidate`, and
  `review_ready`;
- drift signals for runtime bridge, progression model, and overclaim risk;
- refresh or repair command routes for portable proof surfaces;
- decision-packet closure guidance for whether evidence stays local, travels as
  sidecar evidence, or begins owner-reviewed portable eval authoring;
- no accepted portable proof verdict by itself.

## Stronger Owner Split

`mechanics/audit/` owns runtime candidate intake, artifact-to-verdict hook
shape, and selected evidence packet curation.

`mechanics/rpg/` owns progression and unlock proof support.

Source proof bundles own claim wording, verdict semantics, fixtures, and
interpretation.

`Agents-of-Abyss` owns recurrence doctrine. Runtime owners keep runtime truth.

`aoa-evals` owns only the bounded proof interpretation and the recurrence
beacon route that notices repeated proof pressure.

## Stop-Lines

Do not use this part to claim:

- runtime artifacts as candidate evidence are proof canon;
- portable proof is accepted without bundle-local review;
- progression evidence creates a universal score or automatic unlock;
- a beacon is a verdict;
- a recurrence manifest owns audit, RPG, runtime, or sibling truth;
- overclaim detection replaces proof-object repair.

## Validation

Payload coverage anchor: `mechanics/recurrence/parts/portable-proof-beacons/`.

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
```
