# Mechanics Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon
python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory
python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../VALIDATION.md#non-mutating-checks).
