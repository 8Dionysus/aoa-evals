# Audit / Candidate Readers Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `candidate-readers` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/audit/parts/candidate-readers`.

## Commands

```bash
python scripts/validate_eval_candidate_packets.py --schema-only
python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
