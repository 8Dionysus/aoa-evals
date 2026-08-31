# Proof Infra / Reportable Contracts Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `reportable-contracts` child validation block there. It covers the
active-organ C21-C23 schema and semantic validator, its executable negative
corpus including canonical C22 self-digest tampering, the bounded scorer
helper, and broader repository checks. The consuming
`aoa-memo-active-organ-offline-replay` bundle adds 25 conformance cases and
bundle-local methodology tests through its own source route. This file is the
part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/proof-infra/parts/reportable-contracts`.

## Commands

```bash
python mechanics/proof-infra/parts/reportable-contracts/scripts/validate_active_organ_experiment_contracts.py
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_active_organ_experiment_contracts.py mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py tests/test_build_catalog.py tests/test_validate_repo.py
```
