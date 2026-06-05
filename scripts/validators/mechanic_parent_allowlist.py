"""Mechanic parent allowlist and legacy active-path guards."""

from __future__ import annotations

from pathlib import Path

from validators import mechanic_legacy_archive as mechanic_legacy_archive_validator
from validators import mechanic_parent_guidance as mechanic_parent_guidance_validator
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue
from validators.mechanic_parent_common import (
    DECISION_RECORDS_README_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    require_tokens,
)


MECHANIC_PARENT_ALLOWLIST_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0052-mechanic-parent-allowlist.md"
)
MECHANICS_ROOT_ALLOWED_FILES = (
    "AGENTS.md",
    "EVIDENCE_CLUSTERS.md",
    "README.md",
)
MECHANIC_ROUTE_CARD_FILES = tuple(
    route
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    for route in (
        f"mechanics/{parent_name}/AGENTS.md",
        f"mechanics/{parent_name}/README.md",
        f"mechanics/{parent_name}/DIRECTION.md",
        f"mechanics/{parent_name}/PARTS.md",
    )
)
MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Allowlist",
    "no invented parent packages",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "AoA-aligned",
    "evals-native",
    "validator allowlist",
    "Active parents are active, not merely plausible candidates",
)
FORBIDDEN_ACTIVE_MECHANICS_PATHS = (
    "mechanics/agon-proof",
    "mechanics/titan-canaries",
    "mechanics/proof-release",
    "mechanics/runtime-evidence",
    "mechanics/sibling-proof-refs",
    "mechanics/repair",
    "docs/decisions/0016-agon-proof-mechanic-package.md",
    "docs/decisions/0015-titan-canaries-mechanic-package.md",
    "docs/decisions/0014-proof-release-mechanic-package.md",
    "docs/decisions/0007-runtime-evidence-mechanic-package.md",
    "docs/decisions/0008-sibling-proof-refs-mechanic-package.md",
    "docs/RECURRENCE_PROOF_PROGRAM.md",
    "docs/RECURRENCE_CONTROL_PLANE_EVALS.md",
    "docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md",
    "docs/EVAL_INDEX_RECURRENCE_INSERT.md",
    "docs/EVAL_SELECTION_RECURRENCE_INSERT.md",
    "fixtures/recurrence-control-plane-integrity-v1",
    "schemas/recurrence-control-plane-integrity-dossier.schema.json",
    "examples/recurrence_control_plane_integrity.dossier.example.json",
    "scripts/run_recurrence_control_plane_integrity_eval.py",
    "scorers/recurrence_control_plane_integrity.py",
    "tests/test_recurrence_control_plane_integrity_eval_seed.py",
    "manifests/recurrence/component.recurrence-control-plane-integrity-eval.json",
    "manifests/recurrence/component.evals.portable-proof-beacons.json",
    "manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json",
    "docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md",
    "fixtures/return-anchor-v1",
    "fixtures/memo-recall-guardrail-v1",
    "fixtures/recursor-readiness-boundary-v1",
    "fixtures/stats-regrounding-boundary-v1",
    "scripts/run_recursor_readiness_boundary_eval.py",
    "scorers/recursor_readiness_boundary.py",
    "tests/test_recursor_readiness_boundary_eval_seed.py",
    "tests/test_stats_regrounding_boundary_eval.py",
    "tests/test_memo_recall_phase_alpha_report.py",
    "docs/PROGRESSION_EVIDENCE_MODEL.md",
    "docs/UNLOCK_PROOF_BRIDGE.md",
    "schemas/progression_evidence.schema.json",
    "schemas/unlock_proof_catalog.schema.json",
    "examples/progression_evidence.example.json",
    "generated/unlock_proof_cards.min.example.json",
    "docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md",
    "fixtures/a2a-summon-return-checkpoint-v1",
    "fixtures/long-horizon-restart-v1",
    "tests/test_a2a_summon_return_checkpoint_fixture.py",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
    "docs/EXPERIENCE_CERTIFICATION_EVAL_BUNDLES.md",
    "docs/ASSISTANT_CERTIFICATION_JUDGE.md",
    "docs/DEPLOYMENT_INTEGRITY_BUNDLES.md",
    "docs/POST_RELEASE_REGRESSION_VERDICT.md",
    "docs/ROLLBACK_DRILL_VERDICT_MODEL.md",
    "docs/ROLLBACK_TRIGGER_VERDICT.md",
    "docs/WATCHTOWER_ALARM_VERDICT_MODEL.md",
    "docs/ADOPTION_EVAL_BUNDLES.md",
    "docs/ADOPTION_COMPATIBILITY_VERDICT.md",
    "docs/AGONIC_ADOPTION_TRIAL_VERDICT.md",
    "docs/ASSISTANT_ADOPTION_CERTIFICATION_VERDICT.md",
    "docs/ROUTING_ADOPTION_VERDICT.md",
    "docs/SHADOW_ADOPTION_VERDICT.md",
    "docs/FEDERATION_HARVEST_EVAL_BUNDLES.md",
    "docs/KAG_PROMOTION_VERDICT_MODEL.md",
    "docs/OWNER_CONSENT_VERDICT.md",
    "docs/PATTERN_LINEAGE_INTEGRITY_BUNDLES.md",
    "docs/TOS_BOUNDARY_VERDICT_MODEL.md",
    "docs/AUTHORITY_RESOLUTION_VERDICT.md",
    "docs/APPEAL_REVIEW_VERDICT.md",
    "docs/CHARTER_AMENDMENT_EVALS.md",
    "docs/CONSTITUTION_RUNTIME_EVAL_BUNDLES.md",
    "docs/GOVERNANCE_VERDICT_BUNDLES.md",
    "docs/REPLAY_HISTORY_INTEGRITY_VERDICT.md",
    "docs/STAY_ORDER_ENFORCEMENT_VERDICT.md",
    "docs/TOS_DOSSIER_REVIEW_VERDICTS.md",
    "docs/VETO_LEGITIMACY_BUNDLES.md",
    "docs/VOTE_SEAL_INTEGRITY_VERDICT.md",
    "docs/BOUNDARY_GUARD_VERDICTS.md",
    "docs/GOVERNED_RELEASE_VERDICTS.md",
    "docs/HANDOFF_INTEGRITY_VERDICTS.md",
    "docs/INSTALLATION_SMOKE_EVALS.md",
    "docs/MULTI_OFFICE_RELEASE_TRAIN_EVALS.md",
    "docs/OFFICE_SCOPE_FIDELITY_VERDICTS.md",
    "docs/REPLAY_AUDIT_VERDICTS.md",
    "docs/ROLLBACK_DRILL_VERDICTS.md",
    "docs/SERVICE_MESH_REGRESSION_VERDICTS.md",
    "fixtures/experience-verdict-protocol-integrity-v1",
    "fixtures/experience-certification-gate-integrity-v1",
    "fixtures/memo-reviewed-candidate-adoption-guardrail-v1",
    "fixtures/compost-provenance-v1",
    "mechanics/experience/parts/adoption-federation/fixtures/memo-reviewed-candidate-adoption-guardrail-v1",
    "tests/test_experience_protocol_integrity.py",
    "tests/test_experience_certification_gate_integrity.py",
    "tests/test_experience_wave2_seed_contracts.py",
    "tests/test_experience_wave3_seed_contracts.py",
    "tests/test_experience_wave4_seed_contracts.py",
    "tests/test_experience_wave5_seed_contracts.py",
    "docs/STRESS_RECOVERY_WINDOW_EVALS.md",
    "fixtures/stress-recovery-window-bounded-v1",
    "fixtures/repair-boundedness-v1",
    "schemas/antifragility_eval_report_v1.json",
    "schemas/stress_recovery_window_eval_report_v1.json",
    "fixtures/candidate-lineage-v1",
    "fixtures/owner-fit-routing-v1",
)


def validate_mechanics_parent_allowlist(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        issues.append(ValidationIssue("mechanics", "mechanics directory is missing"))
        return issues

    allowed_files = set(MECHANICS_ROOT_ALLOWED_FILES)
    allowed_parents = set(mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in mechanic_legacy_archive_validator.validate_mechanic_legacy_skeleton_surfaces(
            repo_root
        )
    )
    issues.extend(
        mechanic_parent_guidance_validator.validate_mechanic_parent_guidance_boundary(
            repo_root
        )
    )

    for path in sorted(mechanics_root.iterdir(), key=lambda item: item.name):
        relative = path.relative_to(repo_root).as_posix()
        if path.is_file():
            if path.name not in allowed_files:
                issues.append(
                    ValidationIssue(
                        relative,
                        "unexpected mechanics root file must be routed through an allowed source surface",
                    )
                )
            continue
        if not path.is_dir():
            issues.append(
                ValidationIssue(
                    relative,
                    "unexpected mechanics root entry must be a file route card or parent directory",
                )
            )
            continue
        if path.name not in allowed_parents:
            issues.append(
                ValidationIssue(
                    relative,
                    "mechanic parent must be declared in the evidence-cluster allowlist",
                )
            )

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        if not (mechanics_root / parent_name).is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}",
                    "declared mechanic parent directory is missing",
                )
            )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "Active Packages",
            "Package taxonomy requires source surfaces, inputs, outputs, boundaries",
            "Provenance Bridge And Archive Boundary",
            "`PROVENANCE.md`",
            "legacy archive",
            "archive-local accounting",
            "archive internals",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=tuple(f"`{parent_name}`" for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
        tokens=MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name in MECHANIC_ROUTE_CARD_FILES:
        if not (repo_root / path_name).is_file():
            issues.append(
                ValidationIssue(
                    path_name,
                    "active mechanic parent must expose AGENTS.md, README.md, DIRECTION.md, and PARTS.md",
                )
            )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "top-level mechanics parents are validator allowlisted",
            "mechanics/EVIDENCE_CLUSTERS.md",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(MECHANIC_PARENT_ALLOWLIST_DECISION_NAME, "Mechanic Parent Allowlist"),
        issues=issues,
    )
    return issues


def validate_forbidden_active_mechanics_paths(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name in FORBIDDEN_ACTIVE_MECHANICS_PATHS:
        if (repo_root / path_name).exists():
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy mechanics path must not exist as an active route",
                )
            )
    return issues


__all__ = (
    "MECHANIC_PARENT_ALLOWLIST_DECISION_NAME",
    "MECHANICS_ROOT_ALLOWED_FILES",
    "MECHANIC_ROUTE_CARD_FILES",
    "MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS",
    "FORBIDDEN_ACTIVE_MECHANICS_PATHS",
    "validate_mechanics_parent_allowlist",
    "validate_forbidden_active_mechanics_paths",
)
