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

import eval_catalog_contract
import eval_capsule_contract
import eval_comparison_spine_contract
import eval_section_contract
import validate_repo
from validators import (
    eval_bundle_common,
    questbook_projection_records as questbook_projection_records_validator,
    questbook_route_paths as questbook_route_paths_validator,
    root_context,
    runtime_evidence_selection as runtime_evidence_selection_validator,
)
from validators.source_eval_collection import collect_catalog_records
NO_ADDITIONAL_STARTER_BUNDLES_TEXT = (
    eval_bundle_common.NO_ADDITIONAL_STARTER_BUNDLES_TEXT
)

build_catalog_payloads = eval_catalog_contract.build_catalog_payloads
build_capsule_payload = eval_capsule_contract.build_capsule_payload
build_comparison_spine_payload = eval_comparison_spine_contract.build_comparison_spine_payload


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


def make_receipt_intake_dry_review_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
        "docs/decisions/AOA-EV-D-0024-receipt-intake-dry-review.md",
        "docs/decisions/README.md",
        "mechanics/proof-loop/README.md",
        "mechanics/publication-receipts/README.md",
        "reports/README.md",
        "README.md",
        "docs/README.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "generated/eval_report_index.min.json",
        "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
        "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json",
        "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
        ".aoa/live_receipts/eval-result-receipts.jsonl",
        "evals/workflow/aoa-verification-honesty/EVAL.md",
        "evals/workflow/aoa-verification-honesty/eval.yaml",
        "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_release_support_readiness_audit_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
        "docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md",
        "docs/decisions/README.md",
        "mechanics/release-support/README.md",
        "mechanics/release-support/AGENTS.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "docs/operations/RELEASING.md",
        "reports/README.md",
        "README.md",
        "docs/README.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "QUESTBOOK.md",
        "quests/README.md",
        "quests/LIFECYCLE.md",
        "generated/quest_catalog.min.json",
        "generated/quest_dispatch.min.json",
        "docs/architecture/PROOF_TOPOLOGY.md",
        "docs/architecture/LEGACY_NAMING.md",
        "mechanics/README.md",
        "mechanics/proof-object/README.md",
        "mechanics/proof-loop/README.md",
        "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
        "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
        "generated/eval_report_index.min.json",
        "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
        "generated/eval_catalog.min.json",
        "generated/eval_capsules.json",
        "generated/eval_sections.full.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
        "scripts/release_check.py",
        "scripts/validate_repo.py",
        "tests/test_validate_repo.py",
        "tests/test_downstream_feed_contracts.py",
        "mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py",
        "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
        "mechanics/boundary-bridge/README.md",
        "mechanics/boundary-bridge/AGENTS.md",
        "mechanics/boundary-bridge/PARTS.md",
        "mechanics/boundary-bridge/parts/README.md",
        "mechanics/boundary-bridge/parts/compatibility-map/README.md",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_strategic_closeout_audit_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json",
        "docs/decisions/AOA-EV-D-0026-strategic-closeout-audit.md",
        "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
        "docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "mechanics/release-support/parts/strategic-closeout/README.md",
        "README.md",
        "docs/README.md",
        "reports/README.md",
        "docs/operations/RELEASING.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/PROOF_TOPOLOGY.md",
        "docs/architecture/LEGACY_NAMING.md",
        "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
        "QUESTBOOK.md",
        "quests/README.md",
        "quests/LIFECYCLE.md",
        "generated/quest_catalog.min.json",
        "generated/quest_dispatch.min.json",
        "mechanics/README.md",
        "mechanics/proof-object/README.md",
        "mechanics/proof-loop/README.md",
        "mechanics/release-support/README.md",
        "mechanics/audit/README.md",
        "mechanics/boundary-bridge/README.md",
        "mechanics/boundary-bridge/AGENTS.md",
        "mechanics/boundary-bridge/PARTS.md",
        "mechanics/boundary-bridge/parts/README.md",
        "mechanics/boundary-bridge/parts/compatibility-map/README.md",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md",
        ".agents/AGENTS.md",
        ".agents/spark/AGENTS.md",
        ".agents/spark/SWARM.md",
        "scripts/validate_repo.py",
        "scripts/release_check.py",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json",
        "tests/test_validate_repo.py",
        "mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py",
        "mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py",
        "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
        "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
        "generated/eval_report_index.min.json",
        "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
        "generated/eval_catalog.min.json",
        "generated/eval_capsules.json",
        "generated/eval_sections.full.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_release_prep_pr_handoff_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json",
        "docs/decisions/AOA-EV-D-0027-release-prep-pr-handoff.md",
        "docs/decisions/AOA-EV-D-0028-repo-validation-aoa-memo-pin-refresh.md",
        "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
        "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json",
        "docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md",
        "docs/decisions/AOA-EV-D-0026-strategic-closeout-audit.md",
        "docs/decisions/README.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "mechanics/release-support/parts/strategic-closeout/README.md",
        "mechanics/release-support/parts/pr-handoff/README.md",
        "README.md",
        "docs/README.md",
        "reports/README.md",
        "docs/operations/RELEASING.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/architecture/PROOF_TOPOLOGY.md",
        "docs/architecture/LEGACY_NAMING.md",
        "QUESTBOOK.md",
        "quests/README.md",
        "quests/LIFECYCLE.md",
        "generated/quest_catalog.min.json",
        "generated/quest_dispatch.min.json",
        "mechanics/README.md",
        "mechanics/proof-object/README.md",
        "mechanics/proof-loop/README.md",
        "mechanics/release-support/README.md",
        "mechanics/release-support/AGENTS.md",
        "mechanics/audit/README.md",
        "mechanics/boundary-bridge/README.md",
        "mechanics/boundary-bridge/AGENTS.md",
        "mechanics/boundary-bridge/PARTS.md",
        "mechanics/boundary-bridge/parts/README.md",
        "mechanics/boundary-bridge/parts/compatibility-map/README.md",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md",
        ".agents/AGENTS.md",
        ".agents/spark/AGENTS.md",
        ".agents/spark/SWARM.md",
        "scripts/validate_repo.py",
        "scripts/release_check.py",
        "scripts/validate_nested_agents.py",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json",
        "tests/test_validate_repo.py",
        "mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py",
        "mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py",
        "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
        "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
        "generated/eval_report_index.min.json",
        "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
        "generated/eval_catalog.min.json",
        "generated/eval_capsules.json",
        "generated/eval_sections.full.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
    ]:
        copy_repo_text(repo_root, relative_path)


def make_phase_alpha_eval_matrix_surface(repo_root: Path) -> None:
    for relative_path in [
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/schemas/phase-alpha-eval-matrix.schema.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/examples/phase_alpha_eval_matrix.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json",
        "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json",
        "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json",
        "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
        "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
        "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py",
    ]:
        copy_repo_text(repo_root, relative_path)


def phase_alpha_playbooks_root_or_skip() -> Path:
    candidates = [
        root_context.AOA_PLAYBOOKS_ROOT,
        REPO_ROOT.parent / "aoa-playbooks",
        Path("/srv/AbyssOS/aoa-playbooks"),
    ]
    for candidate in candidates:
        if (candidate / "generated" / "phase_alpha_run_matrix.min.json").is_file():
            return candidate
    pytest.skip("aoa-playbooks phase alpha matrix is unavailable")


def write_yaml_payload(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json_payload(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_integrity_example_report(path: Path) -> None:
    write_text(
        path,
        """
        # Example Report

        ## Per-target breakdown

        | target bundle | integrity risk class |
        |---|---|
        | `aoa-regression-same-task` | fixed-baseline drift |
        | `aoa-output-vs-process-gap` | baseline by association |
        | `aoa-longitudinal-growth-snapshot` | longitudinal overclaim |

        ## Taxonomy reference

        - `style-over-substance`
        - `artifact/process collapse`
        - `baseline by association`
        - `growth by association`
        - `peer-compare blur`
        - `fixed-baseline drift`
        - `longitudinal overclaim`
        - `schema-clean but claim-overstated`
        - `routing overreach`
        """,
    )


def ensure_support_bundle(repo_root: Path, name: str, *, category: str = "workflow") -> None:
    bundle_dir = eval_dir_for_test(repo_root, name, category=category)
    if bundle_dir.exists():
        return

    write_text(
        bundle_dir / "EVAL.md",
        f"""
        ---
        name: {name}
        category: {category}
        status: draft
        summary: Minimal support bundle for validation.
        object_under_evaluation: bounded support surface
        claim_type: bounded
        baseline_mode: none
        report_format: summary
        technique_dependencies: []
        skill_dependencies: []
        ---

        # {name}

        ## Intent
        Minimal support intent.

        ## Object under evaluation
        Minimal support object.

        ## Bounded claim
        This eval is designed to support a claim like:

        under these conditions, the bounded support claim holds on this surface.

        This eval does not support claims such as:
        - broad general strength
        - total safety

        ## Trigger boundary
        Use this eval when:
        - bounded review matters
        - the support surface is the real question

        Do not use this eval when:
        - the task is unbounded
        - the main question is something else

        ## Inputs
        - input

        ## Fixtures and case surface
        - fixture

        ## Scoring or verdict logic
        - logic

        ## Baseline or comparison mode
        - none

        ## Execution contract
        - contract

        ## Outputs
        - output

        ## Failure modes
        - failure

        ## Blind spots
        This eval does not prove:
        - broad general strength
        - stable behavior across time
        - downstream artifact excellence

        ## Interpretation guidance
        Treat a positive result as support for one bounded claim:
        the bounded support claim holds on this surface.

        Do not treat a positive result as:
        - proof of general capability
        - proof of total safety
        - proof that every nearby surface is strong

        ## Verification
        - verify

        ## Technique traceability
        - none

        ## Skill traceability
        - none

        ## Adaptation points
        - point
        """,
    )
    write_text(
        bundle_dir / "eval.yaml",
        yaml.safe_dump(
            {
                "name": name,
                "category": category,
                "status": "draft",
                "object_under_evaluation": "bounded support surface",
                "claim_type": "bounded",
                "baseline_mode": "none",
                "verdict_shape": "categorical",
                "report_format": "summary",
                "maturity_score": 1,
                "rigor_level": "bounded",
                "repeatability": "moderate",
                "portability_level": "local-shaped",
                "review_required": True,
                "validation_strength": "baseline",
                "export_ready": True,
                "blind_spot_disclosure": "required-and-present",
                "score_interpretation_bound": "explicit",
                "technique_dependencies": [],
                "skill_dependencies": [],
                "relations": [],
                "evidence": [
                    {"kind": "origin_need", "path": "notes/origin-need.md"},
                    {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
                ],
            },
            sort_keys=False,
        ),
    )
    write_text(bundle_dir / "notes" / "origin-need.md", "# Origin Need\n")
    write_text(bundle_dir / "examples" / "example-report.md", "# Example Report\n")
    write_text(bundle_dir / "checks" / "eval-integrity-check.md", "# Eval Integrity Check\n")


def build_default_comparison_surface(
    repo_root: Path,
    *,
    bundle_name: str,
    baseline_mode: str,
) -> dict[str, object] | None:
    if baseline_mode == "none":
        return None

    ensure_support_bundle(repo_root, "aoa-eval-integrity-check", category="capability")

    if baseline_mode in {"fixed-baseline", "previous-version"}:
        ensure_support_bundle(repo_root, "aoa-anchor-surface")
        write_text(
            repo_root
            / "mechanics"
            / "comparison-spine"
            / "parts"
            / "fixed-baseline"
            / "fixtures"
            / "frozen-same-task-v1"
            / "README.md",
            "# Shared Fixture Family\n",
        )
        write_text(repo_root / "reports" / "same-task-baseline-proof-flow-v1.md", "# Paired Proof\n")
        return {
            "shared_family_path": "mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md",
            "paired_readout_path": "mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md",
            "integrity_sidecar": "aoa-eval-integrity-check",
            "selection_question": "Do you need a frozen-baseline comparison on the same bounded task family?",
            "anchor_surface": "aoa-anchor-surface",
            "baseline_target_label": "RS-v1 frozen bounded workflow reference",
        }

    if baseline_mode == "peer-compare":
        ensure_support_bundle(repo_root, "aoa-peer-left")
        ensure_support_bundle(repo_root, "aoa-peer-right")
        write_text(
            repo_root
            / "mechanics"
            / "comparison-spine"
            / "parts"
            / "peer-compare"
            / "fixtures"
            / "bounded-change-paired-v1"
            / "README.md",
            "# Shared Fixture Family\n",
        )
        write_text(repo_root / "reports" / "artifact-process-paired-proof-flow-v1.md", "# Paired Proof\n")
        write_text(
            repo_root
            / "mechanics"
            / "comparison-spine"
            / "parts"
            / "peer-compare"
            / "fixtures"
            / "bounded-change-paired-v2"
            / "README.md",
            "# Shared Fixture Family\n",
        )
        write_text(repo_root / "reports" / "artifact-process-paired-proof-flow-v2.md", "# Paired Proof\n")
        return {
            "shared_family_path": "mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md",
            "paired_readout_path": "mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md",
            "integrity_sidecar": "aoa-eval-integrity-check",
            "selection_question": "Do you need a side-by-side peer compare between artifact quality and workflow discipline on the same bounded cases?",
            "peer_surfaces": ["aoa-peer-left", "aoa-peer-right"],
            "matched_surface": "same bounded case family under matched peer conditions",
        }

    ensure_support_bundle(repo_root, "aoa-anchor-surface")
    write_text(
        repo_root
        / "mechanics"
        / "comparison-spine"
        / "parts"
        / "longitudinal-window"
        / "fixtures"
        / "repeated-window-bounded-v1"
        / "README.md",
        "# Shared Fixture Family\n",
    )
    write_text(repo_root / "reports" / "repeated-window-proof-flow-v1.md", "# Paired Proof\n")
    write_text(repo_root / "reports" / "repeated-window-proof-flow-v2.md", "# Paired Proof\n")
    return {
        "shared_family_path": "mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md",
        "paired_readout_path": "mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md",
        "integrity_sidecar": "aoa-eval-integrity-check",
        "selection_question": "Do you need ordered repeated-window movement on one named bounded workflow surface?",
        "anchor_surface": "aoa-anchor-surface",
        "window_family_label": "repeated-window-bounded-v1 validation family",
    }


def make_repo_docs(
    repo_root: Path,
    *,
    starter_names: list[str],
    comparison_entries: list[tuple[str, str]] | None = None,
) -> None:
    comparison_entries = comparison_entries or []
    comparison_lines = "\n".join(f"- `{name}`" for _question, name in comparison_entries)
    comparison_questions = "\n".join(
        f"### {question}\n- `{name}`"
        for question, name in comparison_entries
    )
    if not comparison_questions:
        comparison_questions = "### Do you need a frozen-baseline comparison on the same bounded task family?\n- `aoa-regression-same-task`"
    doctrine_names = starter_names + [name for _question, name in comparison_entries] + ["aoa-eval-integrity-check"]
    doctrine_block = "\n".join(f"- `{name}`" for name in sorted(set(doctrine_names)))

    write_text(
        repo_root / "README.md",
        """
        # aoa-evals

        See `docs/guides/COMPARISON_SPINE_GUIDE.md` when you need the comparison ladder.
        See `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` when you need the artifact/process layer.
        See `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` when you need repeated-window discipline.
        See `docs/guides/SHARED_PROOF_INFRA_GUIDE.md` when you need shared proof infra rules.
        Generated comparison routing lives through the generated reader index.
        """,
    )
    write_text(
        repo_root / "docs" / "README.md",
        """
        # Documentation Map

        - [Comparison Spine Guide](guides/COMPARISON_SPINE_GUIDE.md)
        - [Artifact Process Separation Guide](guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
        - [Repeated Window Discipline Guide](guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
        - [Shared Proof Infra Guide](guides/SHARED_PROOF_INFRA_GUIDE.md)
        - `generated/comparison_spine.json`
        """,
    )
    write_text(
        repo_root / "docs" / "guides" / "COMPARISON_SPINE_GUIDE.md",
        f"""
        # Comparison Spine Guide

        Current comparison doctrine:
        {doctrine_block}
        """,
    )
    write_text(
        repo_root / "docs" / "guides" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        """
        # Artifact Process Separation Guide

        `aoa-artifact-review-rubric`
        `aoa-bounded-change-quality`
        `aoa-output-vs-process-gap`
        `aoa-witness-trace-integrity`
        `aoa-compost-provenance-preservation`
        matched conditions
        style-over-substance
        mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md
        mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md
        """,
    )
    write_text(
        repo_root / "docs" / "guides" / "REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        """
        # Repeated Window Discipline Guide

        aoa-longitudinal-growth-snapshot
        context_note
        transition_note
        after the one-run and baseline reads
        """,
    )
    write_text(
        repo_root / "docs" / "guides" / "SHARED_PROOF_INFRA_GUIDE.md",
        """
        # Shared Proof Infra Guide

        shared_fixture_family_path
        additional_shared_fixture_family_paths
        paired_readout_path
        additional_paired_readout_paths
        """,
    )
    write_text(
        repo_root / "EVAL_SELECTION.md",
        f"""
        # Eval Bundle Selection Chooser

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        {"".join(f"- `{name}`\n" for name in starter_names)}

        The artifact/process bridge is read only after the standalone artifact and workflow surfaces are already visible.
        For repeated-window reading, `context_note` is the comparability disclosure and `transition_note` explains movement.

        ## Pick Comparison Surface

        {comparison_questions}
        """,
    )


def make_index(
    repo_root: Path,
    name: str,
    category: str,
    *,
    include_comparison_spine: bool = False,
) -> None:
    comparison_spine_block = ""
    if include_comparison_spine:
        comparison_spine_block = """

        ## Comparison Spine

        The comparison spine is a bounded program layer.
        """
    artifact_process_block = """

        ## Artifact Process Layer

        The artifact/process layer is a bounded program layer.
        `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`
        """
    write_text(
        repo_root / "EVAL_INDEX.md",
        f"""
        # EVAL_INDEX

        ## Starter eval bundles

        | name | category | status | summary |
        |---|---|---|---|
        | {name} | {category} | draft | Minimal summary for validation. |

        ## Planned starter bundles

        {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}
        {comparison_spine_block}
        {artifact_process_block}
        """,
    )


def make_selection(
    repo_root: Path,
    names: list[str],
    comparison_entries: list[tuple[str, str]] | None = None,
) -> None:
    lines = "\n".join(f"- `{name}`" for name in names)
    comparison_entries = comparison_entries or []
    comparison_block = ""
    if comparison_entries:
        comparison_block = "\n## Pick Comparison Surface\n\n" + "\n".join(
            f"### {question}\n- `{name}`"
            for question, name in comparison_entries
        )
    write_text(
        repo_root / "EVAL_SELECTION.md",
        f"""
        # Eval Bundle Selection Chooser

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        {lines}
        The artifact/process bridge is read only after the standalone artifact and workflow surfaces are already visible.
        `context_note` is the comparability disclosure and `transition_note` explains repeated-window movement.
        {comparison_block}
        """,
    )


def make_roadmap(
    repo_root: Path,
    current_public_surface_names: list[str] | None = None,
    *,
    include_absence_note: bool = True,
) -> None:
    current_public_surface_names = current_public_surface_names or []
    current_surface_block = ""
    if current_public_surface_names:
        surface_lines = "\n".join(
            f"- `{name}` as the current public surface for validation."
            for name in current_public_surface_names
        )
        current_surface_block = f"\nCurrent public surface:\n{surface_lines}\n"

    next_candidate_line = (
        f"- {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}"
        if include_absence_note
        else "- placeholder next candidate"
    )

    write_text(
        repo_root / "ROADMAP.md",
        f"""
        # Proof Direction Roadmap

        ## Role

        `ROADMAP.md` is the active direction surface for `aoa-evals`.

        The roadmap owns direction and sequencing.

        Use the stronger owner surface when the work needs detail:

        - release history: [CHANGELOG.md](CHANGELOG.md)

        ## Update Rule

        Update this roadmap when a change moves repo-level proof direction.

        Before closeout, ask whether the change moved proof-organ direction or
        only landed a local surface.

        ## Current Direction

        Highest-priority additions:
        - placeholder
        - keep the agent index chain visible while `docs/architecture/AGENT_INDEX.md` remains the
          index
        - grow the active proof loop while bundle-local review keeps bounded claim
          strength

        ## Direction Anchors

        These anchors keep direction recoverable; changelog and validator ledgers carry
        history/token detail.

        | Anchor | Owner surface | Directional use |
        | --- | --- | --- |
        | Agent index chain | `docs/architecture/AGENT_INDEX.md` | Keep the pass-through route visible. |
        | Route residue guard family | `scripts/validate_repo.py`, route cards, and `docs/decisions/` | Keep generated/readout, active mechanic, root-authored, decision, repo-config, source-bundle, and mechanic-payload residue guards routed to their owner contracts. |
        | Legacy naming | `docs/architecture/LEGACY_NAMING.md` | Keep active names and legacy bridge posture visible. |
        | Mechanics evidence | `mechanics/EVIDENCE_CLUSTERS.md` | Keep parent evidence, root district posture, and residual root-authored surface classification outside roadmap body detail. |
        | Mechanic lower index | `mechanics/README.md`, parent `DIRECTION.md`, parent `PARTS.md`, part `README.md`, part `VALIDATION.md`, and parent `parts/AGENTS.md` | Keep part/payload source surfaces, parts index synchronization, and payload coverage recoverable. |
        | Legacy bridge | parent `PROVENANCE.md` and `legacy/` | Keep single controlled bridge posture, active mechanic surfaces, and runtime evidence limits behind the active route. |

        ## Horizons

        Next likely cross-surface candidate after the current public starter set:
        {next_candidate_line}
        {current_surface_block}
        """,
    )


def make_eval_bundle(
    repo_root: Path,
    *,
    name: str,
    category: str = "workflow",
    status: str = "draft",
    claim_type: str = "bounded",
    baseline_mode: str = "none",
    verdict_shape: str = "categorical",
    report_format: str = "summary",
    portability_level: str | None = None,
    technique_dependencies: list[dict[str, str]] | None = None,
    skill_dependencies: list[dict[str, str]] | None = None,
    relations: list[dict[str, str]] | None = None,
    evidence_entries: list[dict[str, str]] | None = None,
    support_files: dict[str, str] | None = None,
    section_overrides: dict[str, str] | None = None,
    comparison_surface: dict[str, object] | None = None,
    public_safety_reviewed_at: str | None = None,
) -> None:
    bundle_dir = eval_dir_for_test(
        repo_root,
        name,
        category=category,
        baseline_mode=baseline_mode,
    )
    support_files = dict(support_files or {
        "notes/origin-need.md": "# Origin Need\n",
        "examples/example-report.md": "# Example Report\n",
        "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
    })
    technique_dependencies = technique_dependencies or [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md",
        }
    ]
    skill_dependencies = skill_dependencies or [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/core/engineering/aoa-change-protocol/SKILL.md",
        }
    ]
    relations = relations or []
    if comparison_surface is None:
        comparison_surface = build_default_comparison_surface(
            repo_root,
            bundle_name=name,
            baseline_mode=baseline_mode,
        )
    if evidence_entries is None:
        evidence_entries = [
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ]
        if status == "bounded":
            evidence_entries.append(
                {"kind": "support_note", "path": "notes/bounded-promotion-review.md"}
            )
            support_files.setdefault(
                "notes/bounded-promotion-review.md",
                textwrap.dedent(
                    """\
                    # Bounded Review

                    approve for bounded promotion
                    readout distinctions stay explicit
                    failure signals stay visible
                    """
                ),
            )
        if status in {"portable", "baseline", "canonical"}:
            evidence_entries.append(
                {"kind": "portable_review", "path": "notes/portable-review.md"}
            )
            support_files.setdefault("notes/portable-review.md", "# Portable Review\n")
        if status == "canonical":
            evidence_entries.append(
                {"kind": "canonical_readiness", "path": "notes/canonical-readiness.md"}
            )
            support_files.setdefault(
                "notes/canonical-readiness.md",
                "# Canonical Readiness\n",
            )
        if baseline_mode != "none":
            evidence_entries.append(
                {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"}
            )
            support_files.setdefault(
                "notes/baseline-readiness.md",
                "# Baseline Readiness\n",
            )
        if report_format == "comparative-summary":
            if baseline_mode == "longitudinal-window":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/window-contract.md"}
                )
                support_files.setdefault(
                    "notes/window-contract.md",
                    textwrap.dedent(
                        """\
                        # Window Contract

                        ordered window sequence
                        anchor workflow surface
                        no clear directional movement
                        """
                    ),
                )
            elif baseline_mode == "peer-compare":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        matched conditions
                        side-by-side interpretation
                        """
                    ),
                )
            else:
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        baseline target
                        noisy variation
                        style-only overread
                        """
                    ),
                )
    frontmatter = {
        "name": name,
        "category": category,
        "status": status,
        "summary": "Minimal summary for validation.",
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "report_format": report_format,
        "technique_dependencies": [entry["id"] for entry in technique_dependencies],
        "skill_dependencies": [entry["name"] for entry in skill_dependencies],
    }
    if comparison_surface is not None:
        frontmatter["comparison_surface"] = comparison_surface
    section_bodies = {
        "Intent": "Minimal intent.",
        "Object under evaluation": "Minimal object.",
        "Bounded claim": textwrap.dedent(
            """\
            This eval is designed to support a claim like:

            under these conditions, the bounded claim holds on this surface.

            This eval does not support claims such as:
            - broad general strength
            - total safety
            """
        ).strip(),
        "Trigger boundary": textwrap.dedent(
            """\
            Use this eval when:
            - bounded review matters
            - the workflow claim is the real question

            Do not use this eval when:
            - the task is unbounded
            - the main question is something else
            """
        ).strip(),
        "Inputs": "- input",
        "Fixtures and case surface": "- fixture",
        "Scoring or verdict logic": "- logic",
        "Baseline or comparison mode": "- mode",
        "Execution contract": "- contract",
        "Outputs": "- output",
        "Failure modes": "- failure",
        "Blind spots": textwrap.dedent(
            """\
            This eval does not prove:
            - broad general strength
            - stable behavior across time
            - downstream artifact excellence
            """
        ).strip(),
        "Interpretation guidance": textwrap.dedent(
            """\
            Treat a positive result as support for one bounded claim:
            the bounded claim holds on this surface.

            Do not treat a positive result as:
            - proof of general capability
            - proof of total safety
            - proof that every nearby surface is strong
            """
        ).strip(),
        "Verification": "- verify",
        "Technique traceability": "- " + (technique_dependencies[0]["id"] if technique_dependencies else "none"),
        "Skill traceability": "- " + (skill_dependencies[0]["name"] if skill_dependencies else "none"),
        "Adaptation points": "- point",
    }
    if section_overrides:
        section_bodies.update(section_overrides)

    default_portability_by_status = {
        "draft": "local-shaped",
        "bounded": "local-shaped",
        "portable": "portable",
        "baseline": "portable",
        "canonical": "broad",
    }
    if portability_level is None:
        portability_level = default_portability_by_status.get(status, "local-shaped")

    body_sections = [f"# {name}"]
    for heading in (
        "Intent",
        "Object under evaluation",
        "Bounded claim",
        "Trigger boundary",
        "Inputs",
        "Fixtures and case surface",
        "Scoring or verdict logic",
        "Baseline or comparison mode",
        "Execution contract",
        "Outputs",
        "Failure modes",
        "Blind spots",
        "Interpretation guidance",
        "Verification",
        "Technique traceability",
        "Skill traceability",
        "Adaptation points",
    ):
        body_sections.append(f"## {heading}\n{section_bodies[heading]}")
    body = "\n\n".join(body_sections) + "\n"
    write_text(
        bundle_dir / "EVAL.md",
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n"
        + body,
    )

    manifest = {
        "name": name,
        "category": category,
        "status": status,
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "verdict_shape": verdict_shape,
        "report_format": report_format,
        "maturity_score": 2,
        "rigor_level": "bounded",
        "repeatability": "moderate",
        "portability_level": portability_level,
        "review_required": True,
        "validation_strength": "baseline",
        "export_ready": True,
        "blind_spot_disclosure": "required-and-present",
        "score_interpretation_bound": "explicit",
        "technique_dependencies": technique_dependencies,
        "skill_dependencies": skill_dependencies,
        "comparison_surface": comparison_surface,
        "relations": relations,
        "evidence": evidence_entries,
    }
    if public_safety_reviewed_at is not None:
        manifest["public_safety_reviewed_at"] = public_safety_reviewed_at
    write_text(bundle_dir / "eval.yaml", yaml.safe_dump(manifest, sort_keys=False))

    for relative_path, content in support_files.items():
        write_text(bundle_dir / relative_path, content)

    comparison_entries = []
    if isinstance(comparison_surface, dict):
        raw_question = comparison_surface.get("selection_question")
        if isinstance(raw_question, str):
            comparison_entries.append((raw_question, name))

    make_index(
        repo_root,
        name,
        category,
        include_comparison_spine=baseline_mode != "none",
    )
    make_selection(repo_root, [name], comparison_entries=comparison_entries)
    make_roadmap(repo_root, [name])
    make_repo_docs(repo_root, starter_names=[name], comparison_entries=comparison_entries)


def write_catalogs(repo_root: Path) -> None:
    if not (repo_root / "QUESTBOOK.md").is_file():
        make_questbook_surface(repo_root)
    issues, records = collect_catalog_records(repo_root)
    if issues:
        return
    full_catalog, min_catalog = build_catalog_payloads(repo_root, records)
    capsules = build_capsule_payload(repo_root, records, full_catalog)
    comparison_spine = build_comparison_spine_payload(repo_root, records, full_catalog)
    sections, section_issues = eval_section_contract.build_sections_payload(repo_root, records)
    if section_issues:
        return
    eval_catalog_contract.write_json_file(repo_root / "generated" / "eval_catalog.json", full_catalog, compact=False)
    eval_catalog_contract.write_json_file(repo_root / "generated" / "eval_catalog.min.json", min_catalog, compact=True)
    eval_catalog_contract.write_json_file(repo_root / "generated" / "eval_capsules.json", capsules, compact=False)
    eval_catalog_contract.write_json_file(repo_root / "generated" / "comparison_spine.json", comparison_spine, compact=False)
    eval_catalog_contract.write_json_file(repo_root / "generated" / "eval_sections.full.json", sections, compact=False)


def make_abyss_stack_schema(tmp_path: Path, schema_name: str) -> Path:
    schema_roots = {
        "runtime-return-event.schema.json": (
            "mechanics",
            "governed-execution",
            "parts",
            "return-policy",
            "schemas",
        ),
        "runtime-memo-export-candidate.schema.json": (
            "mechanics",
            "governed-execution",
            "parts",
            "candidate-exports",
            "schemas",
        ),
        "runtime-benchmark.schema.json": (
            "mechanics",
            "inference-pilots",
            "parts",
            "local-trials",
            "schemas",
        ),
        "service-degradation-receipt.schema.json": (
            "mechanics",
            "runtime-repair",
            "parts",
            "degradation-receipts",
            "schemas",
        ),
    }
    schema_path = tmp_path / "abyss-stack" / Path(*schema_roots.get(schema_name, ("schemas",))) / schema_name
    write_text(
        schema_path,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "title": "test schema",
          "type": "object"
        }
        """,
    )
    return schema_path


def write_runtime_evidence_selection_example(
    repo_root: Path,
    *,
    filename: str,
    source_schema_ref: str,
    candidate_eval_refs: list[str],
) -> None:
    write_text(
        repo_root / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "$id": "https://aoa-evals/mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json",
          "title": "aoa-evals runtime evidence selection",
          "type": "object",
          "additionalProperties": false,
          "required": [
            "surface_type",
            "selection_id",
            "source_repo",
            "source_schema_ref",
            "source_manifests",
            "bounded_claim",
            "promotion_target",
            "comparison_mode",
            "selected_evidence",
            "environment_invariants",
            "do_not_overread",
            "review_posture"
          ],
          "properties": {
            "surface_type": {"const": "runtime_evidence_selection"},
            "selection_id": {"type": "string"},
            "source_repo": {"const": "abyss-stack"},
            "source_schema_ref": {"type": "string"},
            "source_manifests": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "bounded_claim": {"type": "string", "minLength": 1},
            "promotion_target": {"type": "string", "enum": ["local-only", "evidence-sidecar", "bundle-candidate"]},
            "comparison_mode": {"type": "string", "enum": ["none", "fixed-baseline", "peer-compare", "longitudinal-window"]},
            "candidate_eval_refs": {"type": "array", "items": {"type": "string"}},
            "selected_evidence": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["artifact_ref", "evidence_role", "summary_only"],
                "properties": {
                  "artifact_ref": {"type": "string"},
                  "evidence_role": {"type": "string"},
                  "summary_only": {"type": "boolean"}
                }
              }
            },
            "environment_invariants": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "environment_deltas": {"type": "array", "items": {"type": "string"}},
            "excluded_artifacts": {"type": "array", "items": {"type": "string"}},
            "do_not_overread": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "review_posture": {
              "type": "object",
              "additionalProperties": false,
              "required": ["portable_enough", "comparison_hygiene_named", "human_review_required"],
              "properties": {
                "portable_enough": {"type": "boolean"},
                "comparison_hygiene_named": {"type": "boolean"},
                "human_review_required": {"type": "boolean"}
              }
            }
          }
        }
        """,
    )
    write_text(
        repo_root / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR / filename,
        json.dumps(
            {
                "surface_type": "runtime_evidence_selection",
                "selection_id": "return-anchor-integrity-wrapper-v1",
                "source_repo": "abyss-stack",
                "source_schema_ref": source_schema_ref,
                "source_manifests": [
                    "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/return.manifest.json"
                ],
                "bounded_claim": "Bounded return-aware runtime evidence can support anchor-fidelity reading without becoming a final-quality claim.",
                "promotion_target": "evidence-sidecar",
                "comparison_mode": "none",
                "candidate_eval_refs": candidate_eval_refs,
                "selected_evidence": [
                    {
                        "artifact_ref": "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/return-event.summary.json",
                        "evidence_role": "summary",
                        "summary_only": True,
                    },
                    {
                        "artifact_ref": "repo:abyss-stack/Logs/agent-api/notes/return-integrity-sidecar-v1.md",
                        "evidence_role": "integrity-sidecar",
                        "summary_only": True,
                    },
                ],
                "environment_invariants": [
                    "same wrapper policy family",
                    "same return-aware route family",
                ],
                "environment_deltas": [
                    "route family varies across cases while return policy remains unchanged"
                ],
                "excluded_artifacts": [
                    "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/raw/full-transcript.jsonl"
                ],
                "do_not_overread": [
                    "does not prove final answer quality"
                ],
                "review_posture": {
                    "portable_enough": False,
                    "comparison_hygiene_named": True,
                    "human_review_required": True,
                },
            },
            indent=2,
        )
        + "\n",
    )


def add_materialized_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    report_schema: dict[str, object],
    report_example: dict[str, object],
    comparison_mode: str | None = None,
    include_fixture_contract: bool = True,
    include_paired_readout: bool = False,
    include_runner_contract: bool = True,
    fixture_family_path: str = "fixtures/shared-bounded-family/README.md",
    shared_case_surface: str = "shared bounded case family for validation",
    bounded_replacement_rule: str = "replace only with the same bounded case class and public-safe evidence surface",
    public_safe_requirements: list[str] | None = None,
    runner_inputs: list[str] | None = None,
    paired_readout_path: str = "reports/paired-proof.md",
    additional_fixture_family_paths: list[str] | None = None,
    additional_paired_readout_paths: list[str] | None = None,
) -> None:
    bundle_dir = eval_dir_for_test(repo_root, bundle_name)
    bundle_rel = bundle_dir.relative_to(repo_root).as_posix()
    write_text(
        repo_root
        / "mechanics"
        / "proof-infra"
        / "parts"
        / "reportable-contracts"
        / "runners"
        / "reportable_proof_contract.md",
        "# Runner Contract\n",
    )
    write_text(
        repo_root
        / "mechanics"
        / "proof-infra"
        / "parts"
        / "reportable-contracts"
        / "scorers"
        / "bounded_rubric_breakdown.py",
        "def helper():\n    return {'ok': True}\n",
    )
    if include_paired_readout:
        write_text(repo_root / Path(paired_readout_path), "# Paired Proof\n")
    for extra_path in additional_paired_readout_paths or []:
        write_text(repo_root / Path(extra_path), "# Paired Proof\n")

    if include_fixture_contract:
        public_safe_requirements = public_safe_requirements or [
            "outside reviewers can inspect the surface",
        ]
        write_text(repo_root / Path(fixture_family_path), "# Shared Fixture Family\n")
        for extra_path in additional_fixture_family_paths or []:
            write_text(repo_root / Path(extra_path), "# Shared Fixture Family\n")
        write_text(
            bundle_dir / "fixtures" / "contract.json",
            json.dumps(
                {
                    "contract_version": 1,
                    "shared_fixture_family_path": fixture_family_path,
                    "additional_shared_fixture_family_paths": additional_fixture_family_paths or [],
                    "shared_case_surface": shared_case_surface,
                    "bounded_replacement_rule": bounded_replacement_rule,
                    "public_safe_requirements": public_safe_requirements,
                },
                indent=2,
            ),
        )

    schema_path = f"{bundle_rel}/reports/summary.schema.json"
    example_path = f"{bundle_rel}/reports/example-report.json"
    if comparison_mode is not None:
        schema_required = list(report_schema.get("required", []))
        if "comparison_mode" not in schema_required:
            insert_at = 3 if len(schema_required) >= 3 else len(schema_required)
            schema_required.insert(insert_at, "comparison_mode")
            report_schema["required"] = schema_required
        schema_properties = dict(report_schema.get("properties", {}))
        schema_properties["comparison_mode"] = {"const": comparison_mode}
        report_schema["properties"] = schema_properties
        report_example["comparison_mode"] = comparison_mode
    write_text(
        bundle_dir / "reports" / "summary.schema.json",
        json.dumps(report_schema, indent=2),
    )
    write_text(
        bundle_dir / "reports" / "example-report.json",
        json.dumps(report_example, indent=2),
    )

    if include_runner_contract:
        runner_contract: dict[str, object] = {
            "contract_version": 1,
            "runner_surface_path": "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
            "inputs": runner_inputs or ["bounded case dossier"],
            "scorer_helper_paths": ["mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py"],
            "report_schema_path": schema_path,
            "report_example_path": example_path,
        }
        if include_fixture_contract:
            runner_contract["fixture_contract_paths"] = [
                f"{bundle_rel}/fixtures/contract.json"
            ]
        if include_paired_readout:
            runner_contract["paired_readout_path"] = paired_readout_path
        if additional_paired_readout_paths:
            runner_contract["additional_paired_readout_paths"] = additional_paired_readout_paths

        write_text(
            bundle_dir / "runners" / "contract.json",
            json.dumps(runner_contract, indent=2),
        )


def add_fixed_baseline_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    status: str = "draft",
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
) -> None:
    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="fixed-baseline",
        include_paired_readout=True,
        fixture_family_path="mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md",
        shared_case_surface="shared frozen same-task case family for validation",
        bounded_replacement_rule="replace only with the same bounded task family, the same named frozen baseline target, and the same visible evidence surface",
        public_safe_requirements=[
            "the frozen baseline target stays visible and inspectable",
            "baseline and candidate stay on the same bounded case family",
        ],
        runner_inputs=[
            "frozen baseline target",
            "candidate run family on the same bounded cases",
            "per-case comparison notes",
        ],
        paired_readout_path="mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "baseline_target",
                "case_family",
                "per_case_comparisons",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": status},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "no material regression",
                        "mixed regression signal",
                        "regression present",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "baseline_target": {"type": "string"},
                "case_family": {"type": "string"},
                "per_case_comparisons": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "case_id",
                            "baseline_note",
                            "candidate_note",
                            "comparative_reading",
                            "comparison_note",
                        ],
                        "properties": {
                            "case_id": {"type": "string"},
                            "baseline_note": {"type": "string"},
                            "candidate_note": {"type": "string"},
                            "comparative_reading": {
                                "type": "string",
                                "enum": [
                                    "no material regression",
                                    "bounded improvement present",
                                    "noisy variation",
                                    "regression present",
                                ],
                            },
                            "comparison_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": bundle_name,
            "bundle_status": status,
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed regression signal",
            "claim_boundary": "bounded same-task regression example for validation",
            "limitations": ["still bounded"],
            "baseline_target": "RS-v1 frozen bounded workflow reference",
            "case_family": "frozen-same-task-v1",
            "per_case_comparisons": [
                {
                    "case_id": "RS-01",
                    "baseline_note": "baseline note",
                    "candidate_note": "candidate note",
                    "comparative_reading": "no material regression",
                    "comparison_note": "comparison note",
                }
            ],
        },
    )


def add_longitudinal_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
    report_example_override: dict[str, object] | None = None,
) -> None:
    report_example = {
        "eval_name": bundle_name,
        "bundle_status": "draft",
        "object_under_evaluation": "bounded test surface",
        "verdict": "mixed or unstable movement",
        "claim_boundary": "bounded repeated-window movement example for validation on one anchored surface",
        "limitations": ["this report does not prove general capability growth beyond this anchored surface"],
        "anchor_surface": "aoa-bounded-change-quality",
        "window_family": "repeated-window-bounded-v1",
        "windows": [
            {
                "window_id": "LG-01",
                "window_order": 1,
                "workflow_note": "workflow note",
                "movement_reading": "no clear directional movement",
                "context_note": "context note",
                "transition_note": "initial transition note",
            },
            {
                "window_id": "LG-02",
                "window_order": 2,
                "workflow_note": "workflow note later",
                "movement_reading": "bounded improvement signal",
                "context_note": "context note later",
                "transition_note": "follow-up transition note",
            },
        ],
    }
    if report_example_override:
        report_example.update(report_example_override)

    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="longitudinal-window",
        include_paired_readout=True,
        fixture_family_path="mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md",
        shared_case_surface="shared repeated-window workflow family for validation",
        bounded_replacement_rule="replace only with the same ordered named windows on one bounded workflow surface and explicit context notes",
        public_safe_requirements=[
            "the anchor workflow surface stays explicit across the window sequence",
            "each window has a public report or summary artifact",
        ],
        runner_inputs=[
            "ordered named windows",
            "one public report or summary artifact per window",
            "context-shift notes as comparability disclosure",
            "transition notes for non-initial windows",
        ],
        paired_readout_path="mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md",
        additional_paired_readout_paths=["mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md"],
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "anchor_surface",
                "window_family",
                "windows",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "bounded improvement signal",
                        "no clear directional movement",
                        "mixed or unstable movement",
                        "bounded regression signal",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "anchor_surface": {"type": "string"},
                "window_family": {"type": "string"},
                "windows": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "window_id",
                            "window_order",
                            "workflow_note",
                            "movement_reading",
                            "context_note",
                            "transition_note",
                        ],
                        "properties": {
                            "window_id": {"type": "string"},
                            "window_order": {"type": "integer", "minimum": 1},
                            "workflow_note": {"type": "string"},
                            "movement_reading": {
                                "type": "string",
                                "enum": [
                                    "bounded improvement signal",
                                    "no clear directional movement",
                                    "mixed or unstable movement",
                                    "bounded regression signal",
                                ],
                            },
                            "context_note": {"type": "string"},
                            "transition_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example=report_example,
    )


def add_peer_compare_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
) -> None:
    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="peer-compare",
        include_paired_readout=True,
        fixture_family_path="mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md",
        shared_case_surface="shared bounded change case family for validation",
        bounded_replacement_rule="replace only with the same bounded case family under matched artifact and workflow review conditions",
        public_safe_requirements=[
            "the shared case family stays explicit",
            "the side-by-side artifact and workflow surfaces stay reviewable",
        ],
        runner_inputs=[
            "shared bounded case family",
            "artifact-side readings",
            "process-side readings",
            "matched-condition evidence",
            "paired divergence summary",
        ],
        paired_readout_path="mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md",
        additional_fixture_family_paths=["mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md"],
        additional_paired_readout_paths=["mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md"],
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "case_family",
                "paired_surfaces",
                "per_case_comparisons",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "artifact outruns process",
                        "process outruns artifact",
                        "artifact and process are broadly aligned",
                        "mixed comparison signal",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "case_family": {"type": "string"},
                "paired_surfaces": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                },
                "per_case_comparisons": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "case_id",
                            "artifact_side_reading",
                            "process_side_reading",
                            "gap_reading",
                            "side_by_side_note",
                        ],
                        "properties": {
                            "case_id": {"type": "string"},
                            "artifact_side_reading": {"type": "string"},
                            "process_side_reading": {"type": "string"},
                            "gap_reading": {"type": "string"},
                            "side_by_side_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": bundle_name,
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed comparison signal",
            "claim_boundary": "bounded peer-compare example for validation",
            "limitations": ["still bounded"],
            "case_family": "bounded-change-paired-v1",
            "paired_surfaces": ["aoa-peer-left", "aoa-peer-right"],
            "per_case_comparisons": [
                {
                    "case_id": "PC-01",
                    "artifact_side_reading": "supports bounded claim",
                    "process_side_reading": "mixed support",
                    "gap_reading": "artifact outruns process",
                    "side_by_side_note": "paired note",
                }
            ],
        },
    )
