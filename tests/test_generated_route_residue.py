from __future__ import annotations

import textwrap
from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import eval_catalog_contract
from validators import root_context
from validators import root_topology as root_topology_validator
from validators import route_residue as route_residue_validator


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


def copy_generated_route_residue_surface(repo_root: Path) -> None:
    for path_name in (
        "generated/README.md",
        "generated/AGENTS.md",
        route_residue_validator.GENERATED_ROUTE_RESIDUE_DECISION_NAME,
        "docs/decisions/README.md",
        root_context.PROOF_TOPOLOGY_NAME,
        root_context.LEGACY_NAMING_NAME,
        root_context.ROADMAP_NAME,
    ):
        copy_repo_text(repo_root, path_name)


def validate_generated_route_residue_surfaces(repo_root: Path):
    return route_residue_validator.validate_generated_route_residue_surfaces(
        repo_root,
        context=root_topology_validator.route_residue_context(),
    )


def test_generated_route_residue_accepts_current_generated_readouts() -> None:
    assert route_residue_validator.validate_generated_route_residue(REPO_ROOT) == []


def test_generated_route_residue_surfaces_validate_current_reader_index() -> None:
    assert validate_generated_route_residue_surfaces(REPO_ROOT) == []


def test_generated_route_residue_surfaces_reject_missing_quest_reader_route(
    tmp_path: Path,
) -> None:
    copy_generated_route_residue_surface(tmp_path)
    agents_path = tmp_path / "generated" / "AGENTS.md"
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "`generated/quest_catalog.min.json`, ",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_generated_route_residue_surfaces(tmp_path)

    assert any(
        issue.location == "generated/AGENTS.md"
        and "generated/quest_catalog.min.json" in issue.message
        for issue in issues
    )


def test_generated_reader_index_requires_source_truth_return(
    tmp_path: Path,
) -> None:
    copy_generated_route_residue_surface(tmp_path)
    readme_path = tmp_path / "generated" / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            'Source surfaces answer\n"what is true?"',
            "Generated readers decide truth",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_generated_route_residue_surfaces(tmp_path)

    assert any(
        issue.location == "generated/README.md"
        and "Source surfaces answer" in issue.message
        for issue in issues
    )


def test_generated_reader_index_requires_source_ownership_language(
    tmp_path: Path,
) -> None:
    copy_generated_route_residue_surface(tmp_path)
    readme_path = tmp_path / "generated" / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "authored source ownership",
            "replacing source ownership",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_generated_route_residue_surfaces(tmp_path)

    assert any(
        issue.location == "generated/README.md"
        and "authored source ownership" in issue.message
        for issue in issues
    )


def test_generated_route_residue_rejects_root_route_card_structural_reference(
    tmp_path: Path,
) -> None:
    eval_catalog_contract.write_json_file(
        tmp_path / "generated" / "eval_catalog.json",
        {
            "evals": [
                {
                    "name": "aoa-stale-root-fixture-ref",
                    "proof_artifacts": {
                        "shared_fixture_family_path": "fixtures/old/README.md",
                    },
                }
            ]
        },
    )

    issues = route_residue_validator.validate_generated_route_residue(tmp_path)

    assert any(
        "route-card-only root district 'fixtures/'" in issue.message
        for issue in issues
    )


def test_generated_route_residue_rejects_legacy_mechanic_parent_reference(
    tmp_path: Path,
) -> None:
    eval_catalog_contract.write_json_file(
        tmp_path / "generated" / "comparison_spine.json",
        {
            "evals": [
                {
                    "name": "aoa-stale-titan-parent-ref",
                    "proof_artifacts": {
                        "shared_fixture_family_path": "mechanics/titan-canaries/parts/seed-boundary/README.md",
                    },
                }
            ]
        },
    )

    issues = route_residue_validator.validate_generated_route_residue(tmp_path)

    assert any(
        "not legacy parent route 'mechanics/titan-canaries/'" in issue.message
        for issue in issues
    )


def test_generated_route_residue_allows_part_local_generated_config_reference(
    tmp_path: Path,
) -> None:
    part_root = tmp_path / "mechanics" / "agon" / "parts" / "court-prebinding"
    write_text(part_root / "config" / "seed.json", "{}")
    eval_catalog_contract.write_json_file(
        part_root / "generated" / "registry.min.json",
        {"source": "config/seed.json"},
        compact=True,
    )

    assert route_residue_validator.validate_generated_route_residue(tmp_path) == []


def test_generated_route_residue_ignores_markdown_content_paths(
    tmp_path: Path,
) -> None:
    eval_catalog_contract.write_json_file(
        tmp_path / "generated" / "eval_sections.full.json",
        {
            "evals": [
                {
                    "name": "aoa-markdown-content-only",
                    "content_markdown": "Bundle-local examples may mention `fixtures/contract.json`.",
                }
            ]
        },
    )

    assert route_residue_validator.validate_generated_route_residue(tmp_path) == []
