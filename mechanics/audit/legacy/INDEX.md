# Audit Legacy Index

| Former or overloaded source | Current active route | Posture |
| --- | --- | --- |
| `mechanics/runtime-evidence/` | `mechanics/audit/` | rejected parent naming: runtime-evidence is an evidence class, not the parent mechanic |
| `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md` | `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md` | former docs-root guide path |
| `schemas/runtime-evidence-selection.schema.json` | `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json` | former root schema path |
| `examples/runtime_evidence_selection.*.example.json` | `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json` | former root example family |
| `docs/TRACE_EVAL_BRIDGE.md` | `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md` | former docs-root hook guide path |
| `schemas/artifact-to-verdict-hook.schema.json` | `mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json` | former root schema path |
| `examples/artifact_to_verdict_hook.*.example.json` | `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json` | former root example family |
| `generated/runtime_candidate_template_index.min.json` | `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json` | former root generated reader |
| `generated/runtime_candidate_intake.min.json` | `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json` | former root generated reader |

## Boundary

Former root paths are provenance only. Current audit contracts should cite the
active part-local paths. Generated candidate readers must be rebuilt by the
part-local builders, not hand-edited through old paths.
