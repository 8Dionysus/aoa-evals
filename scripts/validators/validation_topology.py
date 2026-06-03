"""Validation lane, script, and test topology contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VALIDATION_DIR = Path("docs/validation")
TESTING_DIR = Path("docs/testing")
LANE_MANIFEST_PATH = VALIDATION_DIR / "validation_lanes.json"
VALIDATOR_INVENTORY_PATH = VALIDATION_DIR / "validator_inventory.json"
SCRIPT_INVENTORY_PATH = VALIDATION_DIR / "script_inventory.json"
TEST_INVENTORY_PATH = TESTING_DIR / "test_inventory.json"
VALIDATOR_TOPOLOGY_PATH = VALIDATION_DIR / "VALIDATOR_TOPOLOGY.md"
COMMAND_AUTHORITY_PATH = VALIDATION_DIR / "COMMAND_AUTHORITY.md"
SCRIPT_TOPOLOGY_PATH = VALIDATION_DIR / "SCRIPT_TOPOLOGY.md"
TEST_TOPOLOGY_PATH = TESTING_DIR / "TEST_TOPOLOGY.md"

REQUIRED_LANES = {
    "source_fast",
    "generated",
    "mechanics_part_local",
    "pinned_sibling",
    "latest_sibling",
    "trace_eval",
    "audit",
    "release",
    "nightly",
    "advisory",
}
REQUIRED_VALIDATOR_FIELDS = {
    "path",
    "lane",
    "layer",
    "mode",
    "owner_surface",
    "source_truth",
    "input",
    "output",
    "command_sequences",
    "failure_route",
    "disposition",
}
REQUIRED_SCRIPT_FIELDS = {
    "path",
    "family",
    "organ_lane",
    "owner_surface",
    "source_truth",
    "reads",
    "writes",
    "side_effects",
    "validation_lane",
    "ci_inclusion",
    "test_target",
    "disposition",
}
REQUIRED_TEST_FIELDS = {
    "path",
    "family",
    "home_scope",
    "owner_surface",
    "coverage_authority",
    "focused_target",
    "failure_route",
    "disposition",
}
ALLOWED_SCRIPT_ORGAN_LANES = {
    "source/topology",
    "projection/generated",
    "capability/runtime-policy route",
    "mechanics/part-local",
    "runtime-policy route",
    "trace/eval route",
    "observability/audit",
    "security/adversarial",
    "release/nightly",
    "compatibility adapter",
}
ALLOWED_TEST_FAMILIES = {
    "source/proof-contract",
    "generated/read-model",
    "route-card/topology",
    "mechanics/package-topology",
    "mechanics/part-local",
    "boundary/sibling",
    "trace/eval-scenario",
    "audit/release-report",
    "validation-topology/authority",
}
ALLOWED_HOME_SCOPES = {"root", "mechanic-part", "agent-lane"}
ALLOWED_DISPOSITIONS = {"keep", "split", "fold", "add"}


def _load_json(repo_root: Path, relative_path: Path) -> tuple[dict[str, Any] | None, list[tuple[str, str]]]:
    path = repo_root / relative_path
    if not path.is_file():
        return None, [(relative_path.as_posix(), "validation topology JSON surface is missing")]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [(relative_path.as_posix(), f"invalid JSON: {exc.msg}")]
    if not isinstance(payload, dict):
        return None, [(relative_path.as_posix(), "JSON surface must contain an object")]
    return payload, []


def _commands_from_sequence(raw_sequence: object, where: str) -> tuple[tuple[str, ...], ...] | None:
    if not isinstance(raw_sequence, list) or not raw_sequence:
        return None
    commands: list[tuple[str, ...]] = []
    for idx, raw_command in enumerate(raw_sequence):
        if not isinstance(raw_command, list) or not raw_command:
            return None
        if any(not isinstance(part, str) or not part for part in raw_command):
            return None
        commands.append(tuple(raw_command))
    return tuple(commands)


def _command_script_paths(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        for part in command:
            if part.endswith(".py") and (
                part.startswith("scripts/") or "/scripts/" in part
            ):
                paths.add(part)
    return paths


def _discovered_script_surfaces(repo_root: Path) -> set[str]:
    return {
        path.relative_to(repo_root).as_posix()
        for path in repo_root.rglob("*")
        if path.is_file()
        and ".deps" not in path.relative_to(repo_root).parts
        and ".git" not in path.relative_to(repo_root).parts
        and "/scripts/" in f"/{path.relative_to(repo_root).as_posix()}"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


def _discovered_test_surfaces(repo_root: Path) -> set[str]:
    root_tests = {
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "tests").glob("test*.py")
        if path.is_file()
    }
    part_tests = {
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "mechanics").glob("*/parts/*/tests/test*.py")
        if path.is_file()
    }
    return root_tests | part_tests


def _require_tokens(repo_root: Path, relative_path: Path, tokens: tuple[str, ...]) -> list[tuple[str, str]]:
    path = repo_root / relative_path
    if not path.is_file():
        return [(relative_path.as_posix(), "validation topology document is missing")]
    text = path.read_text(encoding="utf-8")
    return [
        (relative_path.as_posix(), f"validation topology document must mention {token!r}")
        for token in tokens
        if token not in text
    ]


def _validate_lane_manifest(repo_root: Path) -> list[tuple[str, str]]:
    manifest, issues = _load_json(repo_root, LANE_MANIFEST_PATH)
    if manifest is None:
        return issues

    if manifest.get("schema_version") != 1:
        issues.append((LANE_MANIFEST_PATH.as_posix(), "lane manifest schema_version must be 1"))
    if manifest.get("command_authority") != LANE_MANIFEST_PATH.as_posix():
        issues.append((LANE_MANIFEST_PATH.as_posix(), "lane manifest must name itself as command_authority"))

    lanes = manifest.get("lanes")
    if not isinstance(lanes, dict):
        issues.append((LANE_MANIFEST_PATH.as_posix(), "lanes must be a mapping"))
        lanes = {}
    missing_lanes = REQUIRED_LANES - set(lanes)
    extra_lanes = set(lanes) - REQUIRED_LANES
    for lane_id in sorted(missing_lanes):
        issues.append((LANE_MANIFEST_PATH.as_posix(), f"missing lane definition {lane_id!r}"))
    for lane_id in sorted(extra_lanes):
        issues.append((LANE_MANIFEST_PATH.as_posix(), f"unexpected lane definition {lane_id!r}"))

    command_sequences = manifest.get("command_sequences")
    if not isinstance(command_sequences, dict):
        issues.append((LANE_MANIFEST_PATH.as_posix(), "command_sequences must be a mapping"))
        command_sequences = {}

    parsed_sequences: dict[str, tuple[tuple[str, ...], ...]] = {}
    for sequence_name, raw_sequence in command_sequences.items():
        parsed = _commands_from_sequence(raw_sequence, f"command_sequences.{sequence_name}")
        if parsed is None:
            issues.append(
                (
                    LANE_MANIFEST_PATH.as_posix(),
                    f"command sequence {sequence_name!r} must contain non-empty argv lists",
                )
            )
            continue
        parsed_sequences[sequence_name] = parsed

    for lane_id, lane in lanes.items():
        if not isinstance(lane, dict):
            issues.append((LANE_MANIFEST_PATH.as_posix(), f"lane {lane_id!r} must be an object"))
            continue
        if lane.get("posture") not in {"blocking", "non_blocking"}:
            issues.append((LANE_MANIFEST_PATH.as_posix(), f"lane {lane_id!r} posture is invalid"))
        owner_surface = lane.get("owner_surface")
        if not isinstance(owner_surface, str) or not owner_surface:
            issues.append((LANE_MANIFEST_PATH.as_posix(), f"lane {lane_id!r} owner_surface is required"))
        elif not (repo_root / owner_surface).exists():
            issues.append((owner_surface, f"lane {lane_id!r} owner_surface does not exist"))
        sequence_name = lane.get("command_sequence")
        if lane.get("posture") == "blocking" and not isinstance(sequence_name, str):
            issues.append((LANE_MANIFEST_PATH.as_posix(), f"blocking lane {lane_id!r} must name a command_sequence"))
        if isinstance(sequence_name, str) and sequence_name not in parsed_sequences:
            issues.append((LANE_MANIFEST_PATH.as_posix(), f"lane {lane_id!r} references missing command_sequence {sequence_name!r}"))

    groups = manifest.get("command_groups")
    if not isinstance(groups, dict):
        issues.append((LANE_MANIFEST_PATH.as_posix(), "command_groups must be a mapping"))
    else:
        generated_groups = groups.get("generated_check")
        if not isinstance(generated_groups, list) or not generated_groups:
            issues.append((LANE_MANIFEST_PATH.as_posix(), "command_groups.generated_check must be a non-empty list"))
        else:
            flattened: list[tuple[str, ...]] = []
            for idx, group in enumerate(generated_groups):
                if not isinstance(group, dict):
                    issues.append((LANE_MANIFEST_PATH.as_posix(), f"generated_check group {idx} must be an object"))
                    continue
                sequence_name = group.get("command_sequence")
                if not isinstance(sequence_name, str) or sequence_name not in parsed_sequences:
                    issues.append((LANE_MANIFEST_PATH.as_posix(), f"generated_check group {idx} references a missing command sequence"))
                    continue
                flattened.extend(parsed_sequences[sequence_name])
            if tuple(flattened) != parsed_sequences.get("generated_check"):
                issues.append((LANE_MANIFEST_PATH.as_posix(), "generated command group must flatten to generated_check sequence"))

    return issues


def _validate_validator_inventory(repo_root: Path) -> list[tuple[str, str]]:
    inventory, issues = _load_json(repo_root, VALIDATOR_INVENTORY_PATH)
    if inventory is None:
        return issues

    if inventory.get("owner") != VALIDATOR_TOPOLOGY_PATH.as_posix():
        issues.append((VALIDATOR_INVENTORY_PATH.as_posix(), "validator inventory owner is wrong"))
    if inventory.get("command_authority") != LANE_MANIFEST_PATH.as_posix():
        issues.append((VALIDATOR_INVENTORY_PATH.as_posix(), "validator inventory must route command authority to lane manifest"))
    if set(inventory.get("required_fields", ())) != REQUIRED_VALIDATOR_FIELDS:
        issues.append((VALIDATOR_INVENTORY_PATH.as_posix(), "validator inventory required_fields are out of sync"))

    entries = inventory.get("entries")
    if not isinstance(entries, list) or not entries:
        return issues + [(VALIDATOR_INVENTORY_PATH.as_posix(), "validator inventory entries must be non-empty")]

    paths: list[str] = []
    for idx, entry in enumerate(entries):
        location = f"{VALIDATOR_INVENTORY_PATH.as_posix()}.entries[{idx}]"
        if not isinstance(entry, dict):
            issues.append((location, "validator inventory entry must be an object"))
            continue
        if set(entry) != REQUIRED_VALIDATOR_FIELDS:
            issues.append((location, "validator inventory entry fields are incomplete"))
            continue
        path_name = str(entry["path"])
        paths.append(path_name)
        if not (repo_root / path_name).exists():
            issues.append((path_name, "validator inventory path does not exist"))
        if not (repo_root / str(entry["owner_surface"])).exists():
            issues.append((str(entry["owner_surface"]), f"validator inventory owner_surface for {path_name!r} does not exist"))
        if entry["lane"] not in REQUIRED_LANES:
            issues.append((location, f"validator inventory lane {entry['lane']!r} is unknown"))
        if entry["mode"] not in {"blocking", "non_blocking", "advisory"}:
            issues.append((location, "validator inventory mode is invalid"))
        if entry["disposition"] not in ALLOWED_DISPOSITIONS:
            issues.append((location, "validator inventory disposition is invalid"))
        for field in ("source_truth", "input", "output", "command_sequences"):
            if not isinstance(entry[field], list) or not entry[field]:
                issues.append((location, f"validator inventory field {field!r} must be a non-empty list"))
        if not isinstance(entry["failure_route"], str) or not entry["failure_route"]:
            issues.append((location, "validator inventory failure_route is required"))

    if len(paths) != len(set(paths)):
        issues.append((VALIDATOR_INVENTORY_PATH.as_posix(), "validator inventory paths must be unique"))

    expected_validator_modules = {
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "scripts" / "validators").glob("*.py")
        if path.is_file() and "__pycache__" not in path.parts
    }
    expected_validator_modules.update(
        {
            "scripts/validate_repo.py",
            "scripts/validate_nested_agents.py",
            "scripts/validate_semantic_agents.py",
        }
    )
    missing = sorted(expected_validator_modules - set(paths))
    for path_name in missing:
        issues.append((path_name, "validator inventory must classify every root validator surface"))

    return issues


def _validate_script_inventory(repo_root: Path) -> list[tuple[str, str]]:
    inventory, issues = _load_json(repo_root, SCRIPT_INVENTORY_PATH)
    if inventory is None:
        return issues

    if inventory.get("owner") != SCRIPT_TOPOLOGY_PATH.as_posix():
        issues.append((SCRIPT_INVENTORY_PATH.as_posix(), "script inventory owner is wrong"))
    if inventory.get("command_authority") != LANE_MANIFEST_PATH.as_posix():
        issues.append((SCRIPT_INVENTORY_PATH.as_posix(), "script inventory must route command authority to lane manifest"))

    entries = inventory.get("script_surfaces")
    if not isinstance(entries, list) or not entries:
        return issues + [(SCRIPT_INVENTORY_PATH.as_posix(), "script inventory surfaces must be non-empty")]

    paths: list[str] = []
    for idx, entry in enumerate(entries):
        location = f"{SCRIPT_INVENTORY_PATH.as_posix()}.script_surfaces[{idx}]"
        if not isinstance(entry, dict):
            issues.append((location, "script inventory entry must be an object"))
            continue
        if set(entry) != REQUIRED_SCRIPT_FIELDS:
            issues.append((location, "script inventory entry fields are incomplete"))
            continue
        path_name = str(entry["path"])
        paths.append(path_name)
        if entry["organ_lane"] not in ALLOWED_SCRIPT_ORGAN_LANES:
            issues.append((location, f"script inventory organ_lane {entry['organ_lane']!r} is unknown"))
        if entry["validation_lane"] not in REQUIRED_LANES:
            issues.append((location, f"script inventory validation_lane {entry['validation_lane']!r} is unknown"))
        if entry["disposition"] not in {"keep", "split", "add"}:
            issues.append((location, "script inventory disposition is invalid"))
        if not (repo_root / path_name).is_file():
            issues.append((path_name, "script inventory path does not exist"))
        for path_field in ("owner_surface", "test_target"):
            if not (repo_root / str(entry[path_field])).exists():
                issues.append((str(entry[path_field]), f"script inventory {path_field} for {path_name!r} does not exist"))
        for field in ("source_truth", "reads", "writes"):
            if not isinstance(entry[field], list):
                issues.append((location, f"script inventory field {field!r} must be a list"))
        for field in ("side_effects", "ci_inclusion"):
            if not isinstance(entry[field], str) or not entry[field]:
                issues.append((location, f"script inventory field {field!r} is required"))

    if len(paths) != len(set(paths)):
        issues.append((SCRIPT_INVENTORY_PATH.as_posix(), "script inventory paths must be unique"))

    discovered = _discovered_script_surfaces(repo_root)
    for path_name in sorted(discovered - set(paths)):
        issues.append((path_name, "script inventory must classify every active script surface"))
    for path_name in sorted(set(paths) - discovered):
        issues.append((path_name, "script inventory classifies a missing script surface"))

    manifest, manifest_issues = _load_json(repo_root, LANE_MANIFEST_PATH)
    issues.extend(manifest_issues)
    if manifest is not None and isinstance(manifest.get("command_sequences"), dict):
        command_paths: set[str] = set()
        for raw_sequence in manifest["command_sequences"].values():
            parsed = _commands_from_sequence(raw_sequence, "command_sequences")
            if parsed is not None:
                command_paths.update(_command_script_paths(parsed))
        for path_name in sorted(command_paths - set(paths)):
            issues.append((path_name, "lane command script must be classified in script inventory"))

    return issues


def _validate_test_inventory(repo_root: Path) -> list[tuple[str, str]]:
    inventory, issues = _load_json(repo_root, TEST_INVENTORY_PATH)
    if inventory is None:
        return issues

    if inventory.get("owner") != TEST_TOPOLOGY_PATH.as_posix():
        issues.append((TEST_INVENTORY_PATH.as_posix(), "test inventory owner is wrong"))
    if inventory.get("command_authority") != LANE_MANIFEST_PATH.as_posix():
        issues.append((TEST_INVENTORY_PATH.as_posix(), "test inventory must route command authority to lane manifest"))
    if set(inventory.get("required_fields", ())) != REQUIRED_TEST_FIELDS:
        issues.append((TEST_INVENTORY_PATH.as_posix(), "test inventory required_fields are out of sync"))

    entries = inventory.get("test_surfaces")
    if not isinstance(entries, list) or not entries:
        return issues + [(TEST_INVENTORY_PATH.as_posix(), "test inventory surfaces must be non-empty")]

    paths: list[str] = []
    for idx, entry in enumerate(entries):
        location = f"{TEST_INVENTORY_PATH.as_posix()}.test_surfaces[{idx}]"
        if not isinstance(entry, dict):
            issues.append((location, "test inventory entry must be an object"))
            continue
        if set(entry) != REQUIRED_TEST_FIELDS:
            issues.append((location, "test inventory entry fields are incomplete"))
            continue
        path_name = str(entry["path"])
        paths.append(path_name)
        if not (repo_root / path_name).is_file():
            issues.append((path_name, "test inventory path does not exist"))
        if not (repo_root / str(entry["owner_surface"])).exists():
            issues.append((str(entry["owner_surface"]), f"test inventory owner_surface for {path_name!r} does not exist"))
        if entry["family"] not in ALLOWED_TEST_FAMILIES:
            issues.append((location, f"test inventory family {entry['family']!r} is unknown"))
        if entry["home_scope"] not in ALLOWED_HOME_SCOPES:
            issues.append((location, "test inventory home_scope is invalid"))
        if not isinstance(entry["coverage_authority"], str) or not entry["coverage_authority"].startswith("validation_lanes."):
            issues.append((location, "test inventory coverage_authority must route through validation_lanes"))
        if entry["disposition"] not in ALLOWED_DISPOSITIONS:
            issues.append((location, "test inventory disposition is invalid"))
        for field in ("focused_target", "failure_route"):
            if not isinstance(entry[field], str) or not entry[field]:
                issues.append((location, f"test inventory field {field!r} is required"))

    if len(paths) != len(set(paths)):
        issues.append((TEST_INVENTORY_PATH.as_posix(), "test inventory paths must be unique"))

    discovered = _discovered_test_surfaces(repo_root)
    for path_name in sorted(discovered - set(paths)):
        issues.append((path_name, "test inventory must classify every root and part-local test"))
    for path_name in sorted(set(paths) - discovered):
        issues.append((path_name, "test inventory classifies a missing test"))

    return issues


def validate_validation_topology(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    issues.extend(
        _require_tokens(
            repo_root,
            VALIDATOR_TOPOLOGY_PATH,
            (
                "source-fast",
                "generated",
                "trace/eval",
                "Memory/context validators",
                "Security/adversarial validators",
            ),
        )
    )
    issues.extend(
        _require_tokens(
            repo_root,
            COMMAND_AUTHORITY_PATH,
            (
                "docs/validation/validation_lanes.json",
                "`config/` is currently a route-card-only",
                "Promotion Rule",
            ),
        )
    )
    issues.extend(_validate_lane_manifest(repo_root))
    issues.extend(_validate_validator_inventory(repo_root))
    issues.extend(_validate_script_inventory(repo_root))
    issues.extend(_validate_test_inventory(repo_root))
    return issues
