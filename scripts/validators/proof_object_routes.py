"""Proof-object route and source-authority boundary contracts."""

from __future__ import annotations

from pathlib import Path

from validators import proof_object_route_paths as proof_paths
from validators import proof_object_route_tokens as proof_tokens
from validators.common import ValidationIssue
from validators.proof_object_route_helpers import DECISION_RECORDS_README_NAME, require_tokens


def validate_proof_object_parts_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = require_tokens(
        repo_root=repo_root,
        path_name=proof_paths.PROOF_OBJECT_PARTS_README_NAME,
        tokens=proof_tokens.PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for forbidden_token in proof_tokens.PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        proof_paths.PROOF_OBJECT_PARTS_README_NAME,
                        "proof-object parts route should use a positive operating card",
                    )
                )
    return issues


def validate_proof_object_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (proof_paths.PROOF_OBJECT_MECHANIC_README_NAME, proof_tokens.PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS),
        (proof_paths.PROOF_OBJECT_MECHANIC_AGENTS_NAME, proof_tokens.PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (proof_paths.PROOF_OBJECT_MECHANIC_PARTS_NAME, proof_tokens.PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS),
        (
            proof_paths.PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME,
            proof_tokens.PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME,
            proof_tokens.PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_MECHANIC_PROVENANCE_NAME,
            proof_tokens.PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_MECHANIC_DECISION_NAME,
            proof_tokens.PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_CONTRACT_PART_DECISION_NAME,
            proof_tokens.PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME,
            proof_tokens.PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        ),
        (
            proof_paths.PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME,
            proof_tokens.PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS,
        ),
        (
            DECISION_RECORDS_README_NAME,
            (
                proof_paths.PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME,
                "Proof-object Part Owner-split Contract",
            ),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    issues.extend(validate_proof_object_parts_route_surface(repo_root))
    return issues


__all__ = (
    "validate_proof_object_parts_route_surface",
    "validate_proof_object_route_surfaces",
)
