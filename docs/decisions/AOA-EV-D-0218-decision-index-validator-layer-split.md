# Decision-index Validator Layer Split

- Decision ID: AOA-EV-D-0218
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused decision-index validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, generated/readout, root/topology
- Mechanic parents: cross-parent
- Guard families: decision index/read-model, source/topology, projection/generated
- Posture: active rationale

## Context

AOA-EV-D-0107 and AOA-EV-D-0114 made decision notes the source of rationale and
generated lookup indexes the cheap read model. The first validator shape kept
record parsing, index rendering, lane-surface contract checks, YAML contract
loading, and generated parity in one module.

That module was useful as the first extraction from `scripts/validate_repo.py`,
but it had become a compact aggregate. A source parser, a renderer, a lane
topology validator, and a generated-parity validator change for different
reasons.

## Decision

Remove `scripts/validators/docs_decisions.py`.

Decision-index validation is split into focused modules:

- `scripts/validators/decision_index_paths.py` owns decision-lane path constants.
- `scripts/validators/decision_records.py` owns decision note metadata parsing
  and canonical record collection.
- `scripts/validators/decision_index_renderer.py` owns generated index rendering
  from parsed records.
- `scripts/validators/decision_lane_surfaces.py` owns index-contract loading and
  unmodeled decision-lane surface checks.
- `scripts/validators/decision_index_surfaces.py` owns generated decision-index
  parity.

`scripts/generate_decision_indexes.py` imports record collection, contract
loading, and rendering directly. Root topology validation imports only the
generated-parity validator.

## Rationale

Generated indexes must not own decision rationale, and lane topology must not be
hidden inside the renderer. Splitting these surfaces keeps the decision lane
honest: source records remain authored truth, generated indexes remain
projections, and unmodeled lane files remain topology issues.

The split also removes another historical validator bucket without preserving a
compatibility facade.

## Consequences

- Positive: parsing, rendering, lane topology, and generated parity now have
  separate owners.
- Positive: `generate_decision_indexes.py` no longer imports a validator
  aggregate to render read models.
- Positive: root token helpers use decision-index path constants without
  importing decision parsing or parity validation.
- Tradeoff: the decision-index layer has more small helper imports.

## Boundaries

This split does not change decision note rationale, generated index content,
canonical decision ID policy, or the decision index contract.

It does not make generated indexes authoritative rationale.

It does not create release evidence, runtime acceptance, or goal completion.

## Validation

- `python -m py_compile scripts/validators/decision_index_paths.py scripts/validators/decision_records.py scripts/validators/decision_index_renderer.py scripts/validators/decision_lane_surfaces.py scripts/validators/decision_index_surfaces.py scripts/generate_decision_indexes.py scripts/validators/root_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python -m pytest -q tests/test_decision_indexes.py tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
