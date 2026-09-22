# Testing Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pytest -q tests/test_test_topology.py
```

This suite tests the checker with bounded positive and negative fixtures. For
an inventory edit, also check the existing current-tree integration route:

```bash
python -m pytest -q tests/test_validation_topology.py::ValidationTopologyTests::test_validation_topology_validator_accepts_current_surfaces
```
