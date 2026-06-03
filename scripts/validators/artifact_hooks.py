"""Artifact-to-verdict hook contract refs.

This module owns the stable cross-repo contract matrix for trace/eval hook
examples. The root validator imports it as data instead of burying sibling
reference posture in the orchestration file.
"""

from __future__ import annotations

from typing import Any


ARTIFACT_VERDICT_HOOK_EXAMPLES = {
    "AOA-P-0014": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json",
    "AOA-P-0006": "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
    "AOA-P-0018": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json",
    "AOA-P-0008": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
    "AOA-P-0009": "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
    "AOA-P-0031": "mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
    "AOA-P-0032": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
}


TRACE_EVAL_HOOK_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "AOA-P-0014": {
        "eval_anchor": "aoa-verification-honesty",
        "artifact_contract_refs": [
            "repo:aoa-playbooks/playbooks/local-stack-diagnosis/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-playbooks/mechanics/real-run-harvest/parts/phase-alpha-evidence-store/docs/alpha-readiness/local-stack-diagnosis.md",
            "repo:aoa-agents/mechanics/questbook/parts/alpha-reference-routes/examples/local-stack-diagnosis.example.json",
            "repo:aoa-memo/examples/phase-alpha/state_capsule.phase-alpha-local-stack.example.json",
            "repo:aoa-memo/examples/phase-alpha/episode.phase-alpha-local-stack.example.json",
            "repo:aoa-memo/examples/phase-alpha/decision.phase-alpha-local-stack.example.json",
        ],
        "trace_surfaces": [],
        "verification_surface": "verification_pack",
    },
    "AOA-P-0006": {
        "eval_anchor": "aoa-approval-boundary-adherence",
        "artifact_contract_refs": [
            "repo:aoa-agents/mechanics/checkpoint/parts/self-agent-checkpoint/schemas/self-agent-checkpoint.schema.json",
            "repo:aoa-playbooks/playbooks/self-agent-checkpoint-rollout/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-memo/docs/memory/MEMORY_MODEL.md#checkpoint-route-writeback",
            "repo:aoa-memo/mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_approval_record.example.json",
            "repo:aoa-memo/mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_health_check.example.json",
            "repo:aoa-memo/mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_improvement_thread.example.json",
        ],
        "trace_surfaces": [],
        "verification_surface": "approval_record",
    },
    "AOA-P-0018": {
        "eval_anchor": "aoa-scope-drift-detection",
        "artifact_contract_refs": [
            "repo:aoa-playbooks/playbooks/validation-driven-remediation/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-playbooks/mechanics/real-run-harvest/parts/phase-alpha-evidence-store/docs/alpha-readiness/validation-driven-remediation.md",
            "repo:aoa-agents/mechanics/questbook/parts/alpha-reference-routes/examples/validation-driven-remediation.example.json",
            "repo:aoa-memo/examples/phase-alpha/episode.phase-alpha-validation-remediation.example.json",
            "repo:aoa-memo/examples/phase-alpha/decision.phase-alpha-validation-remediation.example.json",
            "repo:aoa-memo/examples/recall/recall_contract.object.working.phase-alpha.json",
        ],
        "trace_surfaces": [],
        "verification_surface": "revalidation_pack",
    },
    "AOA-P-0008": {
        "eval_anchor": "aoa-tool-trajectory-discipline",
        "artifact_contract_refs": [
            "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.route_decision.schema.json",
            "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.bounded_plan.schema.json",
            "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.verification_result.schema.json",
            "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.transition_decision.schema.json",
            "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.distillation_pack.schema.json",
        ],
        "trace_surfaces": [
            "repo:aoa-memo/mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
        ],
        "verification_surface": "verification_result",
    },
    "AOA-P-0009": {
        "eval_anchor": "aoa-long-horizon-depth",
        "artifact_contract_refs": [
            "repo:aoa-memo/mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
            "repo:aoa-memo/mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
            "repo:aoa-playbooks/playbooks/restartable-inquiry-loop/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-playbooks/generated/playbook_registry.min.json",
        ],
        "trace_surfaces": [],
        "verification_surface": "inquiry_checkpoint",
    },
    "AOA-P-0031": {
        "eval_anchor": "aoa-a2a-summon-return-checkpoint",
        "artifact_contract_refs": [
            "repo:aoa-playbooks/playbooks/a2a-summon-return-checkpoint/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-skills/skills/core/session-growth/aoa-summon/references/summon-request-v3.schema.json",
            "repo:aoa-skills/skills/core/session-growth/aoa-summon/references/summon-result-v3.schema.json",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/docs/summon-return-checkpoint.md",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/examples/codex_local_target.example.json",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/examples/return_transition_decision.example.json",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/examples/checkpoint_bridge_plan.example.json",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/examples/reviewed_closeout_request.example.json",
            "repo:aoa-sdk/mechanics/checkpoint/parts/child-task-reentry/examples/summon_return_checkpoint_e2e.fixture.json",
            "repo:aoa-memo/mechanics/writeback/docs/A2A_CHILD_RETURN_WRITEBACK.md",
            "repo:abyss-stack/mechanics/runtime-repair/parts/a2a-return-dry-run/docs/A2A_RETURN_DRY_RUN.md",
        ],
        "trace_surfaces": [],
        "verification_surface": "runtime_closeout_dry_run_receipt",
    },
    "AOA-P-0032": {
        "eval_anchor": "aoa-witness-trace-integrity",
        "artifact_contract_refs": [
            "repo:aoa-playbooks/playbooks/runtime-chaos-recovery/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-playbooks/mechanics/antifragility/parts/stress-lanes/examples/playbook_stress_lane.runtime-timeout-chaos.example.json",
            "repo:aoa-playbooks/mechanics/antifragility/parts/reentry-gates/examples/playbook_reentry_gate.retrieval-outage-honesty.example.json",
            "repo:aoa-routing/examples/composite_stress_route_hint.retrieval-outage-honesty.example.json",
            "repo:aoa-kag/examples/regrounding_ticket.retrieval-outage-honesty.example.json",
            "repo:abyss-stack/mechanics/runtime-repair/parts/degradation-receipts/schemas/service-degradation-receipt.schema.json",
            "repo:aoa-memo/mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
        ],
        "trace_surfaces": [
            "repo:aoa-memo/mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
            "repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/examples/provenance_thread.self-agency-continuity.example.json",
        ],
        "verification_surface": "proof_handoff_candidate",
    },
}
