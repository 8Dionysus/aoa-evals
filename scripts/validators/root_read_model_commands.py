"""Root read-model command ownership contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.root_common import markdown_python_commands


READ_MODEL_COMMAND_OWNER_PATHS = (
    ".github/pull_request_template.md",
    "CONTRIBUTING.md",
    "EVAL_SELECTION.md",
    "README.md",
    "ROADMAP.md",
    "AUDIT.md",
    "docs/README.md",
    "docs/architecture/AGENT_INDEX.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "docs/architecture/LEGACY_NAMING.md",
    "docs/operations/RELEASING.md",
    "docs/guides/REGRESSION_PROOF_SURFACES.md",
    "evals/README.md",
    "generated/README.md",
    "quests/README.md",
    "quests/LIFECYCLE.md",
    "mechanics/README.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
)


def validate_read_model_command_ownership(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in READ_MODEL_COMMAND_OWNER_PATHS:
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if not text:
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "guidance surface must route executable validation commands to the nearest AGENTS.md instead of carrying python command lines",
                )
            )

    return issues


__all__ = (
    "READ_MODEL_COMMAND_OWNER_PATHS",
    "validate_read_model_command_ownership",
)
