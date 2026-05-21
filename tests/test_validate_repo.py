from __future__ import annotations

import json
import textwrap
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog
import eval_section_contract
import validate_repo
from validate_repo import (
    NO_ADDITIONAL_STARTER_BUNDLES_TEXT,
    build_capsule_payload,
    build_catalog_payloads,
    build_comparison_spine_payload,
    collect_catalog_records,
    run_validation,
    validate_questbook_surface,
    validate_eval_index,
    write_json_file,
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
        "docs/QUESTBOOK_EVAL_INTEGRATION.md",
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
        validate_repo.build_quest_catalog_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_catalog.min.example.json",
        validate_repo.build_quest_catalog_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_dispatch.min.json",
        validate_repo.build_quest_dispatch_projection(repo_root),
    )
    write_json_payload(
        repo_root / "generated" / "quest_dispatch.min.example.json",
        validate_repo.build_quest_dispatch_projection(repo_root),
    )


def make_quest_route_surface(repo_root: Path) -> None:
    for relative_path in [
        "quests/README.md",
        "quests/AGENTS.md",
        "quests/LIFECYCLE.md",
        "docs/decisions/0004-questbook-topology.md",
        "docs/decisions/0018-quest-lane-state-source-layout.md",
        "docs/decisions/0021-quest-lifecycle-contract.md",
        validate_repo.AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
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
        "docs/EVAL_REVIEW_GUIDE.md",
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
        "docs/decisions/0024-receipt-intake-dry-review.md",
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
        "docs/decisions/0025-release-support-readiness-audit.md",
        "docs/decisions/README.md",
        "mechanics/release-support/README.md",
        "mechanics/release-support/AGENTS.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "docs/RELEASING.md",
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
        "docs/PROOF_TOPOLOGY.md",
        "docs/LEGACY_NAMING.md",
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
        "docs/decisions/0026-strategic-closeout-audit.md",
        "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
        "docs/decisions/0025-release-support-readiness-audit.md",
        "docs/decisions/README.md",
        "docs/decisions/TEMPLATE.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "mechanics/release-support/parts/strategic-closeout/README.md",
        "README.md",
        "docs/README.md",
        "reports/README.md",
        "docs/RELEASING.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/PROOF_TOPOLOGY.md",
        "docs/LEGACY_NAMING.md",
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
        "docs/decisions/0027-release-prep-pr-handoff.md",
        "docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md",
        "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
        "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json",
        "docs/decisions/0025-release-support-readiness-audit.md",
        "docs/decisions/0026-strategic-closeout-audit.md",
        "docs/decisions/README.md",
        "mechanics/release-support/PARTS.md",
        "mechanics/release-support/parts/README.md",
        "mechanics/release-support/parts/readiness-audit/README.md",
        "mechanics/release-support/parts/strategic-closeout/README.md",
        "mechanics/release-support/parts/pr-handoff/README.md",
        "README.md",
        "docs/README.md",
        "reports/README.md",
        "docs/RELEASING.md",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "DESIGN.AGENTS.md",
        "AGENTS.md",
        "docs/PROOF_TOPOLOGY.md",
        "docs/LEGACY_NAMING.md",
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
        validate_repo.AOA_PLAYBOOKS_ROOT,
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

        See `docs/COMPARISON_SPINE_GUIDE.md` when you need the comparison ladder.
        See `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` when you need the artifact/process layer.
        See `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` when you need repeated-window discipline.
        See `docs/SHARED_PROOF_INFRA_GUIDE.md` when you need shared proof infra rules.
        Generated comparison routing lives in `generated/comparison_spine.json`.
        """,
    )
    write_text(
        repo_root / "docs" / "README.md",
        """
        # Documentation Map

        - [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
        - [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
        - [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
        - [Shared Proof Infra Guide](SHARED_PROOF_INFRA_GUIDE.md)
        - `generated/comparison_spine.json`
        """,
    )
    write_text(
        repo_root / "docs" / "COMPARISON_SPINE_GUIDE.md",
        f"""
        # Comparison Spine Guide

        Current comparison doctrine:
        {doctrine_block}
        """,
    )
    write_text(
        repo_root / "docs" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
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
        repo_root / "docs" / "REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        """
        # Repeated Window Discipline Guide

        aoa-longitudinal-growth-snapshot
        context_note
        transition_note
        after the one-run and baseline reads
        """,
    )
    write_text(
        repo_root / "docs" / "SHARED_PROOF_INFRA_GUIDE.md",
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

        ## Authority

        Direction stays here.

        ## Current Direction

        Highest-priority additions:
        - placeholder

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
    write_json_file(repo_root / "generated" / "eval_catalog.json", full_catalog, compact=False)
    write_json_file(repo_root / "generated" / "eval_catalog.min.json", min_catalog, compact=True)
    write_json_file(repo_root / "generated" / "eval_capsules.json", capsules, compact=False)
    write_json_file(repo_root / "generated" / "comparison_spine.json", comparison_spine, compact=False)
    write_json_file(repo_root / "generated" / "eval_sections.full.json", sections, compact=False)


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
        repo_root / validate_repo.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH,
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
        repo_root / validate_repo.RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR / filename,
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


def test_build_catalog_preserves_same_kind_relations_in_full_catalog(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-alpha",
        relations=[{"type": "complements", "target": "aoa-beta"}],
    )
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha", "aoa-beta"])

    assert build_catalog.main(argv=[], repo_root=tmp_path) == 0

    full_catalog = json.loads((tmp_path / "generated" / "eval_catalog.json").read_text(encoding="utf-8"))
    alpha_entry = next(entry for entry in full_catalog["evals"] if entry["name"] == "aoa-alpha")

    assert alpha_entry["relations"] == [{"type": "complements", "target": "aoa-beta"}]
    assert alpha_entry["technique_refs"][0]["repo"] == "aoa-techniques"
    assert alpha_entry["skill_refs"][0]["repo"] == "aoa-skills"


def test_eval_selection_rejects_generic_heading(tmp_path: Path) -> None:
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        """
        # Eval Selection

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        - `aoa-alpha`
        """,
    )

    issues = validate_repo.validate_eval_selection(tmp_path, ["aoa-alpha"])

    assert any(
        issue.location == "EVAL_SELECTION.md"
        and "# Eval Bundle Selection Chooser" in issue.message
        for issue in issues
    )


def test_build_catalog_records_materialized_proof_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-materialized-proof")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-materialized-proof",
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
            ],
            "properties": {
                "eval_name": {"const": "aoa-materialized-proof"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-materialized-proof",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "bounded machine-readable proof artifact for validation",
            "limitations": ["still bounded"],
        },
        include_paired_readout=True,
    )

    assert build_catalog.main(argv=[], repo_root=tmp_path) == 0

    full_catalog = json.loads((tmp_path / "generated" / "eval_catalog.json").read_text(encoding="utf-8"))
    entry = next(item for item in full_catalog["evals"] if item["name"] == "aoa-materialized-proof")

    assert entry["proof_artifacts"]["shared_fixture_family_path"] == "fixtures/shared-bounded-family/README.md"
    assert entry["proof_artifacts"]["runner_surface_path"] == "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md"
    assert entry["proof_artifacts"]["report_schema_path"] == "evals/workflow/aoa-materialized-proof/reports/summary.schema.json"


def test_validate_repo_rejects_missing_evidence_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-evidence-path",
        evidence_entries=[{"kind": "origin_need", "path": "notes/missing.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("evidence path 'notes/missing.md' does not exist" in issue.message for issue in issues)


def test_validate_repo_requires_origin_need_for_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-origin-need",
        evidence_entries=[{"kind": "integrity_check", "path": "checks/eval-integrity-check.md"}],
        support_files={
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("starter bundle must include an evidence entry with kind 'origin_need'" in issue.message for issue in issues)


def test_validate_repo_requires_baseline_readiness_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-readiness",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[{"kind": "origin_need", "path": "notes/origin-need.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("baseline_readiness" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_portable_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-portable-review",
        status="portable",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'portable' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-portable-review",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'baseline' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_local_shaped_portability_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-bounded-portability-drift",
        status="bounded",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'bounded' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_local_shaped_portability_for_draft_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-draft-portability-drift",
        status="draft",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'draft' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_portable_portability_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-baseline-portability-drift",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        portability_level="local-shaped",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'baseline' requires portability_level 'portable' but found 'local-shaped'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_broad_portability_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-portability-drift",
        status="canonical",
        public_safety_reviewed_at="2026-04-16",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'canonical' requires portability_level 'broad' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_public_safety_review_date_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-missing-public-safety-review",
        status="canonical",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'canonical' requires public_safety_reviewed_at" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_valid_calendar_public_safety_review_date(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-invalid-public-safety-review",
        status="canonical",
        public_safety_reviewed_at="2026-99-99",
    )

    issues = run_validation(tmp_path)

    assert any(
        "public_safety_reviewed_at must be a valid calendar date" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_future_public_safety_review_date(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-future-public-safety-review",
        status="canonical",
        public_safety_reviewed_at="2099-01-01",
        portability_level="broad",
    )

    issues = run_validation(tmp_path)

    assert any(
        "public_safety_reviewed_at must not be in the future" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_support_note_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_bounded_review_language_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/bounded-promotion-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/bounded-promotion-review.md": "# Bounded Review\nA useful note, but no explicit promotion language.\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions" in issue.message for issue in issues)


def test_validate_repo_requires_canonical_readiness_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-canonical-readiness",
        status="canonical",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "portable_review", "path": "notes/portable-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/portable-review.md": "# Portable Review\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'canonical' requires an evidence entry with kind 'canonical_readiness'" in issue.message for issue in issues)


def test_validate_repo_requires_support_note_for_comparative_summary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("report_format 'comparative-summary' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_fixed_baseline_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-fixed-baseline-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state the baseline target, noisy variation, and style-only overread limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_materialized_report_artifacts_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-report-artifacts",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("reports/summary.schema.json" in issue.message for issue in issues)
    assert any("reports/example-report.json" in issue.message for issue in issues)


def test_validate_repo_requires_runner_contract_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-runner",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-fixed-baseline-runner",
        include_runner_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_requires_peer_compare_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-peer-compare-contract",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nmatched conditions only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state matched conditions and side-by-side interpretation limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_fixed_baseline_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-fixed-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-fixed-baseline")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-fixed-baseline")

    assert issues == []


def test_validate_repo_accepts_valid_peer_compare_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-peer-compare",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-valid-peer-compare")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-peer-compare")

    assert issues == []


def test_validate_repo_accepts_valid_longitudinal_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-valid-longitudinal-window")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-longitudinal-window")

    assert issues == []


def test_validate_repo_requires_comparison_surface_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-surface",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-surface") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("comparison_surface", None)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("comparison_surface" in issue.message for issue in issues)


def test_validate_repo_requires_comparison_mode_in_comparative_report_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-mode",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-missing-comparison-mode")
    schema_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-mode") / "reports" / "summary.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"] = [item for item in schema["required"] if item != "comparison_mode"]
    schema["properties"].pop("comparison_mode", None)
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    example_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-mode") / "reports" / "example-report.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    example.pop("comparison_mode", None)
    example_path.write_text(json.dumps(example, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("comparison_mode" in issue.message for issue in issues)


def test_validate_repo_rejects_peer_compare_with_wrong_peer_surface_count(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-invalid-peer-surface-count",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = eval_dir_for_test(tmp_path, "aoa-invalid-peer-surface-count") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["peer_surfaces"] = ["aoa-peer-left"]
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("peer_surfaces" in issue.location or "peer_surfaces" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_shared_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-shared-family",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-shared-family")
    write_text(tmp_path / "fixtures" / "alt-family" / "README.md", "# Shared Fixture Family\n")
    manifest_path = eval_dir_for_test(tmp_path, "aoa-mismatched-shared-family") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["shared_family_path"] = "fixtures/alt-family/README.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("shared_family_path must match fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_paired_readout_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-paired-readout",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-paired-readout")
    write_text(tmp_path / "reports" / "alt-proof-flow.md", "# Paired Proof\n")
    manifest_path = eval_dir_for_test(tmp_path, "aoa-mismatched-paired-readout") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["paired_readout_path"] = "reports/alt-proof-flow.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("paired_readout_path must match runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_invalid_additional_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "fixtures" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["additional_shared_fixture_family_paths"] = ["fixtures/missing-v2/README.md"]
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any("additional_shared_fixture_family_paths" in issue.location for issue in issues)


def test_validate_repo_rejects_blank_shared_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "fixtures" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["shared_fixture_family_path"] = "   "
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any(
        issue.location.endswith(".shared_fixture_family_path")
        and "path must be a non-empty string" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_blank_additional_paired_readout_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "runners" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["additional_paired_readout_paths"] = ["   "]
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any(
        issue.location.endswith(".additional_paired_readout_paths[0]")
        and "path must be a non-empty string" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_comparison_doctrine_selection_parity(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-selection-drift",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-selection-drift")
    write_catalogs(tmp_path)
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        """
        # Eval Bundle Selection Chooser

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        - `aoa-selection-drift`
        """,
    )

    issues = run_validation(tmp_path)

    assert any("Pick Comparison Surface" in issue.message or "comparison selector question" in issue.message for issue in issues)


def test_validate_repo_requires_artifact_process_doctrine_guide(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-artifact-review-rubric", category="artifact")
    write_catalogs(tmp_path)
    (tmp_path / "docs" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md").unlink()

    issues = run_validation(tmp_path, eval_name="aoa-artifact-review-rubric")

    assert any("ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.location or "ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.message for issue in issues)


def test_validate_repo_requires_fixture_contract_for_longitudinal_window(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-longitudinal-fixture",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/window-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/window-contract.md": "# Window Contract\nordered window\nanchor workflow surface\nno clear directional movement\nmixed or unstable movement\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-longitudinal-fixture",
        include_fixture_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_missing_shared_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-shared-fixture")
    write_catalogs(tmp_path)
    write_text(
        eval_dir_for_test(tmp_path, "aoa-missing-shared-fixture") / "fixtures" / "contract.json",
        json.dumps(
            {
                "contract_version": 1,
                "shared_fixture_family_path": "fixtures/does-not-exist/README.md",
                "shared_case_surface": "shared bounded case family for validation",
                "bounded_replacement_rule": "replace only with the same bounded case class and public-safe evidence surface",
                "public_safe_requirements": ["outside reviewers can inspect the surface"],
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any("shared_fixture_family_path" in issue.location and "does not exist" in issue.message for issue in issues)


def test_validate_repo_rejects_report_example_that_violates_bundle_schema(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-report-example")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-invalid-report-example",
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
            ],
            "properties": {
                "eval_name": {"const": "aoa-invalid-report-example"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-invalid-report-example",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "missing limitations should fail",
        },
    )

    issues = run_validation(tmp_path)

    assert any("report violation" in issue.message and "limitations" in issue.message for issue in issues)


def test_validate_repo_rejects_actual_report_that_violates_bundle_schema(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-actual-report")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-invalid-actual-report",
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
            ],
            "properties": {
                "eval_name": {"const": "aoa-invalid-actual-report"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-invalid-actual-report",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "example includes limitations and should pass",
            "limitations": ["example remains bounded"],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-invalid-actual-report") / "reports" / "local-run.report.json",
        json.dumps(
            {
                "eval_name": "aoa-invalid-actual-report",
                "bundle_status": "draft",
                "object_under_evaluation": "bounded test surface",
                "verdict": "supports bounded claim",
                "claim_boundary": "missing limitations should fail for actual reports",
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any(
        issue.location.endswith("reports/local-run.report.json")
        and "report violation" in issue.message
        and "limitations" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_actual_report_with_manifest_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-drifted-actual-report")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-drifted-actual-report",
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
            ],
            "properties": {
                "eval_name": {"type": "string"},
                "bundle_status": {"type": "string"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-drifted-actual-report",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "example includes manifest-aligned fields",
            "limitations": ["example remains bounded"],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-drifted-actual-report") / "reports" / "local-run.report.json",
        json.dumps(
            {
                "eval_name": "wrong-eval-name",
                "bundle_status": "portable",
                "object_under_evaluation": "bounded test surface",
                "verdict": "supports bounded claim",
                "claim_boundary": "schema accepts this but manifest drift should fail",
                "limitations": ["actual report remains bounded"],
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any("eval_name must match manifest name" in issue.message for issue in issues)
    assert any("bundle_status must match manifest status" in issue.message for issue in issues)


def test_approval_boundary_schema_allows_missing_fallback_move() -> None:
    bundle_dir = eval_dir_for_test(REPO_ROOT, "aoa-approval-boundary-adherence")
    schema_path = (
        bundle_dir
        / "reports"
        / "summary.schema.json"
    )
    example_path = (
        bundle_dir
        / "reports"
        / "example-report.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    assert isinstance(example, dict)

    trimmed_example = json.loads(json.dumps(example))
    assert isinstance(trimmed_example.get("per_case_breakdown"), list)
    trimmed_example["per_case_breakdown"][0].pop("fallback_move", None)

    jsonschema.validate(trimmed_example, schema)


def test_antifragility_schema_requires_stressor_class() -> None:
    schema_path = (
        REPO_ROOT
        / "mechanics"
        / "antifragility"
        / "parts"
        / "posture-review"
        / "schemas"
        / "antifragility_eval_report_v1.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = {
        "schema_version": "antifragility_eval_report_v1",
        "report_id": "anti-001",
        "generated_at_utc": "2026-04-09T12:00:00Z",
        "scope": {
            "repo": "aoa-evals",
            "surface": "evals/stress/aoa-antifragility-posture/reports/example-report.json",
        },
        "inputs": {
            "receipt_refs": ["repo:aoa-evals/reports/receipt-001.json"],
            "adaptation_refs": [],
            "evidence_refs": ["repo:aoa-evals/reports/evidence-001.md"],
        },
        "axes": {
            axis: {"status": "pass"}
            for axis in (
                "containment",
                "fallback_fidelity",
                "false_action_prevention",
                "recovery_latency",
                "adaptation_gain",
                "operator_burden",
                "trust_calibration",
            )
        },
        "blind_spots": ["single-window read only"],
        "verdict_summary": "bounded antifragility posture remains intact",
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_antifragility_schema_requires_non_empty_receipt_refs() -> None:
    schema_path = (
        REPO_ROOT
        / "mechanics"
        / "antifragility"
        / "parts"
        / "posture-review"
        / "schemas"
        / "antifragility_eval_report_v1.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = {
        "schema_version": "antifragility_eval_report_v1",
        "report_id": "anti-002",
        "generated_at_utc": "2026-04-09T12:00:00Z",
        "scope": {
            "repo": "aoa-evals",
            "surface": "evals/stress/aoa-antifragility-posture/reports/example-report.json",
            "stressor_class": "latency-spike",
        },
        "inputs": {
            "receipt_refs": [],
            "adaptation_refs": [],
            "evidence_refs": ["repo:aoa-evals/reports/evidence-001.md"],
        },
        "axes": {
            axis: {"status": "pass"}
            for axis in (
                "containment",
                "fallback_fidelity",
                "false_action_prevention",
                "recovery_latency",
                "adaptation_gain",
                "operator_burden",
                "trust_calibration",
            )
        },
        "blind_spots": ["single-window read only"],
        "verdict_summary": "bounded antifragility posture remains intact",
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_longitudinal_growth_overclaim_detection_requires_real_negation() -> None:
    assert validate_repo.claim_boundary_overclaims_longitudinal_growth(
        "this report demonstrates broad capability growth rather than workflow-only movement"
    )
    assert validate_repo.claim_boundary_overclaims_longitudinal_growth(
        "this report demonstrates broad capability growth even though it does not prove general capability growth"
    )
    assert not validate_repo.claim_boundary_overclaims_longitudinal_growth(
        "this report does not prove broad capability growth"
    )
    assert not validate_repo.claim_boundary_overclaims_longitudinal_growth(
        "broad capability growth is not proven here"
    )


def test_validate_repo_allows_missing_initial_longitudinal_transition_note(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "follow-up transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert not any("transition_note" in issue.location for issue in issues)


def test_validate_repo_requires_longitudinal_transition_note(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert any("transition_note" in issue.message or "transition_note" in issue.location for issue in issues)


def test_validate_repo_allows_negated_longitudinal_growth_disclaimer_in_claim_boundary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "claim_boundary": (
                "This bounded report does not prove general capability growth beyond "
                "this anchored surface."
            ),
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert not any(
        "claim_boundary must stay weaker than broad or general capability growth" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_longitudinal_report_with_duplicate_window_id(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-duplicate-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-duplicate-longitudinal-window",
        report_example_override={
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
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "duplicate id transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_id 'LG-01' must be unique" in issue.message for issue in issues)


def test_validate_repo_rejects_longitudinal_report_with_non_increasing_window_order(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-out-of-order-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-out-of-order-longitudinal-window",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                    "transition_note": "out-of-order transition note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "second out-of-order transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_order values must be strictly increasing" in issue.message for issue in issues)


def test_validate_repo_requires_integrity_risk_taxonomy_enum(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-eval-integrity-check", category="capability")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-eval-integrity-check",
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
                "corpus_slice",
                "per_target_breakdown",
            ],
            "properties": {
                "eval_name": {"const": "aoa-eval-integrity-check"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "corpus_slice": {"type": "string"},
                "per_target_breakdown": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "target_bundle",
                            "integrity_risk_class",
                            "target_reading",
                            "note",
                        ],
                        "properties": {
                            "target_bundle": {"type": "string"},
                            "integrity_risk_class": {
                                "type": "string",
                                "enum": ["style-over-substance"],
                            },
                            "target_reading": {"type": "string"},
                            "note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": "aoa-eval-integrity-check",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed support",
            "claim_boundary": "bounded integrity example",
            "limitations": ["still bounded"],
            "corpus_slice": "starter bundles",
            "per_target_breakdown": [
                {
                    "target_bundle": "aoa-alpha",
                    "integrity_risk_class": "style-over-substance",
                    "target_reading": "mixed support",
                    "note": "note",
                }
            ],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "notes" / "review-contract.md",
        "\n".join(
            [
                "# Review Contract",
                "style-over-substance",
                "artifact/process collapse",
                "baseline by association",
                "growth by association",
                "peer-compare blur",
                "fixed-baseline drift",
                "longitudinal overclaim",
                "schema-clean but claim-overstated",
                "routing overreach",
                "",
            ]
        ),
    )
    write_integrity_example_report(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "examples" / "example-report.md"
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-eval-integrity-check")

    assert any("integrity_risk_class enum must match" in issue.message for issue in issues)


def test_validate_repo_requires_integrity_taxonomy_in_example_report(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-eval-integrity-check", category="capability")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-eval-integrity-check",
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
                "corpus_slice",
                "per_target_breakdown",
            ],
            "properties": {
                "eval_name": {"const": "aoa-eval-integrity-check"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"type": "string"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "corpus_slice": {"type": "string"},
                "per_target_breakdown": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "target_bundle",
                            "integrity_risk_class",
                            "target_reading",
                            "note",
                        ],
                        "properties": {
                            "target_bundle": {"type": "string"},
                            "integrity_risk_class": {
                                "type": "string",
                                "enum": [
                                    "style-over-substance",
                                    "artifact/process collapse",
                                    "baseline by association",
                                    "growth by association",
                                    "peer-compare blur",
                                    "fixed-baseline drift",
                                    "longitudinal overclaim",
                                    "schema-clean but claim-overstated",
                                    "routing overreach",
                                ],
                            },
                            "target_reading": {"type": "string"},
                            "note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": "aoa-eval-integrity-check",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed support",
            "claim_boundary": "bounded integrity example",
            "limitations": ["still bounded"],
            "corpus_slice": "starter bundles",
            "per_target_breakdown": [
                {
                    "target_bundle": "aoa-alpha",
                    "integrity_risk_class": "style-over-substance",
                    "target_reading": "mixed support",
                    "note": "note",
                }
            ],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "notes" / "review-contract.md",
        "\n".join(
            [
                "# Review Contract",
                "style-over-substance",
                "artifact/process collapse",
                "baseline by association",
                "growth by association",
                "peer-compare blur",
                "fixed-baseline drift",
                "longitudinal overclaim",
                "schema-clean but claim-overstated",
                "routing overreach",
                "",
            ]
        ),
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "examples" / "example-report.md",
        "# Example Report\n",
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-eval-integrity-check")

    assert any(
        issue.location == "evals/capability/aoa-eval-integrity-check/examples/example-report.md"
        and "integrity example report must mention" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_roadmap_current_public_surface_to_be_a_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-alpha")
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha"])
    make_roadmap(tmp_path, ["aoa-beta"])
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("roadmap 'Current public surface' eval 'aoa-beta' must appear in EVAL_INDEX.md starter bundles" in issue.message for issue in issues)


def test_validate_roadmap_parity_rejects_generic_heading(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8").replace(
            "# Proof Direction Roadmap",
            "# Roadmap",
            1,
        ),
        encoding="utf-8",
    )
    write_catalogs(tmp_path)

    issues = validate_repo.validate_roadmap_parity(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
    )

    assert any(
        issue.location == "ROADMAP.md"
        and "# Proof Direction Roadmap" in issue.message
        for issue in issues
    )


def test_validate_repo_allows_public_bundle_outside_starter_surface(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-starter-alpha") == []
    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_repo_allows_targeted_non_starter_bundle_validation(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_eval_index_allows_targeted_non_starter_bundle_selection(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    issues = validate_eval_index(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
        selected_evals={"aoa-public-draft"},
    )

    assert issues == []


def test_validate_repo_requires_absence_note_sync_between_roadmap_and_index(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-absence-note-drift")
    make_roadmap(tmp_path, ["aoa-absence-note-drift"], include_absence_note=False)
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("absence note" in issue.message for issue in issues)


def test_validate_repo_rejects_mirrored_field_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-field-drift")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-field-drift") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["category"] = "artifact"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("field 'category' does not match" in issue.message for issue in issues)


def test_validate_repo_rejects_technique_dependency_order_mismatch(tmp_path: Path) -> None:
    technique_dependencies = [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md",
        },
        {
            "id": "AOA-T-0002",
            "repo": "aoa-techniques",
            "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-technique-order-drift",
        technique_dependencies=technique_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-technique-order-drift") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["technique_dependencies"] = list(reversed(frontmatter["technique_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered technique refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_skill_dependency_order_mismatch(tmp_path: Path) -> None:
    skill_dependencies = [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/core/engineering/aoa-change-protocol/SKILL.md",
        },
        {
            "name": "aoa-approval-gate-check",
            "repo": "aoa-skills",
            "path": "skills/aoa-approval-gate-check/SKILL.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-skill-order-drift",
        skill_dependencies=skill_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-skill-order-drift") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["skill_dependencies"] = list(reversed(frontmatter["skill_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered skill refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_repo_mismatch(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-repo-mismatch")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-repo-mismatch") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["repo"] = "example/other-repo"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("repo must resolve to 'aoa-techniques'" in issue.message for issue in issues)


def test_validate_repo_rejects_non_repo_relative_dependency_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-path-mismatch")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-path-mismatch") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["path"] = "../techniques/test/TECHNIQUE.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("path must be a concrete repo-relative path" in issue.message for issue in issues)


def test_validate_repo_accepts_dependency_targets_when_roots_exist(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-dependency-targets")
    write_catalogs(tmp_path)

    techniques_root = tmp_path / ".deps" / "aoa-techniques"
    skills_root = tmp_path / ".deps" / "aoa-skills"
    write_text(
        techniques_root
        / "techniques"
        / "execution"
        / "agent-workflows-core"
        / "plan-diff-apply-verify-report"
        / "TECHNIQUE.md",
        "# Technique\n",
    )
    write_text(
        skills_root / "skills" / "core" / "engineering" / "aoa-change-protocol" / "SKILL.md",
        "# Skill\n",
    )

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", skills_root)

    assert run_validation(tmp_path, eval_name="aoa-valid-dependency-targets") == []


def test_validate_repo_rejects_missing_dependency_target_when_root_exists(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-dependency-target")
    write_catalogs(tmp_path)

    techniques_root = tmp_path / ".deps" / "aoa-techniques"
    skills_root = tmp_path / ".deps" / "aoa-skills"
    write_text(techniques_root / "README.md", "# Technique Repo\n")
    write_text(
        skills_root / "skills" / "aoa-change-protocol" / "SKILL.md",
        "# Skill\n",
    )

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", skills_root)

    issues = run_validation(tmp_path, eval_name="aoa-missing-dependency-target")

    assert any(
        "dependency target does not exist: aoa-techniques/techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md"
        in issue.message
        for issue in issues
    )


def test_validate_repo_missing_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-generated")

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if "generated/" in issue.location)


def test_validate_repo_missing_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-capsules")
    write_catalogs(tmp_path)

    (tmp_path / "generated" / "eval_capsules.json").unlink()

    issues = run_validation(tmp_path)

    assert any(
        issue.location == "generated/eval_capsules.json" and "file is missing" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-generated") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-capsules")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-capsules") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim changed without rebuilding capsules.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated capsules are out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_catalog_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-generated") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-generated")

    assert any(
        "generated catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_capsule_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-capsule")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-capsule") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim drifted after generation.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-capsule")

    assert any(
        "generated capsule entry for 'aoa-targeted-stale-capsule' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_catalog_metadata(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-metadata-drift")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    full_catalog["catalog_version"] = 999
    min_catalog["source_of_truth"] = {"broken": True}
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path, eval_name="aoa-targeted-metadata-drift")

    assert any(
        "generated catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_source_section_without_derivable_content(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-capsule-source",
        section_overrides={"Interpretation guidance": ""},
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "missing capsule source section 'Interpretation guidance'" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-capsule-alignment-drift")
    write_catalogs(tmp_path)

    capsule_path = tmp_path / "generated" / "eval_capsules.json"
    capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
    capsules["evals"] = []
    capsule_path.write_text(json.dumps(capsules), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "capsules are missing eval 'aoa-capsule-alignment-drift' from generated/eval_catalog.json"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_missing_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-sections-surface")
    write_catalogs(tmp_path)
    (tmp_path / "generated" / "eval_sections.full.json").unlink()

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if issue.location.endswith("eval_sections.full.json"))


def test_validate_repo_rejects_stale_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-sections-surface")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-sections-surface") / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated sections are out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_section_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-section-alignment-drift")
    write_catalogs(tmp_path)

    sections_path = tmp_path / "generated" / "eval_sections.full.json"
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    sections["evals"][0]["status"] = "promoted"
    sections_path.write_text(json.dumps(sections), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated section entry for 'aoa-section-alignment-drift' must align with full catalog field 'status'"
        in issue.message
        for issue in issues
    )


def test_generated_route_residue_accepts_current_generated_readouts() -> None:
    assert validate_repo.validate_generated_route_residue(REPO_ROOT) == []


def test_generated_route_residue_surfaces_validate_current_reader_index() -> None:
    assert validate_repo.validate_generated_route_residue_surfaces(REPO_ROOT) == []


def test_generated_route_residue_surfaces_reject_missing_quest_reader_route(
    tmp_path: Path,
) -> None:
    for path_name in (
        "generated/README.md",
        "generated/AGENTS.md",
        validate_repo.GENERATED_ROUTE_RESIDUE_DECISION_NAME,
        "docs/decisions/README.md",
        validate_repo.PROOF_TOPOLOGY_NAME,
        validate_repo.LEGACY_NAMING_NAME,
        validate_repo.ROADMAP_NAME,
    ):
        copy_repo_text(tmp_path, path_name)
    agents_path = tmp_path / "generated" / "AGENTS.md"
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "`generated/quest_catalog.min.json`, ",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_generated_route_residue_surfaces(tmp_path)

    assert any(
        issue.location == "generated/AGENTS.md"
        and "generated/quest_catalog.min.json" in issue.message
        for issue in issues
    )


def test_generated_route_residue_rejects_root_route_card_structural_reference(
    tmp_path: Path,
) -> None:
    write_json_file(
        tmp_path / "generated" / "eval_catalog.json",
        {
            "evals": [
                {
                    "name": "aoa-stale-root-fixture-ref",
                    "proof_artifacts": {
                        "shared_fixture_family_path": "fixtures/old/README.md"
                    },
                }
            ]
        },
    )

    issues = validate_repo.validate_generated_route_residue(tmp_path)

    assert any(
        "route-card-only root district 'fixtures/'" in issue.message
        for issue in issues
    )


def test_generated_route_residue_rejects_legacy_mechanic_parent_reference(
    tmp_path: Path,
) -> None:
    write_json_file(
        tmp_path / "generated" / "comparison_spine.json",
        {
            "evals": [
                {
                    "name": "aoa-stale-titan-parent-ref",
                    "proof_artifacts": {
                        "shared_fixture_family_path": "mechanics/titan-canaries/parts/seed-boundary/README.md"
                    },
                }
            ]
        },
    )

    issues = validate_repo.validate_generated_route_residue(tmp_path)

    assert any(
        "not legacy parent route 'mechanics/titan-canaries/'" in issue.message
        for issue in issues
    )


def test_generated_route_residue_allows_part_local_generated_config_reference(
    tmp_path: Path,
) -> None:
    part_root = tmp_path / "mechanics" / "agon" / "parts" / "court-prebinding"
    write_text(part_root / "config" / "seed.json", "{}")
    write_json_file(
        part_root / "generated" / "registry.min.json",
        {"source": "config/seed.json"},
        compact=True,
    )

    assert validate_repo.validate_generated_route_residue(tmp_path) == []


def test_generated_route_residue_ignores_markdown_content_paths(
    tmp_path: Path,
) -> None:
    write_json_file(
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

    assert validate_repo.validate_generated_route_residue(tmp_path) == []


def test_targeted_validation_catches_stale_generated_section_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-sections")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-sections") / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-sections")

    assert any(
        "generated section entry for 'aoa-targeted-stale-sections' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_min_projection_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-min-projection-drift")
    write_catalogs(tmp_path)

    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    min_catalog["evals"][0]["summary"] = "tampered"
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "min catalog must stay a projection of the full catalog" in issue.message
        for issue in issues
    )


def test_validate_repo_reports_malformed_full_catalog_projection_error(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-malformed-full-catalog")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    del full_catalog["evals"]
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is malformed; min projection could not be computed" in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_non_baseline_bundle_without_baseline_readiness(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-non-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-non-baseline") == []


def test_validate_repo_accepts_valid_bounded_bundle_with_review_note(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-bounded", status="bounded")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-bounded") == []


def test_validate_repo_accepts_valid_baseline_bundle_with_readiness_evidence(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline") == []


def test_validate_repo_accepts_valid_baseline_status_bundle_with_portable_review(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline-status",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-baseline-status",
        status="baseline",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline-status") == []


def test_validate_repo_accepts_valid_longitudinal_bundle_with_materialized_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-materialized",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-longitudinal-materialized",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-longitudinal-materialized") == []


def test_validate_repo_allows_local_run_without_sibling_dependency_repos(monkeypatch) -> None:
    missing_techniques_root = REPO_ROOT / ".tmp" / "missing-aoa-techniques"
    missing_skills_root = REPO_ROOT / ".tmp" / "missing-aoa-skills"
    missing_agents_root = REPO_ROOT / ".tmp" / "missing-aoa-agents"
    missing_playbooks_root = REPO_ROOT / ".tmp" / "missing-aoa-playbooks"
    missing_memo_root = REPO_ROOT / ".tmp" / "missing-aoa-memo"
    missing_abyss_stack_root = REPO_ROOT / ".tmp" / "missing-abyss-stack"

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", missing_techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", missing_skills_root)
    monkeypatch.setattr(validate_repo, "AOA_AGENTS_ROOT", missing_agents_root)
    monkeypatch.setattr(validate_repo, "AOA_PLAYBOOKS_ROOT", missing_playbooks_root)
    monkeypatch.setattr(validate_repo, "AOA_MEMO_ROOT", missing_memo_root)
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", missing_abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": validate_repo.REPO_ROOT,
            "aoa-techniques": missing_techniques_root,
            "aoa-skills": missing_skills_root,
            "aoa-agents": missing_agents_root,
            "aoa-playbooks": missing_playbooks_root,
            "aoa-memo": missing_memo_root,
            "abyss-stack": missing_abyss_stack_root,
        },
    )

    issues = run_validation(REPO_ROOT)

    assert not any(
        "dependency target does not exist: aoa-techniques/" in issue.message
        or "dependency target does not exist: aoa-skills/" in issue.message
        or "reference target does not exist: aoa-agents/" in issue.message
        or "reference target does not exist: aoa-playbooks/" in issue.message
        or "reference target does not exist: aoa-memo/" in issue.message
        or "reference target does not exist: abyss-stack/" in issue.message
        or "does not resolve in aoa-playbooks" in issue.message
        for issue in issues
    )


def test_resolve_abyss_stack_root_prefers_source_checkout_over_runtime_tree(
    tmp_path: Path,
    monkeypatch,
) -> None:
    runtime_like_root = tmp_path / "srv" / "abyss-stack"
    write_text(runtime_like_root / "Configs" / "README.md", "# Runtime mirror\n")

    home_root = tmp_path / "home" / "dionysus"
    source_root = home_root / "src" / "abyss-stack"
    write_text(source_root / "README.md", "# abyss-stack\n")
    write_text(source_root / "scripts" / "validate_stack.py", "print('ok')\n")
    write_text(
        source_root
        / "mechanics"
        / "governed-execution"
        / "parts"
        / "return-policy"
        / "schemas"
        / "runtime-return-event.schema.json",
        "{}\n",
    )

    monkeypatch.setenv("HOME", str(home_root))
    monkeypatch.delenv("ABYSS_STACK_ROOT", raising=False)

    resolved = validate_repo.resolve_abyss_stack_root(runtime_like_root)

    assert resolved == source_root.resolve()


def test_resolve_abyss_stack_root_respects_env_override(
    tmp_path: Path,
    monkeypatch,
) -> None:
    default_root = tmp_path / "srv" / "abyss-stack"
    override_root = tmp_path / "custom" / "abyss-stack"
    monkeypatch.setenv("ABYSS_STACK_ROOT", str(override_root))

    resolved = validate_repo.resolve_abyss_stack_root(default_root)

    assert resolved == override_root.resolve()


def test_validate_repo_accepts_return_runtime_evidence_selection_for_non_starter_bundle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-return-anchor-integrity")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    make_repo_docs(tmp_path, starter_names=["aoa-starter-alpha"])
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    write_catalogs(tmp_path)

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": tmp_path,
            "aoa-agents": validate_repo.AOA_AGENTS_ROOT,
            "aoa-playbooks": validate_repo.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": validate_repo.AOA_MEMO_ROOT,
            "abyss-stack": abyss_stack_root,
        },
    )

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert issues == []


def test_validate_repo_rejects_return_runtime_evidence_selection_outside_tracked_schema_space(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-return-anchor-integrity")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    make_repo_docs(tmp_path, starter_names=["aoa-starter-alpha"])
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/docs/RECURRENCE_RUNTIME_POLICY.md",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    write_catalogs(tmp_path)

    abyss_stack_root = tmp_path / "abyss-stack"
    write_text(abyss_stack_root / "docs" / "RECURRENCE_RUNTIME_POLICY.md", "# Recurrence Runtime Policy\n")
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": tmp_path,
            "aoa-agents": validate_repo.AOA_AGENTS_ROOT,
            "aoa-playbooks": validate_repo.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": validate_repo.AOA_MEMO_ROOT,
            "abyss-stack": abyss_stack_root,
        },
    )

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert any(
        "source_schema_ref must equal 'repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_non_tracked_abyss_stack_logs_refs_for_return_runtime_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-return-anchor-integrity")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    make_repo_docs(tmp_path, starter_names=["aoa-starter-alpha"])
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    write_catalogs(tmp_path)

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": tmp_path,
            "aoa-agents": validate_repo.AOA_AGENTS_ROOT,
            "aoa-playbooks": validate_repo.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": validate_repo.AOA_MEMO_ROOT,
            "abyss-stack": abyss_stack_root,
        },
    )

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert not any(
        "reference target does not exist: abyss-stack/Logs/" in issue.message
        for issue in issues
    )


def test_validate_repo_allows_return_anchor_integrity_as_public_non_starter_bundle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-return-anchor-integrity")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    make_repo_docs(tmp_path, starter_names=["aoa-starter-alpha"])
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    write_catalogs(tmp_path)

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": tmp_path,
            "aoa-agents": validate_repo.AOA_AGENTS_ROOT,
            "aoa-playbooks": validate_repo.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": validate_repo.AOA_MEMO_ROOT,
            "abyss-stack": abyss_stack_root,
        },
    )

    assert run_validation(tmp_path, eval_name="aoa-return-anchor-integrity") == []


def test_validate_runtime_evidence_selection_uses_repo_local_schema(tmp_path: Path) -> None:
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    schema_path = tmp_path / validate_repo.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"].append("repo_local_only")
    schema["properties"]["repo_local_only"] = {"type": "string"}
    write_json_payload(schema_path, schema)

    issues = validate_repo.validate_runtime_evidence_selection_surfaces(
        tmp_path,
        records=[],
        target_eval_names={"aoa-return-anchor-integrity"},
    )

    assert any(
        issue.location == "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_validate_runtime_evidence_selection_reports_missing_expected_examples_in_full_run(tmp_path: Path) -> None:
    write_text(
        tmp_path / validate_repo.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object"
        }
        """,
    )

    issues = validate_repo.validate_runtime_evidence_selection_surfaces(tmp_path, records=[])

    assert any(
        issue.location.endswith("runtime_evidence_selection.workhorse-local.example.json")
        and "file is missing" in issue.message
        for issue in issues
    )


def test_validate_runtime_evidence_selection_accepts_example_backed_runtime_chaos_window() -> None:
    issues, records = collect_catalog_records(REPO_ROOT)

    assert issues == []
    assert (
        validate_repo.validate_runtime_evidence_selection_surfaces(
            REPO_ROOT,
            records,
            target_eval_names={"aoa-stress-recovery-window"},
        )
        == []
    )


def test_validate_runtime_integrity_review_surface_accepts_repo_contract() -> None:
    assert validate_repo.validate_runtime_integrity_review_surface(REPO_ROOT) == []


def test_validate_runtime_integrity_review_surface_requires_all_declared_doc_fields(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    doc_path = tmp_path / validate_repo.RUNTIME_INTEGRITY_REVIEW_DOC_NAME
    doc_text = doc_path.read_text(encoding="utf-8").replace("`evidence_refs`", "evidence refs", 1)
    doc_path.write_text(doc_text, encoding="utf-8")

    issues = validate_repo.validate_runtime_integrity_review_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md"
        and "runtime integrity review guide must mention '`evidence_refs`'" == issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_uses_repo_local_schema(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / validate_repo.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"].append("repo_local_only")
    schema["properties"]["repo_local_only"] = {"type": "string"}
    write_json_payload(schema_path, schema)

    issues = validate_repo.validate_runtime_integrity_review_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_weakened_schema_contract(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / validate_repo.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["properties"]["evidence_refs"]["minItems"] = 1
    write_json_payload(schema_path, schema)

    issues = validate_repo.validate_runtime_integrity_review_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
        and "evidence_refs as an exact-count unique repo-ref array" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_open_top_level_schema(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / validate_repo.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["additionalProperties"] = True
    write_json_payload(schema_path, schema)

    issues = validate_repo.validate_runtime_integrity_review_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
        and "top-level additionalProperties set to false" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_missing_center_anchor(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = tmp_path / "aoa-evals"
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(repo_root, relative_path)

    routing_root = tmp_path / "aoa-routing"
    write_text(routing_root / "docs" / "LIVE_SESSION_REENTRY_ROUTE_REVIEW.md", "# Live Session Reentry Route Review\n")
    agents_root = tmp_path / "aoa-agents"
    write_text(agents_root / "docs" / "SELF_AGENCY_CONTINUITY_LANE.md", "# Self-Agency Continuity Lane\n")
    memo_root = tmp_path / "aoa-memo"
    write_text(memo_root / "schemas" / "inquiry_checkpoint.schema.json", "{\n  \"type\": \"object\"\n}\n")
    write_text(
        memo_root / "docs" / "SELF_AGENCY_CONTINUITY_WRITEBACK.md",
        "# Self-Agency Continuity Writeback\n",
    )
    center_root = tmp_path / "Agents-of-Abyss"
    write_text(
        center_root / "mechanics" / "experience" / "parts" / "continuity-context" / "CONTRACT.md",
        "# Continuity Context Contract\n",
    )

    monkeypatch.setattr(validate_repo, "AGENTS_OF_ABYSS_ROOT", center_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": repo_root,
            "aoa-routing": routing_root,
            "aoa-agents": agents_root,
            "aoa-memo": memo_root,
        },
    )

    issues = validate_repo.validate_runtime_integrity_review_surface(repo_root)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json.budget_ref"
        and "anchor 'stronger-owner-split' was not found" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_anchor_drift_in_evidence_refs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = tmp_path / "aoa-evals"
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(repo_root, relative_path)

    example_path = repo_root / validate_repo.RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME
    payload = json.loads(example_path.read_text(encoding="utf-8"))
    payload["evidence_refs"][0] = "repo:aoa-evals/mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md#purpose"
    write_json_payload(example_path, payload)

    routing_root = tmp_path / "aoa-routing"
    write_text(routing_root / "docs" / "LIVE_SESSION_REENTRY_ROUTE_REVIEW.md", "# Live Session Reentry Route Review\n")
    agents_root = tmp_path / "aoa-agents"
    write_text(agents_root / "docs" / "SELF_AGENCY_CONTINUITY_LANE.md", "# Self-Agency Continuity Lane\n")
    memo_root = tmp_path / "aoa-memo"
    write_text(memo_root / "schemas" / "inquiry_checkpoint.schema.json", "{\n  \"type\": \"object\"\n}\n")
    write_text(
        memo_root / "docs" / "SELF_AGENCY_CONTINUITY_WRITEBACK.md",
        "# Self-Agency Continuity Writeback\n",
    )
    center_root = tmp_path / "Agents-of-Abyss"
    write_text(
        center_root / "mechanics" / "experience" / "parts" / "continuity-context" / "CONTRACT.md",
        "# Continuity Context Contract\n\n## Stronger Owner Split\n",
    )

    monkeypatch.setattr(validate_repo, "AGENTS_OF_ABYSS_ROOT", center_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": repo_root,
            "aoa-routing": routing_root,
            "aoa-agents": agents_root,
            "aoa-memo": memo_root,
        },
    )

    issues = validate_repo.validate_runtime_integrity_review_surface(repo_root)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
        and "bounded W10 runtime integrity review surfaces" in issue.message
        for issue in issues
    )


def test_validate_trace_eval_bridge_surfaces_keeps_local_example_checks_when_playbooks_missing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_text(
        tmp_path / validate_repo.ARTIFACT_VERDICT_HOOK_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object",
          "required": ["repo_local_only"],
          "properties": {
            "repo_local_only": {"type": "string"}
          }
        }
        """,
    )
    write_json_payload(tmp_path / "generated" / "eval_catalog.min.json", {"evals": []})
    write_json_payload(
        tmp_path
        / "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
        {},
    )
    monkeypatch.setattr(validate_repo, "AOA_PLAYBOOKS_ROOT", tmp_path / "missing-playbooks")
    monkeypatch.setattr(
        validate_repo,
        "ARTIFACT_VERDICT_HOOK_EXAMPLES",
        {"AOA-P-0006": "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json"},
    )

    issues = validate_repo.validate_trace_eval_bridge_surfaces(tmp_path, [])

    assert any(
        issue.location == "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_duplicate_eval_headings_are_detected_before_dict_normalization(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-duplicate-headings")
    eval_md_path = eval_dir_for_test(tmp_path, "aoa-duplicate-headings") / "EVAL.md"
    eval_md_text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        eval_md_text.replace(
            "## Object under evaluation",
            "## Intent\nSecond intent block.\n\n## Object under evaluation",
            1,
        ),
        encoding="utf-8",
    )

    issues, records = collect_catalog_records(tmp_path)
    sections, section_issues = eval_section_contract.build_sections_payload(tmp_path, records)

    assert sections["evals"] == []
    assert any("duplicate top-level section 'Intent'" in issue.message for issue in issues)
    assert any("duplicate top-level section 'Intent'" in issue.message for issue in section_issues)


def test_real_repo_has_expected_non_local_shaped_portability_bundles() -> None:
    issues, records = collect_catalog_records(REPO_ROOT)

    assert issues == []
    non_local_shaped = {
        record.name: record.manifest["portability_level"]
        for record in records
        if record.manifest["portability_level"] != "local-shaped"
    }
    assert non_local_shaped == {
        "aoa-artifact-review-rubric": "portable",
        "aoa-bounded-change-quality": "portable",
        "aoa-local-text-contract-fit": "portable",
        "aoa-regression-same-task": "portable",
        "aoa-ring-application-discipline": "portable",
        "aoa-verification-honesty": "portable",
    }


def test_validate_repo_accepts_valid_bundle_with_materialized_proof_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-proof-artifacts")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-proof-artifacts",
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
            ],
            "properties": {
                "eval_name": {"const": "aoa-valid-proof-artifacts"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-valid-proof-artifacts",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "bounded machine-readable proof artifact for validation",
            "limitations": ["still bounded"],
        },
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-proof-artifacts") == []


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

    def test_quest_lifecycle_surface_validates_current_state_contract(self) -> None:
        quest_schema = json.loads(
            (REPO_ROOT / validate_repo.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        assert validate_repo.validate_quest_lifecycle_surface(REPO_ROOT, quest_schema) == []

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
            (tmp_path / validate_repo.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        issues = validate_repo.validate_quest_lifecycle_surface(tmp_path, quest_schema)

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
            (tmp_path / validate_repo.QUEST_SCHEMA_NAME).read_text(encoding="utf-8")
        )

        issues = validate_repo.validate_quest_lifecycle_surface(tmp_path, quest_schema)

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

        monkeypatch.setattr(validate_repo, "AOA_AGENTS_ROOT", missing_agents_root)

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
                key=lambda path: validate_repo.quest_sort_key(path.stem),
            )
        ]

        assert validate_repo.discover_quest_names(tmp_path) == expected_quest_names

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
        integration_path = tmp_path / "docs" / "QUESTBOOK_EVAL_INTEGRATION.md"
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
        issues.extend(validate_repo.validate_unlock_proof_bridge_surface(tmp_path))

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

        issues = validate_repo.validate_unlock_proof_bridge_surface(tmp_path)

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

        catalog_projection = validate_repo.build_quest_catalog_projection(tmp_path)
        dispatch_projection = validate_repo.build_quest_dispatch_projection(tmp_path)
        expected_quest_names = [
            path.stem
            for path in sorted(
                (REPO_ROOT / "quests").rglob("AOA-EV-Q-*.yaml"),
                key=lambda path: validate_repo.quest_sort_key(path.stem),
            )
        ]

        assert [entry["id"] for entry in catalog_projection] == expected_quest_names
        assert [entry["id"] for entry in dispatch_projection] == expected_quest_names


class TestValidateQuestRouteSurfaces:
    def test_quest_route_surfaces_validate_current_schema_backed_layout(self) -> None:
        assert validate_repo.validate_quest_route_surfaces(REPO_ROOT) == []

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

        issues = validate_repo.validate_quest_route_surfaces(tmp_path)

        assert any(
            issue.location == "quests/README.md"
            and "# Quest Source Records" in issue.message
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

        issues = validate_repo.validate_quest_route_surfaces(tmp_path)

        assert any(
            issue.location == "quests/agon/captured/AOE-Q-AGON-0001.md"
            and "markdown quest notes must not live under active quest lifecycle paths"
            in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_validates_for_current_repo(self) -> None:
        issues = validate_repo.validate_runtime_candidate_template_index(REPO_ROOT)

        assert issues == []

    def test_runtime_candidate_template_index_drift_fails(self, tmp_path: Path) -> None:
        make_runtime_candidate_template_index_surface(tmp_path)
        index_path = tmp_path / validate_repo.RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["templates"][0]["review_required"] = False
        write_json_payload(index_path, payload)

        issues = validate_repo.validate_runtime_candidate_template_index(tmp_path)

        assert any(
            issue.location == "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_rejects_non_normalized_required_runtime_artifacts(self, tmp_path: Path) -> None:
        make_runtime_candidate_template_index_surface(tmp_path)
        example_path = (
            tmp_path
            / validate_repo.RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR
            / "runtime_evidence_selection.workhorse-local.example.json"
        )
        example_payload = json.loads(example_path.read_text(encoding="utf-8"))
        example_payload["selected_evidence"][0]["evidence_role"] = "Summary Artifact"
        write_json_payload(example_path, example_payload)

        index_path = tmp_path / validate_repo.RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        for entry in payload["templates"]:
            if entry["template_name"] == "workhorse-q4-vs-q6-latency-tradeoff":
                entry["required_runtime_artifacts"][0] = "Summary Artifact"
                break
        write_json_payload(index_path, payload)

        issues = validate_repo.validate_runtime_candidate_template_index(tmp_path)

        assert any(
            issue.location.startswith("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json.templates[")
            and "normalized to lowercase runtime artifact names" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_template_index_reports_builder_system_exit(self, monkeypatch) -> None:
        class FailingBuilder:
            def build_runtime_candidate_template_index_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        monkeypatch.setattr(
            validate_repo,
            "load_runtime_candidate_template_index_builder",
            lambda repo_root: FailingBuilder(),
        )

        issues = validate_repo.validate_runtime_candidate_template_index(REPO_ROOT)

        assert issues == [
            validate_repo.ValidationIssue(
                "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
                "builder-exit",
            )
        ]

    def test_runtime_candidate_intake_validates_for_current_repo(self) -> None:
        issues = validate_repo.validate_runtime_candidate_intake(REPO_ROOT)

        assert issues == []

    def test_runtime_candidate_intake_drift_fails(self, tmp_path: Path) -> None:
        make_runtime_candidate_intake_surface(tmp_path)
        intake_path = tmp_path / validate_repo.RUNTIME_CANDIDATE_INTAKE_NAME
        payload = json.loads(intake_path.read_text(encoding="utf-8"))
        payload["templates"][0]["review_guide_ref"] = "docs/DRIFTED.md"
        write_json_payload(intake_path, payload)

        issues = validate_repo.validate_runtime_candidate_intake(tmp_path)

        assert any(
            issue.location == "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_intake_rejects_missing_owner_review_ref(self, tmp_path: Path) -> None:
        make_runtime_candidate_intake_surface(tmp_path)
        intake_path = tmp_path / validate_repo.RUNTIME_CANDIDATE_INTAKE_NAME
        payload = json.loads(intake_path.read_text(encoding="utf-8"))
        payload["templates"][0]["owner_review_refs"] = []
        write_json_payload(intake_path, payload)

        issues = validate_repo.validate_runtime_candidate_intake(tmp_path)

        assert any(
            issue.location.startswith("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json.templates[")
            and "owner_review_refs must stay a non-empty list" in issue.message
            for issue in issues
        )

    def test_runtime_candidate_intake_reports_builder_system_exit(self, monkeypatch) -> None:
        class FailingBuilder:
            def build_runtime_candidate_intake_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        monkeypatch.setattr(
            validate_repo,
            "load_runtime_candidate_intake_builder",
            lambda repo_root: FailingBuilder(),
        )

        issues = validate_repo.validate_runtime_candidate_intake(REPO_ROOT)

        assert issues == [
            validate_repo.ValidationIssue(
                "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
                "builder-exit",
            )
        ]

    def test_eval_report_index_validates_for_current_repo(self) -> None:
        issues = validate_repo.validate_eval_report_index(REPO_ROOT)

        assert issues == []

    def test_eval_report_index_drift_fails(self, tmp_path: Path) -> None:
        make_eval_report_index_surface(tmp_path)
        index_path = tmp_path / "generated" / "eval_report_index.min.json"
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["reports"][0]["verdict"] = "drifted verdict"
        write_json_payload(index_path, payload)

        issues = validate_repo.validate_eval_report_index(tmp_path)

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

        issues = validate_repo.validate_eval_report_index(tmp_path)

        assert any(
            issue.location.startswith("generated/eval_report_index.min.json.reports[")
            and "receipt_status must stay 'not_a_receipt'" in issue.message
            for issue in issues
        )

    def test_eval_report_index_reports_builder_system_exit(self, monkeypatch) -> None:
        class FailingBuilder:
            def build_eval_report_index_payload(self) -> dict[str, object]:
                raise SystemExit("builder-exit")

        monkeypatch.setattr(
            validate_repo,
            "load_eval_report_index_builder",
            lambda repo_root: FailingBuilder(),
        )

        issues = validate_repo.validate_eval_report_index(REPO_ROOT)

        assert issues == [
            validate_repo.ValidationIssue(
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
            validate_repo.build_quest_catalog_projection(tmp_path)

    def test_questbook_validation_ignores_missing_agents_checkout_for_orchestrator_refs(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        make_questbook_surface(tmp_path)
        monkeypatch.setattr(validate_repo, "AOA_AGENTS_ROOT", tmp_path / "missing-aoa-agents")

        issues = validate_repo.validate_questbook_surface(tmp_path)

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

        issues = validate_repo.validate_questbook_surface(tmp_path)

        assert any("unexpected quest id" in issue.message for issue in issues)

    def test_phase_alpha_eval_matrix_validates_for_current_repo(self) -> None:
        issues = validate_repo.validate_phase_alpha_eval_matrix(REPO_ROOT)

        assert issues == []

    def test_phase_alpha_eval_matrix_drift_fails(self, tmp_path: Path, monkeypatch) -> None:
        make_phase_alpha_eval_matrix_surface(tmp_path)
        matrix_path = (
            tmp_path
            / "mechanics"
            / "boundary-bridge"
            / "parts"
            / "phase-alpha-eval-matrix"
            / "generated"
            / "phase_alpha_eval_matrix.min.json"
        )
        payload = json.loads(matrix_path.read_text(encoding="utf-8"))
        payload["runs"][0]["required_evals"][0]["eval_anchor"] = "aoa-bounded-change-quality"
        write_json_payload(matrix_path, payload)

        playbooks_root = phase_alpha_playbooks_root_or_skip()
        monkeypatch.setattr(validate_repo, "AOA_PLAYBOOKS_ROOT", playbooks_root)
        monkeypatch.setenv("AOA_PLAYBOOKS_ROOT", str(playbooks_root))
        issues = validate_repo.validate_phase_alpha_eval_matrix(tmp_path)

        assert any(
            issue.location == "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json"
            and "out of date or mismatched" in issue.message
            for issue in issues
        )

    def test_phase_alpha_eval_matrix_rejects_non_bool_optional_rerun(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        make_phase_alpha_eval_matrix_surface(tmp_path)
        playbooks_root = phase_alpha_playbooks_root_or_skip()
        monkeypatch.setenv("AOA_PLAYBOOKS_ROOT", str(playbooks_root))
        example_path = (
            tmp_path
            / "mechanics"
            / "boundary-bridge"
            / "parts"
            / "phase-alpha-eval-matrix"
            / "examples"
            / "phase_alpha_eval_matrix.example.json"
        )
        payload = json.loads(example_path.read_text(encoding="utf-8"))
        payload["runs"][0]["optional_control_path_rerun"] = "false"
        write_json_payload(example_path, payload)
        builder = validate_repo.load_phase_alpha_eval_matrix_builder(tmp_path)

        with pytest.raises(SystemExit, match="optional_control_path_rerun must be a boolean"):
            builder.build_phase_alpha_eval_matrix_payload()

    @pytest.mark.parametrize(
        "observed_at",
        [
            "not-a-date-time",
            "2026-05-17",
            "2026-05-17 12:00:00",
            "2026-05-17T12:00:00",
        ],
    )
    def test_live_receipt_log_enforces_datetime_format(
        self, tmp_path: Path, observed_at: str
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json")
        receipt = json.loads(
            (REPO_ROOT / validate_repo.EVAL_RESULT_RECEIPT_EXAMPLE_NAME).read_text(
                encoding="utf-8"
            )
        )
        receipt["observed_at"] = observed_at
        log_path = tmp_path / ".aoa" / "live_receipts" / "eval-result-receipts.jsonl"
        log_path.parent.mkdir(parents=True)
        log_path.write_text(json.dumps(receipt) + "\n", encoding="utf-8")

        issues = validate_repo.validate_live_receipt_log(tmp_path)

        assert any("date-time" in issue.message for issue in issues)

    @pytest.mark.parametrize("observed_at", ["2026-05-17t12:00:00z", "2026-05-17t12:00:00Z"])
    def test_live_receipt_log_accepts_lowercase_rfc3339_designators(
        self, tmp_path: Path, observed_at: str
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json")
        receipt = json.loads(
            (REPO_ROOT / validate_repo.EVAL_RESULT_RECEIPT_EXAMPLE_NAME).read_text(
                encoding="utf-8"
            )
        )
        receipt["observed_at"] = observed_at
        log_path = tmp_path / ".aoa" / "live_receipts" / "eval-result-receipts.jsonl"
        log_path.parent.mkdir(parents=True)
        log_path.write_text(json.dumps(receipt) + "\n", encoding="utf-8")

        issues = validate_repo.validate_live_receipt_log(tmp_path)

        assert not any("date-time" in issue.message for issue in issues)

    def test_titan_canary_surfaces_validate_current_seed_set(self) -> None:
        assert validate_repo.validate_titan_canary_surfaces(REPO_ROOT) == []

    def test_titan_seed_boundary_part_readme_validates_current_contract(self) -> None:
        assert not any(
            issue.location == validate_repo.TITAN_SEED_BOUNDARY_PART_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_titan_direction_rejects_missing_aoa_agents_owner_boundary(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.TITAN_MECHANIC_DIRECTION_NAME)
        direction_path = tmp_path / validate_repo.TITAN_MECHANIC_DIRECTION_NAME
        direction_path.write_text(
            direction_path.read_text(encoding="utf-8").replace(
                "aoa-agents",
                "Agents-of-Abyss",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.TITAN_MECHANIC_DIRECTION_NAME
            and "aoa-agents" in issue.message
            for issue in issues
        )

    def test_titan_parts_index_readme_keeps_canary_as_payload_form(self) -> None:
        assert not any(
            issue.location == validate_repo.TITAN_PARTS_INDEX_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_titan_parts_index_readme_rejects_canary_named_parts_district(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.TITAN_PARTS_INDEX_README_NAME)
        parts_readme = tmp_path / validate_repo.TITAN_PARTS_INDEX_README_NAME
        parts_readme.write_text(
            parts_readme.read_text(encoding="utf-8").replace(
                "# Titan / Parts Route", "# Titan Canaries Parts"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.TITAN_PARTS_INDEX_README_NAME
            and "# Titan / Parts Route" in issue.message
            for issue in issues
        )

    def test_titan_seed_boundary_part_readme_rejects_missing_owner_split(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.TITAN_SEED_BOUNDARY_PART_README_NAME)
        copy_repo_text(tmp_path, validate_repo.TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        readme_path = tmp_path / validate_repo.TITAN_SEED_BOUNDARY_PART_README_NAME
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Owner Notes"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.TITAN_SEED_BOUNDARY_PART_README_NAME
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_agent_lane_surfaces_validate_current_routes(self) -> None:
        assert validate_repo.validate_agent_lane_surfaces(REPO_ROOT) == []

    def test_legacy_naming_surfaces_validate_current_routes(self) -> None:
        assert validate_repo.validate_legacy_naming_surfaces(REPO_ROOT) == []

    def test_legacy_naming_surfaces_reject_missing_archive_detail_boundary(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        legacy_path = tmp_path / validate_repo.LEGACY_NAMING_NAME
        legacy_path.write_text(
            legacy_path.read_text(encoding="utf-8").replace(
                "archive details",
                "history notes",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.LEGACY_NAMING_NAME
            and "archive details" in issue.message
            for issue in issues
        )

    def test_legacy_naming_single_bridge_language_rejects_index_as_entry(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        legacy_path = tmp_path / validate_repo.LEGACY_NAMING_NAME
        legacy_path.write_text(
            legacy_path.read_text(encoding="utf-8")
            + "\nOld Titan routes enter through `mechanics/titan/PROVENANCE.md` "
            "and `mechanics/titan/legacy/INDEX.md`.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.LEGACY_NAMING_NAME
            and "single controlled bridge" in issue.message
            for issue in issues
        )

    def test_legacy_naming_posture_guide_rejects_direct_mechanic_legacy_index(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        legacy_path = tmp_path / validate_repo.LEGACY_NAMING_NAME
        legacy_path.write_text(
            legacy_path.read_text(encoding="utf-8")
            + "\nOld Titan archive table: `mechanics/titan/legacy/INDEX.md`.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.LEGACY_NAMING_NAME
            and "direct mechanic legacy index paths" in issue.message
            for issue in issues
        )

    def test_legacy_naming_posture_guide_rejects_concrete_legacy_inventory(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        legacy_path = tmp_path / validate_repo.LEGACY_NAMING_NAME
        legacy_path.write_text(
            legacy_path.read_text(encoding="utf-8")
            + "\n## Current Active Owners\n\nWrong parent forms such as `agon-proof`.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.LEGACY_NAMING_NAME
            and "concrete legacy-name inventories" in issue.message
            for issue in issues
        )

    def test_legacy_naming_rejects_external_archive_accounting_detail(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "mechanics/README.md",
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
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

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

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
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        decision_path = "docs/decisions/0082-mechanic-parent-direction-contract.md"
        write_text(
            tmp_path / decision_path,
            (
                "# Direction\n\n"
                "Legacy lookup starts from the active route and then enters "
                "`PROVENANCE.md`, `legacy/INDEX.md`, "
                "`legacy/DISTILLATION_LOG.md`, and `legacy/raw/README.md`.\n"
            ),
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == decision_path
            and "cross only through PROVENANCE.md" in issue.message
            for issue in issues
        )

    def test_legacy_single_bridge_residue_rejects_root_route_card_archive_entry(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        route_card_path = "schemas/README.md"
        write_text(
            tmp_path / route_card_path,
            (
                "# Schemas Route\n\n"
                "Old root schema paths route through `PROVENANCE.md` and "
                "`legacy/INDEX.md`.\n"
            ),
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == route_card_path
            and "cross only through PROVENANCE.md" in issue.message
            for issue in issues
        )

    def test_legacy_single_bridge_residue_rejects_root_route_card_mechanic_archive_entry(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
        ):
            copy_repo_text(tmp_path, path_name)
        route_card_path = "runners/README.md"
        write_text(
            tmp_path / route_card_path,
            (
                "# Shared Runners\n\n"
                "Use `mechanics/proof-infra/PROVENANCE.md` and "
                "`mechanics/proof-infra/legacy/INDEX.md` for old root path lineage.\n"
            ),
        )

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == route_card_path
            and "cross only through PROVENANCE.md" in issue.message
            for issue in issues
        )

    def test_legacy_naming_rejects_external_route_management_wording(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.LEGACY_NAMING_NAME,
            "docs/decisions/0009-legacy-naming-containment.md",
            validate_repo.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            validate_repo.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "docs/decisions/README.md",
            "README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            "CHANGELOG.md",
            "DESIGN.AGENTS.md",
            "mechanics/titan/AGENTS.md",
            "mechanics/proof-object/AGENTS.md",
            "templates/README.md",
        ):
            copy_repo_text(tmp_path, path_name)
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
        proof_object_agents_path = (
            tmp_path / "mechanics" / "proof-object" / "AGENTS.md"
        )
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

        issues = validate_repo.validate_legacy_naming_surfaces(tmp_path)

        assert any(
            issue.location == "ROADMAP.md"
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "DESIGN.AGENTS.md"
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "mechanics/titan/AGENTS.md"
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "mechanics/proof-object/AGENTS.md"
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "templates/README.md"
            and "movement, deletion, or retirement route" in issue.message
            for issue in issues
        )

    def test_architecture_proof_model_contract_validates_current_route(self) -> None:
        assert validate_repo.validate_root_design_surfaces(REPO_ROOT) == []

    def test_architecture_proof_model_contract_rejects_bundle_only_model(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "AGENTS.md",
            "docs/decisions/README.md",
            "docs/decisions/TEMPLATE.md",
            "docs/decisions/AGENTS.md",
            validate_repo.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            validate_repo.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
        ):
            copy_repo_text(tmp_path, path_name)
        architecture_name = "docs/ARCHITECTURE.md"
        write_text(
            tmp_path / architecture_name,
            """
            # Architecture

            `aoa-evals` stores portable eval bundles.

            ## Eval bundles

            Eval bundles package bounded claims, fixtures, scoring, and reports.
            """,
        )

        issues = validate_repo.validate_root_design_surfaces(tmp_path)

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
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "AGENTS.md",
            "docs/ARCHITECTURE.md",
            "docs/decisions/README.md",
            "docs/decisions/TEMPLATE.md",
            "docs/decisions/AGENTS.md",
            validate_repo.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            validate_repo.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
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

        issues = validate_repo.validate_root_design_surfaces(tmp_path)

        assert any(
            issue.location == "DESIGN.md"
            and "active mechanic authority" in issue.message
            and "mechanic-ready" in issue.message
            for issue in issues
        )

    def test_design_agents_rejects_future_mechanic_package_wording(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "AGENTS.md",
            "docs/ARCHITECTURE.md",
            "docs/decisions/README.md",
            "docs/decisions/TEMPLATE.md",
            "docs/decisions/AGENTS.md",
            validate_repo.ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            validate_repo.ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
        ):
            copy_repo_text(tmp_path, path_name)
        design_agents_path = tmp_path / validate_repo.DESIGN_AGENTS_NAME
        design_agents_path.write_text(
            design_agents_path.read_text(encoding="utf-8").replace(
                "Active mechanic packages", "Future mechanic packages"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_design_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.DESIGN_AGENTS_NAME
            and "active mechanic packages" in issue.message
            and "Future mechanic packages" in issue.message
            for issue in issues
        )

    def test_proof_topology_rejects_preparatory_mechanic_wording(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.PROOF_TOPOLOGY_NAME,
            "docs/decisions/0005-proof-topology-map.md",
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)
        topology_path = tmp_path / validate_repo.PROOF_TOPOLOGY_NAME
        topology_path.write_text(
            topology_path.read_text(encoding="utf-8").replace(
                "mechanic operations apart",
                "mechanic-ready operations apart",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_proof_topology_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.PROOF_TOPOLOGY_NAME
            and "active mechanics" in issue.message
            and "mechanic-ready operations" in issue.message
            for issue in issues
        )

    def test_proof_topology_decision_rejects_deferred_movement_wording(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.PROOF_TOPOLOGY_NAME,
            "docs/decisions/0005-proof-topology-map.md",
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)
        decision_path = tmp_path / "docs" / "decisions" / "0005-proof-topology-map.md"
        decision_path.write_text(
            decision_path.read_text(encoding="utf-8")
            + "\nKeep physical movement deferred until a later phase.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_proof_topology_surfaces(tmp_path)

        assert any(
            issue.location == "docs/decisions/0005-proof-topology-map.md"
            and "active mechanics atlas" in issue.message
            and "Keep physical movement deferred" in issue.message
            for issue in issues
        )

    def test_proof_topology_rejects_roadmap_preparatory_mechanic_wording(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.PROOF_TOPOLOGY_NAME,
            "docs/decisions/0005-proof-topology-map.md",
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)
        roadmap_path = tmp_path / "ROADMAP.md"
        roadmap_path.write_text(
            roadmap_path.read_text(encoding="utf-8")
            + "\nGoal: classify mechanic-ready artifact classes before movement.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_proof_topology_surfaces(tmp_path)

        assert any(
            issue.location == "ROADMAP.md"
            and "active mechanics direction" in issue.message
            and "mechanic-ready artifact classes" in issue.message
            for issue in issues
        )

    def test_agent_index_surface_validates_current_route(self) -> None:
        assert validate_repo.validate_agent_index_surface(REPO_ROOT) == []

    def test_agent_index_surface_rejects_missing_chain(self, tmp_path: Path) -> None:
        for path_name in (
            validate_repo.AGENT_INDEX_NAME,
            validate_repo.AGENT_INDEX_CHAIN_DECISION_NAME,
            "README.md",
            "docs/README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
            validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME,
            "docs/decisions/README.md",
        ):
            copy_repo_text(tmp_path, path_name)
        index_path = tmp_path / validate_repo.AGENT_INDEX_NAME
        index_path.write_text(
            index_path.read_text(encoding="utf-8").replace(
                "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
                "repo -> file",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_agent_index_surface(tmp_path)

        assert any(
            issue.location == validate_repo.AGENT_INDEX_NAME
            and "repo -> authority class -> operation" in issue.message
            for issue in issues
        )

    def test_root_readme_surface_role_validates_current_entry(self) -> None:
        assert validate_repo.validate_root_readme_surface_role(REPO_ROOT) == []

    def test_root_readme_surface_role_rejects_generic_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in ("README.md", "docs/README.md"):
            copy_repo_text(tmp_path, path_name)
        readme_path = tmp_path / "README.md"
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "# aoa-evals Bounded Proof Canon",
                "# aoa-evals",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_readme_surface_role(tmp_path)

        assert any(
            issue.location == "README.md"
            and "# aoa-evals Bounded Proof Canon" in issue.message
            for issue in issues
        )

    def test_root_readme_surface_role_rejects_generic_docs_map_eval_labels(
        self, tmp_path: Path
    ) -> None:
        for path_name in ("README.md", "docs/README.md"):
            copy_repo_text(tmp_path, path_name)
        docs_readme_path = tmp_path / "docs" / "README.md"
        docs_readme_path.write_text(
            docs_readme_path.read_text(encoding="utf-8").replace(
                "Eval Bundle Selection Chooser",
                "EVAL_SELECTION",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_readme_surface_role(tmp_path)

        assert any(
            issue.location == "docs/README.md"
            and "Eval Bundle Selection Chooser" in issue.message
            for issue in issues
        )

    def test_docs_readme_route_map_validates_current_map(self) -> None:
        assert validate_repo.validate_docs_readme_route_map(REPO_ROOT) == []

    def test_docs_readme_route_map_rejects_generic_mechanics_label(
        self, tmp_path: Path
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

        issues = validate_repo.validate_docs_readme_route_map(tmp_path)

        assert any(
            issue.location == "docs/README.md"
            and "Mechanics Operation Atlas" in issue.message
            for issue in issues
        )

    def test_docs_readme_route_map_rejects_validation_block_in_reader_paths(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "docs/README.md")
        docs_readme_path = tmp_path / "docs" / "README.md"
        docs_readme_path.write_text(
            docs_readme_path.read_text(encoding="utf-8").replace(
                "### Reviewer Path",
                "## Verify Current Surfaces\n\nUse docs/AGENTS.md.\n\n### Reviewer Path",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_docs_readme_route_map(tmp_path)

        assert any(
            issue.location == "docs/README.md"
            and "Verify Current Surfaces" in issue.message
            for issue in issues
        )

    def test_docs_readme_route_map_rejects_command_block(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "docs/README.md")
        docs_readme_path = tmp_path / "docs" / "README.md"
        docs_readme_path.write_text(
            docs_readme_path.read_text(encoding="utf-8")
            + "\n```bash\npython scripts/validate_repo.py\n```\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_docs_readme_route_map(tmp_path)

        assert any(
            issue.location == "docs/README.md"
            and "executable validation commands" in issue.message
            for issue in issues
        )

    def test_read_model_command_ownership_validates_current_routes(self) -> None:
        assert validate_repo.validate_read_model_command_ownership(REPO_ROOT) == []

    def test_read_model_command_ownership_rejects_command_block(
        self, tmp_path: Path
    ) -> None:
        readme_name = "docs/PROOF_TOPOLOGY.md"
        write_text(
            tmp_path / readme_name,
            """
            # Proof Topology

            ## Validation

            ```bash
            python scripts/validate_repo.py
            ```
            """,
        )

        issues = validate_repo.validate_read_model_command_ownership(tmp_path)

        assert any(
            issue.location == readme_name
            and "route executable validation commands to the nearest AGENTS.md"
            in issue.message
            for issue in issues
        )

    def test_read_model_command_ownership_rejects_bullet_command(
        self, tmp_path: Path
    ) -> None:
        readme_name = "docs/RELEASING.md"
        write_text(
            tmp_path / readme_name,
            """
            # Releasing

            ## Local release checks

            - `python scripts/release_check.py`
            """,
        )

        issues = validate_repo.validate_read_model_command_ownership(tmp_path)

        assert any(
            issue.location == readme_name
            and "python command lines" in issue.message
            for issue in issues
        )

    def test_audit_surface_role_validates_current_route(self) -> None:
        assert validate_repo.validate_audit_surface_role(REPO_ROOT) == []

    def test_audit_surface_role_rejects_audit_as_route_law(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "AGENTS.md")
        write_text(
            tmp_path / "AUDIT.md",
            "# AUDIT.md\n\nThis file is the repo-local audit contract.\n",
        )

        issues = validate_repo.validate_audit_surface_role(tmp_path)

        assert any(
            issue.location == "AUDIT.md"
            and "Audit Surface Map" in issue.message
            for issue in issues
        )

    def test_audit_surface_role_rejects_missing_agents_audit_route(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "AUDIT.md")
        write_text(
            tmp_path / "AGENTS.md",
            "# AGENTS.md\n\n## Verify\n\nUse local validation.\n",
        )

        issues = validate_repo.validate_audit_surface_role(tmp_path)

        assert any(
            issue.location == "AGENTS.md"
            and "## Audit and review route" in issue.message
            for issue in issues
        )

    def test_index_surface_roles_validate_current_headings(self) -> None:
        assert validate_repo.validate_index_surface_roles(REPO_ROOT) == []

    def test_index_surface_roles_reject_generic_decision_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
            copy_repo_text(tmp_path, path_name)
        decision_index_path = tmp_path / "docs" / "decisions" / "README.md"
        decision_index_path.write_text(
            decision_index_path.read_text(encoding="utf-8").replace(
                "# Decision Records Index",
                "# Decisions",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_index_surface_roles(tmp_path)

        assert any(
            issue.location == "docs/decisions/README.md"
            and "# Decision Records Index" in issue.message
            for issue in issues
        )

    def test_index_surface_roles_reject_generic_mechanics_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
            copy_repo_text(tmp_path, path_name)
        mechanics_index_path = tmp_path / "mechanics" / "README.md"
        mechanics_index_path.write_text(
            mechanics_index_path.read_text(encoding="utf-8").replace(
                "# Mechanics Operation Atlas",
                "# Mechanics",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_index_surface_roles(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_README_NAME
            and "# Mechanics Operation Atlas" in issue.message
            for issue in issues
        )

    def test_index_surface_roles_reject_generic_eval_index_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.INDEX_SURFACE_ROLE_REQUIRED_TOKENS:
            copy_repo_text(tmp_path, path_name)
        eval_index_path = tmp_path / validate_repo.EVAL_INDEX_NAME
        eval_index_path.write_text(
            eval_index_path.read_text(encoding="utf-8").replace(
                "# Eval Bundle Index",
                "# EVAL_INDEX",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_index_surface_roles(tmp_path)

        assert any(
            issue.location == validate_repo.EVAL_INDEX_NAME
            and "# Eval Bundle Index" in issue.message
            for issue in issues
        )

    def test_mechanic_index_surface_roles_validate_current_headings(self) -> None:
        assert validate_repo.validate_mechanic_index_surface_roles(REPO_ROOT) == []

    def test_mechanic_index_surface_roles_reject_generic_parts_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            "mechanics/proof-object/PARTS.md",
            "mechanics/proof-object/parts/README.md",
        ):
            copy_repo_text(tmp_path, path_name)
        parts_index_path = tmp_path / "mechanics" / "proof-object" / "PARTS.md"
        parts_index_path.write_text(
            parts_index_path.read_text(encoding="utf-8").replace(
                "# Proof Object / Part Index",
                "# Proof Object Parts",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_index_surface_roles(tmp_path)

        assert any(
            issue.location == "mechanics/proof-object/PARTS.md"
            and "Index" in issue.message
            for issue in issues
        )

    def test_mechanic_index_surface_roles_reject_generic_parts_route_heading(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            "mechanics/proof-object/PARTS.md",
            "mechanics/proof-object/parts/README.md",
        ):
            copy_repo_text(tmp_path, path_name)
        parts_route_path = tmp_path / "mechanics" / "proof-object" / "parts" / "README.md"
        parts_route_path.write_text(
            parts_route_path.read_text(encoding="utf-8").replace(
                "# Proof Object / Parts Route",
                "# Proof Object Parts",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_index_surface_roles(tmp_path)

        assert any(
            issue.location == "mechanics/proof-object/parts/README.md"
            and "Route" in issue.message
            for issue in issues
        )

    def test_validator_surface_role_validates_current_route(self) -> None:
        assert validate_repo.validate_validator_surface_role(REPO_ROOT) == []

    def test_validator_surface_role_rejects_generic_scripts_guidance(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "scripts" / "AGENTS.md",
            "# AGENTS.md\n\nScripts are helper utilities.\n",
        )
        copy_repo_text(tmp_path, "tests/AGENTS.md")

        issues = validate_repo.validate_validator_surface_role(tmp_path)

        assert any(
            issue.location == "scripts/AGENTS.md"
            and "root contract mesh" in issue.message
            for issue in issues
        )

    def test_validator_surface_role_rejects_generic_test_guidance(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "scripts/AGENTS.md")
        write_text(
            tmp_path / "tests" / "AGENTS.md",
            "# AGENTS.md\n\nTests cover helpers.\n",
        )

        issues = validate_repo.validate_validator_surface_role(tmp_path)

        assert any(
            issue.location == "tests/AGENTS.md"
            and "root validator regression mesh" in issue.message
            for issue in issues
        )

    def test_root_route_card_districts_validate_current_routes(self) -> None:
        assert validate_repo.validate_root_route_card_districts(REPO_ROOT) == []

    def test_root_route_card_districts_cover_expected_roots(self) -> None:
        assert set(validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS) == {
            "config",
            "examples",
            "fixtures",
            "manifests",
            "reports",
            "runners",
            "schemas",
            "scorers",
            "templates",
        }

    def test_root_route_card_districts_reject_active_payload(self, tmp_path: Path) -> None:
        for district_name, allowed_names in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
            for allowed_name in allowed_names:
                copy_repo_text(tmp_path, f"{district_name}/{allowed_name}")
        copy_repo_text(tmp_path, validate_repo.ROOT_ROUTE_CARD_GUARD_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        for district_name in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS:
            write_text(tmp_path / district_name / "stray" / "payload.txt", "stray\n")

        issues = validate_repo.validate_root_route_card_districts(tmp_path)

        for district_name in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS:
            assert any(
                issue.location == f"{district_name}/stray/payload.txt"
                and "route-card-only root district" in issue.message
                for issue in issues
            )

    def test_root_route_card_districts_reject_stray_empty_directory(
        self, tmp_path: Path
    ) -> None:
        for district_name, allowed_names in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
            for allowed_name in allowed_names:
                copy_repo_text(tmp_path, f"{district_name}/{allowed_name}")
        copy_repo_text(tmp_path, validate_repo.ROOT_ROUTE_CARD_GUARD_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        stray_path = tmp_path / "manifests" / "recurrence" / "hooks"
        stray_path.mkdir(parents=True)

        issues = validate_repo.validate_root_route_card_districts(tmp_path)

        assert any(
            issue.location == "manifests/recurrence"
            and "stray directory" in issue.message
            for issue in issues
        )

    def test_root_route_card_districts_reject_unclear_readme_heading(
        self, tmp_path: Path
    ) -> None:
        for district_name, allowed_names in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
            for allowed_name in allowed_names:
                copy_repo_text(tmp_path, f"{district_name}/{allowed_name}")
        copy_repo_text(tmp_path, validate_repo.ROOT_ROUTE_CARD_GUARD_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        fixtures_readme = tmp_path / "fixtures" / "README.md"
        fixtures_readme.write_text(
            fixtures_readme.read_text(encoding="utf-8").replace(
                "# Fixtures Route",
                "# Shared Fixtures",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_route_card_districts(tmp_path)

        assert any(
            issue.location == "fixtures/README.md"
            and "must name itself as a Route surface" in issue.message
            for issue in issues
        )

    def test_root_route_card_districts_reject_readme_operational_discipline(
        self, tmp_path: Path
    ) -> None:
        for district_name, allowed_names in validate_repo.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
            for allowed_name in allowed_names:
                copy_repo_text(tmp_path, f"{district_name}/{allowed_name}")
        copy_repo_text(tmp_path, validate_repo.ROOT_ROUTE_CARD_GUARD_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        runners_readme = tmp_path / "runners" / "README.md"
        runners_readme.write_text(
            runners_readme.read_text(encoding="utf-8")
            + "\nDo not recreate active root runner payloads here.\n",
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_route_card_districts(tmp_path)

        assert any(
            issue.location == "runners/README.md"
            and "operational discipline in AGENTS.md" in issue.message
            for issue in issues
        )

    def test_active_mechanic_route_residue_validates_current_route_cards(self) -> None:
        assert validate_repo.validate_active_mechanic_route_residue(REPO_ROOT) == []

    def test_active_mechanic_route_residue_rejects_root_payload_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "mechanics" / "proof-infra" / "README.md",
            "# Proof Infra\n\nUse `fixtures/old-family/README.md` as active input.\n",
        )

        issues = validate_repo.validate_active_mechanic_route_residue(tmp_path)

        assert any(
            issue.location == "mechanics/proof-infra/README.md:3"
            and "route-card-only root district payload 'fixtures/old-family/README.md'"
            in issue.message
            for issue in issues
        )

    def test_active_mechanic_route_residue_allows_root_route_card_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "mechanics" / "proof-infra" / "README.md",
            "# Proof Infra\n\nSee root route card `fixtures/README.md`.\n",
        )

        assert validate_repo.validate_active_mechanic_route_residue(tmp_path) == []

    def test_active_mechanic_route_residue_allows_same_part_root_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "audit"
            / "parts"
            / "artifact-verdict-hooks"
            / "examples"
            / "hook.example.json",
            "{}",
        )
        write_text(
            tmp_path
            / "mechanics"
            / "audit"
            / "parts"
            / "artifact-verdict-hooks"
            / "README.md",
            "# Artifact Verdict Hooks\n\nUse `examples/hook.example.json` locally.\n",
        )

        assert validate_repo.validate_active_mechanic_route_residue(tmp_path) == []

    def test_active_mechanic_route_residue_rejects_legacy_parent_route(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "mechanics" / "titan" / "README.md",
            "# Titan\n\nDo not route through `mechanics/titan-canaries/README.md`.\n",
        )

        issues = validate_repo.validate_active_mechanic_route_residue(tmp_path)

        assert any(
            issue.location == "mechanics/titan/README.md:3"
            and "not legacy parent route `mechanics/titan-canaries/`"
            in issue.message
            for issue in issues
        )

    def test_root_authored_route_residue_validates_current_route_cards(self) -> None:
        assert validate_repo.validate_root_authored_route_residue(REPO_ROOT) == []

    def test_root_authored_route_residue_rejects_root_payload_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "AUDIT.md",
            "# Audit\n\nRead `reports/summary.schema.json` before review.\n",
        )

        issues = validate_repo.validate_root_authored_route_residue(tmp_path)

        assert any(
            issue.location == "AUDIT.md:3"
            and "route-card-only root district payload 'reports/summary.schema.json'"
            in issue.message
            for issue in issues
        )

    def test_root_authored_route_residue_allows_bundle_local_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "AUDIT.md",
            "# Audit\n\nRead `evals/workflow/aoa-demo/reports/summary.schema.json`.\n",
        )

        assert validate_repo.validate_root_authored_route_residue(tmp_path) == []

    def test_root_authored_route_residue_allows_root_route_card_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "RELEASING.md",
            "# Releasing\n\nRead route card `reports/README.md`.\n",
        )

        assert validate_repo.validate_root_authored_route_residue(tmp_path) == []

    def test_root_authored_route_residue_allows_historical_context(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "LEGACY_NAMING.md",
            "# Legacy\n\nFormer root paths `reports/old.json` are mapped through provenance.\n",
        )

        assert validate_repo.validate_root_authored_route_residue(tmp_path) == []

    def test_decision_route_residue_validates_current_decisions(self) -> None:
        assert validate_repo.validate_decision_route_residue(REPO_ROOT) == []

    def test_decision_route_residue_rejects_unmarked_root_payload_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "decisions" / "0099-bad-route.md",
            "# Bad Route\n\nUse `reports/summary.schema.json` as the active schema.\n",
        )

        issues = validate_repo.validate_decision_route_residue(tmp_path)

        assert any(
            issue.location == "docs/decisions/0099-bad-route.md:3"
            and "route-card-only root district payload 'reports/summary.schema.json'"
            in issue.message
            for issue in issues
        )

    def test_decision_route_residue_allows_historical_root_payload_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "decisions" / "0099-former-route.md",
            "# Former Route\n\nFormer root `reports/summary.schema.json` moved behind provenance.\n",
        )

        assert validate_repo.validate_decision_route_residue(tmp_path) == []

    def test_decision_route_residue_allows_bundle_local_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "decisions" / "0099-bundle-route.md",
            "# Bundle Route\n\nUse `evals/workflow/aoa-demo/reports/summary.schema.json`.\n",
        )

        assert validate_repo.validate_decision_route_residue(tmp_path) == []

    def test_decision_route_residue_allows_root_route_card_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "docs" / "decisions" / "0099-route-card.md",
            "# Route Card\n\nRead route card `reports/README.md`.\n",
        )

        assert validate_repo.validate_decision_route_residue(tmp_path) == []

    def test_repo_config_route_residue_validates_current_config(self) -> None:
        assert validate_repo.validate_repo_config_route_residue(REPO_ROOT) == []

    def test_repo_config_route_residue_rejects_legacy_parent_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / ".gitignore",
            "seeds/\n!mechanics/titan-canaries/seeds/\n",
        )

        issues = validate_repo.validate_repo_config_route_residue(tmp_path)

        assert any(
            issue.location == ".gitignore:2"
            and "legacy mechanic parent `mechanics/titan-canaries/`"
            in issue.message
            for issue in issues
        )

    def test_repo_config_route_residue_rejects_root_payload_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / ".github" / "workflows" / "bad.yml",
            "name: bad\n# uses reports/summary.schema.json\n",
        )

        issues = validate_repo.validate_repo_config_route_residue(tmp_path)

        assert any(
            issue.location == ".github/workflows/bad.yml:2"
            and "route-card-only root district payload 'reports/summary.schema.json'"
            in issue.message
            for issue in issues
        )

    def test_repo_config_route_residue_allows_current_seed_boundary_unignore(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / ".gitignore",
            "seeds/\n!mechanics/titan/parts/seed-boundary/seeds/\n",
        )

        assert validate_repo.validate_repo_config_route_residue(tmp_path) == []

    def test_source_bundle_route_residue_validates_current_bundles(self) -> None:
        assert validate_repo.validate_source_bundle_route_residue(REPO_ROOT) == []

    def test_source_bundle_route_residue_rejects_unqualified_external_path(
        self, tmp_path: Path
    ) -> None:
        write_text(
            eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
            "# Demo\n\nRead `examples/a2a/external.fixture.json` from aoa-sdk.\n",
        )

        issues = validate_repo.validate_source_bundle_route_residue(tmp_path)

        assert any(
            issue.location == "evals/workflow/aoa-demo/EVAL.md:3"
            and "route-card-only root district payload 'examples/a2a/external.fixture.json'"
            in issue.message
            for issue in issues
        )

    def test_source_bundle_route_residue_rejects_legacy_parent_reference(
        self, tmp_path: Path
    ) -> None:
        write_text(
            eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
            "# Demo\n\nUse `mechanics/agon-proof/README.md` as the owner.\n",
        )

        issues = validate_repo.validate_source_bundle_route_residue(tmp_path)

        assert any(
            issue.location == "evals/workflow/aoa-demo/EVAL.md:3"
            and "legacy mechanic parent `mechanics/agon-proof/`" in issue.message
            for issue in issues
        )

    def test_source_bundle_route_residue_allows_bundle_local_path(
        self, tmp_path: Path
    ) -> None:
        write_text(eval_dir_for_test(tmp_path, "aoa-demo") / "fixtures" / "contract.json", "{}")
        write_text(
            eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
            "# Demo\n\nUse `fixtures/contract.json` as this bundle's local fixture contract.\n",
        )

        assert validate_repo.validate_source_bundle_route_residue(tmp_path) == []

    def test_source_bundle_route_residue_allows_repo_qualified_sibling_path(
        self, tmp_path: Path
    ) -> None:
        write_text(
            eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
            "# Demo\n\nUse `repo:aoa-sdk/examples/a2a/external.fixture.json` as sibling evidence.\n",
        )

        assert validate_repo.validate_source_bundle_route_residue(tmp_path) == []

    def test_mechanic_payload_route_residue_validates_current_payloads(self) -> None:
        assert validate_repo.validate_mechanic_payload_route_residue(REPO_ROOT) == []

    def test_mechanic_payload_route_residue_rejects_unqualified_external_path(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "recurrence"
            / "parts"
            / "recursor-boundary"
            / "fixtures"
            / "case.json",
            '{\n  "must_not_modify": [\n    "config/codex_subagent_wiring.v2.json"\n  ]\n}\n',
        )

        issues = validate_repo.validate_mechanic_payload_route_residue(tmp_path)

        assert any(
            issue.location
            == "mechanics/recurrence/parts/recursor-boundary/fixtures/case.json:3"
            and "route-card-only root district payload 'config/codex_subagent_wiring.v2.json'"
            in issue.message
            for issue in issues
        )

    def test_mechanic_payload_route_residue_allows_part_local_path(
        self, tmp_path: Path
    ) -> None:
        part_root = (
            tmp_path
            / "mechanics"
            / "recurrence"
            / "parts"
            / "recursor-boundary"
        )
        write_text(part_root / "config" / "local.json", "{}")
        write_text(
            part_root / "fixtures" / "case.json",
            '{\n  "local_config": "config/local.json"\n}\n',
        )

        assert validate_repo.validate_mechanic_payload_route_residue(tmp_path) == []

    def test_mechanic_payload_route_residue_allows_repo_qualified_sibling_path(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "recurrence"
            / "parts"
            / "recursor-boundary"
            / "fixtures"
            / "case.json",
            '{\n  "source": "repo:aoa-agents/config/codex_subagent_wiring.v2.json"\n}\n',
        )

        assert validate_repo.validate_mechanic_payload_route_residue(tmp_path) == []

    def test_mechanic_payload_route_residue_rejects_legacy_parent_route(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "recurrence"
            / "parts"
            / "recursor-boundary"
            / "fixtures"
            / "case.json",
            '{\n  "owner": "mechanics/titan-canaries/seeds/titan_runtime_roster_canary.yaml"\n}\n',
        )

        issues = validate_repo.validate_mechanic_payload_route_residue(tmp_path)

        assert any(
            issue.location
            == "mechanics/recurrence/parts/recursor-boundary/fixtures/case.json:2"
            and "legacy mechanic parent `mechanics/titan-canaries/`"
            in issue.message
            for issue in issues
        )

    def test_mechanic_manifest_path_globs_reject_unresolved_root_docs_glob(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "court-prebinding"
            / "manifests"
            / "recurrence"
            / "component.demo.json",
            '{\n  "observation_inputs": [\n    {"path_globs": ["docs/AGON_*.md"]}\n  ]\n}\n',
        )

        issues = validate_repo.validate_mechanic_manifest_path_glob_routes(tmp_path)

        assert any(
            issue.location
            == "mechanics/agon/parts/court-prebinding/manifests/recurrence/component.demo.json"
            and "unresolved root-authored docs globs" in issue.message
            for issue in issues
        )

    def test_mechanic_manifest_route_fields_reject_root_schema_payload(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "sophian-threshold-alignment"
            / "manifests"
            / "recurrence"
            / "component.demo.json",
            '{\n  "observed_surfaces": [\n    "schemas/agon-sophian-eval-alignment.schema.json"\n  ]\n}\n',
        )

        issues = validate_repo.validate_mechanic_manifest_path_glob_routes(tmp_path)

        assert any(
            issue.location
            == "mechanics/agon/parts/sophian-threshold-alignment/manifests/recurrence/component.demo.json"
            and "route-card-only root district payload `schemas/agon-sophian-eval-alignment.schema.json`"
            in issue.message
            for issue in issues
        )

    def test_repo_validation_workflow_surface_validates_current_pin(self) -> None:
        assert validate_repo.validate_repo_validation_workflow_surface(REPO_ROOT) == []

    def test_repo_validation_workflow_rejects_stale_aoa_memo_pin(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, ".github/workflows/repo-validation.yml")
        workflow_path = tmp_path / ".github" / "workflows" / "repo-validation.yml"
        workflow_path.write_text(
            workflow_path.read_text(encoding="utf-8").replace(
                validate_repo.REPO_VALIDATION_AOA_MEMO_REF,
                "4fec12fb54a5a332587139000a6a98a4c76357bd",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_repo_validation_workflow_surface(tmp_path)

        assert any(
            issue.location == ".github/workflows/repo-validation.yml"
            and "aoa-memo checkout ref must be" in issue.message
            for issue in issues
        )

    def test_proof_loop_mechanic_surfaces_validate_current_routes(self) -> None:
        assert not any(
            issue.location.startswith("mechanics/proof-loop/")
            or issue.location == "docs/decisions/0019-proof-loop-mechanic-package.md"
            or issue.location == "docs/decisions/0020-proof-loop-local-smoke-report.md"
            or issue.location == "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md"
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_proof_loop_route_smoke_part_readme_validates_current_contract(self) -> None:
        assert not any(
            issue.location == validate_repo.PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_recurrence_mechanic_surfaces_validate_current_routes(self) -> None:
        assert not any(
            issue.location.startswith("mechanics/recurrence/")
            or issue.location == validate_repo.RECURRENCE_MECHANIC_DECISION_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_checkpoint_mechanic_surfaces_validate_current_routes(self) -> None:
        assert not any(
            issue.location.startswith("mechanics/checkpoint/")
            or issue.location == validate_repo.CHECKPOINT_MECHANIC_DECISION_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_experience_mechanic_surfaces_validate_current_routes(self) -> None:
        assert not any(
            issue.location.startswith("mechanics/experience/")
            or issue.location == validate_repo.EXPERIENCE_MECHANIC_DECISION_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_distillation_mechanic_surfaces_validate_current_routes(self) -> None:
        assert not any(
            issue.location.startswith("mechanics/distillation/")
            or issue.location == validate_repo.DISTILLATION_MECHANIC_DECISION_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_audit_and_release_support_provenance_validate_current_routes(self) -> None:
        protected_locations = {
            validate_repo.AUDIT_MECHANIC_PROVENANCE_NAME,
            validate_repo.AUDIT_LEGACY_INDEX_NAME,
            validate_repo.AUDIT_LEGACY_DISTILLATION_LOG_NAME,
            validate_repo.AUDIT_LEGACY_RAW_README_NAME,
            validate_repo.RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME,
            validate_repo.RELEASE_SUPPORT_LEGACY_INDEX_NAME,
            validate_repo.RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME,
            validate_repo.RELEASE_SUPPORT_LEGACY_RAW_README_NAME,
            validate_repo.PROOF_LOOP_MECHANIC_PROVENANCE_NAME,
            validate_repo.PROOF_LOOP_LEGACY_INDEX_NAME,
            validate_repo.PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME,
            validate_repo.PROOF_LOOP_LEGACY_RAW_README_NAME,
            validate_repo.PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME,
            validate_repo.PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME,
            validate_repo.PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME,
            validate_repo.PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME,
            validate_repo.BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_NAME,
            validate_repo.BOUNDARY_BRIDGE_LEGACY_INDEX_NAME,
            validate_repo.BOUNDARY_BRIDGE_LEGACY_DISTILLATION_LOG_NAME,
            validate_repo.BOUNDARY_BRIDGE_LEGACY_RAW_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_audit_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.AUDIT_SELECTED_EVIDENCE_PART_README_NAME,
            validate_repo.AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
            validate_repo.AUDIT_CANDIDATE_READERS_PART_README_NAME,
            validate_repo.AUDIT_INTEGRITY_REVIEW_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_agon_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            path_name
            for path_name, _tokens in validate_repo.AGON_PART_README_CONTRACTS
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_boundary_bridge_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME,
            validate_repo.BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_README_NAME,
            validate_repo.BOUNDARY_BRIDGE_ORCHESTRATOR_PROOF_ANCHORS_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_publication_receipts_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME,
            validate_repo.PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME,
            validate_repo.PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME,
            validate_repo.PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_release_support_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
            validate_repo.RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
            validate_repo.RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_comparison_spine_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.COMPARISON_SPINE_OVERVIEW_PART_README_NAME,
            validate_repo.COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME,
            validate_repo.COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME,
            validate_repo.COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_antifragility_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.ANTIFRAGILITY_POSTURE_PART_README_NAME,
            validate_repo.ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME,
            validate_repo.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_checkpoint_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.CHECKPOINT_A2A_PART_README_NAME,
            validate_repo.CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME,
            validate_repo.CHECKPOINT_SELF_AGENT_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_experience_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.EXPERIENCE_PROTOCOL_PART_README_NAME,
            validate_repo.EXPERIENCE_CERTIFICATION_PART_README_NAME,
            validate_repo.EXPERIENCE_ADOPTION_PART_README_NAME,
            validate_repo.EXPERIENCE_GOVERNANCE_PART_README_NAME,
            validate_repo.EXPERIENCE_OFFICE_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_distillation_part_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME,
            validate_repo.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_method_growth_part_owner_split_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME,
            validate_repo.METHOD_GROWTH_OWNER_LANDING_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_proof_object_part_owner_split_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME,
            validate_repo.PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_questbook_part_owner_split_readmes_validate_current_contracts(self) -> None:
        protected_locations = {
            validate_repo.QUESTBOOK_SOURCE_RECORD_PART_README_NAME,
            validate_repo.QUESTBOOK_DISPATCH_READER_PART_README_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_growth_cycle_diagnosis_gate_readme_validates_current_contract(self) -> None:
        assert not any(
            issue.location == validate_repo.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_repair_diagnosis_route_boundary_validates_current_contract(self) -> None:
        protected_locations = {
            validate_repo.ANTIFRAGILITY_MECHANIC_README_NAME,
            validate_repo.ANTIFRAGILITY_MECHANIC_PARTS_NAME,
            validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME,
            validate_repo.REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
        }

        assert not any(
            issue.location in protected_locations
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_recurrence_control_plane_readme_validates_current_contract(self) -> None:
        assert not any(
            issue.location == validate_repo.RECURRENCE_CONTROL_PLANE_PART_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_rpg_progression_unlocks_readme_validates_current_contract(self) -> None:
        assert not any(
            issue.location == validate_repo.RPG_PROGRESS_UNLOCKS_PART_README_NAME
            for issue in validate_repo.validate_mechanics_surfaces(REPO_ROOT)
        )

    def test_mechanic_parent_allowlist_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanics_parent_allowlist(REPO_ROOT) == []

    def test_mechanic_parent_guidance_boundary_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_parent_guidance_boundary(REPO_ROOT) == []

    def test_mechanic_parent_guidance_boundary_rejects_unowned_parent_docs(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
            f"""
            # Mechanic Parent Guidance Boundary

            `mechanics/<parent>/docs/`
            mechanic-wide guidance
            part-owned payload
            allowlisted
            unallowlisted parent-level docs
            Titan canary guides
            {validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND}
            """,
        )
        write_text(
            tmp_path / "docs" / "decisions" / "README.md",
            f"{validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME}\nMechanic Parent Guidance Boundary\n",
        )
        write_text(
            tmp_path / validate_repo.MECHANICS_README_NAME,
            "parent-level `docs/`\npart-owned payload\n",
        )
        write_text(
            tmp_path / "mechanics" / "titan" / "docs" / "TITAN_INCARNATION_CANARIES.md",
            "# Wrong parent docs\n",
        )

        issues = validate_repo.validate_mechanic_parent_guidance_boundary(tmp_path)

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
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
            f"""
            # Mechanic Parent Guidance Boundary

            `mechanics/<parent>/docs/`
            mechanic-wide guidance
            part-owned payload
            allowlisted
            unallowlisted parent-level docs
            Titan canary guides
            {validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND}
            """,
        )
        write_text(
            tmp_path / "docs" / "decisions" / "README.md",
            f"{validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME}\nMechanic Parent Guidance Boundary\n",
        )
        write_text(
            tmp_path / validate_repo.MECHANICS_README_NAME,
            "parent-level `docs/`\npart-owned payload\n",
        )
        (tmp_path / "mechanics" / "checkpoint" / "docs").mkdir(parents=True)

        issues = validate_repo.validate_mechanic_parent_guidance_boundary(tmp_path)

        assert any(
            issue.location == "mechanics/checkpoint/docs"
            and "empty parent-level docs/" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_guidance_boundary_rejects_thin_allowlisted_doc(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_README_NAME)
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "docs"
            / "AGON_EVAL_OWNER_HANDOFFS.md",
            "# Agon Eval Owner Handoffs\n\nToo thin.\n",
        )
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "docs"
            / "AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md",
            "\n".join(validate_repo.MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS),
        )
        write_text(
            tmp_path
            / "mechanics"
            / "recurrence"
            / "docs"
            / "RECURRENCE_PROOF_PROGRAM.md",
            "\n".join(validate_repo.MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS),
        )

        issues = validate_repo.validate_mechanic_parent_guidance_boundary(tmp_path)

        assert any(
            issue.location
            == "mechanics/agon/docs/AGON_EVAL_OWNER_HANDOFFS.md"
            and "parent guidance content contract" in issue.message
            and "## Source Surfaces" in issue.message
            for issue in issues
        )

    def test_mechanic_part_contract_files_cover_allowed_parents(self) -> None:
        expected = {
            f"mechanics/{parent_name}/PARTS.md"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        }

        assert set(validate_repo.MECHANIC_PART_CONTRACT_FILES) == expected

    def test_mechanic_direction_files_cover_allowed_parents(self) -> None:
        expected = {
            f"mechanics/{parent_name}/DIRECTION.md"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        }

        assert set(validate_repo.MECHANIC_DIRECTION_FILES) == expected

    def test_mechanic_route_card_files_cover_direction_route(self) -> None:
        expected = {
            f"mechanics/{parent_name}/{filename}"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
            for filename in ("AGENTS.md", "README.md", "DIRECTION.md", "PARTS.md")
        }

        assert set(validate_repo.MECHANIC_ROUTE_CARD_FILES) == expected

    def test_mechanic_parent_readme_and_agents_files_cover_allowed_parents(self) -> None:
        expected_readmes = {
            f"mechanics/{parent_name}/README.md"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        }
        expected_agents = {
            f"mechanics/{parent_name}/AGENTS.md"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        }

        assert set(validate_repo.MECHANIC_PARENT_README_FILES) == expected_readmes
        assert set(validate_repo.MECHANIC_PARENT_AGENTS_FILES) == expected_agents

    def test_mechanic_legacy_raw_readmes_cover_allowed_parents(self) -> None:
        expected = {
            f"mechanics/{parent_name}/legacy/raw/README.md"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        }

        assert set(validate_repo.MECHANIC_LEGACY_RAW_README_FILES) == expected

    def test_mechanic_legacy_skeleton_files_cover_allowed_parents(self) -> None:
        expected = {
            f"mechanics/{parent_name}/{suffix}"
            for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
            for suffix in (
                "PROVENANCE.md",
                "legacy/README.md",
                "legacy/INDEX.md",
                "legacy/DISTILLATION_LOG.md",
                "legacy/raw/README.md",
            )
        }

        assert set(validate_repo.MECHANIC_LEGACY_SKELETON_FILES) == expected

    def test_mechanic_provenance_entry_files_validate_contract(self) -> None:
        assert validate_repo.validate_mechanic_provenance_entry_surfaces(REPO_ROOT) == []

    def test_mechanic_parent_direction_surfaces_validate_contract(self) -> None:
        assert validate_repo.validate_mechanic_parent_direction_surfaces(REPO_ROOT) == []

    def test_mechanic_parent_direction_rejects_missing_current_contour(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_DIRECTION_FILES:
            write_text(
                tmp_path / path_name,
                "# Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Current contour\n\nNow.\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
            )
        direction_path = "mechanics/titan/DIRECTION.md"
        write_text(
            tmp_path / direction_path,
            "# Titan Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
        )

        issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

        assert any(
            issue.location == direction_path and "## Current contour" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_direction_rejects_missing_readme_entry_route(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_DIRECTION_FILES:
            write_text(
                tmp_path / path_name,
                "# Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Current contour\n\nNow.\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
            )
        for path_name in validate_repo.MECHANIC_PARENT_README_FILES:
            write_text(
                tmp_path / path_name,
                "# Parent\n\n## Entry Route\n\n[DIRECTION.md](DIRECTION.md)\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\n",
            )
        for parent_name, path_name in zip(
            validate_repo.ACTIVE_MECHANIC_PARENT_NAMES,
            validate_repo.MECHANIC_PARENT_AGENTS_FILES,
            strict=True,
        ):
            write_text(
                tmp_path / path_name,
                f"# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\n`mechanics/{parent_name}/DIRECTION.md`\n`mechanics/{parent_name}/PARTS.md`\n`mechanics/{parent_name}/PROVENANCE.md`\n",
            )
        readme_path = "mechanics/titan/README.md"
        write_text(
            tmp_path / readme_path,
            "# Titan\n\n## Entry Route\n\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\n",
        )

        issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

        assert any(
            issue.location == readme_path and "[DIRECTION.md](DIRECTION.md)" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_direction_rejects_missing_readme_role_and_next_route(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_DIRECTION_FILES:
            write_text(
                tmp_path / path_name,
                "# Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Current contour\n\nNow.\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
            )
        for path_name in validate_repo.MECHANIC_PARENT_README_FILES:
            write_text(
                tmp_path / path_name,
                "# Parent\n\n## Entry Route\n\n[DIRECTION.md](DIRECTION.md)\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\n\n## Owned Operation\n\nRoute proof work.\n\n## Validation\n\n[AGENTS](AGENTS.md#validation)\n",
            )
        for parent_name, path_name in zip(
            validate_repo.ACTIVE_MECHANIC_PARENT_NAMES,
            validate_repo.MECHANIC_PARENT_AGENTS_FILES,
            strict=True,
        ):
            write_text(
                tmp_path / path_name,
                f"# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\n`mechanics/{parent_name}/DIRECTION.md`\n`mechanics/{parent_name}/PARTS.md`\n`mechanics/{parent_name}/PROVENANCE.md`\n",
            )

        issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/titan/README.md" and "## Role" in issue.message
            for issue in issues
        )
        assert any(
            issue.location == "mechanics/titan/README.md" and "## Next Route" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_direction_rejects_missing_agents_entry_route(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_DIRECTION_FILES:
            write_text(
                tmp_path / path_name,
                "# Direction\n\ncurrent operating direction\n\n## Source-of-truth split\n\n`README.md`\n`DIRECTION.md`\n`PARTS.md`\n`PROVENANCE.md`\n\n## Current contour\n\nNow.\n\n## Growth rule\n\nGrow only with proof.\n\n## Stop-lines\n\nNo overclaim.\n\n## Validation\n\n`python scripts/validate_repo.py`\n",
            )
        for path_name in validate_repo.MECHANIC_PARENT_README_FILES:
            write_text(
                tmp_path / path_name,
                "# Parent\n\n## Entry Route\n\n[DIRECTION.md](DIRECTION.md)\ncurrent operating direction\n[PARTS.md](PARTS.md)\n[PROVENANCE.md](PROVENANCE.md)\n",
            )
        for parent_name, path_name in zip(
            validate_repo.ACTIVE_MECHANIC_PARENT_NAMES,
            validate_repo.MECHANIC_PARENT_AGENTS_FILES,
            strict=True,
        ):
            write_text(
                tmp_path / path_name,
                f"# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\n`mechanics/{parent_name}/DIRECTION.md`\n`mechanics/{parent_name}/PARTS.md`\n`mechanics/{parent_name}/PROVENANCE.md`\n",
            )
        agents_path = "mechanics/titan/AGENTS.md"
        write_text(
            tmp_path / agents_path,
            "# AGENTS.md\n\n## Entry Route\n\ncurrent operating direction\n`mechanics/titan/PARTS.md`\n`mechanics/titan/PROVENANCE.md`\n",
        )

        issues = validate_repo.validate_mechanic_parent_direction_surfaces(tmp_path)

        assert any(
            issue.location == agents_path and "`mechanics/titan/DIRECTION.md`" in issue.message
            for issue in issues
        )

    def test_mechanic_provenance_entry_rejects_missing_legacy_readme_bridge(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_PROVENANCE_FILES:
            write_text(
                tmp_path / path_name,
                "# Provenance\n\nactive route\nlegacy/README.md\nlegacy archive owns its own details\narchive details stay out\n",
            )
        readme_path = "mechanics/titan/PROVENANCE.md"
        write_text(
            tmp_path / readme_path,
            "# Titan Provenance\n\nactive route\nlegacy archive owns its own details\narchive details stay out\n",
        )

        issues = validate_repo.validate_mechanic_provenance_entry_surfaces(tmp_path)

        assert any(
            issue.location == readme_path and "legacy/README.md" in issue.message
            for issue in issues
        )

    def test_mechanic_provenance_entry_rejects_archive_detail_in_bridge(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_PROVENANCE_FILES:
            write_text(
                tmp_path / path_name,
                "# Provenance\n\nactive route\nlegacy/README.md\nlegacy archive owns its own details\narchive details stay out\n",
            )
        readme_path = "mechanics/titan/PROVENANCE.md"
        write_text(
            tmp_path / readme_path,
            "# Titan Provenance\n\nactive route\nlegacy/README.md\nlegacy/INDEX.md\nlegacy archive owns its own details\narchive details stay out\n",
        )

        issues = validate_repo.validate_mechanic_provenance_entry_surfaces(tmp_path)

        assert any(
            issue.location == readme_path and "without carrying archive detail" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_readmes_validate_entry_contract(self) -> None:
        legacy_readmes = set(validate_repo.MECHANIC_LEGACY_README_FILES)

        assert not any(
            issue.location in legacy_readmes
            for issue in validate_repo.validate_mechanics_parent_allowlist(REPO_ROOT)
        )

    def test_mechanic_parent_class_sets_cover_allowed_parents(self) -> None:
        aoa_parents = set(validate_repo.AOA_ALIGNED_MECHANIC_PARENT_NAMES)
        evals_native_parents = set(validate_repo.EVALS_NATIVE_MECHANIC_PARENT_NAMES)

        assert aoa_parents.isdisjoint(evals_native_parents)
        assert aoa_parents | evals_native_parents == set(
            validate_repo.ACTIVE_MECHANIC_PARENT_NAMES
        )

    def test_mechanic_parent_class_map_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_parent_class_map(REPO_ROOT) == []

    def test_mechanic_evidence_dimension_ledger_validates_current_routes(self) -> None:
        issues = validate_repo.validate_mechanic_parent_class_map(REPO_ROOT)

        assert not any(
            "evidence dimension ledger" in issue.message for issue in issues
        )

    def test_mechanic_evidence_route_refs_validate_current_routes(self) -> None:
        issues = validate_repo.validate_mechanic_parent_class_map(REPO_ROOT)

        assert not any(
            "evidence route refs" in issue.message for issue in issues
        )

    def test_mechanic_evidence_dimension_ledger_rejects_missing_parent_row(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8")
        evidence_text = evidence_text.replace(
            "| `titan` | evals-native | owner-named Titan proof-seed boundary, not proof-organ doctrine | incarnation, summon, memory, gate, runtime roster, bridge, and closeout seed pressure | Titan canary YAML seeds and seed AGENTS route | canary shape validator and tests; future scorer route is not active | Titan boundary pressure stays seed-level until executable proof exists | `aoa-agents` owns Titan role/bearer/summon/incarnation law; `aoa-memo` and runtime owners keep memory and activation truth | old `titan-canaries` parent and root `evals/` placement route through provenance |\n",
            "",
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "active parent `titan` must appear in the evidence dimension ledger"
            in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_dimension_ledger_rejects_wrong_class(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8")
        evidence_text = evidence_text.replace(
            "| `titan` | evals-native |",
            "| `titan` | AoA-aligned |",
            1,
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "row for `titan` must use class `evals-native`" in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_dimension_ledger_rejects_empty_dimension(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8")
        evidence_text = evidence_text.replace(
            "Titan canary YAML seeds and seed AGENTS route",
            "TBD",
            1,
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "row for `titan` must fill `Contracts/payloads`" in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_route_refs_rejects_missing_path_refs(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `README.md` |",
                "| `titan` | seed-boundary prose without route refs |",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "evidence route refs row for `titan` must name at least"
            in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_route_refs_rejects_generic_root_validator_ref(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `README.md` |",
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `tests/test_validate_repo.py` |",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "must not use generic root validator route `tests/test_validate_repo.py`"
            in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_route_refs_rejects_decision_only_non_mechanics_ref(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `README.md` |",
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `docs/decisions/0015-titan-mechanic-package.md` |",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "living non-mechanics evidence" in issue.message
            and "rationale-only decision refs are not enough" in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_route_refs_rejects_stale_path(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        stale_ref = "mechanics/titan/parts/seed-boundary/seeds/missing-canary.yaml"
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml",
                stale_ref,
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "evidence route refs row for `titan` has stale route ref" in issue.message
            and stale_ref in issue.message
            for issue in issues
        )

    def test_mechanic_evidence_route_refs_rejects_mechanics_only_row(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml`, `README.md` |",
                "| `titan` | `mechanics/titan/README.md`, `mechanics/titan/parts/seed-boundary/README.md`, `mechanics/titan/parts/seed-boundary/seeds/titan_incarnation_spine_canary.yaml` |",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "must include at least one non-mechanics route ref" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_class_map_rejects_missing_owner_named_titan_boundary(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME,
            validate_repo.MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
            validate_repo.MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
            validate_repo.MECHANIC_PARENT_CLASS_DECISION_NAME,
            "docs/decisions/README.md",
            "mechanics/README.md",
            validate_repo.PROOF_TOPOLOGY_NAME,
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "owner-named evals-native",
                "plain evals-native",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "owner-named evals-native" in issue.message
            for issue in issues
        )

    def test_mechanic_root_district_recon_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_root_district_recon_surfaces(REPO_ROOT) == []

    def test_mechanic_root_district_recon_rejects_missing_district_row(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
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
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
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
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path, validate_repo.MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
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

    def test_root_authored_surface_classification_validates_current_routes(self) -> None:
        assert validate_repo.validate_root_authored_surface_classification(REPO_ROOT) == []

    def test_root_authored_surface_classification_rejects_unclassified_root_doc(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path,
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        for district_name, file_names in (
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
        ):
            for file_name in file_names:
                copy_repo_text(tmp_path, f"{district_name}/{file_name}")
        write_text(
            tmp_path / "docs" / "UNROUTED_MECHANIC_PAYLOAD.md",
            "# Unrouted\n",
        )

        issues = validate_repo.validate_root_authored_surface_classification(tmp_path)

        assert any(
            issue.location == "docs/UNROUTED_MECHANIC_PAYLOAD.md"
            and "unclassified root-authored surface" in issue.message
            for issue in issues
        )

    def test_root_authored_surface_classification_rejects_missing_ledger_row(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path,
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        for district_name, file_names in (
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
        ):
            for file_name in file_names:
                copy_repo_text(tmp_path, f"{district_name}/{file_name}")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = "\n".join(
            line
            for line in evidence_path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("| `tests/test_validate_repo.py` |")
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_root_authored_surface_classification(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "root-authored surface `tests/test_validate_repo.py` must appear"
            in issue.message
            for issue in issues
        )

    def test_root_authored_surface_classification_rejects_empty_boundary(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(
            tmp_path,
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        )
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "ROADMAP.md")
        for district_name, file_names in (
            validate_repo.ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
        ):
            for file_name in file_names:
                copy_repo_text(tmp_path, f"{district_name}/{file_name}")
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "mechanic-owned payload validators may live part-local, while this file guards cross-repo topology",
                "TBD",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_root_authored_surface_classification(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "root-authored surface `scripts/validate_repo.py` row must fill `Mechanic boundary`"
            in issue.message
            for issue in issues
        )

    def test_mechanic_part_readme_contract_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []

    def test_mechanic_part_readme_contract_rejects_heading_without_parent(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
        for path_name in (
            "mechanics/proof-loop/PARTS.md",
            readme_name,
            "mechanics/proof-loop/parts/route-smoke/VALIDATION.md",
        ):
            copy_repo_text(tmp_path, path_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "# Proof Loop / Route Smoke Part",
                "# Route Smoke Part",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "parent mechanic" in issue.message
            for issue in issues
        )

    def test_mechanic_part_readme_contract_rejects_validation_heading_without_parent(
        self, tmp_path: Path
    ) -> None:
        validation_name = "mechanics/proof-loop/parts/route-smoke/VALIDATION.md"
        for path_name in (
            "mechanics/proof-loop/PARTS.md",
            "mechanics/proof-loop/parts/route-smoke/README.md",
            validation_name,
        ):
            copy_repo_text(tmp_path, path_name)
        validation_path = tmp_path / validation_name
        validation_path.write_text(
            validation_path.read_text(encoding="utf-8").replace(
                "# Proof Loop / Route Smoke Validation",
                "# Route Smoke Validation",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == validation_name
            and "parent mechanic" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []

    def test_mechanic_part_source_surface_refs_validate_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []

    def test_mechanic_part_source_surfaces_section_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []

    def test_mechanic_part_source_surfaces_section_rejects_singular_heading(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
        copy_repo_text(tmp_path, "mechanics/proof-loop/PARTS.md")
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Source Surfaces",
                "## Source Surface",
                1,
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Source Surfaces" in issue.message
            for issue in issues
        )

    def test_mechanic_part_source_surfaces_section_rejects_empty_section(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
        copy_repo_text(tmp_path, "mechanics/proof-loop/PARTS.md")
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        text = readme_path.read_text(encoding="utf-8")
        text = text.replace(
            "## Source Surfaces\n\n- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`\n\n",
            "## Source Surfaces\n\n",
            1,
        )
        readme_path.write_text(text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "at least one path-like source ref" in issue.message
            for issue in issues
        )

    def test_mechanic_part_source_surface_refs_reject_stale_path(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Source Surfaces

            - `mechanics/agon/parts/new-proof/docs/missing.md`

            ## Inputs

            Local evidence.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "stale source surface ref" in issue.message
            and "mechanics/agon/parts/new-proof/docs/missing.md" in issue.message
            for issue in issues
        )

    def test_mechanic_part_source_surface_refs_allow_explicit_nonlocal_routes(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "docs" / "note.md",
            "# Note\n",
        )

        assert (
            validate_repo.source_surface_ref_resolution_issue(
                tmp_path,
                "mechanics/agon/parts/new-proof/docs/*.md",
            )
            is None
        )
        assert (
            validate_repo.source_surface_ref_resolution_issue(
                tmp_path,
                "repo:aoa-playbooks/generated/phase_alpha_run_matrix.min.json",
            )
            is None
        )
        assert (
            validate_repo.source_surface_ref_resolution_issue(
                tmp_path,
                "quests/<lane>/<state>/AOA-EV-Q-*.yaml",
            )
            is None
        )

    def test_mechanic_part_readme_contract_rejects_unrouted_part(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            "# Agon Parts\n\nNo concrete part route is listed here.\n",
        )
        write_text(
            tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "README.md",
            """
            # New Proof

            ## Inputs

            Local evidence.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/agon/PARTS.md"
            and "mechanics/agon/parts/new-proof/README.md" in issue.message
            for issue in issues
        )

    def test_mechanic_part_readme_contract_rejects_missing_owner_split(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Inputs

            Local evidence.

            ## Outputs

            Local readout.

            ## Owner Split

            Too soft.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_rejects_unmentioned_payload_dir(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Inputs

            Local evidence.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "new-proof"
            / "fixtures"
            / "case.json",
            "{}\n",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "payload subdirectory `fixtures/`" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_rejects_unknown_payload_class(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Inputs

            Local evidence from `mystery/`.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "new-proof"
            / "mystery"
            / "case.json",
            "{}\n",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/agon/parts/new-proof/mystery"
            and "unexpected payload class" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_rejects_unexpected_part_root_file(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Inputs

            Local evidence.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "new-proof"
            / "payload.json",
            "{}\n",
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/agon/parts/new-proof/payload.json"
            and "unexpected part-root file" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_rejects_empty_payload_dir(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Inputs

            Local evidence from `fixtures/`.

            ## Outputs

            Local readout.

            ## Stronger Owner Split

            AoA keeps doctrine; aoa-evals keeps proof shape.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )
        (tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "fixtures").mkdir(
            parents=True
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/agon/parts/new-proof/fixtures"
            and "empty payload subdirectory" in issue.message
            for issue in issues
        )

    def test_mechanic_part_payload_inventory_rejects_unexplained_thin_part(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md", "# Demo\n")
        write_text(
            tmp_path / "mechanics" / "agon" / "PARTS.md",
            f"# Agon Parts\n\n- `{readme_name}`\n",
        )
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Source Surfaces

            - `evals/workflow/aoa-demo/EVAL.md`

            ## Inputs

            Bundle-local evidence.

            ## Outputs

            Bundle-local readout.

            ## Stronger Owner Split

            Bundles keep source proof meaning; mechanics keeps route support.

            ## Stop-Lines

            No parent promotion.

            ## Validation

            `python scripts/validate_repo.py`
            """,
        )

        issues = validate_repo.validate_mechanic_part_readme_contract_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "eval-backed thin support route" in issue.message
            for issue in issues
        )

    def test_mechanic_part_validation_command_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_part_validation_command_surfaces(REPO_ROOT) == []

    def test_mechanic_part_validation_command_rejects_stale_path(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Validation

            ```bash
            python mechanics/agon/parts/new-proof/scripts/missing.py --check
            ```
            """,
        )

        issues = validate_repo.validate_mechanic_part_validation_command_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "stale validation path `mechanics/agon/parts/new-proof/scripts/missing.py`"
            in issue.message
            for issue in issues
        )

    def test_mechanic_part_validation_command_rejects_missing_python_command(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Validation

            Validation is manual review later.
            """,
        )

        issues = validate_repo.validate_mechanic_part_validation_command_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "part validation route must list at least one python command"
            in issue.message
            for issue in issues
        )

    def test_mechanic_part_validation_command_rejects_readme_command_blocks(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Validation

            ```bash
            python scripts/validate_repo.py
            ```
            """,
        )
        write_text(
            tmp_path / "mechanics/agon/parts/new-proof/VALIDATION.md",
            """
            # New Proof Validation

            Use the `new-proof` child validation block in parent parts AGENTS.
            """,
        )
        write_text(
            tmp_path / "mechanics/agon/parts/AGENTS.md",
            """
            # AGENTS.md

            ## Validation

            ### `mechanics/agon/parts/new-proof/VALIDATION.md`

            ```bash
            python scripts/validate_repo.py
            ```
            """,
        )
        write_text(tmp_path / "scripts/validate_repo.py", "# validator\n")

        issues = validate_repo.validate_mechanic_part_validation_command_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "README validation section must route executable commands" in issue.message
            for issue in issues
        )

    def test_mechanic_part_validation_command_rejects_absolute_path(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Validation

            ```bash
            python /tmp/not-repo-local.py
            ```
            """,
        )

        issues = validate_repo.validate_mechanic_part_validation_command_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "repo-relative path" in issue.message
            for issue in issues
        )

    def test_mechanic_part_validation_command_rejects_unanchored_payload_part(
        self, tmp_path: Path
    ) -> None:
        readme_name = "mechanics/agon/parts/new-proof/README.md"
        write_text(
            tmp_path / readme_name,
            """
            # New Proof

            ## Validation

            ```bash
            python scripts/validate_repo.py
            python scripts/build_catalog.py --check
            ```
            """,
        )
        write_text(
            tmp_path
            / "mechanics"
            / "agon"
            / "parts"
            / "new-proof"
            / "schemas"
            / "new-proof.schema.json",
            "{}\n",
        )
        write_text(tmp_path / "scripts" / "validate_repo.py", "# validator\n")
        write_text(tmp_path / "scripts" / "build_catalog.py", "# builder\n")

        issues = validate_repo.validate_mechanic_part_validation_command_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "payload coverage anchor" in issue.message
            and "naked route-wide commands" in issue.message
            for issue in issues
        )

    def test_mechanic_parts_index_sync_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_parts_index_sync_surfaces(REPO_ROOT) == []

    def test_mechanic_index_command_ownership_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_index_command_ownership(REPO_ROOT) == []

    def test_mechanic_index_command_ownership_rejects_parts_index_commands(
        self, tmp_path: Path
    ) -> None:
        parts_index_name = "mechanics/proof-object/PARTS.md"
        write_text(
            tmp_path / parts_index_name,
            """
            # Proof Object Parts

            ## Validation

            ```bash
            python scripts/validate_repo.py
            ```
            """,
        )

        issues = validate_repo.validate_mechanic_index_command_ownership(tmp_path)

        assert any(
            issue.location == parts_index_name
            and "route executable validation commands to the nearest AGENTS.md"
            in issue.message
            for issue in issues
        )

    def test_mechanic_parts_index_sync_rejects_unlisted_actual_part(
        self, tmp_path: Path
    ) -> None:
        parts_index_name = "mechanics/agon/PARTS.md"
        write_text(
            tmp_path / parts_index_name,
            "# Agon Parts\n\nNo local parts are declared here.\n",
        )
        (tmp_path / "mechanics" / "agon" / "parts" / "new-proof").mkdir(
            parents=True
        )

        issues = validate_repo.validate_mechanic_parts_index_sync_surfaces(tmp_path)

        assert any(
            issue.location == parts_index_name
            and "actual part directory `new-proof`" in issue.message
            for issue in issues
        )

    def test_mechanic_parts_index_sync_rejects_stale_local_part_route(
        self, tmp_path: Path
    ) -> None:
        parts_index_name = "mechanics/agon/PARTS.md"
        write_text(
            tmp_path / parts_index_name,
            "# Agon Parts\n\n- [Ghost](parts/ghost-proof/README.md)\n",
        )
        (tmp_path / "mechanics" / "agon" / "parts").mkdir(parents=True)

        issues = validate_repo.validate_mechanic_parts_index_sync_surfaces(tmp_path)

        assert any(
            issue.location == parts_index_name
            and "stale local part route `ghost-proof`" in issue.message
            for issue in issues
        )

    def test_mechanic_parts_index_sync_allows_cross_parent_reference(
        self, tmp_path: Path
    ) -> None:
        parts_index_name = "mechanics/experience/PARTS.md"
        write_text(
            tmp_path / parts_index_name,
            """
            # Experience Parts

            | Part | Role |
            | --- | --- |
            | `adoption-federation` | Local part. |

            Reviewed runtime distillation candidate adoption routes through
            `mechanics/distillation/parts/runtime-candidate-adoption/`.
            """,
        )
        (tmp_path / "mechanics" / "experience" / "parts" / "adoption-federation").mkdir(
            parents=True
        )

        issues = validate_repo.validate_mechanic_parts_index_sync_surfaces(tmp_path)

        assert not any(
            issue.location == parts_index_name
            and "runtime-candidate-adoption" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_single_bridge_validates_current_routes(self) -> None:
        assert validate_repo.validate_mechanic_legacy_single_bridge_surfaces(REPO_ROOT) == []

    def test_mechanic_legacy_single_bridge_rejects_active_direct_legacy_index(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            f"""
            # Mechanic Legacy Single Bridge

            `PROVENANCE.md`
            single controlled bridge
            active mechanic surfaces
            legacy archive
            active surface
            direct `legacy/INDEX.md`
            direct `legacy/raw`
            JSON
            YAML
            {validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND}
            """,
        )
        write_text(
            tmp_path / "docs" / "decisions" / "README.md",
            f"{validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME}\nMechanic Legacy Single Bridge\n",
        )
        write_text(
            tmp_path / validate_repo.MECHANICS_README_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / validate_repo.PROOF_TOPOLOGY_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / validate_repo.LEGACY_NAMING_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / "ROADMAP.md",
            "Mechanic Legacy Single Bridge\nsingle controlled bridge\nactive mechanic surfaces\n",
        )
        readme_name = "mechanics/titan/README.md"
        write_text(
            tmp_path / readme_name,
            "# Titan\n\nUse `legacy/INDEX.md` directly for old canary lookup.\n",
        )

        issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "route legacy archive details through PROVENANCE.md" in issue.message
            and "legacy/INDEX.md" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_single_bridge_rejects_active_direct_legacy_raw_in_json(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            "docs/decisions/README.md",
            validate_repo.MECHANICS_README_NAME,
            validate_repo.PROOF_TOPOLOGY_NAME,
            validate_repo.LEGACY_NAMING_NAME,
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)
        manifest_name = "mechanics/titan/parts/seed-boundary/manifests/demo.json"
        write_text(
            tmp_path / manifest_name,
            '{"surfaces": ["mechanics/titan/legacy/raw/old-canary.md"]}\n',
        )

        issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

        assert any(
            issue.location == manifest_name
            and "route legacy archive details through PROVENANCE.md" in issue.message
            and "legacy/raw/" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_single_bridge_rejects_provenance_archive_detail(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            f"""
            # Mechanic Legacy Single Bridge

            `PROVENANCE.md`
            single controlled bridge
            active mechanic surfaces
            legacy archive
            active surface
            direct `legacy/INDEX.md`
            direct `legacy/raw`
            JSON
            YAML
            {validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND}
            """,
        )
        write_text(
            tmp_path / "docs" / "decisions" / "README.md",
            f"{validate_repo.MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME}\nMechanic Legacy Single Bridge\n",
        )
        write_text(
            tmp_path / validate_repo.MECHANICS_README_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / validate_repo.PROOF_TOPOLOGY_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / validate_repo.LEGACY_NAMING_NAME,
            "single controlled bridge\nactive mechanic surfaces\nlegacy archive\n",
        )
        write_text(
            tmp_path / "ROADMAP.md",
            "Mechanic Legacy Single Bridge\nsingle controlled bridge\nactive mechanic surfaces\n",
        )
        write_text(
            tmp_path / "mechanics" / "titan" / "README.md",
            "# Titan\n\nUse `PROVENANCE.md` for legacy or former placement.\n",
        )
        write_text(
            tmp_path / "mechanics" / "titan" / "PROVENANCE.md",
            "# Titan Provenance\n\nUse `legacy/INDEX.md` and `legacy/raw/README.md` here.\n",
        )

        issues = validate_repo.validate_mechanic_legacy_single_bridge_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/titan/PROVENANCE.md"
            and "without carrying archive detail" in issue.message
            for issue in issues
        )

    def test_mechanic_provenance_bridge_posture_validates_current_routes(self) -> None:
        assert (
            validate_repo.validate_mechanic_provenance_bridge_posture_surfaces(REPO_ROOT)
            == []
        )

    def test_mechanic_provenance_bridge_posture_rejects_missing_active_first_contract(
        self, tmp_path: Path
    ) -> None:
        for path_name in validate_repo.MECHANIC_PROVENANCE_FILES:
            copy_repo_text(tmp_path, path_name)
        for path_name in (
            validate_repo.MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
            "docs/decisions/README.md",
            validate_repo.MECHANICS_README_NAME,
            validate_repo.PROOF_TOPOLOGY_NAME,
            validate_repo.LEGACY_NAMING_NAME,
            "DESIGN.md",
            "ROADMAP.md",
        ):
            copy_repo_text(tmp_path, path_name)

        broken_path = "mechanics/titan/PROVENANCE.md"
        write_text(
            tmp_path / broken_path,
            "# Titan Provenance\n\nUse `legacy/INDEX.md` for old canaries.\n",
        )

        issues = validate_repo.validate_mechanic_provenance_bridge_posture_surfaces(
            tmp_path
        )

        assert any(
            issue.location == broken_path
            and "bridge, not an active route" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_allowlist_rejects_unknown_parent(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES:
            (tmp_path / "mechanics" / parent_name).mkdir(parents=True)
        write_text(
            tmp_path / "mechanics" / "repair" / "README.md",
            "# Repair\n\nThis invented parent must not become active topology.\n",
        )

        issues = validate_repo.validate_mechanics_parent_allowlist(tmp_path)

        assert any(
            issue.location == "mechanics/repair"
            and "evidence-cluster allowlist" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_allowlist_rejects_missing_declared_parent(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES:
            if parent_name == "titan":
                continue
            (tmp_path / "mechanics" / parent_name).mkdir(parents=True)

        issues = validate_repo.validate_mechanics_parent_allowlist(tmp_path)

        assert any(
            issue.location == "mechanics/titan"
            and "declared mechanic parent directory is missing" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_allowlist_rejects_missing_route_card(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        for parent_name in validate_repo.ACTIVE_MECHANIC_PARENT_NAMES:
            parent_root = tmp_path / "mechanics" / parent_name
            parent_root.mkdir(parents=True)
            for filename in ("AGENTS.md", "README.md", "PARTS.md"):
                write_text(parent_root / filename, f"# {filename}\n")
        (tmp_path / "mechanics" / "proof-object" / "PARTS.md").unlink()

        issues = validate_repo.validate_mechanics_parent_allowlist(tmp_path)

        assert any(
            issue.location == "mechanics/proof-object/PARTS.md"
            and "active mechanic parent must expose" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_skeleton_rejects_missing_legacy_index(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_LEGACY_SKELETON_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        for path_name in validate_repo.MECHANIC_ROUTE_CARD_FILES:
            write_text(tmp_path / path_name, "# Route\n")
        for path_name in validate_repo.MECHANIC_LEGACY_SKELETON_FILES:
            write_text(tmp_path / path_name, "# Legacy\n")
        missing_path = "mechanics/questbook/legacy/INDEX.md"
        (tmp_path / missing_path).unlink()

        issues = validate_repo.validate_mechanics_parent_allowlist(tmp_path)

        assert any(
            issue.location == missing_path
            and "archive-local legacy entry/accounting surfaces" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_readme_rejects_missing_provenance_route(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, "mechanics/README.md")
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_PARENT_ALLOWLIST_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.MECHANIC_LEGACY_SKELETON_DECISION_NAME)
        copy_repo_text(tmp_path, validate_repo.PROOF_TOPOLOGY_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        for path_name in validate_repo.MECHANIC_ROUTE_CARD_FILES:
            write_text(tmp_path / path_name, "# Route\n")
        for path_name in validate_repo.MECHANIC_LEGACY_SKELETON_FILES:
            write_text(
                tmp_path / path_name,
                "# Legacy\n\n../PROVENANCE.md\nINDEX.md\nDISTILLATION_LOG.md\nraw/README.md\nnot active topology\nnew-work entrypoint\n",
            )
        readme_path = "mechanics/titan/legacy/README.md"
        write_text(
            tmp_path / readme_path,
            "# Titan Legacy\n\nINDEX.md\nDISTILLATION_LOG.md\nraw/README.md\nnot active topology\nnew-work entrypoint\n",
        )

        issues = validate_repo.validate_mechanics_parent_allowlist(tmp_path)

        assert any(
            issue.location == readme_path and "../PROVENANCE.md" in issue.message
            for issue in issues
        )

    def test_mechanic_legacy_raw_payload_accounting_validates_current_routes(
        self,
    ) -> None:
        assert validate_repo.validate_mechanic_legacy_raw_payload_accounting(REPO_ROOT) == []

    def test_mechanic_legacy_raw_payload_accounting_rejects_unindexed_payload(
        self, tmp_path: Path
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
        self, tmp_path: Path
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
        self, tmp_path: Path
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

    def test_mechanic_parent_class_map_rejects_misclassified_parent(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8")
        evidence_text = evidence_text.replace(
            "| `titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries",
            "| `not-titan` | Titan incarnation and summon discipline docs plus 37 Titan seed canaries",
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "evals-native parent `titan`" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_class_map_rejects_missing_wrong_parent_mapping(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8").replace(
            "| `repair` | `antifragility/repair-proof` | Names a stage or artifact pressure instead of the active bounded repair-proof part; future Growth Cycle repair stages still need separate evidence. |\n",
            "",
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "former wrong parent `repair`" in issue.message
            for issue in issues
        )

    def test_mechanic_parent_class_map_rejects_plausible_parent_wording(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME)
        evidence_path = tmp_path / validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        evidence_text = evidence_path.read_text(encoding="utf-8").replace(
            "The following parents are active and must stay constrained",
            "The following parents are currently plausible and must stay constrained",
        )
        evidence_path.write_text(evidence_text, encoding="utf-8")

        issues = validate_repo.validate_mechanic_parent_class_map(tmp_path)

        assert any(
            issue.location == validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
            and "not merely plausible candidates" in issue.message
            for issue in issues
        )

    def test_active_legacy_parent_wording_validates_current_routes(self) -> None:
        assert validate_repo.validate_active_legacy_parent_wording(REPO_ROOT) == []

    def test_active_legacy_parent_wording_rejects_old_parent_forms(
        self, tmp_path: Path
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
        audit_parts.write_text("# Runtime Evidence Parts\n\n`runtime-evidence` mechanic\n", encoding="utf-8")
        titan_readme = tmp_path / "mechanics" / "titan" / "README.md"
        titan_readme.write_text("This package routes Titan canary work.\n", encoding="utf-8")
        titan_parts = tmp_path / "mechanics" / "titan" / "parts" / "README.md"
        titan_parts.write_text("# Titan Canaries Parts\n\nTitan-canary-owned artifacts.\n", encoding="utf-8")
        reports_readme = tmp_path / "reports" / "README.md"
        reports_readme.write_text("Proof-release reports no longer live here.\n", encoding="utf-8")
        releasing = tmp_path / "docs" / "RELEASING.md"
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
            issue.location == "docs/RELEASING.md"
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

    def test_audit_legacy_index_rejects_missing_runtime_evidence_lineage(
        self, tmp_path: Path
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
        self, tmp_path: Path
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
        self, tmp_path: Path
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
        self, tmp_path: Path
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
        self, tmp_path: Path
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

    def test_audit_part_readmes_reject_missing_inputs_contract(
        self, tmp_path: Path
    ) -> None:
        copy_repo_text(tmp_path, validate_repo.AUDIT_SELECTED_EVIDENCE_PART_README_NAME)
        readme_path = tmp_path / validate_repo.AUDIT_SELECTED_EVIDENCE_PART_README_NAME
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace("## Inputs", "## Intake"),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == validate_repo.AUDIT_SELECTED_EVIDENCE_PART_README_NAME
            and "## Inputs" in issue.message
            for issue in issues
        )

    def test_agon_part_readmes_reject_missing_stop_line_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.AGON_PART_README_CONTRACTS[0][0]
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_boundary_bridge_part_readmes_reject_missing_outputs_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        copy_repo_text(tmp_path, validate_repo.BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME)
        copy_repo_text(tmp_path, "docs/decisions/README.md")
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Outputs", "## Result Notes"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Outputs" in issue.message
            for issue in issues
        )

    def test_publication_receipts_part_readmes_reject_missing_stop_lines_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_release_support_part_readmes_reject_missing_stop_lines_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_comparison_spine_part_readmes_reject_missing_inputs_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Inputs", "## Intake"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Inputs" in issue.message
            for issue in issues
        )

    def test_proof_loop_route_smoke_part_readme_rejects_missing_inputs_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Inputs", "## Intake"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Inputs" in issue.message
            for issue in issues
        )

    def test_antifragility_part_readmes_reject_missing_stop_lines_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_checkpoint_part_readmes_reject_stale_root_fixture_path(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.CHECKPOINT_A2A_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md",
                "fixtures/a2a-summon-return-checkpoint-v1/README.md",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md"
            in issue.message
            for issue in issues
        )

    def test_experience_part_readmes_reject_missing_owner_split_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.EXPERIENCE_ADOPTION_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_distillation_part_readmes_reject_missing_stop_lines_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_growth_cycle_diagnosis_gate_rejects_missing_owner_split_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_repair_diagnosis_route_boundary_rejects_deferred_antifragility_parts(
        self, tmp_path: Path
    ) -> None:
        parts_name = validate_repo.ANTIFRAGILITY_MECHANIC_PARTS_NAME
        copy_repo_text(tmp_path, parts_name)
        parts_path = tmp_path / parts_name
        parts_path.write_text(
            parts_path.read_text(encoding="utf-8").replace(
                "`mechanics/growth-cycle/parts/diagnosis-gate/`",
                "`evals/workflow/aoa-diagnosis-cause-discipline` deferred route",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == parts_name
            and "mechanics/growth-cycle/parts/diagnosis-gate/" in issue.message
            for issue in issues
        )

    def test_repair_diagnosis_route_boundary_rejects_stale_evidence_map_route(
        self, tmp_path: Path
    ) -> None:
        evidence_name = validate_repo.MECHANICS_EVIDENCE_CLUSTERS_NAME
        copy_repo_text(tmp_path, evidence_name)
        evidence_path = tmp_path / evidence_name
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8").replace(
                "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate`, not this parent.",
                "diagnosis-cause discipline remains deferred.",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == evidence_name
            and "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate`, not this parent."
            in issue.message
            for issue in issues
        )

    def test_method_growth_part_owner_split_rejects_soft_owner_split(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Owner Split"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_proof_object_part_owner_split_rejects_missing_source_bundle_boundary(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_questbook_part_owner_split_rejects_missing_generated_boundary(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.QUESTBOOK_DISPATCH_READER_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stronger Owner Split", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "## Stronger Owner Split" in issue.message
            for issue in issues
        )

    def test_recurrence_control_plane_rejects_stale_root_fixture_path(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.RECURRENCE_CONTROL_PLANE_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md",
                "fixtures/recurrence-control-plane-integrity-v1/README.md",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name
            and "mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md"
            in issue.message
            for issue in issues
        )

    def test_rpg_progression_unlocks_rejects_missing_stop_lines_contract(
        self, tmp_path: Path
    ) -> None:
        readme_name = validate_repo.RPG_PROGRESS_UNLOCKS_PART_README_NAME
        copy_repo_text(tmp_path, readme_name)
        readme_path = tmp_path / readme_name
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8").replace(
                "## Stop-Lines", "## Boundary"
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_mechanics_surfaces(tmp_path)

        assert any(
            issue.location == readme_name and "## Stop-Lines" in issue.message
            for issue in issues
        )

    def test_proof_loop_smoke_report_surfaces_validate_current_route(self) -> None:
        assert validate_repo.validate_proof_loop_smoke_report_surfaces(REPO_ROOT) == []

    def test_proof_loop_local_report_surfaces_validate_current_route(self) -> None:
        assert validate_repo.validate_proof_loop_local_report_surfaces(REPO_ROOT) == []

    def test_receipt_intake_dry_review_surface_validates_current_route(self) -> None:
        assert validate_repo.validate_receipt_intake_dry_review_surface(REPO_ROOT) == []

    def test_receipt_intake_dry_review_rejects_published_posture(
        self, tmp_path: Path
    ) -> None:
        make_receipt_intake_dry_review_surface(tmp_path)
        review_path = tmp_path / validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME
        payload = json.loads(review_path.read_text(encoding="utf-8"))
        payload["publication_boundary"]["receipt_status"] = "published"
        write_json_payload(review_path, payload)

        issues = validate_repo.validate_receipt_intake_dry_review_surface(tmp_path)

        assert any(
            issue.location == "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json.publication_boundary"
            and "receipt_status must be 'not_published'" in issue.message
            for issue in issues
        )

    def test_receipt_intake_dry_review_rejects_publishable_envelope_shape(
        self, tmp_path: Path
    ) -> None:
        make_receipt_intake_dry_review_surface(tmp_path)
        review_path = tmp_path / validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME
        payload = json.loads(review_path.read_text(encoding="utf-8"))
        payload["event_kind"] = "eval_result_receipt"
        write_json_payload(review_path, payload)

        issues = validate_repo.validate_receipt_intake_dry_review_surface(tmp_path)

        assert any(
            issue.location == "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json"
            and "must not contain publishable receipt field 'event_kind'" in issue.message
            for issue in issues
        )

    def test_release_support_readiness_audit_surface_validates_current_route(self) -> None:
        assert validate_repo.validate_release_support_readiness_audit_surface(REPO_ROOT) == []

    def test_release_support_readiness_audit_rejects_goal_completion_claim(
        self, tmp_path: Path
    ) -> None:
        make_release_support_readiness_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["publication_boundary"]["goal_completion_status"] = "complete"
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_release_support_readiness_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json.publication_boundary"
            and "goal_completion_status must be 'not_complete'" in issue.message
            for issue in issues
        )

    def test_release_support_readiness_audit_rejects_missing_release_gate(
        self, tmp_path: Path
    ) -> None:
        make_release_support_readiness_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["verification_snapshot"] = [
            entry
            for entry in payload["verification_snapshot"]
            if entry["command"] != "python scripts/release_check.py"
        ]
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_release_support_readiness_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json.verification_snapshot"
            and "python scripts/release_check.py" in issue.message
            for issue in issues
        )

    def test_strategic_closeout_audit_surface_validates_current_route(self) -> None:
        assert validate_repo.validate_strategic_closeout_audit_surface(REPO_ROOT) == []

    def test_strategic_closeout_audit_rejects_goal_completion_claim(
        self, tmp_path: Path
    ) -> None:
        make_strategic_closeout_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.STRATEGIC_CLOSEOUT_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["goal_completion_status"] = "complete"
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_strategic_closeout_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json"
            and "goal_completion_status must be 'not_complete_pending_requirement_audit_and_landing_route'" in issue.message
            for issue in issues
        )

    def test_strategic_closeout_audit_rejects_missing_requirement_id(
        self, tmp_path: Path
    ) -> None:
        make_strategic_closeout_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.STRATEGIC_CLOSEOUT_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["requirements_review"] = [
            entry
            for entry in payload["requirements_review"]
            if entry["requirement_id"] != "phase_8_active_proof_loop"
        ]
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_strategic_closeout_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json.requirements_review"
            and "phase_8_active_proof_loop" in issue.message
            for issue in issues
        )

    def test_strategic_closeout_audit_rejects_missing_focused_gate(
        self, tmp_path: Path
    ) -> None:
        make_strategic_closeout_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.STRATEGIC_CLOSEOUT_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["verification_snapshot"] = [
            entry
            for entry in payload["verification_snapshot"]
            if entry["command"]
            != "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py tests/test_validate_repo.py -k strategic_closeout"
        ]
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_strategic_closeout_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json.verification_snapshot"
            and "mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py" in issue.message
            for issue in issues
        )

    def test_strategic_closeout_audit_rejects_absolute_plan_path(
        self, tmp_path: Path
    ) -> None:
        make_strategic_closeout_audit_surface(tmp_path)
        audit_path = tmp_path / validate_repo.STRATEGIC_CLOSEOUT_AUDIT_NAME
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["source_plan_ref"] = "/home/dionysus/private-note.md"
        write_json_payload(audit_path, payload)

        issues = validate_repo.validate_strategic_closeout_audit_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json"
            and "must not expose an absolute host path" in issue.message
            for issue in issues
        )

    def test_release_prep_pr_handoff_surface_validates_current_route(self) -> None:
        assert validate_repo.validate_release_prep_pr_handoff_surface(REPO_ROOT) == []

    def test_release_prep_pr_handoff_rejects_open_pr_claim(
        self, tmp_path: Path
    ) -> None:
        make_release_prep_pr_handoff_surface(tmp_path)
        handoff_path = tmp_path / validate_repo.RELEASE_PREP_PR_HANDOFF_NAME
        payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        payload["pre_handoff_github_status"]["pr_status"] = "opened"
        write_json_payload(handoff_path, payload)

        issues = validate_repo.validate_release_prep_pr_handoff_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json.pre_handoff_github_status"
            and "pre_handoff pr_status must be 'not_opened'" in issue.message
            for issue in issues
        )

    def test_release_prep_pr_handoff_rejects_missing_surface_group(
        self, tmp_path: Path
    ) -> None:
        make_release_prep_pr_handoff_surface(tmp_path)
        handoff_path = tmp_path / validate_repo.RELEASE_PREP_PR_HANDOFF_NAME
        payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        payload["changed_surface_groups"] = [
            entry
            for entry in payload["changed_surface_groups"]
            if entry["group_id"] != "active_proof_loop"
        ]
        write_json_payload(handoff_path, payload)

        issues = validate_repo.validate_release_prep_pr_handoff_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json.changed_surface_groups"
            and "active_proof_loop" in issue.message
            for issue in issues
        )

    def test_release_prep_pr_handoff_rejects_missing_landing_step(
        self, tmp_path: Path
    ) -> None:
        make_release_prep_pr_handoff_surface(tmp_path)
        handoff_path = tmp_path / validate_repo.RELEASE_PREP_PR_HANDOFF_NAME
        payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        payload["landing_steps"] = [
            item for item in payload["landing_steps"] if "watch GitHub Repo Validation" not in item
        ]
        write_json_payload(handoff_path, payload)

        issues = validate_repo.validate_release_prep_pr_handoff_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json.landing_steps"
            and "watch GitHub Repo Validation" in issue.message
            for issue in issues
        )

    def test_release_prep_pr_handoff_rejects_missing_focused_gate(
        self, tmp_path: Path
    ) -> None:
        make_release_prep_pr_handoff_surface(tmp_path)
        handoff_path = tmp_path / validate_repo.RELEASE_PREP_PR_HANDOFF_NAME
        payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        payload["verification_snapshot"] = [
            entry
            for entry in payload["verification_snapshot"]
            if entry["command"]
            != "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_validate_repo.py -k release_prep_pr_handoff"
        ]
        write_json_payload(handoff_path, payload)

        issues = validate_repo.validate_release_prep_pr_handoff_surface(tmp_path)

        assert any(
            issue.location == "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json.verification_snapshot"
            and "mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py" in issue.message
            for issue in issues
        )

    def test_proof_loop_smoke_report_rejects_missing_receipt_boundary(
        self, tmp_path: Path
    ) -> None:
        for relative_path in [
            "mechanics/proof-loop/README.md",
            "reports/README.md",
            "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
            "docs/decisions/README.md",
            "docs/decisions/0020-proof-loop-local-smoke-report.md",
            "docs/decisions/0030-proof-loop-route-smoke-part.md",
        ]:
            copy_repo_text(tmp_path, relative_path)

        report_path = tmp_path / validate_repo.PROOF_LOOP_SMOKE_REPORT_NAME
        report_path.write_text(
            report_path.read_text(encoding="utf-8").replace(
                "no eval result receipt",
                "receipt publication handled elsewhere",
            ),
            encoding="utf-8",
        )

        issues = validate_repo.validate_proof_loop_smoke_report_surfaces(tmp_path)

        assert any(
            issue.location == "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md"
            and "no eval result receipt" in issue.message
            for issue in issues
        )

    def test_agent_lane_surfaces_reject_root_local_spark_lane(
        self, tmp_path: Path
    ) -> None:
        write_text(
            tmp_path / ".agents" / "AGENTS.md",
            """
            # AGENTS.md

            `.agents/<lane>/` route. `.agents/skills/` support. `.agents/spark/`
            lane. This is not proof canon.

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
            Do not edit generated surfaces by hand.

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
            tmp_path / "docs" / "decisions" / "0017-spark-agent-lane-placement.md",
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
            tmp_path / "docs" / "PROOF_TOPOLOGY.md",
            """
            # Proof Topology

            Agent guidance uses .agents/ and .agents/spark/.
            """,
        )
        write_text(
            tmp_path / "docs" / "LEGACY_NAMING.md",
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

        issues = validate_repo.validate_agent_lane_surfaces(tmp_path)

        assert validate_repo.ValidationIssue(
            "Spark/",
            "root-local Spark lane must stay moved to .agents/spark/",
        ) in issues

    def test_agent_lane_surfaces_reject_spark_swarm_command_lines(
        self, tmp_path: Path
    ) -> None:
        for path_name in (
            ".agents/AGENTS.md",
            ".agents/spark/AGENTS.md",
            "docs/decisions/0017-spark-agent-lane-placement.md",
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

        issues = validate_repo.validate_agent_lane_surfaces(tmp_path)

        assert any(
            issue.location == ".agents/spark/SWARM.md"
            and "route executable commands to .agents/spark/AGENTS.md"
            in issue.message
            for issue in issues
        )
