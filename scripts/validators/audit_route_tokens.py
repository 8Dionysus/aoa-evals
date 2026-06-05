"""Audit route token constants."""

from __future__ import annotations


MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
AUDIT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
    "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json",
    "candidate-only",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "runtime or trace artifact",
    "selected evidence packet",
    "runtime candidate reader",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/audit/",
    "runtime evidence selection",
    "artifact-to-verdict",
    "generated readers",
    "bundle-local review",
    "does not turn runtime evidence into proof canon",
)
AUDIT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for `audit` part-local candidate-evidence suboperations",
    "## Active Parts",
    "`selected-evidence-packets/`",
    "`artifact-verdict-hooks/`",
    "`candidate-readers/`",
    "`integrity-review/`",
    "## Part Admission Route",
    "source surfaces",
    "drift-catching validation",
    "stronger-owner boundary",
    "mechanics/audit/AGENTS.md#validation",
)
AUDIT_PARTS_README_FORBIDDEN_TOKENS = (
    "Do not create another part unless",
)
AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
AUDIT_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/runtime-evidence/",
    "mechanics/audit/",
    "schemas/runtime-evidence-selection.schema.json",
    "mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json",
    "generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
)
AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "runtime-evidence",
    "audit",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "Current route:",
    "new audit proof work starts in the owning active part",
)
AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)
AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Audit Part Contract Guard",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "inputs, outputs",
    "stronger-owner split",
    "candidate-only",
    "python scripts/validate_repo.py",
)
AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "runtime-evidence-selection.schema.json",
    "runtime_evidence_selection.*.example.json",
    "candidate-only",
    "bundle-local review",
    "overread-routing notes",
    "runtime-owner review and bundle-local eval review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "TRACE_EVAL_BRIDGE.md",
    "artifact-to-verdict-hook.schema.json",
    "mechanic-local hook examples",
    "review metadata",
    "route to the owning eval bundle",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "generate_runtime_candidate_template_index.py",
    "runtime_candidate_template_index.min.json",
    "runtime_candidate_intake.min.json",
    "Reader changes start in",
    "generated reader content needs to change",
)
AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "RUNTIME_INTEGRITY_REVIEW.md",
    "runtime-integrity-review.schema.json",
    "runtime_integrity_review.example.json",
    "candidate-only",
    "runtime continuity activation is requested",
    "route to Experience and runtime-owner gates",
    "python -m pytest -q tests/test_runtime_evidence_surfaces.py -k runtime_integrity_review",
)


__all__ = tuple(name for name in globals() if name.endswith("_TOKENS"))
