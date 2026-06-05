"""Mechanic route-domain validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    agon_routes as agon_routes_validator,
    antifragility_routes as antifragility_routes_validator,
    audit_routes as audit_routes_validator,
    boundary_bridge_canary as boundary_bridge_canary_validator,
    boundary_bridge_routes as boundary_bridge_routes_validator,
    boundary_bridge_workflow as boundary_bridge_workflow_validator,
    checkpoint_routes as checkpoint_routes_validator,
    comparison_spine_routes as comparison_spine_routes_validator,
    distillation_routes as distillation_routes_validator,
    experience_routes as experience_routes_validator,
    growth_cycle_routes as growth_cycle_routes_validator,
    mechanic_evidence_dimensions as mechanic_evidence_dimensions_validator,
    mechanic_evidence_route_refs as mechanic_evidence_route_refs_validator,
    mechanic_parent_allowlist as mechanic_parent_allowlist_validator,
    mechanic_parent_direction as mechanic_parent_direction_validator,
    mechanic_parent_index as mechanic_parent_index_validator,
    mechanic_parent_registry as mechanic_parent_registry_validator,
    mechanic_part_contract_index as mechanic_part_contract_index_validator,
    mechanic_part_readme_contract as mechanic_part_readme_contract_validator,
    mechanic_part_validation_commands as mechanic_part_validation_commands_validator,
    mechanic_parts_index_sync as mechanic_parts_index_sync_validator,
    mechanic_provenance_bridge as mechanic_provenance_bridge_validator,
    mechanics as mechanics_validator,
    method_growth_routes as method_growth_routes_validator,
    proof_infra_routes as proof_infra_validator,
    proof_loop_local_report as proof_loop_local_report_validator,
    proof_loop_routes as proof_loop_routes_validator,
    proof_loop_smoke_report as proof_loop_smoke_report_validator,
    proof_object_routes as proof_object_routes_validator,
    publication_receipts_routes as publication_receipts_routes_validator,
    questbook_routes as questbook_routes_validator,
    recurrence_routes as recurrence_routes_validator,
    release_support_routes as release_support_routes_validator,
    root_route_tokens,
    route_residue_active_mechanics as route_residue_active_mechanics_validator,
    route_residue_common as route_residue_common_validator,
    route_residue_mechanic_payload as route_residue_mechanic_payload_validator,
    rpg_routes as rpg_routes_validator,
    titan_routes as titan_routes_validator,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def _route_residue_context() -> route_residue_common_validator.RouteResidueContext:
    return route_residue_common_validator.RouteResidueContext(
        require_tokens=root_route_tokens.context_require_tokens,
    )


def _recurrence_route_context() -> recurrence_routes_validator.RecurrenceRouteContext:
    return recurrence_routes_validator.RecurrenceRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _checkpoint_route_context() -> checkpoint_routes_validator.CheckpointRouteContext:
    return checkpoint_routes_validator.CheckpointRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _experience_route_context() -> experience_routes_validator.ExperienceRouteContext:
    return experience_routes_validator.ExperienceRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _antifragility_route_context() -> antifragility_routes_validator.AntifragilityRouteContext:
    return antifragility_routes_validator.AntifragilityRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _method_growth_route_context() -> method_growth_routes_validator.MethodGrowthRouteContext:
    return method_growth_routes_validator.MethodGrowthRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _rpg_route_context() -> rpg_routes_validator.RpgRouteContext:
    return rpg_routes_validator.RpgRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _growth_cycle_route_context() -> growth_cycle_routes_validator.GrowthCycleRouteContext:
    return growth_cycle_routes_validator.GrowthCycleRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _distillation_route_context() -> distillation_routes_validator.DistillationRouteContext:
    return distillation_routes_validator.DistillationRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _titan_route_context() -> titan_routes_validator.TitanRouteContext:
    return titan_routes_validator.TitanRouteContext(require_tokens=root_route_tokens.context_require_tokens)


def _agon_route_context() -> agon_routes_validator.AgonRouteContext:
    return agon_routes_validator.AgonRouteContext(require_tokens=root_route_tokens.context_require_tokens)


def _questbook_route_context() -> questbook_routes_validator.QuestbookRouteContext:
    return questbook_routes_validator.QuestbookRouteContext(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def validate_mechanics_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        _module_issues(
            mechanic_parent_registry_validator.validate_mechanic_parent_class_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_evidence_dimensions_validator.validate_mechanic_evidence_dimension_ledger(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_evidence_route_refs_validator.validate_mechanic_evidence_route_refs(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parent_allowlist_validator.validate_mechanics_parent_allowlist(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parent_direction_validator.validate_mechanic_parent_direction_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parent_index_validator.validate_mechanic_index_command_ownership(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parent_index_validator.validate_mechanic_lower_parts_index_operating_cards(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parent_allowlist_validator.validate_forbidden_active_mechanics_paths(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_part_contract_index_validator.validate_mechanic_part_contract_index_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_part_readme_contract_validator.validate_mechanic_part_readme_contract_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_parts_index_sync_validator.validate_mechanic_parts_index_sync_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_part_validation_commands_validator.validate_mechanic_part_validation_command_surfaces(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            mechanic_provenance_bridge_validator.validate_mechanic_legacy_bridge_surfaces(repo_root)
        )
    )
    issues.extend(
        _module_issues(mechanics_validator.validate_mechanic_root_district_recon_surfaces(repo_root))
    )
    issues.extend(
        _module_issues(mechanics_validator.validate_root_authored_surface_classification(repo_root))
    )
    issues.extend(
        _module_issues(
            route_residue_active_mechanics_validator.validate_active_mechanic_route_residue_surfaces(
                repo_root,
                context=_route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue_surfaces(
                repo_root,
                context=_route_residue_context(),
            )
        )
    )
    issues.extend(_module_issues(mechanics_validator.validate_mechanics_root_route_surfaces(repo_root)))
    issues.extend(_module_issues(proof_object_routes_validator.validate_proof_object_route_surfaces(repo_root)))
    issues.extend(_module_issues(proof_loop_routes_validator.validate_proof_loop_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(
            proof_loop_smoke_report_validator.validate_proof_loop_smoke_report_surfaces(repo_root)
        )
    )
    issues.extend(
        _module_issues(
            proof_loop_local_report_validator.validate_proof_loop_local_report_surfaces(repo_root)
        )
    )
    issues.extend(
        _module_issues(comparison_spine_routes_validator.validate_comparison_spine_route_surfaces(repo_root))
    )
    issues.extend(_module_issues(proof_infra_validator.validate_proof_infra_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(publication_receipts_routes_validator.validate_publication_receipts_route_surfaces(repo_root))
    )
    issues.extend(_module_issues(release_support_routes_validator.validate_release_support_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(
            titan_routes_validator.validate_titan_route_surfaces(
                repo_root,
                context=_titan_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            agon_routes_validator.validate_agon_route_surfaces(
                repo_root,
                context=_agon_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            recurrence_routes_validator.validate_recurrence_route_surfaces(
                repo_root,
                context=_recurrence_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            checkpoint_routes_validator.validate_checkpoint_route_surfaces(
                repo_root,
                context=_checkpoint_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            experience_routes_validator.validate_experience_route_surfaces(
                repo_root,
                context=_experience_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            antifragility_routes_validator.validate_antifragility_route_surfaces(
                repo_root,
                context=_antifragility_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            method_growth_routes_validator.validate_method_growth_route_surfaces(
                repo_root,
                context=_method_growth_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            rpg_routes_validator.validate_rpg_route_surfaces(
                repo_root,
                context=_rpg_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            growth_cycle_routes_validator.validate_growth_cycle_route_surfaces(
                repo_root,
                context=_growth_cycle_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            distillation_routes_validator.validate_distillation_route_surfaces(
                repo_root,
                context=_distillation_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            questbook_routes_validator.validate_questbook_route_surfaces(
                repo_root,
                context=_questbook_route_context(),
            )
        )
    )
    issues.extend(_module_issues(audit_routes_validator.validate_audit_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(boundary_bridge_routes_validator.validate_boundary_bridge_route_surfaces(repo_root))
    )
    issues.extend(
        _module_issues(boundary_bridge_workflow_validator.validate_repo_validation_workflow_surface(repo_root))
    )
    issues.extend(
        _module_issues(boundary_bridge_canary_validator.validate_sibling_canary_matrix_surface(repo_root))
    )
    return issues
