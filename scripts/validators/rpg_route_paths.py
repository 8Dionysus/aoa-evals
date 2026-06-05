"""RPG route path constants."""

from __future__ import annotations


RPG_MECHANIC_README_NAME = "mechanics/rpg/README.md"
RPG_MECHANIC_AGENTS_NAME = "mechanics/rpg/AGENTS.md"
RPG_MECHANIC_PARTS_NAME = "mechanics/rpg/PARTS.md"
RPG_MECHANIC_PROVENANCE_NAME = "mechanics/rpg/PROVENANCE.md"
RPG_PROGRESS_UNLOCKS_PART_README_NAME = (
    "mechanics/rpg/parts/progression-unlocks/README.md"
)
RPG_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0036-rpg-mechanic-package.md"
RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0067-rpg-progression-unlocks-contract.md"
)


__all__ = tuple(name for name in globals() if name.startswith("RPG_"))
