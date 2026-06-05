"""Validator inventory contract checks."""

from __future__ import annotations

from pathlib import Path

from validators.validation_topology_common import (
    ALLOWED_DISPOSITIONS,
    LANE_MANIFEST_PATH,
    REQUIRED_LANES,
    REQUIRED_VALIDATOR_FIELDS,
    VALIDATOR_INVENTORY_PATH,
    VALIDATOR_TOPOLOGY_PATH,
    _load_json,
)


def validate_validator_inventory(repo_root: Path) -> list[tuple[str, str]]:
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


__all__ = ("validate_validator_inventory",)
