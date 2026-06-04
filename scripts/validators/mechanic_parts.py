"""Mechanic part contract, payload, index, and validation-route guards."""

from __future__ import annotations

import re
import shlex
from pathlib import Path, PurePosixPath
from typing import Sequence

from validators import docs_decisions
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue


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
MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0087-mechanic-part-validation-command-reachability.md"
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0102-mechanic-part-validation-command-ownership.md"
)
MECHANIC_PART_VALIDATION_COMMAND_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command"
)
MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0088-mechanic-parts-index-synchronization.md"
)
MECHANIC_PARTS_INDEX_SYNC_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync"
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
)
MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Reachability",
    "`## Validation`",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "python command",
    "reachable path",
    "payload coverage anchor",
    "naked route-wide command",
    "stale validation path",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "mechanics/AGENTS.md#validation",
    "focused mechanic part validation-command guard",
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Ownership",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`mechanics/<parent>/parts/<part>/VALIDATION.md`",
    "`mechanics/<parent>/parts/AGENTS.md`",
    "mechanic index surfaces",
    "centralized child validation",
    "python command",
    "payload coverage anchor",
    "stale validation path",
    "Current Applicability",
    "Review Log",
    "validation route",
    "README files remain contract maps",
    "nearest `AGENTS.md`",
)
MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS = (
    "Mechanic PARTS Index Synchronization",
    "`mechanics/<parent>/PARTS.md`",
    "actual part directory",
    "declared part route",
    "stale local part route",
    "cross-parent reference",
    MECHANIC_PARTS_INDEX_SYNC_COMMAND,
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


def _require_tokens(
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
        for relative_path in docs_decisions.GENERATED_INDEX_PATHS:
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


def markdown_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug_compact_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def validate_mechanic_part_role_heading(
    *,
    path_name: str,
    text: str,
    parent_name: str,
    part_name: str,
    role_name: str,
    issues: list[ValidationIssue],
) -> None:
    heading = markdown_h1(text)
    heading_compact = slug_compact_token(heading)
    missing: list[str] = []
    if slug_compact_token(parent_name) not in heading_compact:
        missing.append("parent mechanic")
    if slug_compact_token(part_name) not in heading_compact:
        missing.append("local role token")
    if role_name.lower() not in heading.lower():
        missing.append(role_name)
    if " / " not in heading:
        missing.append("Parent / Part heading shape")
    if missing:
        issues.append(
            ValidationIssue(
                path_name,
                "mechanic route H1 must name parent mechanic, local role token, and role; missing "
                + ", ".join(missing),
            )
        )


def validate_mechanic_index_surface_roles(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        validate_mechanic_part_role_heading(
            path_name=parts_index_name,
            text=parts_index_text,
            parent_name=parent_name,
            part_name="part",
            role_name="Index",
            issues=issues,
        )

        parts_route_name = f"mechanics/{parent_name}/parts/README.md"
        parts_route_path = repo_root / parts_route_name
        if parts_route_path.is_file():
            parts_route_text = read_text_or_issue(
                parts_route_path,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=parts_route_name,
                text=parts_route_text,
                parent_name=parent_name,
                part_name="parts",
                role_name="Route",
                issues=issues,
            )

    return issues


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


def mechanic_part_validation_block(readme_text: str) -> str:
    return markdown_heading_section(readme_text, "Validation")


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


SOURCE_SURFACE_CODE_REF_RE = re.compile(r"`([^`\n]+)`")
SOURCE_SURFACE_FILE_REF_RE = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9_.-]*$")


def mechanic_part_source_surface_refs(readme_text: str) -> list[str]:
    section = markdown_heading_section(readme_text, "Source Surfaces")
    refs: list[str] = []
    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(section):
        ref = match.group(1).strip()
        if not ref:
            continue
        if source_surface_ref_is_path_like(ref):
            refs.append(ref)
    return list(dict.fromkeys(refs))


def source_surface_ref_is_path_like(ref: str) -> bool:
    return (
        ref.startswith(("repo:", ".", "/"))
        or "/" in ref
        or "*" in ref
        or "?" in ref
        or "[" in ref
        or SOURCE_SURFACE_FILE_REF_RE.search(ref) is not None
    )


def source_surface_ref_resolution_issue(repo_root: Path, ref: str) -> str | None:
    if ref.startswith("repo:"):
        return None
    if ref.startswith(("http://", "https://")):
        return None
    if ref.startswith("/"):
        return "source surface ref must be repo-relative or repo-qualified, not absolute"
    if ".." in PurePosixPath(ref).parts:
        return "source surface ref must not traverse outside the repository"
    if "<" in ref or ">" in ref:
        return None

    if any(char in ref for char in "*?["):
        if any(repo_root.glob(ref)):
            return None
        return "stale source surface ref must resolve as a repo-relative glob"

    if (repo_root / ref.rstrip("/")).exists():
        return None
    return "stale source surface ref must resolve as a repo-relative path"


MECHANIC_PART_SLUG_PATTERN = r"[a-z0-9][a-z0-9_.-]+"


def mechanic_parts_index_declared_slugs(
    parts_index_text: str,
    parent_name: str,
) -> set[str]:
    declared: set[str] = set()

    full_path_pattern = re.compile(
        rf"mechanics/{re.escape(parent_name)}/parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)"
    )
    declared.update(full_path_pattern.findall(parts_index_text))

    relative_path_pattern = re.compile(
        rf"(?:^|[^A-Za-z0-9_./-])parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)",
        re.MULTILINE,
    )
    declared.update(relative_path_pattern.findall(parts_index_text))

    heading_pattern = re.compile(
        rf"^###\s+`?({MECHANIC_PART_SLUG_PATTERN})`?\s*$",
        re.MULTILINE,
    )
    declared.update(heading_pattern.findall(parts_index_text))

    lines = parts_index_text.splitlines()
    index = 0
    while index < len(lines) - 1:
        line = lines[index].strip()
        next_line = lines[index + 1].strip()
        if line.startswith("|") and next_line.startswith("|"):
            header_cells = [cell.strip().lower() for cell in line.strip("|").split("|")]
            separator_cells = [
                cell.strip().replace(" ", "")
                for cell in next_line.strip("|").split("|")
            ]
            is_separator = bool(separator_cells) and all(
                set(cell) <= {"-", ":"} and "-" in cell for cell in separator_cells
            )
            if header_cells and "part" in header_cells[0] and is_separator:
                row_index = index + 2
                while row_index < len(lines) and lines[row_index].strip().startswith("|"):
                    first_cell = lines[row_index].strip().strip("|").split("|")[0]
                    declared.update(
                        re.findall(rf"`({MECHANIC_PART_SLUG_PATTERN})`", first_cell)
                    )
                    row_index += 1
                index = row_index
                continue
        index += 1

    return declared


def validation_command_referenced_paths(command: str) -> tuple[list[str], str | None]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return [], f"validation command cannot be parsed: {exc}"

    if not parts:
        return [], None

    paths: list[str] = []
    if (
        len(parts) > 3
        and parts[1] == "-m"
        and parts[2] == "pytest"
    ):
        for token in parts[3:]:
            if token.startswith("-") or token in {"and", "|"}:
                continue
            if token.endswith(".py") or "/" in token:
                paths.append(token.split("::", 1)[0])
        return paths, None

    if len(parts) > 1:
        first_arg = parts[1]
        if first_arg.endswith(".py") or "/" in first_arg:
            paths.append(first_arg)
    return paths, None


def part_payload_directories(part_root: Path) -> list[Path]:
    return [
        child
        for child in sorted(part_root.iterdir(), key=lambda item: item.name)
        if child.is_dir() and child.name in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS
    ]


def validation_section_has_payload_coverage_anchor(
    part_relative: str,
    validation_section: str,
    commands: Sequence[str],
) -> bool:
    part_prefix = f"{part_relative.rstrip('/')}/"
    if any(part_prefix in command for command in commands):
        return True
    if any("scripts/validate_repo.py --eval " in command for command in commands):
        return True

    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(validation_section):
        ref = match.group(1).strip().rstrip("/")
        if ref == part_relative or ref.startswith(part_prefix):
            return True
    return False


PART_README_PATH_RE = re.compile(
    r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$"
)
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


def part_readme_path_name(path_name: str) -> bool:
    return PART_README_PATH_RE.match(path_name) is not None


def mechanic_parent_readme_path_name(path_name: str) -> bool:
    return MECHANIC_PARENT_README_PATH_RE.match(path_name) is not None


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""

    parent_name = match.group(1)
    agents_path = repo_root / "mechanics" / parent_name / "AGENTS.md"
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


def mechanic_part_validation_sources(
    repo_root: Path,
    parent_name: str,
    part_root: Path,
    readme_name: str,
    readme_text: str,
    issues: list[ValidationIssue],
) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []

    readme_section = mechanic_part_validation_block(readme_text)
    sources.append((readme_name, readme_section))

    part_relative = part_root.relative_to(repo_root).as_posix()
    validation_name = f"{part_relative}/VALIDATION.md"
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        validation_text = read_text_or_issue(validation_path, issues, root=repo_root)
        if validation_text:
            sources.append((validation_name, validation_text))
    else:
        issues.append(
            ValidationIssue(
                validation_name,
                "part validation route marker is missing",
            )
        )

    parts_agents_name = f"mechanics/{parent_name}/parts/AGENTS.md"
    parts_agents_path = repo_root / parts_agents_name
    if parts_agents_path.is_file():
        agents_text = read_text_or_issue(parts_agents_path, issues, root=repo_root)
        if agents_text:
            child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
            if child_section:
                sources.append((parts_agents_name, child_section))
            else:
                issues.append(
                    ValidationIssue(
                        parts_agents_name,
                        f"missing centralized child validation block for `{validation_name}`",
                    )
                )
    else:
        issues.append(
            ValidationIssue(
                parts_agents_name,
                "parent parts AGENTS validation lane is missing",
            )
        )

    return sources


def validate_mechanic_part_readme_contract_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}/parts",
                    "active mechanic parent must expose a parts/ directory",
                )
            )
            continue

        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )

        for path in sorted(parts_root.iterdir(), key=lambda item: item.name):
            relative = path.relative_to(repo_root).as_posix()
            if path.is_file():
                if path.name not in {"AGENTS.md", "README.md"}:
                    issues.append(
                        ValidationIssue(
                            relative,
                            "unexpected mechanics parts root file must be a route README or a part directory",
                        )
                    )
                continue
            if not path.is_dir():
                issues.append(
                    ValidationIssue(
                        relative,
                        "unexpected mechanics parts root entry must be a part directory",
                    )
                )
                continue

            readme_name = f"{relative}/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=readme_name,
                text=readme_text,
                parent_name=parent_name,
                part_name=path.name,
                role_name="Part",
                issues=issues,
            )
            validation_name = f"{relative}/VALIDATION.md"
            validation_path = repo_root / validation_name
            if validation_path.is_file():
                validation_text = read_text_or_issue(
                    validation_path,
                    issues,
                    root=repo_root,
                )
                validate_mechanic_part_role_heading(
                    path_name=validation_name,
                    text=validation_text,
                    parent_name=parent_name,
                    part_name=path.name,
                    role_name="Validation",
                    issues=issues,
                )
            part_route_text = "\n\n".join(
                (
                    readme_text,
                    part_validation_route_text(repo_root, readme_name),
                )
            )
            route_tokens = (
                readme_name,
                f"parts/{path.name}/README.md",
                f"`{path.name}`",
            )
            if parts_index_text and not any(token in parts_index_text for token in route_tokens):
                issues.append(
                    ValidationIssue(
                        parts_index_name,
                        f"parent PARTS.md must route concrete part `{readme_name}` by README path or exact part slug",
                    )
                )
            _require_tokens(
                repo_root=repo_root,
                path_name=readme_name,
                tokens=MECHANIC_PART_README_REQUIRED_TOKENS,
                issues=issues,
            )
            for stale_lead_in in MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS:
                if readme_text and stale_lead_in in readme_text:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            "mechanic part README must introduce Stop-Lines as a local proof-operation boundary, not the old part-claim scaffold",
                        )
                    )
            source_refs = mechanic_part_source_surface_refs(readme_text)
            if readme_text and "## Source Surfaces" in readme_text and not source_refs:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part README Source Surfaces must name at least one path-like source ref",
                    )
                )
            for ref in source_refs:
                ref_issue = source_surface_ref_resolution_issue(repo_root, ref)
                if ref_issue is not None:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            f"{ref_issue}: `{ref}`",
                        )
                    )
            payload_dir_count = 0
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                child_relative = child.relative_to(repo_root).as_posix()
                if child.is_file():
                    if child.name not in {"AGENTS.md", "README.md", "VALIDATION.md"}:
                        issues.append(
                            ValidationIssue(
                                child_relative,
                                "unexpected part-root file must move under a payload subdirectory or be routed by the part contract",
                            )
                        )
                    continue
                if not child.is_dir():
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected part-root entry must be a payload subdirectory",
                        )
                    )
                    continue
                if child.name not in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS:
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected payload class directory under mechanic part",
                        )
                    )
                    continue
                payload_dir_count += 1
                if not any(child.iterdir()):
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "empty payload subdirectory under mechanic part",
                        )
                    )
                    continue
                if part_route_text:
                    payload_tokens = (
                        f"{child.name}/",
                        f"`{child.name}`",
                        child_relative,
                    )
                    if not any(token in part_route_text for token in payload_tokens):
                        issues.append(
                            ValidationIssue(
                                readme_name,
                                f"part README must route payload subdirectory `{child.name}/`",
                            )
                        )
            if payload_dir_count == 0 and readme_text:
                missing_thin_tokens = [
                    token
                    for token in MECHANIC_THIN_PART_REQUIRED_TOKENS
                    if token not in readme_text
                ]
                if missing_thin_tokens:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            "mechanic part with no payload subdirectories must "
                            "declare an eval-backed thin support route; missing "
                            + ", ".join(repr(token) for token in missing_thin_tokens),
                        )
                    )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        tokens=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    payload_decision_text = read_text_or_issue(
        repo_root / MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if payload_decision_text and markdown_python_commands(
        markdown_heading_section(payload_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
            "Mechanic Part Payload Inventory",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload subdirectory", "mechanic part"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("payload subdirectory", "unexpected payload class"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
            "Mechanic Part Source Surface Reference Guard",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Source Surfaces", "stale source surface ref"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "repo-relative path"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
            "Mechanic Part Source Surfaces Section Contract",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("## Source Surfaces", "at least one path-like source ref"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "plural section"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_parts_index_sync_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            continue

        actual_parts = {
            path.name
            for path in parts_root.iterdir()
            if path.is_dir()
        }
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        if not parts_index_text:
            continue

        declared_parts = mechanic_parts_index_declared_slugs(
            parts_index_text,
            parent_name,
        )
        for part_name in sorted(actual_parts - declared_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md must declare actual part directory `{part_name}` as a local part route",
                )
            )
        for part_name in sorted(declared_parts - actual_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md declares stale local part route `{part_name}` with no matching actual part directory",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
        tokens=MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
            "Mechanic PARTS Index Synchronization",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("declared part route", "stale local part route"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("actual part directory", "cross-parent reference"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_part_validation_command_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parts_root = repo_root / "mechanics" / parent_name / "parts"
        if not parts_root.is_dir():
            continue

        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            if not part_root.is_dir():
                continue
            readme_name = part_root.relative_to(repo_root).as_posix() + "/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            if not readme_text:
                continue

            sources = mechanic_part_validation_sources(
                repo_root,
                parent_name,
                part_root,
                readme_name,
                readme_text,
                issues,
            )
            readme_validation_section = mechanic_part_validation_block(readme_text)
            readme_commands = markdown_python_commands(readme_validation_section)
            if readme_commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part README validation section must route executable commands to VALIDATION.md or parent parts/AGENTS.md instead of carrying python command blocks",
                    )
                )

            command_locations: dict[str, str] = {}
            commands: list[str] = []
            for location, source_text in sources:
                for command in markdown_python_commands(source_text):
                    if command in command_locations:
                        continue
                    command_locations[command] = location
                    commands.append(command)

            if not commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must list at least one python command",
                    )
                )
                continue

            part_relative = part_root.relative_to(repo_root).as_posix()
            combined_validation_route = "\n\n".join(source_text for _, source_text in sources)
            if part_payload_directories(part_root) and not validation_section_has_payload_coverage_anchor(
                part_relative,
                combined_validation_route,
                commands,
            ):
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must include a payload coverage anchor, such as a part-local path or specific `python scripts/validate_repo.py --eval ...`; route-wide commands need a part-local or bundle-specific anchor for parts with payload",
                    )
                )

            for command in commands:
                command_location = command_locations.get(command, readme_name)
                command_paths, parse_issue = validation_command_referenced_paths(command)
                if parse_issue:
                    issues.append(ValidationIssue(command_location, parse_issue))
                    continue
                for command_path in command_paths:
                    if any(token in command_path for token in ("*", "?", "[")):
                        continue
                    if command_path.startswith("/"):
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"validation command must use repo-relative path, not absolute path `{command_path}`",
                            )
                        )
                        continue
                    if not (repo_root / command_path).exists():
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"part validation command has stale validation path `{command_path}`",
                            )
                        )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        tokens=MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    validation_command_decision_text = read_text_or_issue(
        repo_root / MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if validation_command_decision_text and markdown_python_commands(
        markdown_heading_section(validation_command_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
        tokens=MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
            MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
            "Mechanic Part Validation Command Reachability",
            "Mechanic Part Validation Command Ownership",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload coverage anchor", "stale validation path"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("part validation route", "payload coverage anchor"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues



def validate_mechanic_part_contract_index_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name in MECHANIC_PART_CONTRACT_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PART_CONTRACT_REQUIRED_TOKENS,
            issues=issues,
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_README_CONTRACT_DECISION_NAME,
        tokens=MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PART_README_CONTRACT_DECISION_NAME,
            "Mechanic Part README Contract",
        ),
        issues=issues,
    )
    return issues


def validate_mechanic_part_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanic_part_contract_index_surfaces(repo_root))
    issues.extend(validate_mechanic_part_readme_contract_surfaces(repo_root))
    issues.extend(validate_mechanic_parts_index_sync_surfaces(repo_root))
    issues.extend(validate_mechanic_part_validation_command_surfaces(repo_root))
    return issues
