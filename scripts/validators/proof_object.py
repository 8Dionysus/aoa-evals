"""Proof-object route and source-authority boundary contracts."""

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

PROOF_OBJECT_MECHANIC_README_NAME = "mechanics/proof-object/README.md"
PROOF_OBJECT_MECHANIC_AGENTS_NAME = "mechanics/proof-object/AGENTS.md"
PROOF_OBJECT_MECHANIC_PARTS_NAME = "mechanics/proof-object/PARTS.md"
PROOF_OBJECT_MECHANIC_PROVENANCE_NAME = "mechanics/proof-object/PROVENANCE.md"
PROOF_OBJECT_PARTS_README_NAME = "mechanics/proof-object/parts/README.md"
PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-authoring/README.md"
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-contracts/README.md"
)
PROOF_OBJECT_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0010-proof-object-mechanic-package.md"
PROOF_OBJECT_CONTRACT_PART_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0048-proof-object-contract-parts.md"
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0069-proof-object-part-owner-split-contract.md"
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0105-proof-object-eval-part-names.md"
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
PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "proof-object completeness review",
    "bundle-local review",
    "Source eval packages stay under `evals/`",
    "python scripts/build_catalog.py --check",
    "AGENTS.md#validation",
)
PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source proof objects",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "EVAL.md and eval.yaml",
    "eval-local support artifacts",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "eval-authoring",
    "eval-contracts",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "Source eval packages stay under `evals/`",
    "AGENTS.md#validation",
)
PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for proof-object authoring and contract support parts",
    "source eval bundle for proof meaning",
    "source `evals/**/EVAL.md` and `evals/**/eval.yaml`",
    "## Part Admission Route",
    "`eval-authoring/`",
    "`eval-contracts/`",
    "stronger-owner split",
    "mechanics/proof-object/AGENTS.md#validation",
    "generated-reader check",
    "generated-reader freshness checks",
)
PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS = (
    "They do not own source eval meaning and do not replace generated readers",
)
PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS = (
    "Eval Authoring",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "actual source proof",
    "template",
    "doctrine or accepted proof meaning",
    "sibling refs outrank source eval packages",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS = (
    "Eval Contracts",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "schema-backed contract validation",
    "claim invention",
    "schema acceptance reads as eval-local review",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "proof-object completeness review",
    "does not move `evals/`",
    "generated readers",
    "bundle-local review",
)
PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/",
    "source bundles stay under `evals/`",
    "generated readers stay",
    "python scripts/validate_repo.py",
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Proof-object Part Owner-split Contract",
    "mechanics/proof-object/parts/eval-authoring/README.md",
    "mechanics/proof-object/parts/eval-contracts/README.md",
    "`## Stronger Owner Split`",
    "source proof object remains",
    "Source proof bundle meaning stays under `evals/`",
    "generated readers, reports, receipts, runtime candidates, sibling refs, quests",
    "Schema acceptance may prove metadata shape",
    "python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_object_part_owner_split",
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS = (
    "Proof-object Eval Part Names",
    "bundle-authoring",
    "eval-authoring",
    "bundle-contracts",
    "eval-contracts",
    "active directory topology",
    "source eval packages into mechanics",
    "python scripts/validate_repo.py",
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


def validate_proof_object_parts_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_PARTS_README_NAME,
        tokens=PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for forbidden_token in PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        PROOF_OBJECT_PARTS_README_NAME,
                        "proof-object parts route should use a positive operating card",
                    )
                )
    return issues


def validate_proof_object_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_OBJECT_MECHANIC_README_NAME, PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS),
        (PROOF_OBJECT_MECHANIC_AGENTS_NAME, PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (PROOF_OBJECT_MECHANIC_PARTS_NAME, PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS),
        (PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME, PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS),
        (PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME, PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS),
        (PROOF_OBJECT_MECHANIC_PROVENANCE_NAME, PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (PROOF_OBJECT_MECHANIC_DECISION_NAME, PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS),
        (PROOF_OBJECT_CONTRACT_PART_DECISION_NAME, PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS),
        (PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME, PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS),
        (PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME, PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS),
        (
            DECISION_RECORDS_README_NAME,
            (
                PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME,
                "Proof-object Part Owner-split Contract",
            ),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    issues.extend(validate_proof_object_parts_route_surface(repo_root))
    return issues
