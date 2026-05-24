# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/titan/DIRECTION.md` for current operating direction, `mechanics/titan/PARTS.md` for active parts, and `mechanics/titan/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/titan/` and Titan canary route guidance.

## Role

This package routes Titan proof-seed boundary work. The current payloads are
Titan seed canaries.

It keeps owner-named Titan boundary pressure seed-defined, falsifiable, and
ready for later scorer or stronger-owner review. The current proof claim is
seed-boundary evidence only; full incarnation proof routes to stronger owner
review.

## Operating Card

| Field | Route |
| --- | --- |
| role | Titan proof-seed boundary route for Titan seed canaries |
| input | seed canary YAML, mutation gate change, judgment gate change, canary docs, or `validate_titan_canary_surfaces` pressure |
| output | seed-boundary update, validation route, scorer-readiness handoff, or stronger-owner Titan route |
| owner | this package owns eval-side seed-boundary proof; stronger Titan doctrine and runtime owners keep summon, memory, incarnation, and activation law |
| next route | `mechanics/titan/README.md`, `DIRECTION.md`, `PARTS.md`, seed-boundary docs, `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`, and affected `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml` |
| tools | root validator, semantic AGENTS validator, titan canary tests, `validate_titan_canary_surfaces` |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| seed canary payload | `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml` |
| mutation gate or judgment gate posture | seed-boundary docs and canary validation |
| executable scorer behavior | later scorer contract before proof strengthening |
| Titan doctrine, summon, incarnation, or runtime activation | stronger owner route outside `aoa-evals` |
| memory truth | memory owner route before adoption |
| legacy canary vocabulary | `mechanics/titan/PROVENANCE.md` and validator-backed compatibility path |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/LEGACY_NAMING.md`
6. `mechanics/README.md`
7. `mechanics/titan/README.md`
8. `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`
9. `mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`
10. `mechanics/titan/parts/seed-boundary/seeds/README.md`
11. `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`
12. affected `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`
13. `scripts/validate_repo.py` function `validate_titan_canary_surfaces`

## Local Law

- Keep `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml` seed-defined until executable scorer
  contracts exist.
- Keep canary `id` or `eval_id` equal to the filename stem.
- Keep each canary falsifiable through `checks`, `expected_failure`,
  `expected_result`, `expected`, `forbidden`, or failure examples.
- Keep mutation gate and judgment gate boundaries explicit.
- Keep memory canaries candidate-only and source-ref oriented.
- Keep named Titan language from collapsing into generic role shadows.

## Route Rules

- Keep seed YAML files inside this package unless a later decision creates a
  stronger source home.
- Keep seed canaries framed as seed-boundary evidence; route full incarnation
  proof to stronger owners.
- Route runtime, hidden arena, and live summon behavior to stronger owners.
- Keep Titan canaries below stronger owner law.
- Change legacy canary vocabulary compatibility through a decision and
  validator-backed compatibility path.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```

Run broader generated and release checks when canary changes affect public
selection, catalogs, release posture, or generated readers.

## Closeout

Report which Titan boundary pressure changed, which canary YAML files changed,
whether the change is still seed-defined or scorer-backed, what validation ran,
and which stronger-owner Titan law or runtime boundary stayed outside
`aoa-evals`.
