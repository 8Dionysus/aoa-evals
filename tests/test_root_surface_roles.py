from __future__ import annotations

import textwrap
from pathlib import Path

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import root_agent_index as root_agent_index_validator
from validators import root_agent_lanes as root_agent_lanes_validator
from validators import root_audit_routes as root_audit_routes_validator
from validators import root_decision_status as root_decision_status_validator
from validators import root_design_docs as root_design_validator
from validators import root_frontdoor_guidance as root_frontdoor_guidance_validator
from validators import root_legacy_bridge_residue as root_legacy_bridge_residue_validator
from validators import root_legacy_external_leakage as root_legacy_external_leakage_validator
from validators import root_legacy_naming as root_legacy_validator
from validators import root_memory_boundary as root_memory_boundary_validator
from validators import root_proof_topology as root_proof_topology_validator
from validators import root_validator_surfaces as root_validator_surfaces_validator
from validators.common import ValidationIssue


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


def copy_root_readme_surface(repo_root: Path) -> None:
    for path_name in ("README.md", "docs/README.md"):
        copy_repo_text(repo_root, path_name)


LEGACY_NAMING_SURFACE_PATHS = (
    root_legacy_validator.LEGACY_NAMING_NAME,
    "docs/decisions/AOA-EV-D-0009-legacy-naming-containment.md",
    root_legacy_validator.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
    root_legacy_validator.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
    "docs/decisions/README.md",
    "README.md",
    root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
    "ROADMAP.md",
    "CHANGELOG.md",
)


def copy_legacy_naming_surface(repo_root: Path, *extra_paths: str) -> Path:
    for path_name in (*LEGACY_NAMING_SURFACE_PATHS, *extra_paths):
        copy_repo_text(repo_root, path_name)
    return repo_root / root_legacy_validator.LEGACY_NAMING_NAME


def legacy_naming_issues(repo_root: Path) -> list[ValidationIssue]:
    return [
        *root_legacy_validator.validate_legacy_naming_posture_surfaces(repo_root),
        *root_legacy_bridge_residue_validator.validate_legacy_single_bridge_residue_surfaces(repo_root),
        *root_legacy_external_leakage_validator.validate_legacy_external_leakage_surfaces(repo_root),
    ]


def test_root_readme_surface_role_validates_current_entry() -> None:
    assert root_frontdoor_guidance_validator.validate_root_readme_surface_role(REPO_ROOT) == []


def test_agent_lane_surfaces_validate_current_routes() -> None:
    assert root_agent_lanes_validator.validate_agent_lane_surfaces(REPO_ROOT) == []


def test_agent_lane_surfaces_reject_root_local_spark_lane(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / ".agents" / "AGENTS.md",
        """
        # AGENTS.md

        `.agents/<lane>/` route. `.agents/skills/` support. `.agents/spark/`
        lane. Proof authority stays with the source bundle.

        python scripts/validate_repo.py
        python scripts/validate_nested_agents.py
        """,
    )
    write_text(
        tmp_path / ".agents" / "spark" / "AGENTS.md",
        """
        # AGENTS.md

        `.agents/spark/` fast-loop lane for one bounded claim.
        Bundle-local `EVAL.md` and eval.yaml stay stronger.
        generated/AGENTS.md routes generated reader changes.

        python scripts/validate_nested_agents.py
        """,
    )
    write_text(
        tmp_path / ".agents" / "spark" / "SWARM.md",
        """
        # Spark Swarm

        `.agents/spark/SWARM.md`
        Use this for one bounded eval bundle.
        Boundary Keeper checks repo validation and build catalog through
        .agents/spark/AGENTS.md#validation.
        """,
    )
    write_text(
        tmp_path / "docs" / "decisions" / "AOA-EV-D-0017-spark-agent-lane-placement.md",
        """
        # 0017 Spark Agent Lane Placement

        Spark/ moves to .agents/spark/ with .agents/AGENTS.md.
        This does not let Spark widen proof claims and does not make
        `.agents/` a doctrine center.
        `Spark/` is absent.
        """,
    )
    write_text(
        tmp_path / "README.md",
        """
        # README

        .agents/AGENTS.md
        .agents/spark/AGENTS.md
        """,
    )
    write_text(
        tmp_path / "docs" / "architecture" / "PROOF_TOPOLOGY.md",
        """
        # Proof Topology

        Agent guidance uses .agents/ and .agents/spark/.
        """,
    )
    write_text(
        tmp_path / "docs" / "architecture" / "LEGACY_NAMING.md",
        """
        # Legacy Naming

        .agents/spark/
        old `Spark/`
        """,
    )
    write_text(
        tmp_path / "Spark" / "AGENTS.md",
        """
        # AGENTS.md

        stale root lane
        """,
    )

    issues = root_agent_lanes_validator.validate_agent_lane_surfaces(tmp_path)

    assert ValidationIssue(
        "Spark/",
        "root-local Spark lane must stay moved to .agents/spark/",
    ) in issues


def test_agent_lane_surfaces_reject_spark_swarm_command_lines(
    tmp_path: Path,
) -> None:
    for path_name in (
        ".agents/AGENTS.md",
        ".agents/spark/AGENTS.md",
        "docs/decisions/AOA-EV-D-0017-spark-agent-lane-placement.md",
    ):
        copy_repo_text(tmp_path, path_name)
    write_text(
        tmp_path / ".agents" / "spark" / "SWARM.md",
        """
        # Spark Swarm

        `.agents/spark/SWARM.md`
        Use this for one bounded eval bundle.
        Boundary Keeper checks repo validation and build catalog through
        .agents/spark/AGENTS.md#validation.

        ```bash
        python scripts/validate_repo.py
        ```
        """,
    )

    issues = root_agent_lanes_validator.validate_agent_lane_surfaces(tmp_path)

    assert any(
        issue.location == ".agents/spark/SWARM.md"
        and "route executable commands to .agents/spark/AGENTS.md"
        in issue.message
        for issue in issues
    )


def test_legacy_naming_surfaces_validate_current_routes() -> None:
    assert legacy_naming_issues(REPO_ROOT) == []


def test_legacy_naming_surfaces_reject_missing_archive_detail_boundary(
    tmp_path: Path,
) -> None:
    legacy_path = copy_legacy_naming_surface(tmp_path)
    legacy_path.write_text(
        legacy_path.read_text(encoding="utf-8").replace(
            "archive details",
            "history notes",
        ),
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == root_legacy_validator.LEGACY_NAMING_NAME
        and "archive details" in issue.message
        for issue in issues
    )


def test_legacy_naming_single_bridge_language_rejects_index_as_entry(
    tmp_path: Path,
) -> None:
    legacy_path = copy_legacy_naming_surface(tmp_path)
    legacy_path.write_text(
        legacy_path.read_text(encoding="utf-8")
        + "\nOld Titan routes enter through `mechanics/titan/PROVENANCE.md` "
        "and `mechanics/titan/legacy/INDEX.md`.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == root_legacy_validator.LEGACY_NAMING_NAME
        and "single controlled bridge" in issue.message
        for issue in issues
    )


def test_legacy_naming_posture_guide_rejects_direct_mechanic_legacy_index(
    tmp_path: Path,
) -> None:
    legacy_path = copy_legacy_naming_surface(tmp_path)
    legacy_path.write_text(
        legacy_path.read_text(encoding="utf-8")
        + "\nOld Titan archive table: `mechanics/titan/legacy/INDEX.md`.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == root_legacy_validator.LEGACY_NAMING_NAME
        and "direct mechanic legacy index paths" in issue.message
        for issue in issues
    )


def test_legacy_naming_posture_guide_rejects_concrete_legacy_inventory(
    tmp_path: Path,
) -> None:
    legacy_path = copy_legacy_naming_surface(tmp_path)
    legacy_path.write_text(
        legacy_path.read_text(encoding="utf-8")
        + "\n## Current Active Owners\n\nWrong parent forms such as `agon-proof`.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == root_legacy_validator.LEGACY_NAMING_NAME
        and "concrete legacy-name inventories" in issue.message
        for issue in issues
    )


def test_legacy_naming_rejects_negative_role_scaffold(
    tmp_path: Path,
) -> None:
    legacy_path = copy_legacy_naming_surface(tmp_path)
    legacy_path.write_text(
        legacy_path.read_text(encoding="utf-8")
        + "\nIt is not an archive map.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == root_legacy_validator.LEGACY_NAMING_NAME
        and "concrete legacy-name inventories" in issue.message
        for issue in issues
    )


def test_legacy_naming_rejects_external_archive_accounting_detail(
    tmp_path: Path,
) -> None:
    copy_legacy_naming_surface(tmp_path, "mechanics/README.md")
    mechanics_path = tmp_path / "mechanics" / "README.md"
    mechanics_path.write_text(
        mechanics_path.read_text(encoding="utf-8")
        + "\nInside the archive, every raw payload must point somewhere.\n",
        encoding="utf-8",
    )
    changelog_path = tmp_path / "CHANGELOG.md"
    changelog_path.write_text(
        changelog_path.read_text(encoding="utf-8")
        + "\nlegacy raw payload accounting now rejects archive loops.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == "mechanics/README.md"
        and "archive-local accounting detail" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "CHANGELOG.md"
        and "archive-local accounting detail" in issue.message
        for issue in issues
    )


def test_legacy_single_bridge_residue_rejects_decision_second_entry(
    tmp_path: Path,
) -> None:
    copy_legacy_naming_surface(tmp_path)
    decision_path = "docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md"
    write_text(
        tmp_path / decision_path,
        (
            "# Direction\n\n"
            "Legacy lookup starts from the active route and then enters "
            "`PROVENANCE.md`, `legacy/INDEX.md`, "
            "`legacy/DISTILLATION_LOG.md`, and `legacy/raw/README.md`.\n"
        ),
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == decision_path
        and "cross only through PROVENANCE.md" in issue.message
        for issue in issues
    )


def test_legacy_single_bridge_residue_rejects_root_route_card_archive_entry(
    tmp_path: Path,
) -> None:
    copy_legacy_naming_surface(tmp_path)
    route_card_path = "schemas/README.md"
    write_text(
        tmp_path / route_card_path,
        (
            "# Schemas Route\n\n"
            "Old root schema paths route through `PROVENANCE.md` and "
            "`legacy/INDEX.md`.\n"
        ),
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == route_card_path
        and "cross only through PROVENANCE.md" in issue.message
        for issue in issues
    )


def test_legacy_single_bridge_residue_rejects_root_route_card_mechanic_archive_entry(
    tmp_path: Path,
) -> None:
    copy_legacy_naming_surface(tmp_path)
    route_card_path = "runners/README.md"
    write_text(
        tmp_path / route_card_path,
        (
            "# Shared Runners\n\n"
            "Use `mechanics/proof-infra/PROVENANCE.md` and "
            "`mechanics/proof-infra/legacy/INDEX.md` for old root path lineage.\n"
        ),
    )

    issues = legacy_naming_issues(tmp_path)

    assert any(
        issue.location == route_card_path
        and "cross only through PROVENANCE.md" in issue.message
        for issue in issues
    )


def test_legacy_naming_rejects_external_route_management_wording(
    tmp_path: Path,
) -> None:
    copy_legacy_naming_surface(
        tmp_path,
        "DESIGN.AGENTS.md",
        "mechanics/titan/AGENTS.md",
        "mechanics/proof-object/AGENTS.md",
        "templates/README.md",
    )
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8")
        + "\nLegacy map comes before physical movement, deletion, or retirement.\n",
        encoding="utf-8",
    )
    design_agents_path = tmp_path / "DESIGN.AGENTS.md"
    design_agents_path.write_text(
        design_agents_path.read_text(encoding="utf-8")
        + "\nLegacy cards explain retirement or containment posture.\n",
        encoding="utf-8",
    )
    titan_agents_path = tmp_path / "mechanics" / "titan" / "AGENTS.md"
    titan_agents_path.write_text(
        titan_agents_path.read_text(encoding="utf-8")
        + "\nDo not erase legacy canary vocabulary without a validator-backed retirement path.\n",
        encoding="utf-8",
    )
    proof_object_agents_path = tmp_path / "mechanics" / "proof-object" / "AGENTS.md"
    proof_object_agents_path.write_text(
        proof_object_agents_path.read_text(encoding="utf-8")
        + "\nKeep retired root template and schema aliases retired.\n",
        encoding="utf-8",
    )
    templates_readme_path = tmp_path / "templates" / "README.md"
    templates_readme_path.write_text(
        templates_readme_path.read_text(encoding="utf-8")
        + "\nDo not recreate the retired root template alias.\n",
        encoding="utf-8",
    )

    issues = legacy_naming_issues(tmp_path)

    for location in (
        "ROADMAP.md",
        "DESIGN.AGENTS.md",
        "mechanics/titan/AGENTS.md",
        "mechanics/proof-object/AGENTS.md",
        "templates/README.md",
    ):
        assert any(
            issue.location == location
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )


def test_root_readme_surface_role_rejects_generic_heading(tmp_path: Path) -> None:
    copy_root_readme_surface(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "# aoa-evals Bounded Proof Canon",
            "# aoa-evals",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_frontdoor_guidance_validator.validate_root_readme_surface_role(tmp_path)

    assert any(
        issue.location == "README.md"
        and "# aoa-evals Bounded Proof Canon" in issue.message
        for issue in issues
    )


def test_root_readme_surface_role_requires_positive_validation_route(
    tmp_path: Path,
) -> None:
    copy_root_readme_surface(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "Executable validation routes live in",
            "Validation is elsewhere",
        ),
        encoding="utf-8",
    )

    issues = root_frontdoor_guidance_validator.validate_root_readme_surface_role(tmp_path)

    assert any(
        issue.location == "README.md"
        and "Executable validation routes live in" in issue.message
        for issue in issues
    )


def test_root_readme_surface_role_rejects_docs_guide_catalog_in_proof_check(
    tmp_path: Path,
) -> None:
    copy_root_readme_surface(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8")
        + "\n| Which comparison, artifact/process, repeated-window, or shared-infra guide applies? | docs guide catalog |\n",
        encoding="utf-8",
    )

    issues = root_frontdoor_guidance_validator.validate_root_readme_surface_role(tmp_path)

    assert any(
        issue.location == "README.md"
        and "detailed proof-guide catalogs route to docs/README.md" in issue.message
        for issue in issues
    )


def test_root_readme_surface_role_rejects_generated_reader_catalog_bloat(
    tmp_path: Path,
) -> None:
    copy_root_readme_surface(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8")
        + "\n- [generated/eval_report_index.min.json](generated/eval_report_index.min.json)\n",
        encoding="utf-8",
    )

    issues = root_frontdoor_guidance_validator.validate_root_readme_surface_role(tmp_path)

    assert any(
        issue.location == "README.md"
        and "detailed proof-guide catalogs route to docs/README.md" in issue.message
        for issue in issues
    )


def test_root_readme_surface_role_rejects_generic_docs_map_eval_labels(
    tmp_path: Path,
) -> None:
    copy_root_readme_surface(tmp_path)
    docs_readme_path = tmp_path / "docs" / "README.md"
    docs_readme_path.write_text(
        docs_readme_path.read_text(encoding="utf-8").replace(
            "Eval Bundle Selection Chooser",
            "EVAL_SELECTION",
        ),
        encoding="utf-8",
    )

    issues = root_frontdoor_guidance_validator.validate_root_readme_surface_role(tmp_path)

    assert any(
        issue.location == "docs/README.md"
        and "Eval Bundle Selection Chooser" in issue.message
        for issue in issues
    )


def test_audit_surface_role_validates_current_route() -> None:
    assert root_audit_routes_validator.validate_audit_surface_role(REPO_ROOT) == []


def test_audit_surface_role_rejects_stale_negative_boundary_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "AUDIT.md")
    copy_repo_text(tmp_path, "AGENTS.md")
    agents_path = tmp_path / "AGENTS.md"

    for stale_phrase in root_audit_routes_validator.ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES:
        agents_path.write_text(
            agents_path.read_text(encoding="utf-8") + f"\n\n{stale_phrase}\n",
            encoding="utf-8",
        )

        issues = root_audit_routes_validator.validate_audit_surface_role(tmp_path)

        assert any(
            issue.location == "AGENTS.md"
            and "claim pressure routes instead of stale negative boundary scaffold"
            in issue.message
            for issue in issues
        )

        agents_path.write_text(
            agents_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}\n",
                "",
            ),
            encoding="utf-8",
        )


def test_audit_surface_role_rejects_audit_as_route_law(tmp_path: Path) -> None:
    copy_repo_text(tmp_path, "AGENTS.md")
    write_text(
        tmp_path / "AUDIT.md",
        "# AUDIT.md\n\nThis file maps audit surfaces without naming AGENTS ownership.\n",
    )

    issues = root_audit_routes_validator.validate_audit_surface_role(tmp_path)

    assert any(
        issue.location == "AUDIT.md" and "Audit Surface Map" in issue.message
        for issue in issues
    )


def test_audit_surface_role_requires_route_outward_owner_map(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "AUDIT.md")
    copy_repo_text(tmp_path, "AGENTS.md")
    audit_path = tmp_path / "AUDIT.md"
    audit_path.write_text(
        audit_path.read_text(encoding="utf-8").replace(
            "Route outward for:",
            "External boundaries:",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_audit_routes_validator.validate_audit_surface_role(tmp_path)

    assert any(
        issue.location == "AUDIT.md" and "Route outward for:" in issue.message
        for issue in issues
    )


def test_audit_surface_role_rejects_missing_agents_audit_route(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "AUDIT.md")
    write_text(
        tmp_path / "AGENTS.md",
        "# AGENTS.md\n\n## Verify\n\nUse local validation.\n",
    )

    issues = root_audit_routes_validator.validate_audit_surface_role(tmp_path)

    assert any(
        issue.location == "AGENTS.md"
        and "## Audit and review route" in issue.message
        for issue in issues
    )


def test_validator_surface_role_validates_current_route() -> None:
    assert root_validator_surfaces_validator.validate_validator_surface_role(REPO_ROOT) == []


def test_validator_surface_role_rejects_stale_negative_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "scripts/AGENTS.md")
    copy_repo_text(tmp_path, "tests/AGENTS.md")

    for path_name, stale_phrase in (
        ("scripts/AGENTS.md", "Validator changes must not weaken bounded proof posture"),
        ("tests/AGENTS.md", "Do not move a part-local test back"),
        ("tests/AGENTS.md", "Do not update expected outputs"),
    ):
        agents_path = tmp_path / path_name
        agents_path.write_text(
            agents_path.read_text(encoding="utf-8") + f"\n\n{stale_phrase}.\n",
            encoding="utf-8",
        )

        issues = root_validator_surfaces_validator.validate_validator_surface_role(tmp_path)

        assert any(
            issue.location == path_name
            and "owner maps instead of stale negative scaffold" in issue.message
            for issue in issues
        )

        agents_path.write_text(
            agents_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}.\n",
                "",
            ),
            encoding="utf-8",
        )


def test_validator_surface_role_rejects_generic_scripts_guidance(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "scripts" / "AGENTS.md",
        "# AGENTS.md\n\nScripts are helper utilities.\n",
    )
    copy_repo_text(tmp_path, "tests/AGENTS.md")

    issues = root_validator_surfaces_validator.validate_validator_surface_role(tmp_path)

    assert any(
        issue.location == "scripts/AGENTS.md"
        and "root contract mesh" in issue.message
        for issue in issues
    )


def test_validator_surface_role_rejects_generic_test_guidance(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "scripts/AGENTS.md")
    write_text(
        tmp_path / "tests" / "AGENTS.md",
        "# AGENTS.md\n\nTests cover helpers.\n",
    )

    issues = root_validator_surfaces_validator.validate_validator_surface_role(tmp_path)

    assert any(
        issue.location == "tests/AGENTS.md"
        and "root validator regression mesh" in issue.message
        for issue in issues
    )

def test_architecture_proof_model_contract_validates_current_route() -> None:
    assert root_design_validator.validate_root_design_surfaces(REPO_ROOT) == []

def test_decision_agents_requires_review_log_route(tmp_path: Path) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    agents_path = tmp_path / "docs" / "decisions" / "AGENTS.md"
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "## Amendment Route",
            "## Decision Updates",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "docs/decisions/AGENTS.md"
        and "Amendment Route" in issue.message
        for issue in issues
    )

def test_decision_template_requires_review_log_shape(tmp_path: Path) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    template_path = tmp_path / "docs" / "decisions" / "TEMPLATE.md"
    template_path.write_text(
        template_path.read_text(encoding="utf-8").replace(
            "## Review Log",
            "## Review Notes",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "docs/decisions/TEMPLATE.md"
        and "Review Log" in issue.message
        for issue in issues
    )

def test_decision_status_line_rejects_embedded_supersession_detail(
    tmp_path: Path
) -> None:
    write_text(
        tmp_path / "docs" / "decisions" / "AOA-EV-D-0001-example.md",
        """
        # Example

        - Decision ID: AOA-EV-D-0001
        - Status: Accepted; source route superseded by 0002
        - Date: 2026-05-24
        """,
    )

    issues = root_decision_status_validator.validate_decision_status_lines(tmp_path)

    assert any(
        issue.location == "docs/decisions/AOA-EV-D-0001-example.md:4"
        and "decision status should stay atomic" in issue.message
        for issue in issues
    )

def test_architecture_proof_model_contract_rejects_bundle_only_model(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    architecture_name = "docs/architecture/ARCHITECTURE.md"
    write_text(
        tmp_path / architecture_name,
        """
        # Architecture

        `aoa-evals` stores portable eval bundles.

        ## Eval bundles

        Eval bundles package bounded claims, fixtures, scoring, and reports.
        """,
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == architecture_name
        and "mechanics/EVIDENCE_CLUSTERS.md" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == architecture_name
        and "single controlled bridge" in issue.message
        for issue in issues
    )

def test_root_design_surfaces_reject_stale_mechanic_ready_wording(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    design_path = tmp_path / "DESIGN.md"
    design_path.write_text(
        design_path.read_text(encoding="utf-8").replace(
            "active mechanic\nauthority classes",
            "mechanic-ready\nauthority classes",
        ),
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "DESIGN.md"
        and "active mechanic authority" in issue.message
        and "mechanic-ready" in issue.message
        for issue in issues
    )

def test_root_design_surfaces_reject_negative_architecture_role_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    architecture_path = tmp_path / "docs" / "architecture" / "ARCHITECTURE.md"
    architecture_path.write_text(
        architecture_path.read_text(encoding="utf-8")
        + "\nIt is not the system design thesis.\n",
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "docs/architecture/ARCHITECTURE.md"
        and "positive" in issue.message
        and "It is not the system design thesis" in issue.message
        for issue in issues
    )

def test_root_design_surfaces_reject_architecture_direction_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    architecture_path = tmp_path / "docs" / "architecture" / "ARCHITECTURE.md"
    architecture_path.write_text(
        architecture_path.read_text(encoding="utf-8")
        + "\n- regression visibility without metric theater\n"
        + "- growth tracking without inflated claims\n",
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "docs/architecture/ARCHITECTURE.md"
        and "proof route" in issue.message
        and "regression visibility without metric theater" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "docs/architecture/ARCHITECTURE.md"
        and "proof route" in issue.message
        and "growth tracking without inflated claims" in issue.message
        for issue in issues
    )

def test_root_design_surfaces_reject_old_route_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    design_path = tmp_path / "DESIGN.md"
    design_path.write_text(
        design_path.read_text(encoding="utf-8")
        + "\nThe repository should feel useful without requiring a full local AoA deployment.\n"
        + "\nGreen file presence alone is not proof.\n"
        + "This file does not override local owner truth.\n",
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == "DESIGN.md"
        and "positive owner language" in issue.message
        and "Green file presence alone is not proof" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "DESIGN.md"
        and "positive owner language" in issue.message
        and "This file does not override local owner truth" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "DESIGN.md"
        and "positive owner language" in issue.message
        and "without requiring a full local AoA deployment" in issue.message
        for issue in issues
    )

def test_design_agents_rejects_future_mechanic_package_wording(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    design_agents_path = tmp_path / root_design_validator.DESIGN_AGENTS_NAME
    design_agents_path.write_text(
        design_agents_path.read_text(encoding="utf-8").replace(
            "Active mechanic packages", "Future mechanic packages"
        ),
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == root_design_validator.DESIGN_AGENTS_NAME
        and "active mechanic packages" in issue.message
        and "Future mechanic packages" in issue.message
        for issue in issues
    )

def test_design_agents_rejects_old_negative_route_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "docs/decisions/AGENTS.md",
        root_design_validator.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        root_design_validator.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    design_agents_path = tmp_path / root_design_validator.DESIGN_AGENTS_NAME
    design_agents_path.write_text(
        design_agents_path.read_text(encoding="utf-8")
        + "\nthey do not replace the\nsource surface\n"
        + "\nPresence-only checks are not enough for proof meaning.\n"
        + "### Negative boundaries stay narrow\n",
        encoding="utf-8",
    )

    issues = root_design_validator.validate_root_design_surfaces(tmp_path)

    assert any(
        issue.location == root_design_validator.DESIGN_AGENTS_NAME
        and "owner routes" in issue.message
        and "Presence-only checks are not enough" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_design_validator.DESIGN_AGENTS_NAME
        and "owner routes" in issue.message
        and "Negative boundaries stay narrow" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_design_validator.DESIGN_AGENTS_NAME
        and "owner routes" in issue.message
        and "they do not replace" in issue.message
        for issue in issues
    )

def test_proof_topology_requires_stats_authority_class_and_district(
    tmp_path: Path,
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8")
        .replace("Owner-local statistics", "Unclassified local data", 1)
        .replace(
            "| `stats/` | owner-local statistics port",
            "| `stats/` | unclassified local data",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any("Owner-local statistics" in issue.message for issue in issues)
    assert any("owner-local statistics port" in issue.message for issue in issues)


def test_proof_topology_rejects_preparatory_mechanic_wording(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8").replace(
            "mechanic operations apart",
            "mechanic-ready operations apart",
        ),
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "active mechanics" in issue.message
        and "mechanic-ready operations" in issue.message
        for issue in issues
    )

def test_proof_topology_rejects_negative_role_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8")
        + "\nIt is not the roadmap.\n",
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "active mechanics" in issue.message
        and "It is not the roadmap" in issue.message
        for issue in issues
    )

def test_proof_topology_requires_positive_authority_boundary_routes(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8").replace(
            "candidate packets enter bundle-local review before verdict meaning",
            "candidate evidence is only a loose input",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "candidate packets enter bundle-local review before verdict meaning"
        in issue.message
        for issue in issues
    )

def test_proof_topology_required_tokens_must_live_in_proof_topology(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/architecture/ROUTE_RESIDUE_GUARDS.md",
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    token = root_proof_topology_validator.PROOF_TOPOLOGY_REQUIRED_TOKENS[0]
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8").replace(token, "token removed from proof topology", 1),
        encoding="utf-8",
    )
    route_guard_path = tmp_path / "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
    route_guard_path.write_text(
        route_guard_path.read_text(encoding="utf-8") + f"\n{token}\n",
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and token in issue.message
        for issue in issues
    )

def test_proof_topology_rejects_old_negative_route_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8")
        + "\nquests are obligations, not eval bundles\n"
        + "no active root reports payload should live here\n"
        + "not proof canon\n"
        + "a generic root validator file and a rationale-only decision ref are not enough\n"
        + "If those answers are unclear, do not move the file yet.\n",
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "owner routes" in issue.message
        and "quests are obligations" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "owner routes" in issue.message
        and "no active root reports payload" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "owner routes" in issue.message
        and "not proof canon" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "owner routes" in issue.message
        and "rationale-only decision ref" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "owner routes" in issue.message
        and "do not move the file yet" in issue.message
        for issue in issues
    )

def test_memory_consumer_topology_requires_positive_source_authority_route(
    tmp_path: Path
) -> None:
    for path_name in (
        "README.md",
        "docs/guides/EVAL_PHILOSOPHY.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        root_memory_boundary_validator.MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    topology_path = tmp_path / root_proof_topology_validator.PROOF_TOPOLOGY_NAME
    topology_path.write_text(
        topology_path.read_text(encoding="utf-8").replace(
            "reviewed memory provides recall context; local proof authority stays with the eval bundle or owning mechanic",
            "reviewed memory route is unclear",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_memory_boundary_validator.validate_memory_consumer_proof_boundary_surfaces(
        tmp_path
    )

    assert any(
        issue.location == root_proof_topology_validator.PROOF_TOPOLOGY_NAME
        and "reviewed memory provides recall context" in issue.message
        for issue in issues
    )

def test_proof_topology_decision_rejects_deferred_movement_wording(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    decision_path = tmp_path / "docs" / "decisions" / "AOA-EV-D-0005-proof-topology-map.md"
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8")
        + "\nKeep physical movement deferred until a later phase.\n",
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == "docs/decisions/AOA-EV-D-0005-proof-topology-map.md"
        and "active mechanics atlas" in issue.message
        and "Keep physical movement deferred" in issue.message
        for issue in issues
    )

def test_proof_topology_rejects_roadmap_preparatory_mechanic_wording(
    tmp_path: Path
) -> None:
    for path_name in (
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        "ROADMAP.md",
    ):
        copy_repo_text(tmp_path, path_name)
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8")
        + "\nGoal: classify mechanic-ready artifact classes before movement.\n",
        encoding="utf-8",
    )

    issues = root_proof_topology_validator.validate_proof_topology_surfaces(tmp_path)

    assert any(
        issue.location == "ROADMAP.md"
        and "active mechanics direction" in issue.message
        and "mechanic-ready artifact classes" in issue.message
        for issue in issues
    )

def test_agent_index_surface_validates_current_route() -> None:
    assert root_agent_index_validator.validate_agent_index_surface(REPO_ROOT) == []

def test_github_agents_surface_validates_current_route() -> None:
    assert root_audit_routes_validator.validate_github_agent_surface(REPO_ROOT) == []

def test_github_agents_rejects_stale_negative_platform_scaffold(
    tmp_path: Path
) -> None:
    copy_repo_text(tmp_path, root_audit_routes_validator.GITHUB_AGENTS_NAME)
    agents_path = tmp_path / root_audit_routes_validator.GITHUB_AGENTS_NAME

    for stale_phrase in root_audit_routes_validator.GITHUB_AGENTS_STALE_ROUTE_PHRASES:
        agents_path.write_text(
            agents_path.read_text(encoding="utf-8")
            + f"\n\n{stale_phrase}.\n",
            encoding="utf-8",
        )

        issues = root_audit_routes_validator.validate_github_agent_surface(tmp_path)

        assert any(
            issue.location == root_audit_routes_validator.GITHUB_AGENTS_NAME
            and "operating card and boundary route table" in issue.message
            for issue in issues
        )

        agents_path.write_text(
            agents_path.read_text(encoding="utf-8").replace(
                f"\n\n{stale_phrase}.\n",
                "",
            ),
            encoding="utf-8",
        )

def test_agent_index_surface_rejects_missing_chain(tmp_path: Path) -> None:
    for path_name in (
        root_agent_index_validator.AGENT_INDEX_NAME,
        root_agent_index_validator.AGENT_INDEX_CHAIN_DECISION_NAME,
        "README.md",
        "docs/README.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "ROADMAP.md",
        root_agent_index_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    index_path = tmp_path / root_agent_index_validator.AGENT_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
            "repo -> file",
        ),
        encoding="utf-8",
    )

    issues = root_agent_index_validator.validate_agent_index_surface(tmp_path)

    assert any(
        issue.location == root_agent_index_validator.AGENT_INDEX_NAME
        and "repo -> authority class -> operation" in issue.message
        for issue in issues
    )


def test_agent_index_surface_requires_stats_authority_route(tmp_path: Path) -> None:
    for path_name in (
        root_agent_index_validator.AGENT_INDEX_NAME,
        root_agent_index_validator.AGENT_INDEX_CHAIN_DECISION_NAME,
        "README.md",
        "docs/README.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "ROADMAP.md",
        root_agent_index_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    index_path = tmp_path / root_agent_index_validator.AGENT_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "| `stats/**` | owner-local statistics",
            "| `stats/**` | unclassified",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_agent_index_validator.validate_agent_index_surface(tmp_path)

    assert any(
        issue.location == root_agent_index_validator.AGENT_INDEX_NAME
        and "owner-local statistics" in issue.message
        for issue in issues
    )

def test_agent_index_surface_rejects_old_negative_route_scaffold(
    tmp_path: Path
) -> None:
    for path_name in (
        root_agent_index_validator.AGENT_INDEX_NAME,
        root_agent_index_validator.AGENT_INDEX_CHAIN_DECISION_NAME,
        "README.md",
        "docs/README.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        "ROADMAP.md",
        root_agent_index_validator.MECHANICS_EVIDENCE_CLUSTERS_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    index_path = tmp_path / root_agent_index_validator.AGENT_INDEX_NAME
    index_path.write_text(
        index_path.read_text(encoding="utf-8")
        + "\nUse this index when the path name is not enough by itself.\n"
        + "An agent should expect only route cards here.\n",
        encoding="utf-8",
    )

    issues = root_agent_index_validator.validate_agent_index_surface(tmp_path)

    assert any(
        issue.location == root_agent_index_validator.AGENT_INDEX_NAME
        and "explicit owner routes" in issue.message
        and "path name is not enough" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == root_agent_index_validator.AGENT_INDEX_NAME
        and "explicit owner routes" in issue.message
        and "An agent should expect only" in issue.message
        for issue in issues
    )

def test_memory_consumer_proof_boundary_validates_current_route() -> None:
    assert root_memory_boundary_validator.validate_memory_consumer_proof_boundary_surfaces(REPO_ROOT) == []

def test_memory_consumer_proof_boundary_rejects_root_route_anchor_loss(
    tmp_path: Path
) -> None:
    for path_name in (
        "README.md",
        "docs/guides/EVAL_PHILOSOPHY.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        root_memory_boundary_validator.MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "proof authority stays with",
            "proof route is unclear",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_memory_boundary_validator.validate_memory_consumer_proof_boundary_surfaces(tmp_path)

    assert any(
        issue.location == "README.md"
        and "proof authority stays with" in issue.message
        for issue in issues
    )

def test_memory_consumer_proof_boundary_requires_positive_memory_route(
    tmp_path: Path
) -> None:
    for path_name in (
        "README.md",
        "docs/guides/EVAL_PHILOSOPHY.md",
        root_proof_topology_validator.PROOF_TOPOLOGY_NAME,
        root_memory_boundary_validator.MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME,
        "docs/decisions/README.md",
    ):
        copy_repo_text(tmp_path, path_name)
    philosophy_path = tmp_path / "docs" / "guides" / "EVAL_PHILOSOPHY.md"
    philosophy_path.write_text(
        philosophy_path.read_text(encoding="utf-8").replace(
            "Reviewed memory routes recall into proof review.",
            "Memory route is unclear.",
            1,
        ),
        encoding="utf-8",
    )

    issues = root_memory_boundary_validator.validate_memory_consumer_proof_boundary_surfaces(tmp_path)

    assert any(
        issue.location == "docs/guides/EVAL_PHILOSOPHY.md"
        and "Reviewed memory routes recall into proof review." in issue.message
        for issue in issues
    )
