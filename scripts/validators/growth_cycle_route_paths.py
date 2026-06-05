"""Growth-cycle route path constants."""

from __future__ import annotations


GROWTH_CYCLE_MECHANIC_README_NAME = "mechanics/growth-cycle/README.md"
GROWTH_CYCLE_MECHANIC_AGENTS_NAME = "mechanics/growth-cycle/AGENTS.md"
GROWTH_CYCLE_MECHANIC_PARTS_NAME = "mechanics/growth-cycle/PARTS.md"
GROWTH_CYCLE_PARTS_README_NAME = "mechanics/growth-cycle/parts/README.md"
GROWTH_CYCLE_MECHANIC_PROVENANCE_NAME = "mechanics/growth-cycle/PROVENANCE.md"
GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME = (
    "mechanics/growth-cycle/parts/diagnosis-gate/README.md"
)
GROWTH_CYCLE_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0037-growth-cycle-mechanic-package.md"
)
GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0065-growth-cycle-diagnosis-gate-contract.md"
)
REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0099-repair-diagnosis-route-boundary.md"
)


__all__ = tuple(
    name for name in globals() if name.startswith(("GROWTH_CYCLE_", "REPAIR_"))
)
