"""Mechanic parent route, guidance, and allowlist guards."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators import docs_decisions
from validators import mechanic_legacy as mechanic_legacy_validator
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"

MECHANIC_PARENT_ALLOWLIST_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0052-mechanic-parent-allowlist.md"
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0097-mechanic-parent-guidance-boundary.md"
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_topology.py -k mechanic_parent_guidance_boundary"
)
MECHANIC_PARENT_DIRECTION_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md"
)
MECHANIC_PARENT_DIRECTION_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_direction.py -k mechanic_parent_direction"
)

MECHANICS_ROOT_ALLOWED_FILES = (
    "AGENTS.md",
    "EVIDENCE_CLUSTERS.md",
    "README.md",
)
MECHANIC_ROUTE_CARD_FILES = tuple(
    route
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
    for route in (
        f"mechanics/{parent_name}/AGENTS.md",
        f"mechanics/{parent_name}/README.md",
        f"mechanics/{parent_name}/DIRECTION.md",
        f"mechanics/{parent_name}/PARTS.md",
    )
)
MECHANIC_PARENT_README_FILES = tuple(
    f"mechanics/{parent_name}/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PARENT_AGENTS_FILES = tuple(
    f"mechanics/{parent_name}/AGENTS.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_DIRECTION_FILES = tuple(
    f"mechanics/{parent_name}/DIRECTION.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)

MECHANIC_PARENT_ROOT_ALLOWED_FILES = frozenset(
    {
        "AGENTS.md",
        "DIRECTION.md",
        "PARTS.md",
        "PROVENANCE.md",
        "README.md",
    }
)
MECHANIC_PARENT_ROOT_ALLOWED_DIRS = frozenset({"legacy", "parts"})
MECHANIC_PARENT_GUIDANCE_DOCS = {
    "agon": frozenset(
        {
            "AGON_EVAL_OWNER_HANDOFFS.md",
            "AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md",
        }
    ),
    "recurrence": frozenset({"RECURRENCE_PROOF_PROGRAM.md"}),
}
MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS = (
    "## Role",
    "## Mechanic-wide Scope",
    "## Source Surfaces",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Guidance Boundary",
    "`mechanics/<parent>/docs/`",
    "mechanic-wide guidance",
    "parent guidance content contract",
    "part-owned payload",
    "`## Source Surfaces`",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "allowlisted",
    "unallowlisted parent-level docs",
    "Titan canary guides",
    MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND,
)

MECHANIC_DIRECTION_REQUIRED_TOKENS = (
    "current operating direction",
    "## Source-of-truth split",
    "`README.md`",
    "`DIRECTION.md`",
    "`PARTS.md`",
    "`PROVENANCE.md`",
    "`legacy/`",
    "archive-local route",
    "## Current contour",
    "## Growth rule",
    "## Stop-lines",
    "## Validation",
)
MECHANIC_PARENT_README_DIRECTION_ROUTE_REQUIRED_TOKENS = (
    "## Entry Route",
    "## Role",
    "## Owned Operation",
    "[DIRECTION.md](DIRECTION.md)",
    "current operating direction",
    "[PARTS.md](PARTS.md)",
    "[PROVENANCE.md](PROVENANCE.md)",
    "active-to-archive bridge",
    "## Validation",
    "AGENTS.md#validation",
    "## Next Route",
)
MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN = "Do not use this package to claim:"
MECHANIC_PARENT_README_STALE_PROVENANCE_ROUTE = (
    "[PROVENANCE.md](PROVENANCE.md) only"
)
ACTIVE_MECHANIC_ROUTE_STALE_ROLE_PHRASES: dict[str, tuple[str, ...]] = {
    "mechanics/boundary-bridge/README.md": (
        "refs that should not feed proof",
    ),
    "mechanics/agon/PARTS.md": (
        "Do not split one future-growing operation",
    ),
    "mechanics/agon/README.md": (
        "They do not define the active package name",
        "not the route for new Agon work",
    ),
    "mechanics/distillation/README.md": (
        "It is not an active Distillation source surface",
        "not a replacement for the source bundles",
    ),
    "mechanics/proof-loop/README.md": (
        "Do not use it as a generic eval-result example",
    ),
}
MECHANIC_PARENT_AGENTS_DIRECTION_ROUTE_REQUIRED_TOKENS = (
    "## Entry Route",
    "current operating direction",
    "active-to-archive bridge",
)
MECHANIC_PARENT_AGENTS_STALE_PROVENANCE_ROUTE_TEMPLATE = (
    "`mechanics/{parent_name}/PROVENANCE.md` only"
)
MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Direction Contract",
    "`DIRECTION.md`",
    "current operating direction",
    "`## Role`",
    "`## Next Route`",
    "`README.md`",
    "`PARTS.md`",
    "`PROVENANCE.md`",
    "active-to-archive bridge",
    "not provenance",
    "not a part map",
    MECHANIC_PARENT_DIRECTION_COMMAND,
)
MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Allowlist",
    "no invented parent packages",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "AoA-aligned",
    "evals-native",
    "validator allowlist",
    "Active parents are active, not merely plausible candidates",
)
MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS = (
    "## Operating Card",
    "| role |",
    "| input |",
    "| output |",
    "| owner |",
    "| next route |",
    "| tools |",
    "| validation |",
    "## Active Parts",
    "## Part Admission Route",
    "AGENTS.md#validation",
)
ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS = (
    "Mechanic lower index",
    "DIRECTION.md",
    "part/payload source surfaces",
    "parts index synchronization",
    "payload coverage",
)
FORBIDDEN_ACTIVE_MECHANICS_PATHS = (
    "mechanics/agon-proof",
    "mechanics/titan-canaries",
    "mechanics/proof-release",
    "mechanics/runtime-evidence",
    "mechanics/sibling-proof-refs",
    "mechanics/repair",
    "docs/decisions/0016-agon-proof-mechanic-package.md",
    "docs/decisions/0015-titan-canaries-mechanic-package.md",
    "docs/decisions/0014-proof-release-mechanic-package.md",
    "docs/decisions/0007-runtime-evidence-mechanic-package.md",
    "docs/decisions/0008-sibling-proof-refs-mechanic-package.md",
    "docs/RECURRENCE_PROOF_PROGRAM.md",
    "docs/RECURRENCE_CONTROL_PLANE_EVALS.md",
    "docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md",
    "docs/EVAL_INDEX_RECURRENCE_INSERT.md",
    "docs/EVAL_SELECTION_RECURRENCE_INSERT.md",
    "fixtures/recurrence-control-plane-integrity-v1",
    "schemas/recurrence-control-plane-integrity-dossier.schema.json",
    "examples/recurrence_control_plane_integrity.dossier.example.json",
    "scripts/run_recurrence_control_plane_integrity_eval.py",
    "scorers/recurrence_control_plane_integrity.py",
    "tests/test_recurrence_control_plane_integrity_eval_seed.py",
    "manifests/recurrence/component.recurrence-control-plane-integrity-eval.json",
    "manifests/recurrence/component.evals.portable-proof-beacons.json",
    "manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json",
    "docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md",
    "fixtures/return-anchor-v1",
    "fixtures/memo-recall-guardrail-v1",
    "fixtures/recursor-readiness-boundary-v1",
    "fixtures/stats-regrounding-boundary-v1",
    "scripts/run_recursor_readiness_boundary_eval.py",
    "scorers/recursor_readiness_boundary.py",
    "tests/test_recursor_readiness_boundary_eval_seed.py",
    "tests/test_stats_regrounding_boundary_eval.py",
    "tests/test_memo_recall_phase_alpha_report.py",
    "docs/PROGRESSION_EVIDENCE_MODEL.md",
    "docs/UNLOCK_PROOF_BRIDGE.md",
    "schemas/progression_evidence.schema.json",
    "schemas/unlock_proof_catalog.schema.json",
    "examples/progression_evidence.example.json",
    "generated/unlock_proof_cards.min.example.json",
    "docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md",
    "fixtures/a2a-summon-return-checkpoint-v1",
    "fixtures/long-horizon-restart-v1",
    "tests/test_a2a_summon_return_checkpoint_fixture.py",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
    "docs/EXPERIENCE_CERTIFICATION_EVAL_BUNDLES.md",
    "docs/ASSISTANT_CERTIFICATION_JUDGE.md",
    "docs/DEPLOYMENT_INTEGRITY_BUNDLES.md",
    "docs/POST_RELEASE_REGRESSION_VERDICT.md",
    "docs/ROLLBACK_DRILL_VERDICT_MODEL.md",
    "docs/ROLLBACK_TRIGGER_VERDICT.md",
    "docs/WATCHTOWER_ALARM_VERDICT_MODEL.md",
    "docs/ADOPTION_EVAL_BUNDLES.md",
    "docs/ADOPTION_COMPATIBILITY_VERDICT.md",
    "docs/AGONIC_ADOPTION_TRIAL_VERDICT.md",
    "docs/ASSISTANT_ADOPTION_CERTIFICATION_VERDICT.md",
    "docs/ROUTING_ADOPTION_VERDICT.md",
    "docs/SHADOW_ADOPTION_VERDICT.md",
    "docs/FEDERATION_HARVEST_EVAL_BUNDLES.md",
    "docs/KAG_PROMOTION_VERDICT_MODEL.md",
    "docs/OWNER_CONSENT_VERDICT.md",
    "docs/PATTERN_LINEAGE_INTEGRITY_BUNDLES.md",
    "docs/TOS_BOUNDARY_VERDICT_MODEL.md",
    "docs/AUTHORITY_RESOLUTION_VERDICT.md",
    "docs/APPEAL_REVIEW_VERDICT.md",
    "docs/CHARTER_AMENDMENT_EVALS.md",
    "docs/CONSTITUTION_RUNTIME_EVAL_BUNDLES.md",
    "docs/GOVERNANCE_VERDICT_BUNDLES.md",
    "docs/REPLAY_HISTORY_INTEGRITY_VERDICT.md",
    "docs/STAY_ORDER_ENFORCEMENT_VERDICT.md",
    "docs/TOS_DOSSIER_REVIEW_VERDICTS.md",
    "docs/VETO_LEGITIMACY_BUNDLES.md",
    "docs/VOTE_SEAL_INTEGRITY_VERDICT.md",
    "docs/BOUNDARY_GUARD_VERDICTS.md",
    "docs/GOVERNED_RELEASE_VERDICTS.md",
    "docs/HANDOFF_INTEGRITY_VERDICTS.md",
    "docs/INSTALLATION_SMOKE_EVALS.md",
    "docs/MULTI_OFFICE_RELEASE_TRAIN_EVALS.md",
    "docs/OFFICE_SCOPE_FIDELITY_VERDICTS.md",
    "docs/REPLAY_AUDIT_VERDICTS.md",
    "docs/ROLLBACK_DRILL_VERDICTS.md",
    "docs/SERVICE_MESH_REGRESSION_VERDICTS.md",
    "fixtures/experience-verdict-protocol-integrity-v1",
    "fixtures/experience-certification-gate-integrity-v1",
    "fixtures/memo-reviewed-candidate-adoption-guardrail-v1",
    "fixtures/compost-provenance-v1",
    "mechanics/experience/parts/adoption-federation/fixtures/memo-reviewed-candidate-adoption-guardrail-v1",
    "tests/test_experience_protocol_integrity.py",
    "tests/test_experience_certification_gate_integrity.py",
    "tests/test_experience_wave2_seed_contracts.py",
    "tests/test_experience_wave3_seed_contracts.py",
    "tests/test_experience_wave4_seed_contracts.py",
    "tests/test_experience_wave5_seed_contracts.py",
    "docs/STRESS_RECOVERY_WINDOW_EVALS.md",
    "fixtures/stress-recovery-window-bounded-v1",
    "fixtures/repair-boundedness-v1",
    "schemas/antifragility_eval_report_v1.json",
    "schemas/stress_recovery_window_eval_report_v1.json",
    "fixtures/candidate-lineage-v1",
    "fixtures/owner-fit-routing-v1",
)


def _require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text

    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in docs_decisions.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    if path_name == PROOF_TOPOLOGY_NAME:
        route_guard_path = repo_root / ROUTE_RESIDUE_GUARDS_NAME
        if route_guard_path.is_file():
            companion_texts.append(route_guard_path.read_text(encoding="utf-8"))

    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))
    return text


def markdown_python_commands(section: str) -> list[str]:
    commands: list[str] = []
    commands.extend(re.findall(r"`(python3? [^`]+)`", section))
    in_fence = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped.startswith("python ") or stripped.startswith("python3 "):
            commands.append(stripped)
    return list(dict.fromkeys(commands))


def validate_mechanic_index_command_ownership(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_paths = sorted((repo_root / "mechanics").glob("*/PARTS.md"))
    index_paths.extend(sorted((repo_root / "mechanics").glob("*/parts/README.md")))

    for path in index_paths:
        relative_name = path.relative_to(repo_root).as_posix()
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    relative_name,
                    "mechanic index surfaces must route executable validation commands to the nearest AGENTS.md instead of carrying python command blocks",
                )
            )

    return issues


def validate_mechanic_lower_parts_index_operating_cards(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    parts_dirs = sorted(
        path for path in (repo_root / "mechanics").glob("*/parts") if path.is_dir()
    )

    for parts_dir in parts_dirs:
        path = parts_dir / "README.md"
        relative_name = path.relative_to(repo_root).as_posix()
        if not path.exists():
            issues.append(
                ValidationIssue(
                    relative_name,
                    "lower parts index README is missing",
                )
            )
            continue
        _require_tokens(
            repo_root=repo_root,
            path_name=relative_name,
            tokens=MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS,
            issues=issues,
        )

    return issues


def validate_mechanic_parent_direction_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_DIRECTION_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_DIRECTION_REQUIRED_TOKENS,
            issues=issues,
        )

    for path_name in MECHANIC_PARENT_README_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PARENT_README_DIRECTION_ROUTE_REQUIRED_TOKENS,
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        if MECHANIC_PARENT_README_STALE_PROVENANCE_ROUTE in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent README must route PROVENANCE.md as the active-to-archive bridge; stale only-when legacy side-path wording is retired",
                )
            )
        if MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent README must introduce Stop-Lines as a bounded eval-side proof boundary, not the old package-claim scaffold",
                )
            )

    for path_name, stale_phrases in ACTIVE_MECHANIC_ROUTE_STALE_ROLE_PHRASES.items():
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        for stale_phrase in stale_phrases:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "active mechanic route surface must use positive owner-route language instead of stale negative role scaffold "
                        f"{stale_phrase!r}",
                    )
                )

    for parent_name, path_name in zip(
        mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES,
        MECHANIC_PARENT_AGENTS_FILES,
        strict=True,
    ):
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(
                *MECHANIC_PARENT_AGENTS_DIRECTION_ROUTE_REQUIRED_TOKENS,
                f"`mechanics/{parent_name}/DIRECTION.md`",
                f"`mechanics/{parent_name}/PARTS.md`",
                f"`mechanics/{parent_name}/PROVENANCE.md`",
            ),
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        stale_route = MECHANIC_PARENT_AGENTS_STALE_PROVENANCE_ROUTE_TEMPLATE.format(
            parent_name=parent_name
        )
        if stale_route in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent AGENTS card must route PROVENANCE.md as the active-to-archive bridge; stale only-when legacy side-path wording is retired",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_DIRECTION_DECISION_NAME,
        tokens=MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PARENT_DIRECTION_DECISION_NAME,
            "Mechanic Parent Direction Contract",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Mechanic parent direction", "`DIRECTION.md`"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("DIRECTION.md", "current operating direction"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("DIRECTION.md", "current operating direction", "Entry Route"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=("target package `DIRECTION.md`", "current operating direction"),
        issues=issues,
    )
    return issues


def validate_mechanic_parent_guidance_boundary(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue

        allowed_guidance_docs = MECHANIC_PARENT_GUIDANCE_DOCS.get(
            parent_name,
            frozenset(),
        )
        for child in sorted(parent_root.iterdir(), key=lambda item: item.name):
            child_relative = child.relative_to(repo_root).as_posix()
            if child.is_file():
                if child.name not in MECHANIC_PARENT_ROOT_ALLOWED_FILES:
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected mechanic parent-root file must move under an owning part payload directory",
                        )
                    )
                continue
            if not child.is_dir():
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "unexpected mechanic parent-root entry must be a route file, parts/, legacy/, or explicit guidance docs/",
                    )
                )
                continue
            if child.name in MECHANIC_PARENT_ROOT_ALLOWED_DIRS:
                continue
            if child.name != "docs":
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "unexpected mechanic parent-root directory must move under parts/<part>/ or be declared as parent guidance",
                    )
                )
                continue
            if not allowed_guidance_docs:
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "parent-level docs/ is only for explicit mechanic-wide guidance; part-owned payload docs must live under parts/<part>/docs/",
                    )
                )
            entries = sorted(child.iterdir(), key=lambda item: item.name)
            if not entries:
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "empty parent-level docs/ directory must not be kept as future payload space",
                    )
                )
                continue
            for entry in entries:
                entry_relative = entry.relative_to(repo_root).as_posix()
                if not entry.is_file():
                    issues.append(
                        ValidationIssue(
                            entry_relative,
                            "parent-level docs/ may contain only explicitly allowlisted mechanic-wide guidance files",
                        )
                    )
                    continue
                if entry.name not in allowed_guidance_docs:
                    issues.append(
                        ValidationIssue(
                            entry_relative,
                            "unallowlisted parent-level docs must move under the owning part payload route",
                        )
                    )
                    continue
                guidance_text = read_text_or_issue(entry, issues, root=repo_root)
                if guidance_text is None:
                    continue
                for token in MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS:
                    if token not in guidance_text:
                        issues.append(
                            ValidationIssue(
                                entry_relative,
                                f"mechanic-wide guidance doc must expose parent guidance content contract token {token!r}",
                            )
                        )
            for doc_name in allowed_guidance_docs:
                if not (child / doc_name).is_file():
                    issues.append(
                        ValidationIssue(
                            f"mechanics/{parent_name}/docs/{doc_name}",
                            "allowlisted mechanic-wide guidance doc is missing",
                        )
                    )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
        tokens=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
            "Mechanic Parent Guidance Boundary",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("parent-level `docs/`", "part-owned payload"),
        issues=issues,
    )
    return issues


def validate_mechanics_parent_allowlist(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        issues.append(ValidationIssue("mechanics", "mechanics directory is missing"))
        return issues

    allowed_files = set(MECHANICS_ROOT_ALLOWED_FILES)
    allowed_parents = set(mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in mechanics_validator.validate_mechanic_parent_class_map(repo_root)
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in mechanic_legacy_validator.validate_mechanic_legacy_skeleton_surfaces(
            repo_root
        )
    )
    issues.extend(validate_mechanic_parent_guidance_boundary(repo_root))

    for path in sorted(mechanics_root.iterdir(), key=lambda item: item.name):
        relative = path.relative_to(repo_root).as_posix()
        if path.is_file():
            if path.name not in allowed_files:
                issues.append(
                    ValidationIssue(
                        relative,
                        "unexpected mechanics root file must be routed through an allowed source surface",
                    )
                )
            continue
        if not path.is_dir():
            issues.append(
                ValidationIssue(
                    relative,
                    "unexpected mechanics root entry must be a file route card or parent directory",
                )
            )
            continue
        if path.name not in allowed_parents:
            issues.append(
                ValidationIssue(
                    relative,
                    "mechanic parent must be declared in the evidence-cluster allowlist",
                )
            )

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        if not (mechanics_root / parent_name).is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}",
                    "declared mechanic parent directory is missing",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "Active Packages",
            "Package taxonomy requires source surfaces, inputs, outputs, boundaries",
            "Provenance Bridge And Archive Boundary",
            "`PROVENANCE.md`",
            "legacy archive",
            "archive-local accounting",
            "archive internals",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=tuple(f"`{parent_name}`" for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_ALLOWLIST_DECISION_NAME,
        tokens=MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name in MECHANIC_ROUTE_CARD_FILES:
        if not (repo_root / path_name).is_file():
            issues.append(
                ValidationIssue(
                    path_name,
                    "active mechanic parent must expose AGENTS.md, README.md, DIRECTION.md, and PARTS.md",
                )
            )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "top-level mechanics parents are validator allowlisted",
            "mechanics/EVIDENCE_CLUSTERS.md",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(MECHANIC_PARENT_ALLOWLIST_DECISION_NAME, "Mechanic Parent Allowlist"),
        issues=issues,
    )
    return issues


def validate_forbidden_active_mechanics_paths(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name in FORBIDDEN_ACTIVE_MECHANICS_PATHS:
        if (repo_root / path_name).exists():
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy mechanics path must not exist as an active route",
                )
            )
    return issues


def validate_mechanic_parent_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanics_parent_allowlist(repo_root))
    issues.extend(validate_mechanic_parent_direction_surfaces(repo_root))
    issues.extend(validate_mechanic_index_command_ownership(repo_root))
    issues.extend(validate_mechanic_lower_parts_index_operating_cards(repo_root))
    issues.extend(validate_forbidden_active_mechanics_paths(repo_root))
    return issues
