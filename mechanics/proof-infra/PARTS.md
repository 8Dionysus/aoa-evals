# Proof Infra / Part Index

## Role

`PARTS.md` lists the active parts inside `mechanics/proof-infra/`.

Use it to route shared proof-support pressure into the active part, payload
home, stronger owner, and validation lane:

`shared support pressure -> active part -> payload home -> stronger owner -> validation route`

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

Stop-lines route fixture-family parent pressure, former root aliases, and
bundle-local proof objects through the boundary routes below.

Validation routes through [AGENTS](AGENTS.md#validation) and the affected part
route cards, plus targeted bundle checks when shared fixture or reportable
paths move.

## Boundary Routes

| Pressure | Route |
| --- | --- |
| Fixture-family parent pressure | `mechanics/EVIDENCE_CLUSTERS.md` before any parent proposal; fixture-family names stay part-local support. |
| Domain-owned fixture pressure | the narrower active mechanic part that owns the operation. |
| Fixture placement as proof acceptance | bundle-local `EVAL.md`, `eval.yaml`, fixture contract, and reviewed report. |
| Former root fixture aliases | `PROVENANCE.md` and `legacy/` as historical compatibility vocabulary. |
| Root `runners/`, `scorers/`, or `schemas` alias pressure | route-card-only root districts plus the active `reportable-contracts` part paths. |
| `runner_surface_path`, `scorer_helper_paths`, or shared schema authority pressure | bundle-local interpretation surfaces and reviewed reports. |
| Bundle-local proof-object or report pressure | source bundle files, bundle-local runner contracts, report schemas, and reviewed reports. |

## Validation

After part movement, fixture-family path changes, or reportable contract path
changes, use [AGENTS](AGENTS.md#validation) for executable validation commands.

Run targeted bundle validation for every bundle whose
`shared_fixture_family_path`, `runner_surface_path`, or `scorer_helper_paths`
changed.
