"""Generated decision index parity validation."""

from __future__ import annotations

from pathlib import Path

from validators.decision_index_paths import GENERATED_INDEX_PATHS, INDEX_CONTRACT_PATH
from validators.decision_index_renderer import render_index_files
from validators.decision_lane_surfaces import load_index_contract, validate_decision_lane_surfaces
from validators.decision_records import collect_decision_records


def validate_decision_index_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    records, issues = collect_decision_records(repo_root)
    issues.extend(validate_decision_lane_surfaces(repo_root))
    contract, contract_issues = load_index_contract(repo_root)
    issues.extend(contract_issues)
    if contract is not None:
        expected = [path.as_posix() for path in GENERATED_INDEX_PATHS]
        if contract.get("generated_indexes") != expected:
            issues.append(
                (
                    INDEX_CONTRACT_PATH.as_posix(),
                    "generated_indexes must match the decision index read-model set",
                )
            )
    if issues:
        return issues

    rendered = render_index_files(records)
    for relative_path, expected_text in rendered.items():
        path = repo_root / relative_path
        if not path.is_file():
            issues.append((relative_path.as_posix(), "generated decision index is missing"))
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            issues.append(
                (
                    relative_path.as_posix(),
                    "generated decision index is stale; run python scripts/generate_decision_indexes.py",
                )
            )
    return issues


__all__ = ("validate_decision_index_surfaces",)
