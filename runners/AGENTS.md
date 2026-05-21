# AGENTS.md

## Role

`runners/` is a route-card-only compatibility route card for shared runner
contract paths.

## Current surfaces

- `README.md`

Active runner payload:

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`

## Rules

Keep runner contracts explicit about bounded inputs, shared fixture replacement, scorer helper use, and report schema validation.
Bundle-local `evals/<family>/<eval>/runners/contract.json` files should point to the active
part-local surface through `runner_surface_path` instead of silently forking
runner doctrine.
If one bundle participates in more than one shared readout, keep the main dossier in `paired_readout_path` and list the rest in `additional_paired_readout_paths`.
Keep dossier guidance weaker than the bundle-local `EVAL.md` boundary.
Root active runner payload aliases route through proof-infra provenance and the
active part-local surface.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
