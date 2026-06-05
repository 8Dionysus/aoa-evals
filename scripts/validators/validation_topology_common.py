"""Shared helpers for validation topology validators."""

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


__all__ = (
    "ALLOWED_DISPOSITIONS",
    "ALLOWED_HOME_SCOPES",
    "ALLOWED_SCRIPT_ORGAN_LANES",
    "ALLOWED_TEST_FAMILIES",
    "COMMAND_AUTHORITY_PATH",
    "LANE_MANIFEST_PATH",
    "REQUIRED_LANES",
    "REQUIRED_SCRIPT_FIELDS",
    "REQUIRED_TEST_FIELDS",
    "REQUIRED_VALIDATOR_FIELDS",
    "SCRIPT_INVENTORY_PATH",
    "SCRIPT_TOPOLOGY_PATH",
    "TESTING_DIR",
    "TEST_INVENTORY_PATH",
    "TEST_TOPOLOGY_PATH",
    "VALIDATION_DIR",
    "VALIDATOR_INVENTORY_PATH",
    "VALIDATOR_TOPOLOGY_PATH",
    "_command_script_paths",
    "_commands_from_sequence",
    "_discovered_script_surfaces",
    "_discovered_test_surfaces",
    "_load_json",
    "_require_tokens",
)
