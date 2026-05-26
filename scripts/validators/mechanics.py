"""Mechanics-facing root-authored surface contracts."""

from __future__ import annotations

import re
from pathlib import Path


MECHANICS_EVIDENCE_CLUSTERS = Path("mechanics/EVIDENCE_CLUSTERS.md")
ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION = "Residual Root-authored Surface Classification"
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS = (
    "Surface",
    "Root role",
    "Mechanic boundary",
    "Validation guard",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS = (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    "Root role",
    "Mechanic boundary",
    "Validation guard",
    "root-owned",
    "mechanic-owned payload",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS: dict[str, tuple[str, ...]] = {
    "docs": (
        "AGENTS.md",
        "README.md",
        "architecture/AGENT_INDEX.md",
        "architecture/AOA_EVALS_MCP_CONTRACT.md",
        "architecture/ARCHITECTURE.md",
        "architecture/LEGACY_NAMING.md",
        "architecture/PROOF_TOPOLOGY.md",
        "architecture/ROUTE_RESIDUE_GUARDS.md",
        "architecture/topology_contract.yaml",
        "guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        "guides/BASELINE_COMPARISON_GUIDE.md",
        "guides/BLIND_SPOT_DISCLOSURE_GUIDE.md",
        "guides/BOUNDARY_ROUTE_CHECKLIST.md",
        "guides/COMPARISON_SPINE_GUIDE.md",
        "guides/EVAL_PHILOSOPHY.md",
        "guides/EVAL_REVIEW_GUIDE.md",
        "guides/EVAL_RUBRIC.md",
        "guides/FIXTURE_SURFACE_GUIDE.md",
        "guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md",
        "guides/REGRESSION_PROOF_SURFACES.md",
        "guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        "guides/SCORE_SEMANTICS_GUIDE.md",
        "guides/SHARED_PROOF_INFRA_GUIDE.md",
        "guides/VERDICT_INTERPRETATION_GUIDE.md",
        "operations/AGENTS_ROOT_REFERENCE.md",
        "operations/QUESTBOOK_EVAL_INTEGRATION.md",
        "operations/RELEASING.md",
        "operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md",
    ),
    "scripts": (
        "AGENTS.md",
        "build_catalog.py",
        "eval_capsule_contract.py",
        "eval_catalog_contract.py",
        "eval_comparison_spine_contract.py",
        "eval_proof_contract_helpers.py",
        "eval_section_contract.py",
        "generate_decision_indexes.py",
        "generate_eval_report_index.py",
        "release_check.py",
        "validate_nested_agents.py",
        "validate_repo.py",
        "validate_semantic_agents.py",
        "validators/__init__.py",
        "validators/artifact_hooks.py",
        "validators/docs_decisions.py",
        "validators/docs_routes.py",
        "validators/docs_topology.py",
        "validators/eval_bundles.py",
        "validators/generated_parity.py",
        "validators/mechanics.py",
    ),
    "tests": (
        "AGENTS.md",
        "test_build_catalog.py",
        "test_current_direction_routes.py",
        "test_downstream_feed_contracts.py",
        "test_memo_contradiction_phase_alpha_gap_report.py",
        "test_memo_contradiction_phase_alpha_rerun_report.py",
        "test_memo_writeback_act_phase_alpha_report.py",
        "test_nested_agents_docs.py",
        "test_roadmap_parity.py",
        "test_validate_repo.py",
        "test_validate_semantic_agents.py",
        "test_verification_honesty_local_report.py",
    ),
}


def _markdown_heading_section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        return ""
    start = match.start()
    search_start = match.end()
    next_heading = re.search(r"^## ", text[search_start:], re.MULTILINE)
    end = len(text) if next_heading is None else search_start + next_heading.start()
    return text[start:end]


def _markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows


def validate_root_authored_surface_classification(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    evidence_path = repo_root / MECHANICS_EVIDENCE_CLUSTERS
    if not evidence_path.is_file():
        return [(MECHANICS_EVIDENCE_CLUSTERS.as_posix(), "mechanics evidence cluster map is missing")]

    text = evidence_path.read_text(encoding="utf-8")
    section = _markdown_heading_section(text, ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION)
    if not section:
        issues.append(
            (
                MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                f"mechanics evidence cluster map must contain section {ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION!r}",
            )
        )

    for token in ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS:
        if token not in section:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface classification must mention {token!r}",
                )
            )

    expected_surfaces = {
        f"{district_name}/{file_name}"
        for district_name, file_names in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
        for file_name in file_names
    }
    actual_surfaces: set[str] = set()
    for district_name, allowed_names in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items():
        district = repo_root / district_name
        if not district.is_dir():
            issues.append((district_name, "classified root-authored district is missing"))
            continue
        allowed = set(allowed_names)
        if district_name == "docs":
            actual_names = {
                path.relative_to(district).as_posix()
                for path in district.rglob("*")
                if path.is_file() and path.relative_to(district).parts[:1] != ("decisions",)
            }
        elif district_name == "scripts":
            actual_names = {
                path.relative_to(district).as_posix()
                for path in district.rglob("*")
                if path.is_file() and "__pycache__" not in path.relative_to(district).parts
            }
        else:
            actual_names = {path.name for path in district.iterdir() if path.is_file()}
        for file_name in sorted(actual_names - allowed):
            issues.append(
                (
                    f"{district_name}/{file_name}",
                    "unclassified root-authored surface must be routed, moved, or added to the residual classification ledger",
                )
            )
        for file_name in sorted(allowed - actual_names):
            issues.append(
                (
                    f"{district_name}/{file_name}",
                    "classified root-authored surface is missing; update the residual classification ledger if it moved",
                )
            )
        actual_surfaces.update(
            f"{district_name}/{file_name}"
            for file_name in actual_names
            if file_name in allowed
        )

    ledger_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(section):
        if not cells or cells[0] == "Surface":
            continue
        surface_name = cells[0].strip("`")
        if surface_name not in expected_surfaces:
            continue
        if surface_name in ledger_rows:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must appear only once in the residual classification ledger",
                )
            )
        ledger_rows[surface_name] = cells
        if len(cells) != len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS):
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must have {len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS)} columns",
                )
            )
            continue
        for column_name, cell in zip(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS[1:],
            cells[1:],
            strict=True,
        ):
            if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                issues.append(
                    (
                        MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                        f"root-authored surface `{surface_name}` row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        if "mechanic-owned payload" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its mechanic-owned payload boundary",
                )
            )
        if "root-owned" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its root-owned role",
                )
            )

    for surface_name in sorted(expected_surfaces):
        if surface_name not in ledger_rows:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must appear in the residual classification ledger",
                )
            )

    for surface_name in sorted(actual_surfaces - expected_surfaces):
        issues.append((surface_name, "unclassified root-authored surface must not remain in root districts"))

    return issues
