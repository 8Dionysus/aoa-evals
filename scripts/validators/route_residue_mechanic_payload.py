"""Active mechanic payload route-residue validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.root_route_cards import ROOT_ROUTE_CARD_ONLY_DISTRICTS
from validators.route_residue_common import (
    ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE,
    ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
    RouteResidueContext,
    normalize_active_mechanic_route_token,
    root_route_card_reference_is_allowed,
)


MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0081-mechanic-payload-route-residue-guard.md"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k mechanic_payload_route_residue"
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
        file_location = path.relative_to(repo_root).as_posix()
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
