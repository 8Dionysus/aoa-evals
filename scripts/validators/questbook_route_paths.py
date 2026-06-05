"""Questbook route path constants."""

from __future__ import annotations

QUESTBOOK_NAME = "QUESTBOOK.md"
QUESTS_README_NAME = "quests/README.md"
QUESTS_AGENTS_NAME = "quests/AGENTS.md"
QUEST_LIFECYCLE_NAME = "quests/LIFECYCLE.md"
QUESTBOOK_INTEGRATION_NAME = "docs/operations/QUESTBOOK_EVAL_INTEGRATION.md"
QUESTBOOK_MECHANIC_README_NAME = "mechanics/questbook/README.md"
QUESTBOOK_MECHANIC_AGENTS_NAME = "mechanics/questbook/AGENTS.md"
QUESTBOOK_MECHANIC_PARTS_NAME = "mechanics/questbook/PARTS.md"
QUESTBOOK_MECHANIC_PROVENANCE_NAME = "mechanics/questbook/PROVENANCE.md"
QUESTBOOK_SOURCE_RECORD_PART_README_NAME = (
    "mechanics/questbook/parts/source-record-contract/README.md"
)
QUESTBOOK_DISPATCH_READER_PART_README_NAME = (
    "mechanics/questbook/parts/dispatch-reader/README.md"
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0070-questbook-part-owner-split-contract.md"
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0098-agon-quest-note-provenance-route.md"
)


__all__ = tuple(name for name in globals() if name.endswith("_NAME"))
