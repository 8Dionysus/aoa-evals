"""Root memory-consumer proof boundary contracts."""

from __future__ import annotations

from pathlib import Path

from validators import root_design_common as root_design_common_validator
from validators.common import ValidationIssue
from validators.root_common import DECISION_RECORDS_README_NAME, require_tokens


PROOF_TOPOLOGY_NAME = root_design_common_validator.PROOF_TOPOLOGY_NAME
MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0106-memory-consumer-proof-boundary.md"
)
MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS = (
    "`aoa-evals`",
    "reviewed `aoa-memo` object ids and provenance",
    "can cite reviewed recall as bounded context",
    "local `memo/` can hold write-candidate-only proof-layer memory",
    "proof authority stays with",
    "eval bundle or owning mechanic",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS = (
    "Reviewed memory routes recall into proof review.",
    "`aoa-evals` can cite reviewed `aoa-memo` object ids, provenance, lifecycle, and",
    "generated read models as bounded recall context",
    "Proof authority stays",
    "selected evidence, scoring or verdict logic",
    "`aoa-evals` keeps memory-consumer proof posture.",
    "local `memo/` port may",
    "`write_candidate_only` proof-layer memory candidates",
    "Those packets are review material",
    "not proof authority or",
    "durable memory",
    "Session evidence routes through `.aoa`, local memo candidates, or source proof",
    "later `aoa-memo` reviewed intake.",
    "Durable memory and export-packet landing route through reviewed owner surfaces",
    "with visible provenance",
    "`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs are",
    "access-plane evidence for inspection and review",
    "Owner surfaces keep proof authority and durable write authority.",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS = (
    "Memory evidence context",
    "reviewed `aoa-memo` object ids, provenance, lifecycle, generated memory read models",
    "local `memo/` port packets",
    "`aoa_memo` MCP access-plane dry-runs",
    "reviewed memory provides recall context; local proof authority stays with the eval bundle or owning mechanic",
    "local `memo/` packets are review material, not proof authority",
    "MCP output remains inspection evidence",
    "durable memory lands only in `aoa-memo`",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Memory Consumer Proof Boundary",
    "memory-consumer proof boundary",
    "object ids, provenance, lifecycle, and generated read models",
    "Memory is not proof.",
    "AOA-EV-D-0243",
    "write_candidate_only",
    "hidden memo ports",
    "Durable memory lands only in `aoa-memo`.",
    "`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs",
    "access-plane evidence only",
    "direct durable",
    "write authority",
)


def validate_memory_consumer_proof_boundary_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(repo_root, "README.md", MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS, issues)
    require_tokens(repo_root, "docs/guides/EVAL_PHILOSOPHY.md", MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS, issues)
    require_tokens(repo_root, PROOF_TOPOLOGY_NAME, MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS, issues)
    require_tokens(repo_root, MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME, MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS, issues)
    require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME, "Memory Consumer Proof Boundary"),
        issues,
    )

    return issues


__all__ = (
    "MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME",
    "MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS",
    "MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS",
    "MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS",
    "MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS",
    "validate_memory_consumer_proof_boundary_surfaces",
)
