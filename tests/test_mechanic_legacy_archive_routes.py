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


def test_mechanic_legacy_readmes_validate_entry_contract() -> None:
    legacy_readmes = set(validate_repo.MECHANIC_LEGACY_README_FILES)

    assert not any(
        issue.location in legacy_readmes
        for issue in validate_repo.validate_mechanics_parent_allowlist(REPO_ROOT)
    )


def test_mechanic_legacy_archive_route_language_validates_current_routes() -> None:
    assert validate_repo.validate_mechanic_legacy_archive_route_language(REPO_ROOT) == []


def test_mechanic_legacy_raw_payload_accounting_validates_current_routes() -> None:
    assert validate_repo.validate_mechanic_legacy_raw_payload_accounting(REPO_ROOT) == []


def test_active_legacy_parent_wording_validates_current_routes() -> None:
    assert validate_repo.validate_active_legacy_parent_wording(REPO_ROOT) == []


def test_mechanic_legacy_archive_route_language_rejects_command_blocks(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES:
        write_text(tmp_path / path_name, "# Legacy\n\nCurrent route.\n")
    target = "mechanics/questbook/legacy/INDEX.md"
    write_text(
        tmp_path / target,
        "# Legacy\n\n```bash\npython scripts/validate_repo.py\n```\n",
    )

    issues = validate_repo.validate_mechanic_legacy_archive_route_language(tmp_path)

    assert any(
        issue.location == target and "AGENTS.md" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_archive_route_language_rejects_negative_scaffold(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES:
        write_text(tmp_path / path_name, "# Legacy\n\nCurrent route.\n")
    target = "mechanics/proof-object/legacy/DISTILLATION_LOG.md"
    write_text(
        tmp_path / target,
        "# Legacy\n\nIt is not a changelog.\n",
    )

    issues = validate_repo.validate_mechanic_legacy_archive_route_language(tmp_path)

    assert any(
        issue.location == target and "current active route expectations" in issue.message
        for issue in issues
    )


def test_active_legacy_parent_wording_rejects_old_parent_forms(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN:
        copy_repo_text(tmp_path, path_name)
    for path_name in (
        validate_repo.ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
        "docs/decisions/README.md",
        "ROADMAP.md",
        "CHANGELOG.md",
    ):
        copy_repo_text(tmp_path, path_name)
    audit_parts = tmp_path / "mechanics" / "audit" / "parts" / "README.md"
    audit_parts.write_text(
        "# Runtime Evidence Parts\n\n`runtime-evidence` mechanic\n",
        encoding="utf-8",
    )
    titan_readme = tmp_path / "mechanics" / "titan" / "README.md"
    titan_readme.write_text("This package routes Titan canary work.\n", encoding="utf-8")
    titan_parts = tmp_path / "mechanics" / "titan" / "parts" / "README.md"
    titan_parts.write_text(
        "# Titan Canaries Parts\n\nTitan-canary-owned artifacts.\n",
        encoding="utf-8",
    )
    reports_readme = tmp_path / "reports" / "README.md"
    reports_readme.write_text(
        "Proof-release reports no longer live here.\n",
        encoding="utf-8",
    )
    releasing = tmp_path / "docs" / "operations" / "RELEASING.md"
    releasing.write_text(
        "runtime-evidence example refs should not sound like an active route.\n",
        encoding="utf-8",
    )
    boundary_bridge = tmp_path / "mechanics" / "boundary-bridge" / "README.md"
    boundary_bridge.write_text(
        "runtime-evidence schema refs should be runtime evidence schema refs.\n",
        encoding="utf-8",
    )

    issues = validate_repo.validate_active_legacy_parent_wording(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/README.md"
        and "legacy parent form" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "reports/README.md"
        and "legacy parent form" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "docs/operations/RELEASING.md"
        and "runtime-evidence example refs" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "mechanics/boundary-bridge/README.md"
        and "runtime-evidence schema refs" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "mechanics/titan/README.md"
        and "legacy parent form" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "mechanics/titan/parts/README.md"
        and "legacy parent form" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_raw_payload_accounting_rejects_unindexed_payload(
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "mechanics" / "titan" / "legacy"
    write_text(legacy_root / "INDEX.md", "# Titan Legacy Index\n")
    write_text(legacy_root / "DISTILLATION_LOG.md", "# Titan Distillation Log\n")
    write_text(legacy_root / "raw" / "README.md", "# Raw\n")
    write_text(
        legacy_root / "raw" / "forgotten-placement.md",
        "# Forgotten Placement\n\nThis raw payload has no accounting link.\n",
    )

    issues = validate_repo.validate_mechanic_legacy_raw_payload_accounting(tmp_path)

    assert any(
        issue.location == "mechanics/titan/legacy/raw/forgotten-placement.md"
        and "archive-local index or accounting log" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_raw_payload_accounting_rejects_raw_only_index_route(
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "mechanics" / "titan" / "legacy"
    write_text(
        legacy_root / "INDEX.md",
        (
            "# Titan Legacy Index\n\n"
            "| Former source | Preserved raw | Current active route | Posture |\n"
            "| --- | --- | --- | --- |\n"
            "| `evals/` | [raw/old.md](raw/old.md) | `legacy/raw/old.md` | historical placement |\n"
        ),
    )
    write_text(legacy_root / "DISTILLATION_LOG.md", "# Titan Distillation Log\nold.md\n")
    write_text(legacy_root / "raw" / "old.md", "# Old Placement\n")

    issues = validate_repo.validate_mechanic_legacy_raw_payload_accounting(tmp_path)

    assert any(
        issue.location == "mechanics/titan/legacy/raw/old.md"
        and "current active part route" in issue.message
        and "raw-only archive route" in issue.message
        for issue in issues
    )


def test_mechanic_legacy_raw_payload_accounting_rejects_parent_only_index_route(
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "mechanics" / "titan" / "legacy"
    write_text(
        legacy_root / "INDEX.md",
        (
            "# Titan Legacy Index\n\n"
            "| Former source | Preserved raw | Current active route | Posture |\n"
            "| --- | --- | --- | --- |\n"
            "| `evals/` | [raw/old.md](raw/old.md) | `mechanics/titan/` | historical placement |\n"
        ),
    )
    write_text(legacy_root / "DISTILLATION_LOG.md", "# Titan Distillation Log\nold.md\n")
    write_text(legacy_root / "raw" / "old.md", "# Old Placement\n")

    issues = validate_repo.validate_mechanic_legacy_raw_payload_accounting(tmp_path)

    assert any(
        issue.location == "mechanics/titan/legacy/raw/old.md"
        and "active part route" in issue.message
        for issue in issues
    )


def test_audit_legacy_index_rejects_missing_runtime_evidence_lineage(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.AUDIT_LEGACY_INDEX_NAME)
    index_path = tmp_path / validate_repo.AUDIT_LEGACY_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "mechanics/runtime-evidence/",
            "mechanics/old-runtime-packets/",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.AUDIT_LEGACY_INDEX_NAME
        and "mechanics/runtime-evidence/" in issue.message
        for issue in issues
    )


def test_release_support_legacy_index_rejects_missing_proof_release_lineage(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.RELEASE_SUPPORT_LEGACY_INDEX_NAME)
    index_path = tmp_path / validate_repo.RELEASE_SUPPORT_LEGACY_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "mechanics/proof-release/",
            "mechanics/old-release-proof/",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.RELEASE_SUPPORT_LEGACY_INDEX_NAME
        and "mechanics/proof-release/" in issue.message
        for issue in issues
    )


def test_proof_loop_legacy_index_rejects_missing_root_report_lineage(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.PROOF_LOOP_LEGACY_INDEX_NAME)
    index_path = tmp_path / validate_repo.PROOF_LOOP_LEGACY_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "reports/proof-loop-local-route-smoke-v1.md",
            "reports/old-proof-loop-smoke.md",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.PROOF_LOOP_LEGACY_INDEX_NAME
        and "reports/proof-loop-local-route-smoke-v1.md" in issue.message
        for issue in issues
    )


def test_publication_receipts_legacy_index_rejects_missing_root_guide_lineage(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME)
    index_path = tmp_path / validate_repo.PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "docs/EVAL_RESULT_RECEIPT_GUIDE.md",
            "docs/OLD_RECEIPT_GUIDE.md",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME
        and "docs/EVAL_RESULT_RECEIPT_GUIDE.md" in issue.message
        for issue in issues
    )


def test_boundary_bridge_legacy_index_rejects_missing_rejected_parent_lineage(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.BOUNDARY_BRIDGE_LEGACY_INDEX_NAME)
    index_path = tmp_path / validate_repo.BOUNDARY_BRIDGE_LEGACY_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "mechanics/sibling-proof-refs/",
            "mechanics/old-sibling-refs/",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.BOUNDARY_BRIDGE_LEGACY_INDEX_NAME
        and "mechanics/sibling-proof-refs/" in issue.message
        for issue in issues
    )
