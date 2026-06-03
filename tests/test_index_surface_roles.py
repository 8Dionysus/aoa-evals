from __future__ import annotations

from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def test_index_surface_roles_validate_current_headings() -> None:
    assert validate_repo.validate_index_surface_roles(REPO_ROOT) == []


def test_index_surface_roles_reject_generic_decision_heading(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
        copy_repo_text(tmp_path, path_name)
    decision_index_path = tmp_path / "docs" / "decisions" / "README.md"
    decision_index_path.write_text(
        decision_index_path.read_text(encoding="utf-8").replace(
            "# Decision Records Index",
            "# Decisions",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_index_surface_roles(tmp_path)

    assert any(
        issue.location == "docs/decisions/README.md"
        and "# Decision Records Index" in issue.message
        for issue in issues
    )


def test_index_surface_roles_reject_generic_mechanics_heading(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
        copy_repo_text(tmp_path, path_name)
    mechanics_index_path = tmp_path / "mechanics" / "README.md"
    mechanics_index_path.write_text(
        mechanics_index_path.read_text(encoding="utf-8").replace(
            "# Mechanics Operation Atlas",
            "# Mechanics",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_index_surface_roles(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANICS_README_NAME
        and "# Mechanics Operation Atlas" in issue.message
        for issue in issues
    )


def test_index_surface_roles_reject_generic_eval_index_heading(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
        copy_repo_text(tmp_path, path_name)
    eval_index_path = tmp_path / validate_repo.EVAL_INDEX_NAME
    eval_index_path.write_text(
        eval_index_path.read_text(encoding="utf-8").replace(
            "# Eval Bundle Index",
            "# EVAL_INDEX",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_index_surface_roles(tmp_path)

    assert any(
        issue.location == validate_repo.EVAL_INDEX_NAME
        and "# Eval Bundle Index" in issue.message
        for issue in issues
    )


def test_mechanic_index_surface_roles_validate_current_headings() -> None:
    assert validate_repo.validate_mechanic_index_surface_roles(REPO_ROOT) == []


def test_mechanic_index_surface_roles_reject_generic_parts_heading(
    tmp_path: Path,
) -> None:
    for path_name in (
        "mechanics/proof-object/PARTS.md",
        "mechanics/proof-object/parts/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    parts_index_path = tmp_path / "mechanics" / "proof-object" / "PARTS.md"
    parts_index_path.write_text(
        parts_index_path.read_text(encoding="utf-8").replace(
            "# Proof Object / Part Index",
            "# Proof Object Parts",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_index_surface_roles(tmp_path)

    assert any(
        issue.location == "mechanics/proof-object/PARTS.md"
        and "Index" in issue.message
        for issue in issues
    )


def test_mechanic_index_surface_roles_reject_generic_parts_route_heading(
    tmp_path: Path,
) -> None:
    for path_name in (
        "mechanics/proof-object/PARTS.md",
        "mechanics/proof-object/parts/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    parts_route_path = tmp_path / "mechanics" / "proof-object" / "parts" / "README.md"
    parts_route_path.write_text(
        parts_route_path.read_text(encoding="utf-8").replace(
            "# Proof Object / Parts Route",
            "# Proof Object Parts",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_index_surface_roles(tmp_path)

    assert any(
        issue.location == "mechanics/proof-object/parts/README.md"
        and "Route" in issue.message
        for issue in issues
    )
