# Source Eval Entry And Tree Subvalidators

- Decision ID: AOA-EV-D-0184
- Status: Accepted
- Date: 2026-06-04
- Historical owner surface: `scripts/validators/eval_entry_surfaces.py`, `scripts/validators/eval_tree_topology.py`
- Refined by: AOA-EV-D-0221

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0150 moved source eval entry and tree checks out of
`scripts/validate_repo.py`, but `scripts/validators/eval_bundles.py` still
mixed separate boundaries:

- public entry and direction surfaces: `EVAL_INDEX.md`,
  `EVAL_SELECTION.md`, `ROADMAP.md`, starter bundle evidence, and public
  surface parity; and
- physical source-tree topology: `evals/README.md`, `evals/AGENTS.md`,
  required claim-family directories, eval manifest path shape, `EVAL.md`
  pairing, and the source-tree topology decision route.

Those checks both live in source-fast, but their failure routes are different.

## Decision

Source eval validation is split into focused modules:

- `scripts/validators/eval_entry_surfaces.py` owns source eval entry and
  direction checks: operating cards, starter table consistency,
  `EVAL_SELECTION.md` coverage, starter bundle evidence minimums, roadmap
  direction tokens, public-surface parity, and absence-note synchronization.
- `scripts/validators/eval_tree_topology.py` owns source eval tree topology:
  source-tree route tokens, required claim-family directories, eval manifest
  path shape, `EVAL.md` pairing, manifest topology fields, source-tree
  topology decision routing, and `evals/AGENTS.md` command exposure.
- `scripts/validators/eval_bundle_common.py` owns only shared constants,
  YAML loading, markdown command parsing, table/bullet extraction, and bundle
  discovery helpers.

`scripts/validators/eval_bundles.py` is removed after direct callers move to
the focused modules.

## Rationale

Public entry surfaces route agents toward source eval bundles. Physical
source-tree topology proves that bundle homes and manifest paths are shaped
correctly. Keeping both in one module recreated a broad source-eval bucket and
made future growth ambiguous.

The helper module has no validation authority. It exists so the two owner
modules can share parsing and discovery without smuggling meaning into a common
gate.

## Consequences

- Positive: source eval entry/roadmap checks and source-tree topology checks
  now have distinct failure routes.
- Positive: `eval_bundles.py` is removed instead of preserved as a historical
  compatibility facade.
- Positive: `scripts/validate_repo.py`, root topology validation, and tests
  import the focused owners directly.
- Tradeoff: tests that previously imported `eval_bundles.py` now name the
  specific source eval boundary they exercise.

## Current Applicability

As of 2026-06-04:

- Still valid: public source eval entry surfaces must route to bundle-local
  proof objects and keep starter/readout claims synchronized.
- Changed: source eval entry/roadmap checks moved into
  `eval_entry_surfaces.py`; source-tree topology checks moved into
  `eval_tree_topology.py`; shared helpers moved into `eval_bundle_common.py`.
- Refined on 2026-06-05: AOA-EV-D-0221 removed
  `eval_entry_surfaces.py` after splitting entry-card checks,
  starter/index/selection/evidence checks, roadmap parity, and validate-repo
  orchestration into separate modules. Source-tree topology remains in
  `eval_tree_topology.py`.
- Supersedes: the single-module owner shape described by AOA-EV-D-0150.
- Superseded by: AOA-EV-D-0221 for the entry/roadmap aggregate shape.

## Boundaries

This decision does not let source-entry validators define source eval meaning.
Bundle-local `EVAL.md`, `eval.yaml`, schemas, runners, scorers, and reports keep
their own authority.

It does not make roadmap prose, generated catalogs, report indexes, release
artifacts, runtime guardrails, trace completeness, or grader outcomes source
truth.

It does not let `eval_bundle_common.py` own validation semantics.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/eval_bundle_common.py scripts/validators/eval_entry_cards.py scripts/validators/eval_starter_surfaces.py scripts/validators/eval_roadmap_parity.py scripts/validators/eval_entry_routes.py scripts/validators/eval_tree_topology.py scripts/validators/root_topology.py scripts/validators/mechanics_root_districts.py scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py`
- `python -m pytest -q tests/test_eval_source_topology.py tests/test_roadmap_parity.py tests/test_validate_repo.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
