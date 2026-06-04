"""Proof-loop route-smoke and bundle-local report boundary contracts."""

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

PROOF_INFRA_MECHANIC_README_NAME = "mechanics/proof-infra/README.md"
PROOF_LOOP_MECHANIC_README_NAME = "mechanics/proof-loop/README.md"
PROOF_LOOP_MECHANIC_AGENTS_NAME = "mechanics/proof-loop/AGENTS.md"
PROOF_LOOP_MECHANIC_PARTS_NAME = "mechanics/proof-loop/PARTS.md"
PROOF_LOOP_MECHANIC_PROVENANCE_NAME = "mechanics/proof-loop/PROVENANCE.md"
PROOF_LOOP_LEGACY_INDEX_NAME = "mechanics/proof-loop/legacy/INDEX.md"
PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME = "mechanics/proof-loop/legacy/DISTILLATION_LOG.md"
PROOF_LOOP_LEGACY_RAW_README_NAME = "mechanics/proof-loop/legacy/raw/README.md"
PROOF_LOOP_PARTS_README_NAME = "mechanics/proof-loop/parts/README.md"
PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME = "mechanics/proof-loop/parts/route-smoke/README.md"
PROOF_LOOP_SMOKE_REPORT_NAME = (
    "mechanics/proof-loop/parts/route-smoke/reports/"
    "proof-loop-local-route-smoke-v1.md"
)
PROOF_LOOP_SMOKE_DECISION_NAME = "docs/decisions/AOA-EV-D-0020-proof-loop-local-smoke-report.md"
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0030-proof-loop-route-smoke-part.md"
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0060-proof-loop-route-smoke-contract.md"
)
PROOF_LOOP_LOCAL_REPORT_NAME = (
    "evals/workflow/aoa-verification-honesty/reports/"
    "aoa-evals-slice-19-lifecycle-contract.report.json"
)
PROOF_LOOP_LOCAL_REPORT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0022-proof-loop-bundle-local-report.md"
)
PROOF_LOOP_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0019-proof-loop-mechanic-package.md"

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
PROOF_LOOP_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Step Owners",
    "EVAL_SELECTION.md",
    "mechanics/proof-object/",
    "mechanics/proof-infra/",
    "mechanics/audit/",
    "mechanics/publication-receipts/",
    "mechanics/boundary-bridge/",
    "PARTS.md",
    "route-smoke",
    "generated readers remain derived readers below bundle-local proof authority",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "active proof-loop route",
    "source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Keep generated readers subordinate",
    "Keep receipts below reviewed reports",
    "mechanics/proof-loop/PARTS.md",
    "Keep route-smoke reports",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-loop/",
    "pick proof question",
    "existing mechanics",
    "does not own bundle meaning",
    "does not create runtime dispatch",
    "does not allow receipts",
)
PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS = (
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "docs/decisions/AOA-EV-D-0020-proof-loop-local-smoke-report.md",
    "docs/decisions/AOA-EV-D-0030-proof-loop-route-smoke-part.md",
    "Former root report paths are provenance only",
)
PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-loop",
    "route-smoke",
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "Current route:",
    "new proof-loop route-smoke work starts in the owning active part",
)
PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active proof-loop",
)
PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS = (
    "bounded route-smoke",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "aoa-verification-honesty",
    "no eval result receipt",
    "no bundle promotion",
    "defer/handoff",
    "No runtime candidate packet is accepted by this smoke",
    "No sibling proof ref is required by this smoke",
    "parts/AGENTS.md#validation",
)
PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "aoa-verification-honesty",
    "bounded route-smoke",
    "no eval result receipt",
    "no bundle promotion",
    "no runtime dispatch",
    "no sibling-owner approval",
)
PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "Proof Loop / Part Index",
    "proof question -> selection route -> source proof object",
    "route-smoke",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "bounded part contracts inside the parent mechanic",
    "no eval result receipt",
)
PROOF_LOOP_PARTS_README_REQUIRED_TOKENS = (
    "Proof Loop / Parts Route",
    "## Operating Card",
    "| role | lower index for active proof-loop part artifacts |",
    "## Active Parts",
    "route-smoke/README.md",
    "## Owner Pressure Routes",
    "| source proof object meaning | `mechanics/proof-object/` plus affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |",
    "| support contract pressure | `mechanics/proof-infra/` |",
    "| candidate evidence packet | `mechanics/audit/` |",
    "| receipt publication or receipt-intake pressure | `mechanics/publication-receipts/` |",
    "## Part Admission Route",
    "| one local loop path needs public-safe routeability proof | bounded route-smoke report with no receipt publication | `route-smoke/README.md` |",
    "mechanics/proof-loop/parts/AGENTS.md#validation",
)
PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS = (
    "Route Smoke Part",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "bounded route-smoke report artifact",
    "no eval result receipt",
    "route-smoke report read as eval-result run",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "route-smoke",
    "root `reports/`",
    "mechanics/proof-loop/PARTS.md",
    "does not create an eval result receipt",
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Proof Loop Route-Smoke Contract",
    "mechanics/proof-loop/parts/route-smoke/README.md",
    "part-level contract",
    "stronger owner split",
    "stop-lines",
    "no eval result receipt",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS = (
    "aoa-verification-honesty",
    "aoa-evals slice 19 quest lifecycle contract",
    "No receipt publisher run was attempted",
    "No runtime mutation or machine maintenance check was attempted",
    "`python scripts/release_check.py`",
)
PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_LOCAL_REPORT_NAME,
    "bundle-local report",
    "reports/summary.schema.json",
    "validate every bundle-local `*.report.json`",
    "no eval result receipt",
    "no bundle status is promoted",
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


def markdown_python_commands(section: str) -> list[str]:
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


def validate_proof_loop_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_LOOP_MECHANIC_README_NAME, PROOF_LOOP_MECHANIC_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_AGENTS_NAME, PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_PARTS_NAME, PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS),
        (PROOF_LOOP_PARTS_README_NAME, PROOF_LOOP_PARTS_README_REQUIRED_TOKENS),
        (PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME, PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS),
        (
            PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME,
            PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS,
        ),
        (
            DECISION_RECORDS_README_NAME,
            (PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME, "Proof Loop Route-Smoke Contract"),
        ),
        (PROOF_LOOP_MECHANIC_PROVENANCE_NAME, PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_INDEX_NAME, PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME, PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_RAW_README_NAME, PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_DECISION_NAME, PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    issues.extend(validate_proof_loop_smoke_report_surfaces(repo_root))
    issues.extend(validate_proof_loop_local_report_surfaces(repo_root))
    return issues


def validate_proof_loop_smoke_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    report_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_SMOKE_REPORT_NAME,
        tokens=PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS,
        issues=issues,
    )
    if report_text and markdown_python_commands(report_text):
        issues.append(
            ValidationIssue(
                PROOF_LOOP_SMOKE_REPORT_NAME,
                "bounded route-smoke report must route executable validation commands to mechanics/proof-loop/parts/AGENTS.md",
            )
        )
    for path_name, tokens in (
        (PROOF_LOOP_SMOKE_DECISION_NAME, PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS),
        (PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME, PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS),
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (PROOF_LOOP_SMOKE_REPORT_NAME, "bounded route-smoke", "no eval result receipt"),
        ),
        ("reports/README.md", (PROOF_LOOP_SMOKE_REPORT_NAME, "route-smoke report")),
        (
            DECISION_RECORDS_README_NAME,
            (
                PROOF_LOOP_SMOKE_DECISION_NAME,
                PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME,
                "Further proof-loop examples",
            ),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues


def validate_proof_loop_local_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_LOOP_LOCAL_REPORT_NAME, PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS),
        (PROOF_LOOP_LOCAL_REPORT_DECISION_NAME, PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS),
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (PROOF_LOOP_LOCAL_REPORT_NAME, "First Bundle-Local Report", "no eval result receipt"),
        ),
        (
            PROOF_INFRA_MECHANIC_README_NAME,
            ("`*.report.json`", "`evals/<family>/<eval>/reports/summary.schema.json`"),
        ),
        ("ROADMAP.md", ("Proof loop route", "mechanics/proof-loop/README.md")),
        ("CHANGELOG.md", (PROOF_LOOP_LOCAL_REPORT_NAME, "bundle-local report validation")),
        (DECISION_RECORDS_README_NAME, (PROOF_LOOP_LOCAL_REPORT_DECISION_NAME, "Further proof-loop examples")),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues
