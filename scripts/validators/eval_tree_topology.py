"""Source eval tree route and topology contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue
from validators.eval_bundle_common import (
    EVALS_AGENTS,
    EVALS_AGENTS_NAME,
    EVALS_DIR,
    EVALS_README,
    expected_manifest_parent,
    markdown_heading_section,
    markdown_python_commands,
    read_mapping,
    require_tokens,
)

SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0104-source-eval-tree-topology.md"
)
DECISION_INDEX_BY_NUMBER_NAME = "docs/decisions/indexes/by-number.md"
SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS = (
    "python scripts/validate_repo.py",
    "python scripts/build_catalog.py --check",
    "python scripts/generate_eval_report_index.py --check",
    "python -m pytest -q",
)
SOURCE_EVAL_TREE_TOPOLOGY_DECISION_REQUIRED_TOKENS = (
    "Source Eval Tree Topology",
    "`evals/<claim-family>/<eval-name>/`",
    "recursive",
    "evals/AGENTS.md#validation",
    "source-tree topology path",
)
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


def validate_source_eval_tree_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(
        repo_root=repo_root,
        path_name=SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
        tokens=SOURCE_EVAL_TREE_TOPOLOGY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )

    decision_text = read_text_or_issue(
        repo_root / SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if decision_text and markdown_python_commands(
        markdown_heading_section(decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
                "decision validation must route executable commands to evals/AGENTS.md#validation",
            )
        )

    require_tokens(
        repo_root=repo_root,
        path_name=EVALS_AGENTS_NAME,
        tokens=("source-tree topology", *SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_INDEX_BY_NUMBER_NAME,
        tokens=(SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME, "Source Eval Tree Topology"),
        issues=issues,
    )

    return issues


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

        payload, parse_issue = read_mapping(manifest_path)
        if parse_issue is not None:
            issues.append((relative_path.as_posix(), parse_issue))
            continue
        assert payload is not None
        expected_parent = expected_manifest_parent(payload)
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


__all__ = (
    "DECISION_INDEX_BY_NUMBER_NAME",
    "SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS",
    "SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME",
    "SOURCE_EVAL_TREE_TOPOLOGY_DECISION_REQUIRED_TOKENS",
    "validate_eval_bundle_topology",
    "validate_source_eval_tree_topology_surfaces",
)
