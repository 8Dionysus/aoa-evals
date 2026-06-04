"""Recurrence mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue


RECURRENCE_MECHANIC_README_NAME = "mechanics/recurrence/README.md"
RECURRENCE_MECHANIC_AGENTS_NAME = "mechanics/recurrence/AGENTS.md"
RECURRENCE_MECHANIC_PARTS_NAME = "mechanics/recurrence/PARTS.md"
RECURRENCE_MECHANIC_PROVENANCE_NAME = "mechanics/recurrence/PROVENANCE.md"
RECURRENCE_CONTROL_PLANE_PART_README_NAME = (
    "mechanics/recurrence/parts/control-plane-integrity/README.md"
)
RECURRENCE_ANCHOR_RETURN_PART_README_NAME = (
    "mechanics/recurrence/parts/anchor-return/README.md"
)
RECURRENCE_MEMORY_RECALL_PART_README_NAME = (
    "mechanics/recurrence/parts/memory-recall/README.md"
)
RECURRENCE_RECURSOR_BOUNDARY_PART_README_NAME = (
    "mechanics/recurrence/parts/recursor-boundary/README.md"
)
RECURRENCE_STATS_REGROUNDING_PART_README_NAME = (
    "mechanics/recurrence/parts/stats-regrounding-boundary/README.md"
)
RECURRENCE_PORTABLE_PROOF_BEACONS_PART_README_NAME = (
    "mechanics/recurrence/parts/portable-proof-beacons/README.md"
)
RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME = (
    "mechanics/recurrence/parts/portable-proof-beacons/AGENTS.md"
)
RECURRENCE_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0031-recurrence-mechanic-package.md"
RECURRENCE_SUPPORT_PARTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0039-recurrence-support-parts-expansion.md"
)
RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0042-recurrence-portable-proof-beacons-part.md"
)
RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0066-recurrence-control-plane-contract.md"
)
RECURRENCE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "recurrence pressure",
    "control-plane-integrity",
    "anchor-return",
    "memory-recall",
    "recursor-boundary",
    "stats-regrounding-boundary",
    "portable-proof-beacons",
    "evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md",
    "evals/workflow/aoa-return-anchor-integrity/EVAL.md",
    "evals/workflow/aoa-memo-recall-integrity/EVAL.md",
    "evals/boundary/aoa-stats-regrounding-boundary-integrity/EVAL.md",
    "mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py",
    "mechanics/recurrence/parts/control-plane-integrity/scorers/recurrence_control_plane_integrity.py",
    "mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py",
    "mechanics/recurrence/parts/recursor-boundary/scorers/recursor_readiness_boundary.py",
    "Stronger Owner Split",
    "Stop-Lines",
    "| global recurrence completeness pressure | Agents-of-Abyss recurrence law route plus source-owner proof review |",
    "| hidden continuity pressure | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |",
    "| automatic recursor or agent-spawn pressure | `aoa-agents` role route plus `aoa-sdk` control-plane readiness route |",
    "| runtime self-healing or runtime activation pressure | `abyss-stack` runtime route after owner gates |",
    "| owner artifact promotion pressure | owner repository acceptance route |",
    "| beacon verdict authority pressure | bundle-local proof review plus portable-proof-beacon decision closure |",
    "| portable proof acceptance by recurrence manifest pressure | source bundle authoring and owner-reviewed portable eval route |",
    "| routing, stats, KAG, or Agon source-truth pressure | owning route, stats, KAG, or Agon source surface |",
    "python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py",
    "python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py",
)
RECURRENCE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "recurrence proof work",
    "mechanics/recurrence/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "candidate-only",
    "Create recurrence parts from a multi-surface proof operation",
    "python scripts/validate_repo.py",
)
RECURRENCE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "control-plane-integrity",
    "anchor-return",
    "memory-recall",
    "recursor-boundary",
    "stats-regrounding-boundary",
    "portable-proof-beacons",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "Continuity-anchor and self-reanchor proof remain bundle-local",
    "| global recurrence completeness | Agents-of-Abyss recurrence law plus source-owner proof review |",
    "| hidden continuity | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |",
    "| runtime self-healing | `abyss-stack` runtime route after owner gates |",
    "| automatic recursor spawn | `aoa-agents` role route plus `aoa-sdk` control-plane readiness route |",
    "| beacon verdicts | bundle-local proof review plus portable-proof-beacon decision closure |",
    "| owner promotion | owner repository acceptance route |",
    "| source-truth transfer to generated projections | source owner plus generated-surface owner route |",
    "| accepted portable proof | source bundle authoring and owner-reviewed portable eval route |",
)
RECURRENCE_CONTROL_PLANE_PART_REQUIRED_TOKENS = (
    "aoa-recurrence-control-plane-integrity",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md",
    "mechanics/recurrence/parts/control-plane-integrity/examples/recurrence_control_plane_integrity.dossier.example.json",
    "mechanics/recurrence/parts/control-plane-integrity/schemas/recurrence-control-plane-integrity-dossier.schema.json",
    "mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py",
    "mechanics/recurrence/parts/control-plane-integrity/scorers/recurrence_control_plane_integrity.py",
    "mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py",
    "| recurrence doctrine pressure | Agents-of-Abyss recurrence route |",
    "| global recurrence completeness pressure | Agents-of-Abyss law plus source-owner proof review |",
    "| hidden continuity pressure | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |",
    "| runtime status or runtime activation pressure | `abyss-stack` runtime route |",
    "| runtime self-healing pressure | `abyss-stack` repair and recovery route after owner gates |",
    "| promotion readiness pressure | owner repository acceptance route plus bundle-local proof review |",
    "| owner review acceptance pressure | owner repository review route |",
    "| downstream projection truth pressure | downstream source owner route |",
    "| Agon source truth pressure | Agon owner surface |",
    "| automatic recursor or agent-spawn pressure | `aoa-agents` role route plus `aoa-sdk` readiness route |",
    "| beacon verdict authority pressure | portable-proof-beacon decision closure plus bundle-local proof review |",
    "| portable proof acceptance by recurrence manifest pressure | source bundle authoring and owner-reviewed portable eval route |",
    "python scripts/build_catalog.py --check",
)
RECURRENCE_ANCHOR_RETURN_PART_REQUIRED_TOKENS = (
    "aoa-return-anchor-integrity",
    "mechanics/recurrence/parts/anchor-return/fixtures/return-anchor-v1/README.md",
    "runtime_evidence_selection.return-anchor-integrity.example.json",
    "Stronger Owner Split",
    "Stop-Lines",
    "| final task quality pressure | owner repository acceptance route |",
    "| broad workflow safety pressure | source-owner review plus relevant skill/playbook route |",
    "| hidden continuity pressure | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |",
    "| automatic runtime recovery pressure | `abyss-stack` runtime recovery route after owner gates |",
    "| general long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |",
    "python scripts/validate_repo.py --eval aoa-return-anchor-integrity",
)
RECURRENCE_MEMORY_RECALL_PART_REQUIRED_TOKENS = (
    "aoa-memo-recall-integrity",
    "mechanics/recurrence/parts/memory-recall/fixtures/memo-recall-guardrail-v1/README.md",
    "test_memo_recall_phase_alpha_report.py",
    "aoa-memo",
    "Stop-Lines",
    "| general memory quality pressure | `aoa-memo` recall quality route |",
    "| contradiction handling pressure | `aoa-memo` provenance and conflict route |",
    "| permission inference pressure | source owner plus role/approval route |",
    "| memory canon pressure | `aoa-memo` memory-object route |",
    "| runtime ranking behavior pressure | runtime owner route |",
    "| future writeback acceptance pressure | `aoa-memo` writeback acceptance route plus source-owner review |",
    "python scripts/validate_repo.py --eval aoa-memo-recall-integrity",
)
RECURRENCE_RECURSOR_BOUNDARY_PART_REQUIRED_TOKENS = (
    "recursor readiness boundary",
    "mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/",
    "scorers/recursor_readiness_boundary.py",
    "scripts/run_recursor_readiness_boundary_eval.py",
    "aoa-agents",
    "aoa-sdk",
    "| live recursor activation pressure | `aoa-agents` role route plus `abyss-stack` runtime route |",
    "| agent spawn authority pressure | `aoa-agents` approval and role route |",
    "| arena eligibility pressure | Agon owner surface plus owner acceptance route |",
    "| scar ownership pressure | Agon owner surface plus source-owner evidence route |",
    "| verdict authority pressure | bundle-local proof review plus owner verdict route |",
    "| rank mutation pressure | Agon/ranking owner route |",
    "| hidden scheduling pressure | `aoa-playbooks` choreography route plus runtime owner route |",
    "| runtime readiness pressure | `abyss-stack` runtime readiness route after owner gates |",
)
RECURRENCE_STATS_REGROUNDING_PART_REQUIRED_TOKENS = (
    "aoa-stats-regrounding-boundary-integrity",
    "mechanics/recurrence/parts/stats-regrounding-boundary/fixtures/stats-regrounding-boundary-v1/README.md",
    "test_stats_regrounding_boundary_eval.py",
    "aoa-stats",
    "aoa-sdk",
    "aoa-routing",
    "| owner artifact correctness pressure | owner repository source-truth route |",
    "| route approval pressure | `aoa-routing` advisory route plus owner acceptance |",
    "| project health pressure | owner repository review plus derived stats context |",
    "| SDK optimality pressure | `aoa-sdk` policy and implementation route |",
    "| routing authority pressure | `aoa-routing` route-authority boundary |",
    "| stats-as-proof pressure | `aoa-stats` derived-only route plus bundle-local proof review |",
)
RECURRENCE_PORTABLE_PROOF_BEACONS_PART_REQUIRED_TOKENS = (
    "component:evals:portable-proof-beacons",
    "mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/component.evals.portable-proof-beacons.json",
    "component.evals.portable-proof-beacons.hooks.json",
    "RECURRENCE_REVIEW_DECISION_CLOSURE.md",
    "watch",
    "candidate",
    "review_ready",
    "| runtime artifact proof-canon pressure | audit-selected evidence route plus source proof bundle review |",
    "| accepted portable proof pressure | bundle-local review plus owner-reviewed portable eval authoring route |",
    "| universal score or automatic unlock pressure | `mechanics/rpg/` progression route plus owner acceptance |",
    "| beacon-as-verdict pressure | recurrence decision closure plus bundle-local proof review |",
    "| recurrence manifest ownership of audit, RPG, runtime, or sibling truth pressure | owning audit, RPG, runtime, or sibling source surface |",
    "| overclaim repair pressure | proof-object repair route |",
    "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
    "mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "python scripts/validate_repo.py",
)
RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "portable-proof beacon pressure",
    "component:evals:portable-proof-beacons",
    "Runtime artifact evidence pressure",
    "Accepted portable proof pressure",
    "Progression or unlock pressure",
    "Beacon-as-verdict pressure",
    "centralized-child-validation",
)
RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_STALE_ROUTE_PHRASES = (
    "It does not own runtime evidence intake",
    "Keep `component:evals:portable-proof-beacons` inside `recurrence`; do not",
    "Treat runtime artifacts as candidate evidence",
    "Keep audit packet curation",
    "Keep progression and unlock support",
    "python scripts/build_catalog.py --check",
)
RECURRENCE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/recurrence/",
    "AoA-aligned",
    "control-plane integrity",
    "source proof bundles stay under `evals/`",
    "owning legacy archive",
    "return-anchor",
    "continuity-anchor",
    "self-reanchor",
    "global recurrence completeness",
    "python scripts/validate_repo.py",
)
RECURRENCE_SUPPORT_PARTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/recurrence/",
    "anchor-return",
    "memory-recall",
    "recursor-boundary",
    "stats-regrounding-boundary",
    "Source proof bundles stay under",
    "Continuity-anchor and self-reanchor remain bundle-local",
    "memory canon",
    "recursor activation",
    "stats-as-proof",
)
RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_REQUIRED_TOKENS = (
    "mechanics/recurrence/parts/portable-proof-beacons/",
    "component:evals:portable-proof-beacons",
    "hint -> watch -> candidate -> review_ready",
    "recurrence",
    "does not own audit candidate packet curation",
    "does not make runtime evidence proof canon",
    "python scripts/validate_repo.py",
)
RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Recurrence Control-plane Contract",
    "mechanics/recurrence/parts/control-plane-integrity/README.md",
    "current part-local paths",
    "runtime status",
    "promotion readiness",
    "downstream projection truth",
    "owner review acceptance",
    "Agon source truth",
    "beacon verdict authority",
    "portable proof acceptance",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class RecurrenceRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: RecurrenceRouteContext,
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


def validate_recurrence_route_surfaces(
    repo_root: Path,
    *,
    context: RecurrenceRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, RECURRENCE_MECHANIC_README_NAME, RECURRENCE_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_MECHANIC_AGENTS_NAME, RECURRENCE_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_MECHANIC_PARTS_NAME, RECURRENCE_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_CONTROL_PLANE_PART_README_NAME, RECURRENCE_CONTROL_PLANE_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_ANCHOR_RETURN_PART_README_NAME, RECURRENCE_ANCHOR_RETURN_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_MEMORY_RECALL_PART_README_NAME, RECURRENCE_MEMORY_RECALL_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_RECURSOR_BOUNDARY_PART_README_NAME, RECURRENCE_RECURSOR_BOUNDARY_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_STATS_REGROUNDING_PART_README_NAME, RECURRENCE_STATS_REGROUNDING_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_PORTABLE_PROOF_BEACONS_PART_README_NAME, RECURRENCE_PORTABLE_PROOF_BEACONS_PART_REQUIRED_TOKENS, issues)
    portable_proof_beacons_agents_text = _require(
        context,
        repo_root,
        RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME,
        RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    if portable_proof_beacons_agents_text:
        for stale_phrase in RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in portable_proof_beacons_agents_text:
                issues.append(
                    ValidationIssue(
                        RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME,
                        "recurrence portable-proof-beacons AGENTS card should use an operating card and owner route table instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )
    _require(context, repo_root, RECURRENCE_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, RECURRENCE_MECHANIC_DECISION_NAME, RECURRENCE_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_SUPPORT_PARTS_DECISION_NAME, RECURRENCE_SUPPORT_PARTS_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_NAME, RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME, RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME,
            "Recurrence Control-plane Contract",
        ),
        issues,
    )
    return issues
