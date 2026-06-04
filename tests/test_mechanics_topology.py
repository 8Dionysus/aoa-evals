from __future__ import annotations

import textwrap
from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import mechanics as mechanics_validator


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def copy_mechanics_root_surface(repo_root: Path) -> None:
    for path_name in (
        mechanics_validator.MECHANICS_README_NAME,
        mechanics_validator.MECHANICS_AGENTS_NAME,
        mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        mechanics_validator.PART_LOCAL_TEST_PLACEMENT_DECISION_NAME,
        "docs/decisions/README.md",
        "docs/decisions/indexes/by-number.md",
    ):
        copy_repo_text(repo_root, path_name)


def copy_root_authored_classification_surface(repo_root: Path) -> None:
    copy_repo_text(repo_root, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        repo_root,
        mechanics_validator.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
    )
    copy_repo_text(repo_root, "docs/decisions/README.md")
    copy_repo_text(repo_root, mechanics_validator.PROOF_TOPOLOGY_NAME)
    copy_repo_text(repo_root, "ROADMAP.md")
    for district_name, file_names in (
        mechanics_validator.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
    ):
        for file_name in file_names:
            copy_repo_text(repo_root, f"{district_name}/{file_name}")


def test_mechanics_root_surfaces_validate_current_routes() -> None:
    assert mechanics_validator.validate_mechanics_root_surfaces(REPO_ROOT) == []


def test_mechanics_root_surfaces_reject_missing_operation_atlas_token(
    tmp_path: Path,
) -> None:
    copy_mechanics_root_surface(tmp_path)
    readme_path = tmp_path / mechanics_validator.MECHANICS_README_NAME
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "operation atlas",
            "operation map",
        ),
        encoding="utf-8",
    )

    issues = mechanics_validator.validate_mechanics_root_surfaces(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_README_NAME
        and "operation atlas" in issue.message
        for issue in issues
    )


def test_root_authored_surface_classification_validates_current_routes() -> None:
    assert mechanics_validator.validate_root_authored_surface_classification(REPO_ROOT) == []


def test_root_authored_surface_classification_rejects_unclassified_root_doc(
    tmp_path: Path,
) -> None:
    copy_root_authored_classification_surface(tmp_path)
    write_text(
        tmp_path / "docs" / "UNROUTED_MECHANIC_PAYLOAD.md",
        "# Unrouted\n",
    )

    issues = mechanics_validator.validate_root_authored_surface_classification(tmp_path)

    assert any(
        issue.location == "docs/UNROUTED_MECHANIC_PAYLOAD.md"
        and "unclassified root-authored surface" in issue.message
        for issue in issues
    )


def test_root_authored_surface_classification_rejects_missing_ledger_row(
    tmp_path: Path,
) -> None:
    copy_root_authored_classification_surface(tmp_path)
    evidence_path = tmp_path / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_text = "\n".join(
        line
        for line in evidence_path.read_text(encoding="utf-8").splitlines()
        if not line.startswith("| `tests/test_mechanics_topology.py` |")
    )
    evidence_path.write_text(evidence_text, encoding="utf-8")

    issues = mechanics_validator.validate_root_authored_surface_classification(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "root-authored surface `tests/test_mechanics_topology.py` must appear"
        in issue.message
        for issue in issues
    )


def test_root_authored_surface_classification_rejects_empty_boundary(
    tmp_path: Path,
) -> None:
    copy_root_authored_classification_surface(tmp_path)
    evidence_path = tmp_path / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "mechanic-owned payload validators may live part-local, while this file guards cross-repo topology",
            "TBD",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanics_validator.validate_root_authored_surface_classification(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "root-authored surface `scripts/validate_repo.py` row must fill `Mechanic boundary`"
        in issue.message
        for issue in issues
    )
