# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/experience/DIRECTION.md` for current operating direction, `mechanics/experience/PARTS.md` for active parts, and `mechanics/experience/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/experience/` and its nested part surfaces.

## Role

This package routes checkpointed Experience proof work on the eval side.

It does not own Experience center law, live runtime, office installation,
operator certification, release approval, memory truth, routing behavior,
playbook choreography, ToS-authored meaning, or owner-local adoption.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/EVIDENCE_CLUSTERS.md`
6. `mechanics/README.md`
7. `mechanics/experience/README.md`
8. `mechanics/experience/PARTS.md`
9. `mechanics/experience/PROVENANCE.md` when old root path or wave naming is involved
10. the target part `README.md`

## Boundaries

- Keep source proof bundles under `evals/`.
- Keep verdict support surfaces part-local when they have schema/example/test
  contracts.
- Keep adoption, certification, office, governance, runtime, KAG, ToS, and
  release language bounded to proof interpretation.
- Do not create new Experience parts from one document or one example.
- Do not turn old wave names into active topology.
- Do not treat generated readers as source truth.

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
