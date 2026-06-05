"""Antifragility route path constants."""

from __future__ import annotations


ANTIFRAGILITY_MECHANIC_README_NAME = "mechanics/antifragility/README.md"
ANTIFRAGILITY_MECHANIC_AGENTS_NAME = "mechanics/antifragility/AGENTS.md"
ANTIFRAGILITY_MECHANIC_PARTS_NAME = "mechanics/antifragility/PARTS.md"
ANTIFRAGILITY_PARTS_README_NAME = "mechanics/antifragility/parts/README.md"
ANTIFRAGILITY_MECHANIC_PROVENANCE_NAME = "mechanics/antifragility/PROVENANCE.md"
ANTIFRAGILITY_POSTURE_PART_README_NAME = (
    "mechanics/antifragility/parts/posture-review/README.md"
)
ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME = (
    "mechanics/antifragility/parts/stress-recovery-window/README.md"
)
ANTIFRAGILITY_STRESS_WINDOW_DOC_NAME = (
    "mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md"
)
ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME = (
    "mechanics/antifragility/parts/repair-proof/README.md"
)
ANTIFRAGILITY_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0034-antifragility-mechanic-package.md"
)
ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0061-antifragility-part-contract-guard.md"
)


__all__ = tuple(name for name in globals() if name.startswith("ANTIFRAGILITY_"))
