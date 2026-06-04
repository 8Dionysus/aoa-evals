"""Comparison-spine route, part, and anti-overread boundary contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)

COMPARISON_SPINE_MECHANIC_README_NAME = "mechanics/comparison-spine/README.md"
COMPARISON_SPINE_MECHANIC_AGENTS_NAME = "mechanics/comparison-spine/AGENTS.md"
COMPARISON_SPINE_MECHANIC_PARTS_NAME = "mechanics/comparison-spine/PARTS.md"
COMPARISON_SPINE_PARTS_README_NAME = "mechanics/comparison-spine/parts/README.md"
COMPARISON_SPINE_OVERVIEW_PART_README_NAME = "mechanics/comparison-spine/parts/spine-overview/README.md"
COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/README.md"
)
COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/README.md"
)
COMPARISON_SPINE_OVERVIEW_REPORT_NAME = (
    "mechanics/comparison-spine/parts/spine-overview/reports/"
    "comparison-spine-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/reports/"
    "same-task-baseline-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/fixtures/"
    "frozen-same-task-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v1.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v2.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v2/README.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v2.md"
)
COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "stress-recovery-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/fixtures/"
    "repeated-window-bounded-v1/README.md"
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0029-comparison-spine-report-parts.md"
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0040-comparison-spine-fixture-parts.md"
)
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0059-comparison-spine-part-contract-guard.md"
)
COMPARISON_SPINE_PROVENANCE_NAME = "mechanics/comparison-spine/PROVENANCE.md"
COMPARISON_SPINE_LEGACY_INDEX_NAME = "mechanics/comparison-spine/legacy/INDEX.md"
COMPARISON_SPINE_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0011-comparison-spine-mechanic-package.md"
)

MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
COMPARISON_SPINE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/guides/COMPARISON_SPINE_GUIDE.md",
    "docs/guides/BASELINE_COMPARISON_GUIDE.md",
    "docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
    "generated/comparison_spine.json",
    "mechanics/comparison-spine/PARTS.md",
    COMPARISON_SPINE_OVERVIEW_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME,
    COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME,
    COMPARISON_SPINE_PROVENANCE_NAME,
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "style-only movement",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "baseline_mode",
    "comparison_surface",
    "fixtures/contract.json",
    "generated/comparison_spine.json",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/",
    "generated/comparison_spine.json",
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "pressure-to-route maps",
)
COMPARISON_SPINE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "Parts carry comparison-spine fixture and readout surfaces",
    "Source claim meaning stays in `evals/**/EVAL.md`",
    "fixture and readout surfaces",
    "| repo-global score or broad growth proof | source bundle review plus `longitudinal-window` evidence and growth/progression owner route |",
)
COMPARISON_SPINE_PARTS_README_REQUIRED_TOKENS = (
    "spine-overview/",
    "fixed-baseline/",
    "peer-compare/",
    "longitudinal-window/",
    "AGENTS.md#validation",
)
COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_OVERVIEW_PART_REQUIRED_TOKENS = (
    "comparison-spine-proof-flow-v1.md",
    "cross-mode",
    "generated/comparison_spine.json",
    "| overview dossier as comparison result | source bundle comparison surface plus mode-specific part report |",
    "| fixed-baseline, peer-compare, and longitudinal-window collapsed into one score | mode-specific part route plus bundle-local review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_FIXED_BASELINE_PART_REQUIRED_TOKENS = (
    "frozen-same-task-v1",
    "same-task-baseline-proof-flow-v1.md",
    "fixed-baseline",
    "repo-global score",
    "baseline_target_label",
    "| one fixed-baseline result as repo-global score | source bundle review plus comparison-spine bounded read |",
    "| broad growth from same-task regression evidence | `longitudinal-window` evidence plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PEER_COMPARE_PART_REQUIRED_TOKENS = (
    "bounded-change-paired-v1",
    "bounded-change-paired-v2",
    "artifact-process-paired-proof-flow-v1.md",
    "artifact-process-paired-proof-flow-v2.md",
    "Peer-compare",
    "matched_surface",
    "| peer comparison into fixed-baseline by association | source bundle `baseline_mode` and fixed-baseline part route |",
    "| peer-compare blur as broad capability growth or repo-global score | bounded comparison read plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_LONGITUDINAL_PART_REQUIRED_TOKENS = (
    "repeated-window-bounded-v1",
    "repeated-window-proof-flow-v1.md",
    "repeated-window-proof-flow-v2.md",
    "stress-recovery-window-proof-flow-v1.md",
    "broad growth proof",
    "cross-window invariants",
    "| ordered-window movement as broad growth by association | source bundle claim plus growth/progression owner review |",
    "| repeated-window or stress-recovery evidence as runtime health or antifragility acceptance | `abyss-stack` runtime route or `mechanics/antifragility/` owner route |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Comparison Spine Part Contract Guard",
    "mechanics/comparison-spine/parts/spine-overview/README.md",
    "mechanics/comparison-spine/parts/fixed-baseline/README.md",
    "mechanics/comparison-spine/parts/peer-compare/README.md",
    "mechanics/comparison-spine/parts/longitudinal-window/README.md",
    "part-level contracts",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "stronger owner split",
    "stop-lines",
    "broad growth",
    "pressure-to-owner routes",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/parts/",
    "paired_readout_path",
    "generated `proof_artifacts`",
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "does not make a shared dossier stronger than the source proof object",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_REQUIRED_TOKENS = (
    "fixed-baseline/fixtures/frozen-same-task-v1/",
    "peer-compare/fixtures/bounded-change-paired-v1/",
    "peer-compare/fixtures/bounded-change-paired-v2/",
    "longitudinal-window/fixtures/repeated-window-bounded-v1/",
    "Bundle source truth stays in `evals/**/EVAL.md`",
    "does not make a fixture family stronger than the source proof object",
    "mechanics/comparison-spine/PROVENANCE.md",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
COMPARISON_SPINE_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/frozen-same-task-v1/",
    "fixtures/bounded-change-paired-v1/",
    "fixtures/bounded-change-paired-v2/",
    "fixtures/repeated-window-bounded-v1/",
    "active fixed-baseline fixture family",
    "active peer-compare fixture family",
    "active longitudinal-window fixture family",
)

PART_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$")
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def markdown_heading_section(text: str, heading: str) -> str:
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


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    agents_path = repo_root / "mechanics" / match.group(1) / "AGENTS.md"
    if not agents_path.is_file():
        return ""
    return agents_path.read_text(encoding="utf-8")


def part_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = PART_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    parent_name, part_name = match.groups()
    part_relative = f"mechanics/{parent_name}/parts/{part_name}"
    validation_name = f"{part_relative}/VALIDATION.md"
    chunks: list[str] = []
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        chunks.append(validation_path.read_text(encoding="utf-8"))
    agents_path = repo_root / "mechanics" / parent_name / "parts" / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
        if child_section:
            chunks.append(child_section)
    return "\n\n".join(chunks)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    decision_index_text = ""
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        decision_index_text = "\n\n".join(index_texts)
    for token in tokens:
        search_text = text
        if decision_index_text:
            search_text = "\n\n".join((text, decision_index_text))
        if PART_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif MECHANIC_PARENT_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def validate_comparison_spine_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (COMPARISON_SPINE_MECHANIC_README_NAME, COMPARISON_SPINE_MECHANIC_REQUIRED_TOKENS),
        (COMPARISON_SPINE_MECHANIC_AGENTS_NAME, COMPARISON_SPINE_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (COMPARISON_SPINE_MECHANIC_PARTS_NAME, COMPARISON_SPINE_MECHANIC_PARTS_REQUIRED_TOKENS),
        (COMPARISON_SPINE_PARTS_README_NAME, COMPARISON_SPINE_PARTS_README_REQUIRED_TOKENS),
        (COMPARISON_SPINE_OVERVIEW_PART_README_NAME, COMPARISON_SPINE_OVERVIEW_PART_REQUIRED_TOKENS),
        (COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME, COMPARISON_SPINE_FIXED_BASELINE_PART_REQUIRED_TOKENS),
        (COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME, COMPARISON_SPINE_PEER_COMPARE_PART_REQUIRED_TOKENS),
        (COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME, COMPARISON_SPINE_LONGITUDINAL_PART_REQUIRED_TOKENS),
        (COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME, COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS),
        (
            DECISION_RECORDS_README_NAME,
            (COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME, "Comparison Spine Part Contract Guard"),
        ),
        (COMPARISON_SPINE_MECHANIC_DECISION_NAME, COMPARISON_SPINE_MECHANIC_DECISION_REQUIRED_TOKENS),
        (COMPARISON_SPINE_REPORT_PARTS_DECISION_NAME, COMPARISON_SPINE_REPORT_PARTS_DECISION_REQUIRED_TOKENS),
        (COMPARISON_SPINE_FIXTURE_PARTS_DECISION_NAME, COMPARISON_SPINE_FIXTURE_PARTS_DECISION_REQUIRED_TOKENS),
        (COMPARISON_SPINE_PROVENANCE_NAME, COMPARISON_SPINE_PROVENANCE_REQUIRED_TOKENS),
        (COMPARISON_SPINE_LEGACY_INDEX_NAME, COMPARISON_SPINE_LEGACY_INDEX_REQUIRED_TOKENS),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues
