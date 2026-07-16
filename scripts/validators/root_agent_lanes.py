"""Root agent-lane route contracts."""

from __future__ import annotations

from pathlib import Path

from validators import root_design_common as root_design_common_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.root_common import markdown_python_commands, require_tokens


AGENTS_DISTRICT_NAME = ".agents/AGENTS.md"
SPARK_LANE_AGENTS_NAME = ".agents/spark/AGENTS.md"
SPARK_LANE_SWARM_NAME = ".agents/spark/SWARM.md"
PROOF_TOPOLOGY_NAME = root_design_common_validator.PROOF_TOPOLOGY_NAME
AGENTS_DISTRICT_REQUIRED_TOKENS = (
    ".agents/<lane>/",
    "top-level `skills/`",
    "owner-admitted",
    ".agents/spark/",
    "Proof authority stays",
    "python scripts/validate_repo.py",
    "python scripts/validate_nested_agents.py",
)
SPARK_LANE_AGENTS_REQUIRED_TOKENS = (
    ".agents/spark/",
    "fast-loop lane",
    "one bounded claim",
    "Bundle-local `EVAL.md`",
    "eval.yaml",
    "generated/AGENTS.md",
    "python scripts/validate_nested_agents.py",
)
SPARK_LANE_SWARM_REQUIRED_TOKENS = (
    ".agents/spark/SWARM.md",
    "one bounded eval bundle",
    "Boundary Keeper",
    "repo validation",
    "build catalog",
    ".agents/spark/AGENTS.md#validation",
)
SPARK_LANE_DECISION_REQUIRED_TOKENS = (
    "Spark/",
    ".agents/spark/",
    ".agents/AGENTS.md",
    "does not let Spark",
    "does not make `.agents/` a doctrine center",
    "`Spark/` is absent",
)


def validate_agent_lane_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(repo_root, AGENTS_DISTRICT_NAME, AGENTS_DISTRICT_REQUIRED_TOKENS, issues)
    require_tokens(repo_root, SPARK_LANE_AGENTS_NAME, SPARK_LANE_AGENTS_REQUIRED_TOKENS, issues)
    require_tokens(repo_root, SPARK_LANE_SWARM_NAME, SPARK_LANE_SWARM_REQUIRED_TOKENS, issues)
    swarm_text = read_text_or_issue(repo_root / SPARK_LANE_SWARM_NAME, issues, root=repo_root)
    if swarm_text and markdown_python_commands(swarm_text):
        issues.append(
            ValidationIssue(
                SPARK_LANE_SWARM_NAME,
                "Spark SWARM context must route executable commands to .agents/spark/AGENTS.md instead of carrying python command lines",
            )
        )
    require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0017-spark-agent-lane-placement.md",
        SPARK_LANE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(repo_root, "README.md", (AGENTS_DISTRICT_NAME, SPARK_LANE_AGENTS_NAME), issues)
    require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (".agents/", ".agents/spark/", "Agent guidance"), issues)
    repo_skill_home = repo_root / "skills"
    repo_skill_projection = repo_root / ".agents" / "skills"
    if repo_skill_projection.exists() and not repo_skill_home.exists():
        issues.append(
            ValidationIssue(
                ".agents/skills/",
                "repo skill projection requires an owner-admitted top-level skills/ home",
            )
        )
    if (repo_root / "Spark").exists():
        issues.append(ValidationIssue("Spark/", "root-local Spark lane must stay moved to .agents/spark/"))
    return issues


__all__ = (
    "AGENTS_DISTRICT_NAME",
    "AGENTS_DISTRICT_REQUIRED_TOKENS",
    "SPARK_LANE_AGENTS_NAME",
    "SPARK_LANE_AGENTS_REQUIRED_TOKENS",
    "SPARK_LANE_DECISION_REQUIRED_TOKENS",
    "SPARK_LANE_SWARM_NAME",
    "SPARK_LANE_SWARM_REQUIRED_TOKENS",
    "validate_agent_lane_surfaces",
)
