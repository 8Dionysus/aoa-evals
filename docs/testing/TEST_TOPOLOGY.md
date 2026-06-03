# Test Topology

Tests in `aoa-evals` protect proof boundaries. They should answer which
boundary is protected, which owner surface is authoritative, where the test
lives, which lane covers it, and where a failure routes next.

The machine inventory is [`test_inventory.json`](test_inventory.json). Update
it when adding, deleting, renaming, splitting, folding, or changing the home of
a test file.

## Route Shape

Use the compact route shape:

```text
family -> protects -> owner surface -> home scope -> coverage authority -> focused target -> failure route
```

Test files are not command authority. Lane command sequences live in
[`docs/validation/validation_lanes.json`](../validation/validation_lanes.json).

## Home Scopes

| Home Scope | Homes | Protects | Coverage Authority | Failure Route |
| --- | --- | --- | --- | --- |
| `root` | `tests/` | Repo-wide eval contracts, generated readers, route cards, validators, release reports, and topology authority. | `validation_lanes.release` and focused pytest targets | Fix the root-owned source or validator before widening to release. |
| `mechanic-part` | `mechanics/<parent>/parts/<part>/tests/` | One mechanic part payload, generated companion, report, fixture, or local builder. | `validation_lanes.mechanics_part_local` | Fix the owning part source, builder, validator, or report before changing root tests. |
| `agent-lane` | `.agents/*/tests/` when present | Maintained agent-lane scenarios or local agent support contracts. | `validation_lanes.release` or `validation_lanes.advisory` | Fix the agent-lane route and scenario registry before treating release as clean. |

## Families

| Family | Protects | Owner Surface |
| --- | --- | --- |
| `source/proof-contract` | Source eval bundle schema, proof posture, report artifacts, and bounded claims. | `evals/**/EVAL.md`, `evals/**/eval.yaml`, `scripts/validate_repo.py` |
| `generated/read-model` | Generated catalogs, report indexes, comparison spine, and projection parity. | builders and `scripts/validators/generated_parity.py` |
| `route-card/topology` | AGENTS mesh, docs topology, root route cards, route residue, and semantic snippets. | nearest `AGENTS.md`, docs topology, and validator modules |
| `mechanics/package-topology` | Mechanic parent, part, legacy, provenance, payload, and validation route contracts. | `mechanics/<parent>/` and part READMEs |
| `mechanics/part-local` | One mechanic part report, registry, fixture, script, or generated surface. | `mechanics/<parent>/parts/<part>/` |
| `boundary/sibling` | Explicit compatibility snapshots, latest sibling canary, phase-alpha matrix, and sibling-owned truth boundaries. | boundary-bridge and release-support mechanics |
| `trace/eval-scenario` | Tool trajectory, trace/outcome, approval, memory, and witness fixtures. | proof-infra fixture families and bounded eval bundles |
| `audit/release-report` | Readiness audit, strategic closeout, PR handoff, receipts, and verification honesty reports. | release-support, publication-receipts, proof-loop, and audit parts |
| `validation-topology/authority` | Lane manifest, validator inventory, script inventory, and test inventory. | `docs/validation/*`, `docs/testing/*`, and loader tests |

## Lane Rules

- Inventory entries must name a `focused_target`, not duplicate a full release
  command sequence.
- Root tests should split by owner surface as `test_validate_repo.py` shrinks.
- Mechanic-part tests should stay part-local unless the checked invariant spans
  the repository.
- Trace/eval, safety, memory, handoff, and fault-injection suites should start
  from curated bounded fixtures and then feed release/nightly only when stable.
- Release command order belongs in the lane manifest; tests may assert coverage
  but must not become a second command store.
