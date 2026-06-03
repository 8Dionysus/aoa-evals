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


def write_legacy_single_bridge_scaffold(repo_root: Path) -> None:
    write_text(
        repo_root / validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
        f"""
        # Mechanic Legacy Single Bridge

        `PROVENANCE.md`
        single controlled bridge
        active mechanic surfaces
        legacy archive
        active surface
        direct `legacy/INDEX.md`
        direct `legacy/raw`
        JSON
        YAML
        {validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND}
        """,
    )
    write_text(
        repo_root / "docs" / "decisions" / "README.md",
        f"{validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME}\nMechanic Legacy Single Bridge\n",
    )
    for path_name in (
        validate_repo.MECHANICS_README_NAME,
        validate_repo.PROOF_TOPOLOGY_NAME,
        validate_repo.LEGACY_NAMING_NAME,
    ):
        write_text(
            repo_root / path_name,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
    write_text(
        repo_root / "ROADMAP.md",
        "Mechanic Legacy Single Bridge\nsingle controlled bridge\nactive mechanic surfaces\n",
    )


def test_mechanic_legacy_single_bridge_validates_current_routes() -> None:
    assert validate_repo.validate_mechanic_legacy_single_bridge_surfaces(REPO_ROOT) == []


def test_mechanic_legacy_single_bridge_rejects_active_direct_legacy_index(
    tmp_path: Path,
) -> None:
    write_legacy_single_bridge_scaffold(tmp_path)
    readme_name = "mechanics/titan/README.md"
    write_text(
        tmp_path / readme_name,
        "# Titan\n\nUse `legacy/INDEX.md` directly for old canary lookup.\n",
    )

    issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "route legacy archive details through PROVENANCE.md" in issue.message
        and "legacy/INDEX.md" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_single_bridge_rejects_active_direct_legacy_raw_in_json(
    tmp_path: Path,
) -> None:
    for path_name in (
        validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
        "docs/decisions/README.md",
        validate_repo.MECHANICS_README_NAME,
        validate_repo.PROOF_TOPOLOGY_NAME,
        validate_repo.LEGACY_NAMING_NAME,
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    manifest_name = "mechanics/titan/parts/seed-boundary/manifests/demo.json"
    write_text(
        tmp_path / manifest_name,
        '{"surfaces": ["mechanics/titan/legacy/raw/old-canary.md"]}\n',
    )

    issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

    assert any(
        issue.location == manifest_name
        and "route legacy archive details through PROVENANCE.md" in issue.message
        and "legacy/raw/" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_single_bridge_rejects_provenance_archive_detail(
    tmp_path: Path,
) -> None:
    write_legacy_single_bridge_scaffold(tmp_path)
    write_text(
        tmp_path / "mechanics" / "titan" / "README.md",
        "# Titan\n\nUse `PROVENANCE.md` for legacy or former placement.\n",
    )
    write_text(
        tmp_path / "mechanics" / "titan" / "PROVENANCE.md",
        "# Titan Provenance\n\nUse `legacy/INDEX.md` and `legacy/raw/README.md` here.\n",
    )

    issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/titan/PROVENANCE.md"
        and "without carrying archive detail" in issue.message
        for issue in issues
    )


def test_mechanic_provenance_bridge_posture_validates_current_routes() -> None:
    assert (
        validate_repo.validate_mechanic_provenance_bridge_posture_surfaces(REPO_ROOT)
        == []
    )


def test_mechanic_provenance_bridge_posture_rejects_missing_active_first_contract(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.MECHANIC_PROVENANCE_FILES:
        copy_repo_text(tmp_path, path_name)
    for path_name in (
        validate_repo.MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
        "docs/decisions/README.md",
        validate_repo.MECHANICS_README_NAME,
        validate_repo.PROOF_TOPOLOGY_NAME,
        validate_repo.LEGACY_NAMING_NAME,
        "DESIGN.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)

    broken_path = "mechanics/titan/PROVENANCE.md"
    write_text(
        tmp_path / broken_path,
        "# Titan Provenance\n\nUse `legacy/INDEX.md` for old canaries.\n",
    )

    issues = validate_repo.validate_mechanic_provenance_bridge_posture_surfaces(tmp_path)

    assert any(
        issue.location == broken_path
        and "active-to-archive bridge" in issue.message
        for issue in issues
    )
