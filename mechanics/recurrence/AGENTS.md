# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/recurrence/DIRECTION.md` for current operating direction, `mechanics/recurrence/PARTS.md` for active parts, and `mechanics/recurrence/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/recurrence/` and recurrence-owned part-local support surfaces.

## Role

This package routes recurrence proof work inside `aoa-evals`.

It maps recurrence proof pressure to control-plane integrity, anchor return,
memory recall, recursor boundary, stats regrounding, portable-proof beacons,
bundle-local review, or stronger-owner handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | recurrence proof work route inside `aoa-evals` |
| input | recurrence support artifact, scorer/runner/schema/fixture/manifest/example change, candidate-only runtime evidence, beacon, or owner-routing question |
| output | active part route, bundle-local review, generated surface check, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded recurrence proof support; stronger owners keep doctrine, runtime return, memory anchors, routing, scenario choreography, Agon runtime authority, and artifact promotion |
| next route | `mechanics/recurrence/README.md`, `DIRECTION.md`, `PARTS.md`, target part README, and source proof bundle |
| tools | part-local execution checks, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/architecture/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/recurrence/README.md`
6. `mechanics/recurrence/PARTS.md`
7. target part `README.md`
8. `mechanics/recurrence/PROVENANCE.md` as the active-to-archive bridge for old placement or raw lineage

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep recurrence support artifacts part-local when a recurrence part owns
  their scorer, runner, schema, fixture, manifest, or example route.
- Keep runtime return evidence candidate-only until a bundle accepts it.
- Keep beacons, downstream projections, and Agon diagnostics weaker than owner
  decisions and source truth.
- Create recurrence parts from a multi-surface proof operation with validator
  coverage.

## Validation

```bash
python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py
python mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py --case mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/cases/RRB-001.no-spawn-readiness.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py
python scripts/validate_repo.py
```

## Closeout

Report which recurrence proof route changed, which owner truth stayed stronger,
which generated surfaces were refreshed, and which recurrence family remains
deferred or bundle-local.
