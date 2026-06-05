# Source Eval Record Validator Boundary

- Decision ID: AOA-EV-D-0178
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_records.py`, `evals/AGENTS.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: proof-object, proof-infra, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After artifact, evidence, reference, and comparison checks moved into focused
modules, `scripts/validators/source_eval_contracts.py` still carried authored
record parsing and schema checks: `EvalBundleRecord`, EVAL.md frontmatter
parsing, section extraction, frontmatter and manifest schema envelopes, capsule
source section checks, mirrored manifest fields, support artifact presence, and
source EVAL.md command ownership.

That left the aggregate validator as both a record parser and projection/build
adapter. Those are separate boundaries.

## Decision

Source eval authored-record validation lives in
`scripts/validators/source_eval_records.py`.

The module owns:

- `EvalBundleRecord`;
- source EVAL.md frontmatter parsing;
- EVAL.md section extraction and section/capsule-source heading contracts;
- frontmatter and manifest schema-envelope checks;
- manifest/frontmatter mirrored-field checks;
- support artifact presence under `examples/`, `checks/`, or `notes/`; and
- source EVAL.md command-ownership checks.

`scripts/validators/source_eval_collection.py` later becomes the collection
owner for bundle discovery and accepted catalog records. Catalog, capsule, and
comparison-spine projection helpers route through direct `eval_*_contract.py`
modules.

## Rationale

Authored source records define the proof object input. Projection builders
derive read models from accepted records. Evidence, references, comparison
surfaces, and artifact contracts answer further focused questions.

Keeping record parsing inside the aggregate facade made the facade look like the
natural owner of all source-eval behavior. Splitting record contracts keeps
authored source truth visible without moving generated freshness or runtime
outcomes into source validation.

## Consequences

- Positive: authored record parsing/schema checks have a focused validator,
  inventory row, mechanics ledger row, and decision rationale.
- Changed later: the aggregate facade was removed; source eval collection now
  routes through `source_eval_collection.py` without compatibility aliases.

## Current Applicability

As of 2026-06-04:

- Still valid: every source eval bundle must expose schema-backed EVAL.md and
  eval.yaml records with valid headings, mirrored fields, and support artifacts.
- Changed: authored record parsing, schema-envelope, heading, mirrored-field,
  support-artifact, and command-ownership checks moved out of
  `source_eval_contracts.py` and into `source_eval_records.py`.
- Superseded by: AOA-EV-D-0187 for source eval collection and
  projection-adapter removal.

## Boundaries

This decision does not let `source_eval_records.py` own comparison-surface
meaning, evidence/review policy, dependency refs, artifact report/fixture/runner
contracts, generated freshness, release packaging, runtime outcomes, score
interpretation, or public entry routing.

Those route to focused source-eval validators, generated validators, release
validators, runtime/eval surfaces, or stronger owner surfaces.

## Validation

- `python -m py_compile scripts/validators/source_eval_collection.py scripts/validators/source_eval_records.py`
- `python -m pytest -q tests/test_build_catalog.py tests/test_validate_repo.py tests/test_eval_source_topology.py tests/test_downstream_feed_contracts.py mechanics/proof-object/parts/eval-authoring/tests/test_scaffold_eval_bundle.py`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
