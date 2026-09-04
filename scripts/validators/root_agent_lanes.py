"""Root agent-lane route contracts."""

from __future__ import annotations

from pathlib import Path

from validators import root_design_common as root_design_common_validator
from validators.common import ValidationIssue
from validators.root_common import require_tokens


AGENTS_DISTRICT_NAME = ".agents/AGENTS.md"
PROOF_TOPOLOGY_NAME = root_design_common_validator.PROOF_TOPOLOGY_NAME
AGENTS_DISTRICT_REQUIRED_TOKENS = (
    ".agents/<lane>/",
    "top-level `skills/`",
    "owner-admitted",
    "Proof authority stays",
    "python scripts/validate_repo.py",
    "python scripts/validate_nested_agents.py",
)
def validate_agent_lane_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(repo_root, AGENTS_DISTRICT_NAME, AGENTS_DISTRICT_REQUIRED_TOKENS, issues)
    require_tokens(repo_root, "README.md", (AGENTS_DISTRICT_NAME,), issues)
    require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (".agents/", "Agent guidance"), issues)
    repo_skill_home = repo_root / "skills"
    repo_skill_projection = repo_root / ".agents" / "skills"
    if repo_skill_projection.exists() and not repo_skill_home.exists():
        issues.append(
            ValidationIssue(
                ".agents/skills/",
                "repo skill projection requires an owner-admitted top-level skills/ home",
            )
        )
    return issues


__all__ = (
    "AGENTS_DISTRICT_NAME",
    "AGENTS_DISTRICT_REQUIRED_TOKENS",
    "validate_agent_lane_surfaces",
)
