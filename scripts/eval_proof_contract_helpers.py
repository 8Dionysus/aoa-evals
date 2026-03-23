from __future__ import annotations

from typing import Any


ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY = "additional_shared_fixture_family_paths"
ADDITIONAL_PAIRED_READOUT_PATHS_KEY = "additional_paired_readout_paths"


def normalize_repo_relative_path(raw_value: Any) -> str | None:
    if not isinstance(raw_value, str) or not raw_value.strip():
        return None
    return raw_value.strip().replace("\\", "/")


def normalize_repo_relative_path_list(payload: dict[str, Any], key: str) -> list[str]:
    raw_values = payload.get(key, [])
    if not isinstance(raw_values, list):
        return []
    return [
        normalized
        for item in raw_values
        if (normalized := normalize_repo_relative_path(item)) is not None
    ]


def collect_primary_and_additional_paths(
    payload: dict[str, Any] | None,
    *,
    primary_key: str,
    additional_key: str,
) -> list[str]:
    if not isinstance(payload, dict):
        return []

    paths: list[str] = []
    primary_path = normalize_repo_relative_path(payload.get(primary_key))
    if primary_path is not None:
        paths.append(primary_path)

    for path in normalize_repo_relative_path_list(payload, additional_key):
        if path not in paths:
            paths.append(path)
    return paths


def collect_fixture_family_paths(payload: dict[str, Any] | None) -> list[str]:
    return collect_primary_and_additional_paths(
        payload,
        primary_key="shared_fixture_family_path",
        additional_key=ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
    )


def collect_paired_readout_paths(payload: dict[str, Any] | None) -> list[str]:
    return collect_primary_and_additional_paths(
        payload,
        primary_key="paired_readout_path",
        additional_key=ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
    )
