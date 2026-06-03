from __future__ import annotations

import sys
from pathlib import Path


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


def test_portable_eval_boundary_guide_validates_current_route() -> None:
    assert validate_repo.validate_portable_eval_boundary_guide_surface(REPO_ROOT) == []


def test_portable_eval_boundary_guide_rejects_route_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.PORTABLE_EVAL_BOUNDARY_GUIDE_NAME)
    guide_path = tmp_path / validate_repo.PORTABLE_EVAL_BOUNDARY_GUIDE_NAME
    guide_path.write_text(
        guide_path.read_text(encoding="utf-8")
        + "\nDo not confuse portability with scale.\n"
        + "Could they run or adapt the bundle without hidden private knowledge?\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_portable_eval_boundary_guide_surface(tmp_path)

    assert any(
        issue.location == validate_repo.PORTABLE_EVAL_BOUNDARY_GUIDE_NAME
        and "positive review criteria" in issue.message
        and "Do not confuse portability with scale" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == validate_repo.PORTABLE_EVAL_BOUNDARY_GUIDE_NAME
        and "positive review criteria" in issue.message
        and "without hidden private knowledge" in issue.message
        for issue in issues
    )


def test_closeout_writeback_ingress_validates_current_route() -> None:
    assert validate_repo.validate_closeout_writeback_ingress_surface(REPO_ROOT) == []


def test_closeout_writeback_ingress_rejects_route_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.CLOSEOUT_WRITEBACK_INGRESS_NAME)
    copy_repo_text(tmp_path, validate_repo.CLOSEOUT_WRITEBACK_INGRESS_DECISION_NAME)
    ingress_path = tmp_path / validate_repo.CLOSEOUT_WRITEBACK_INGRESS_NAME
    ingress_path.write_text(
        ingress_path.read_text(encoding="utf-8")
        + "\nThis note remains the owner-local re-read anchor for the lane, not a shadow copy of bundle truth.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_closeout_writeback_ingress_surface(tmp_path)

    assert any(
        issue.location == validate_repo.CLOSEOUT_WRITEBACK_INGRESS_NAME
        and "re-read route" in issue.message
        and "not a shadow copy" in issue.message
        for issue in issues
    )


def test_contributing_route_validates_current_surface() -> None:
    assert validate_repo.validate_contributing_route_surface(REPO_ROOT) == []


def test_contributing_route_rejects_stale_scaffold(tmp_path: Path) -> None:
    copy_repo_text(tmp_path, "CONTRIBUTING.md")
    contributing_path = tmp_path / "CONTRIBUTING.md"
    contributing_path.write_text(
        contributing_path.read_text(encoding="utf-8")
        + "\nIf the answer depends on hidden intuition, the bundle is not ready.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_contributing_route_surface(tmp_path)

    assert any(
        issue.location == "CONTRIBUTING.md"
        and "owner routes and proof criteria" in issue.message
        and "hidden intuition" in issue.message
        for issue in issues
    )


def test_score_semantics_guide_validates_current_surface() -> None:
    assert validate_repo.validate_score_semantics_guide_surface(REPO_ROOT) == []


def test_score_semantics_guide_rejects_stale_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.SCORE_SEMANTICS_GUIDE_NAME)
    guide_path = tmp_path / validate_repo.SCORE_SEMANTICS_GUIDE_NAME
    guide_path.write_text(
        guide_path.read_text(encoding="utf-8")
        + "\nNot valid without stable comparison semantics.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_score_semantics_guide_surface(tmp_path)

    assert any(
        issue.location == validate_repo.SCORE_SEMANTICS_GUIDE_NAME
        and "interpretation route criteria" in issue.message
        and "Not valid without stable comparison semantics" in issue.message
        for issue in issues
    )


def test_eval_review_guide_validates_current_surface() -> None:
    assert validate_repo.validate_eval_review_guide_surface(REPO_ROOT) == []


def test_eval_review_guide_rejects_stale_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.EVAL_REVIEW_GUIDE_NAME)
    guide_path = tmp_path / validate_repo.EVAL_REVIEW_GUIDE_NAME
    guide_path.write_text(
        guide_path.read_text(encoding="utf-8")
        + "\nIt still reads like one useful option among peers without a crisp default-use rationale.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_eval_review_guide_surface(tmp_path)

    assert any(
        issue.location == validate_repo.EVAL_REVIEW_GUIDE_NAME
        and "maturity gap routes" in issue.message
        and "without a crisp default-use rationale" in issue.message
        for issue in issues
    )


def test_blind_spot_disclosure_guide_validates_current_surface() -> None:
    assert validate_repo.validate_blind_spot_disclosure_guide_surface(REPO_ROOT) == []


def test_blind_spot_disclosure_guide_rejects_stale_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.BLIND_SPOT_DISCLOSURE_GUIDE_NAME)
    guide_path = tmp_path / validate_repo.BLIND_SPOT_DISCLOSURE_GUIDE_NAME
    guide_path.write_text(
        guide_path.read_text(encoding="utf-8")
        + "\nWeak disclosure sounds like a generic umbrella caveat.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_blind_spot_disclosure_guide_surface(tmp_path)

    assert any(
        issue.location == validate_repo.BLIND_SPOT_DISCLOSURE_GUIDE_NAME
        and "disclosure gap routes" in issue.message
        and "Weak disclosure sounds like" in issue.message
        for issue in issues
    )
