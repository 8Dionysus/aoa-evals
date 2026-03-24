# AGENTS.md

Local guidance for `runners/`.

## Purpose

This directory stores top-level runner contracts for portable proof execution, not hidden harness logic.

## Current surfaces

- `README.md`
- `reportable_proof_contract.md`

## Rules

Keep runner contracts explicit about bounded inputs, shared fixture replacement, scorer helper use, and report schema validation.
Bundle-local `runners/contract.json` files should point back to these top-level surfaces instead of silently forking runner doctrine.
If one bundle participates in more than one shared readout, keep the main dossier in `paired_readout_path` and list the rest in `additional_paired_readout_paths`.
Keep dossier guidance weaker than the bundle-local `EVAL.md` boundary.
