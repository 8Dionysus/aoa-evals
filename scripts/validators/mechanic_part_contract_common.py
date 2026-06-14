"""Shared mechanic part contract constants and helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators import decision_index_paths
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_validation_common import (
    MECHANIC_PARENT_README_PATH_RE,
    PART_README_PATH_RE,
    markdown_heading_section,
    markdown_python_commands,
    mechanic_parent_readme_path_name,
    mechanic_parent_validation_route_text,
    part_readme_path_name,
    part_validation_route_text,
)


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
ROADMAP_NAME = "ROADMAP.md"
ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS = (
    "Mechanic lower index",
    "DIRECTION.md",
    "part/payload source surfaces",
    "parts index synchronization",
    "payload coverage",
)

MECHANIC_PART_CONTRACT_FILES = tuple(
    f"mechanics/{parent_name}/PARTS.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PART_CONTRACT_REQUIRED_TOKENS = (
    "## Part Contract",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
)
MECHANIC_PART_README_REQUIRED_TOKENS = (
    "## Source Surfaces",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
MECHANIC_PART_README_STOP_LINE_LEAD_IN = (
    "Boundary: this part supports its local proof operation. These claims stay outside\n"
    "the part:"
)
MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS = (
    "This part must not claim:",
    "Do not use this part to claim:",
)
MECHANIC_PART_README_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0074-mechanic-part-readme-contract.md"
)
MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0086-mechanic-part-payload-inventory.md"
)
MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory"
)
MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0094-mechanic-part-source-surface-reference-guard.md"
)
MECHANIC_PART_SOURCE_SURFACE_REF_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_source_surface"
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0095-mechanic-part-source-surfaces-section-contract.md"
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_source_surfaces_section"
)
MECHANIC_PART_ALLOWED_PAYLOAD_DIRS = (
    "config",
    "docs",
    "examples",
    "fixtures",
    "generated",
    "manifests",
    "reports",
    "runners",
    "schemas",
    "scorers",
    "scripts",
    "seeds",
    "templates",
    "tests",
)
MECHANIC_THIN_PART_REQUIRED_TOKENS = (
    "eval-backed thin support route",
    "payload subdirectories are absent by design",
    "source eval package stays under `evals/`",
)
MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part README Contract",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`## Source Surfaces`",
    "`## Inputs`",
    "`## Outputs`",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "`## Validation`",
    "parent `PARTS.md`",
    "orphan part",
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
)
MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Payload Inventory",
    "`mechanics/<parent>/parts/<part>/`",
    "payload subdirectory",
    "eval-backed thin support route",
    "part README",
    "unexpected payload class",
    "empty payload subdirectory",
    "unexpected part-root file",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "mechanics/AGENTS.md#validation",
    "focused mechanic part payload-inventory guard",
    MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
)
MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Source Surface Reference Guard",
    "`## Source Surfaces`",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "repo-relative path",
    "repo-qualified sibling ref",
    "placeholder route",
    "stale source surface ref",
    MECHANIC_PART_SOURCE_SURFACE_REF_COMMAND,
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Source Surfaces Section Contract",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`## Source Surfaces`",
    "at least one path-like source ref",
    "plural section",
    "not `## Source Surface`",
    "not `## Active Surfaces`",
    MECHANIC_PART_SOURCE_SURFACES_SECTION_COMMAND,
)


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

    for token in tokens:
        search_text = text
        if companion_texts:
            search_text = "\n\n".join((search_text, *companion_texts))
        if part_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif mechanic_parent_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))
    return text


def markdown_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug_compact_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if cells[0] == "Parent":
            continue
        if all(set(cell.replace(" ", "")) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    return rows


_require_tokens = require_tokens


__all__ = (
    "DECISION_RECORDS_README_NAME",
    "MECHANICS_README_NAME",
    "MECHANICS_AGENTS_NAME",
    "PROOF_TOPOLOGY_NAME",
    "ROUTE_RESIDUE_GUARDS_NAME",
    "ROADMAP_NAME",
    "ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS",
    "MECHANIC_PART_CONTRACT_FILES",
    "MECHANIC_PART_CONTRACT_REQUIRED_TOKENS",
    "MECHANIC_PART_README_REQUIRED_TOKENS",
    "MECHANIC_PART_README_STOP_LINE_LEAD_IN",
    "MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS",
    "MECHANIC_PART_README_CONTRACT_DECISION_NAME",
    "MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME",
    "MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND",
    "MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME",
    "MECHANIC_PART_SOURCE_SURFACE_REF_COMMAND",
    "MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME",
    "MECHANIC_PART_SOURCE_SURFACES_SECTION_COMMAND",
    "MECHANIC_PART_ALLOWED_PAYLOAD_DIRS",
    "MECHANIC_THIN_PART_REQUIRED_TOKENS",
    "MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS",
    "require_tokens",
    "_require_tokens",
    "markdown_heading_section",
    "markdown_h1",
    "markdown_table_rows",
    "markdown_python_commands",
    "slug_compact_token",
    "mechanic_parent_validation_route_text",
    "part_validation_route_text",
    "PART_README_PATH_RE",
    "MECHANIC_PARENT_README_PATH_RE",
    "part_readme_path_name",
    "mechanic_parent_readme_path_name",
)
