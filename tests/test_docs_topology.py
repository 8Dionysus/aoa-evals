from __future__ import annotations

from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import docs_routes
from validators import docs_topology
from validators.common import ValidationIssue
from validators import root_guidance as root_guidance_validator


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def copy_docs_topology_surface(repo_root: Path) -> None:
    for path in docs_topology.ALL_AUTHORED_DOC_FILES:
        copy_repo_text(repo_root, path.as_posix())
    copy_repo_text(repo_root, docs_topology.TOPOLOGY_CONTRACT_PATH.as_posix())


def docs_route_contracts(repo_root: Path) -> list[ValidationIssue]:
    return [
        ValidationIssue(location, message)
        for location, message in docs_routes.validate_docs_routes(repo_root)
    ]


def docs_topology_read_model(repo_root: Path) -> list[ValidationIssue]:
    return [
        ValidationIssue(location, message)
        for location, message in docs_topology.validate_docs_topology(repo_root)
    ]


def test_docs_route_contracts_validate_current_map() -> None:
    assert docs_route_contracts(REPO_ROOT) == []


def test_docs_topology_read_model_validates_current_contract() -> None:
    assert docs_topology_read_model(REPO_ROOT) == []


def test_docs_readme_route_map_validates_current_map() -> None:
    assert root_guidance_validator.validate_docs_readme_route_map(REPO_ROOT) == []


def test_docs_route_contracts_reject_command_block_in_entrypoint(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/README.md")
    readme_path = tmp_path / "docs" / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8")
        + "\n```bash\npython scripts/validate_repo.py\n```\n",
        encoding="utf-8",
    )

    issues = docs_route_contracts(tmp_path)

    assert any(
        issue.location == "docs/README.md"
        and "must link validation routes" in issue.message
        for issue in issues
    )


def test_docs_readme_route_map_rejects_generic_mechanics_label(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/README.md")
    docs_readme_path = tmp_path / "docs" / "README.md"
    docs_readme_path.write_text(
        docs_readme_path.read_text(encoding="utf-8").replace(
            "Mechanics Operation Atlas",
            "Mechanics",
        ),
        encoding="utf-8",
    )

    issues = root_guidance_validator.validate_docs_readme_route_map(tmp_path)

    assert any(
        issue.location == "docs/README.md"
        and "Mechanics Operation Atlas" in issue.message
        for issue in issues
    )


def test_docs_readme_route_map_rejects_validation_block_in_reader_paths(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/README.md")
    docs_readme_path = tmp_path / "docs" / "README.md"
    docs_readme_path.write_text(
        docs_readme_path.read_text(encoding="utf-8").replace(
            "## Recommended Reading Paths",
            "## Verify Current Surfaces\n\nUse docs/AGENTS.md.\n\n## Recommended Reading Paths",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_guidance_validator.validate_docs_readme_route_map(tmp_path)

    assert any(
        issue.location == "docs/README.md"
        and "Verify Current Surfaces" in issue.message
        for issue in issues
    )


def test_docs_readme_route_map_rejects_command_block(tmp_path: Path) -> None:
    copy_repo_text(tmp_path, "docs/README.md")
    docs_readme_path = tmp_path / "docs" / "README.md"
    docs_readme_path.write_text(
        docs_readme_path.read_text(encoding="utf-8")
        + "\n```bash\npython scripts/validate_repo.py\n```\n",
        encoding="utf-8",
    )

    issues = root_guidance_validator.validate_docs_readme_route_map(tmp_path)

    assert any(
        issue.location == "docs/README.md"
        and "executable validation commands" in issue.message
        for issue in issues
    )


def test_docs_readme_route_map_rejects_missing_folder_map_route(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/README.md")
    docs_readme_path = tmp_path / "docs" / "README.md"
    docs_readme_path.write_text(
        docs_readme_path.read_text(encoding="utf-8").replace(
            "docs/guides/",
            "docs/guide-drift/",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_guidance_validator.validate_docs_readme_route_map(tmp_path)

    assert any(
        issue.location == "docs/README.md" and "docs/guides/" in issue.message
        for issue in issues
    )


def test_docs_topology_rejects_unrouted_flat_docs_file(tmp_path: Path) -> None:
    copy_docs_topology_surface(tmp_path)
    flat_path = tmp_path / "docs" / "UNROUTED_PAYLOAD.md"
    flat_path.write_text("# Unrouted\n", encoding="utf-8")

    issues = docs_topology_read_model(tmp_path)

    assert any(
        issue.location == "docs/UNROUTED_PAYLOAD.md"
        and "flat docs file must move" in issue.message
        for issue in issues
    )


def test_docs_topology_rejects_contract_drift(tmp_path: Path) -> None:
    copy_docs_topology_surface(tmp_path)
    contract_path = tmp_path / docs_topology.TOPOLOGY_CONTRACT_PATH
    contract_path.write_text(
        contract_path.read_text(encoding="utf-8").replace(
            "  - docs/testing/TEST_TOPOLOGY.md\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = docs_topology_read_model(tmp_path)

    assert any(
        issue.location == docs_topology.TOPOLOGY_CONTRACT_PATH.as_posix()
        and "testing must match the docs topology contract" in issue.message
        for issue in issues
    )
