# Recurrence / Portable Proof Beacons Part

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
- `docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md`

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
- owner-reviewed portable eval route when accepted portable proof pressure
  appears.

## Stronger Owner Split

`mechanics/audit/` owns runtime candidate intake, artifact-to-verdict hook
shape, and selected evidence packet curation.

`mechanics/rpg/` owns progression and unlock proof support.

Source proof bundles own claim wording, verdict semantics, fixtures, and
interpretation.

`Agents-of-Abyss` owns recurrence doctrine. Runtime owners keep runtime truth.

`aoa-evals` owns only the bounded proof interpretation and the recurrence
beacon route that notices repeated proof pressure. Authority beyond that proof
reading routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep portable-proof-beacon pressure with the owner that can act
on it:

| Pressure | Owner route |
| --- | --- |
| runtime artifact proof-canon pressure | audit-selected evidence route plus source proof bundle review |
| accepted portable proof pressure | bundle-local review plus owner-reviewed portable eval authoring route |
| universal score or automatic unlock pressure | `mechanics/rpg/` progression route plus owner acceptance |
| beacon-as-verdict pressure | recurrence decision closure plus bundle-local proof review |
| recurrence manifest ownership of audit, RPG, runtime, or sibling truth pressure | owning audit, RPG, runtime, or sibling source surface |
| overclaim repair pressure | proof-object repair route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
