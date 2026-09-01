# KAG Provider Validation

This on-demand route validates the owner-local provider first, then the
stronger `aoa-kag` provider-family contract. It does not make the generated
provider view proof authority.

## Owner-local check

```bash
python scripts/validate_repo.py
```

## Cross-owner provider check

Set `AOA_KAG_ROOT` to the exact prepared `aoa-kag` checkout. Its provider
registry must name the current `aoa-evals` commit before this check can pass.

```bash
AOA_EVALS_ROOT="$PWD" python "${AOA_KAG_ROOT:?set AOA_KAG_ROOT}/scripts/validate_kag.py" --scope os-wide
```
