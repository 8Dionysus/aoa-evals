# 0069 Proof-object Part Owner-split Contract

## Status

Accepted.

## Context

`mechanics/proof-object/` is an evals-native parent for the operation around
source proof objects. Its active parts are support surfaces:

- `bundle-authoring` owns the starter `EVAL.md` scaffold.
- `bundle-contracts` owns schema-backed frontmatter and manifest validation.

Neither part is the source proof object. The source proof object remains
`evals/**/EVAL.md`, `evals/**/eval.yaml`, and bundle-local support artifacts.
Without explicit stronger-owner split, templates and schemas can accidentally
be read as doctrine, accepted proof meaning, bundle maturity, generated-reader
authority, or registry approval.

## Decision

Require both proof-object part README files to expose `## Stronger Owner Split`
and `## Stop-Lines`:

- `mechanics/proof-object/parts/bundle-authoring/README.md`
- `mechanics/proof-object/parts/bundle-contracts/README.md`

`bundle-authoring` remains scaffold support. `bundle-contracts` remains schema
validation support. Source proof bundle meaning stays under `evals/`, and
generated readers, reports, receipts, runtime candidates, sibling refs, quests,
and release surfaces stay weaker than bundle-local review.

## Consequences

- Future proof-object part edits must preserve the split between authoring
  support, schema validation support, and source bundle meaning.
- A template may shape a draft, but it must not become active proof meaning or
  doctrine.
- Schema acceptance may prove metadata shape, but it must not claim evidence
  acceptance, status maturity, publication, release readiness, or verdict truth.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k proof_object_part_owner_split
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q
```
