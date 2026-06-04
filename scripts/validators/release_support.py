"""Release-support route, readiness, closeout, and PR-handoff contracts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping


REPO_REF_PREFIX = "repo:"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

RELEASE_SUPPORT_READINESS_AUDIT_NAME = (
    "mechanics/release-support/parts/readiness-audit/reports/"
    "release-support-readiness-audit-v1.json"
)
RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md"
)
STRATEGIC_CLOSEOUT_AUDIT_NAME = (
    "mechanics/release-support/parts/strategic-closeout/reports/"
    "strategic-closeout-audit-v1.json"
)
STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0026-strategic-closeout-audit.md"
)
RELEASE_PREP_PR_HANDOFF_NAME = (
    "mechanics/release-support/parts/pr-handoff/reports/"
    "release-prep-pr-handoff-v1.json"
)
RELEASE_PREP_PR_HANDOFF_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0027-release-prep-pr-handoff.md"
)

RELEASE_SUPPORT_MECHANIC_README_NAME = "mechanics/release-support/README.md"
RELEASE_SUPPORT_MECHANIC_AGENTS_NAME = "mechanics/release-support/AGENTS.md"
RELEASE_SUPPORT_MECHANIC_PARTS_NAME = "mechanics/release-support/PARTS.md"
RELEASE_SUPPORT_MECHANIC_PARTS_README_NAME = "mechanics/release-support/parts/README.md"
RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME = "mechanics/release-support/PROVENANCE.md"
RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME = (
    "mechanics/release-support/parts/readiness-audit/README.md"
)
RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME = (
    "mechanics/release-support/parts/strategic-closeout/README.md"
)
RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME = (
    "mechanics/release-support/parts/pr-handoff/README.md"
)
RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0058-release-support-part-contract-guard.md"
)
RELEASE_SUPPORT_LEGACY_INDEX_NAME = "mechanics/release-support/legacy/INDEX.md"
RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/release-support/legacy/DISTILLATION_LOG.md"
)
RELEASE_SUPPORT_LEGACY_RAW_README_NAME = "mechanics/release-support/legacy/raw/README.md"
RELEASE_SUPPORT_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0014-release-support-mechanic-package.md"
)

LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language"
)
ACTIVE_LEGACY_PARENT_WORDING_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k active_mechanic_route_residue"
)
ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k root_authored_route_residue"
)
DECISION_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k decision_route_residue"
)
REPO_CONFIG_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k repo_config_route_residue"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k source_bundle_route_residue"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k mechanic_payload_route_residue"
)
MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory"
)
MECHANIC_PART_VALIDATION_COMMAND_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command"
)
MECHANIC_PARTS_INDEX_SYNC_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture"
)
MECHANIC_PARENT_DIRECTION_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_direction.py -k mechanic_parent_direction"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_dimension"
)
MECHANIC_ROOT_DISTRICT_RECON_COMMAND = (
    "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND = "python -m pytest -q tests/test_mechanics_topology.py"

MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)

RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS = (
    "release_support_readiness_audit",
    "local_release_prep_review_ready_with_open_landing",
    "accumulated_strategic_refactor_diff",
    "ready_for_release_prep_review",
    "not_published",
    "not_created",
    "not_opened",
    "not_observed_for_this_uncommitted_diff",
    "not_complete",
    "not_attempted",
    "not a release",
    "not a tag",
    "not GitHub Repo Validation",
    "not goal completion",
)
RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS = (
    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
    "scripts/release_check.py",
    "GitHub `Repo Validation`",
    "not the same as a bounded release-prep review",
    "no tag",
    "no GitHub Release",
    "no PR approval",
    "no goal completion",
)
STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS = (
    "strategic_closeout_audit",
    "current_objective_audit_and_landing_route_in_progress_after_mechanics_validation_hardening",
    "not_complete_pending_requirement_audit_and_landing_route",
    "satisfied_for_local_refactor",
    "meta_truth_and_positive_boundary",
    "codex_maxxing_durable_loop",
    "phase_8_active_proof_loop",
    "trap_audit_and_completion_boundary",
    "does not mark the goal complete",
    "does not treat PR or GitHub landing alone as objective completion",
    "requirement-by-requirement mechanics objective audit",
    "does not publish an eval result receipt",
    "does not mutate sibling repos",
)
STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS = (
    STRATEGIC_CLOSEOUT_AUDIT_NAME,
    "requirement-by-requirement",
    "current objective audit",
    "not a PR ritual",
    "GitHub `Repo Validation`",
    "live eval-result receipt",
    "mutate sibling repos",
)
RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS = (
    "release_prep_pr_handoff",
    "ready_for_owner_landing_route_with_open_pr",
    "pre_pr_handoff_snapshot",
    "pre_landing_worktree_posture",
    "dirty_uncommitted_local_diff",
    "pre_handoff_github_status",
    "not_created_by_this_handoff",
    "not_opened",
    "not_observed_for_this_uncommitted_diff",
    "candidate_branch_name",
    "candidate_pr_title",
    "draft_pr_body",
    "At the snapshot time",
    "did not create a branch",
    "did not create a commit",
    "did not push",
    "did not open a PR",
    "did not observe GitHub Repo Validation",
    "did not mark the goal complete",
    "supersedes this snapshot",
)
RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS = (
    RELEASE_PREP_PR_HANDOFF_NAME,
    "PR shape prepared",
    "this artifact alone is not PR evidence",
    "GitHub `Repo Validation`",
    "not an explicit commit/push/merge instruction",
    "Do not infer from this artifact alone that a branch was created",
    "After a branch or PR exists",
    "mutate sibling repos",
    "mark the goal complete",
)

RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "PARTS.md",
    "docs/operations/RELEASING.md",
    "CHANGELOG.md",
    "scripts/release_check.py",
    ".github/workflows/repo-validation.yml",
    "parts/readiness-audit",
    "parts/strategic-closeout",
    "parts/pr-handoff",
    "tests/test_release_support_readiness_audit.py",
    "tests/test_strategic_closeout_audit.py",
    "tests/test_release_prep_pr_handoff.py",
    "Repo Validation",
    "pre-PR owner landing handoff",
    "bounded release scope",
    "changelog narrative",
    "GitHub release notes",
    "eval claim strength stays with source proof surfaces",
    "AGENTS.md#validation",
    "owns command execution",
)
RELEASE_SUPPORT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "bounded `aoa-evals` release",
    "mechanics/release-support/PARTS.md",
    "mechanics/release-support/parts/",
    "CHANGELOG.md",
    "scripts/release_check.py",
    "Repo Validation",
    "plain tag-shaped",
    "bundle-local review",
    "python scripts/release_check.py",
)
RELEASE_SUPPORT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/release-support/",
    "mechanics/release-support/parts/",
    "bounded release scope",
    "changelog narrative",
    "release audit",
    "Repo Validation",
    "does not create a tag",
    "release notes",
    "bundle-local `EVAL.md`",
)
RELEASE_SUPPORT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "Release Support / Part Index",
    "CHANGELOG.md",
    "docs/operations/RELEASING.md",
    "scripts/release_check.py",
    ".github/workflows/repo-validation.yml",
    "Readiness Audit",
    "Strategic Closeout",
    "PR Handoff",
    "Live publication state is",
)
RELEASE_SUPPORT_PARTS_README_REQUIRED_TOKENS = (
    "Release Support / Parts Route",
    "Readiness Audit",
    "Strategic Closeout",
    "PR Handoff",
    "current git and GitHub evidence own live branch",
)
RELEASE_SUPPORT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "VALIDATION.md",
    "parent `parts/AGENTS.md` lane",
)
RELEASE_SUPPORT_READINESS_AUDIT_PART_REQUIRED_TOKENS = (
    "Readiness Audit",
    "release_support_readiness_audit",
    "publication_boundary",
    "GitHub PR approval and Repo Validation",
    "current git branch/merge state",
    "current goal review",
    "not_complete",
    "readiness audit treated as tag",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_REQUIRED_TOKENS = (
    "Strategic Closeout",
    "strategic_closeout_audit",
    "goal_completion_status",
    "not_complete",
    "owner-visible final audit",
    "local handoff readiness as goal completion",
    "open landing requirements stay visible",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_PR_HANDOFF_PART_REQUIRED_TOKENS = (
    "PR Handoff",
    "release_prep_pr_handoff",
    "pre_handoff_github_status",
    "draft PR body",
    "Live GitHub state is owned by current local git",
    "snapshot treated as created branch",
    "current git and GitHub evidence replace this snapshot",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Release Support Part Contract Guard",
    "mechanics/release-support/parts/readiness-audit/README.md",
    "mechanics/release-support/parts/strategic-closeout/README.md",
    "mechanics/release-support/parts/pr-handoff/README.md",
    "part-level contracts",
    "readiness-audit",
    "strategic-closeout",
    "pr-handoff",
    "stronger owner split",
    "stop-lines",
    "not_complete",
    "python scripts/release_check.py",
)
RELEASE_SUPPORT_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/proof-release/",
    "mechanics/release-support/",
    "reports/proof-release-readiness-audit-v1.json",
    "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
    "tests/test_proof_release_readiness_audit.py",
    "mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py",
    "docs/decisions/0014-proof-release-mechanic-package.md",
    "docs/decisions/AOA-EV-D-0014-release-support-mechanic-package.md",
)
RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-release",
    "release-support",
    "readiness-audit",
    "strategic-closeout",
    "pr-handoff",
    "Current route:",
    "new release-support work starts in the owning active part",
)
RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    search_text = text
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def parse_repo_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(ValidationIssue(location, "reference must include a repo name and repo-relative path"))
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = repo_ref_roots.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if repo_name != "aoa-evals" and not strict_sibling_compat:
        return repo_name, target, anchor or None
    if not repo_root.exists():
        issues.append(
            ValidationIssue(
                location,
                f"strict sibling compatibility requires available repo root for {repo_name}: {repo_root}",
            )
        )
        return None
    if not target.exists():
        issues.append(ValidationIssue(location, f"reference target does not exist: {repo_name}/{path_text}"))
        return None

    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'"))
            return None
        if anchor not in markdown_anchors(target):
            issues.append(ValidationIssue(location, f"markdown anchor does not exist for ref '{raw_ref}'"))
            return None

    return repo_name, target, anchor or None


def _repo_ref_roots(repo_root: Path, repo_ref_roots: Mapping[str, Path] | None) -> Mapping[str, Path]:
    if repo_ref_roots is None:
        return {"aoa-evals": repo_root}
    return repo_ref_roots


def _require_route_tokens(
    repo_root: Path,
    issues: list[ValidationIssue],
    checks: Iterable[tuple[str, Iterable[str]]],
) -> None:
    for path_name, tokens in checks:
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)


def _validate_repo_ref_list(
    refs: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> None:
    if not isinstance(refs, list) or not refs:
        issues.append(ValidationIssue(location, "evidence_refs must be a non-empty list"))
        return
    for ref_index, evidence_ref in enumerate(refs):
        parse_repo_ref(
            evidence_ref,
            location=f"{location}[{ref_index}]",
            issues=issues,
            repo_ref_roots=repo_ref_roots,
            strict_sibling_compat=strict_sibling_compat,
        )


def _validate_required_object_ids(
    entries: Any,
    *,
    location: str,
    id_key: str,
    required_ids: set[str],
    status_value: str | None,
    min_claim_limit_length: int,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> None:
    if not isinstance(entries, list):
        issues.append(ValidationIssue(location, f"{location.rsplit('.', 1)[-1]} must be a list"))
        return
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        entry_location = f"{location}[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(entry_location, f"{id_key.removesuffix('_id')} entry must be an object"))
            continue
        entry_id = entry.get(id_key)
        if isinstance(entry_id, str):
            seen_ids.add(entry_id)
        else:
            issues.append(ValidationIssue(entry_location, f"{id_key} must be a string"))
        if status_value is not None and entry.get("status") != status_value:
            issues.append(ValidationIssue(entry_location, f"status must stay '{status_value}'"))
        if "evidence_refs" in entry:
            _validate_repo_ref_list(
                entry.get("evidence_refs"),
                location=f"{entry_location}.evidence_refs",
                issues=issues,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        claim_limit = entry.get("claim_limit")
        if not isinstance(claim_limit, str) or len(claim_limit) < min_claim_limit_length:
            issues.append(ValidationIssue(entry_location, "claim_limit must be a meaningful string"))
    for missing_id in sorted(required_ids - seen_ids):
        issues.append(ValidationIssue(location, f"missing {id_key} {missing_id!r}"))


def _validate_verification_snapshot(
    payload: dict[str, Any],
    *,
    location: str,
    required_commands: set[str],
    issues: list[ValidationIssue],
) -> None:
    verification_snapshot = payload.get("verification_snapshot")
    if not isinstance(verification_snapshot, list):
        issues.append(ValidationIssue(location, "verification_snapshot must be a list"))
        return
    seen_commands: set[str] = set()
    for index, entry in enumerate(verification_snapshot):
        entry_location = f"{location}.verification_snapshot[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(entry_location, "verification entry must be an object"))
            continue
        command = entry.get("command")
        if isinstance(command, str):
            seen_commands.add(command)
        else:
            issues.append(ValidationIssue(entry_location, "command must be a string"))
        if entry.get("result") != "passed":
            issues.append(ValidationIssue(entry_location, "result must stay 'passed'"))
        claim_limit = entry.get("claim_limit")
        if not isinstance(claim_limit, str) or len(claim_limit) < 20:
            issues.append(ValidationIssue(entry_location, "claim_limit must be a meaningful string"))
    for command in sorted(required_commands - seen_commands):
        issues.append(
            ValidationIssue(
                f"{location}.verification_snapshot",
                f"missing verification command {command!r}",
            )
        )


def _require_joined_list_tokens(
    payload: dict[str, Any],
    *,
    location: str,
    key: str,
    tokens: Iterable[str],
    message_name: str,
    issues: list[ValidationIssue],
) -> None:
    value = payload.get(key)
    if not isinstance(value, list):
        issues.append(ValidationIssue(location, f"{key} must be a list"))
        return
    joined = "\n".join(item for item in value if isinstance(item, str))
    for token in tokens:
        if token not in joined:
            issues.append(ValidationIssue(f"{location}.{key}", f"{message_name} must mention '{token}'"))


def _require_claim_limit_tokens(
    payload: dict[str, Any],
    *,
    location: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> None:
    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
        return
    for token in tokens:
        if token not in claim_limit:
            issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))


def validate_release_support_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_SUPPORT_MECHANIC_README_NAME, RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_AGENTS_NAME, RELEASE_SUPPORT_MECHANIC_AGENTS_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_PARTS_NAME, RELEASE_SUPPORT_MECHANIC_PARTS_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_PARTS_README_NAME, RELEASE_SUPPORT_PARTS_README_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
                RELEASE_SUPPORT_READINESS_AUDIT_PART_REQUIRED_TOKENS,
            ),
            (
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_REQUIRED_TOKENS,
            ),
            (RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME, RELEASE_SUPPORT_PR_HANDOFF_PART_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME,
                RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
            ),
            (
                DECISION_RECORDS_README_NAME,
                (RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME, "Release Support Part Contract Guard"),
            ),
            (RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME, RELEASE_SUPPORT_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_INDEX_NAME, RELEASE_SUPPORT_LEGACY_INDEX_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME, RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_RAW_README_NAME, RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_DECISION_NAME, RELEASE_SUPPORT_MECHANIC_DECISION_REQUIRED_TOKENS),
        ),
    )
    return issues


def validate_release_support_readiness_audit_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = _repo_ref_roots(repo_root, repo_ref_roots)
    audit_path = repo_root / RELEASE_SUPPORT_READINESS_AUDIT_NAME
    location = RELEASE_SUPPORT_READINESS_AUDIT_NAME

    _require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_SUPPORT_READINESS_AUDIT_NAME, RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME,
                RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS,
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "Readiness Audit",
                    "GitHub Release evidence",
                    "GitHub `Repo Validation`",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
                (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "readiness audits", "GitHub `Repo Validation`"),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "local release-prep reviewability evidence",
                    "current git, GitHub, tag, release, PR, and objective evidence",
                ),
            ),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "GitHub PR approval and Repo Validation",
                    "current goal review",
                ),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "goal completion")),
            (
                DECISION_RECORDS_README_NAME,
                (RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME, "release-prep PR handoff"),
            ),
        ),
    )

    payload = load_json_payload(audit_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "release-support readiness audit must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "release_support_readiness_audit",
        "schema_version": 1,
        "audit_id": "release-support-readiness-audit-v1",
        "audited_at": "2026-05-19",
        "scope_kind": "accumulated_strategic_refactor_diff",
        "readiness_verdict": "local_release_prep_review_ready_with_open_landing",
        "changelog_anchor_ref": "repo:aoa-evals/CHANGELOG.md",
        "release_support_mechanic_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_MECHANIC_README_NAME}",
        "release_check_ref": "repo:aoa-evals/scripts/release_check.py",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    release_scope = payload.get("release_scope")
    if not isinstance(release_scope, str):
        issues.append(ValidationIssue(location, "release_scope must be a string"))
    else:
        for token in (
            "Unreleased",
            "strategic refactor",
            "root design",
            "proof topology",
            "proof-loop reports",
            "receipt-intake dry review",
            "validators",
        ):
            if token not in release_scope:
                issues.append(ValidationIssue(location, f"release_scope must mention '{token}'"))

    _validate_required_object_ids(
        payload.get("requirements_review"),
        location=f"{location}.requirements_review",
        id_key="requirement_id",
        required_ids={
            "root_design_spine",
            "decision_memory",
            "roadmap_quest_and_lifecycle_route",
            "proof_topology_legacy_and_mechanics",
            "proof_loop_materialization",
            "generated_reader_freshness",
            "local_release_gate_coverage",
            "sibling_boundary_and_canary",
        },
        status_value="ready_for_release_prep_review",
        min_claim_limit_length=20,
        issues=issues,
        repo_ref_roots=refs,
        strict_sibling_compat=strict_sibling_compat,
    )

    _validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
            MECHANIC_PARTS_INDEX_SYNC_COMMAND,
            MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
            "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
            MECHANIC_PARENT_DIRECTION_COMMAND,
            MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
            MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
            ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
            ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
            ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
            DECISION_ROUTE_RESIDUE_COMMAND,
            REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
            SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python scripts/validate_nested_agents.py",
            "python scripts/build_catalog.py --check",
            "python scripts/generate_eval_report_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
            "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
            "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
            "python -m pytest -q",
            "python scripts/release_check.py",
            "git diff --check",
        },
        issues=issues,
    )

    publication_boundary = payload.get("publication_boundary")
    if isinstance(publication_boundary, dict):
        expected_boundary_values = {
            "release_publication_status": "not_published",
            "tag_status": "not_created",
            "github_release_status": "not_published",
            "github_pr_status": "not_opened",
            "github_repo_validation_status": "not_observed_for_this_uncommitted_diff",
            "goal_completion_status": "not_complete",
            "live_receipt_publication_status": "not_attempted",
        }
        for key, expected in expected_boundary_values.items():
            if publication_boundary.get(key) != expected:
                issues.append(ValidationIssue(f"{location}.publication_boundary", f"{key} must be {expected!r}"))
        boundary = publication_boundary.get("boundary")
        if not isinstance(boundary, str):
            issues.append(ValidationIssue(f"{location}.publication_boundary", "boundary must be a string"))
        else:
            for token in (
                "not a release",
                "not a tag",
                "not GitHub Repo Validation",
                "not a GitHub Release",
                "not PR approval",
                "not an eval result receipt",
                "not goal completion",
            ):
                if token not in boundary:
                    issues.append(
                        ValidationIssue(
                            f"{location}.publication_boundary.boundary",
                            f"boundary must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(location, "publication_boundary must be a JSON object"))

    _require_joined_list_tokens(
        payload,
        location=location,
        key="open_requirements_before_publication",
        tokens=(
            "review the accumulated diff",
            "open a PR",
            "observe GitHub Repo Validation",
            "merge only after required checks are green",
            "create any tag or GitHub Release only after",
            "goal completion audit",
        ),
        message_name="open requirements",
        issues=issues,
    )
    _require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "does not publish a release",
            "create a tag",
            "open or approve a PR",
            "observe GitHub Repo Validation",
            "publish an eval result receipt",
            "mutate sibling repos",
            "mark the aoa-evals strategic goal complete",
        ),
        issues=issues,
    )
    return issues


def validate_strategic_closeout_audit_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = _repo_ref_roots(repo_root, repo_ref_roots)
    audit_path = repo_root / STRATEGIC_CLOSEOUT_AUDIT_NAME
    location = STRATEGIC_CLOSEOUT_AUDIT_NAME

    _require_route_tokens(
        repo_root,
        issues,
        (
            (STRATEGIC_CLOSEOUT_AUDIT_NAME, STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS),
            (STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME, STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
                (
                    STRATEGIC_CLOSEOUT_AUDIT_NAME,
                    "goal open",
                    "GitHub",
                    "current objective audit",
                ),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    STRATEGIC_CLOSEOUT_AUDIT_NAME,
                    "requirement-by-requirement handoff evidence",
                    "current objective audit and landing evidence",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (STRATEGIC_CLOSEOUT_AUDIT_NAME, "Strategic Closeout Audit", "Goal completion routes"),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (STRATEGIC_CLOSEOUT_AUDIT_NAME, "goal completion")),
            (DECISION_RECORDS_README_NAME, (STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME, "Goal completion")),
        ),
    )

    payload = load_json_payload(audit_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "strategic closeout audit must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "strategic_closeout_audit",
        "schema_version": 1,
        "audit_id": "strategic-closeout-audit-v1",
        "audited_at": "2026-05-19",
        "scope_kind": "local_strategic_refactor_diff",
        "completion_verdict": "current_objective_audit_and_landing_route_in_progress_after_mechanics_validation_hardening",
        "goal_completion_status": "not_complete_pending_requirement_audit_and_landing_route",
        "release_support_readiness_audit_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_READINESS_AUDIT_NAME}",
        "decision_ref": f"repo:aoa-evals/{STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME}",
        "current_objective_ref": (
            "thread goal: deep mechanics refactor as proof-side organ with evidence-derived parent map, "
            "part contracts, active-first legacy, and source-of-truth validation"
        ),
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    source_plan_ref = payload.get("source_plan_ref")
    if not isinstance(source_plan_ref, str):
        issues.append(ValidationIssue(location, "source_plan_ref must be a string"))
    else:
        for token in ("operator working note", "outside the repository"):
            if token not in source_plan_ref:
                issues.append(ValidationIssue(location, f"source_plan_ref must mention '{token}'"))
        if "/home/" in source_plan_ref:
            issues.append(ValidationIssue(location, "source_plan_ref must not expose an absolute host path"))

    _validate_required_object_ids(
        payload.get("requirements_review"),
        location=f"{location}.requirements_review",
        id_key="requirement_id",
        required_ids={
            "meta_truth_and_positive_boundary",
            "codex_maxxing_durable_loop",
            "aoa_law_and_sibling_meta_examples",
            "phase_0_truth_map",
            "phase_1_root_design_spine",
            "phase_2_decision_lane",
            "phase_3_roadmap_changelog_questbook_quests",
            "phase_4_proof_topology",
            "phase_5_mechanics_atlas_and_packages",
            "phase_6_legacy_provenance",
            "phase_7_validator_invariants",
            "phase_8_active_proof_loop",
            "runtime_machine_boundary",
            "spark_agent_lane_cleanup",
            "release_readiness",
            "trap_audit_and_completion_boundary",
        },
        status_value="satisfied_for_local_refactor",
        min_claim_limit_length=40,
        issues=issues,
        repo_ref_roots=refs,
        strict_sibling_compat=strict_sibling_compat,
    )

    trap_review = payload.get("trap_review")
    if isinstance(trap_review, list):
        seen_trap_ids: set[str] = set()
        for index, trap in enumerate(trap_review):
            trap_location = f"{location}.trap_review[{index}]"
            if not isinstance(trap, dict):
                issues.append(ValidationIssue(trap_location, "trap entry must be an object"))
                continue
            trap_id = trap.get("trap_id")
            if isinstance(trap_id, str):
                seen_trap_ids.add(trap_id)
            else:
                issues.append(ValidationIssue(trap_location, "trap_id must be a string"))
            mitigation = trap.get("mitigation")
            if not isinstance(mitigation, str) or len(mitigation) < 40:
                issues.append(ValidationIssue(trap_location, "mitigation must be a meaningful string"))
        for trap_id in sorted(
            {
                "durable_note_trap",
                "root_design_overreach",
                "decision_lane_ceremony",
                "questbook_gravity",
                "mechanics_explosion",
                "sibling_compatibility_swamp",
                "machine_gravity",
                "positive_boundary_erosion",
                "legacy_permanence",
                "validation_theatre",
                "release_check_spiral",
                "active_use_premature_connection",
            }
            - seen_trap_ids
        ):
            issues.append(ValidationIssue(f"{location}.trap_review", f"missing trap_id {trap_id!r}"))
    else:
        issues.append(ValidationIssue(location, "trap_review must be a list"))

    _validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py",
            "python -m pytest -q tests/test_generated_route_residue.py",
            ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
            ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
            ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
            DECISION_ROUTE_RESIDUE_COMMAND,
            REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
            SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
            "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
            MECHANIC_PARTS_INDEX_SYNC_COMMAND,
            MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
            "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
            MECHANIC_PARENT_DIRECTION_COMMAND,
            MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
            MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python scripts/validate_nested_agents.py",
            "git diff --check",
            "python scripts/build_catalog.py --check",
            "python scripts/generate_eval_report_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
            "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
            "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
            "python -m pytest -q",
            "python scripts/release_check.py",
        },
        issues=issues,
    )

    _require_joined_list_tokens(
        payload,
        location=location,
        key="open_items_before_goal_completion",
        tokens=(
            "requirement-by-requirement mechanics objective audit",
            "cross-root evidence clusters",
            "payload coverage anchors",
            "PROVENANCE.md",
            "old names",
            "full local validation battery",
            "requested landing route",
            "GitHub Repo Validation",
            "clean worktree",
        ),
        message_name="open items",
        issues=issues,
    )
    _require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "does not mark the goal complete",
            "does not treat PR or GitHub landing alone as objective completion",
            "does not publish a release",
            "does not create a tag",
            "does not publish a GitHub Release",
            "does not publish an eval result receipt",
            "does not promote any bundle",
            "does not accept runtime evidence",
            "does not mutate sibling repos",
        ),
        issues=issues,
    )
    return issues


def validate_release_prep_pr_handoff_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = _repo_ref_roots(repo_root, repo_ref_roots)
    handoff_path = repo_root / RELEASE_PREP_PR_HANDOFF_NAME
    location = RELEASE_PREP_PR_HANDOFF_NAME

    _require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_PREP_PR_HANDOFF_NAME, RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS),
            (RELEASE_PREP_PR_HANDOFF_DECISION_NAME, RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "branch", "GitHub evidence", "goal completion"),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    RELEASE_PREP_PR_HANDOFF_NAME,
                    "pre-PR snapshot",
                    "current git and GitHub evidence for live branch, commit, push, PR",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "Release Prep PR Handoff", "snapshot status for branch"),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "live PR or GitHub `Repo Validation` state"),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (RELEASE_PREP_PR_HANDOFF_NAME, "goal completion")),
            (DECISION_RECORDS_README_NAME, (RELEASE_PREP_PR_HANDOFF_DECISION_NAME, "live PR status")),
        ),
    )

    payload = load_json_payload(handoff_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "release-prep PR handoff must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "release_prep_pr_handoff",
        "schema_version": 1,
        "handoff_id": "release-prep-pr-handoff-v1",
        "prepared_at": "2026-05-19",
        "scope_kind": "accumulated_strategic_refactor_diff",
        "status_snapshot_kind": "pre_pr_handoff_snapshot",
        "pre_landing_worktree_posture": "dirty_uncommitted_local_diff",
        "source_readiness_audit_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_READINESS_AUDIT_NAME}",
        "source_strategic_closeout_audit_ref": f"repo:aoa-evals/{STRATEGIC_CLOSEOUT_AUDIT_NAME}",
        "decision_ref": f"repo:aoa-evals/{RELEASE_PREP_PR_HANDOFF_DECISION_NAME}",
        "handoff_verdict": "ready_for_owner_landing_route_with_open_pr",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    for key in ("candidate_branch_name", "candidate_commit_message", "candidate_pr_title"):
        value = payload.get(key)
        if not isinstance(value, str) or len(value) < 10:
            issues.append(ValidationIssue(location, f"{key} must be a meaningful string"))

    github_status = payload.get("pre_handoff_github_status")
    if isinstance(github_status, dict):
        for key, expected in {
            "branch_status": "not_created_by_this_handoff",
            "commit_status": "not_created_by_this_handoff",
            "push_status": "not_attempted",
            "pr_status": "not_opened",
            "repo_validation_status": "not_observed_for_this_uncommitted_diff",
            "merge_status": "not_attempted",
            "tag_status": "not_created",
            "github_release_status": "not_published",
        }.items():
            if github_status.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{location}.pre_handoff_github_status",
                        f"pre_handoff {key} must be {expected!r}",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "pre_handoff_github_status must be a JSON object"))

    changed_groups = payload.get("changed_surface_groups")
    if isinstance(changed_groups, list):
        seen_group_ids: set[str] = set()
        for index, group in enumerate(changed_groups):
            group_location = f"{location}.changed_surface_groups[{index}]"
            if not isinstance(group, dict):
                issues.append(ValidationIssue(group_location, "changed surface group must be an object"))
                continue
            group_id = group.get("group_id")
            if isinstance(group_id, str):
                seen_group_ids.add(group_id)
            else:
                issues.append(ValidationIssue(group_location, "group_id must be a string"))
            summary = group.get("summary")
            if not isinstance(summary, str) or len(summary) < 30:
                issues.append(ValidationIssue(group_location, "summary must be a meaningful string"))
            _validate_repo_ref_list(
                group.get("evidence_refs"),
                location=f"{group_location}.evidence_refs",
                issues=issues,
                repo_ref_roots=refs,
                strict_sibling_compat=strict_sibling_compat,
            )
        for group_id in sorted(
            {
                "root_design_and_route",
                "decision_memory",
                "roadmap_changelog_quests",
                "proof_topology_legacy_mechanics",
                "active_proof_loop",
                "agent_lane_and_generated_readers",
                "validators_and_tests",
            }
            - seen_group_ids
        ):
            issues.append(ValidationIssue(f"{location}.changed_surface_groups", f"missing group_id {group_id!r}"))
    else:
        issues.append(ValidationIssue(location, "changed_surface_groups must be a list"))

    _require_joined_list_tokens(
        payload,
        location=location,
        key="draft_pr_body",
        tokens=(
            "## Summary",
            "## Validation",
            "## Boundaries",
            "python scripts/validate_repo.py",
            "python scripts/release_check.py",
            "no tag or GitHub Release",
            "no live eval-result receipt publication",
            "no runtime evidence acceptance",
            "no sibling repository mutation",
            "goal completion remains open",
        ),
        message_name="draft PR body",
        issues=issues,
    )

    _validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py",
            "python -m pytest -q tests/test_generated_route_residue.py",
            ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
            ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
            ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
            DECISION_ROUTE_RESIDUE_COMMAND,
            REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
            SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
            "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
            MECHANIC_PARTS_INDEX_SYNC_COMMAND,
            MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
            "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
            MECHANIC_PARENT_DIRECTION_COMMAND,
            MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
            MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python scripts/validate_nested_agents.py",
            "git diff --check",
            "python scripts/build_catalog.py --check",
            "python scripts/generate_eval_report_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
            "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
            "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
            "python -m pytest -q",
            "python scripts/release_check.py",
        },
        issues=issues,
    )

    _require_joined_list_tokens(
        payload,
        location=location,
        key="landing_steps",
        tokens=(
            "create a branch",
            "commit the intended accumulated diff",
            "push the branch",
            "open a PR",
            "watch GitHub Repo Validation",
            "merge only after required checks are green",
            "worktree is clean",
            "final owner-visible completion audit",
        ),
        message_name="landing steps",
        issues=issues,
    )
    _require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "At the snapshot time",
            "did not create a branch",
            "did not create a commit",
            "did not push",
            "did not open a PR",
            "did not observe GitHub Repo Validation",
            "did not merge",
            "did not publish a release",
            "did not create a tag",
            "did not publish a GitHub Release",
            "did not publish an eval result receipt",
            "did not promote any bundle",
            "did not accept runtime evidence",
            "did not mutate sibling repos",
            "did not mark the goal complete",
            "supersedes this snapshot",
        ),
        issues=issues,
    )
    return issues
