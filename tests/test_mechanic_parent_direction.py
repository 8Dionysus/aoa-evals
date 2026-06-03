from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo


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


def write_valid_direction_files(repo_root: Path) -> None:
    for path_name in validate_repo.MECHANIC_DIRECTION_FILES:
        write_text(
            repo_root / path_name,
            "# Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n`legacy/`\narchive-local route\n\n## Current contour\n\nNow.\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
        )


def write_valid_parent_readmes(repo_root: Path) -> None:
    for path_name in validate_repo.MECHANIC_PARENT_README_FILES:
        write_text(
            repo_root / path_name,
            "# Parent\n\n## Entry Route\n\n[DIRECTION.md](DIRECTION.md)\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\nactive-to-archive bridge\n",
        )


def write_valid_parent_agents(repo_root: Path) -> None:
    for parent_name, path_name in zip(
        validate_repo.ACTIVE_MECHANIC_PARENT_NAMES,
        validate_repo.MECHANIC_PARENT_AGENTS_FILES,
        strict=True,
    ):
        write_text(
            repo_root / path_name,
            f"# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\nactive-to-archive bridge\n`mechanics/{parent_name}/DIRECTION.md`\n`mechanics/{parent_name}/PARTS.md`\n`mechanics/{parent_name}/PROVENANCE.md`\n",
        )


def write_valid_provenance_files(repo_root: Path) -> None:
    for path_name in validate_repo.MECHANIC_PROVENANCE_FILES:
        write_text(
            repo_root / path_name,
            "# Provenance\n\nactive route\nlegacy/README.md\nlegacy archive owns its own details\narchive details stay out\n",
        )


def test_mechanic_parent_direction_rejects_missing_current_contour(
    tmp_path: Path,
) -> None:
    write_valid_direction_files(tmp_path)
    direction_path = "mechanics/titan/DIRECTION.md"
    write_text(
        tmp_path / direction_path,
        "# Titan Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == direction_path and "## Current contour" in issue.message
        for issue in issues
    )


def test_mechanic_parent_direction_rejects_missing_readme_entry_route(
    tmp_path: Path,
) -> None:
    write_valid_direction_files(tmp_path)
    write_valid_parent_readmes(tmp_path)
    write_valid_parent_agents(tmp_path)
    readme_path = "mechanics/titan/README.md"
    write_text(
        tmp_path / readme_path,
        "# Titan\n\n## Entry Route\n\ncurrent operating direction\nactive-to-archive bridge\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\n",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == readme_path and "[DIRECTION.md](DIRECTION.md)" in issue.message
        for issue in issues
    )


def test_mechanic_parent_direction_rejects_missing_readme_role_and_next_route(
    tmp_path: Path,
) -> None:
    write_valid_direction_files(tmp_path)
    for path_name in validate_repo.MECHANIC_PARENT_README_FILES:
        write_text(
            tmp_path / path_name,
            "# Parent\n\n## Entry Route\n\n[DIRECTION.md](DIRECTION.md)\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\nactive-to-archive bridge\n\n## Owned Operation\n\nRoute proof work.\n\n## Validation\n\n[AGENTS](AGENTS.md#validation)\n",
        )
    write_valid_parent_agents(tmp_path)

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/titan/README.md" and "## Role" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "mechanics/titan/README.md" and "## Next Route" in issue.message
        for issue in issues
    )


def test_mechanic_parent_readme_rejects_stale_stop_line_lead_in(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/recurrence/README.md"
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "Boundary routes keep recurrence proof pressure with the owner that can act on\nit:",
            validate_repo.MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "old package-claim scaffold" in issue.message
        for issue in issues
    )


def test_mechanic_parent_readme_rejects_stale_provenance_side_path(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/titan/README.md"
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "[PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.",
            "[PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "stale only-when legacy side-path wording" in issue.message
        for issue in issues
    )


def test_mechanic_parent_direction_rejects_stale_negative_route_language(
    tmp_path: Path,
) -> None:
    readme_name = validate_repo.AGON_MECHANIC_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "The active\npackage name stays `mechanics/agon/`.",
            "They do not define the active package name.",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "positive owner-route language" in issue.message
        for issue in issues
    )


def test_mechanic_parent_agents_rejects_stale_provenance_side_path(
    tmp_path: Path,
) -> None:
    agents_name = "mechanics/titan/AGENTS.md"
    copy_repo_text(tmp_path, agents_name)
    agents_path = tmp_path / agents_name
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "`mechanics/titan/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.",
            "`mechanics/titan/PROVENANCE.md` only when legacy or former placement matters.",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == agents_name
        and "stale only-when legacy side-path wording" in issue.message
        for issue in issues
    )


def test_mechanic_parent_direction_rejects_missing_agents_entry_route(
    tmp_path: Path,
) -> None:
    write_valid_direction_files(tmp_path)
    write_valid_parent_readmes(tmp_path)
    write_valid_parent_agents(tmp_path)
    agents_path = "mechanics/titan/AGENTS.md"
    write_text(
        tmp_path / agents_path,
        "# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\nactive-to-archive bridge\n`mechanics/titan/PARTS.md`\n`mechanics/titan/PROVENANCE.md`\n",
    )

    issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

    assert any(
        issue.location == agents_path
        and "`mechanics/titan/DIRECTION.md`" in issue.message
        for issue in issues
    )


def test_mechanic_provenance_entry_rejects_missing_legacy_readme_bridge(
    tmp_path: Path,
) -> None:
    write_valid_provenance_files(tmp_path)
    readme_path = "mechanics/titan/PROVENANCE.md"
    write_text(
        tmp_path / readme_path,
        "# Titan Provenance\n\nactive route\nlegacy archive owns its own details\narchive details stay out\n",
    )

    issues = validate_repo.validate_mechanic_provenance_entry_surfaces(tmp_path)

    assert any(
        issue.location == readme_path and "legacy/README.md" in issue.message
        for issue in issues
    )


def test_mechanic_provenance_entry_rejects_archive_detail_in_bridge(
    tmp_path: Path,
) -> None:
    write_valid_provenance_files(tmp_path)
    readme_path = "mechanics/titan/PROVENANCE.md"
    write_text(
        tmp_path / readme_path,
        "# Titan Provenance\n\nactive route\nlegacy/README.md\nlegacy/INDEX.md\nlegacy archive owns its own details\narchive details stay out\n",
    )

    issues = validate_repo.validate_mechanic_provenance_entry_surfaces(tmp_path)

    assert any(
        issue.location == readme_path
        and "without carrying archive detail" in issue.message
        for issue in issues
    )
