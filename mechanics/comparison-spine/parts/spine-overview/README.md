# Spine Overview Part

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

This part owns only the cross-mode read-order dossier. Generated comparison
readers remain derived companions, not source truth.

## Boundary

The overview dossier routes fixed-baseline, peer-compare, and
longitudinal-window reading. It does not replace bundle-local comparison
surfaces or `generated/comparison_spine.json`.

## Stop-Lines

- Do not treat the overview dossier as a comparison result.
- Do not collapse fixed-baseline, peer-compare, and longitudinal-window into
  one score.
- Do not use generated comparison readers as source truth.
- Do not use read-order guidance to promote or deprecate bundles.
- Do not turn one clean comparison into broad capability growth.

## Validation

Payload coverage anchor: `mechanics/comparison-spine/parts/spine-overview/`.

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
