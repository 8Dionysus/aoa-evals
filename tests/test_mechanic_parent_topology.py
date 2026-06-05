from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validators import mechanic_legacy_archive as mechanic_legacy_archive_validator
from validators import mechanic_parent_allowlist as mechanic_parent_allowlist_validator
from validators import mechanic_parent_direction as mechanic_parent_direction_validator
from validators import mechanic_parent_guidance as mechanic_parent_guidance_validator
from validators import mechanic_part_contract_common as mechanic_parts_validator
from validators import mechanics as mechanics_validator
from validators import mechanic_provenance_bridge as mechanic_provenance_bridge_validator
from validators import root_context


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


def write_guidance_boundary_scaffold(repo_root: Path) -> None:
    write_text(
        repo_root
        / mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
        f"""
        # Mechanic Parent Guidance Boundary

        `mechanics/<parent>/docs/`
        mechanic-wide guidance
        part-owned payload
        allowlisted
        unallowlisted parent-level docs
        Titan canary guides
        {mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND}
        """,
    )
    write_text(
        repo_root / "docs" / "decisions" / "README.md",
        f"{mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME}\nMechanic Parent Guidance Boundary\n",
    )
    write_text(
        repo_root / mechanics_validator.MECHANICS_README_NAME,
        "parent-level `docs/`\npart-owned payload\n",
    )


def test_mechanic_parent_allowlist_validates_current_routes() -> None:
    assert mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(REPO_ROOT) == []


def test_mechanic_parent_allowlist_rejects_unknown_parent(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "mechanics/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        tmp_path,
        mechanic_parent_allowlist_validator.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
    )
    copy_repo_text(tmp_path, root_context.PROOF_TOPOLOGY_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        (tmp_path / "mechanics" / parent_name).mkdir(parents=True)
    write_text(
        tmp_path / "mechanics" / "repair" / "README.md",
        "# Repair\n\nThis invented parent must not become active topology.\n",
    )

    issues = mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(tmp_path)

    assert any(
        issue.location == "mechanics/repair"
        and "evidence-cluster allowlist" in issue.message
        for issue in issues
    )


def test_mechanic_parent_allowlist_rejects_missing_declared_parent(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "mechanics/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        tmp_path,
        mechanic_parent_allowlist_validator.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
    )
    copy_repo_text(tmp_path, root_context.PROOF_TOPOLOGY_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        if parent_name == "titan":
            continue
        (tmp_path / "mechanics" / parent_name).mkdir(parents=True)

    issues = mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(tmp_path)

    assert any(
        issue.location == "mechanics/titan"
        and "declared mechanic parent directory is missing" in issue.message
        for issue in issues
    )


def test_mechanic_parent_allowlist_rejects_missing_route_card(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "mechanics/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        tmp_path,
        mechanic_parent_allowlist_validator.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
    )
    copy_repo_text(tmp_path, root_context.PROOF_TOPOLOGY_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = tmp_path / "mechanics" / parent_name
        parent_root.mkdir(parents=True)
        for filename in ("AGENTS.md", "README.md", "PARTS.md"):
            write_text(parent_root / filename, f"# {filename}\n")
    (tmp_path / "mechanics" / "proof-object" / "PARTS.md").unlink()

    issues = mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(tmp_path)

    assert any(
        issue.location == "mechanics/proof-object/PARTS.md"
        and "active mechanic parent must expose" in issue.message
        for issue in issues
    )


def test_mechanic_parent_guidance_boundary_validates_current_routes() -> None:
    assert (
        mechanic_parent_guidance_validator.validate_mechanic_parent_guidance_boundary(REPO_ROOT)
        == []
    )


def test_mechanic_parent_guidance_boundary_rejects_unowned_parent_docs(
    tmp_path: Path,
) -> None:
    write_guidance_boundary_scaffold(tmp_path)
    write_text(
        tmp_path / "mechanics" / "titan" / "docs" / "TITAN_INCARNATION_CANARIES.md",
        "# Wrong parent docs\n",
    )

    issues = mechanic_parent_guidance_validator.validate_mechanic_parent_guidance_boundary(
        tmp_path
    )

    assert any(
        issue.location == "mechanics/titan/docs"
        and "parent-level docs/" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "mechanics/titan/docs/TITAN_INCARNATION_CANARIES.md"
        and "unallowlisted parent-level docs" in issue.message
        for issue in issues
    )


def test_mechanic_parent_guidance_boundary_rejects_empty_parent_docs(
    tmp_path: Path,
) -> None:
    write_guidance_boundary_scaffold(tmp_path)
    (tmp_path / "mechanics" / "checkpoint" / "docs").mkdir(parents=True)

    issues = mechanic_parent_guidance_validator.validate_mechanic_parent_guidance_boundary(
        tmp_path
    )

    assert any(
        issue.location == "mechanics/checkpoint/docs"
        and "empty parent-level docs/" in issue.message
        for issue in issues
    )


def test_mechanic_parent_guidance_boundary_rejects_thin_allowlisted_doc(
    tmp_path: Path,
) -> None:
    copy_repo_text(
        tmp_path,
        mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
    )
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_README_NAME)
    write_text(
        tmp_path / "mechanics" / "agon" / "docs" / "AGON_EVAL_OWNER_HANDOFFS.md",
        "# Agon Eval Owner Handoffs\n\nToo thin.\n",
    )
    write_text(
        tmp_path
        / "mechanics"
        / "agon"
        / "docs"
        / "AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md",
        "\n".join(mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS),
    )
    write_text(
        tmp_path / "mechanics" / "recurrence" / "docs" / "RECURRENCE_PROOF_PROGRAM.md",
        "\n".join(mechanic_parent_guidance_validator.MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS),
    )

    issues = mechanic_parent_guidance_validator.validate_mechanic_parent_guidance_boundary(
        tmp_path
    )

    assert any(
        issue.location == "mechanics/agon/docs/AGON_EVAL_OWNER_HANDOFFS.md"
        and "parent guidance content contract" in issue.message
        and "## Source Surfaces" in issue.message
        for issue in issues
    )


def test_mechanic_part_contract_files_cover_allowed_parents() -> None:
    expected = {
        f"mechanics/{parent_name}/PARTS.md"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    }

    assert set(mechanic_parts_validator.MECHANIC_PART_CONTRACT_FILES) == expected


def test_mechanic_direction_files_cover_allowed_parents() -> None:
    expected = {
        f"mechanics/{parent_name}/DIRECTION.md"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    }

    assert set(mechanic_parent_direction_validator.MECHANIC_DIRECTION_FILES) == expected


def test_mechanic_route_card_files_cover_direction_route() -> None:
    expected = {
        f"mechanics/{parent_name}/{filename}"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
        for filename in ("AGENTS.md", "README.md", "DIRECTION.md", "PARTS.md")
    }

    assert set(mechanic_parent_allowlist_validator.MECHANIC_ROUTE_CARD_FILES) == expected


def test_mechanic_parent_readme_and_agents_files_cover_allowed_parents() -> None:
    expected_readmes = {
        f"mechanics/{parent_name}/README.md"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    }
    expected_agents = {
        f"mechanics/{parent_name}/AGENTS.md"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    }

    assert set(mechanic_parent_direction_validator.MECHANIC_PARENT_README_FILES) == expected_readmes
    assert set(mechanic_parent_direction_validator.MECHANIC_PARENT_AGENTS_FILES) == expected_agents


def test_mechanic_legacy_raw_readmes_cover_allowed_parents() -> None:
    expected = {
        f"mechanics/{parent_name}/legacy/raw/README.md"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    }

    assert set(mechanic_legacy_archive_validator.MECHANIC_LEGACY_RAW_README_FILES) == expected


def test_mechanic_legacy_skeleton_files_cover_allowed_parents() -> None:
    expected = {
        f"mechanics/{parent_name}/{suffix}"
        for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
        for suffix in (
            "PROVENANCE.md",
            "legacy/README.md",
            "legacy/INDEX.md",
            "legacy/DISTILLATION_LOG.md",
            "legacy/raw/README.md",
        )
    }

    assert set(mechanic_legacy_archive_validator.MECHANIC_LEGACY_SKELETON_FILES) == expected


def test_mechanic_legacy_skeleton_rejects_missing_legacy_index(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "mechanics/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        tmp_path,
        mechanic_parent_allowlist_validator.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
    )
    copy_repo_text(
        tmp_path,
        mechanic_legacy_archive_validator.MECHANIC_LEGACY_SKELETON_DECISION_NAME,
    )
    copy_repo_text(tmp_path, root_context.PROOF_TOPOLOGY_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    for path_name in mechanic_parent_allowlist_validator.MECHANIC_ROUTE_CARD_FILES:
        write_text(tmp_path / path_name, "# Route\n")
    for path_name in mechanic_legacy_archive_validator.MECHANIC_LEGACY_SKELETON_FILES:
        write_text(tmp_path / path_name, "# Legacy\n")
    missing_path = "mechanics/questbook/legacy/INDEX.md"
    (tmp_path / missing_path).unlink()

    issues = mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(tmp_path)

    assert any(
        issue.location == missing_path
        and "archive-local legacy entry/accounting surfaces" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_readme_rejects_missing_provenance_route(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "mechanics/README.md")
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    copy_repo_text(
        tmp_path,
        mechanic_parent_allowlist_validator.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
    )
    copy_repo_text(
        tmp_path,
        mechanic_legacy_archive_validator.MECHANIC_LEGACY_SKELETON_DECISION_NAME,
    )
    copy_repo_text(tmp_path, root_context.PROOF_TOPOLOGY_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    for path_name in mechanic_parent_allowlist_validator.MECHANIC_ROUTE_CARD_FILES:
        write_text(tmp_path / path_name, "# Route\n")
    for path_name in mechanic_legacy_archive_validator.MECHANIC_LEGACY_SKELETON_FILES:
        write_text(
            tmp_path / path_name,
            "# Legacy\n\n../PROVENANCE.md\nINDEX.md\nDISTILLATION_LOG.md\nraw/README.md\narchive-local route\ncurrent active route\n",
        )
    readme_path = "mechanics/titan/legacy/README.md"
    write_text(
        tmp_path / readme_path,
        "# Titan Legacy\n\nINDEX.md\nDISTILLATION_LOG.md\nraw/README.md\narchive-local route\ncurrent active route\n",
    )

    issues = mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(tmp_path)

    assert any(
        issue.location == readme_path and "../PROVENANCE.md" in issue.message
        for issue in issues
    )


def test_mechanic_provenance_entry_files_validate_contract() -> None:
    assert (
        mechanic_provenance_bridge_validator.validate_mechanic_provenance_entry_surfaces(
            REPO_ROOT
        )
        == []
    )


def test_mechanic_parent_direction_surfaces_validate_contract() -> None:
    assert (
        mechanic_parent_direction_validator.validate_mechanic_parent_direction_surfaces(
            REPO_ROOT
        )
        == []
    )
