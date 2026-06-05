"""Shared proof-loop validation helpers and path constants."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from validators.common import ValidationIssue, read_text_or_issue


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)

PROOF_INFRA_MECHANIC_README_NAME = "mechanics/proof-infra/README.md"
PROOF_LOOP_MECHANIC_README_NAME = "mechanics/proof-loop/README.md"
PROOF_LOOP_MECHANIC_AGENTS_NAME = "mechanics/proof-loop/AGENTS.md"
PROOF_LOOP_MECHANIC_PARTS_NAME = "mechanics/proof-loop/PARTS.md"
PROOF_LOOP_MECHANIC_PROVENANCE_NAME = "mechanics/proof-loop/PROVENANCE.md"
PROOF_LOOP_LEGACY_INDEX_NAME = "mechanics/proof-loop/legacy/INDEX.md"
PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME = "mechanics/proof-loop/legacy/DISTILLATION_LOG.md"
PROOF_LOOP_LEGACY_RAW_README_NAME = "mechanics/proof-loop/legacy/raw/README.md"
PROOF_LOOP_PARTS_README_NAME = "mechanics/proof-loop/parts/README.md"
PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME = "mechanics/proof-loop/parts/route-smoke/README.md"
PROOF_LOOP_SMOKE_REPORT_NAME = (
    "mechanics/proof-loop/parts/route-smoke/reports/"
    "proof-loop-local-route-smoke-v1.md"
)
PROOF_LOOP_SMOKE_DECISION_NAME = "docs/decisions/AOA-EV-D-0020-proof-loop-local-smoke-report.md"
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0030-proof-loop-route-smoke-part.md"
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0060-proof-loop-route-smoke-contract.md"
)
PROOF_LOOP_LOCAL_REPORT_NAME = (
    "evals/workflow/aoa-verification-honesty/reports/"
    "aoa-evals-slice-19-lifecycle-contract.report.json"
)
PROOF_LOOP_LOCAL_REPORT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0022-proof-loop-bundle-local-report.md"
)
PROOF_LOOP_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0019-proof-loop-mechanic-package.md"

PART_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$")
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


def markdown_heading_section(text: str, heading: str) -> str:
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


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    agents_path = repo_root / "mechanics" / match.group(1) / "AGENTS.md"
    if not agents_path.is_file():
        return ""
    return agents_path.read_text(encoding="utf-8")


def part_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = PART_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    parent_name, part_name = match.groups()
    part_relative = f"mechanics/{parent_name}/parts/{part_name}"
    validation_name = f"{part_relative}/VALIDATION.md"
    chunks: list[str] = []
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        chunks.append(validation_path.read_text(encoding="utf-8"))
    agents_path = repo_root / "mechanics" / parent_name / "parts" / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
        if child_section:
            chunks.append(child_section)
    return "\n\n".join(chunks)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    decision_index_text = ""
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        decision_index_text = "\n\n".join(index_texts)
    for token in tokens:
        search_text = text
        if decision_index_text:
            search_text = "\n\n".join((text, decision_index_text))
        if PART_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif MECHANIC_PARENT_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text
