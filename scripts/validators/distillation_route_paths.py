"""Distillation route path constants."""

from __future__ import annotations


DISTILLATION_MECHANIC_README_NAME = "mechanics/distillation/README.md"
DISTILLATION_MECHANIC_DIRECTION_NAME = "mechanics/distillation/DIRECTION.md"
DISTILLATION_MECHANIC_AGENTS_NAME = "mechanics/distillation/AGENTS.md"
DISTILLATION_MECHANIC_PARTS_NAME = "mechanics/distillation/PARTS.md"
DISTILLATION_MECHANIC_PROVENANCE_NAME = "mechanics/distillation/PROVENANCE.md"
DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME = (
    "mechanics/distillation/parts/compost-provenance/README.md"
)
DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME = (
    "mechanics/distillation/parts/runtime-candidate-adoption/README.md"
)
DISTILLATION_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0038-distillation-mechanic-package.md"
)
DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0064-distillation-part-contract-guard.md"
)


__all__ = tuple(name for name in globals() if name.startswith("DISTILLATION_"))
