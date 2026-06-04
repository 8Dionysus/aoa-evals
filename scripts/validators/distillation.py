"""Distillation mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue


DISTILLATION_MECHANIC_README_NAME = "mechanics/distillation/README.md"
DISTILLATION_MECHANIC_AGENTS_NAME = "mechanics/distillation/AGENTS.md"
DISTILLATION_MECHANIC_PARTS_NAME = "mechanics/distillation/PARTS.md"
DISTILLATION_MECHANIC_PROVENANCE_NAME = "mechanics/distillation/PROVENANCE.md"
DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME = (
    "mechanics/distillation/parts/compost-provenance/README.md"
)
DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME = (
    "mechanics/distillation/parts/runtime-candidate-adoption/README.md"
)
DISTILLATION_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0038-distillation-mechanic-package.md"
)
DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0064-distillation-part-contract-guard.md"
)
DISTILLATION_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "distillation pressure",
    "compost-provenance",
    "runtime-candidate-adoption",
    "evals/artifact/aoa-compost-provenance-preservation/EVAL.md",
    "evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "| summary-as-proof pressure | source trace, source bundle, and bundle-local review route |",
    "| raw deletion authority pressure | owner repository source-retention route |",
    "| proof verdict without bundle-local review pressure | bundle-local review route |",
    "| memory canon, recall sovereignty, or live memory-ledger pressure | `aoa-memo` memory route |",
    "| runtime activation or hidden runtime-store pressure | `abyss-stack` runtime route |",
    "| owner acceptance, owner-local adoption, or final promotion pressure | owner repository acceptance route |",
    "| Tree-of-Sophia canon or compost authority pressure | Tree-of-Sophia canon route |",
    "| KAG bridge promotion or graph lift pressure | `aoa-kag` graph-lift route |",
    "| memo contradiction or confirmed writeback-act pressure | owning eval bundle or mechanic part route |",
    "| memo recall pressure | `mechanics/recurrence/parts/memory-recall/` route |",
    "python scripts/validate_repo.py --eval aoa-compost-provenance-preservation",
)
DISTILLATION_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Distillation proof work",
    "mechanics/distillation/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create Distillation parts from a recurring proof operation",
    "python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity",
)
DISTILLATION_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "compost-provenance",
    "runtime-candidate-adoption",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-compost-provenance-preservation",
    "aoa-memo-reviewed-candidate-adoption-integrity",
    "| summary-as-proof or raw deletion authority | source trace, source bundle, owner source-retention route |",
    "| memory canon or live memory-ledger behavior | `aoa-memo` memory route |",
    "| runtime activation or hidden runtime-store truth | `abyss-stack` runtime route |",
    "| owner acceptance, owner-local adoption, or final promotion | owner repository acceptance route |",
    "| ToS canon or compost authority | Tree-of-Sophia canon route |",
    "| KAG bridge promotion or graph lift | `aoa-kag` graph-lift route |",
    "| generic adoption readiness | `mechanics/experience/parts/adoption-federation/` route |",
    "| memo recall after active recurrence routing | `mechanics/recurrence/parts/memory-recall/` route |",
    "| nearby contradiction or base writeback proof | owning eval bundle or mechanic part route |",
)
DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
DISTILLATION_COMPOST_PROVENANCE_PART_REQUIRED_TOKENS = (
    "Compost Provenance Part",
    "evals/artifact/aoa-compost-provenance-preservation/EVAL.md",
    "mechanics/distillation/parts/compost-provenance/fixtures/compost-provenance-v1/README.md",
    "| ToS canon pressure | Tree-of-Sophia canon route |",
    "| principle truth pressure | Tree-of-Sophia authored-meaning route |",
    "| compost canon pressure | Tree-of-Sophia compost route |",
    "| original run quality pressure | owner repository source-artifact route |",
    "| witness trace honesty pressure | witness-source evidence route |",
    "| artifact-quality verdict pressure | bundle-local artifact review route |",
    "| artifact/process comparison pressure | `comparison-spine` route |",
    "| memory canon pressure | `aoa-memo` memory route |",
    "| operational ownership transfer pressure | owner repository transfer route |",
    "python scripts/validate_repo.py --eval aoa-compost-provenance-preservation",
) + DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS
DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_REQUIRED_TOKENS = (
    "Runtime Candidate Adoption Part",
    "evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md",
    "mechanics/distillation/parts/runtime-candidate-adoption/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md",
    "distillation_claim_candidate",
    "aoa-memo-writeback-act-integrity",
    "| final promotion pressure | owner approval and durable memory review route |",
    "| memory canon or memo object truth pressure | `aoa-memo` memory-object route |",
    "| live memory-ledger behavior pressure | `aoa-memo` and `abyss-stack` runtime route |",
    "| memo recall implementation pressure | `mechanics/recurrence/parts/memory-recall/` and `aoa-memo` route |",
    "| runtime pack contract authority pressure | `aoa-agents` runtime artifact route |",
    "| live receipt append behavior pressure | `publication-receipts` and runtime receipt route |",
    "| Experience adoption federation pressure | `mechanics/experience/parts/adoption-federation/` |",
    "| KAG lift or bridge-ready truth pressure | `aoa-kag` graph-lift route |",
    "| owner-local adoption or final owner acceptance pressure | owner repository route |",
    "python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity",
) + DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS
DISTILLATION_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/distillation/",
    "AoA-aligned",
    "compost-provenance",
    "runtime-candidate-adoption",
    "Source proof bundles stay under `evals/`",
    "summary-as-proof",
    "aoa-memo-writeback-act-integrity",
    "python scripts/validate_repo.py",
)
DISTILLATION_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Distillation Part Contract Guard",
    "mechanics/distillation/parts/compost-provenance/README.md",
    "mechanics/distillation/parts/runtime-candidate-adoption/README.md",
    "ToS canon",
    "memory canon",
    "runtime promotion",
    "receipt publication",
    "Experience adoption federation",
    "KAG lift",
    "owner-local acceptance",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class DistillationRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: DistillationRouteContext,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    return context.require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=tokens,
        issues=issues,
    )


def validate_distillation_route_surfaces(
    repo_root: Path,
    *,
    context: DistillationRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, DISTILLATION_MECHANIC_README_NAME, DISTILLATION_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, DISTILLATION_MECHANIC_AGENTS_NAME, DISTILLATION_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, DISTILLATION_MECHANIC_PARTS_NAME, DISTILLATION_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME, DISTILLATION_COMPOST_PROVENANCE_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME, DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, DISTILLATION_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, DISTILLATION_MECHANIC_DECISION_NAME, DISTILLATION_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
        DISTILLATION_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
            "Distillation Part Contract Guard",
        ),
        issues,
    )
    return issues
