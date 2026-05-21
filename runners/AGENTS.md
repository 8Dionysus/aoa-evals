# AGENTS.md

Local guidance for `runners/`.

## Purpose

This directory is a compatibility route card for shared runner contracts, not
hidden harness logic.

## Current surfaces

- `README.md`

Active runner payload:

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`

## Rules

Keep runner contracts explicit about bounded inputs, shared fixture replacement, scorer helper use, and report schema validation.
Bundle-local `bundles/<bundle>/runners/contract.json` files should point to the active
part-local surface through `runner_surface_path` instead of silently forking
runner doctrine.
If one bundle participates in more than one shared readout, keep the main dossier in `paired_readout_path` and list the rest in `additional_paired_readout_paths`.
Keep dossier guidance weaker than the bundle-local `EVAL.md` boundary.
Do not recreate root active runner payload aliases here.
