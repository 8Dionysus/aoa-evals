# AGENTS.md

## Applies to

`mechanics/proof-infra/parts/fixture-families/`.

## Role

This part owns generic shared fixture-family support for proof objects.

It does not own bundle meaning, verdict logic, memo truth, audit acceptance,
comparison semantics, runtime evidence, or sibling owner truth.

Families here must stay public-safe and reviewable without hidden local
context.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/proof-infra/README.md`
6. `mechanics/proof-infra/PARTS.md`
7. `mechanics/proof-infra/parts/fixture-families/README.md`
8. affected `bundles/*/EVAL.md`
9. affected `bundles/*/fixtures/contract.json`

## Boundaries

- Keep the family weaker than the bundle-local claim.
- Keep `shared_fixture_family_path` explicit and current.
- Move a family out of this part only when a narrower active mechanic owns the
  operation and a decision/provenance bridge records the move.
- Do not add hidden benchmark cases, private logs, or source-owner secrets.

## Validation

Run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run targeted bundle validation for any bundle whose fixture contract changed.

## Closeout

Report which fixture families moved or changed, which source bundles still own
the proof meaning, which generated readers were rebuilt, and which active
mechanic boundary remained stronger.
