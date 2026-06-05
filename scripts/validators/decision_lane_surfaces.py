"""Decision-lane topology and index-contract validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from validators.decision_index_paths import (
    DECISIONS_DIR,
    FULL_ID_FILENAME_RE,
    GENERATED_INDEX_PATHS,
    INDEX_CONTRACT_PATH,
)


def load_index_contract(repo_root: Path) -> tuple[dict[str, object] | None, list[tuple[str, str]]]:
    path = repo_root / INDEX_CONTRACT_PATH
    if not path.is_file():
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract is missing")]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract must be a mapping")]
    return payload, []


def modeled_decision_lane_surfaces(
    repo_root: Path,
    contract: dict[str, object],
    issues: list[tuple[str, str]],
) -> set[str]:
    modeled = contract.get("modeled_surfaces", [])
    if modeled is None:
        return set()
    if not isinstance(modeled, list) or not all(isinstance(item, str) for item in modeled):
        issues.append((INDEX_CONTRACT_PATH.as_posix(), "modeled_surfaces must be a list of repo-relative docs/decisions paths"))
        return set()
    prefix = f"{DECISIONS_DIR.as_posix()}/"
    allowed: set[str] = set()
    for item in modeled:
        if not item.startswith(prefix):
            issues.append((INDEX_CONTRACT_PATH.as_posix(), f"modeled_surfaces entry must live under {DECISIONS_DIR.as_posix()}: {item}"))
            continue
        relative = Path(item)
        if relative.parent == DECISIONS_DIR and relative.suffix == ".md" and not FULL_ID_FILENAME_RE.match(relative.name):
            issues.append((INDEX_CONTRACT_PATH.as_posix(), f"modeled_surfaces must not include root non-record Markdown: {item}"))
            continue
        if not (repo_root / relative).is_file():
            issues.append((INDEX_CONTRACT_PATH.as_posix(), f"modeled_surfaces entry does not exist: {item}"))
            continue
        allowed.add(item)
    return allowed


def validate_decision_lane_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    decisions_root = repo_root / DECISIONS_DIR
    if not decisions_root.is_dir():
        return [(DECISIONS_DIR.as_posix(), "decision directory is missing")]

    contract, contract_issues = load_index_contract(repo_root)
    issues = list(contract_issues)
    allowed_paths = {
        (DECISIONS_DIR / "AGENTS.md").as_posix(),
        (DECISIONS_DIR / "README.md").as_posix(),
        (DECISIONS_DIR / "TEMPLATE.md").as_posix(),
        INDEX_CONTRACT_PATH.as_posix(),
        *(path.as_posix() for path in GENERATED_INDEX_PATHS),
    }
    if contract is not None:
        allowed_paths.update(modeled_decision_lane_surfaces(repo_root, contract, issues))
    for path in sorted(decisions_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(repo_root)
        relative_text = relative.as_posix()
        if relative_text in allowed_paths:
            continue
        decision_relative = path.relative_to(decisions_root)
        if len(decision_relative.parts) == 1 and FULL_ID_FILENAME_RE.match(path.name):
            continue
        issues.append(
            (
                relative_text,
                "unmodeled decision-lane surface; add it to modeled_surfaces in docs/decisions/indexes/index_contract.yaml or move it outside docs/decisions",
            )
        )
    return issues


__all__ = (
    "load_index_contract",
    "modeled_decision_lane_surfaces",
    "validate_decision_lane_surfaces",
)
