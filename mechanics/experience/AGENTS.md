# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/experience/DIRECTION.md` for current operating direction, `mechanics/experience/PARTS.md` for active parts, and `mechanics/experience/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/experience/` and its nested part surfaces.

## Role

This package routes checkpointed Experience proof work on the eval side.

It maps Experience proof pressure to protocol integrity, certification gate,
adoption federation, governance/runtime boundary, office release train,
bundle-local review, or stronger-owner handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | Experience proof work route on the eval side |
| input | protocol-integrity evidence, certification-gate evidence, adoption pressure, governance/runtime boundary evidence, office release-train evidence, or Experience owner question |
| output | active part route, source bundle review, generated reader check, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded Experience proof support; stronger owners keep center law, live runtime, office installation, certification, release approval, memory, routing, playbooks, ToS meaning, and owner-local adoption |
| next route | `mechanics/experience/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, affected source proof bundle, and source owner route |
| tools | part-local pytest, catalog builder, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `mechanics/EVIDENCE_CLUSTERS.md`
6. `mechanics/README.md`
7. `mechanics/experience/README.md`
8. `mechanics/experience/PARTS.md`
9. `mechanics/experience/PROVENANCE.md` when old root path or wave naming is involved
10. the target part `README.md`

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep verdict support surfaces part-local when they have schema/example/test
  contracts.
- Keep adoption, certification, office, governance, runtime, KAG, ToS, and
  release language bounded to proof interpretation.
- Create Experience parts from a recurring proof operation with validator
  coverage.
- Keep old wave names as provenance or compatibility vocabulary.
- Check generated readers from source surfaces and builders.

## Validation

Run the part-local tests for the touched part and then:

```bash
python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py
python -m pytest -q mechanics/experience/parts/certification-gate/tests
python -m pytest -q mechanics/experience/parts/adoption-federation/tests
python -m pytest -q mechanics/experience/parts/governance-runtime-boundary/tests
python -m pytest -q mechanics/experience/parts/office-release-train/tests
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which Experience part changed, which source surfaces it routes, whether
`PROVENANCE.md` was needed, which validators ran, which stronger-owner
boundary stayed intact, and which Experience pressure remains deferred.
