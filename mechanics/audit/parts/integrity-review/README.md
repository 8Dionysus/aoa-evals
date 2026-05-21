# Integrity Review

## Role

This part owns the owner-local runtime integrity review contract.

It captures W10-shaped runtime continuity evidence as `candidate_only`, keeps
human review mandatory, and points upward to the stronger Experience owner split
instead of defining activation authority locally.

## Source Surfaces

- `mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md`
- `mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json`
- `mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json`

## Inputs

- candidate-only W10 runtime continuity evidence refs;
- replay requirement fields and forbidden-claim constraints;
- budget refs, reviewer refs, and owner-route refs;
- selected runtime evidence and trace refs that stay below proof canon.

## Outputs

- schema-backed `runtime_integrity_review.example.json`;
- a review guide for owner-local runtime continuity inspection;
- explicit replay and authority-jump requirements;
- bounded candidate posture for later Experience or bundle-local review.

## Stronger Owner Split

`aoa-evals` owns the runtime integrity review contract and candidate-only
interpretation limits.

Runtime activation, continuity truth, memory canon, and Experience owner truth
stay outside this audit part until their owning surfaces accept them.

## Boundary

The review surface does not become proof canon, runtime activation authority,
owner override, or canon write permission.

## Stop-Lines

- Do not activate runtime continuity from this review.
- Do not write memory canon, owner approval, or proof verdicts from this
  candidate-only artifact.
- Do not remove human review or replay requirements.

## Validation

Payload coverage anchor: `mechanics/audit/parts/integrity-review/`.

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_validate_repo.py -k runtime_integrity_review
```
