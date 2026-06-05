from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validators import mechanic_evidence_dimensions as mechanic_evidence_dimensions_validator
from validators import mechanic_evidence_route_refs as mechanic_evidence_route_refs_validator
from validators import mechanic_parent_registry as mechanic_parent_registry_validator
from validators import mechanics as mechanics_validator
from validators import root_context


TITAN_DIMENSION_ROW = (
    "| `titan` | evals-native | owner-named Titan proof-seed boundary with proof-organ claim limits | "
    "incarnation, summon, memory, gate, runtime roster, bridge, and closeout seed pressure | "
    "Titan canary YAML seeds and seed AGENTS route | canary shape validator and tests; future scorer route remains deferred | "
    "Titan boundary pressure stays seed-level until executable proof exists | "
    "`aoa-agents` owns Titan role/bearer/summon/incarnation law; `aoa-memo` and runtime owners keep memory and activation truth | "
    "old `titan-canaries` parent and root `evals/` placement route through provenance |\n"
)
TITAN_ROUTE_REFS_ROW = (
    "| `titan` | `mechanics/titan/README.md`, "
    "`mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, "
    "`mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, "
    "`README.md` |"
)


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def copy_class_map_surface(repo_root: Path, *extra_paths: str) -> None:
    for path_name in (
        mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        "docs/decisions/README.md",
        "mechanics/README.md",
        root_context.PROOF_TOPOLOGY_NAME,
        "ROADMAP.md",
        *extra_paths,
    ):
        copy_repo_text(repo_root, path_name)


def evidence_text_path(repo_root: Path) -> Path:
    return repo_root / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME


def test_mechanic_parent_class_sets_cover_allowed_parents() -> None:
    aoa_parents = set(mechanics_validator.AOA_ALIGNED_MECHANIC_PARENT_NAMES)
    evals_native_parents = set(mechanics_validator.EVALS_NATIVE_MECHANIC_PARENT_NAMES)

    assert aoa_parents.isdisjoint(evals_native_parents)
    assert aoa_parents | evals_native_parents == set(
        mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    )


def test_mechanic_parent_class_map_validates_current_routes() -> None:
    assert mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(REPO_ROOT) == []


def test_mechanic_evidence_dimension_ledger_validates_current_routes() -> None:
    issues = mechanic_evidence_dimensions_validator.validate_mechanic_evidence_dimension_ledger(REPO_ROOT)

    assert not any("evidence dimension ledger" in issue.message for issue in issues)


def test_mechanic_evidence_route_refs_validate_current_routes() -> None:
    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(REPO_ROOT)

    assert not any("evidence route refs" in issue.message for issue in issues)


def test_mechanic_evidence_dimension_ledger_rejects_missing_parent_row(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(
        tmp_path,
        mechanics_validator.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
    )
    evidence_path = evidence_text_path(tmp_path)
    evidence_text = evidence_path.read_text(encoding="utf-8")
    evidence_path.write_text(evidence_text.replace(TITAN_DIMENSION_ROW, ""), encoding="utf-8")

    issues = mechanic_evidence_dimensions_validator.validate_mechanic_evidence_dimension_ledger(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "active parent `titan` must appear in the evidence dimension ledger"
        in issue.message
        for issue in issues
    )


def test_mechanic_evidence_dimension_ledger_rejects_wrong_class(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(
        tmp_path,
        mechanics_validator.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
    )
    evidence_path = evidence_text_path(tmp_path)
    evidence_text = evidence_path.read_text(encoding="utf-8")
    evidence_path.write_text(
        evidence_text.replace("| `titan` | evals-native |", "| `titan` | AoA-aligned |", 1),
        encoding="utf-8",
    )

    issues = mechanic_evidence_dimensions_validator.validate_mechanic_evidence_dimension_ledger(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "row for `titan` must use class `evals-native`" in issue.message
        for issue in issues
    )


def test_mechanic_evidence_dimension_ledger_rejects_empty_dimension(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(
        tmp_path,
        mechanics_validator.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
    )
    evidence_path = evidence_text_path(tmp_path)
    evidence_text = evidence_path.read_text(encoding="utf-8")
    evidence_path.write_text(
        evidence_text.replace("Titan canary YAML seeds and seed AGENTS route", "TBD", 1),
        encoding="utf-8",
    )

    issues = mechanic_evidence_dimensions_validator.validate_mechanic_evidence_dimension_ledger(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "row for `titan` must fill `Contracts/payloads`" in issue.message
        for issue in issues
    )


def test_mechanic_evidence_route_refs_rejects_missing_path_refs(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(tmp_path, mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME)
    evidence_path = evidence_text_path(tmp_path)
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            TITAN_ROUTE_REFS_ROW,
            "| `titan` | seed-boundary prose without route refs |",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "evidence route refs row for `titan` must name at least" in issue.message
        for issue in issues
    )


def test_mechanic_evidence_route_refs_rejects_generic_root_validator_ref(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(tmp_path, mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME)
    evidence_path = evidence_text_path(tmp_path)
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            TITAN_ROUTE_REFS_ROW,
            "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `tests/test_validate_repo.py` |",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "must not use generic root validator route `tests/test_validate_repo.py`"
        in issue.message
        for issue in issues
    )


def test_mechanic_evidence_route_refs_rejects_decision_only_non_mechanics_ref(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(tmp_path, mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME)
    evidence_path = evidence_text_path(tmp_path)
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            TITAN_ROUTE_REFS_ROW,
            "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `docs/decisions/AOA-EV-D-0015-titan-mechanic-package.md` |",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "living non-mechanics evidence" in issue.message
        and "rationale-only decision refs are not enough" in issue.message
        for issue in issues
    )


def test_mechanic_evidence_route_refs_rejects_stale_path(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(tmp_path, mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME)
    evidence_path = evidence_text_path(tmp_path)
    stale_ref = "mechanics/titan/parts/seed-boundary/seeds/missing-canary.yaml"
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml",
            stale_ref,
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "evidence route refs row for `titan` has stale route ref" in issue.message
        and stale_ref in issue.message
        for issue in issues
    )


def test_mechanic_evidence_route_refs_rejects_mechanics_only_row(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(tmp_path, mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME)
    evidence_path = evidence_text_path(tmp_path)
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            TITAN_ROUTE_REFS_ROW,
            "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/README.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml` |",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "must include at least one non-mechanics route ref" in issue.message
        for issue in issues
    )


def test_mechanic_parent_class_map_rejects_missing_owner_named_titan_boundary(
    tmp_path: Path,
) -> None:
    copy_class_map_surface(
        tmp_path,
        mechanics_validator.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
        mechanics_validator.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
        mechanics_validator.MECHANIC_PARENT_CLASS_DECISION_NAME,
    )
    evidence_path = evidence_text_path(tmp_path)
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "owner-named evals-native",
            "plain evals-native",
        ),
        encoding="utf-8",
    )

    issues = mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "owner-named evals-native" in issue.message
        for issue in issues
    )


def test_mechanic_parent_class_map_rejects_misclassified_parent(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    evidence_path = tmp_path / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_text = evidence_path.read_text(encoding="utf-8")
    evidence_text = evidence_text.replace(
        "| `titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries",
        "| `not-titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries",
    )
    evidence_path.write_text(evidence_text, encoding="utf-8")

    issues = mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "evals-native parent `titan`" in issue.message
        for issue in issues
    )


def test_mechanic_parent_class_map_rejects_missing_wrong_parent_mapping(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    evidence_path = tmp_path / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_text = evidence_path.read_text(encoding="utf-8").replace(
        "| `repair` | `antifragility/repair-proof` | Active route sends bounded repair pressure through the repair-proof part; future Growth Cycle repair stages still need separate evidence. |\n",
        "",
    )
    evidence_path.write_text(evidence_text, encoding="utf-8")

    issues = mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "former wrong parent `repair`" in issue.message
        for issue in issues
    )


def test_mechanic_parent_class_map_rejects_plausible_parent_wording(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME)
    evidence_path = tmp_path / mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    evidence_text = evidence_path.read_text(encoding="utf-8").replace(
        "The following parents are active and must stay constrained",
        "The following parents are currently plausible and must stay constrained",
    )
    evidence_path.write_text(evidence_text, encoding="utf-8")

    issues = mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(tmp_path)

    assert any(
        issue.location == mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
        and "not merely plausible candidates" in issue.message
        for issue in issues
    )
