from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_nested_agents  # noqa: E402


def materialize_valid_agents(repo_root: Path) -> None:
    for relative_path, required_phrases in validate_nested_agents.REQUIRED_AGENTS.items():
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# AGENTS.md\n\n" + "\n".join(f"- {phrase}" for phrase in required_phrases) + "\n",
            encoding="utf-8",
        )


def test_nested_agents_docs_are_present_and_shaped() -> None:
    assert validate_nested_agents.run_validation(REPO_ROOT) == []


def test_nested_agents_validator_reports_missing_file(tmp_path: Path) -> None:
    materialize_valid_agents(tmp_path)
    missing_path = tmp_path / "generated" / "AGENTS.md"
    missing_path.unlink()

    issues = validate_nested_agents.run_validation(tmp_path)

    assert ("generated/AGENTS.md", "missing required nested AGENTS.md") in issues


def test_nested_agents_validator_reports_missing_anchor_phrase(tmp_path: Path) -> None:
    materialize_valid_agents(tmp_path)
    target_path = tmp_path / "templates" / "AGENTS.md"
    target_path.write_text(
        "# AGENTS.md\n\nTemplate surface without its required anchors.\n",
        encoding="utf-8",
    )

    issues = validate_nested_agents.run_validation(tmp_path)

    assert any(
        location == "templates/AGENTS.md"
        and "EVAL.template.md" in message
        for location, message in issues
    )
