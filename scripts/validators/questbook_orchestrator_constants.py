"""Questbook orchestrator proof and sibling-reference constants."""

from __future__ import annotations


ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS = {
    "repo_layer_selection",
    "evidence_closure",
    "bounded_next_step",
}
ORCHESTRATOR_PROOF_QUESTS = {
    "AOA-EV-Q-0006": ("aoa-agents:router", "repo_layer_selection"),
    "AOA-EV-Q-0007": ("aoa-agents:review", "evidence_closure"),
    "AOA-EV-Q-0008": ("aoa-agents:bounded_execution", "bounded_next_step"),
}
ORCHESTRATOR_CLASS_CATALOG_NAME = "generated/orchestrator_class_catalog.min.json"
ORCHESTRATOR_PROOF_ALIGNMENT_NAME = (
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/"
    "ORCHESTRATOR_PROOF_ALIGNMENT.md"
)
ORCHESTRATOR_PROOF_REQUIRED_TOKENS = (
    "## Router",
    "## Review",
    "## Bounded execution",
    "## Boundary rule",
    "Proof surfaces judge work.",
)


__all__ = (
    "ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS",
    "ORCHESTRATOR_CLASS_CATALOG_NAME",
    "ORCHESTRATOR_PROOF_ALIGNMENT_NAME",
    "ORCHESTRATOR_PROOF_QUESTS",
    "ORCHESTRATOR_PROOF_REQUIRED_TOKENS",
)
