from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validators import mechanic_part_contract_common
from validators import mechanic_part_validation_command_tokens as command_tokens
from validators import mechanic_part_validation_commands as mechanic_parts_validator


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


def test_mechanic_part_validation_command_validates_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(REPO_ROOT) == []


def test_mechanic_part_validation_command_rejects_active_decision_command_list(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME)
    copy_repo_text(
        tmp_path,
        command_tokens.MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
    )
    copy_repo_text(tmp_path, mechanic_part_contract_common.MECHANICS_AGENTS_NAME)
    decision_path = tmp_path / command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "## Validation\n\nCurrent executable",
            "## Validation\n\n- python scripts/validate_repo.py\n\nCurrent executable",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME
        and "mechanics/AGENTS.md#validation" in issue.message
        for issue in issues
    )


def test_mechanic_part_validation_command_rejects_stale_path(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_text(
        tmp_path / readme_name,
        """
        # New Proof

        ## Validation

        ```bash
        python mechanics/agon/parts/new-proof/scripts/missing.py --check
        ```
        """,
    )

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "stale validation path `mechanics/agon/parts/new-proof/scripts/missing.py`"
        in issue.message
        for issue in issues
    )


def test_mechanic_part_validation_command_rejects_missing_python_command(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_text(
        tmp_path / readme_name,
        """
        # New Proof

        ## Validation

        Validation is manual review later.
        """,
    )

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "part validation route must list at least one python command" in issue.message
        for issue in issues
    )


def test_mechanic_part_validation_command_rejects_readme_command_blocks(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_text(
        tmp_path / readme_name,
        """
        # New Proof

        ## Validation

        ```bash
        python scripts/validate_repo.py
        ```
        """,
    )
    write_text(
        tmp_path / "mechanics/agon/parts/new-proof/VALIDATION.md",
        """
        # New Proof Validation

        Use the `new-proof` child validation block in parent parts AGENTS.
        """,
    )
    write_text(
        tmp_path / "mechanics/agon/parts/AGENTS.md",
        """
        # AGENTS.md

        ## Validation

        ### `mechanics/agon/parts/new-proof/VALIDATION.md`

        ```bash
        python scripts/validate_repo.py
        ```
        """,
    )
    write_text(tmp_path / "scripts/validate_repo.py", "# validator\n")

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "README validation section must route executable commands" in issue.message
        for issue in issues
    )


def test_mechanic_part_validation_command_rejects_absolute_path(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_text(
        tmp_path / readme_name,
        """
        # New Proof

        ## Validation

        ```bash
        python /tmp/not-repo-local.py
        ```
        """,
    )

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "repo-relative path" in issue.message
        for issue in issues
    )


def test_mechanic_part_validation_command_rejects_unanchored_payload_part(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_text(
        tmp_path / readme_name,
        """
        # New Proof

        ## Validation

        ```bash
        python scripts/validate_repo.py
        python scripts/build_catalog.py --check
        ```
        """,
    )
    write_text(
        tmp_path
        / "mechanics"
        / "agon"
        / "parts"
        / "new-proof"
        / "schemas"
        / "new-proof.schema.json",
        "{}\n",
    )
    write_text(tmp_path / "scripts" / "validate_repo.py", "# validator\n")
    write_text(tmp_path / "scripts" / "build_catalog.py", "# builder\n")

    issues = mechanic_parts_validator.validate_mechanic_part_validation_command_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "payload coverage anchor" in issue.message
        and "part-local or bundle-specific anchor" in issue.message
        for issue in issues
    )
