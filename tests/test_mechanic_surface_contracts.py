from __future__ import annotations

import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import mechanic_parts as mechanic_parts_validator
from validators import mechanics as mechanics_validator
from validators import mechanics_routes as mechanics_routes_validator
from validators.common import ValidationIssue
from validators import (
    agon as agon_validator,
    antifragility as antifragility_validator,
    audit as audit_validator,
    boundary_bridge as boundary_bridge_validator,
    checkpoint as checkpoint_validator,
    comparison_spine as comparison_spine_validator,
    distillation as distillation_validator,
    experience as experience_validator,
    growth_cycle as growth_cycle_validator,
    method_growth as method_growth_validator,
    proof_infra as proof_infra_validator,
    proof_loop as proof_loop_validator,
    proof_object as proof_object_validator,
    publication_receipts as publication_receipts_validator,
    questbook as questbook_validator,
    recurrence as recurrence_validator,
    release_support as release_support_validator,
    rpg as rpg_validator,
    titan as titan_validator,
)


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def mechanics_issues(repo_root: Path = REPO_ROOT) -> list[ValidationIssue]:
    return mechanics_routes_validator.validate_mechanics_surfaces(repo_root)


def assert_no_mechanics_issue_for_locations(locations: set[str]) -> None:
    assert not any(issue.location in locations for issue in mechanics_issues())


def assert_no_mechanics_issue_for_location(location: str) -> None:
    assert not any(issue.location == location for issue in mechanics_issues())


def test_proof_loop_mechanic_surfaces_validate_current_routes() -> None:
    assert not any(
        issue.location.startswith("mechanics/proof-loop/")
        or issue.location == "docs/decisions/AOA-EV-D-0019-proof-loop-mechanic-package.md"
        or issue.location == "docs/decisions/AOA-EV-D-0020-proof-loop-local-smoke-report.md"
        or issue.location
        == "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md"
        for issue in mechanics_issues()
    )


def test_proof_loop_smoke_report_surfaces_validate_current_route() -> None:
    assert proof_loop_validator.validate_proof_loop_smoke_report_surfaces(REPO_ROOT) == []


def test_proof_loop_local_report_surfaces_validate_current_route() -> None:
    assert proof_loop_validator.validate_proof_loop_local_report_surfaces(REPO_ROOT) == []


def test_proof_loop_smoke_report_rejects_missing_receipt_boundary(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME)
    report_path = tmp_path / proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME
    report_path.write_text(
        report_path.read_text(encoding="utf-8").replace(
            "no eval result receipt",
            "receipt publication handled elsewhere",
        ),
        encoding="utf-8",
    )

    issues = proof_loop_validator.validate_proof_loop_smoke_report_surfaces(tmp_path)

    assert any(
        issue.location == proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME
        and "no eval result receipt" in issue.message
        for issue in issues
    )


def test_proof_loop_smoke_report_rejects_validation_command_block(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME)
    report_path = tmp_path / proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME
    report_path.write_text(
        report_path.read_text(encoding="utf-8")
        + "\n```bash\npython scripts/validate_repo.py\n```\n",
        encoding="utf-8",
    )

    issues = proof_loop_validator.validate_proof_loop_smoke_report_surfaces(tmp_path)

    assert any(
        issue.location == proof_loop_validator.PROOF_LOOP_SMOKE_REPORT_NAME
        and "parts/AGENTS.md" in issue.message
        for issue in issues
    )


@pytest.mark.parametrize(
    ("prefix", "decision_name"),
    (
        ("mechanics/recurrence/", recurrence_validator.RECURRENCE_MECHANIC_DECISION_NAME),
        ("mechanics/checkpoint/", checkpoint_validator.CHECKPOINT_MECHANIC_DECISION_NAME),
        ("mechanics/experience/", experience_validator.EXPERIENCE_MECHANIC_DECISION_NAME),
        ("mechanics/distillation/", distillation_validator.DISTILLATION_MECHANIC_DECISION_NAME),
    ),
)
def test_mechanic_parent_surfaces_validate_current_routes(
    prefix: str,
    decision_name: str,
) -> None:
    assert not any(
        issue.location.startswith(prefix) or issue.location == decision_name
        for issue in mechanics_issues()
    )


def test_audit_and_release_support_provenance_validate_current_routes() -> None:
    protected_locations = {
        audit_validator.AUDIT_MECHANIC_PROVENANCE_NAME,
        audit_validator.AUDIT_LEGACY_INDEX_NAME,
        audit_validator.AUDIT_LEGACY_DISTILLATION_LOG_NAME,
        audit_validator.AUDIT_LEGACY_RAW_README_NAME,
        release_support_validator.RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME,
        release_support_validator.RELEASE_SUPPORT_LEGACY_INDEX_NAME,
        release_support_validator.RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME,
        release_support_validator.RELEASE_SUPPORT_LEGACY_RAW_README_NAME,
        proof_loop_validator.PROOF_LOOP_MECHANIC_PROVENANCE_NAME,
        proof_loop_validator.PROOF_LOOP_LEGACY_INDEX_NAME,
        proof_loop_validator.PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME,
        proof_loop_validator.PROOF_LOOP_LEGACY_RAW_README_NAME,
        publication_receipts_validator.PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME,
        publication_receipts_validator.PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME,
        publication_receipts_validator.PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME,
        publication_receipts_validator.PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME,
        boundary_bridge_validator.BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_NAME,
        boundary_bridge_validator.BOUNDARY_BRIDGE_LEGACY_INDEX_NAME,
        boundary_bridge_validator.BOUNDARY_BRIDGE_LEGACY_DISTILLATION_LOG_NAME,
        boundary_bridge_validator.BOUNDARY_BRIDGE_LEGACY_RAW_README_NAME,
    }

    assert_no_mechanics_issue_for_locations(protected_locations)


def test_titan_canary_surfaces_validate_current_seed_set() -> None:
    assert titan_validator.validate_titan_canary_surfaces(REPO_ROOT) == []


def test_titan_seed_boundary_part_readme_validates_current_contract() -> None:
    assert_no_mechanics_issue_for_location(titan_validator.TITAN_SEED_BOUNDARY_PART_README_NAME)


def test_titan_direction_rejects_missing_aoa_agents_owner_boundary(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, titan_validator.TITAN_MECHANIC_DIRECTION_NAME)
    direction_path = tmp_path / titan_validator.TITAN_MECHANIC_DIRECTION_NAME
    direction_path.write_text(
        direction_path.read_text(encoding="utf-8").replace(
            "aoa-agents",
            "Agents-of-Abyss",
        ),
        encoding="utf-8",
    )

    issues = mechanics_issues(tmp_path)

    assert any(
        issue.location == titan_validator.TITAN_MECHANIC_DIRECTION_NAME
        and "aoa-agents" in issue.message
        for issue in issues
    )


def test_titan_parts_index_readme_keeps_canary_as_payload_form() -> None:
    assert_no_mechanics_issue_for_location(titan_validator.TITAN_PARTS_INDEX_README_NAME)


def test_titan_parts_index_readme_rejects_canary_named_parts_district(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, titan_validator.TITAN_PARTS_INDEX_README_NAME)
    parts_readme = tmp_path / titan_validator.TITAN_PARTS_INDEX_README_NAME
    parts_readme.write_text(
        parts_readme.read_text(encoding="utf-8").replace(
            "# Titan / Parts Route", "# Titan Canaries Parts"
        ),
        encoding="utf-8",
    )

    issues = mechanics_issues(tmp_path)

    assert any(
        issue.location == titan_validator.TITAN_PARTS_INDEX_README_NAME
        and "# Titan / Parts Route" in issue.message
        for issue in issues
    )


def test_titan_seed_boundary_part_readme_rejects_missing_owner_split(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, titan_validator.TITAN_SEED_BOUNDARY_PART_README_NAME)
    copy_repo_text(tmp_path, titan_validator.TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    readme_path = tmp_path / titan_validator.TITAN_SEED_BOUNDARY_PART_README_NAME
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Owner Notes"
        ),
        encoding="utf-8",
    )

    issues = mechanics_issues(tmp_path)

    assert any(
        issue.location == titan_validator.TITAN_SEED_BOUNDARY_PART_README_NAME
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_titan_seed_boundary_seeds_agents_requires_operating_card(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, titan_validator.TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME)
    agents_path = tmp_path / titan_validator.TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "## Operating Card", "## Route Card"
        ),
        encoding="utf-8",
    )

    issues = mechanics_issues(tmp_path)

    assert any(
        issue.location == titan_validator.TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME
        and "## Operating Card" in issue.message
        for issue in issues
    )


def test_titan_seed_boundary_surfaces_reject_stale_negative_claim_limits(
    tmp_path: Path,
) -> None:
    readme_name = titan_validator.TITAN_SEED_BOUNDARY_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name

    for stale_phrase in titan_validator.TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES:
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8")
            + f"\n\n{stale_phrase}.\n",
            encoding="utf-8",
        )

        issues = mechanics_issues(tmp_path)

        assert any(
            issue.location == readme_name
            and "owner maps instead of stale negative" in issue.message
            for issue in issues
        )

        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}.\n",
                "",
            ),
            encoding="utf-8",
        )


@pytest.mark.parametrize(
    ("surface_group", "protected_locations"),
    (
        (
            "audit",
            {
                audit_validator.AUDIT_SELECTED_EVIDENCE_PART_README_NAME,
                audit_validator.AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
                audit_validator.AUDIT_CANDIDATE_READERS_PART_README_NAME,
                audit_validator.AUDIT_INTEGRITY_REVIEW_PART_README_NAME,
            },
        ),
        (
            "agon",
            {path_name for path_name, _tokens in agon_validator.AGON_PART_README_CONTRACTS},
        ),
        (
            "boundary_bridge",
            {
                boundary_bridge_validator.BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME,
                boundary_bridge_validator.BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_README_NAME,
                boundary_bridge_validator.BOUNDARY_BRIDGE_ORCHESTRATOR_PROOF_ANCHORS_PART_README_NAME,
            },
        ),
        (
            "publication_receipts",
            {
                publication_receipts_validator.PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME,
                publication_receipts_validator.PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME,
                publication_receipts_validator.PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME,
                publication_receipts_validator.PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME,
            },
        ),
        (
            "release_support",
            {
                release_support_validator.RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
                release_support_validator.RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
                release_support_validator.RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
            },
        ),
        (
            "comparison_spine",
            {
                comparison_spine_validator.COMPARISON_SPINE_OVERVIEW_PART_README_NAME,
                comparison_spine_validator.COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME,
                comparison_spine_validator.COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME,
                comparison_spine_validator.COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME,
            },
        ),
        (
            "antifragility",
            {
                antifragility_validator.ANTIFRAGILITY_POSTURE_PART_README_NAME,
                antifragility_validator.ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME,
                antifragility_validator.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME,
            },
        ),
        (
            "checkpoint",
            {
                checkpoint_validator.CHECKPOINT_A2A_PART_README_NAME,
                checkpoint_validator.CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME,
                checkpoint_validator.CHECKPOINT_SELF_AGENT_PART_README_NAME,
            },
        ),
        (
            "experience",
            {
                experience_validator.EXPERIENCE_PROTOCOL_PART_README_NAME,
                experience_validator.EXPERIENCE_CERTIFICATION_PART_README_NAME,
                experience_validator.EXPERIENCE_ADOPTION_PART_README_NAME,
                experience_validator.EXPERIENCE_GOVERNANCE_PART_README_NAME,
                experience_validator.EXPERIENCE_OFFICE_PART_README_NAME,
            },
        ),
        (
            "distillation",
            {
                distillation_validator.DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME,
                distillation_validator.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME,
            },
        ),
        (
            "method_growth",
            {
                method_growth_validator.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME,
                method_growth_validator.METHOD_GROWTH_OWNER_LANDING_PART_README_NAME,
            },
        ),
        (
            "proof_object",
            {
                proof_object_validator.PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME,
                proof_object_validator.PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME,
            },
        ),
        (
            "questbook",
            {
                questbook_validator.QUESTBOOK_SOURCE_RECORD_PART_README_NAME,
                questbook_validator.QUESTBOOK_DISPATCH_READER_PART_README_NAME,
            },
        ),
    ),
)
def test_mechanic_part_readmes_validate_current_contracts(
    surface_group: str,
    protected_locations: set[str],
) -> None:
    assert surface_group
    assert_no_mechanics_issue_for_locations(protected_locations)


@pytest.mark.parametrize(
    "readme_name",
    (
        proof_loop_validator.PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME,
        growth_cycle_validator.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME,
        recurrence_validator.RECURRENCE_CONTROL_PLANE_PART_README_NAME,
        rpg_validator.RPG_PROGRESS_UNLOCKS_PART_README_NAME,
    ),
)
def test_single_mechanic_part_readmes_validate_current_contracts(
    readme_name: str,
) -> None:
    assert_no_mechanics_issue_for_location(readme_name)


@pytest.mark.parametrize(
    "readme_name",
    (
        proof_loop_validator.PROOF_LOOP_PARTS_README_NAME,
        growth_cycle_validator.GROWTH_CYCLE_PARTS_README_NAME,
        titan_validator.TITAN_PARTS_INDEX_README_NAME,
    ),
)
def test_single_part_lower_indexes_validate_current_operating_cards(
    readme_name: str,
) -> None:
    assert_no_mechanics_issue_for_location(readme_name)


@pytest.mark.parametrize(
    "readme_name",
    (
        proof_loop_validator.PROOF_LOOP_PARTS_README_NAME,
        growth_cycle_validator.GROWTH_CYCLE_PARTS_README_NAME,
        titan_validator.TITAN_PARTS_INDEX_README_NAME,
    ),
)
def test_single_part_lower_indexes_reject_missing_operating_card(
    tmp_path: Path,
    readme_name: str,
) -> None:
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Operating Card", "## Route Notes"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Operating Card" in issue.message
        for issue in issues
    )


def test_repair_diagnosis_route_boundary_validates_current_contract() -> None:
    protected_locations = {
        antifragility_validator.ANTIFRAGILITY_MECHANIC_README_NAME,
        antifragility_validator.ANTIFRAGILITY_MECHANIC_PARTS_NAME,
        mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        growth_cycle_validator.REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
    }

    assert_no_mechanics_issue_for_locations(protected_locations)


def test_audit_part_readmes_reject_missing_inputs_contract(tmp_path: Path) -> None:
    copy_repo_text(tmp_path, audit_validator.AUDIT_SELECTED_EVIDENCE_PART_README_NAME)
    readme_path = tmp_path / audit_validator.AUDIT_SELECTED_EVIDENCE_PART_README_NAME
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace("## Inputs", "## Intake"),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == audit_validator.AUDIT_SELECTED_EVIDENCE_PART_README_NAME
        and "## Inputs" in issue.message
        for issue in issues
    )


def test_agon_part_readmes_reject_missing_stop_line_contract(
    tmp_path: Path,
) -> None:
    readme_name = agon_validator.AGON_PART_README_CONTRACTS[0][0]
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )


def test_agon_part_readmes_reject_stale_imperative_stop_line_phrasing(
    tmp_path: Path,
) -> None:
    readme_name = agon_validator.AGON_PART_README_CONTRACTS[1][0]
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name

    for stale_phrase in agon_validator.AGON_PART_README_STALE_STOP_LINE_PHRASES:
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8")
            + f"\n\n{stale_phrase}.\n",
            encoding="utf-8",
        )

        issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "owner tables instead of stale imperative" in issue.message
            for issue in issues
        )

        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}.\n",
                "",
            ),
            encoding="utf-8",
        )


def test_proof_infra_part_agents_reject_stale_negative_scaffold(
    tmp_path: Path,
) -> None:
    for path_name in (
        proof_infra_validator.PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME,
        proof_infra_validator.PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
        agents_path = tmp_path / path_name

        for stale_phrase in proof_infra_validator.PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES:
            agents_path.write_text(
                agents_path.read_text(encoding="utf-8")
                + f"\n\n{stale_phrase}.\n",
                encoding="utf-8",
            )

            issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

            assert any(
                issue.location == path_name
                and "operating cards and owner route tables" in issue.message
                for issue in issues
            )

            agents_path.write_text(
                agents_path.read_text(encoding="utf-8").replace(
                    f"\n\n{stale_phrase}.\n",
                    "",
                ),
                encoding="utf-8",
            )


def test_recurrence_portable_beacon_agents_reject_stale_negative_scaffold(
    tmp_path: Path,
) -> None:
    path_name = recurrence_validator.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME
    copy_repo_text(tmp_path, path_name)
    agents_path = tmp_path / path_name

    for stale_phrase in recurrence_validator.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_STALE_ROUTE_PHRASES:
        agents_path.write_text(
            agents_path.read_text(encoding="utf-8")
            + f"\n\n{stale_phrase}.\n",
            encoding="utf-8",
        )

        issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == path_name
            and "operating card and owner route table" in issue.message
            for issue in issues
        )

        agents_path.write_text(
            agents_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}.\n",
                "",
            ),
            encoding="utf-8",
        )


def test_boundary_bridge_part_readmes_reject_missing_outputs_contract(
    tmp_path: Path,
) -> None:
    readme_name = boundary_bridge_validator.BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    copy_repo_text(tmp_path, boundary_bridge_validator.BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Outputs", "## Result Notes"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Outputs" in issue.message
        for issue in issues
    )


def test_publication_receipts_part_readmes_reject_missing_stop_lines_contract(
    tmp_path: Path,
) -> None:
    readme_name = publication_receipts_validator.PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )


def test_release_support_part_readmes_reject_missing_stop_lines_contract(
    tmp_path: Path,
) -> None:
    readme_name = release_support_validator.RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )


def test_comparison_spine_part_readmes_reject_missing_inputs_contract(
    tmp_path: Path,
) -> None:
    readme_name = comparison_spine_validator.COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Inputs", "## Intake"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Inputs" in issue.message
        for issue in issues
    )


def test_proof_loop_route_smoke_part_readme_rejects_missing_inputs_contract(
    tmp_path: Path,
) -> None:
    readme_name = proof_loop_validator.PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Inputs", "## Intake"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Inputs" in issue.message
        for issue in issues
    )


def test_antifragility_part_readmes_reject_missing_stop_lines_contract(
    tmp_path: Path,
) -> None:
    readme_name = antifragility_validator.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )


def test_antifragility_parts_route_validates_current_operating_card(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, antifragility_validator.ANTIFRAGILITY_PARTS_README_NAME)

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert not any(
        issue.location == antifragility_validator.ANTIFRAGILITY_PARTS_README_NAME
        for issue in issues
    )


def test_antifragility_parts_route_rejects_stale_negative_boundary_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, antifragility_validator.ANTIFRAGILITY_PARTS_README_NAME)
    parts_path = tmp_path / antifragility_validator.ANTIFRAGILITY_PARTS_README_NAME
    parts_path.write_text(
        parts_path.read_text(encoding="utf-8")
        + "\n\nThe parts support proof review. They do not own source proof bundle meaning, "
        "AoA antifragility doctrine, runtime repair, memory truth, stats truth, or "
        "owner-local cleanup.\n",
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == antifragility_validator.ANTIFRAGILITY_PARTS_README_NAME
        and "stale negative boundary scaffold" in issue.message
        for issue in issues
    )


def test_mechanic_part_readmes_reject_stale_stop_line_lead_ins(
    tmp_path: Path,
) -> None:
    readme_name = antifragility_validator.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    current_route_lead_in = (
        "Boundary routes keep repair-proof pressure with the owner that can act on it:"
    )

    for stale_lead_in in mechanic_parts_validator.MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS:
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                current_route_lead_in,
                stale_lead_in,
            ),
            encoding="utf-8",
        )

        issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "old part-claim scaffold" in issue.message
            for issue in issues
        )

        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                stale_lead_in,
                current_route_lead_in,
            ),
            encoding="utf-8",
        )


def test_checkpoint_part_readmes_reject_stale_root_fixture_path(
    tmp_path: Path,
) -> None:
    readme_name = checkpoint_validator.CHECKPOINT_A2A_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md",
            "fixtures/a2a-summon-return-checkpoint-v1/README.md",
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md"
        in issue.message
        for issue in issues
    )


def test_experience_part_readmes_reject_missing_owner_split_contract(
    tmp_path: Path,
) -> None:
    readme_name = experience_validator.EXPERIENCE_ADOPTION_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_distillation_part_readmes_reject_missing_stop_lines_contract(
    tmp_path: Path,
) -> None:
    readme_name = distillation_validator.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )


def test_growth_cycle_diagnosis_gate_rejects_missing_owner_split_contract(
    tmp_path: Path,
) -> None:
    readme_name = growth_cycle_validator.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_repair_diagnosis_route_boundary_rejects_deferred_antifragility_parts(
    tmp_path: Path,
) -> None:
    parts_name = antifragility_validator.ANTIFRAGILITY_MECHANIC_PARTS_NAME
    copy_repo_text(tmp_path, parts_name)
    parts_path = tmp_path / parts_name
    parts_path.write_text(
        parts_path.read_text(encoding="utf-8").replace(
            "`mechanics/growth-cycle/parts/diagnosis-gate/`",
            "`evals/workflow/aoa-diagnosis-cause-discipline` deferred route",
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == parts_name
        and "mechanics/growth-cycle/parts/diagnosis-gate/" in issue.message
        for issue in issues
    )


def test_audit_parts_index_validates_current_route() -> None:
    assert mechanics_routes_validator.validate_mechanics_surfaces(REPO_ROOT) == []


def test_audit_parts_index_rejects_stale_negative_admission_scaffold(
    tmp_path: Path,
) -> None:
    for path_name in (
        audit_validator.AUDIT_MECHANIC_README_NAME,
        audit_validator.AUDIT_MECHANIC_AGENTS_NAME,
        audit_validator.AUDIT_MECHANIC_PROVENANCE_NAME,
        audit_validator.AUDIT_PARTS_README_NAME,
        audit_validator.AUDIT_LEGACY_INDEX_NAME,
        audit_validator.AUDIT_LEGACY_DISTILLATION_LOG_NAME,
        audit_validator.AUDIT_LEGACY_RAW_README_NAME,
        audit_validator.AUDIT_SELECTED_EVIDENCE_PART_README_NAME,
        audit_validator.AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
        audit_validator.AUDIT_CANDIDATE_READERS_PART_README_NAME,
        audit_validator.AUDIT_INTEGRITY_REVIEW_PART_README_NAME,
        audit_validator.AUDIT_PART_CONTRACT_GUARD_DECISION_NAME,
        "docs/decisions/README.md",
        "docs/decisions/AOA-EV-D-0007-audit-mechanic-package.md",
    ):
        copy_repo_text(tmp_path, path_name)
    parts_path = tmp_path / audit_validator.AUDIT_PARTS_README_NAME
    parts_path.write_text(
        parts_path.read_text(encoding="utf-8")
        + "\nDo not create another part unless it has source surfaces.\n",
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == audit_validator.AUDIT_PARTS_README_NAME
        and "positive part-admission route" in issue.message
        for issue in issues
    )


def test_repair_diagnosis_route_boundary_rejects_stale_evidence_map_route(
    tmp_path: Path,
) -> None:
    evidence_name = mechanics_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME
    copy_repo_text(tmp_path, evidence_name)
    evidence_path = tmp_path / evidence_name
    evidence_path.write_text(
        evidence_path.read_text(encoding="utf-8").replace(
            "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane.",
            "diagnosis-cause discipline remains deferred.",
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == evidence_name
        and "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane."
        in issue.message
        for issue in issues
    )


def test_method_growth_part_owner_split_rejects_soft_owner_split(
    tmp_path: Path,
) -> None:
    readme_name = method_growth_validator.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Owner Split"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_proof_object_part_owner_split_rejects_missing_source_bundle_boundary(
    tmp_path: Path,
) -> None:
    readme_name = proof_object_validator.PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_questbook_part_owner_split_rejects_missing_generated_boundary(
    tmp_path: Path,
) -> None:
    readme_name = questbook_validator.QUESTBOOK_DISPATCH_READER_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stronger Owner Split", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_recurrence_control_plane_rejects_stale_root_fixture_path(
    tmp_path: Path,
) -> None:
    readme_name = recurrence_validator.RECURRENCE_CONTROL_PLANE_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md",
            "fixtures/recurrence-control-plane-integrity-v1/README.md",
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md"
        in issue.message
        for issue in issues
    )


def test_rpg_progression_unlocks_rejects_missing_stop_lines_contract(
    tmp_path: Path,
) -> None:
    readme_name = rpg_validator.RPG_PROGRESS_UNLOCKS_PART_README_NAME
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Stop-Lines", "## Boundary"
        ),
        encoding="utf-8",
    )

    issues = mechanics_routes_validator.validate_mechanics_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stop-Lines" in issue.message
        for issue in issues
    )
