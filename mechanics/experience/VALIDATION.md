# Experience Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py
python -m pytest -q mechanics/experience/parts/certification-gate/tests
python -m pytest -q mechanics/experience/parts/adoption-federation/tests
python -m pytest -q mechanics/experience/parts/governance-runtime-boundary/tests
python -m pytest -q mechanics/experience/parts/office-release-train/tests
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
