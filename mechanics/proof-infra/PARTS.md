# Proof Infra Parts

## Role

`PARTS.md` lists the active parts inside `mechanics/proof-infra/`.

It is not a generic inventory of every fixture, runner, scorer, schema, report,
or template in the repository. A part is active only when `proof-infra` owns the
operation and the stronger proof meaning stays in the bundle or owning
mechanic.

## Active Parts

### `fixture-families`

Owned operation:

`bundle support need -> reusable public-safe fixture family -> bundle-local fixture contract -> generated proof_artifacts`

This part owns generic shared fixture-family support when no narrower
AoA-aligned or evals-native mechanic owns the family.

Active families:

- `ambiguity-bounded-v1`
- `approval-boundary-bounded-v1`
- `local-text-contract-v1`
- `memo-contradiction-guardrail-v1`
- `memo-writeback-act-guardrail-v1`
- `ring-application-discipline-v1`
- `scope-drift-bounded-v1`
- `tool-trajectory-bounded-v1`
- `trace-outcome-bounded-v1`
- `verification-honesty-v1`
- `witness-trace-v1`

### `reportable-contracts`

Owned operation:

`bundle report need -> shared reportable proof contract -> bundle-local runner contract -> schema-backed report artifact -> generated proof_artifacts`

This part owns the reusable runner surface, bounded scorer helper, and shared
schemas that bundle-local runner/report contracts use when a bundle exposes
machine-readable proof artifacts.

Active surfaces:

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json`

## Part Contract

Inputs are bundle support needs, reusable fixture-family requirements,
reportable runner/scorer/schema contracts, and generated `proof_artifacts`
references.

Outputs are shared fixture-family support, reusable reportable proof contracts,
bounded scorer helpers, schema-backed report artifacts, and catalog-visible
proof artifact routes.

Owner split stays explicit: proof-infra owns reusable support contracts; source
bundles, bundle-local runner contracts, report schemas, and owning mechanics
keep stronger proof meaning.

Stop-lines forbid promoting fixture family names into parent mechanics,
recreating active root infrastructure aliases, or absorbing bundle-local proof
objects and reviewed reports.

Validation is `python scripts/build_catalog.py --check`,
`python scripts/validate_repo.py`, and
`python scripts/validate_semantic_agents.py`, plus targeted bundle checks when
shared fixture or reportable paths move.

## Stop-Lines

- Do not promote a fixture family name into a parent mechanic.
- Do not move a family here when an active mechanic part already owns the
  operation.
- Do not treat fixture-family placement as proof acceptance.
- Keep former root fixture-family aliases as historical compatibility
  vocabulary for active families.
- Do not recreate active root `runners/`, `scorers/`, or `schemas/` payload
  aliases for reportable contracts.
- Do not treat `runner_surface_path`, `scorer_helper_paths`, or shared schemas
  as stronger than bundle-local `EVAL.md`, `eval.yaml`, report schemas, or
  reviewed reports.
- Do not use this part to absorb bundle-local `EVAL.md`, `eval.yaml`, runner
  contracts, report schemas, or reviewed reports.

## Validation

After part movement, fixture-family path changes, or reportable contract path
changes, run:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run targeted bundle validation for every bundle whose
`shared_fixture_family_path`, `runner_surface_path`, or `scorer_helper_paths`
changed.
