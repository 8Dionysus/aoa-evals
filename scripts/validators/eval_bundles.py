"""Source eval bundle topology contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


EVALS_DIR = Path("evals")
EVALS_README = EVALS_DIR / "README.md"
EVALS_AGENTS = EVALS_DIR / "AGENTS.md"
REQUIRED_FAMILIES = (
    "workflow",
    "boundary",
    "artifact",
    "stress",
    "capability",
    "comparison/fixed-baseline",
    "comparison/peer-compare",
    "comparison/longitudinal-window",
)
REQUIRED_ROUTE_TOKENS = (
    "evals/<claim-family>/<eval-name>/",
    "bundle-local `EVAL.md` and `eval.yaml`",
)
README_ROUTE_TOKENS = (
    *REQUIRED_ROUTE_TOKENS,
    "evals/AGENTS.md#validation",
)
AGENTS_ROUTE_TOKENS = (
    *REQUIRED_ROUTE_TOKENS,
    "source-tree topology",
)


def _read_mapping(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, f"eval manifest must be valid yaml: {exc}"
    if not isinstance(payload, dict):
        return None, "eval manifest must be a mapping"
    return payload, None


def _expected_manifest_parent(payload: dict[str, Any]) -> Path | None:
    name = payload.get("name")
    category = payload.get("category")
    baseline_mode = payload.get("baseline_mode", "none")
    if not isinstance(name, str) or not name:
        return None
    if baseline_mode and baseline_mode != "none":
        if not isinstance(baseline_mode, str):
            return None
        return EVALS_DIR / "comparison" / baseline_mode / name
    if not isinstance(category, str) or not category:
        return None
    return EVALS_DIR / category / name


def validate_eval_bundle_topology(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    evals_root = repo_root / EVALS_DIR
    if not evals_root.is_dir():
        return [(EVALS_DIR.as_posix(), "source eval tree is missing")]

    for route_path in (EVALS_README, EVALS_AGENTS):
        path = repo_root / route_path
        if not path.is_file():
            issues.append((route_path.as_posix(), "source eval route surface is missing"))
            continue
        text = path.read_text(encoding="utf-8")
        route_tokens = README_ROUTE_TOKENS if route_path == EVALS_README else AGENTS_ROUTE_TOKENS
        for token in route_tokens:
            if token not in text:
                issues.append((route_path.as_posix(), f"source eval route surface must mention {token!r}"))

    for family in REQUIRED_FAMILIES:
        if not (evals_root / family).is_dir():
            issues.append((f"evals/{family}", "source eval claim family directory is missing"))

    manifest_paths = sorted(evals_root.rglob("eval.yaml"))
    if not manifest_paths:
        issues.append((EVALS_DIR.as_posix(), "source eval tree must contain eval manifests"))
    for manifest_path in manifest_paths:
        relative_path = manifest_path.relative_to(repo_root)
        parent_relative = manifest_path.parent.relative_to(repo_root)
        parts = relative_path.parts
        valid_shape = (
            len(parts) == 4
            and parts[0] == "evals"
            and parts[1] != "comparison"
            and parts[3] == "eval.yaml"
        ) or (
            len(parts) == 5
            and parts[0] == "evals"
            and parts[1] == "comparison"
            and parts[4] == "eval.yaml"
        )
        if not valid_shape:
            issues.append(
                (
                    relative_path.as_posix(),
                    "eval manifest must live under evals/<claim-family>/<eval-name>/ or evals/comparison/<baseline-mode>/<eval-name>/",
                )
            )

        if not (manifest_path.parent / "EVAL.md").is_file():
            issues.append((parent_relative.as_posix(), "source eval bundle must include EVAL.md"))

        payload, parse_issue = _read_mapping(manifest_path)
        if parse_issue is not None:
            issues.append((relative_path.as_posix(), parse_issue))
            continue
        assert payload is not None
        expected_parent = _expected_manifest_parent(payload)
        if expected_parent is None:
            issues.append(
                (
                    relative_path.as_posix(),
                    "eval manifest must define name, category, and baseline_mode topology fields",
                )
            )
            continue
        if parent_relative != expected_parent:
            issues.append(
                (
                    relative_path.as_posix(),
                    f"eval manifest path must match manifest topology fields: {expected_parent.as_posix()}",
                )
            )

    return issues
