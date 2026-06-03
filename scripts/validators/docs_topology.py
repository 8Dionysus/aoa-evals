"""Docs topology contracts for agent-operable documentation layout."""

from __future__ import annotations

from pathlib import Path

import yaml


DOCS_DIR = Path("docs")
TOPOLOGY_CONTRACT_PATH = DOCS_DIR / "architecture" / "topology_contract.yaml"

ROOT_FILES = (
    DOCS_DIR / "AGENTS.md",
    DOCS_DIR / "README.md",
)
ARCHITECTURE_FILES = (
    DOCS_DIR / "architecture" / "AGENT_INDEX.md",
    DOCS_DIR / "architecture" / "ARCHITECTURE.md",
    DOCS_DIR / "architecture" / "PROOF_TOPOLOGY.md",
    DOCS_DIR / "architecture" / "ROUTE_RESIDUE_GUARDS.md",
    DOCS_DIR / "architecture" / "LEGACY_NAMING.md",
)
GUIDE_FILES = (
    DOCS_DIR / "guides" / "EVAL_PHILOSOPHY.md",
    DOCS_DIR / "guides" / "EVAL_RUBRIC.md",
    DOCS_DIR / "guides" / "EVAL_REVIEW_GUIDE.md",
    DOCS_DIR / "guides" / "SCORE_SEMANTICS_GUIDE.md",
    DOCS_DIR / "guides" / "VERDICT_INTERPRETATION_GUIDE.md",
    DOCS_DIR / "guides" / "COMPARISON_SPINE_GUIDE.md",
    DOCS_DIR / "guides" / "REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
    DOCS_DIR / "guides" / "PORTABLE_EVAL_BOUNDARY_GUIDE.md",
    DOCS_DIR / "guides" / "FIXTURE_SURFACE_GUIDE.md",
    DOCS_DIR / "guides" / "BLIND_SPOT_DISCLOSURE_GUIDE.md",
    DOCS_DIR / "guides" / "SHARED_PROOF_INFRA_GUIDE.md",
    DOCS_DIR / "guides" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
    DOCS_DIR / "guides" / "BASELINE_COMPARISON_GUIDE.md",
    DOCS_DIR / "guides" / "REGRESSION_PROOF_SURFACES.md",
    DOCS_DIR / "guides" / "BOUNDARY_ROUTE_CHECKLIST.md",
)
OPERATION_FILES = (
    DOCS_DIR / "operations" / "RELEASING.md",
    DOCS_DIR / "operations" / "QUESTBOOK_EVAL_INTEGRATION.md",
    DOCS_DIR / "operations" / "REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md",
    DOCS_DIR / "operations" / "AGENTS_ROOT_REFERENCE.md",
)
VALIDATION_FILES = (
    DOCS_DIR / "validation" / "AGENTS.md",
    DOCS_DIR / "validation" / "VALIDATOR_TOPOLOGY.md",
    DOCS_DIR / "validation" / "COMMAND_AUTHORITY.md",
    DOCS_DIR / "validation" / "SCRIPT_TOPOLOGY.md",
)
TESTING_FILES = (
    DOCS_DIR / "testing" / "AGENTS.md",
    DOCS_DIR / "testing" / "TEST_TOPOLOGY.md",
)
EXPECTED_FLAT_DOC_FILES = ROOT_FILES
ALL_AUTHORED_DOC_FILES = (
    ROOT_FILES
    + ARCHITECTURE_FILES
    + GUIDE_FILES
    + OPERATION_FILES
    + VALIDATION_FILES
    + TESTING_FILES
)


def _as_posix(paths: tuple[Path, ...]) -> list[str]:
    return [path.as_posix() for path in paths]


def _load_contract(repo_root: Path) -> tuple[dict[str, object] | None, list[tuple[str, str]]]:
    path = repo_root / TOPOLOGY_CONTRACT_PATH
    if not path.is_file():
        return None, [(TOPOLOGY_CONTRACT_PATH.as_posix(), "docs topology contract is missing")]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None, [(TOPOLOGY_CONTRACT_PATH.as_posix(), "docs topology contract must be a mapping")]
    return payload, []


def validate_docs_topology(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    docs_root = repo_root / DOCS_DIR
    if not docs_root.is_dir():
        return [(DOCS_DIR.as_posix(), "docs directory is missing")]

    flat_files = {
        path.relative_to(repo_root).as_posix()
        for path in docs_root.iterdir()
        if path.is_file()
    }
    expected_flat = {path.as_posix() for path in EXPECTED_FLAT_DOC_FILES}
    for path_name in sorted(flat_files - expected_flat):
        issues.append((path_name, "flat docs file must move into architecture, guides, operations, or decisions"))
    for path in ALL_AUTHORED_DOC_FILES:
        if not (repo_root / path).is_file():
            issues.append((path.as_posix(), "docs topology surface is missing"))

    contract, contract_issues = _load_contract(repo_root)
    issues.extend(contract_issues)
    if contract is not None:
        expected = {
            "root_files": _as_posix(ROOT_FILES),
            "architecture": _as_posix(ARCHITECTURE_FILES),
            "guides": _as_posix(GUIDE_FILES),
            "operations": _as_posix(OPERATION_FILES),
            "validation": _as_posix(VALIDATION_FILES),
            "testing": _as_posix(TESTING_FILES),
            "decision_surface": "docs/decisions/",
        }
        for key, value in expected.items():
            if contract.get(key) != value:
                issues.append(
                    (
                        TOPOLOGY_CONTRACT_PATH.as_posix(),
                        f"{key} must match the docs topology contract",
                    )
                )

    readme = repo_root / DOCS_DIR / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for token in (
            "docs/architecture/",
            "docs/guides/",
            "docs/operations/",
            "docs/validation/",
            "docs/testing/",
            "docs/decisions/",
            "Route Residue Guards",
        ):
            if token not in text:
                issues.append(("docs/README.md", f"docs route chooser must mention {token!r}"))

    return issues
