"""Antifragility route token constants."""

from __future__ import annotations


ANTIFRAGILITY_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "stress or repair pressure",
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "evals/stress/aoa-antifragility-posture/EVAL.md",
    "evals/comparison/longitudinal-window/aoa-stress-recovery-window/EVAL.md",
    "evals/workflow/aoa-repair-boundedness/EVAL.md",
    "mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "Stronger Owner Split",
    "Stop-Lines",
    "| global resilience or federation-health pressure | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| live runtime self-healing pressure | runtime owner or `abyss-stack` runtime route |",
    "| deletion, cleanup, or owner-local repair authority pressure | owner repository repair and cleanup route |",
    "| one-score antifragility pressure | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| route, stats, memo, or generated-reader authority pressure | owning route, stats, memo, generated-source, and owner-receipt routes |",
    "| diagnosis-cause discipline or growth-cycle movement pressure | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "python scripts/validate_repo.py --eval aoa-stress-recovery-window",
)
ANTIFRAGILITY_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "antifragility proof work",
    "mechanics/antifragility/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "comparison-spine",
    "audit",
    "Create antifragility parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
ANTIFRAGILITY_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-diagnosis-cause-discipline",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "| global resilience or federation health | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| one-score health or antifragility movement | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| deletion theater, cleanup authority, runtime self-healing, or owner-local repair execution | owner repository or `abyss-stack` runtime route |",
    "| route, memo, stats, KAG, playbook, or generated-reader truth promotion | owning route, memo, stats, KAG, playbook, generated-source, and owner-receipt routes |",
    "| diagnosis-cause discipline or growth-cycle movement | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
)
ANTIFRAGILITY_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "| role | lower index for active eval-side Antifragility proof parts |",
    "## Active Parts",
    "| `posture-review/` | first-wave owner-local antifragility posture support |",
    "| `stress-recovery-window/` | repeated-window stress recovery support with comparison-spine readout |",
    "| `repair-proof/` | bounded repair-proof support with owner acceptance route |",
    "## Owner Pressure Routes",
    "| global resilience or federation health | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| one-score health or antifragility movement | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| runtime repair, live self-healing, cleanup authority, or owner-local repair execution | owner repository or `abyss-stack` runtime route |",
    "| source proof meaning or verdict support | affected `evals/**/EVAL.md`, `evals/**/eval.yaml`, and bundle-local report contract |",
    "| diagnosis-cause discipline or growth-cycle movement | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "## Part Admission Route",
    "| new antifragility pressure | recurring operation with distinct inputs, outputs, owner split, and validation | parent `PARTS.md` update plus decision review |",
    "mechanics/antifragility/parts/AGENTS.md#validation",
)
ANTIFRAGILITY_PARTS_README_FORBIDDEN_TOKENS = (
    "The parts support proof review. They do not own source proof bundle meaning",
)
ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
ANTIFRAGILITY_POSTURE_PART_REQUIRED_TOKENS = (
    "aoa-antifragility-posture",
    "mechanics/antifragility/parts/posture-review/schemas/antifragility_eval_report_v1.json",
    "source eval package stays under `evals/`",
    "owner repository owns the local",
    "| repo-global resilience pressure | `Agents-of-Abyss` doctrine route plus owner evidence review |",
    "| repeated-window improvement pressure | `stress-recovery-window` and `comparison-spine` longitudinal routes |",
    "| runtime repair or live self-healing pressure | owner repository or `abyss-stack` runtime route |",
    "| source-ownership transfer pressure | owner repository receipt route |",
    "| route hints, stats, memory, or generated-reader authority pressure | owner receipts plus owning route, stats, memo, and generated-source routes |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_STRESS_WINDOW_PART_REQUIRED_TOKENS = (
    "aoa-stress-recovery-window",
    "mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md",
    "mechanics/antifragility/parts/stress-recovery-window/fixtures/stress-recovery-window-bounded-v1/README.md",
    "mechanics/antifragility/parts/stress-recovery-window/schemas/stress_recovery_window_eval_report_v1.json",
    "mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md",
    "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
    "comparison-spine",
    "audit",
    "| federation-wide resilience pressure | `Agents-of-Abyss` doctrine route plus owner evidence review |",
    "| live health or runtime recovery authority pressure | runtime owner or `abyss-stack` runtime route |",
    "| one-score antifragility movement pressure | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| route, KAG, memo, playbook, or generated-reader authority pressure | owning route, KAG, memo, playbook, generated-source, and owner-evidence routes |",
    "| comparison acceptance pressure | `mechanics/comparison-spine/parts/longitudinal-window/` readout route |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_STRESS_WINDOW_DOC_REQUIRED_TOKENS = (
    "It answers a narrow question",
    "This remains a proof surface",
    "Workflow ownership stays with the owner route",
    "Federation-wide vibe-check pressure routes back to named owner evidence",
    "| route hints outranking owner receipts | owner receipt route before route-hint interpretation |",
    "| memo pattern objects standing in for current-run truth | owner evidence route before memo context |",
    "| regrounding success from ticket existence alone | regrounding evidence route with outcome conditions |",
    "| KAG quarantine exit as healthy re-entry | KAG condition route plus explicit re-entry evidence |",
    "| single-number movement pressure | split-axis stress-recovery readout route |",
)
ANTIFRAGILITY_REPAIR_PROOF_PART_REQUIRED_TOKENS = (
    "aoa-repair-boundedness",
    "mechanics/antifragility/parts/repair-proof/fixtures/repair-boundedness-v1/README.md",
    "repair-proof route",
    "aoa-diagnosis-cause-discipline",
    "| final owner-object quality pressure | owner repository acceptance route |",
    "| permanent stability pressure | owner repository regression and follow-through route |",
    "| authority widening after a repair pressure | owner approval and route-law review |",
    "| repair parent topology pressure | `mechanics/antifragility/` parent route plus evidence-cluster review |",
    "| `aoa-diagnosis-cause-discipline` pressure | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "| growth-cycle improvement pressure | growth-cycle proof route |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/antifragility/",
    "AoA-aligned",
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "Source proof bundles stay under `evals/`",
    "comparison-spine",
    "audit",
    "aoa-diagnosis-cause-discipline",
)
ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Antifragility Part Contract Guard",
    "mechanics/antifragility/parts/posture-review/README.md",
    "mechanics/antifragility/parts/stress-recovery-window/README.md",
    "mechanics/antifragility/parts/repair-proof/README.md",
    "global resilience",
    "live self-healing",
    "permanent stability",
    "repair parent",
    "growth-cycle completion",
    "growth-cycle/diagnosis-gate",
)


__all__ = tuple(
    name for name in globals() if name.startswith("ANTIFRAGILITY_") and name.endswith("_TOKENS")
)
