# Generated Parity Subvalidators

- Decision ID: AOA-EV-D-0183
- Status: Accepted
- Date: 2026-06-04
- Historical owner surface: `scripts/validators/generated_eval_readmodels.py`, `scripts/validators/generated_route_surfaces.py`
- Refined by: AOA-EV-D-0200

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/readout
- Mechanic parents: proof-object, comparison-spine, questbook, cross-parent
- Guard families: projection/generated, source/topology
- Posture: active rationale

## Context

AOA-EV-D-0132 moved generated read-model parity out of
`scripts/validate_repo.py`, but `scripts/validators/generated_parity.py` still
carried two different contracts:

- generated route/topology checks for `generated/README.md`,
  `generated/AGENTS.md`, root generated readers, docs reader links,
  decision-index notices, and part-local generated districts; and
- eval read-model projection parity for catalog/min-catalog, capsules,
  sections, and comparison spine.

Both are generated-lane checks, but they fail for different reasons and protect
different boundaries.

## Decision

Generated validation is split into focused modules:

- `scripts/validators/generated_route_surfaces.py` owns generated route and
  topology parity: reader route cards, root-reader existence, generator
  command exposure, decision-index generator notices, docs reader links, and
  part-local generated district presence.
- `scripts/validators/generated_eval_readmodels.py` owns eval read-model
  projection parity: catalog/min-catalog, capsule, section, and
  comparison-spine payloads derived from source eval records and builder
  output.

Historical imports from repo validation, tests, and evidence readouts are moved
directly to the focused modules. `scripts/validators/generated_parity.py` is
removed instead of preserved as a compatibility facade.

## Rationale

Generated validators should prove projection parity and routing freshness, not
become a second source of eval meaning or a catch-all generated bucket.

The route module can fail when generated reader navigation or generator
command exposure drifts. The read-model module can fail when JSON projection
payloads drift from source records. Keeping those checks apart makes the
failure route concrete and prevents the compatibility facade from accumulating
new behavior.

## Consequences

- Positive: the historical `generated_parity.py` surface is removed instead of
  kept as a compatibility adapter.
- Positive: route/topology drift and eval read-model projection drift have
  distinct owner modules.
- Positive: generated eval read models remain downstream of source eval
  records and builder output.
- Tradeoff: callers must import the focused validator that owns the behavior.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/build_catalog.py` remains the source builder for eval
  catalog, min-catalog, capsule, section, and comparison-spine read models.
- Changed: generated route/topology checks moved into
  `generated_route_surfaces.py`; eval read-model parity moved into
  `generated_eval_readmodels.py`; the historical
  `scripts/validators/generated_parity.py` module was removed.
- Further changed by: AOA-EV-D-0200 removes
  `scripts/validators/generated_eval_readmodels.py`; active eval read-model
  parity now routes through focused catalog, capsule, section, and
  comparison-spine validators plus a helper-only common context.
- Supersedes: the single-module owner shape described by AOA-EV-D-0132.
- Superseded by: AOA-EV-D-0200 for the generated eval read-model aggregate
  shape.

## Boundaries

This decision does not promote generated catalogs, capsules, sections,
comparison-spine readers, quest readers, report indexes, or decision indexes
into source truth.

It does not let generated route/topology validation own eval read-model
payload parity.

It does not let eval read-model parity own generated route cards, docs route
links, part-local generated districts, report verdicts, release packaging, or
runtime outcomes.

## Validation

- `python -m py_compile scripts/validators/generated_eval_readmodel_common.py scripts/validators/generated_eval_catalogs.py scripts/validators/generated_eval_capsules.py scripts/validators/generated_eval_sections.py scripts/validators/generated_eval_comparison_spine.py scripts/validators/generated_route_surfaces.py scripts/validators/evidence_readouts.py scripts/validators/root_topology.py scripts/validators/mechanics_root_districts.py scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py`
- `python -m pytest -q tests/test_generated_parity.py tests/test_build_catalog.py tests/test_downstream_feed_contracts.py tests/test_quest_and_reader_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
