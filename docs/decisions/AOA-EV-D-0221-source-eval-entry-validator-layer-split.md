# Source Eval Entry Validator Layer Split

- Decision ID: AOA-EV-D-0221
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused source eval entry validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0184 correctly split source eval entry checks from physical
source-tree topology. The entry module still carried four separate concerns in
one file:

- operating-card route text for `EVAL_INDEX.md`, `EVAL_SELECTION.md`, and
  `evals/README.md`;
- starter table consistency, selection coverage, and starter manifest evidence;
- `ROADMAP.md` direction tokens, public-surface parity, and absence-note sync;
  and
- validate-repo orchestration for the starter and roadmap checks.

That kept the source eval entry lane smaller than the old root validator, but
still too broad for a validator boundary.

## Decision

Remove `scripts/validators/eval_entry_surfaces.py`.

Source eval entry validation is split into focused modules:

- `scripts/validators/eval_entry_cards.py` owns operating-card route tokens.
- `scripts/validators/eval_starter_surfaces.py` owns starter table,
  selection coverage, and starter evidence minimums.
- `scripts/validators/eval_roadmap_parity.py` owns roadmap direction and
  public-surface parity.
- `scripts/validators/eval_entry_routes.py` only wires starter and roadmap
  validators for `scripts/validate_repo.py`.

`root_topology.py` imports `eval_entry_cards.py` directly. `validate_repo.py`
loads starter names from `eval_starter_surfaces.py` and delegates entry-route
checks to `eval_entry_routes.py`.

## Rationale

Entry-card wording, starter evidence, and roadmap direction change for
different reasons. Keeping them in one module made the source eval entry lane
look like a catch-all for every public source-eval surface.

The split keeps each validator close to the source it protects and leaves
bundle-local `EVAL.md`, `eval.yaml`, schemas, runners, scorers, and reports as
the source of eval meaning.

## Consequences

- Positive: operating-card, starter, and roadmap failures now have distinct
  owner routes.
- Positive: `eval_entry_routes.py` is orchestration-only and does not define
  source eval meaning.
- Positive: `eval_entry_surfaces.py` is removed instead of preserved as a
  compatibility facade.
- Tradeoff: tests import the exact source eval entry submodule they exercise.

## Boundaries

This split does not move source eval meaning out of bundle-local files.

It does not make roadmap prose, generated catalogs, report indexes, release
artifacts, runtime guardrails, trace completeness, or grader outcomes source
truth.

It does not let `eval_bundle_common.py` or `eval_entry_routes.py` own validation
semantics beyond helper/orchestration roles.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/eval_bundle_common.py scripts/validators/eval_entry_cards.py scripts/validators/eval_starter_surfaces.py scripts/validators/eval_roadmap_parity.py scripts/validators/eval_entry_routes.py scripts/validators/eval_tree_topology.py scripts/validators/root_topology.py tests/test_eval_source_topology.py tests/test_roadmap_parity.py tests/test_validate_repo.py tests/validate_repo_fixtures.py`
- `python -m pytest -q tests/test_eval_source_topology.py tests/test_roadmap_parity.py tests/test_validate_repo.py -k "eval_source_entry or roadmap or eval_selection or starter"`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
