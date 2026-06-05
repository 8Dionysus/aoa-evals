"""Proof-infra mechanic route boundary checks."""

from __future__ import annotations

from pathlib import Path

from validators import proof_infra_common as common
from validators import proof_infra_route_tokens as route_tokens
from validators.common import ValidationIssue


def validate_proof_infra_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (common.PROOF_INFRA_MECHANIC_README_NAME, route_tokens.PROOF_INFRA_MECHANIC_REQUIRED_TOKENS),
        (common.PROOF_INFRA_MECHANIC_AGENTS_NAME, route_tokens.PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (common.PROOF_INFRA_MECHANIC_PARTS_NAME, route_tokens.PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS),
        (
            common.PROOF_INFRA_FIXTURE_FAMILIES_README_NAME,
            route_tokens.PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS,
        ),
        (
            common.PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME,
            route_tokens.PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS,
        ),
        (common.PROOF_INFRA_PROVENANCE_NAME, route_tokens.PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS),
        (common.PROOF_INFRA_LEGACY_INDEX_NAME, route_tokens.PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS),
        (
            common.PROOF_INFRA_MECHANIC_DECISION_NAME,
            route_tokens.PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            common.PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME,
            route_tokens.PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS,
        ),
        (
            common.PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME,
            route_tokens.PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS,
        ),
    ):
        common.require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    fixture_families_agents_text = common.require_tokens(
        repo_root=repo_root,
        path_name=common.PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME,
        tokens=route_tokens.PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    reportable_contracts_agents_text = common.require_tokens(
        repo_root=repo_root,
        path_name=common.PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME,
        tokens=route_tokens.PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, text in (
        (common.PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME, fixture_families_agents_text),
        (common.PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME, reportable_contracts_agents_text),
    ):
        if not text:
            continue
        for stale_phrase in route_tokens.PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "proof-infra part AGENTS cards should use operating cards and owner route tables instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )
    return issues


__all__ = ("validate_proof_infra_route_surfaces",)
