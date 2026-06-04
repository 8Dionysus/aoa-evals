"""Route residue guards for source, generated, config, and mechanic payloads."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import eval_catalog_contract

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue, relative_location
from validators.root_route_cards import ROOT_ROUTE_CARD_ONLY_DISTRICTS


SOURCE_EVALS_DIR_NAME = "evals"
MECHANICS_README_NAME = "mechanics/README.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"

GENERATED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0073-generated-route-residue-guard.md"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0076-active-mechanic-route-residue-guard.md"
)
ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0077-root-authored-route-residue-guard.md"
)
DECISION_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0078-decision-route-residue-guard.md"
)
REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0079-repo-config-route-residue-guard.md"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0080-source-bundle-route-residue-guard.md"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0081-mechanic-payload-route-residue-guard.md"
)

GENERATED_READER_INDEX_REQUIRED_TOKENS = (
    "# Generated Reader Index",
    "repo-wide derived reader surfaces",
    "authored source ownership",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.example.json",
    "source owner surface",
    'Source surfaces answer\n"what is true?"',
)
GENERATED_AGENTS_REQUIRED_TOKENS = (
    "repo-wide derived reader surfaces only",
    "Authored source surfaces keep doctrine",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "generated/quest_catalog.min.example.json",
    "generated/quest_dispatch.min.example.json",
)
GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Generated Route Residue Guard",
    "structured references",
    "route-card-only root district",
    "part-local generated readers",
    "content_markdown",
    "python -m pytest -q tests/test_generated_route_residue.py",
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k active_mechanic_route_residue"
)
ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k root_authored_route_residue"
)
DECISION_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k decision_route_residue"
)
REPO_CONFIG_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k repo_config_route_residue"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k source_bundle_route_residue"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k mechanic_payload_route_residue"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Active Mechanic Route Residue Guard",
    "authored mechanics route cards",
    "route-card-only root district",
    "same part root",
    "`evals/<family>/<eval>/...`",
    "legacy parent route",
    ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
)
ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Root Authored Route Residue Guard",
    "root-facing authored surfaces",
    "route-card-only root district",
    "docs/decisions/",
    "historical context",
    "`evals/<family>/<eval>/...`",
    ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
)
DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Decision Route Residue Guard",
    "decision records",
    "historical context",
    "route-card-only root district",
    "`evals/<family>/<eval>/...`",
    "active `mechanics/...`",
    DECISION_ROUTE_RESIDUE_COMMAND,
)
REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Repo Config Route Residue Guard",
    ".gitignore",
    ".github/workflows/",
    "legacy mechanic parent",
    "route-card-only root district",
    "not historical memory",
    REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
)
SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Source Bundle Route Residue Guard",
    "source proof objects",
    "bundle-local path",
    "repo-qualified sibling",
    "legacy mechanic parent",
    "route-card-only root district",
    SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Payload Route Residue Guard",
    "active mechanics payload",
    "part-local path",
    "repo-qualified sibling",
    "legacy mechanic parent",
    "route-card-only root district",
    "structured manifest route fields",
    "root-authored docs globs",
    MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
)
ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS = (
    "Route residue guard family",
    "generated/readout, active mechanic, root-authored, decision, repo-config, source-bundle, and mechanic-payload residue guards",
    "owner contracts",
)

GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES = tuple(
    f"mechanics/{wrong_parent}/"
    for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES = tuple(
    f"mechanics/{wrong_parent}"
    for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES = tuple(
    f"{district_name}/" for district_name in ROOT_ROUTE_CARD_ONLY_DISTRICTS
)
GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES = tuple(ROOT_ROUTE_CARD_ONLY_DISTRICTS)
GENERATED_ROUTE_RESIDUE_SKIP_KEYS = frozenset({"content_markdown"})
ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>(?:"
    + "|".join(re.escape(district) for district in ROOT_ROUTE_CARD_ONLY_DISTRICTS)
    + r")(?:/[A-Za-z0-9._*<>-]+)+/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>mechanics/(?:"
    + "|".join(
        re.escape(wrong_parent)
        for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
    )
    + r")(?:/[A-Za-z0-9._*<>-]+)*/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_TOKEN_STRIP_CHARS = "`.,;:)]}\"'"
ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES = (
    ".agents/spark/SWARM.md",
    "AGENTS.md",
    "AUDIT.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "DESIGN.AGENTS.md",
    "DESIGN.md",
    "EVAL_INDEX.md",
    "EVAL_SELECTION.md",
    "QUESTBOOK.md",
    "README.md",
    "ROADMAP.md",
    "evals/AGENTS.md",
)
ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    "Former root",
    "former root",
    "historical root",
    "Do not recreate",
    "compatibility route card",
    "mapped through",
    "route-card",
    "route card",
)
DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    *ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS,
    "legacy",
    "provenance",
    "old root",
    "previous root",
    "stale authored path example",
)
SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES = frozenset(
    {".json", ".md", ".txt", ".yaml", ".yml"}
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_SUFFIXES = frozenset(
    {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_ROUTE_CARD_NAMES = frozenset(
    {"AGENTS.md", "PARTS.md", "PROVENANCE.md", "README.md"}
)
MECHANIC_MANIFEST_STRUCTURED_ROUTE_KEYS = frozenset(
    {
        "generated_surfaces",
        "observed_surfaces",
        "proof_surfaces",
        "source_files",
        "source_surfaces",
        "validation_surfaces",
    }
)


@dataclass(frozen=True)
class RouteResidueContext:
    require_tokens: Callable[[Path, str, Iterable[str], list[ValidationIssue]], str]


def iter_generated_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    generated_root = repo_root / "generated"
    if generated_root.is_dir():
        paths.update(path for path in generated_root.glob("*.json") if path.is_file())
    mechanics_root = repo_root / "mechanics"
    if mechanics_root.is_dir():
        paths.update(
            path
            for path in mechanics_root.rglob("generated/*.json")
            if path.is_file()
        )
    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def format_generated_json_location(file_location: str, json_path: Sequence[str | int]) -> str:
    suffix = ""
    for part in json_path:
        if isinstance(part, int):
            suffix += f"[{part}]"
        else:
            suffix += f".{part}"
    return f"{file_location}{suffix}"


def mechanic_part_root_for_generated_json(path: Path, repo_root: Path) -> Path | None:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return None
    if len(parts) < 6:
        return None
    if parts[0] != "mechanics" or parts[2] != "parts" or parts[4] != "generated":
        return None
    return repo_root.joinpath(*parts[:4])


def generated_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = value.strip().replace("\\", "/")
    if not normalized or normalized.startswith("repo:"):
        return None

    for exact_route in GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{exact_route}'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{prefix}'"
            )

    part_root = mechanic_part_root_for_generated_json(source_file, repo_root)
    if part_root is not None and (part_root / normalized).exists():
        return None

    for exact_route in GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{exact_route}/'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{prefix}'"
            )

    return None


def validate_generated_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def walk_json(
        value: Any,
        *,
        source_file: Path,
        file_location: str,
        json_path: list[str | int],
    ) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in GENERATED_ROUTE_RESIDUE_SKIP_KEYS:
                    continue
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, key],
                )
            return
        if isinstance(value, list):
            for index, child in enumerate(value):
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, index],
                )
            return
        if not isinstance(value, str):
            return

        message = generated_route_residue_message(
            value,
            source_file=source_file,
            repo_root=repo_root,
        )
        if message is not None:
            issues.append(
                ValidationIssue(
                    format_generated_json_location(file_location, json_path),
                    message,
                )
            )

    for path in iter_generated_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in contract_issues
        )
        if payload is None:
            continue
        walk_json(payload, source_file=path, file_location=file_location, json_path=[])

    return issues


def validate_generated_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_generated_route_residue(repo_root)
    for path_name, tokens in (
        ("generated/README.md", GENERATED_READER_INDEX_REQUIRED_TOKENS),
        ("generated/AGENTS.md", GENERATED_AGENTS_REQUIRED_TOKENS),
        (GENERATED_ROUTE_RESIDUE_DECISION_NAME, GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (GENERATED_ROUTE_RESIDUE_DECISION_NAME, "Generated Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Generated route residue", "same part root")),
        (LEGACY_NAMING_NAME, ("generated/readout JSON", "same part")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_active_mechanic_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    mechanics_readme = repo_root / MECHANICS_README_NAME
    if mechanics_readme.is_file():
        paths.add(mechanics_readme)

    mechanics_root = repo_root / "mechanics"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = mechanics_root / parent_name
        for route_card_name in ("AGENTS.md", "README.md", "PARTS.md"):
            route_card = parent_root / route_card_name
            if route_card.is_file():
                paths.add(route_card)

        parts_root = parent_root / "parts"
        parts_readme = parts_root / "README.md"
        if parts_readme.is_file():
            paths.add(parts_readme)
        if not parts_root.is_dir():
            continue
        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            part_readme = part_root / "README.md"
            if part_readme.is_file():
                paths.add(part_readme)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def mechanic_owner_root_for_route_card(path: Path, repo_root: Path) -> Path:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return repo_root / "mechanics"

    if len(parts) >= 5 and parts[0] == "mechanics" and parts[2] == "parts":
        return repo_root.joinpath(*parts[:4])
    if len(parts) >= 2 and parts[0] == "mechanics":
        return repo_root.joinpath(*parts[:2])
    return repo_root / "mechanics"


def normalize_active_mechanic_route_token(token: str) -> str:
    normalized = token.strip().replace("\\", "/")
    normalized = normalized.strip(ACTIVE_MECHANIC_ROUTE_RESIDUE_TOKEN_STRIP_CHARS)
    return normalized.rstrip("/")


def root_route_card_reference_is_allowed(normalized: str) -> bool:
    if "/" not in normalized:
        return True
    district_name, remainder = normalized.split("/", 1)
    if district_name not in ROOT_ROUTE_CARD_ONLY_DISTRICTS:
        return False
    if not remainder:
        return True
    return remainder in ROOT_ROUTE_CARD_ONLY_DISTRICTS[district_name]


def active_mechanic_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None

    owner_root = mechanic_owner_root_for_route_card(source_file, repo_root)
    if (owner_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "active mechanic route card must not point at route-card-only root "
        f"district payload '{normalized}'; use a part-local path under the "
        f"same part root, a bundle-local `evals/<family>/<eval>/...` path, or the "
        f"root route card '{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def active_mechanic_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "active mechanic route card must use the active mechanic parent "
                f"`mechanics/{correct_route}/`, not legacy parent route "
                f"`{wrong_route}/`"
            )
    return None


def validate_active_mechanic_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_active_mechanic_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = active_mechanic_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = active_mechanic_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_active_mechanic_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_active_mechanic_route_residue(repo_root)
    for path_name, tokens in (
        (
            ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME,
            ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            "docs/decisions/README.md",
            (ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME, "Active Mechanic Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Active mechanic route residue", "same part root")),
        (LEGACY_NAMING_NAME, ("authored mechanics route cards", "legacy parent route")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_root_authored_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()

    for path_name in ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES:
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    docs_root = repo_root / "docs"
    if docs_root.is_dir():
        paths.update(path for path in docs_root.glob("*.md") if path.is_file())

    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        district = repo_root / district_name
        for allowed_name in allowed_names:
            path = district / allowed_name
            if path.is_file():
                paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def root_authored_route_context_allows(lines: Sequence[str], line_number: int) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS)


def root_authored_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "root-facing authored surface must not point at route-card-only root "
        f"district payload '{normalized}'; use `evals/<family>/<eval>/...`, an "
        "active `mechanics/...` route, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def validate_root_authored_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_root_authored_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if root_authored_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = root_authored_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_root_authored_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_root_authored_route_residue(repo_root)
    for path_name, tokens in (
        (
            ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME,
            ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            "docs/decisions/README.md",
            (ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME, "Root Authored Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Root authored route residue", "`evals/<family>/<eval>/...`")),
        (LEGACY_NAMING_NAME, ("root-facing authored surfaces", "historical context")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_decision_route_residue_files(repo_root: Path) -> list[Path]:
    decisions_root = repo_root / "docs" / "decisions"
    if not decisions_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in decisions_root.glob("*.md")
            if path.name not in {"AGENTS.md", "README.md", "TEMPLATE.md"}
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def decision_route_context_allows(lines: Sequence[str], line_number: int) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS)


def decision_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "decision record must not present route-card-only root district payload "
        f"'{normalized}' as a current route; mark it as former root or "
        "historical context, route to `evals/<family>/<eval>/...` or active "
        f"`mechanics/...`, or cite the root route card '{district_name}/README.md' "
        f"or '{district_name}/AGENTS.md'"
    )


def validate_decision_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_decision_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if decision_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = decision_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_decision_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_decision_route_residue(repo_root)
    for path_name, tokens in (
        (DECISION_ROUTE_RESIDUE_DECISION_NAME, DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (DECISION_ROUTE_RESIDUE_DECISION_NAME, "Decision Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Decision route residue", "historical context")),
        (LEGACY_NAMING_NAME, ("decision records", "former root")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_repo_config_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for path_name in (".gitignore", "pytest.ini"):
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    workflows_root = repo_root / ".github" / "workflows"
    if workflows_root.is_dir():
        paths.update(path for path in workflows_root.glob("*.yml") if path.is_file())
        paths.update(path for path in workflows_root.glob("*.yaml") if path.is_file())

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def repo_config_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "repo config surface must not point at route-card-only root district "
        f"payload '{normalized}'; use an active `mechanics/...` route, "
        f"`evals/<family>/<eval>/...`, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def repo_config_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "repo config surface must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/`"
            )
    return None


def validate_repo_config_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_repo_config_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = repo_config_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = repo_config_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_repo_config_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_repo_config_route_residue(repo_root)
    for path_name, tokens in (
        (REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME, REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME, "Repo Config Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Repo config route residue", ".gitignore")),
        (LEGACY_NAMING_NAME, ("repo config surfaces", "legacy mechanic parent")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_source_bundle_route_residue_files(repo_root: Path) -> list[Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in source_root.rglob("*")
            if path.is_file() and path.suffix in SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def bundle_root_for_source_file(path: Path, repo_root: Path) -> Path | None:
    try:
        path.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
    except ValueError:
        return None

    for parent in (path.parent, *path.parents):
        if parent == repo_root:
            break
        try:
            parent.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
        except ValueError:
            continue
        if (parent / "EVAL.md").is_file() and (parent / "eval.yaml").is_file():
            return parent
    return None


def source_bundle_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if (
        not normalized
        or normalized.startswith("repo:")
        or root_route_card_reference_is_allowed(normalized)
    ):
        return None

    bundle_root = bundle_root_for_source_file(source_file, repo_root)
    if bundle_root is not None and (bundle_root / normalized).exists():
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "source bundle must not carry ambiguous route-card-only root district "
        f"payload '{normalized}'; use a bundle-local path that exists under the "
        "owning eval package, `evals/<family>/<target>/...`, a repo-qualified sibling ref, "
        f"or the root route card '{district_name}/README.md' or "
        f"'{district_name}/AGENTS.md'"
    )


def source_bundle_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "source bundle must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/` or "
                "a provenance/legacy route with explicit historical context"
            )
    return None


def validate_source_bundle_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_source_bundle_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = source_bundle_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = source_bundle_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_source_bundle_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_source_bundle_route_residue(repo_root)
    for path_name, tokens in (
        (SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME, SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME, "Source Bundle Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Source bundle route residue", "repo-qualified sibling")),
        (LEGACY_NAMING_NAME, ("source proof bundles", "repo-qualified sibling")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


def iter_mechanic_payload_route_residue_files(repo_root: Path) -> list[Path]:
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in mechanics_root.rglob("*")
            if path.is_file()
            and path.suffix in MECHANIC_PAYLOAD_ROUTE_RESIDUE_SUFFIXES
            and path.name not in MECHANIC_PAYLOAD_ROUTE_RESIDUE_ROUTE_CARD_NAMES
            and "legacy" not in path.relative_to(repo_root).parts
            and "generated" not in path.relative_to(repo_root).parts
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def mechanic_payload_owner_root_for_source_file(path: Path, repo_root: Path) -> Path:
    try:
        relative_parts = path.relative_to(repo_root).parts
    except ValueError:
        return repo_root / "mechanics"

    if (
        len(relative_parts) >= 4
        and relative_parts[0] == "mechanics"
        and relative_parts[2] == "parts"
    ):
        return repo_root.joinpath(*relative_parts[:4])
    if len(relative_parts) >= 2 and relative_parts[0] == "mechanics":
        return repo_root.joinpath(*relative_parts[:2])
    return repo_root / "mechanics"


def mechanic_payload_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if (
        not normalized
        or normalized.startswith("repo:")
        or root_route_card_reference_is_allowed(normalized)
    ):
        return None

    owner_root = mechanic_payload_owner_root_for_source_file(source_file, repo_root)
    if (owner_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None
    if (repo_root / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "active mechanics payload must not carry ambiguous route-card-only "
        f"root district payload '{normalized}'; use a path that resolves under "
        "the same mechanic or part root, an active repo path, a repo-qualified "
        f"sibling ref, or the root route card '{district_name}/README.md' or "
        f"'{district_name}/AGENTS.md'"
    )


def mechanic_payload_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "active mechanics payload must not point at legacy mechanic "
                f"parent `{wrong_route}/`; use active "
                f"`mechanics/{correct_route}/` or a provenance/legacy route "
                "with explicit historical context"
            )
    return None


def validate_mechanic_payload_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_mechanic_payload_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = mechanic_payload_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = mechanic_payload_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def iter_json_string_values_for_keys(
    payload: Any,
    keys: frozenset[str],
) -> Iterable[tuple[str, str]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in keys and isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        yield key, item
            yield from iter_json_string_values_for_keys(value, keys)
    elif isinstance(payload, list):
        for item in payload:
            yield from iter_json_string_values_for_keys(item, keys)


def repo_relative_path_or_glob_exists(repo_root: Path, value: str) -> bool:
    normalized = value.split("#", 1)[0].strip().strip("`")
    if not normalized or normalized.startswith(("repo:", "component:")):
        return True
    if "<" in normalized or ">" in normalized:
        return True
    if "*" in normalized:
        return any(repo_root.glob(normalized))
    return (repo_root / normalized).exists()


def validate_mechanic_manifest_path_glob_routes(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        return issues

    for path in sorted(mechanics_root.glob("**/manifests/**/*.json")):
        if "legacy" in path.relative_to(repo_root).parts:
            continue
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        for _key, value in iter_json_string_values_for_keys(payload, frozenset({"path_globs"})):
            if not value.startswith("docs/"):
                continue
            if repo_relative_path_or_glob_exists(repo_root, value):
                continue
            issues.append(
                ValidationIssue(
                    path.relative_to(repo_root).as_posix(),
                    "mechanic manifest path_globs must not point at unresolved root-authored docs globs; use current repo-relative mechanic paths or an existing root-owned docs surface",
                )
            )
        for _key, value in iter_json_string_values_for_keys(
            payload,
            MECHANIC_MANIFEST_STRUCTURED_ROUTE_KEYS,
        ):
            normalized = normalize_active_mechanic_route_token(value)
            if not normalized:
                continue
            if root_route_card_reference_is_allowed(normalized):
                continue
            district_name = normalized.split("/", 1)[0]
            if district_name not in ROOT_ROUTE_CARD_ONLY_DISTRICTS:
                continue
            issues.append(
                ValidationIssue(
                    path.relative_to(repo_root).as_posix(),
                    "mechanic manifest structured route fields must not use "
                    f"route-card-only root district payload `{normalized}`; "
                    "use the current repo-relative mechanic path",
                )
            )

    return issues


def validate_mechanic_payload_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_mechanic_payload_route_residue(repo_root)
    issues.extend(validate_mechanic_manifest_path_glob_routes(repo_root))
    for path_name, tokens in (
        (
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            "docs/decisions/README.md",
            (MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME, "Mechanic Payload Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Mechanic payload route residue", "repo-qualified sibling")),
        (LEGACY_NAMING_NAME, ("active mechanics payload", "repo-qualified sibling")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues
