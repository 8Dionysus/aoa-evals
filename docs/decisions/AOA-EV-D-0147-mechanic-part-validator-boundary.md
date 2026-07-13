# Mechanic Part Validator Boundary

- Decision ID: AOA-EV-D-0147
- Status: Accepted
- Date: 2026-06-04
- Owner surface: mechanic part contract guard family
- Refined by: AOA-EV-D-0175, AOA-EV-D-0188, AOA-EV-D-0195, AOA-EV-D-0204

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

Mechanic part contracts protect part README shape, source-surface refs, payload
inventory, parent `PARTS.md` synchronization, lower parts index route posture,
and validation command reachability.

Before this split, those checks lived inside `scripts/validate_repo.py` beside
repo-wide orchestration, generated projection checks, legacy bridge checks, and
root topology checks. That made the root validator remember part-local contract
law and decision-token matrices directly.

## Decision

Mechanic part aggregate validation routes through
`scripts/validators/mechanic_parts.py`.

The focused modules own:

- `mechanic_part_contracts.py`: parent `PARTS.md` contract tokens, part README
  required-section checks, part/index route heading roles, and aggregate
  part-contract traversal;
- `mechanic_part_payload_inventory.py`: allowed payload classes, unexpected
  part-root entries, empty payload dirs, README payload routing, thin-part
  posture, and payload-inventory decision routing;
- `mechanic_part_source_surfaces.py`: Source Surfaces path-like refs,
  repo-relative reachability, placeholder/nonlocal allowances, and
  source-surface decision routing;
- `mechanic_parts_index_sync.py`: parent `PARTS.md` synchronization;
- `mechanic_part_validation_commands.py`: part validation command
  reachability/ownership; and
- `mechanic_parts.py`: compatibility aliases and aggregate
  `validate_mechanic_part_surfaces`.

`scripts/validate_repo.py` delegates to the module through
`validate_mechanic_part_surfaces`. Tests for moved behavior import
`validators/mechanic_parts.py` directly instead of using root compatibility
wrappers.

## Rationale

Mechanic part contracts are mechanic-local boundaries. They decide whether a
part has a readable route, enough source refs, explicit payload ownership, and
reachable validation evidence.

They do not define source eval meaning, generated read-model parity, release
artifact freeze, runtime policy, trace/eval grading, or sibling truth. Keeping
them in a focused module prevents the root validator from accumulating one more
historical gate family.

## Consequences

- Positive: `validate_repo.py` no longer exports mechanic part contract,
  PARTS sync, index-role, or validation command wrappers.
- Positive: part-contract tests now call the owning module directly.
- Positive: script and validator inventories name mechanic part contracts as a
  distinct source-fast surface.
- Follow-up: remaining parent direction, legacy/provenance, and allowlist
  mechanics checks should split only when their owner boundary is equally
  coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parts must keep contract, payload, source-ref, index,
  and validation-route evidence explicit.
- Changed: mechanic part checks moved from `scripts/validate_repo.py` into
  focused part validators. The later `mechanic_parts.py` aggregate facade is
  removed; the later `mechanic_part_validation.py` aggregate is also removed;
  mechanics route orchestration now calls focused part validators directly.
- Superseded by: AOA-EV-D-0165 for the validation-route split and
  AOA-EV-D-0175 for the README/payload/source-surface sub-boundary split;
  AOA-EV-D-0188 for aggregate facade removal; AOA-EV-D-0195 for the remaining
  validation aggregate removal.

## Review Log

### 2026-06-04 - Validation route split

- Previous assumption: `mechanic_parts.py` should carry README contracts,
  payload inventory, source refs, index synchronization, and validation-command
  reachability as one part contract validator.
- New reality: README/payload/source-ref/index-role checks remain in
  `mechanic_parts.py`; PARTS index synchronization and validation-command
  reachability/ownership moved into
  `scripts/validators/mechanic_part_validation.py`, which is later removed by
  AOA-EV-D-0195.
- Reason: executable validation route evidence is distinct from part contract
  description and payload/source-surface boundaries.
- Source surfaces updated: `scripts/validators/mechanic_parts.py`,
  `scripts/validators/mechanic_part_validation.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - README, payload, and source-surface split

- Previous assumption: `mechanic_parts.py` should remain the concrete owner for
  README contracts, payload inventory, source refs, index-role checks, and
  aggregate validation.
- New reality: `mechanic_parts.py` is a compatibility facade; README/index
  checks live in `mechanic_part_contracts.py`, payload inventory checks live in
  `mechanic_part_payload_inventory.py`, and source-surface checks live in
  `mechanic_part_source_surfaces.py`.
- Reason: README shape, payload inventory, source references, and executable
  validation routes are adjacent part-local boundaries, but not one validator
  organ.
- Source surfaces updated: `scripts/validators/mechanic_parts.py`,
  `scripts/validators/mechanic_part_contracts.py`,
  `scripts/validators/mechanic_part_payload_inventory.py`,
  `scripts/validators/mechanic_part_source_surfaces.py`,
  `scripts/validators/mechanic_part_validation.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Aggregate facade removal

- Previous assumption: `mechanic_parts.py` could remain as aggregate
  compatibility after README, payload, source-surface, and validation-command
  checks split out.
- New reality: `mechanic_parts.py` is removed. `mechanics_routes.py`,
  root-topology checks, and tests import focused part validators directly.
- Reason: the facade carried only aliases and aggregate glue after the owner
  split was complete.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Validation aggregate removal

- Previous assumption: `mechanic_part_validation.py` could own both parent
  PARTS index synchronization and part validation-command reachability.
- New reality: index synchronization lives in `mechanic_parts_index_sync.py`;
  command reachability lives in `mechanic_part_validation_commands.py`; shared
  parsing lives in `mechanic_part_validation_common.py`.
- Reason: parent route-map parity and executable part validation evidence are
  adjacent but distinct source-fast boundaries.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Contract aggregate removal

- Previous assumption: `mechanic_part_contracts.py` could remain as the
  concrete owner for parent `PARTS.md` contract tokens, route role headings,
  README traversal, and shared constants.
- New reality: `mechanic_part_contracts.py` is removed. Shared constants route
  through `mechanic_part_contract_common.py`; parent `PARTS.md` contract tokens
  route through `mechanic_part_contract_index.py`; route H1 roles route through
  `mechanic_part_role_headings.py`; part README traversal routes through
  `mechanic_part_readme_contract.py`.
- Reason: contract-index checks, role-heading checks, README traversal, payload
  inventory, source refs, and validation commands are adjacent but distinct
  part-local boundaries.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not let part validators define part payload meaning. Payload
meaning stays with the owning mechanic part and its source surfaces.

It does not turn part validation commands into release artifact freeze or
runtime policy enforcement.

PARTS index synchronization routes through
`scripts/validators/mechanic_parts_index_sync.py`; validation-command
reachability routes through
`scripts/validators/mechanic_part_validation_commands.py`; shared route parsing
routes through `scripts/validators/mechanic_part_validation_common.py`.
Parent `PARTS.md` contract tokens route through
`scripts/validators/mechanic_part_contract_index.py`; route headings route
through `scripts/validators/mechanic_part_role_headings.py`; README traversal
routes through `scripts/validators/mechanic_part_readme_contract.py`; payload
inventory and source-ref checks route through their focused part validator
modules. No aggregate `mechanic_parts.py`, `mechanic_part_validation.py`, or
`mechanic_part_contracts.py` compatibility module remains.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
