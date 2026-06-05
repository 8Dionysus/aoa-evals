from __future__ import annotations

from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import decision_index_surfaces
from validators.common import ValidationIssue


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def decision_index_read_models(repo_root: Path) -> list[ValidationIssue]:
    return [
        ValidationIssue(location, message)
        for location, message in decision_index_surfaces.validate_decision_index_surfaces(repo_root)
    ]


def test_decision_index_read_models_validate_current_metadata() -> None:
    assert decision_index_read_models(REPO_ROOT) == []


def test_decision_index_read_models_reject_missing_metadata(tmp_path: Path) -> None:
    copy_repo_text(
        tmp_path,
        "docs/decisions/AOA-EV-D-0107-agent-operable-docs-and-decision-indexes.md",
    )
    decision_path = (
        tmp_path
        / "docs"
        / "decisions"
        / "AOA-EV-D-0107-agent-operable-docs-and-decision-indexes.md"
    )
    text = decision_path.read_text(encoding="utf-8")
    start = text.index("\n## Index Metadata\n")
    end = text.index("\n## Context\n")
    decision_path.write_text(text[:start] + text[end:], encoding="utf-8")

    issues = decision_index_read_models(tmp_path)

    assert any("Index Metadata" in issue.message for issue in issues)
