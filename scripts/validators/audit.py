"""Audit route, provenance, and candidate-evidence boundary contracts."""

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
PART_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$")
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")

AUDIT_MECHANIC_README_NAME = "mechanics/audit/README.md"
AUDIT_MECHANIC_AGENTS_NAME = "mechanics/audit/AGENTS.md"
AUDIT_MECHANIC_PROVENANCE_NAME = "mechanics/audit/PROVENANCE.md"
AUDIT_PARTS_README_NAME = "mechanics/audit/parts/README.md"
AUDIT_LEGACY_INDEX_NAME = "mechanics/audit/legacy/INDEX.md"
AUDIT_LEGACY_DISTILLATION_LOG_NAME = "mechanics/audit/legacy/DISTILLATION_LOG.md"
AUDIT_LEGACY_RAW_README_NAME = "mechanics/audit/legacy/raw/README.md"
AUDIT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0053-audit-part-contract-guard.md"
)
AUDIT_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0007-audit-mechanic-package.md"
AUDIT_SELECTED_EVIDENCE_PART_README_NAME = (
    "mechanics/audit/parts/selected-evidence-packets/README.md"
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME = (
    "mechanics/audit/parts/artifact-verdict-hooks/README.md"
)
AUDIT_CANDIDATE_READERS_PART_README_NAME = (
    "mechanics/audit/parts/candidate-readers/README.md"
)
AUDIT_INTEGRITY_REVIEW_PART_README_NAME = (
    "mechanics/audit/parts/integrity-review/README.md"
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
AUDIT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
    "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json",
    "candidate-only",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "runtime or trace artifact",
    "selected evidence packet",
    "runtime candidate reader",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/audit/",
    "runtime evidence selection",
    "artifact-to-verdict",
    "generated readers",
    "bundle-local review",
    "does not turn runtime evidence into proof canon",
)
AUDIT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for `audit` part-local candidate-evidence suboperations",
    "## Active Parts",
    "`selected-evidence-packets/`",
    "`artifact-verdict-hooks/`",
    "`candidate-readers/`",
    "`integrity-review/`",
    "## Part Admission Route",
    "source surfaces",
    "drift-catching validation",
    "stronger-owner boundary",
    "mechanics/audit/AGENTS.md#validation",
)
AUDIT_PARTS_README_FORBIDDEN_TOKENS = (
    "Do not create another part unless",
)
AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
AUDIT_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/runtime-evidence/",
    "mechanics/audit/",
    "schemas/runtime-evidence-selection.schema.json",
    "mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json",
    "generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
)
AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "runtime-evidence",
    "audit",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "Current route:",
    "new audit proof work starts in the owning active part",
)
AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)
AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Audit Part Contract Guard",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "inputs, outputs",
    "stronger-owner split",
    "candidate-only",
    "python scripts/validate_repo.py",
)
AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "runtime-evidence-selection.schema.json",
    "runtime_evidence_selection.*.example.json",
    "candidate-only",
    "bundle-local review",
    "overread-routing notes",
    "runtime-owner review and bundle-local eval review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "TRACE_EVAL_BRIDGE.md",
    "artifact-to-verdict-hook.schema.json",
    "mechanic-local hook examples",
    "review metadata",
    "route to the owning eval bundle",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "generate_runtime_candidate_template_index.py",
    "runtime_candidate_template_index.min.json",
    "runtime_candidate_intake.min.json",
    "Reader changes start in",
    "generated reader content needs to change",
)
AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "RUNTIME_INTEGRITY_REVIEW.md",
    "runtime-integrity-review.schema.json",
    "runtime_integrity_review.example.json",
    "candidate-only",
    "runtime continuity activation is requested",
    "route to Experience and runtime-owner gates",
    "python -m pytest -q tests/test_runtime_evidence_surfaces.py -k runtime_integrity_review",
)


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
    pattern = re.compile(rf"^(##+)\s+{re.escape(heading)}\s*$", flags=re.MULTILINE)
    start = -1
    heading_level = 0
    marker = ""
    for match in pattern.finditer(text):
        marker = match.group(1)
        level = len(marker)
        if level >= 2:
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
    search_text = text
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        token_search_text = search_text
        if PART_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif MECHANIC_PARENT_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in token_search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def validate_audit_parts_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_PARTS_README_NAME,
        tokens=AUDIT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for forbidden_token in AUDIT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        AUDIT_PARTS_README_NAME,
                        "audit parts index should expose a positive part-admission route",
                    )
                )
    return issues


def validate_audit_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (AUDIT_MECHANIC_README_NAME, AUDIT_MECHANIC_REQUIRED_TOKENS),
        (AUDIT_MECHANIC_AGENTS_NAME, AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (AUDIT_MECHANIC_PROVENANCE_NAME, AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (AUDIT_LEGACY_INDEX_NAME, AUDIT_LEGACY_INDEX_REQUIRED_TOKENS),
        (AUDIT_LEGACY_DISTILLATION_LOG_NAME, AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS),
        (AUDIT_LEGACY_RAW_README_NAME, AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS),
        (AUDIT_SELECTED_EVIDENCE_PART_README_NAME, AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS),
        (
            AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
            AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS,
        ),
        (AUDIT_CANDIDATE_READERS_PART_README_NAME, AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS),
        (AUDIT_INTEGRITY_REVIEW_PART_README_NAME, AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS),
        (AUDIT_PART_CONTRACT_GUARD_DECISION_NAME, AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS),
        (
            DECISION_RECORDS_README_NAME,
            (AUDIT_PART_CONTRACT_GUARD_DECISION_NAME, "Audit Part Contract Guard"),
        ),
        (AUDIT_MECHANIC_DECISION_NAME, AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    issues.extend(validate_audit_parts_route_surface(repo_root))
    return issues
