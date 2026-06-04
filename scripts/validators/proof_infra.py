"""Proof-infra reusable support and shared contract boundary checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import eval_catalog_contract
import eval_proof_contract_helpers


SOURCE_EVALS_DIR_NAME = "evals"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)

SHARED_PROOF_INFRA_GUIDE_NAME = "docs/guides/SHARED_PROOF_INFRA_GUIDE.md"
PROOF_INFRA_MECHANIC_README_NAME = "mechanics/proof-infra/README.md"
PROOF_INFRA_MECHANIC_AGENTS_NAME = "mechanics/proof-infra/AGENTS.md"
PROOF_INFRA_MECHANIC_PARTS_NAME = "mechanics/proof-infra/PARTS.md"
PROOF_INFRA_FIXTURE_FAMILIES_README_NAME = (
    "mechanics/proof-infra/parts/fixture-families/README.md"
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME = (
    "mechanics/proof-infra/parts/fixture-families/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/README.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py"
)
FIXTURE_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json"
)
RUNNER_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json"
)
REPORT_SUMMARY_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json"
)
PROOF_INFRA_PROVENANCE_NAME = "mechanics/proof-infra/PROVENANCE.md"
PROOF_INFRA_LEGACY_INDEX_NAME = "mechanics/proof-infra/legacy/INDEX.md"
PROOF_INFRA_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0012-proof-infra-mechanic-package.md"
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0041-proof-infra-fixture-families.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0049-proof-infra-reportable-contracts.md"
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
PROOF_INFRA_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/guides/SHARED_PROOF_INFRA_GUIDE.md",
    "fixtures/README.md",
    PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
    PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME,
    FIXTURE_CONTRACT_SCHEMA_NAME,
    RUNNER_CONTRACT_SCHEMA_NAME,
    REPORT_SUMMARY_SCHEMA_NAME,
    "reports/README.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "generated catalog `proof_artifacts`",
    "shared_fixture_family_path",
    "mechanics/proof-infra/parts/fixture-families/fixtures/",
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "report_schema_path",
    "root infrastructure districts stay route-card districts unless a part-local owner exists",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "shared proof infrastructure",
    "fixtures/contract.json",
    "runners/contract.json",
    "reports/summary.schema.json",
    "generated catalog `proof_artifacts`",
    "bundle-local interpretation",
    "parts/fixture-families/fixtures/",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "fixture-families",
    "reportable-contracts",
    "bundle support need",
    "shared_fixture_family_path",
    "runner_surface_path",
    "Fixture-family parent pressure",
    "Boundary Routes",
    "AGENTS.md#validation",
)
PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS = (
    "bundle support need",
    "public-safe reusable family",
    "shared_fixture_family_path",
    "ambiguity-bounded-v1",
    "verification-honesty-v1",
    "witness-trace-v1",
    "Family-name parent pressure",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "generic shared fixture-family support",
    "public-safe reusable support",
    "bundle-local `EVAL.md`",
    "evals/**/fixtures/contract.json",
    "shared_fixture_family_path",
    "Family-name parent pressure",
    "centralized-child-validation",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS = (
    "bundle-local runner contract",
    "reportable proof contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "fixture-contract.schema.json",
    "runner-contract.schema.json",
    "report-summary.schema.json",
    "`evals/<family>/<eval>/EVAL.md`",
    "tests/test_bounded_rubric_breakdown.py",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "reportable-contracts",
    "bundle-local runner contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "Schema weakening pressure",
    "Root alias pressure",
    "centralized-child-validation",
    "bounded rubric scorer test",
)
PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES = (
    "It does not own bundle meaning",
    "It does not own bundle-local meaning",
    "Keep the family weaker than the bundle-local claim",
    "Keep the shared runner surface weaker than bundle-local interpretation",
    "Do not add hidden benchmark cases",
    "Do not add hidden harness logic",
    "Do not recreate active root aliases",
)
PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/ambiguity-bounded-v1/README.md",
    "fixtures/verification-honesty-v1/README.md",
    "mechanics/proof-infra/parts/fixture-families/fixtures",
    "runners/reportable_proof_contract.md",
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
    "scorers/bounded_rubric_breakdown.py",
    "schemas/runner-contract.schema.json",
    "Former root paths are provenance only",
)
PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/",
    "shared proof contract",
    "generated proof_artifacts",
    "Decision 0041",
    "Decision 0049",
    "bundle-local `EVAL.md`",
    "schema weakening",
    "repo-global scoring",
)
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/fixture-families/",
    "generic shared fixture families",
    "no narrower active mechanic",
    "Root `fixtures/` remains a compatibility route card",
    "does not make fixture families stronger than bundle-local meaning",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "root `runners/`, `scorers/`, and `schemas/` remain compatibility route cards",
    "does not make reportable contracts stronger than bundle-local meaning",
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


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return {}

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_dirs.setdefault(eval_dir.name, eval_dir)
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    return discover_eval_dirs(repo_root).get(
        eval_name,
        repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
    )


def validate_proof_infra_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_INFRA_MECHANIC_README_NAME, PROOF_INFRA_MECHANIC_REQUIRED_TOKENS),
        (PROOF_INFRA_MECHANIC_AGENTS_NAME, PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (PROOF_INFRA_MECHANIC_PARTS_NAME, PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS),
        (PROOF_INFRA_FIXTURE_FAMILIES_README_NAME, PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS),
        (
            PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME,
            PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS,
        ),
        (PROOF_INFRA_PROVENANCE_NAME, PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS),
        (PROOF_INFRA_LEGACY_INDEX_NAME, PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS),
        (PROOF_INFRA_MECHANIC_DECISION_NAME, PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS),
        (
            PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME,
            PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS,
        ),
        (
            PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME,
            PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS,
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    fixture_families_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME,
        tokens=PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    reportable_contracts_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME,
        tokens=PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, text in (
        (PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME, fixture_families_agents_text),
        (PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME, reportable_contracts_agents_text),
    ):
        if not text:
            continue
        for stale_phrase in PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "proof-infra part AGENTS cards should use operating cards and owner route tables instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )
    return issues


def validate_shared_proof_infra_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    fixture_relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
    }
    runner_relevant_names = fixture_relevant_names | {
        "aoa-longitudinal-growth-snapshot",
    }
    relevant_names = fixture_relevant_names | runner_relevant_names
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / SHARED_PROOF_INFRA_GUIDE_NAME,
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    fixtures_agents_text = read_text_or_issue(
        repo_root / "fixtures" / "AGENTS.md",
        issues,
        root=repo_root,
    )
    reports_agents_text = read_text_or_issue(
        repo_root / "reports" / "AGENTS.md",
        issues,
        root=repo_root,
    )
    runner_surface_text = read_text_or_issue(
        repo_root / PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
        issues,
        root=repo_root,
    )

    if "Shared Proof Infra Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Shared Proof Infra Guide",
            )
        )
    for phrase in (
        "additional_shared_fixture_family_paths",
        "additional_paired_readout_paths",
        "shared_fixture_family_path",
        "paired_readout_path",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    SHARED_PROOF_INFRA_GUIDE_NAME,
                    f"shared proof infra guide must mention '{phrase}'",
                )
            )

    if "additional_shared_fixture_family_paths" not in fixtures_agents_text:
        issues.append(
            ValidationIssue(
                "fixtures/AGENTS.md",
                "fixtures/AGENTS.md must describe additional_shared_fixture_family_paths",
            )
        )
    if "additional_paired_readout_paths" not in reports_agents_text:
        issues.append(
            ValidationIssue(
                "reports/AGENTS.md",
                "reports/AGENTS.md must describe additional_paired_readout_paths",
            )
        )
    if "additional_paired_readout_paths" not in runner_surface_text:
        issues.append(
            ValidationIssue(
                PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
                (
                    f"{PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME} "
                    "must describe additional_paired_readout_paths"
                ),
            )
        )

    fixture_bundle_names = (
        selected_evals.intersection(fixture_relevant_names)
        if selected_evals is not None
        else fixture_relevant_names
    )
    runner_bundle_names = (
        selected_evals.intersection(runner_relevant_names)
        if selected_evals is not None
        else runner_relevant_names
    )
    fixture_contracts_with_additional = 0
    runner_contracts_with_additional = 0
    for name in fixture_bundle_names:
        fixture_payload = eval_catalog_contract.load_optional_json(
            source_eval_dir(repo_root, name) / "fixtures" / "contract.json"
        )
        fixture_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            fixture_payload if isinstance(fixture_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        )
        if fixture_paths:
            fixture_contracts_with_additional += 1
    for name in runner_bundle_names:
        runner_payload = eval_catalog_contract.load_optional_json(
            source_eval_dir(repo_root, name) / "runners" / "contract.json"
        )
        runner_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            runner_payload if isinstance(runner_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        )
        if runner_paths:
            runner_contracts_with_additional += 1

    minimum_fixture_count = 1 if selected_evals is not None and fixture_bundle_names else 2
    minimum_runner_count = 1 if selected_evals is not None and runner_bundle_names else 2
    if fixture_bundle_names and fixture_contracts_with_additional < minimum_fixture_count:
        issues.append(
            ValidationIssue(
                "fixtures/README.md",
                "shared proof infra must be exercised by fixture contracts in more than one bundle family",
            )
        )
    if runner_bundle_names and runner_contracts_with_additional < minimum_runner_count:
        issues.append(
            ValidationIssue(
                "reports/README.md",
                "shared proof infra must be exercised by runner contracts in more than one bundle family",
            )
        )
    return issues
