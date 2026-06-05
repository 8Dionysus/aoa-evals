"""Shared mechanics topology validator helpers."""

from __future__ import annotations

import re
from pathlib import Path

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue

MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
MECHANICS_EVIDENCE_CLUSTERS = Path(MECHANICS_EVIDENCE_CLUSTERS_NAME)
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROADMAP_NAME = "ROADMAP.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS = (
    "Mechanics evidence",
    "parent evidence",
    "root district posture",
    "residual root-authored surface classification",
)


def _markdown_heading_section(text: str, heading: str) -> str:
    marker = ""
    heading_level = 0
    start = -1
    for level in (3, 2):
        pattern = re.compile(rf"(?m)^{'#' * level} {re.escape(heading)}\s*$")
        match = pattern.search(text)
        if match:
            marker = match.group(0)
            heading_level = level
            start = match.start()
            break
    if start == -1:
        return ""
    next_h2 = text.find("\n## ", start + len(marker))
    next_h3 = text.find("\n### ", start + len(marker)) if heading_level > 2 else -1
    candidates = [index for index in (next_h2, next_h3) if index != -1]
    end = min(candidates) if candidates else len(text)
    return text[start:end]


def _markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows


def _require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: tuple[str, ...],
    issues: list[ValidationIssue],
) -> None:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return
    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))




__all__ = (
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "MECHANICS_EVIDENCE_CLUSTERS",
    "MECHANICS_README_NAME",
    "MECHANICS_AGENTS_NAME",
    "PROOF_TOPOLOGY_NAME",
    "ROADMAP_NAME",
    "DECISION_RECORDS_README_NAME",
    "ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS",
    "_markdown_heading_section",
    "_markdown_table_rows",
    "_require_tokens",
)
