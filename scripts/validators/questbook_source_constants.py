"""Questbook authored source and generated projection constants."""

from __future__ import annotations

from validators import questbook_route_paths as questbook_route_paths_validator


QUESTBOOK_NAME = questbook_route_paths_validator.QUESTBOOK_NAME
QUESTBOOK_INTEGRATION_NAME = questbook_route_paths_validator.QUESTBOOK_INTEGRATION_NAME
QUEST_SCHEMA_NAME = "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json"
QUEST_DISPATCH_SCHEMA_NAME = "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json"
QUEST_CATALOG_NAME = "generated/quest_catalog.min.json"
QUEST_DISPATCH_NAME = "generated/quest_dispatch.min.json"
QUEST_CATALOG_EXAMPLE_NAME = "generated/quest_catalog.min.example.json"
QUEST_DISPATCH_EXAMPLE_NAME = "generated/quest_dispatch.min.example.json"
QUEST_SOURCE_LANES = (
    "proof",
    "trace",
    "orchestrator",
    "unlock",
    "runtime",
    "closeout",
    "agon",
    "harvest",
    "questbook",
)
QUEST_SOURCE_STATES = (
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
)
FOUNDATION_QUEST_NAMES = (
    "AOA-EV-Q-0001",
    "AOA-EV-Q-0002",
    "AOA-EV-Q-0003",
    "AOA-EV-Q-0004",
)
CLOSED_QUEST_STATES = {"done", "dropped"}
QUEST_SCHEMA_TITLE = "work_quest_v1"
QUEST_SCHEMA_VERSION = "work_quest_v1"
QUEST_DISPATCH_SCHEMA_TITLE = "quest_dispatch_v1"
QUEST_DISPATCH_SCHEMA_VERSION = "quest_dispatch_v1"
QUEST_DISPATCH_ARTIFACT_OVERRIDES = {
    "AOA-EV-Q-0001": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0002": [
        "bounded_plan",
        "evaluation_result",
        "verification_result",
    ],
    "AOA-EV-Q-0003": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0004": [
        "recurrence_evidence",
        "promotion_decision",
    ],
}


__all__ = (
    "CLOSED_QUEST_STATES",
    "FOUNDATION_QUEST_NAMES",
    "QUESTBOOK_INTEGRATION_NAME",
    "QUESTBOOK_NAME",
    "QUEST_CATALOG_EXAMPLE_NAME",
    "QUEST_CATALOG_NAME",
    "QUEST_DISPATCH_ARTIFACT_OVERRIDES",
    "QUEST_DISPATCH_EXAMPLE_NAME",
    "QUEST_DISPATCH_NAME",
    "QUEST_DISPATCH_SCHEMA_NAME",
    "QUEST_DISPATCH_SCHEMA_TITLE",
    "QUEST_DISPATCH_SCHEMA_VERSION",
    "QUEST_SCHEMA_NAME",
    "QUEST_SCHEMA_TITLE",
    "QUEST_SCHEMA_VERSION",
    "QUEST_SOURCE_LANES",
    "QUEST_SOURCE_STATES",
)
