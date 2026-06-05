"""Test inventory contract checks."""

from __future__ import annotations

from pathlib import Path

from validators.validation_topology_common import (
    ALLOWED_DISPOSITIONS,
    ALLOWED_HOME_SCOPES,
    ALLOWED_TEST_FAMILIES,
    LANE_MANIFEST_PATH,
    REQUIRED_TEST_FIELDS,
    TEST_INVENTORY_PATH,
    TEST_TOPOLOGY_PATH,
    _discovered_test_surfaces,
    _load_json,
)


def validate_test_inventory(repo_root: Path) -> list[tuple[str, str]]:
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


__all__ = ("validate_test_inventory",)
