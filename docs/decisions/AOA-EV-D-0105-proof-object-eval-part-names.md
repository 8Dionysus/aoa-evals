# Proof-object Eval Part Names

- Decision ID: AOA-EV-D-0105

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-22
- Surface classes: proof topology, mechanic part
- Mechanic parents: proof-object
- Guard families: part and payload
- Posture: active rationale

## Context

`evals/` is now the source eval tree. The active proof-object support parts
still used the older `bundle-authoring` and `bundle-contracts` names after the
source tree moved away from root `bundles/`.

That made the agent-facing folder chain less convex:

`repo -> evals -> source eval package -> proof-object -> bundle-* support`

The support operation is still proof-object support, but the directory names
should let an agent understand the location without translating old root
vocabulary first.

## Decision

Rename the active proof-object parts:

- `mechanics/proof-object/parts/bundle-authoring/` becomes
  `mechanics/proof-object/parts/eval-authoring/`.
- `mechanics/proof-object/parts/bundle-contracts/` becomes
  `mechanics/proof-object/parts/eval-contracts/`.

Keep bundle vocabulary only where it describes existing eval-local artifacts,
historical compatibility, generated content, or legacy/provenance context.

## Rationale

The source proof objects now live in `evals/<claim-family>/<eval-name>/`.
The proof-object parts should therefore read as support for eval authoring and
eval contracts rather than as a leftover root `bundles/` district.

This preserves the authority split:

- `evals/**/EVAL.md` and `evals/**/eval.yaml` own source proof meaning.
- `eval-authoring` owns the starter scaffold.
- `eval-contracts` owns schema-backed metadata validation.
- generated readers, receipts, runtime candidates, and sibling refs remain
  derived or subordinate.

## Consequences

- Positive: the active mechanic part names now match the source eval tree.
- Positive: route cards and validator constants no longer expose stale
  `bundle-*` part names.
- Tradeoff: older decisions and changelog entries may still mention bundle
  vocabulary when they are describing the historical contract language.

## Boundaries

This decision does not rename every legitimate use of `bundle` across the
repository. `bundle-local`, generated bundle references, and legacy
compatibility language remain valid where they describe actual artifact
vocabulary rather than active directory topology.

This decision does not move source eval packages into mechanics.

## Validation

- `mechanics/proof-object/PARTS.md` names `eval-authoring` and
  `eval-contracts`.
- `scripts/validate_repo.py` checks the renamed part paths.
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python -m pytest -q tests/test_validate_repo.py -k proof_object`
