"""Root agent index chain surface contracts."""

from __future__ import annotations

from pathlib import Path

from validators import root_design_common as root_design_common_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.root_common import DECISION_RECORDS_README_NAME, require_tokens


ROADMAP_NAME = root_design_common_validator.ROADMAP_NAME
PROOF_TOPOLOGY_NAME = root_design_common_validator.PROOF_TOPOLOGY_NAME
AGENT_INDEX_NAME = "docs/architecture/AGENT_INDEX.md"
AGENT_INDEX_CHAIN_DECISION_NAME = "docs/decisions/AOA-EV-D-0103-agent-index-chain-surface.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
AGENT_INDEX_REQUIRED_TOKENS = (
    "pass-through index for agents",
    "path needs an explicit owner route",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "nearest `AGENTS.md`",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/README.md",
    "docs/decisions/README.md",
    "route-card-only",
    "compatibility districts",
    "mechanics/<parent>/parts/<part>/VALIDATION.md",
    "mechanics/<parent>/parts/AGENTS.md",
    "Executable validation commands belong in the nearest `AGENTS.md`",
)
AGENT_INDEX_FORBIDDEN_ROUTE_SCAFFOLD = (
    "path name is not enough",
    "An agent should expect only",
    "should it be part-local",
)
AGENT_INDEX_DECISION_REQUIRED_TOKENS = (
    "Agent Index Chain Surface",
    "docs/architecture/AGENT_INDEX.md",
    "docs/README.md",
    "active mechanic parent",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "route-card-only root districts",
    "Executable validation commands remain in the nearest `AGENTS.md`",
)


def validate_agent_index_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(repo_root, AGENT_INDEX_NAME, AGENT_INDEX_REQUIRED_TOKENS, issues)
    index_text = read_text_or_issue(repo_root / AGENT_INDEX_NAME, issues, root=repo_root)
    if index_text:
        for stale_phrase in AGENT_INDEX_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in index_text:
                issues.append(
                    ValidationIssue(
                        AGENT_INDEX_NAME,
                        "agent index should name explicit owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    require_tokens(repo_root, AGENT_INDEX_CHAIN_DECISION_NAME, AGENT_INDEX_DECISION_REQUIRED_TOKENS, issues)
    require_tokens(repo_root, "README.md", (AGENT_INDEX_NAME, "repo to authority class"), issues)
    require_tokens(repo_root, "docs/README.md", ("AGENT_INDEX.md", "Agent Index", "Mechanics Refactor Path"), issues)
    require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (AGENT_INDEX_NAME, "pass-through reader"), issues)
    require_tokens(repo_root, ROADMAP_NAME, (AGENT_INDEX_NAME, "Agent index chain"), issues)
    require_tokens(repo_root, MECHANICS_EVIDENCE_CLUSTERS_NAME, (AGENT_INDEX_NAME, "agent-facing pass-through index"), issues)
    require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (AGENT_INDEX_CHAIN_DECISION_NAME, "Agent Index Chain Surface"),
        issues,
    )

    return issues


__all__ = (
    "AGENT_INDEX_CHAIN_DECISION_NAME",
    "AGENT_INDEX_DECISION_REQUIRED_TOKENS",
    "AGENT_INDEX_FORBIDDEN_ROUTE_SCAFFOLD",
    "AGENT_INDEX_NAME",
    "AGENT_INDEX_REQUIRED_TOKENS",
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "validate_agent_index_surface",
)
