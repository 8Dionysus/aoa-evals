"""Root design validator shared paths and token loader."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue


ROADMAP_NAME = "ROADMAP.md"
DESIGN_NAME = "DESIGN.md"
DESIGN_AGENTS_NAME = "DESIGN.AGENTS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"


def require_tokens(
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
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


__all__ = (
    "ROADMAP_NAME",
    "DESIGN_NAME",
    "DESIGN_AGENTS_NAME",
    "PROOF_TOPOLOGY_NAME",
    "ROUTE_RESIDUE_GUARDS_NAME",
    "DECISION_RECORDS_README_NAME",
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "require_tokens",
)
