# Source Eval Entry Validator Boundary

- Decision ID: AOA-EV-D-0150
- Status: Accepted
- Date: 2026-06-04
- Historical owner surface: `scripts/validators/eval_bundles.py`, source eval entry/topology guard family
- Refined by: AOA-EV-D-0184, AOA-EV-D-0221

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Source eval entry validation protects the route from public eval readout
surfaces into bundle-local proof objects. The guarded surfaces include
`EVAL_INDEX.md`, `EVAL_SELECTION.md`, `ROADMAP.md`, `evals/README.md`,
`evals/AGENTS.md`, and bundle-local `EVAL.md` / `eval.yaml` topology.

Before this split, `scripts/validate_repo.py` owned the starter table parser,
selection chooser checks, starter-bundle evidence contract, roadmap parity,
source-tree topology route checks, and source-entry operating-card checks beside
many unrelated proof, mechanics, generated, and release-adjacent validators.

## Decision

Source eval entry and bundle-topology validation lives in
`scripts/validators/eval_bundles.py`.

The module owns:

- starter eval names loaded from `EVAL_INDEX.md`;
- `EVAL_INDEX.md` duplicate and missing-bundle checks;
- `EVAL_SELECTION.md` chooser identity and starter coverage checks;
- starter-bundle example report and manifest evidence checks;
- `ROADMAP.md` public-surface parity with source eval bundles and starter rows;
- `evals/README.md`, `evals/AGENTS.md`, and source-tree topology route checks;
- source-entry operating-card checks for `EVAL_INDEX.md`, `EVAL_SELECTION.md`,
  and `evals/README.md`.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain to the module. Tests for moved behavior import
`validators/eval_bundles.py` directly instead of using root wrappers.

## Rationale

These checks are source/topology boundaries. They decide whether public entry
surfaces route to source eval packages without letting indexes, chooser docs, or
roadmap prose outrank bundle-local proof meaning.

They do not define generated catalog parity, report-index freshness,
release-artifact freeze, runtime policy, trace grading, or actual eval outcome.
Keeping this boundary focused prevents the root validator from becoming a
history pile for every source-eval public-surface wave.

## Consequences

- Positive: `validate_repo.py` no longer exports source eval entry/topology
  wrappers for starter names, selection, roadmap parity, or source-tree route
  checks.
- Positive: source eval topology, roadmap parity, selection, and fixture tests
  now route through `validators/eval_bundles.py`.
- Positive: validation inventories name source eval entry/topology as a focused
  source-fast boundary.
- Follow-up: remaining source eval bundle-core checks can split later only when
  the new module boundary is not expanded into generated, runtime, or outcome
  ownership.

## Current Applicability

As of 2026-06-04:

- Still valid: public source eval entry surfaces must route to bundle-local
  proof objects and keep starter/readout claims synchronized.
- Changed: source eval entry and source-tree topology checks moved from
  `scripts/validate_repo.py` to `scripts/validators/eval_bundles.py`.
- Refined on 2026-06-04: AOA-EV-D-0184 removed
  `scripts/validators/eval_bundles.py` after moving entry/roadmap checks to
  `scripts/validators/eval_entry_surfaces.py`, tree-topology checks to
  `scripts/validators/eval_tree_topology.py`, and shared helpers to
  `scripts/validators/eval_bundle_common.py`.
- Refined on 2026-06-05: AOA-EV-D-0221 removed
  `scripts/validators/eval_entry_surfaces.py` after moving entry-card checks to
  `scripts/validators/eval_entry_cards.py`, starter/index checks to
  `scripts/validators/eval_starter_surfaces.py`, roadmap parity checks to
  `scripts/validators/eval_roadmap_parity.py`, and validate-repo wiring to
  `scripts/validators/eval_entry_routes.py`.
- Superseded by: AOA-EV-D-0184 and AOA-EV-D-0221 for the single-module owner
  shapes.

## Boundaries

This decision does not let source-entry validators define source eval meaning.
Bundle-local `EVAL.md`, `eval.yaml`, schemas, runners, scorers, and reports keep
their own authority.

It does not make generated catalogs or report indexes source truth.

It does not validate runtime guardrails, tool permissions, trace completeness,
or grader outcomes.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
