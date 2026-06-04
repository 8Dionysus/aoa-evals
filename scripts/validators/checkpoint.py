"""Checkpoint mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue


CHECKPOINT_MECHANIC_README_NAME = "mechanics/checkpoint/README.md"
CHECKPOINT_MECHANIC_AGENTS_NAME = "mechanics/checkpoint/AGENTS.md"
CHECKPOINT_MECHANIC_PARTS_NAME = "mechanics/checkpoint/PARTS.md"
CHECKPOINT_MECHANIC_PROVENANCE_NAME = "mechanics/checkpoint/PROVENANCE.md"
CHECKPOINT_A2A_PART_README_NAME = (
    "mechanics/checkpoint/parts/a2a-summon-return/README.md"
)
CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME = (
    "mechanics/checkpoint/parts/restartable-inquiry/README.md"
)
CHECKPOINT_SELF_AGENT_PART_README_NAME = (
    "mechanics/checkpoint/parts/self-agent-posture/README.md"
)
CHECKPOINT_SELF_AGENT_POSTURE_DOC_NAME = (
    "mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md"
)
CHECKPOINT_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0032-checkpoint-mechanic-package.md"
CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0062-checkpoint-part-contract-guard.md"
)
CHECKPOINT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "checkpoint pressure",
    "a2a-summon-return",
    "restartable-inquiry",
    "self-agent-posture",
    "evals/workflow/aoa-a2a-summon-return-checkpoint/EVAL.md",
    "evals/workflow/aoa-long-horizon-depth/EVAL.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "| checkpoint implementation authority pressure | Agents-of-Abyss law route plus `aoa-sdk` checkpoint-control route |",
    "| memory canon or recall sovereignty pressure | `aoa-memo` memory route |",
    "| live runtime activation pressure | `abyss-stack` runtime route |",
    "| owner acceptance or promotion pressure | owner repository acceptance route |",
    "| hidden scheduler behavior pressure | `aoa-playbooks` choreography route plus `abyss-stack` runtime route |",
    "| autonomous self-repair pressure | `aoa-agents` role, approval, rollback, and health route |",
    "| final child-output quality pressure | owner repository child-output acceptance route |",
    "| broad long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |",
    "python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py",
)
CHECKPOINT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "checkpoint proof work",
    "mechanics/checkpoint/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "candidate-only",
    "Create checkpoint parts from a multi-surface checkpoint proof operation",
    "python scripts/validate_repo.py",
)
CHECKPOINT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "a2a-summon-return",
    "restartable-inquiry",
    "self-agent-posture",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "| checkpoint implementation authority | Agents-of-Abyss law route plus `aoa-sdk` checkpoint-control route |",
    "| memory canon or recall sovereignty | `aoa-memo` memory route |",
    "| live runtime activation | `abyss-stack` runtime route |",
    "| owner acceptance or promotion | owner repository acceptance route |",
    "| hidden scheduling behavior | `aoa-playbooks` choreography route plus `abyss-stack` runtime route |",
    "| autonomous self-repair | `aoa-agents` role, approval, rollback, and health route |",
    "| final child-output quality grading | owner repository child-output acceptance route |",
    "| broad long-horizon competence | bundle-local proof object plus source-owner evidence review |",
)
CHECKPOINT_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
CHECKPOINT_A2A_PART_REQUIRED_TOKENS = (
    "aoa-a2a-summon-return-checkpoint",
    "mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md",
    "mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
    "mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py",
    "| checkpoint doctrine pressure | Agents-of-Abyss center route |",
    "| A2A control-plane implementation pressure | `aoa-sdk` A2A checkpoint-control route |",
    "| summon skill truth pressure | `aoa-skills` summon and closeout skill route |",
    "| memo canon or memo writeback acceptance pressure | `aoa-memo` writeback route |",
    "| live runtime execution or runtime closeout authority pressure | `abyss-stack` runtime route |",
    "| owner acceptance or final child-output quality pressure | owner repository child-output acceptance route |",
    "python scripts/build_catalog.py --check",
) + CHECKPOINT_PART_README_COMMON_REQUIRED_TOKENS
CHECKPOINT_RESTARTABLE_INQUIRY_PART_REQUIRED_TOKENS = (
    "aoa-long-horizon-depth",
    "mechanics/checkpoint/parts/restartable-inquiry/fixtures/long-horizon-restart-v1/README.md",
    "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
    "| memo checkpoint schema authority pressure | `aoa-memo` checkpoint schema route |",
    "| playbook choreography ownership pressure | `aoa-playbooks` restartable-inquiry route |",
    "| canon meaning pressure | owner repository canon route |",
    "| raw transcript continuity pressure | owner repository transcript route |",
    "| final inquiry truth or final-answer grading pressure | owner repository inquiry acceptance route |",
    "| broad long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |",
    "python scripts/build_catalog.py --check",
) + CHECKPOINT_PART_README_COMMON_REQUIRED_TOKENS
CHECKPOINT_SELF_AGENT_PART_REQUIRED_TOKENS = (
    "mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md",
    "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
    "aoa-approval-boundary-adherence",
    "aoa-bounded-change-quality",
    "| self-agent checkpoint contract meaning pressure | `aoa-agents` self-agent route |",
    "| scenario composition pressure | `aoa-playbooks` scenario route |",
    "| checkpoint writeback authority pressure | `aoa-memo` checkpoint writeback route |",
    "| checkpoint ontology pressure | Agents-of-Abyss checkpoint doctrine route |",
    "| sovereign checkpoint proof-canon pressure | Agents-of-Abyss doctrine plus bundle-local proof route |",
    "| owner acceptance or runtime activation pressure | owner repository acceptance route plus `abyss-stack` runtime route |",
    "python scripts/validate_repo.py",
) + CHECKPOINT_PART_README_COMMON_REQUIRED_TOKENS
CHECKPOINT_SELF_AGENT_POSTURE_DOC_REQUIRED_TOKENS = (
    "Checkpoint-only proof-canon pressure routes back to stronger owners.",
    "| self-agent contract meaning | `aoa-agents` |",
    "| scenario composition | `aoa-playbooks` |",
    "| checkpoint memory objects | `aoa-memo` |",
    "pressure routes back to the checkpoint owner split.",
    "Checkpoint ontology pressure routes to Agents-of-Abyss checkpoint doctrine.",
    "`aoa-evals` remains authoritative for bounded proof wording",
)
CHECKPOINT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/checkpoint/",
    "AoA-aligned",
    "a2a-summon-return",
    "restartable-inquiry",
    "self-agent-posture",
    "source proof bundles stay under `evals/`",
    "artifact-to-verdict hook schema",
    "checkpoint implementation authority",
    "python scripts/validate_repo.py",
)
CHECKPOINT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Checkpoint Part Contract Guard",
    "mechanics/checkpoint/parts/a2a-summon-return/README.md",
    "mechanics/checkpoint/parts/restartable-inquiry/README.md",
    "mechanics/checkpoint/parts/self-agent-posture/README.md",
    "former root `fixtures/`, `examples/`,",
    "current part-local homes",
    "memory canon",
    "runtime activation",
    "owner acceptance",
    "broad long-horizon",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class CheckpointRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: CheckpointRouteContext,
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


def validate_checkpoint_route_surfaces(
    repo_root: Path,
    *,
    context: CheckpointRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, CHECKPOINT_MECHANIC_README_NAME, CHECKPOINT_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_MECHANIC_AGENTS_NAME, CHECKPOINT_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_MECHANIC_PARTS_NAME, CHECKPOINT_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_A2A_PART_README_NAME, CHECKPOINT_A2A_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME, CHECKPOINT_RESTARTABLE_INQUIRY_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_SELF_AGENT_PART_README_NAME, CHECKPOINT_SELF_AGENT_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_SELF_AGENT_POSTURE_DOC_NAME, CHECKPOINT_SELF_AGENT_POSTURE_DOC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, CHECKPOINT_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, CHECKPOINT_MECHANIC_DECISION_NAME, CHECKPOINT_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
        CHECKPOINT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
            "Checkpoint Part Contract Guard",
        ),
        issues,
    )
    return issues
