"""Audit route path constants."""

from __future__ import annotations


AUDIT_MECHANIC_README_NAME = "mechanics/audit/README.md"
AUDIT_MECHANIC_AGENTS_NAME = "mechanics/audit/AGENTS.md"
AUDIT_MECHANIC_PROVENANCE_NAME = "mechanics/audit/PROVENANCE.md"
AUDIT_PARTS_README_NAME = "mechanics/audit/parts/README.md"
AUDIT_LEGACY_INDEX_NAME = "mechanics/audit/legacy/INDEX.md"
AUDIT_LEGACY_DISTILLATION_LOG_NAME = "mechanics/audit/legacy/DISTILLATION_LOG.md"
AUDIT_LEGACY_RAW_README_NAME = "mechanics/audit/legacy/raw/README.md"
AUDIT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0053-audit-part-contract-guard.md"
)
AUDIT_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0007-audit-mechanic-package.md"
AUDIT_SELECTED_EVIDENCE_PART_README_NAME = (
    "mechanics/audit/parts/selected-evidence-packets/README.md"
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME = (
    "mechanics/audit/parts/artifact-verdict-hooks/README.md"
)
AUDIT_CANDIDATE_READERS_PART_README_NAME = (
    "mechanics/audit/parts/candidate-readers/README.md"
)
AUDIT_INTEGRITY_REVIEW_PART_README_NAME = (
    "mechanics/audit/parts/integrity-review/README.md"
)


__all__ = tuple(name for name in globals() if name.startswith("AUDIT_"))
