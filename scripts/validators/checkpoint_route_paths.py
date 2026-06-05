"""Checkpoint route path constants."""

from __future__ import annotations


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


__all__ = tuple(name for name in globals() if name.startswith("CHECKPOINT_"))
