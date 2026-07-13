# Generated Eval Read-model Aggregate Removal

- Decision ID: AOA-EV-D-0200
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused generated eval catalog, capsule, section, and comparison-spine parity validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/readout
- Mechanic parents: proof-object, comparison-spine, questbook, cross-parent
- Guard families: projection/generated
- Posture: active rationale

## Context

AOA-EV-D-0183 removed the broad `generated_parity.py` facade and separated
generated route/topology checks from eval read-model projection checks.

The remaining `scripts/validators/generated_eval_readmodels.py` module still
mixed four generated payload families:

- catalog and min-catalog projection parity;
- capsule projection parity and catalog alignment;
- section projection parity and catalog field alignment; and
- comparison-spine projection parity and catalog alignment.

Those payloads are all generated from source eval records and builder output,
but they fail through different contracts and should not share one aggregate
owner.

## Decision

`scripts/validators/generated_eval_readmodels.py` is removed.

Generated eval read-model validation now routes through focused modules:

- `generated_eval_catalogs.py` owns catalog and min-catalog projection parity.
- `generated_eval_capsules.py` owns capsule projection parity and catalog
  alignment.
- `generated_eval_sections.py` owns section projection parity and catalog field
  alignment.
- `generated_eval_comparison_spine.py` owns comparison-spine projection parity
  and catalog alignment.
- `generated_eval_readmodel_common.py` is helper-only shared context, names,
  versions, source-of-truth constants, and min-catalog metadata helpers.

`evidence_readouts.py` remains the readout orchestrator and calls the focused
validators directly with the injected builder context.

## Rationale

Generated validators should prove that read models are exact projections of
source and builder output. They should not become a historical bucket where
every generated payload adds another branch.

Catalog, capsule, section, and comparison-spine parity have different repair
routes and different contract checks. Splitting them keeps failure messages
close to the artifact that drifted while preserving the shared context boundary
that prevents validators from reconstructing source meaning.

## Consequences

- Positive: no generated eval read-model aggregate validator remains.
- Positive: generated catalog, capsule, section, and comparison-spine drift now
  route to separate owner modules.
- Positive: common generated read-model helpers have no parity-rule authority.
- Tradeoff: `evidence_readouts.py` imports the focused parity validators
  directly because it orchestrates readout validation.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/build_catalog.py` remains the source builder for eval
  catalog, min-catalog, capsule, section, and comparison-spine read models.
- Changed: eval read-model parity no longer lives in
  `generated_eval_readmodels.py`; it is split across focused generated eval
  parity validators.
- Supersedes: the remaining generated eval read-model aggregate shape left by
  AOA-EV-D-0183.

## Boundaries

This decision does not promote generated catalogs, capsules, sections,
comparison-spine readers, quest readers, report indexes, or decision indexes
into source truth.

It does not let generated eval parity validators own generated route cards,
docs route links, part-local generated districts, report verdicts, release
packaging, runtime outcomes, or source eval meaning.

It does not create a replacement generated eval read-model aggregate under
another name.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
