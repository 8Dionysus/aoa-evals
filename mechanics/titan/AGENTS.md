# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/titan/DIRECTION.md` for current operating direction, `mechanics/titan/PARTS.md` for active parts, and `mechanics/titan/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/titan/` and Titan canary route guidance.

## Role

This package routes Titan proof-seed boundary work. The current payloads are
Titan seed canaries.

It does not own Titan doctrine, runtime activation, summon authority, memory
truth, executable scorer behavior, or full incarnation proof. In short, these
route cards are not full incarnation proof.

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

## Boundaries

- Keep seed YAML files inside this package unless a later decision creates a
  stronger source home.
- Do not claim full incarnation proof from seed canaries.
- Do not activate runtime, hidden arena, or live summon behavior.
- Do not let Titan canaries override stronger owner law.
- Do not change legacy canary vocabulary compatibility without a decision and
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
