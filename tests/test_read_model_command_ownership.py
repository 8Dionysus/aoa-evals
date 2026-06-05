from __future__ import annotations

import textwrap
from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


from validators import root_read_model_commands as root_read_model_commands_validator



def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def test_read_model_command_ownership_validates_current_routes() -> None:
    assert root_read_model_commands_validator.validate_read_model_command_ownership(REPO_ROOT) == []


def test_read_model_command_ownership_rejects_command_block(
    tmp_path: Path,
) -> None:
    readme_name = "docs/architecture/PROOF_TOPOLOGY.md"
    write_text(
        tmp_path / readme_name,
        """
        # Proof Topology

        ## Validation

        ```bash
        python scripts/validate_repo.py
        ```
        """,
    )

    issues = root_read_model_commands_validator.validate_read_model_command_ownership(tmp_path)

    assert any(
        issue.location == readme_name
        and "route executable validation commands to the nearest AGENTS.md"
        in issue.message
        for issue in issues
    )


def test_read_model_command_ownership_rejects_bullet_command(
    tmp_path: Path,
) -> None:
    readme_name = "docs/operations/RELEASING.md"
    write_text(
        tmp_path / readme_name,
        """
        # Releasing

        ## Local release checks

        - `python scripts/release_check.py`
        """,
    )

    issues = root_read_model_commands_validator.validate_read_model_command_ownership(tmp_path)

    assert any(
        issue.location == readme_name and "python command lines" in issue.message
        for issue in issues
    )


def test_read_model_command_ownership_rejects_eval_selection_command(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        "# Selection\n\nValidate with `python scripts/validate_repo.py --eval sample`.\n",
    )

    issues = root_read_model_commands_validator.validate_read_model_command_ownership(tmp_path)

    assert any(
        issue.location == "EVAL_SELECTION.md"
        and "nearest AGENTS.md" in issue.message
        for issue in issues
    )
