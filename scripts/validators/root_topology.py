"""Root source/topology validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    active_legacy_parent_wording as active_legacy_parent_wording_validator,
    decision_index_surfaces as decision_index_surfaces_validator,
    docs_routes,
    docs_topology,
    eval_entry_cards as eval_entry_cards_validator,
    eval_tree_topology,
    generated_route_surfaces,
    mechanic_part_role_headings as mechanic_part_role_headings_validator,
    mechanic_provenance_bridge as mechanic_provenance_bridge_validator,
    mechanics_routes as mechanics_routes_validator,
    questbook_routes as questbook_routes_validator,
    report_index as report_index_validator,
    root_agent_index as root_agent_index_validator,
    root_agent_lanes as root_agent_lanes_validator,
    root_audit_routes as root_audit_routes_validator,
    root_context,
    root_decision_status as root_decision_status_validator,
    root_design_docs as root_design_docs_validator,
    root_eval_guides as root_eval_guides_validator,
    root_frontdoor_guidance as root_frontdoor_guidance_validator,
    root_index_surfaces as root_index_surfaces_validator,
    root_legacy_bridge_residue as root_legacy_bridge_residue_validator,
    root_legacy_external_leakage as root_legacy_external_leakage_validator,
    root_legacy_naming as root_legacy_naming_validator,
    root_memory_boundary as root_memory_boundary_validator,
    root_operations_guidance as root_operations_guidance_validator,
    root_proof_topology as root_proof_topology_validator,
    root_read_model_commands as root_read_model_commands_validator,
    root_release_guidance as root_release_guidance_validator,
    root_route_cards as root_route_cards_validator,
    root_validator_surfaces as root_validator_surfaces_validator,
    route_residue_common as route_residue_common_validator,
    route_residue_decisions as route_residue_decisions_validator,
    route_residue_generated as route_residue_generated_validator,
    route_residue_repo_config as route_residue_repo_config_validator,
    route_residue_root_authored as route_residue_root_authored_validator,
    route_residue_source_bundle as route_residue_source_bundle_validator,
    validation_lane_manifest as validation_lane_manifest_validator,
    validation_script_inventory as validation_script_inventory_validator,
    validation_test_inventory as validation_test_inventory_validator,
    validation_topology_docs as validation_topology_docs_validator,
    validation_validator_inventory as validation_validator_inventory_validator,
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


def route_residue_context() -> route_residue_common_validator.RouteResidueContext:
    return route_residue_common_validator.RouteResidueContext(
        require_tokens=root_context.context_require_tokens,
    )


def questbook_route_context() -> questbook_routes_validator.QuestbookRouteContext:
    return questbook_routes_validator.QuestbookRouteContext(
        require_tokens=root_context.context_require_tokens,
        provenance_tokens=mechanic_provenance_bridge_validator.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
    )


def validate_root_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(root_agent_index_validator.validate_agent_index_surface(repo_root))
    issues.extend(root_frontdoor_guidance_validator.validate_root_readme_surface_role(repo_root))
    issues.extend(
        root_memory_boundary_validator.validate_memory_consumer_proof_boundary_surfaces(
            repo_root
        )
    )
    issues.extend(root_eval_guides_validator.validate_eval_philosophy_route_map_surface(repo_root))
    issues.extend(root_eval_guides_validator.validate_score_semantics_guide_surface(repo_root))
    issues.extend(root_eval_guides_validator.validate_eval_review_guide_surface(repo_root))
    issues.extend(root_eval_guides_validator.validate_blind_spot_disclosure_guide_surface(repo_root))
    issues.extend(root_frontdoor_guidance_validator.validate_docs_readme_route_map(repo_root))
    issues.extend(root_eval_guides_validator.validate_portable_eval_boundary_guide_surface(repo_root))
    issues.extend(root_operations_guidance_validator.validate_closeout_writeback_ingress_surface(repo_root))
    issues.extend(root_operations_guidance_validator.validate_contributing_route_surface(repo_root))
    issues.extend(root_read_model_commands_validator.validate_read_model_command_ownership(repo_root))
    issues.extend(root_release_guidance_validator.validate_releasing_route_map_surface(repo_root))
    issues.extend(_module_issues(eval_tree_topology.validate_source_eval_tree_topology_surfaces(repo_root)))
    issues.extend(_tuple_issues(eval_tree_topology.validate_eval_bundle_topology(repo_root)))
    issues.extend(root_audit_routes_validator.validate_audit_surface_role(repo_root))
    issues.extend(root_audit_routes_validator.validate_github_agent_surface(repo_root))
    issues.extend(root_index_surfaces_validator.validate_index_surface_roles(repo_root))
    issues.extend(
        _module_issues(
            eval_entry_cards_validator.validate_eval_source_entry_operating_cards(
                repo_root
            )
        )
    )
    issues.extend(root_validator_surfaces_validator.validate_validator_surface_role(repo_root))
    issues.extend(
        _module_issues(
            mechanic_part_role_headings_validator.validate_mechanic_index_surface_roles(
                repo_root
            )
        )
    )
    issues.extend(root_design_docs_validator.validate_root_design_surfaces(repo_root))
    issues.extend(_tuple_issues(docs_topology.validate_docs_topology(repo_root)))
    issues.extend(_tuple_issues(docs_routes.validate_docs_routes(repo_root)))
    issues.extend(_tuple_issues(validation_topology_docs_validator.validate_validation_topology_docs(repo_root)))
    issues.extend(_tuple_issues(validation_lane_manifest_validator.validate_validation_lane_manifest(repo_root)))
    issues.extend(_tuple_issues(validation_validator_inventory_validator.validate_validator_inventory(repo_root)))
    issues.extend(_tuple_issues(validation_script_inventory_validator.validate_script_inventory(repo_root)))
    issues.extend(_tuple_issues(validation_test_inventory_validator.validate_test_inventory(repo_root)))
    issues.extend(_tuple_issues(decision_index_surfaces_validator.validate_decision_index_surfaces(repo_root)))
    issues.extend(_tuple_issues(generated_route_surfaces.validate_generated_route_surfaces(repo_root)))
    issues.extend(root_decision_status_validator.validate_decision_status_lines(repo_root))
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
            route_residue_root_authored_validator.validate_root_authored_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_decisions_validator.validate_decision_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_repo_config_validator.validate_repo_config_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_source_bundle_validator.validate_source_bundle_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(root_agent_lanes_validator.validate_agent_lane_surfaces(repo_root))
    issues.extend(
        _module_issues(
            questbook_routes_validator.validate_quest_route_surfaces(
                repo_root,
                context=questbook_route_context(),
            )
        )
    )
    issues.extend(root_proof_topology_validator.validate_proof_topology_surfaces(repo_root))
    issues.extend(root_legacy_naming_validator.validate_legacy_naming_posture_surfaces(repo_root))
    issues.extend(
        root_legacy_bridge_residue_validator.validate_legacy_single_bridge_residue_surfaces(
            repo_root
        )
    )
    issues.extend(
        root_legacy_external_leakage_validator.validate_legacy_external_leakage_surfaces(
            repo_root
        )
    )
    issues.extend(mechanics_routes_validator.validate_mechanics_surfaces(repo_root))
    issues.extend(
        _module_issues(
            active_legacy_parent_wording_validator.validate_active_legacy_parent_wording(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            route_residue_generated_validator.validate_generated_route_residue_surfaces(
                repo_root,
                context=route_residue_context(),
            )
        )
    )
    issues.extend(_module_issues(report_index_validator.validate_eval_report_index_route_surfaces(repo_root)))
    return issues
