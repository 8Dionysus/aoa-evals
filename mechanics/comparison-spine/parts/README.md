# Comparison Spine Parts

This directory holds package-local parts for comparison-spine fixture and
readout surfaces.

Use these parts when a bundle's `comparison_surface`, fixture contract, or
runner contract points to a comparison-spine support surface.

## Active Parts

- `spine-overview/`: cross-mode comparison-spine read order.
- `fixed-baseline/`: same-task fixed-baseline fixture family and dossier.
- `peer-compare/`: artifact/process paired fixture families and dossiers.
- `longitudinal-window/`: repeated-window fixture family plus
  repeated-window and stress-recovery dossiers.

## Validation

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
