# Comparison Spine / Spine Overview Part

## Role

This part owns the cross-mode comparison-spine read-order dossier.

## Source Surfaces

- `mechanics/comparison-spine/parts/spine-overview/reports/comparison-spine-proof-flow-v1.md`

## Inputs

- bundle-local `baseline_mode` and `comparison_surface` records;
- generated `generated/comparison_spine.json` and catalog proof-artifact routes;
- fixed-baseline, peer-compare, and longitudinal-window part reports;
- comparison guide wording that names anti-overread boundaries;
- selection questions that need a cross-mode read order.

## Outputs

- one cross-mode comparison-spine proof-flow dossier;
- read-order guidance for fixed-baseline, peer-compare, and
  longitudinal-window claims;
- route notes that point readers back to source bundles and generated readers;
- warnings when a comparison mode is likely to be overread as broad growth,
  ranking, promotion, or source truth.

## Stronger Owner Split

Source proof bundles own claim meaning, object under evaluation, comparison
surface, verdict posture, and blind spots.

This part owns the cross-mode read-order dossier. Generated comparison readers
route as derived companions.

## Boundary

The overview dossier routes fixed-baseline, peer-compare, and
longitudinal-window reading. Bundle-local comparison surfaces and
`generated/comparison_spine.json` keep their own source routes.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| overview dossier as comparison result | source bundle comparison surface plus mode-specific part report |
| fixed-baseline, peer-compare, and longitudinal-window collapsed into one score | mode-specific part route plus bundle-local review |
| generated comparison reader as source truth | source bundle, builder, and `build_catalog.py --check` route |
| read-order guidance as bundle promotion or deprecation | bundle-local review and release/report owner route |
| one clean comparison as broad capability growth | declared comparison mode plus growth/progression owner review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
