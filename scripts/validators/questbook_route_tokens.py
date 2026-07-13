"""Questbook route token constants."""

from __future__ import annotations

QUESTBOOK_INTEGRATION_REQUIRED_TOKENS = (
    "proof",
    "regression",
    "verdict-bridge",
    "example-only",
    "repo-local review projection",
    "not live portable verdict authority",
)
QUESTBOOK_NOTE_REQUIRED_TOKENS = (
    "# Questbook Obligation Index",
    "public human obligation index",
    "proof",
    "regression",
    "verdict-bridge",
    "Closed source records stay in `quests/` and generated projections as",
    "Promotion happens through reviewed owner acceptance",
    "Quest-harvest route:",
    "route output into quest source records, owner handoff, or reviewed",
    "Eval bundle meaning stays in source bundles",
)
QUESTS_README_REQUIRED_TOKENS = (
    "# Quest Source Records",
    "source quest record district",
    "human questbook index",
    "mechanics/questbook/",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "source eval packages under `evals/`",
)
QUESTS_AGENTS_REQUIRED_TOKENS = (
    "source quest record district",
    "mechanics/questbook/",
    "generated quest files as dispatch readers",
    "source quest records",
    "schema-backed YAML",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "validate_repo.py",
)
QUEST_LIFECYCLE_REQUIRED_TOKENS = (
    "# Quest Lifecycle Contract",
    "State Matrix",
    "Open-index posture",
    "Return posture",
    "Promotion posture",
    "Proof-Loop Return Use",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "below eval result receipt",
    "Open states",
    "Closed states",
    "`QUESTBOOK.md` must list open quest IDs and leave closed quest IDs out",
)
QUESTBOOK_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "quests/",
    "quests/LIFECYCLE.md",
    "source-record-contract",
    "dispatch-reader",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "lane/state",
    "Quests route eval-bundle",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source quest record",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "mechanics/questbook/PROVENANCE.md",
    "quests/LIFECYCLE.md",
    "generated quest reader",
    "lane/state",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "source-record-contract",
    "dispatch-reader",
    "generated quest reader",
    "source quest record",
    "old top-level quest source path revived as alias",
    "AGENTS.md#validation",
)
QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS = (
    "Quest Source Record Contract",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json",
    "quests/<lane>/<state>/AOA-EV-Q-*.yaml",
    "quests/LIFECYCLE.md",
    "QUESTBOOK.md",
    "generated projection input",
    "source quest record identity",
    "aoa-quest-harvest",
    "roadmap direction",
    "owner acceptance",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS = (
    "Quest Dispatch Reader",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "scripts/build_catalog.py",
    "generated projection contract",
    "source quest truth",
    "live task assignment",
    "proof-surface promotion",
    "python scripts/build_catalog.py --check",
)
QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS = (
    "quests/LIFECYCLE.md",
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
    "proof-loop",
    "route-smoke",
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS = (
    "mechanics/agon/PROVENANCE.md",
    "Agon legacy archive",
    "archive-local accounting",
    "schema-backed source quest records",
    "markdown quest notes",
    "quests/",
)
QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/questbook/",
    "source quest records",
    "generated quest",
    "lane/state",
    "no empty taxonomy",
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Questbook Part Owner-split Contract",
    "mechanics/questbook/parts/source-record-contract/README.md",
    "mechanics/questbook/parts/dispatch-reader/README.md",
    "`## Stronger Owner Split`",
    "Source quest records stay under `quests/<lane>/<state>/`",
    "Human visibility stays",
    "Generated quest readers stay under root `generated/`",
    "aoa-quest-harvest",
    "live task assignment",
)


__all__ = tuple(name for name in globals() if name.endswith("_TOKENS"))
