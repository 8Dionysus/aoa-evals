"""Script inventory contract checks."""

from __future__ import annotations

from pathlib import Path

from validators.validation_topology_common import (
    ALLOWED_SCRIPT_ORGAN_LANES,
    LANE_MANIFEST_PATH,
    REQUIRED_LANES,
    REQUIRED_SCRIPT_FIELDS,
    SCRIPT_INVENTORY_PATH,
    SCRIPT_TOPOLOGY_PATH,
    _command_script_paths,
    _commands_from_sequence,
    _discovered_script_surfaces,
    _load_json,
)


def validate_script_inventory(repo_root: Path) -> list[tuple[str, str]]:
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


__all__ = ("validate_script_inventory",)
