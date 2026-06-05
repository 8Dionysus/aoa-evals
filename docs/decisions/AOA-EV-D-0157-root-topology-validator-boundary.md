# Root Topology Validator Boundary

- Decision ID: AOA-EV-D-0157
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_topology.py`, root source/topology validation orchestration

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After the evidence/readout split, `scripts/validate_repo.py` still carried the
root source/topology domain: root authority checks, guidance route checks, docs
topology, validation topology, decision-index parity, generated route posture,
route-card-only districts, route residue families, quest route checks, mechanics
route-domain validation, and report-index route checks.

Those checks describe the authored source/topology surface of the repo. They are
not argument parsing, eval scope selection, source record discovery, or CLI
output formatting.

## Decision

Root source/topology orchestration lives in
`scripts/validators/root_topology.py`.

The module owns:

- aggregation order for root authority, root guidance, docs topology,
  validation topology, decision-index, generated route, route-card, route
  residue, quest route, mechanics route-domain, and report-index route checks;
- root route-card context construction;
- root route-residue context construction;
- Questbook route context construction from `root_route_tokens.py` and mechanic
  provenance bridge tokens;
- conversion of focused validator issue objects into the root
  `ValidationIssue` shape.

`scripts/validate_repo.py` remains the CLI entrypoint and calls
`root_topology.validate_root_topology_surfaces(repo_root)` for the repo root
source/topology pass.

## Rationale

The root topology domain is the source-fast boundary for authored root surfaces.
Keeping it inside the CLI preserved the old mega-validator shape: every focused
source/topology rule looked like a method of `validate_repo.py`.

Moving the aggregation to a named module lets the command stay a scope runner
while root topology remains explicit and separate from source eval contracts,
generated/readout freshness, runtime policy, release evidence, and mechanic
payload truth.

## Consequences

- Positive: `scripts/validate_repo.py` no longer carries root source/topology
  aggregation or route-card, route-residue, and Questbook context factories.
- Positive: route residue and Questbook tests import the root topology owner
  directly.
- Positive: root topology can grow by calling focused validators without turning
  the CLI back into a historical rule bucket.
- Tradeoff: this module imports many focused source/topology validators; new
  rule meaning must stay in focused modules or owning source surfaces.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command and eval scope selector.
- Changed: root source/topology orchestration and root route contexts moved to
  `scripts/validators/root_topology.py`.
- Superseded by: none.

## Boundaries

This decision does not let `root_topology.py` define source eval contracts,
generated source meaning, runtime policy acceptance, trace/eval grading, live
receipt publication truth, release artifact identity, sibling compatibility
truth, or mechanic payload meaning.

It is an orchestration boundary for root source/topology validators, not a new
generated validator or release gate.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/root_topology.py tests/test_generated_route_residue.py tests/test_route_residue.py tests/test_quest_and_reader_surfaces.py`
- `python -m pytest -q tests/test_route_residue.py tests/test_generated_route_residue.py tests/test_quest_and_reader_surfaces.py tests/test_root_surface_roles.py tests/test_validation_topology.py`
