"""Experience route path constants."""

from __future__ import annotations


EXPERIENCE_MECHANIC_README_NAME = "mechanics/experience/README.md"
EXPERIENCE_MECHANIC_AGENTS_NAME = "mechanics/experience/AGENTS.md"
EXPERIENCE_MECHANIC_PARTS_NAME = "mechanics/experience/PARTS.md"
EXPERIENCE_MECHANIC_PROVENANCE_NAME = "mechanics/experience/PROVENANCE.md"
EXPERIENCE_PROTOCOL_PART_README_NAME = (
    "mechanics/experience/parts/protocol-integrity/README.md"
)
EXPERIENCE_CERTIFICATION_PART_README_NAME = (
    "mechanics/experience/parts/certification-gate/README.md"
)
EXPERIENCE_ADOPTION_PART_README_NAME = (
    "mechanics/experience/parts/adoption-federation/README.md"
)
EXPERIENCE_GOVERNANCE_PART_README_NAME = (
    "mechanics/experience/parts/governance-runtime-boundary/README.md"
)
EXPERIENCE_OFFICE_PART_README_NAME = (
    "mechanics/experience/parts/office-release-train/README.md"
)
EXPERIENCE_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0033-experience-mechanic-package.md"
EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0043-experience-verdict-residue-parts.md"
)
EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0063-experience-part-contract-guard.md"
)


__all__ = tuple(name for name in globals() if name.startswith("EXPERIENCE_"))
