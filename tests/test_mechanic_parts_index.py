from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import mechanic_parent_index as mechanic_parent_index_validator
from validators import mechanic_parts_index_sync as mechanic_parts_validator
from validators import comparison_spine_paths as comparison_spine_paths_validator


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


def test_mechanic_parts_index_sync_validates_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_parts_index_sync_surfaces(REPO_ROOT) == []


def test_mechanic_index_command_ownership_validates_current_routes() -> None:
    assert mechanic_parent_index_validator.validate_mechanic_index_command_ownership(REPO_ROOT) == []


def test_mechanic_lower_parts_index_operating_cards_validate_current_routes() -> None:
    assert (
        mechanic_parent_index_validator.validate_mechanic_lower_parts_index_operating_cards(
            REPO_ROOT
        )
        == []
    )


def test_mechanic_lower_parts_index_operating_cards_reject_missing_tools_row(
    tmp_path: Path,
) -> None:
    readme_name = comparison_spine_paths_validator.COMPARISON_SPINE_PARTS_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "| tools |", "| command route |", 1
        ),
        encoding="utf-8",
    )

    issues = (
        mechanic_parent_index_validator.validate_mechanic_lower_parts_index_operating_cards(
            tmp_path
        )
    )

    assert any(
        issue.location == readme_name and "| tools |" in issue.message
        for issue in issues
    )


def test_mechanic_lower_parts_index_operating_cards_reject_missing_index(
    tmp_path: Path,
) -> None:
    parts_dir = tmp_path / "mechanics" / "missing-parent" / "parts"
    parts_dir.mkdir(parents=True)

    issues = (
        mechanic_parent_index_validator.validate_mechanic_lower_parts_index_operating_cards(
            tmp_path
        )
    )

    assert any(
        issue.location == "mechanics/missing-parent/parts/README.md"
        and "lower parts index README is missing" in issue.message
        for issue in issues
    )


def test_mechanic_index_command_ownership_rejects_parts_index_commands(
    tmp_path: Path,
) -> None:
    parts_index_name = "mechanics/proof-object/PARTS.md"
    write_text(
        tmp_path / parts_index_name,
        """
        # Proof Object Parts

        ## Validation

        ```bash
        python scripts/validate_repo.py
        ```
        """,
    )

    issues = mechanic_parent_index_validator.validate_mechanic_index_command_ownership(
        tmp_path
    )

    assert any(
        issue.location == parts_index_name
        and "route executable validation commands to the nearest AGENTS.md"
        in issue.message
        for issue in issues
    )


def test_mechanic_parts_index_sync_rejects_unlisted_actual_part(
    tmp_path: Path,
) -> None:
    parts_index_name = "mechanics/agon/PARTS.md"
    write_text(
        tmp_path / parts_index_name,
        "# Agon Parts\n\nNo local parts are declared here.\n",
    )
    (tmp_path / "mechanics" / "agon" / "parts" / "new-proof").mkdir(parents=True)

    issues = mechanic_parts_validator.validate_mechanic_parts_index_sync_surfaces(tmp_path)

    assert any(
        issue.location == parts_index_name
        and "actual part directory `new-proof`" in issue.message
        for issue in issues
    )


def test_mechanic_parts_index_sync_rejects_stale_local_part_route(
    tmp_path: Path,
) -> None:
    parts_index_name = "mechanics/agon/PARTS.md"
    write_text(
        tmp_path / parts_index_name,
        "# Agon Parts\n\n- [Ghost](parts/ghost-proof/README.md)\n",
    )
    (tmp_path / "mechanics" / "agon" / "parts").mkdir(parents=True)

    issues = mechanic_parts_validator.validate_mechanic_parts_index_sync_surfaces(tmp_path)

    assert any(
        issue.location == parts_index_name
        and "stale local part route `ghost-proof`" in issue.message
        for issue in issues
    )


def test_mechanic_parts_index_sync_allows_cross_parent_reference(
    tmp_path: Path,
) -> None:
    parts_index_name = "mechanics/experience/PARTS.md"
    write_text(
        tmp_path / parts_index_name,
        """
        # Experience Parts

        | Part | Role |
        | --- | --- |
        | `adoption-federation` | Local part. |

        Reviewed runtime distillation candidate adoption routes through
        `mechanics/distillation/parts/runtime-candidate-adoption/`.
        """,
    )
    (tmp_path / "mechanics" / "experience" / "parts" / "adoption-federation").mkdir(
        parents=True
    )

    issues = mechanic_parts_validator.validate_mechanic_parts_index_sync_surfaces(tmp_path)

    assert not any(
        issue.location == parts_index_name
        and "runtime-candidate-adoption" in issue.message
        for issue in issues
    )
