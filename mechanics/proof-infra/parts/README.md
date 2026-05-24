# Proof Infra / Parts Route

`mechanics/proof-infra/parts/` is the lower index for reusable proof-support
parts. Use it after the parent Proof Infra route has selected a shared support
operation and the next agent needs the exact part, payload home, owner route,
tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for reusable proof support contracts |
| input | bundle support need, reusable fixture-family requirement, reportable runner contract, scorer helper, shared schema, or generated proof-artifact reference |
| output | fixture-family route, reportable-contract route, shared schema route, generated proof-artifact route, or bundle-local review handoff |
| owner | proof-infra owns reusable support contracts; source bundles, bundle-local runner contracts, report schemas, and narrower mechanics keep stronger proof meaning |
| next route | `mechanics/proof-infra/PARTS.md`, selected part README, affected source bundle, bundle-local contract, and parent validation lane |
| tools | affected bundle checks, generated catalog checks, repo validator, and focused proof-infra tests through `mechanics/proof-infra/AGENTS.md#validation` |
| validation | `mechanics/proof-infra/parts/AGENTS.md#validation` and `mechanics/proof-infra/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `fixture-families/` | generic shared fixture-family support for bundle-local fixture contracts | `fixture-families/README.md` |
| `reportable-contracts/` | shared runner surface, scorer helper, and schemas consumed by bundle-local runner/report contracts | `reportable-contracts/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| fixture-family parent pressure | `mechanics/EVIDENCE_CLUSTERS.md` before any parent proposal |
| domain-owned fixture pressure | narrower active mechanic part that owns the operation |
| fixture placement as proof acceptance | bundle-local `EVAL.md`, `eval.yaml`, fixture contract, and reviewed report |
| former root fixture aliases | `PROVENANCE.md` and `legacy/` as historical compatibility vocabulary |
| root runner, scorer, or schema alias pressure | route-card-only root district plus active `reportable-contracts` paths |
| shared schema or scorer helper authority pressure | bundle-local interpretation surfaces and reviewed reports |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| reusable public-safe fixture family is needed across bundles | no narrower mechanic owns the fixture operation | `fixture-families/README.md` |
| reusable runner/scorer/schema support is needed for reportable proof | shared contract feeds bundle-local runner/report contracts | `reportable-contracts/README.md` |
| new proof-support family pressure | source surface, payload home, owner split, and validation lane are distinct from current parts | parent `PARTS.md` update plus evidence-cluster review |
