#!/usr/bin/env python3
"""Local validator and catalog builder helpers for aoa-evals source packages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Sequence

import validate_nested_agents
from validators import (
    eval_entry_routes as eval_entry_routes_validator,
    eval_starter_surfaces as eval_starter_surfaces_validator,
    generated_readouts as generated_readouts_validator,
    observability_readouts as observability_readouts_validator,
    phase_alpha_readouts as phase_alpha_readouts_validator,
    questbook_obligation_index as questbook_obligation_index_validator,
    questbook_projection_parity as questbook_projection_parity_validator,
    questbook_progression as questbook_progression_validator,
    questbook_schema_lifecycle as questbook_schema_lifecycle_validator,
    questbook_source_records as questbook_source_records_validator,
    readout_contexts,
    root_context,
    root_topology as root_topology_validator,
    runtime_readouts as runtime_readouts_validator,
    source_eval_collection as source_eval_collection_validator,
    source_eval_domains,
    titan_canary as titan_canary_validator,
)
from validators.common import ValidationIssue

REPO_ROOT = root_context.REPO_ROOT


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-evals source packages.")
    parser.add_argument(
        "--eval",
        help="Validate a single eval bundle by directory name.",
    )
    return parser.parse_args(argv)

def validator_module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]



def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)

def validate_repo_wide_readouts(
    repo_root: Path,
    records: Sequence[Any],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    runtime_context = readout_contexts.runtime_audit_context()
    generated_context = readout_contexts.generated_read_model_context()

    issues.extend(
        runtime_readouts_validator.validate_repo_wide_runtime_readout_surfaces(
            repo_root,
            records,
            context=runtime_context,
        )
    )
    issues.extend(observability_readouts_validator.validate_observability_readout_surfaces(repo_root))
    issues.extend(phase_alpha_readouts_validator.validate_phase_alpha_readout_surfaces(repo_root))
    issues.extend(
        validator_module_issues(titan_canary_validator.validate_titan_canary_surfaces(repo_root))
    )
    issues.extend(
        generated_readouts_validator.validate_generated_readout_surfaces(
            repo_root,
            records,
            context=generated_context,
        )
    )
    return issues

def validate_target_eval_readouts(
    repo_root: Path,
    records: Sequence[Any],
    *,
    target_evals: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    runtime_context = readout_contexts.runtime_audit_context()
    generated_context = readout_contexts.generated_read_model_context()

    issues.extend(
        runtime_readouts_validator.validate_target_runtime_readout_surfaces(
            repo_root,
            records,
            target_eval_names=set(target_evals),
            context=runtime_context,
        )
    )
    issues.extend(
        generated_readouts_validator.validate_generated_readout_surfaces(
            repo_root,
            records,
            context=generated_context,
            target_eval_names=target_evals,
        )
    )
    return issues

def run_validation(
    repo_root: Path,
    eval_name: str | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if repo_root.resolve() == REPO_ROOT.resolve() and eval_name is None:
        issues.extend(root_topology_validator.validate_root_topology_surfaces(repo_root))
    source_evals_dir_exists = (
        repo_root / source_eval_collection_validator.SOURCE_EVALS_DIR_NAME
    ).is_dir()
    try:
        all_eval_names = source_eval_collection_validator.discover_eval_names(repo_root)
    except FileNotFoundError:
        issues.append(
            ValidationIssue(
                source_eval_collection_validator.SOURCE_EVALS_DIR_NAME,
                "directory is missing",
            )
        )
        all_eval_names = []
    starter_issues: list[Any] = []
    starter_names = eval_starter_surfaces_validator.load_starter_eval_names(
        repo_root,
        starter_issues,
    )
    issues.extend(validator_module_issues(starter_issues))
    starter_set = set(starter_names)

    if eval_name is not None:
        if eval_name not in all_eval_names:
            raise ValueError(f"unknown eval '{eval_name}'")
        target_evals = [eval_name]
        selected_evals = {eval_name}
        selected_starter_evals = selected_evals.intersection(starter_set)
    else:
        target_evals = all_eval_names
        selected_evals = None
        selected_starter_evals = None

    if all_eval_names:
        source_issues, records = source_eval_collection_validator.collect_catalog_records(
            repo_root,
            target_evals,
            dependency_roots=source_eval_domains.source_eval_dependency_roots(),
        )
    else:
        source_issues, records = [], []
    issues.extend(source_issues)

    if source_evals_dir_exists:
        issues.extend(
            validator_module_issues(
                eval_entry_routes_validator.validate_source_eval_entry_surfaces(
                    repo_root,
                    starter_names=starter_names,
                    selected_evals=selected_evals,
                    selected_starter_evals=selected_starter_evals,
                )
            )
        )
    if source_evals_dir_exists and not source_issues:
        issues.extend(
            source_eval_domains.validate_source_eval_doctrine_surfaces(
                repo_root,
                records,
                selected_evals=selected_evals,
            )
        )

    if source_evals_dir_exists and eval_name is None and not source_issues:
        all_source_issues, all_records = (
            source_eval_collection_validator.collect_catalog_records(
                repo_root,
                dependency_roots=source_eval_domains.source_eval_dependency_roots(),
            )
        )
        if not all_source_issues:
            issues.extend(validate_repo_wide_readouts(repo_root, all_records))
    elif source_evals_dir_exists and eval_name is not None and not source_issues:
        issues.extend(validate_target_eval_readouts(repo_root, records, target_evals=target_evals))

    quest_schema_validation = (
        questbook_schema_lifecycle_validator.validate_quest_schema_lifecycle_surfaces(
            repo_root
        )
    )
    issues.extend(validator_module_issues(quest_schema_validation.issues))
    quest_source_validation = (
        questbook_source_records_validator.validate_quest_source_records(repo_root)
    )
    issues.extend(validator_module_issues(quest_source_validation.issues))
    issues.extend(
        validator_module_issues(
            questbook_obligation_index_validator.validate_questbook_obligation_index(
                repo_root,
                active_quest_ids=quest_source_validation.active_quest_ids,
                closed_quest_ids=quest_source_validation.closed_quest_ids,
                needs_orchestrator_alignment_doc=(
                    quest_source_validation.needs_orchestrator_alignment_doc
                ),
            )
        )
    )
    if quest_source_validation.unlock_proof_bridge_quest_present:
        issues.extend(
            validator_module_issues(
                questbook_progression_validator.validate_unlock_proof_bridge_surface(
                    repo_root
                )
            )
        )
    questbook_projection_parity_validator.validate_generated_quest_projection_surfaces(
        repo_root,
        valid_quest_ids=quest_source_validation.valid_quest_ids,
        expected_catalog_entries=quest_source_validation.expected_catalog_entries,
        expected_dispatch_entries=quest_source_validation.expected_dispatch_entries,
        issues=issues,
    )

    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, eval_name=args.eval)
        if args.eval is None:
            issues.extend(
                ValidationIssue(location, message)
                for location, message in validate_nested_agents.run_validation(repo_root)
            )
    except ValueError as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    if issues:
        scope = args.eval if args.eval else "repository"
        print(f"Validation failed for {scope}.")
        print(format_issues(issues))
        return 1

    if args.eval:
        print(f"Validation passed for eval '{args.eval}'.")
    else:
        eval_count = len(source_eval_collection_validator.discover_eval_names(repo_root))
        print(f"Validation passed for {eval_count} eval bundles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
