# 0059 Comparison Spine Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/comparison-spine/parts/`

## Index Metadata

- Surface classes: mechanic part, validation guard
- Mechanic parents: comparison-spine
- Guard families: part and payload
- Posture: active guard rationale

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

## Current Applicability

As of 2026-05-24:

- Still valid: the four comparison-spine part README files remain the active
  part-level contract surfaces for overview, fixed-baseline, peer-compare, and
  longitudinal-window support.
- Changed: each required `## Stop-Lines` section now carries
  pressure-to-owner routes for overread, generated truth, broad growth,
  repo-global scoring, runtime health, sibling acceptance, promotion, and
  bundle-local contract pressure.
- Superseded by: none.

## Review Log

### 2026-05-24 - Part-level pressure routes

- Previous assumption: part README stop-lines could list overread limits and
  remain clear enough for future agents.
- New reality: part stop-lines now route the pressure to the next owner:
  source bundle review, mode-specific part reports, generated builder checks,
  release/report owner routes, `abyss-stack`, antifragility, sibling owners, or
  growth/progression review.
- Reason: comparison-spine parts are readout support, so the right next action
  is owner routing rather than a local refusal.
- Source surfaces updated:
  `mechanics/comparison-spine/parts/spine-overview/README.md`,
  `mechanics/comparison-spine/parts/fixed-baseline/README.md`,
  `mechanics/comparison-spine/parts/peer-compare/README.md`,
  `mechanics/comparison-spine/parts/longitudinal-window/README.md`,
  `mechanics/comparison-spine/PARTS.md`, and `scripts/validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k comparison_spine_part_readmes`,
  `python scripts/validate_repo.py`, `python scripts/build_catalog.py --check`,
  `python scripts/validate_semantic_agents.py`, and full pytest are the
  expected checks for this slice.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python -m pytest -q tests/test_validate_repo.py -k comparison_spine_part_readmes`
