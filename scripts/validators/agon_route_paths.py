"""Agon route path constants."""

from __future__ import annotations


AGON_MECHANIC_README_NAME = "mechanics/agon/README.md"
AGON_MECHANIC_AGENTS_NAME = "mechanics/agon/AGENTS.md"
AGON_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0016-agon-mechanic-package.md"
AGON_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0054-agon-part-contract-guard.md"
)
AGON_COURT_PREBINDING_PART_README_NAME = (
    "mechanics/agon/parts/court-prebinding/README.md"
)
AGON_CCS_ALIGNMENT_PART_README_NAME = "mechanics/agon/parts/ccs-alignment/README.md"
AGON_VDS_ALIGNMENT_PART_README_NAME = "mechanics/agon/parts/vds-alignment/README.md"
AGON_MECHANICAL_TRIAL_SUITES_PART_README_NAME = (
    "mechanics/agon/parts/mechanical-trial-suites/README.md"
)
AGON_RETENTION_RANK_ALIGNMENT_PART_README_NAME = (
    "mechanics/agon/parts/retention-rank-alignment/README.md"
)
AGON_EPISTEMIC_ALIGNMENT_PART_README_NAME = (
    "mechanics/agon/parts/epistemic-alignment/README.md"
)
AGON_SLC_ALIGNMENT_PART_README_NAME = "mechanics/agon/parts/slc-alignment/README.md"
AGON_KAG_ALIGNMENT_PART_README_NAME = "mechanics/agon/parts/kag-alignment/README.md"
AGON_SOPHIAN_THRESHOLD_ALIGNMENT_PART_README_NAME = (
    "mechanics/agon/parts/sophian-threshold-alignment/README.md"
)
AGON_PART_README_NAMES = (
    AGON_COURT_PREBINDING_PART_README_NAME,
    AGON_CCS_ALIGNMENT_PART_README_NAME,
    AGON_VDS_ALIGNMENT_PART_README_NAME,
    AGON_MECHANICAL_TRIAL_SUITES_PART_README_NAME,
    AGON_RETENTION_RANK_ALIGNMENT_PART_README_NAME,
    AGON_EPISTEMIC_ALIGNMENT_PART_README_NAME,
    AGON_SLC_ALIGNMENT_PART_README_NAME,
    AGON_KAG_ALIGNMENT_PART_README_NAME,
    AGON_SOPHIAN_THRESHOLD_ALIGNMENT_PART_README_NAME,
)


__all__ = tuple(name for name in globals() if name.startswith("AGON_"))
