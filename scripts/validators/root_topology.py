"""Root source/topology validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    docs_decisions,
    docs_routes,
    docs_topology,
    eval_bundles,
    generated_parity,
    mechanic_legacy as mechanic_legacy_validator,
    mechanic_parts as mechanic_parts_validator,
    mechanics_routes as mechanics_routes_validator,
    questbook as questbook_validator,
    report_index as report_index_validator,
    root_authority as root_authority_validator,
    root_context,
    root_guidance as root_guidance_validator,
    root_route_cards as root_route_cards_validator,
    route_residue as route_residue_validator,
    validation_topology,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def _tuple_issues(module_issues: Sequence[tuple[str, str]]) -> list[ValidationIssue]:
    return [
        ValidationIssue(location, message)
        for location, message in module_issues
    ]


def root_route_card_context() -> root_route_cards_validator.RootRouteCardContext:
    return root_route_cards_validator.RootRouteCardContext(
        require_tokens=root_context.context_require_tokens,
    )


def route_residue_context() -> route_residue_validator.RouteResidueContext:
    return route_residue_validator.RouteResidueContext(
        require_tokens=root_context.context_require_tokens,
    )


def questbook_route_context() -> questbook_validator.QuestbookRouteContext:
    return questbook_validator.QuestbookRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_legacy_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def validate_root_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(root_authority_validator.validate_agent_index_surface(repo_root))
    issues.extend(root_guidance_validator.validate_root_readme_surface_role(repo_root))
    issues.extend(
        root_authority_validator.validate_memory_consumer_proof_boundary_surfaces(
            repo_root
        )
    )
    issues.extend(root_guidance_validator.validate_eval_philosophy_route_map_surface(repo_root))
    issues.extend(root_guidance_validator.validate_score_semantics_guide_surface(repo_root))
    issues.extend(root_guidance_validator.validate_eval_review_guide_surface(repo_root))
    issues.extend(root_guidance_validator.validate_blind_spot_disclosure_guide_surface(repo_root))
    issues.extend(root_guidance_validator.validate_docs_readme_route_map(repo_root))
    issues.extend(root_guidance_validator.validate_portable_eval_boundary_guide_surface(repo_root))
    issues.extend(root_guidance_validator.validate_closeout_writeback_ingress_surface(repo_root))
    issues.extend(root_guidance_validator.validate_contributing_route_surface(repo_root))
    issues.extend(root_authority_validator.validate_read_model_command_ownership(repo_root))
    issues.extend(root_guidance_validator.validate_releasing_route_map_surface(repo_root))
    issues.extend(_module_issues(eval_bundles.validate_source_eval_tree_topology_surfaces(repo_root)))
    issues.extend(_tuple_issues(eval_bundles.validate_eval_bundle_topology(repo_root)))
    issues.extend(root_authority_validator.validate_audit_surface_role(repo_root))
    issues.extend(root_authority_validator.validate_github_agent_surface(repo_root))
    issues.extend(root_authority_validator.validate_index_surface_roles(repo_root))
    issues.extend(_module_issues(eval_bundles.validate_eval_source_entry_operating_cards(repo_root)))
    issues.extend(root_authority_validator.validate_validator_surface_role(repo_root))
    issues.extend(
        _module_issues(
            mechanic_parts_validator.validate_mechanic_index_surface_roles(
                repo_root
            )
        )
    )
    issues.extend(root_authority_validator.validate_root_design_surfaces(repo_root))
    issues.extend(_tuple_issues(docs_topology.validate_docs_topology(repo_root)))
    issues.extend(_tuple_issues(docs_routes.validate_docs_routes(repo_root)))
    issues.extend(_tuple_issues(validation_topology.validate_validation_topology(repo_root)))
    issues.extend(_tuple_issues(docs_decisions.validate_decision_index_surfaces(repo_root)))
    issues.extend(_tuple_issues(generated_parity.validate_generated_parity(repo_root)))
    issues.extend(root_authority_validator.validate_decision_status_lines(repo_root))
    issues.extend(
        _module_issues(
            root_route_cards_validator.validate_root_route_card_districts(
                repo_root,
                context=root_route_card_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_root_authored_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_decision_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_repo_config_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_source_bundle_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(root_authority_validator.validate_agent_lane_surfaces(repo_root))
    issues.extend(
        _module_issues(
            questbook_validator.validate_quest_route_surfaces(
                repo_root,
                context=questbook_route_context(),
            )
        )
    )
    issues.extend(root_authority_validator.validate_proof_topology_surfaces(repo_root))
    issues.extend(root_authority_validator.validate_legacy_naming_surfaces(repo_root))
    issues.extend(mechanics_routes_validator.validate_mechanics_surfaces(repo_root))
    issues.extend(
        _module_issues(
            mechanic_legacy_validator.validate_active_legacy_parent_wording(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_validator.validate_generated_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(_module_issues(report_index_validator.validate_eval_report_index_route_surfaces(repo_root)))
    return issues
