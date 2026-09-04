# Comparison Spine / Peer Compare Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `peer-compare` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/comparison-spine/parts/peer-compare`.

## Commands

```bash
python mechanics/comparison-spine/parts/peer-compare/scripts/run_validation_routing_comparison.py --format text
python -m pytest -q mechanics/comparison-spine/parts/peer-compare/tests/test_validation_routing_comparison.py
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
