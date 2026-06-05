# Source Eval Contract Validator Boundary

- Decision ID: AOA-EV-D-0151
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_contracts.py`, source eval proof-object contract guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Source eval bundle-core validation protects the authored proof object inside
`evals/<kind>/<name>/`. The guarded surfaces include bundle-local `EVAL.md`,
`eval.yaml`, evidence references, dependency refs, report contracts, fixtures,
runners, proof artifacts used to build catalog records, and command ownership
inside source `EVAL.md` files.

Before this split, `scripts/validate_repo.py` owned these checks beside public
source-entry topology, generated projection parity, mechanics route checks,
runtime-adjacent audit checks, and release-support gates. That kept the root
entrypoint large enough to hide owner boundaries.

## Decision

Source eval proof-object contract validation lives in
`scripts/validators/source_eval_contracts.py`.

The module originally owned:

- source eval record parsing from bundle-local `EVAL.md` and `eval.yaml`;
- frontmatter, manifest, required-section, and evidence contract checks;
- dependency drift and dependency target reachability checks for technique and
  skill refs;
- comparison surface, report schema, example report, actual report, fixture,
  runner, and proof artifact contract checks;
- source `EVAL.md` executable command ownership checks;
- source eval discovery and catalog-record source APIs used by generated
  builders and tests;
- source-bundle claim-boundary checks that prevent overclaiming longitudinal
  growth from local proof artifacts.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain to the module. `scripts/build_catalog.py` and tests import the focused
module directly instead of depending on root wrappers.

## Rationale

These checks are source/topology boundaries for authored proof objects. They
decide whether a bundle is internally coherent and whether generated projections
can be rebuilt from it without letting generated readers define source meaning.

They do not define public source-entry topology, generated catalog freshness,
report-index freshness, release-artifact freeze, runtime policy, trace grading,
or eval outcome quality. Keeping this boundary focused stops the root validator
from becoming a historical collection of every source-eval proof rule.

## Consequences

- Positive: `validate_repo.py` no longer exports source eval record, catalog,
  dependency, report, fixture, runner, or proof-artifact contract helpers.
- Positive: catalog builders and tests now depend on the source eval contract
  module as the source API for authored bundle records.
- Positive: validation inventories and the residual root-authored ledger name
  this module as a focused source-fast boundary.
- Follow-up: future runtime policy, trace/eval, release, and generated parity
  checks must stay in their own owner lanes instead of expanding this module.

## Review Log

### 2026-06-04 - Artifact contracts split

- Previous assumption: `source_eval_contracts.py` owned both source record
  contracts and bundle-local report, fixture, runner, and proof-artifact
  contracts.
- New reality: bundle-local artifact contract logic lives in
  `scripts/validators/source_eval_artifacts.py`; shared source-eval schema and
  payload helpers live in `scripts/validators/source_eval_common.py`.
- Reason: source record coherence and materialized support artifact shape are
  adjacent source-fast boundaries, but they should not remain one historical
  validator block.
- Source surfaces updated: `scripts/validators/source_eval_contracts.py`,
  `scripts/validators/source_eval_artifacts.py`,
  `scripts/validators/source_eval_common.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0159.

### 2026-06-04 - Evidence and review-policy split

- Previous assumption: `source_eval_contracts.py` owned manifest evidence path
  checks, status/portability posture, public safety review dates, and
  comparative-summary support-note rules.
- New reality: evidence and review-policy checks live in
  `scripts/validators/source_eval_evidence.py`.
- Reason: authored evidence sufficiency is adjacent to source proof-object
  structure, but it should not remain in the same historical validator block as
  manifest/frontmatter schema, command ownership, dependency reachability,
  relations, and catalog-record APIs.
- Source surfaces updated: `scripts/validators/source_eval_contracts.py`,
  `scripts/validators/source_eval_evidence.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0166.

### 2026-06-04 - Reference edge split

- Previous assumption: `source_eval_contracts.py` owned technique/skill
  dependency drift, dependency target reachability, cross-eval relation
  integrity, and claim-family tree location.
- New reality: dependency, relation, and tree-location checks live in
  `scripts/validators/source_eval_references.py`.
- Reason: reference edges are source-fast contracts, but sibling repo
  reachability and cross-bundle topology should not remain in the same
  historical validator block as proof-object parsing and schema validation.
- Source surfaces updated: `scripts/validators/source_eval_contracts.py`,
  `scripts/validators/source_eval_references.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0168.

### 2026-06-04 - Comparison-surface split

- Previous assumption: `source_eval_contracts.py` owned baseline-mode
  comparison surface keys, target eval refs, repo-relative comparison paths, and
  fixture/runner consistency checks.
- New reality: comparison-surface contract checks live in
  `scripts/validators/source_eval_comparison.py`.
- Reason: comparison route shape is an authored source manifest contract, but it
  should not remain in the same historical validator block as EVAL.md parsing,
  manifest/frontmatter schema, catalog-record APIs, evidence policy, references,
  and artifact contracts.
- Source surfaces updated: `scripts/validators/source_eval_contracts.py`,
  `scripts/validators/source_eval_comparison.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0173.

### 2026-06-04 - Authored record split

- Previous assumption: `source_eval_contracts.py` could keep EVAL.md parsing,
  manifest/frontmatter schema checks, mirrored fields, support artifact
  presence, command ownership, and projection-builder adapters together.
- New reality: authored record parsing and schema checks live in
  `scripts/validators/source_eval_records.py`; `source_eval_contracts.py`
  delegates record validation and remains the aggregate/projection adapter.
- Reason: authored source records and generated projection adapters answer
  different boundary questions and should not stay hidden in one facade.
- Source surfaces updated: `scripts/validators/source_eval_contracts.py`,
  `scripts/validators/source_eval_records.py`, validation inventories, and
  mechanics residual classification.
- Validation: see AOA-EV-D-0178.

### 2026-06-04 - Collection/projection adapter removal

- Previous assumption: `source_eval_contracts.py` could remain as the
  aggregate validation facade and projection adapter after focused source eval
  validators split out.
- New reality: bundle discovery and accepted catalog-record collection live in
  `scripts/validators/source_eval_collection.py`; catalog, capsule, and
  comparison-spine builders route through direct `eval_*_contract.py` modules.
- Reason: keeping projection adapters inside a validator facade kept an old
  compatibility bucket alive after the owner split was complete.
- Validation: see AOA-EV-D-0187.

## Current Applicability

As of 2026-06-04:

- Still valid: bundle-local source eval proof objects must satisfy their
  manifest, markdown, delegated evidence, delegated reference, and delegated
  artifact contracts before generated readers can project them, and executable
  validation commands must route to `evals/AGENTS.md` or the nearest route card.
- Changed: source eval bundle-core contract checks moved from
  `scripts/validate_repo.py` to `scripts/validators/source_eval_contracts.py`;
  report, fixture, runner, and proof-artifact checks later split across
  `scripts/validators/source_eval_report_artifacts.py`,
  `scripts/validators/source_eval_fixture_contracts.py`, and
  `scripts/validators/source_eval_runner_contracts.py`; evidence/review-policy checks
  later moved to `scripts/validators/source_eval_evidence.py`; dependency,
  relation, and tree-location checks later moved to
  `scripts/validators/source_eval_references.py`; comparison-surface checks
  later moved to `scripts/validators/source_eval_comparison.py`; authored
  record parsing, schema-envelope, heading, mirrored-field, support-artifact,
  and command-ownership checks later moved to
  `scripts/validators/source_eval_records.py`; bundle discovery and accepted
  catalog-record collection later moved to
  `scripts/validators/source_eval_collection.py`, while projection builders now
  route through direct `eval_*_contract.py` modules.
- Superseded by: AOA-EV-D-0159 for bundle-local artifact contracts; AOA-EV-D-0166 for evidence/review-policy contracts; AOA-EV-D-0168 for source eval reference contracts; AOA-EV-D-0173 for source eval comparison-surface contracts; AOA-EV-D-0178 for source eval authored-record contracts; AOA-EV-D-0187 for source eval collection and projection-adapter removal; AOA-EV-D-0199 for artifact aggregate removal.

## Boundaries

This decision does not let source eval contract validators own generated reader
freshness or generated parity.

It no longer makes `source_eval_contracts.py` the owner of bundle-local report,
fixture, runner, or proof-artifact contract logic; those owners are
`scripts/validators/source_eval_report_artifacts.py`,
`scripts/validators/source_eval_fixture_contracts.py`, and
`scripts/validators/source_eval_runner_contracts.py`.

It no longer makes `source_eval_contracts.py` the owner of source eval
evidence/review-policy logic; that owner is
`scripts/validators/source_eval_evidence.py`.

It no longer makes `source_eval_contracts.py` the owner of source eval
dependency, relation, or tree-location logic; that owner is
`scripts/validators/source_eval_references.py`.

It no longer makes `source_eval_contracts.py` the owner of source eval
comparison-surface logic; that owner is
`scripts/validators/source_eval_comparison.py`.

It no longer makes `source_eval_contracts.py` the owner of source eval authored
record parsing, schema-envelope, section/capsule heading, mirrored-field,
support-artifact, or command-ownership logic; that owner is
`scripts/validators/source_eval_records.py`.

It no longer keeps `source_eval_contracts.py` as a compatibility facade or
projection adapter; source bundle collection lives in
`scripts/validators/source_eval_collection.py`, and projection builders route
through direct `eval_*_contract.py` modules.

It does not own public source eval entry or tree topology; those remain in
`scripts/validators/eval_entry_cards.py`,
`scripts/validators/eval_starter_surfaces.py`,
`scripts/validators/eval_roadmap_parity.py`,
`scripts/validators/eval_entry_routes.py`, and
`scripts/validators/eval_tree_topology.py`.

It does not validate runtime guardrails, tool permissions, trace completeness,
grader outcomes, release packaging, or frozen artifact provenance.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/source_eval_collection.py scripts/build_catalog.py`
- `python -m pytest -q tests/test_build_catalog.py tests/test_downstream_feed_contracts.py tests/test_validate_repo.py tests/test_runtime_evidence_surfaces.py tests/test_eval_source_topology.py tests/test_report_schema_contracts.py mechanics/proof-object/parts/eval-authoring/tests/test_scaffold_eval_bundle.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
