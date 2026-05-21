# 0059 Comparison Spine Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/comparison-spine/parts/`

## Context

`comparison-spine` owns the route:

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

Decisions `0029` and `0040` moved comparison dossiers and comparison-owned
fixture families into part-local homes. The four part README files still needed
local contracts. Without part-level contracts, fixed-baseline, peer-compare,
longitudinal-window, and overview surfaces can be overread as broad growth,
repo-global scoring, generated truth, or bundle promotion.

## Decision

Make the four comparison-spine part README files carry explicit part-level
contracts:

- `mechanics/comparison-spine/parts/spine-overview/README.md`;
- `mechanics/comparison-spine/parts/fixed-baseline/README.md`;
- `mechanics/comparison-spine/parts/peer-compare/README.md`;
- `mechanics/comparison-spine/parts/longitudinal-window/README.md`.

Each part must expose inputs, outputs, `stronger owner split`, stop-lines, and
validation.

## Rationale

The active parent is `comparison-spine`. Overview, fixed-baseline,
peer-compare, and longitudinal-window are comparison modes or read-order parts,
not independent parent mechanics and not proof authority.

Source proof bundles own claim meaning, comparison surface, verdict posture,
and blind spots. Generated comparison readers remain derived. Part-local
fixtures and dossiers support bounded comparison review, but they do not create
broad growth proof.

## Consequences

- Positive: future comparison work starts from local mode contracts.
- Positive: `python scripts/validate_repo.py` now catches drift in the four
  comparison-spine part README files.
- Positive: fixed-baseline, peer-compare, and longitudinal-window stay visibly
  distinct.
- Tradeoff: comparison wording is stricter where a polished readout might tempt
  a broader claim.

## Boundaries

This decision does not move comparison bundles, promote bundle status, edit
generated comparison readers as source truth, create repo-global scores, accept
runtime health, transfer sibling authority, or claim broad capability growth.

It does not move bundle-local fixture, runner, report, or schema contracts into
comparison-spine parts.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python -m pytest -q tests/test_validate_repo.py -k comparison_spine_part_readmes`
