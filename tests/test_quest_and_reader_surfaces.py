from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import (
    questbook_context as questbook_context_validator,
    questbook_obligation_index as questbook_obligation_index_validator,
    questbook_projection_parity as questbook_projection_parity_validator,
    questbook_projection_records as questbook_projection_records_validator,
    questbook_progression as questbook_progression_validator,
    questbook_route_paths as questbook_route_paths_validator,
    questbook_routes as questbook_routes_validator,
    questbook_schema_lifecycle as questbook_schema_lifecycle_validator,
    questbook_source_constants as questbook_source_constants_validator,
    questbook_source_records as questbook_source_records_validator,
    report_index as report_index_validator,
    root_topology as root_topology_validator,
    runtime_evidence_selection as runtime_evidence_selection_validator,
    runtime_candidate_common as runtime_candidate_common_validator,
    runtime_candidate_intake as runtime_candidate_intake_validator,
    runtime_candidate_template_index as runtime_candidate_template_index_validator,
)
from validate_repo import (
    run_validation,
)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def eval_family_for_test(category: str = "workflow", baseline_mode: str = "none") -> Path:
    if baseline_mode == "fixed-baseline":
        return Path("comparison") / "fixed-baseline"
    if baseline_mode == "peer-compare":
        return Path("comparison") / "peer-compare"
    if baseline_mode == "longitudinal-window":
        return Path("comparison") / "longitudinal-window"
    return Path(category)


def eval_dir_for_test(
    repo_root: Path,
    name: str,
    *,
    category: str = "workflow",
    baseline_mode: str = "none",
) -> Path:
    matches = sorted((repo_root / "evals").glob(f"**/{name}/eval.yaml"))
    if matches:
        return matches[0].parent
    return repo_root / "evals" / eval_family_for_test(category, baseline_mode) / name


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def quest_fixture_path(repo_root: Path, quest_id: str) -> Path:
    matches = sorted((repo_root / "quests").rglob(f"{quest_id}.yaml"))
    if len(matches) != 1:
        raise AssertionError(f"expected one source path for {quest_id}, found {len(matches)}")
    return matches[0]


def make_questbook_surface(repo_root: Path) -> None:
    for relative_path in [
        "QUESTBOOK.md",
        "quests/LIFECYCLE.md",
        "docs/operations/QUESTBOOK_EVAL_INTEGRATION.md",
        "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md",
        "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
        "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
        "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json",
        "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json",
        "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json",
        "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json",
        "mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json",
        "generated/quest_catalog.min.json",
        "generated/quest_dispatch.min.json",
        "generated/quest_catalog.min.example.json",
        "generated/quest_dispatch.min.example.json",
        "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
    ]:
        copy_repo_text(repo_root, relative_path)
    for quest_path in sorted((REPO_ROOT / "quests").rglob("AOA-EV-Q-*.yaml")):
        copy_repo_text(repo_root, quest_path.relative_to(REPO_ROOT).as_posix())


def rewrite_questbook_projections(repo_root: Path) -> None:
    write_json_payload(
        repo_root / "generated" / "quest_catalog.min.json",
        questbook_projection_records_validator.build_quest_catalog_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_catalog.min.example.json",
        questbook_projection_records_validator.build_quest_catalog_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_dispatch.min.json",
        questbook_projection_records_validator.build_quest_dispatch_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_dispatch.min.example.json",
        questbook_projection_records_validator.build_quest_dispatch_projection(repo_root),
    )


def make_quest_route_surface(repo_root: Path) -> None:
    for relative_path in [
        "quests/README.md",
        "quests/AGENTS.md",
        "quests/LIFECYCLE.md",
        "docs/decisions/AOA-EV-D-0004-questbook-topology.md",
        "docs/decisions/AOA-EV-D-0018-quest-lane-state-source-layout.md",
        "docs/decisions/AOA-EV-D-0021-quest-lifecycle-contract.md",
        questbook_route_paths_validator.AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
    ]:
        copy_repo_text(repo_root, relative_path)


def make_runtime_candidate_template_index_surface(repo_root: Path) -> None:
    for relative_path in [
        "generated/eval_catalog.min.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.workhorse-local.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json",
        "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
        "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
        "mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
        "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_runtime_candidate_intake_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
        "docs/guides/EVAL_REVIEW_GUIDE.md",
        "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.workhorse-local.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json",
        "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
        "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
        "mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
        "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_eval_report_index_surface(repo_root: Path) -> None:
    for relative_path in [
        "generated/eval_report_index.min.json",
        "scripts/generate_eval_report_index.py",
    ]:
        copy_repo_text(repo_root, relative_path)
    for report_path in sorted((REPO_ROOT / "evals").glob("**/reports/*.report.json")):
        bundle_dir = report_path.parents[1]
        for source_path in [
            bundle_dir / "EVAL.md",
            bundle_dir / "eval.yaml",
            bundle_dir / "reports" / "summary.schema.json",
            report_path,
        ]:
            copy_repo_text(repo_root, source_path.relative_to(REPO_ROOT).as_posix())


def validate_runtime_candidate_template_index(repo_root: Path, *, builder_loader=None):
    return runtime_candidate_template_index_validator.validate_runtime_candidate_template_index(
        repo_root,
        builder_loader=builder_loader
        or runtime_candidate_template_index_validator.load_runtime_candidate_template_index_builder,
    )


def validate_runtime_candidate_intake(repo_root: Path, *, builder_loader=None):
    return runtime_candidate_intake_validator.validate_runtime_candidate_intake(
        repo_root,
        builder_loader=builder_loader
        or runtime_candidate_intake_validator.load_runtime_candidate_intake_builder,
    )


def validate_eval_report_index(repo_root: Path, *, builder_loader=None):
    return report_index_validator.validate_eval_report_index(
        repo_root,
        builder_loader=builder_loader
        or report_index_validator.load_eval_report_index_builder,
    )


def validate_questbook_surface(repo_root: Path):
    issues = []
    schema_validation = (
        questbook_schema_lifecycle_validator.validate_quest_schema_lifecycle_surfaces(
            repo_root
        )
    )
    issues.extend(schema_validation.issues)
    source_validation = questbook_source_records_validator.validate_quest_source_records(
        repo_root
    )
    issues.extend(source_validation.issues)
    issues.extend(
        questbook_obligation_index_validator.validate_questbook_obligation_index(
            repo_root,
            active_quest_ids=source_validation.active_quest_ids,
            closed_quest_ids=source_validation.closed_quest_ids,
            needs_orchestrator_alignment_doc=(
                source_validation.needs_orchestrator_alignment_doc
            ),
        )
    )
    if source_validation.unlock_proof_bridge_quest_present:
        issues.extend(
            questbook_progression_validator.validate_unlock_proof_bridge_surface(
                repo_root
            )
        )
    questbook_projection_parity_validator.validate_generated_quest_projection_surfaces(
        repo_root,
        valid_quest_ids=source_validation.valid_quest_ids,
        expected_catalog_entries=source_validation.expected_catalog_entries,
        expected_dispatch_entries=source_validation.expected_dispatch_entries,
        issues=issues,
    )
    return issues


def write_yaml_payload(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json_payload(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

class TestValidateQuestbookSurface:
    def test_valid_questbook_surface_passes(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)

        assert validate_questbook_surface(tmp_path) == []

    def test_questbook_surface_rejects_generic_obligation_heading(
        self, tmp_path: Path
    ) -> None:
        make_questbook_surface(tmp_path)
        questbook_path = tmp_path / "QUESTBOOK.md"
        questbook_path.write_text(
            questbook_path.read_text(encoding="utf-8").replace(
                "# Questbook Obligation Index",
                "# QUESTBOOK.md - aoa-evals",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location == "QUESTBOOK.md"
            and "# Questbook Obligation Index" in issue.message
            for issue in issues
        )

    def test_questbook_surface_requires_reviewed_harvest_route(
        self, tmp_path: Path
    ) -> None:
        make_questbook_surface(tmp_path)
        questbook_path = tmp_path / "QUESTBOOK.md"
        questbook_path.write_text(
            questbook_path.read_text(encoding="utf-8").replace(
                "Promotion happens through reviewed owner acceptance",
                "Promotion happens immediately",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location == "QUESTBOOK.md"
            and "Promotion happens through reviewed owner acceptance"
            in issue.message
            for issue in issues
        )

    def test_quest_lifecycle_surface_validates_current_state_contract(self) -> None:
        quest_schema = json.loads(
            (REPO_ROOT / questbook_source_constants_validator.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        assert questbook_schema_lifecycle_validator.validate_quest_lifecycle_surface(REPO_ROOT, quest_schema) == []

    def test_quest_lifecycle_surface_rejects_generic_heading(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "quests/LIFECYCLE.md")
        copy_repo_text(tmp_path, "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json")
        lifecycle_path = tmp_path / "quests" / "LIFECYCLE.md"
        lifecycle_path.write_text(
            lifecycle_path.read_text(encoding="utf-8").replace(
                "# Quest Lifecycle Contract",
                "# Quest Lifecycle",
                1,
            ),
            encoding="utf-8",
        )
        quest_schema = json.loads(
            (tmp_path / questbook_source_constants_validator.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        issues = questbook_schema_lifecycle_validator.validate_quest_lifecycle_surface(tmp_path, quest_schema)

        assert any(
            issue.location == "quests/LIFECYCLE.md"
            and "# Quest Lifecycle Contract" in issue.message
            for issue in issues
        )

    def test_quest_lifecycle_surface_rejects_missing_state_matrix_entry(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "quests/LIFECYCLE.md")
        copy_repo_text(tmp_path, "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json")
        lifecycle_path = tmp_path / "quests" / "LIFECYCLE.md"
        lifecycle_path.write_text(
            lifecycle_path.read_text(encoding="utf-8").replace(
                "| `reanchor` | listed in `QUESTBOOK.md` |",
                "| `return-anchor` | listed in `QUESTBOOK.md` |",
            ),
            encoding="utf-8",
        )
        quest_schema = json.loads(
            (tmp_path / questbook_source_constants_validator.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        issues = questbook_schema_lifecycle_validator.validate_quest_lifecycle_surface(tmp_path, quest_schema)

        assert any(
            issue.location == "quests/LIFECYCLE.md"
            and "state 'reanchor'" in issue.message
            for issue in issues
        )

    def test_missing_orchestrator_catalog_is_ignored_until_needed(
        self,
        tmp_path: Path,
        monkeypatch,
    ) -> None:
        make_questbook_surface(tmp_path)
        missing_agents_root = tmp_path / "missing-aoa-agents"

        monkeypatch.setattr(questbook_context_validator, "AOA_AGENTS_ROOT", missing_agents_root)

        assert validate_questbook_surface(tmp_path) == []

    def test_missing_questbook_file_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        (tmp_path / "QUESTBOOK.md").unlink()

        issues = validate_questbook_surface(tmp_path)

        assert any(issue.location.endswith("QUESTBOOK.md") for issue in issues)
        assert any("file is missing" in issue.message for issue in issues)

    def test_discover_quest_names_includes_additive_quests(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)

        expected_quest_names = [
            path.stem
            for path in sorted(
                (REPO_ROOT / "quests").rglob("AOA-EV-Q-*.yaml"),
                key=lambda path: questbook_projection_records_validator.quest_sort_key(path.stem),
            )
        ]

        assert questbook_projection_records_validator.discover_quest_names(tmp_path) == expected_quest_names

    def test_missing_tracked_id_in_questbook_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        questbook_path = tmp_path / "QUESTBOOK.md"
        questbook_text = questbook_path.read_text(encoding="utf-8").replace(
            "AOA-EV-Q-0004",
            "AOA-EV-Q-9999",
        )
        questbook_path.write_text(questbook_text, encoding="utf-8")

        issues = validate_questbook_surface(tmp_path)

        assert any(
            "QUESTBOOK.md must reference active quest id 'AOA-EV-Q-0004'" in issue.message
            for issue in issues
        )

    def test_missing_integration_boundary_token_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        integration_path = tmp_path / "docs" / "operations" / "QUESTBOOK_EVAL_INTEGRATION.md"
        integration_text = integration_path.read_text(encoding="utf-8").replace(
            "verdict-bridge",
            "verdict bridge",
        )
        integration_path.write_text(integration_text, encoding="utf-8")

        issues = validate_questbook_surface(tmp_path)

        assert any("integration note must mention 'verdict-bridge'" in issue.message for issue in issues)

    def test_missing_quest_yaml_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_fixture_path(tmp_path, "AOA-EV-Q-0002").unlink()

        issues = validate_questbook_surface(tmp_path)

        assert any("quests" == issue.location for issue in issues)
        assert any("missing required foundation quest file 'AOA-EV-Q-0002.yaml'" in issue.message for issue in issues)

    def test_quest_id_filename_mismatch_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0003")
        quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        quest_data["id"] = "AOA-EV-Q-9999"
        write_yaml_payload(quest_path, quest_data)

        issues = validate_questbook_surface(tmp_path)

        assert any("quest id must match filename 'AOA-EV-Q-0003'" in issue.message for issue in issues)

    def test_top_level_quest_source_path_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0004")
        stale_path = tmp_path / "quests" / quest_path.name
        stale_path.write_text(quest_path.read_text(encoding="utf-8"), encoding="utf-8")
        quest_path.unlink()

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location == "quests/AOA-EV-Q-0004.yaml"
            and "quests/<lane>/<state>/<quest-id>.yaml" in issue.message
            for issue in issues
        )

    def test_quest_state_directory_mismatch_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0005")
        wrong_state_path = tmp_path / "quests" / "proof" / "triaged" / quest_path.name
        wrong_state_path.parent.mkdir(parents=True, exist_ok=True)
        wrong_state_path.write_text(quest_path.read_text(encoding="utf-8"), encoding="utf-8")
        quest_path.unlink()

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location == "quests/proof/triaged/AOA-EV-Q-0005.yaml"
            and "must match state 'captured'" in issue.message
            for issue in issues
        )

    def test_wrong_repo_value_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0001")
        quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        quest_data["repo"] = "aoa-techniques"
        write_yaml_payload(quest_path, quest_data)

        issues = validate_questbook_surface(tmp_path)

        assert any("quest repo must be 'aoa-evals'" in issue.message for issue in issues)

    def test_missing_public_safe_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0005")
        quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        quest_data["public_safe"] = False
        write_yaml_payload(quest_path, quest_data)

        issues = validate_questbook_surface(tmp_path)

        assert any("quest must set public_safe to true" in issue.message for issue in issues)

    def test_example_projection_drift_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        catalog_path = tmp_path / "generated" / "quest_catalog.min.example.json"
        catalog_data = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog_data[0]["source_path"] = "quests/not-the-right-file.yaml"
        write_json_payload(catalog_path, catalog_data)

        issues = validate_questbook_surface(tmp_path)

        assert any("generated quest catalog example is out of date or mismatched" in issue.message for issue in issues)

    def test_missing_live_catalog_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        (tmp_path / "generated" / "quest_catalog.min.json").unlink()

        issues = validate_questbook_surface(tmp_path)

        assert any("generated/quest_catalog.min.json" in issue.location for issue in issues)
        assert any("file is missing" in issue.message for issue in issues)

    def test_live_dispatch_drift_fails(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        dispatch_path = tmp_path / "generated" / "quest_dispatch.min.json"
        dispatch_data = json.loads(dispatch_path.read_text(encoding="utf-8"))
        dispatch_data[0]["source_path"] = "quests/not-the-right-file.yaml"
        write_json_payload(dispatch_path, dispatch_data)

        issues = validate_questbook_surface(tmp_path)

        assert any("generated quest dispatch is out of date or mismatched" in issue.message for issue in issues)

    def test_live_dispatch_optional_field_schema_violation_surfaces_before_parity(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        dispatch_path = tmp_path / "generated" / "quest_dispatch.min.json"
        dispatch_data = json.loads(dispatch_path.read_text(encoding="utf-8"))
        dispatch_data[0]["fallback_tier"] = None
        write_json_payload(dispatch_path, dispatch_data)

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location.endswith("quest_dispatch.min.json[0]")
            and "fallback_tier" in issue.message
            for issue in issues
        )
        assert not any(
            issue.location.endswith("quest_dispatch.min.json")
            and issue.message == "generated quest dispatch is out of date or mismatched"
            for issue in issues
        )

    def test_unlock_proof_bridge_additive_surface_passes(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        for relative_path in [
            "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
            "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json",
            "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
            "quests/unlock/triaged/AOA-EV-Q-0009.yaml",
        ]:
            copy_repo_text(tmp_path, relative_path)
        rewrite_questbook_projections(tmp_path)

        issues = validate_questbook_surface(tmp_path)
        issues.extend(
            questbook_progression_validator.validate_unlock_proof_bridge_surface(tmp_path)
        )

        assert issues == []

    def test_unlock_proof_bridge_rejects_legacy_playbook_quest_ref(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        for relative_path in [
            "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
            "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json",
            "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
            "quests/unlock/triaged/AOA-EV-Q-0009.yaml",
        ]:
            copy_repo_text(tmp_path, relative_path)
        example_path = (
            tmp_path
            / "mechanics"
            / "rpg"
            / "parts"
            / "progression-unlocks"
            / "generated"
            / "unlock_proof_cards.min.example.json"
        )
        example_text = example_path.read_text(encoding="utf-8").replace("AOA-PB-Q-0007", "AOA-PB-Q-0004")
        example_path.write_text(example_text, encoding="utf-8")
        rewrite_questbook_projections(tmp_path)

        issues = questbook_progression_validator.validate_unlock_proof_bridge_surface(tmp_path)

        assert any("legacy playbook quest id" in issue.message for issue in issues)

    def test_example_dispatch_optional_field_schema_violation_surfaces_before_parity(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        dispatch_path = tmp_path / "generated" / "quest_dispatch.min.example.json"
        dispatch_data = json.loads(dispatch_path.read_text(encoding="utf-8"))
        dispatch_data[0]["wrapper_class"] = None
        write_json_payload(dispatch_path, dispatch_data)

        issues = validate_questbook_surface(tmp_path)

        assert any(
            issue.location.endswith("quest_dispatch.min.example.json[0]")
            and "wrapper_class" in issue.message
            for issue in issues
        )
        assert not any(
            issue.location.endswith("quest_dispatch.min.example.json")
            and issue.message == "generated quest dispatch example is out of date or mismatched"
            for issue in issues
        )

    def test_run_validation_reports_missing_questbook_surface_without_gate(self, tmp_path: Path) -> None:
        issues = run_validation(tmp_path)

        assert any(
            issue.location.endswith("QUESTBOOK.md") and issue.message == "file is missing"
            for issue in issues
        )

    def test_quest_projection_includes_additive_quest(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)

        catalog_projection = questbook_projection_records_validator.build_quest_catalog_projection(tmp_path)
        dispatch_projection = questbook_projection_records_validator.build_quest_dispatch_projection(tmp_path)
        expected_quest_names = [
            path.stem
            for path in sorted(
                (REPO_ROOT / "quests").rglob("AOA-EV-Q-*.yaml"),
                key=lambda path: questbook_projection_records_validator.quest_sort_key(path.stem),
            )
        ]

        assert [entry["id"] for entry in catalog_projection] == expected_quest_names
        assert [entry["id"] for entry in dispatch_projection] == expected_quest_names


class TestValidateQuestRouteSurfaces:
    def test_quest_route_surfaces_validate_current_schema_backed_layout(self) -> None:
        assert questbook_routes_validator.validate_quest_route_surfaces(
            REPO_ROOT,
            context=root_topology_validator.questbook_route_context(),
        ) == []

    def test_quest_route_surfaces_reject_generic_readme_heading(
        self, tmp_path: Path
    ) -> None:
        make_quest_route_surface(tmp_path)
        readme_path = tmp_path / "quests" / "README.md"
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "# Quest Source Records",
                "# Quests",
                1,
            ),
            encoding="utf-8",
        )

        issues = questbook_routes_validator.validate_quest_route_surfaces(
            tmp_path,
            context=root_topology_validator.questbook_route_context(),
        )

        assert any(
            issue.location == "quests/README.md"
            and "# Quest Source Records" in issue.message
            for issue in issues
        )

    def test_quest_route_surfaces_reject_stale_negative_scaffold(
        self, tmp_path: Path
    ) -> None:
        make_quest_route_surface(tmp_path)
        readme_path = tmp_path / "quests" / "README.md"
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "A quest is an obligation-return source record:",
                "Quests are not eval bundles.\n\nA quest is an obligation-return source record:",
                1,
            ),
            encoding="utf-8",
        )
        lifecycle_path = tmp_path / "quests" / "LIFECYCLE.md"
        lifecycle_path.write_text(
            lifecycle_path.read_text(encoding="utf-8").replace(
                "below eval result receipt\ncreation",
                "below eval result receipt\ncreation. It does not create an eval result receipt",
                1,
            ),
            encoding="utf-8",
        )

        issues = questbook_routes_validator.validate_quest_route_surfaces(
            tmp_path,
            context=root_topology_validator.questbook_route_context(),
        )

        assert any(
            issue.location == "quests/README.md"
            and "positive role routing" in issue.message
            and "Quests are not eval bundles." in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "quests/LIFECYCLE.md"
            and "positive role routing" in issue.message
            and "does not create an eval result receipt" in issue.message
            for issue in issues
        )

    def test_quest_route_surfaces_reject_markdown_notes_in_lifecycle_path(
        self, tmp_path: Path
    ) -> None:
        make_quest_route_surface(tmp_path)
        stale_note = tmp_path / "quests" / "agon" / "captured" / "AOE-Q-AGON-0001.md"
        write_text(
            stale_note,
            """
            # AOE-Q-AGON-0001

            Legacy note form.
            """,
        )

        issues = questbook_routes_validator.validate_quest_route_surfaces(
            tmp_path,
            context=root_topology_validator.questbook_route_context(),
        )

        assert any(
            issue.location == "quests/agon/captured/AOE-Q-AGON-0001.md"
            and "markdown quest notes must not live under active quest lifecycle paths"
            in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_validates_for_current_repo(self) -> None:
        issues = validate_runtime_candidate_template_index(REPO_ROOT)

        assert issues == []

    def test_runtime_candidate_template_index_drift_fails(self, tmp_path: Path) -> None:
        make_runtime_candidate_template_index_surface(tmp_path)
        index_path = tmp_path / runtime_candidate_common_validator.RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["templates"][0]["review_required"] = False
        write_json_payload(index_path, payload)

        issues = validate_runtime_candidate_template_index(tmp_path)

        assert any(
            issue.location == "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_rejects_non_normalized_required_runtime_artifacts(self, tmp_path: Path) -> None:
        make_runtime_candidate_template_index_surface(tmp_path)
        example_path = (
            tmp_path
            / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR
            / "runtime_evidence_selection.workhorse-local.example.json"
        )
        example_payload = json.loads(example_path.read_text(encoding="utf-8"))
        example_payload["selected_evidence"][0]["evidence_role"] = "Summary Artifact"
        write_json_payload(example_path, example_payload)

        index_path = tmp_path / runtime_candidate_common_validator.RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        for entry in payload["templates"]:
            if entry["template_name"] == "workhorse-q4-vs-q6-latency-tradeoff":
                entry["required_runtime_artifacts"][0] = "Summary Artifact"
                break
        write_json_payload(index_path, payload)

        issues = validate_runtime_candidate_template_index(tmp_path)

        assert any(
            issue.location.startswith("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json.templates[")
            and "normalized to lowercase runtime artifact names" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_reports_builder_system_exit(self) -> None:
        class FailingBuilder:
            def build_runtime_candidate_template_index_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        issues = validate_runtime_candidate_template_index(
            REPO_ROOT,
            builder_loader=lambda repo_root: FailingBuilder(),
        )

        assert [(issue.location, issue.message) for issue in issues] == [
            (
                "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
                "builder-exit",
            )
        ]

    def test_runtime_candidate_intake_validates_for_current_repo(self) -> None:
        issues = validate_runtime_candidate_intake(REPO_ROOT)

        assert issues == []

    def test_runtime_candidate_intake_drift_fails(self, tmp_path: Path) -> None:
        make_runtime_candidate_intake_surface(tmp_path)
        intake_path = tmp_path / runtime_candidate_common_validator.RUNTIME_CANDIDATE_INTAKE_NAME
        payload = json.loads(intake_path.read_text(encoding="utf-8"))
        payload["templates"][0]["review_guide_ref"] = "docs/DRIFTED.md"
        write_json_payload(intake_path, payload)

        issues = validate_runtime_candidate_intake(tmp_path)

        assert any(
            issue.location == "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_intake_rejects_missing_owner_review_ref(self, tmp_path: Path) -> None:
        make_runtime_candidate_intake_surface(tmp_path)
        intake_path = tmp_path / runtime_candidate_common_validator.RUNTIME_CANDIDATE_INTAKE_NAME
        payload = json.loads(intake_path.read_text(encoding="utf-8"))
        payload["templates"][0]["owner_review_refs"] = []
        write_json_payload(intake_path, payload)

        issues = validate_runtime_candidate_intake(tmp_path)

        assert any(
            issue.location.startswith("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json.templates[")
            and "owner_review_refs must stay a non-empty list" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_intake_reports_builder_system_exit(self) -> None:
        class FailingBuilder:
            def build_runtime_candidate_intake_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        issues = validate_runtime_candidate_intake(
            REPO_ROOT,
            builder_loader=lambda repo_root: FailingBuilder(),
        )

        assert [(issue.location, issue.message) for issue in issues] == [
            (
                "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
                "builder-exit",
            )
        ]

    def test_eval_report_index_validates_for_current_repo(self) -> None:
        issues = validate_eval_report_index(REPO_ROOT)

        assert issues == []

    def test_eval_report_index_drift_fails(self, tmp_path: Path) -> None:
        make_eval_report_index_surface(tmp_path)
        index_path = tmp_path / "generated" / "eval_report_index.min.json"
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["reports"][0]["verdict"] = "drifted verdict"
        write_json_payload(index_path, payload)

        issues = validate_eval_report_index(tmp_path)

        assert any(
            issue.location == "generated/eval_report_index.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )
        assert any(
            issue.location.startswith("generated/eval_report_index.min.json.reports[")
            and "verdict must match source_report_path" in issue.message
            for issue in issues
        )

    def test_eval_report_index_rejects_receipt_posture(self, tmp_path: Path) -> None:
        make_eval_report_index_surface(tmp_path)
        index_path = tmp_path / "generated" / "eval_report_index.min.json"
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["reports"][0]["receipt_status"] = "published_receipt"
        write_json_payload(index_path, payload)

        issues = validate_eval_report_index(tmp_path)

        assert any(
            issue.location.startswith("generated/eval_report_index.min.json.reports[")
            and "receipt_status must stay 'not_a_receipt'" in issue.message
            for issue in issues
        )

    def test_eval_report_index_reports_builder_system_exit(self) -> None:
        class FailingBuilder:
            def build_eval_report_index_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        issues = validate_eval_report_index(
            REPO_ROOT,
            builder_loader=lambda repo_root: FailingBuilder(),
        )

        assert [(issue.location, issue.message) for issue in issues] == [
            (
                "generated/eval_report_index.min.json",
                "builder-exit",
            )
        ]

    def test_quest_projection_records_validate_full_quest_schema(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        quest_path = quest_fixture_path(tmp_path, "AOA-EV-Q-0001")
        quest = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        quest.pop("title", None)
        write_yaml_payload(quest_path, quest)

        with pytest.raises(ValueError, match=r"violates .*quest\.schema\.json"):
            questbook_projection_records_validator.build_quest_catalog_projection(tmp_path)

    def test_questbook_validation_ignores_missing_agents_checkout_for_orchestrator_refs(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        make_questbook_surface(tmp_path)
        monkeypatch.setattr(
            questbook_context_validator,
            "AOA_AGENTS_ROOT",
            tmp_path / "missing-aoa-agents",
        )

        issues = validate_questbook_surface(tmp_path)

        assert not any("orchestrator class catalog" in issue.message for issue in issues)

    def test_questbook_validation_rejects_unexpected_catalog_ids(self, tmp_path: Path) -> None:
        make_questbook_surface(tmp_path)
        rewrite_questbook_projections(tmp_path)
        catalog_path = tmp_path / "generated" / "quest_catalog.min.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog.append(
            {
                **catalog[0],
                "id": "AOA-EV-Q-9999",
                "source_path": "quests/AOA-EV-Q-9999.yaml",
            }
        )
        write_json_payload(catalog_path, catalog)

        issues = validate_questbook_surface(tmp_path)

        assert any("unexpected quest id" in issue.message for issue in issues)
