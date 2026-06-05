"""Shared helpers for mechanic parent validators."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text

    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    if path_name == PROOF_TOPOLOGY_NAME:
        route_guard_path = repo_root / ROUTE_RESIDUE_GUARDS_NAME
        if route_guard_path.is_file():
            companion_texts.append(route_guard_path.read_text(encoding="utf-8"))

    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))
    return text


def markdown_python_commands(section: str) -> list[str]:
    commands: list[str] = []
    commands.extend(re.findall(r"`(python3? [^`]+)`", section))
    in_fence = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped.startswith("python ") or stripped.startswith("python3 "):
            commands.append(stripped)
    return list(dict.fromkeys(commands))


__all__ = (
    "DECISION_RECORDS_README_NAME",
    "MECHANICS_README_NAME",
    "MECHANICS_AGENTS_NAME",
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "PROOF_TOPOLOGY_NAME",
    "ROUTE_RESIDUE_GUARDS_NAME",
    "LEGACY_NAMING_NAME",
    "ROADMAP_NAME",
    "require_tokens",
    "markdown_python_commands",
)
