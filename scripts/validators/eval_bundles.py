"""Source eval bundle topology contracts."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Any, Sequence

import yaml

from validators.common import ValidationIssue, read_text_or_issue, relative_location


SOURCE_EVALS_DIR_NAME = "evals"
EVALS_DIR = Path(SOURCE_EVALS_DIR_NAME)
EVALS_README = EVALS_DIR / "README.md"
EVALS_AGENTS = EVALS_DIR / "AGENTS.md"
EVALS_AGENTS_NAME = EVALS_AGENTS.as_posix()
EVAL_INDEX_NAME = "EVAL_INDEX.md"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
ROADMAP_NAME = "ROADMAP.md"
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
ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS = (
    "# Proof Direction Roadmap",
    "active direction surface for `aoa-evals`",
    "roadmap owns direction and sequencing",
    "release history: [CHANGELOG.md](CHANGELOG.md)",
    "## Update Rule",
    "## Current Direction",
    "`docs/architecture/AGENT_INDEX.md` remains",
    "bundle-local review keeps bounded claim",
    "## Direction Anchors",
    "changelog and validator ledgers carry",
    "## Horizons",
)
ROADMAP_FORBIDDEN_ROUTE_SCAFFOLD = (
    "without making the roadmap an index",
    "without strengthening the bounded claim",
    "without turning the roadmap into",
)
EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    EVAL_SELECTION_NAME: (
        "## Operating Card",
        "root eval chooser for first bundle selection",
        "proof question, claim class, maturity need, comparison need, or diagnostic pressure",
        "selected source eval bundle, comparison surface, or defer-to-index route",
        "`EVAL_SELECTION.md` owns first-choice chooser wording",
        "[evals/AGENTS.md#validation](evals/AGENTS.md#validation)",
    ),
    EVAL_INDEX_NAME: (
        "## Operating Card",
        "repository-wide agent-facing index of public eval bundles",
        "public bundle inventory question, eval layer/status map question",
        "`EVAL_INDEX.md` owns public starter-table and layer-index wording",
        "generated catalog/readers, comparison spine reader, report index, and eval source validator",
        "[evals/AGENTS.md#validation](evals/AGENTS.md#validation)",
    ),
    EVALS_README.as_posix(): (
        "## Operating Card",
        "source eval package tree for bundle-local proof objects",
        "source proof question, bundle lookup, claim-family path",
        "bundle-local `EVAL.md` and `eval.yaml` own claim meaning",
        "`evals/AGENTS.md` owns source-tree edit law",
        "[evals/AGENTS.md#validation](AGENTS.md#validation)",
    ),
}
NO_ADDITIONAL_STARTER_BUNDLES_TEXT = (
    "No additional planned starter bundles are currently named publicly."
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


def _require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    for token in tokens:
        if token not in text:
            issues.append(
                ValidationIssue(path_name, f"missing required text token: {token}")
            )
    return text


def _markdown_heading_section(text: str, heading: str) -> str:
    marker = ""
    heading_level = 0
    start = -1
    for level in (3, 2):
        pattern = re.compile(rf"(?m)^{'#' * level} {re.escape(heading)}\s*$")
        match = pattern.search(text)
        if match:
            marker = match.group(0)
            heading_level = level
            start = match.start()
            break
    if start == -1:
        return ""
    next_h2 = text.find("\n## ", start + len(marker))
    next_h3 = text.find("\n### ", start + len(marker)) if heading_level > 2 else -1
    candidates = [index for index in (next_h2, next_h3) if index != -1]
    end = min(candidates) if candidates else len(text)
    return text[start:end]


def _markdown_python_commands(section: str) -> list[str]:
    commands: list[str] = []
    commands.extend(re.findall(r"`(python3? [^`]+)`", section))
    in_fence = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped.startswith("python ") or stripped.startswith("python3 "):
            commands.append(stripped)
    return list(dict.fromkeys(commands))


def _read_mapping(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, f"eval manifest must be valid yaml: {exc}"
    if not isinstance(payload, dict):
        return None, "eval manifest must be a mapping"
    return payload, None


def _load_yaml_file(
    path: Path,
    issues: list[ValidationIssue],
    *,
    repo_root: Path,
) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, repo_root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(relative_location(path, repo_root), f"invalid YAML: {exc}")
        )
        return None
    return data


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


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / EVALS_DIR
    if not source_root.is_dir():
        raise FileNotFoundError(f"missing source eval directory at {source_root}")

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_name = eval_dir.name
        if eval_name in eval_dirs:
            raise ValueError(
                "duplicate source eval directory name "
                f"'{eval_name}' at {relative_location(eval_dirs[eval_name], repo_root)} "
                f"and {relative_location(eval_dir, repo_root)}"
            )
        eval_dirs[eval_name] = eval_dir
    return eval_dirs


def extract_table_eval_names(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start_index = next(
            index for index, line in enumerate(lines) if line.strip() == heading
        )
    except StopIteration:
        return []

    table_lines: list[str] = []
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines and not stripped:
            break
        if table_lines:
            break

    pattern = re.compile(r"^\|\s*(aoa-[a-z0-9-]+)\s*\|")
    return [
        pattern.match(line).group(1)
        for line in table_lines
        if pattern.match(line)
    ]


def load_starter_eval_names(
    repo_root: Path,
    issues: list[ValidationIssue] | None = None,
) -> list[str]:
    active_issues = issues if issues is not None else []
    index_path = repo_root / EVAL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        active_issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))
        return []

    starter_names = extract_table_eval_names(text, "## Starter eval bundles")
    if not starter_names:
        active_issues.append(
            ValidationIssue(
                relative_location(index_path, repo_root),
                "missing or empty 'Starter eval bundles' table",
            )
        )
    return starter_names


def extract_bulleted_eval_names(text: str, label: str) -> list[str]:
    lines = text.splitlines()
    names: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                break
            if not stripped.startswith("- "):
                break
            names.extend(re.findall(r"aoa-[a-z0-9-]+", stripped))
    return names


def validate_source_eval_tree_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    _require_tokens(
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
    if decision_text and _markdown_python_commands(
        _markdown_heading_section(decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
                "decision validation must route executable commands to evals/AGENTS.md#validation",
            )
        )

    _require_tokens(
        repo_root=repo_root,
        path_name=EVALS_AGENTS_NAME,
        tokens=("source-tree topology", *SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_INDEX_BY_NUMBER_NAME,
        tokens=(SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME, "Source Eval Tree Topology"),
        issues=issues,
    )

    return issues


def validate_eval_source_entry_operating_cards(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name, tokens in EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS.items():
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
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


def validate_eval_index(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_path = repo_root / EVAL_INDEX_NAME
    location = relative_location(index_path, repo_root)
    counts = Counter(starter_names)

    if selected_evals is None:
        eval_dirs = set(discover_eval_dirs(repo_root))

        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

        starter_set = set(counts.keys())

        for extra in sorted(starter_set - eval_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{extra}' has no matching source eval package directory",
                )
            )
    else:
        for name in sorted(selected_evals):
            count = counts.get(name, 0)
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

    return issues


def validate_eval_selection(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    selection_path = repo_root / EVAL_SELECTION_NAME
    try:
        text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(EVAL_SELECTION_NAME, "file is missing")]

    location = relative_location(selection_path, repo_root)
    names_in_selection = set(re.findall(r"aoa-[a-z0-9-]+", text))
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    issues: list[ValidationIssue] = []

    for token in (
        "# Eval Bundle Selection Chooser",
        "repository-wide chooser for public eval bundles",
    ):
        if token not in text:
            issues.append(
                ValidationIssue(
                    location,
                    f"EVAL_SELECTION.md must mention '{token}'",
                )
            )

    for name in sorted(names_to_check):
        if name not in names_in_selection:
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{name}' is missing from EVAL_SELECTION.md",
                )
            )

    return issues


def validate_starter_bundle_contract(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    eval_dirs = discover_eval_dirs(repo_root)

    for name in sorted(names_to_check):
        bundle_dir = eval_dirs.get(name, repo_root / EVALS_DIR / name)
        manifest_path = bundle_dir / "eval.yaml"
        location = relative_location(bundle_dir, repo_root)

        example_report = bundle_dir / "examples" / "example-report.md"
        if not example_report.is_file():
            issues.append(
                ValidationIssue(
                    location,
                    "starter bundle is missing examples/example-report.md",
                )
            )

        manifest_issues: list[ValidationIssue] = []
        manifest = _load_yaml_file(manifest_path, manifest_issues, repo_root=repo_root)
        issues.extend(manifest_issues)
        if not isinstance(manifest, dict):
            continue

        evidence = manifest.get("evidence", [])
        if not evidence:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include at least one manifest evidence entry",
                )
            )
            continue

        has_integrity_check = any(
            item.get("kind") == "integrity_check" for item in evidence
        )
        if not has_integrity_check:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'integrity_check'",
                )
            )

        has_origin_need = any(item.get("kind") == "origin_need" for item in evidence)
        if not has_origin_need:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'origin_need'",
                )
            )

    return issues


def validate_roadmap_parity(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    roadmap_path = repo_root / ROADMAP_NAME
    try:
        roadmap_text = roadmap_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(ROADMAP_NAME, "file is missing")]

    location = relative_location(roadmap_path, repo_root)
    issues: list[ValidationIssue] = []
    for token in ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS:
        if token not in roadmap_text:
            issues.append(
                ValidationIssue(
                    location,
                    f"ROADMAP.md must include '{token}'",
                )
            )
    for stale_phrase in ROADMAP_FORBIDDEN_ROUTE_SCAFFOLD:
        if stale_phrase in roadmap_text:
            issues.append(
                ValidationIssue(
                    location,
                    "ROADMAP.md should name direction owner routes before old "
                    f"negative scaffold '{stale_phrase}'",
                )
            )

    starter_set = set(starter_names)
    bundle_names = set(discover_eval_dirs(repo_root))
    current_public_surface_names = set(
        extract_bulleted_eval_names(roadmap_text, "Current public surface:")
    )
    names_to_check = current_public_surface_names
    if selected_evals is not None:
        names_to_check = current_public_surface_names.intersection(selected_evals)

    for name in sorted(names_to_check):
        if name not in bundle_names:
            issues.append(
                ValidationIssue(
                    location,
                    "roadmap 'Current public surface' eval "
                    f"'{name}' has no matching source eval package directory",
                )
            )
            continue
        if name not in starter_set:
            issues.append(
                ValidationIssue(
                    location,
                    f"roadmap 'Current public surface' eval '{name}' must appear in EVAL_INDEX.md starter bundles",
                )
            )

    if selected_evals is not None:
        return issues

    index_path = repo_root / EVAL_INDEX_NAME
    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return issues

    roadmap_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in roadmap_text
    index_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in index_text
    if roadmap_has_absence_note != index_has_absence_note:
        issues.append(
            ValidationIssue(
                location,
                f"absence note '{NO_ADDITIONAL_STARTER_BUNDLES_TEXT}' must stay synchronized with {EVAL_INDEX_NAME}",
            )
        )

    return issues


def validate_source_eval_entry_surfaces(
    repo_root: Path,
    *,
    starter_names: Sequence[str],
    selected_evals: set[str] | None,
    selected_starter_evals: set[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        validate_eval_index(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_eval_selection(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_starter_bundle_contract(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_roadmap_parity(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )
    return issues
