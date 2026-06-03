from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def copy_root_district_recon_surface(repo_root: Path) -> None:
    for path_name in (
        validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
        "docs/decisions/README.md",
        "mechanics/README.md",
        validate_repo.MECHANICS_AGENTS_NAME,
        validate_repo.PROOF_TOPOLOGY_NAME,
        "ROADMAP.md",
    ):
        copy_repo_text(repo_root, path_name)


def test_mechanic_root_district_recon_validates_current_routes() -> None:
    assert validate_repo.validate_mechanic_root_district_recon_surfaces(REPO_ROOT) == []


def test_mechanic_root_district_recon_requires_source_tree_supersession(
    tmp_path: Path,
) -> None:
    copy_root_district_recon_surface(tmp_path)
    decision_path = tmp_path / validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "`evals/<claim-family>/<eval-name>/`",
            "`old-flat-source-tree/`",
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_root_district_recon_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME
        and "`evals/<claim-family>/<eval-name>/`" in issue.message
        for issue in issues
    )


def test_mechanic_root_district_recon_requires_agents_command_route(
    tmp_path: Path,
) -> None:
    copy_root_district_recon_surface(tmp_path)
    agents_path = tmp_path / validate_repo.MECHANICS_AGENTS_NAME
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            validate_repo.MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
            "python -m pytest -q tests/test_validate_repo.py -k wrong_route",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_root_district_recon_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANICS_AGENTS_NAME
        and validate_repo.MECHANIC_ROOT_DISTRICT_RECON_COMMAND in issue.message
        for issue in issues
    )


def test_mechanic_root_district_recon_rejects_missing_district_row(
    tmp_path: Path,
) -> None:
    copy_root_district_recon_surface(tmp_path)
    evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_text = "\n".join(
        line
        for line in evidence_path.read_text(encoding="utf-8").splitlines()
        if not line.startswith("| `quests` |")
    )
    evidence_path.write_text(evidence_text, encoding="utf-8")

    issues = validate_repo.validate_mechanic_root_district_recon_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "root district `quests` must appear in the reconnaissance ledger"
        in issue.message
        for issue in issues
    )


def test_mechanic_root_district_recon_rejects_missing_route_card_posture(
    tmp_path: Path,
) -> None:
    copy_root_district_recon_surface(tmp_path)
    evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "route-card-only compatibility posture; active fixture families live under proof-infra or domain mechanic parts",
            "compatibility root posture; no active fixture family remains in root `fixtures/`",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_root_district_recon_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "root district `fixtures` reconnaissance row must preserve route-card-only posture"
        in issue.message
        for issue in issues
    )


def test_mechanic_root_district_recon_rejects_empty_validation_guard(
    tmp_path: Path,
) -> None:
    copy_root_district_recon_surface(tmp_path)
    evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "quest route validation, generated quest catalog checks, and catalog-check route",
            "TBD",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_mechanic_root_district_recon_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "root district `quests` reconnaissance row must fill `Validation guard`"
        in issue.message
        for issue in issues
    )
