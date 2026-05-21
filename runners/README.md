# Runners Route

This directory is the compatibility route card for historical shared runner
contract paths.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root runner contract routing |
| entry | open when an old root runner path appears or a shared runner contract needs an owner |
| input | runner contract, bundle-local runner pointer, or old root runner reference |
| output | proof-infra reportable-contract runner route or bundle-local pointer review |
| owner | `runners/AGENTS.md` for route law; proof-infra reportable-contracts for the active shared runner |
| next route | `mechanics/proof-infra/parts/reportable-contracts/runners/` |
| validation | `runners/AGENTS.md` and proof-infra route checks |

The active shared reportable proof runner surface now lives at:

`mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`

Bundle-local `evals/<family>/<eval>/runners/contract.json` files point to that
part-local surface through `runner_surface_path`.

Use [AGENTS.md](AGENTS.md) for runner contract rules and old-path lineage.
