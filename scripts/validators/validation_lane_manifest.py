"""Validation lane manifest contract checks."""

from __future__ import annotations

from pathlib import Path

from validators.validation_topology_common import (
    LANE_MANIFEST_PATH,
    REQUIRED_LANES,
    _commands_from_sequence,
    _load_json,
)


def validate_validation_lane_manifest(repo_root: Path) -> list[tuple[str, str]]:
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


__all__ = ("validate_validation_lane_manifest",)
