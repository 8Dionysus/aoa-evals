"""Method-growth route path constants."""

from __future__ import annotations


METHOD_GROWTH_MECHANIC_README_NAME = "mechanics/method-growth/README.md"
METHOD_GROWTH_MECHANIC_AGENTS_NAME = "mechanics/method-growth/AGENTS.md"
METHOD_GROWTH_MECHANIC_PARTS_NAME = "mechanics/method-growth/PARTS.md"
METHOD_GROWTH_MECHANIC_PROVENANCE_NAME = "mechanics/method-growth/PROVENANCE.md"
METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME = (
    "mechanics/method-growth/parts/candidate-lineage/README.md"
)
METHOD_GROWTH_OWNER_LANDING_PART_README_NAME = (
    "mechanics/method-growth/parts/owner-landing/README.md"
)
METHOD_GROWTH_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0035-method-growth-mechanic-package.md"
)
METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0068-method-growth-part-owner-split-contract.md"
)


__all__ = tuple(name for name in globals() if name.startswith("METHOD_GROWTH_"))
