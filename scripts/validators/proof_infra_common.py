"""Shared helpers for proof-infra validators."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue

SOURCE_EVALS_DIR_NAME = "evals"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"

SHARED_PROOF_INFRA_GUIDE_NAME = "docs/guides/SHARED_PROOF_INFRA_GUIDE.md"
PROOF_INFRA_MECHANIC_README_NAME = "mechanics/proof-infra/README.md"
PROOF_INFRA_MECHANIC_AGENTS_NAME = "mechanics/proof-infra/AGENTS.md"
PROOF_INFRA_MECHANIC_PARTS_NAME = "mechanics/proof-infra/PARTS.md"
PROOF_INFRA_FIXTURE_FAMILIES_README_NAME = (
    "mechanics/proof-infra/parts/fixture-families/README.md"
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME = (
    "mechanics/proof-infra/parts/fixture-families/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/README.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py"
)
FIXTURE_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json"
)
RUNNER_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json"
)
REPORT_SUMMARY_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json"
)
PROOF_INFRA_PROVENANCE_NAME = "mechanics/proof-infra/PROVENANCE.md"
PROOF_INFRA_LEGACY_INDEX_NAME = "mechanics/proof-infra/legacy/INDEX.md"
PROOF_INFRA_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0012-proof-infra-mechanic-package.md"
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0041-proof-infra-fixture-families.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0049-proof-infra-reportable-contracts.md"
)

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
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
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


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return {}

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_dirs.setdefault(eval_dir.name, eval_dir)
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    return discover_eval_dirs(repo_root).get(
        eval_name,
        repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
    )
