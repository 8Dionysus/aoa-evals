# AGENTS.md

## Applies to

`mechanics/recurrence/parts/portable-proof-beacons/`.

## Role

This part routes portable-proof beacon pressure inside the recurrence mechanic.

It does not own runtime evidence intake, progression proof, source proof bundle
meaning, portable proof acceptance, or recurrence doctrine.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/recurrence/README.md`
6. `mechanics/recurrence/PARTS.md`
7. `mechanics/recurrence/parts/portable-proof-beacons/README.md`
8. `mechanics/recurrence/PROVENANCE.md` only for old root placement

## Boundaries

- Keep `component:evals:portable-proof-beacons` inside `recurrence`; do not
  recreate `portable-proof-beacons` as a parent mechanic.
- Treat runtime artifacts as candidate evidence until bundle-local review
  accepts a bounded interpretation.
- Keep audit packet curation with `mechanics/audit/`.
- Keep progression and unlock support with `mechanics/rpg/`.
- Keep beacon statuses below verdicts and owner decisions.

## Validation

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
```

## Closeout

Report whether the recurrence beacon route changed, which audit/RPG/source
truth stayed stronger, which generated surfaces were checked, and whether any
old root manifest or closure path still appears.
