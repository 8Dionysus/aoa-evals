"""Mechanic route-domain validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

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
    mechanic_legacy as mechanic_legacy_validator,
    mechanic_parents as mechanic_parents_validator,
    mechanic_parts as mechanic_parts_validator,
    mechanics as mechanics_validator,
    method_growth as method_growth_validator,
    proof_infra as proof_infra_validator,
    proof_loop as proof_loop_validator,
    proof_object as proof_object_validator,
    publication_receipts as publication_receipts_validator,
    questbook as questbook_validator,
    recurrence as recurrence_validator,
    release_support as release_support_validator,
    root_context,
    route_residue as route_residue_validator,
    rpg as rpg_validator,
    titan as titan_validator,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def _route_residue_context() -> route_residue_validator.RouteResidueContext:
    return route_residue_validator.RouteResidueContext(
        require_tokens=root_context.context_require_tokens,
    )


def _recurrence_route_context() -> recurrence_validator.RecurrenceRouteContext:
    return recurrence_validator.RecurrenceRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _checkpoint_route_context() -> checkpoint_validator.CheckpointRouteContext:
    return checkpoint_validator.CheckpointRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _experience_route_context() -> experience_validator.ExperienceRouteContext:
    return experience_validator.ExperienceRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _antifragility_route_context() -> antifragility_validator.AntifragilityRouteContext:
    return antifragility_validator.AntifragilityRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _method_growth_route_context() -> method_growth_validator.MethodGrowthRouteContext:
    return method_growth_validator.MethodGrowthRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _rpg_route_context() -> rpg_validator.RpgRouteContext:
    return rpg_validator.RpgRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _growth_cycle_route_context() -> growth_cycle_validator.GrowthCycleRouteContext:
    return growth_cycle_validator.GrowthCycleRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _distillation_route_context() -> distillation_validator.DistillationRouteContext:
    return distillation_validator.DistillationRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def _titan_route_context() -> titan_validator.TitanRouteContext:
    return titan_validator.TitanRouteContext(require_tokens=root_context.context_require_tokens)


def _agon_route_context() -> agon_validator.AgonRouteContext:
    return agon_validator.AgonRouteContext(require_tokens=root_context.context_require_tokens)


def _questbook_route_context() -> questbook_validator.QuestbookRouteContext:
    return questbook_validator.QuestbookRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def validate_mechanics_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(_module_issues(mechanic_parents_validator.validate_mechanic_parent_surfaces(repo_root)))
    issues.extend(_module_issues(mechanic_parts_validator.validate_mechanic_part_surfaces(repo_root)))
    issues.extend(
        _module_issues(
            mechanic_legacy_validator.validate_mechanic_legacy_bridge_surfaces(repo_root)
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
            route_residue_validator.validate_active_mechanic_route_residue_surfaces(
                repo_root,
                context=_route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_mechanic_payload_route_residue_surfaces(
                repo_root,
                context=_route_residue_context(),
            )
        )
    )
    issues.extend(_module_issues(mechanics_validator.validate_mechanics_root_surfaces(repo_root)))
    issues.extend(_module_issues(proof_object_validator.validate_proof_object_route_surfaces(repo_root)))
    issues.extend(_module_issues(proof_loop_validator.validate_proof_loop_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(comparison_spine_validator.validate_comparison_spine_route_surfaces(repo_root))
    )
    issues.extend(_module_issues(proof_infra_validator.validate_proof_infra_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(publication_receipts_validator.validate_publication_receipts_route_surfaces(repo_root))
    )
    issues.extend(_module_issues(release_support_validator.validate_release_support_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(
            titan_validator.validate_titan_route_surfaces(
                repo_root,
                context=_titan_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            agon_validator.validate_agon_route_surfaces(
                repo_root,
                context=_agon_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            recurrence_validator.validate_recurrence_route_surfaces(
                repo_root,
                context=_recurrence_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            checkpoint_validator.validate_checkpoint_route_surfaces(
                repo_root,
                context=_checkpoint_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            experience_validator.validate_experience_route_surfaces(
                repo_root,
                context=_experience_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            antifragility_validator.validate_antifragility_route_surfaces(
                repo_root,
                context=_antifragility_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            method_growth_validator.validate_method_growth_route_surfaces(
                repo_root,
                context=_method_growth_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            rpg_validator.validate_rpg_route_surfaces(
                repo_root,
                context=_rpg_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            growth_cycle_validator.validate_growth_cycle_route_surfaces(
                repo_root,
                context=_growth_cycle_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            distillation_validator.validate_distillation_route_surfaces(
                repo_root,
                context=_distillation_route_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            questbook_validator.validate_questbook_route_surfaces(
                repo_root,
                context=_questbook_route_context(),
            )
        )
    )
    issues.extend(_module_issues(audit_validator.validate_audit_route_surfaces(repo_root)))
    issues.extend(
        _module_issues(boundary_bridge_validator.validate_boundary_bridge_route_surfaces(repo_root))
    )
    issues.extend(
        _module_issues(boundary_bridge_validator.validate_repo_validation_workflow_surface(repo_root))
    )
    issues.extend(
        _module_issues(boundary_bridge_validator.validate_sibling_canary_matrix_surface(repo_root))
    )
    return issues
