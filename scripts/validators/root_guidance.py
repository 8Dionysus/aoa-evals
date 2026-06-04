"""Root guidance, README, and operations route contracts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue


RELEASING_GUIDE_NAME = "docs/operations/RELEASING.md"
RELEASING_ROUTE_MAP_REQUIRED_TOKENS = (
    "## Operating Card",
    "root release process guide",
    "bounded release scope",
    "readiness/live-status route",
    "release-support validation lane",
    "root validation lane",
    "local release-prep reviewability evidence",
    "current git, GitHub, tag, release, PR, and objective evidence",
    "requirement-by-requirement handoff evidence",
    "current objective audit and landing evidence",
    "pre-PR snapshot",
    "current git and GitHub evidence for live branch, commit, push, PR",
)
RELEASING_FORBIDDEN_STATUS_LEDGER_TOKENS = (
    "not a tag",
    "not a branch",
    "not goal completion",
    "goal-completion proof",
)

ROOT_README_SURFACE_REQUIRED_TOKENS = (
    "# aoa-evals Bounded Proof Canon",
    "AoA proof canon",
    "bounded proof surface",
    "repo to authority class",
    "docs/architecture/AGENT_INDEX.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/README.md",
    "Eval Bundle Selection Chooser",
    "Eval Bundle Index",
    "public proof-organ entry",
    "Agent route law and local checks",
    "Executable validation routes live in",
    "practice canon -> workflow canon -> proof canon",
)
ROOT_README_SURFACE_FORBIDDEN_TOKENS = (
    "Which comparison, artifact/process, repeated-window, or shared-infra guide applies?",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "generated/eval_report_index.min.json",
    "generated/comparison_spine.json",
)

DOCS_README_ROUTE_MAP_REQUIRED_TOKENS = (
    "# Documentation Map",
    "human and agent entrypoint",
    "Operational edit law belongs in the nearest `AGENTS.md`",
    "aoa-evals Bounded Proof Canon",
    "Mechanics Operation Atlas",
    "Decision Records Index",
    "Eval Bundle Selection Chooser",
    "Eval Bundle Index",
    "Folder Map",
    "docs/architecture/",
    "docs/guides/",
    "docs/operations/",
    "Route Residue Guards",
    "Recommended Reading Paths",
    "Mechanics Refactor Path",
    "Validation Route",
    "docs/AGENTS.md#validation",
)
DOCS_README_ROUTE_MAP_FORBIDDEN_TOKENS = (
    "[Mechanics](../mechanics/README.md)",
    "[Decisions](decisions/README.md)",
    "[README](../README.md)",
    "[EVAL_SELECTION]",
    "[EVAL_INDEX]",
    "Verify Current Surfaces",
)

EVAL_PHILOSOPHY_ROUTE_MAP_REQUIRED_TOKENS = (
    "## Operating Card",
    "epistemic posture guide for bounded proof",
    "proof distinction, owner route, interpretation boundary",
    "## Core distinction routes",
    "artifact looks convincing",
    "memory looks relevant",
    "project-local success looks portable",
    "growth story looks tempting",
    "Read every metric as one bounded signal inside a review.",
    "Strong claims require named blind spots.",
    "public proof waits for a portable route",
    "growth organ and proof discipline",
    "Weak form:",
    "Bounded form:",
)
EVAL_PHILOSOPHY_FORBIDDEN_FLAT_NEGATIVE_TOKENS = (
    "Neither fact alone proves quality.",
    "Neither is enough by itself.",
    "Never as the whole truth of quality.",
    "Blind spots are not embarrassing leftovers.",
    "not ready to make strong claims",
    "not humiliation and not performance theater",
    "not a punishment ritual",
    "Not:\n- \"the agent is good\"",
)

PORTABLE_EVAL_BOUNDARY_GUIDE_NAME = "docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md"
PORTABLE_EVAL_BOUNDARY_GUIDE_REQUIRED_TOKENS = (
    "portability route for evaluation bundles",
    "Operating Card",
    "replacement contract that preserves the claim class",
    "public setup and replacement rules",
    "bounded portable meaning",
    "claim, fixture contract, verdict logic",
)
PORTABLE_EVAL_BOUNDARY_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "movable without letting local context",
    "what it does not measure",
    "without hidden private knowledge",
    "but they should not depend on",
    "Full universality is not required",
    "Do not confuse portability with scale",
)

CLOSEOUT_WRITEBACK_INGRESS_NAME = "docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md"
CLOSEOUT_WRITEBACK_INGRESS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0045-closeout-writeback-ingress-boundary.md"
)
CLOSEOUT_WRITEBACK_INGRESS_REQUIRED_TOKENS = (
    "traceable proof ingress",
    "owner-local re-read anchor",
    "bundle remains the source surface",
    "workflow meaning routes to `aoa-skills`",
    "neighboring proof context",
    "bundle truth stays",
    "new-bundle authority deferred",
)
CLOSEOUT_WRITEBACK_INGRESS_FORBIDDEN_ROUTE_SCAFFOLD = (
    "instead of leaving it as closeout residue or chat memory",
    "rather than as a second source of truth",
    "should not absorb this proof lane",
    "not a rewording of the already-landed recall",
    "not a shadow copy",
    "still does not name a new bundle",
)
CLOSEOUT_WRITEBACK_INGRESS_DECISION_REQUIRED_TOKENS = (
    "Closeout Writeback Ingress Boundary",
    "owner-local ingress anchor",
    "root ingress",
    "reviewed-candidate adoption",
    "Current Applicability",
    "Review Log",
    "owner-local re-read anchor",
    "traceable proof ingress",
)

CONTRIBUTING_ROUTE_REQUIRED_TOKENS = (
    "Operating Card",
    "public contribution route",
    "AGENTS.md` owns agent workflow",
    "validation evidence",
    "security handoff",
    "outputs that preserve claim limits",
    "fixtures and scoring expose public setup",
    "Canonical promotion needs evidence",
    "Hidden intuition routes to a written judgment rule",
    "A good eval bundle proves one bounded thing honestly",
)
CONTRIBUTING_FORBIDDEN_ROUTE_SCAFFOLD = (
    "outputs that do not overstate what was learned",
    "fixtures and scoring do not depend on hidden local assumptions",
    "Do not mark an eval `canonical`",
    "what does the eval still fail to prove?",
    "If the answer depends on hidden intuition, the bundle is not ready.",
    "do not open a public issue or PR",
    "A good eval bundle does not try to prove everything.",
)

SCORE_SEMANTICS_GUIDE_NAME = "docs/guides/SCORE_SEMANTICS_GUIDE.md"
SCORE_SEMANTICS_GUIDE_REQUIRED_TOKENS = (
    "Operating Card",
    "score and verdict interpretation guide",
    "explicit interpretation bounds",
    "carry one bounded part of the claim",
    "Requires stable comparison semantics before the result can be read comparatively.",
    "route back to evidence or weaken the score shape",
)
SCORE_SEMANTICS_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "avoid heavy overlap with nearby axes",
    "avoid pretending to be the whole claim",
    "Not valid without stable comparison semantics.",
    "explicit caution notes",
    "If it hides that, weaken it.",
)

EVAL_REVIEW_GUIDE_NAME = "docs/guides/EVAL_REVIEW_GUIDE.md"
EVAL_REVIEW_GUIDE_REQUIRED_TOKENS = (
    "bounded maturity review guide",
    "remaining-gap route",
    "explicit review evidence",
    "The default-use rationale is weak or missing.",
    "smallest concrete remaining gap and the route that closes it",
    "Deferral Routes",
    "score semantics need clearer interpretation bounds",
    "report summaries need weaker claim language",
)
EVAL_REVIEW_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "without a crisp default-use rationale",
    "rather than a broad wish list",
    "before they become theater",
    "Strong reasons to defer",
    "score semantics still too vague",
    "verdict logic still too dependent on hidden reviewer intuition",
)

BLIND_SPOT_DISCLOSURE_GUIDE_NAME = "docs/guides/BLIND_SPOT_DISCLOSURE_GUIDE.md"
BLIND_SPOT_DISCLOSURE_GUIDE_REQUIRED_TOKENS = (
    "blind-spot disclosure guide",
    "Disclosure Posture",
    "Disclosure needs a review gap route",
    "bundle-shaped specificity",
    "false-pass paths need exposure",
    "Review defers through these gap routes",
)
BLIND_SPOT_DISCLOSURE_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "Weak disclosure sounds like",
    "the blind spots are generic rather than bundle-shaped",
    "the bundle hides likely false-pass paths",
    "Strong review usually defers when",
)


def _require_tokens(
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    for token in tokens:
        if token not in text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
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


def validate_releasing_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = _require_tokens(
        repo_root,
        RELEASING_GUIDE_NAME,
        RELEASING_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if text:
        for stale_phrase in RELEASING_FORBIDDEN_STATUS_LEDGER_TOKENS:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        RELEASING_GUIDE_NAME,
                        "release guide must route readiness artifacts to live-status owners instead of stale status-ledger negative wording "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_root_readme_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = _require_tokens(
        repo_root,
        "README.md",
        ROOT_README_SURFACE_REQUIRED_TOKENS,
        issues,
    )
    if text:
        for token in ROOT_README_SURFACE_FORBIDDEN_TOKENS:
            if token in text:
                issues.append(
                    ValidationIssue(
                        "README.md",
                        "root README Proof Check should stay compact; detailed proof-guide catalogs route to docs/README.md",
                    )
                )
    _require_tokens(
        repo_root,
        "docs/README.md",
        (
            "aoa-evals Bounded Proof Canon",
            "Eval Bundle Selection Chooser",
            "Eval Bundle Index",
        ),
        issues,
    )

    return issues


def validate_eval_philosophy_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = _require_tokens(
        repo_root,
        "docs/guides/EVAL_PHILOSOPHY.md",
        EVAL_PHILOSOPHY_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if text:
        for stale_phrase in EVAL_PHILOSOPHY_FORBIDDEN_FLAT_NEGATIVE_TOKENS:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        "docs/guides/EVAL_PHILOSOPHY.md",
                        "eval philosophy should route proof pressure through positive distinctions instead of flat negative slogan wording "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_docs_readme_route_map(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = _require_tokens(
        repo_root,
        "docs/README.md",
        DOCS_README_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if not text:
        return issues

    for token in DOCS_README_ROUTE_MAP_FORBIDDEN_TOKENS:
        if token in text:
            issues.append(
                ValidationIssue(
                    "docs/README.md",
                    f"docs route map must use role labels and keep validation route out of reader paths; found '{token}'",
                )
            )
    if markdown_python_commands(text):
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs route map must route executable validation commands to docs/AGENTS.md instead of carrying command blocks",
            )
        )

    recommended_pos = text.find("## Recommended Reading Paths")
    validation_pos = text.find("## Validation Route")
    if validation_pos != -1 and recommended_pos != -1 and validation_pos < recommended_pos:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "Validation Route must stay after Recommended Reading Paths so reader paths remain contiguous",
            )
        )

    return issues


def validate_portable_eval_boundary_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = _require_tokens(
        repo_root,
        PORTABLE_EVAL_BOUNDARY_GUIDE_NAME,
        PORTABLE_EVAL_BOUNDARY_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        for stale_phrase in PORTABLE_EVAL_BOUNDARY_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in guide_text:
                issues.append(
                    ValidationIssue(
                        PORTABLE_EVAL_BOUNDARY_GUIDE_NAME,
                        "portable eval boundary guide should route portability "
                        f"through positive review criteria instead of stale scaffold '{stale_phrase}'",
                    )
                )
    return issues


def validate_closeout_writeback_ingress_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    ingress_text = _require_tokens(
        repo_root,
        CLOSEOUT_WRITEBACK_INGRESS_NAME,
        CLOSEOUT_WRITEBACK_INGRESS_REQUIRED_TOKENS,
        issues,
    )
    if ingress_text:
        for stale_phrase in CLOSEOUT_WRITEBACK_INGRESS_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in ingress_text:
                issues.append(
                    ValidationIssue(
                        CLOSEOUT_WRITEBACK_INGRESS_NAME,
                        "closeout writeback ingress should name the active "
                        f"re-read route instead of stale scaffold '{stale_phrase}'",
                    )
                )
    _require_tokens(
        repo_root,
        CLOSEOUT_WRITEBACK_INGRESS_DECISION_NAME,
        CLOSEOUT_WRITEBACK_INGRESS_DECISION_REQUIRED_TOKENS,
        issues,
    )
    return issues


def validate_contributing_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    contributing_text = _require_tokens(
        repo_root,
        "CONTRIBUTING.md",
        CONTRIBUTING_ROUTE_REQUIRED_TOKENS,
        issues,
    )
    if contributing_text:
        for stale_phrase in CONTRIBUTING_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in contributing_text:
                issues.append(
                    ValidationIssue(
                        "CONTRIBUTING.md",
                        "contributing guide should name owner routes and proof criteria "
                        f"instead of stale scaffold '{stale_phrase}'",
                    )
                )
    return issues


def validate_score_semantics_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = _require_tokens(
        repo_root,
        SCORE_SEMANTICS_GUIDE_NAME,
        SCORE_SEMANTICS_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        for stale_phrase in SCORE_SEMANTICS_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in guide_text:
                issues.append(
                    ValidationIssue(
                        SCORE_SEMANTICS_GUIDE_NAME,
                        "score semantics guide should name interpretation route "
                        f"criteria instead of stale scaffold '{stale_phrase}'",
                    )
                )
    return issues


def validate_eval_review_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = _require_tokens(
        repo_root,
        EVAL_REVIEW_GUIDE_NAME,
        EVAL_REVIEW_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        for stale_phrase in EVAL_REVIEW_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in guide_text:
                issues.append(
                    ValidationIssue(
                        EVAL_REVIEW_GUIDE_NAME,
                        "eval review guide should name maturity gap routes "
                        f"instead of stale scaffold '{stale_phrase}'",
                    )
                )
    return issues


def validate_blind_spot_disclosure_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = _require_tokens(
        repo_root,
        BLIND_SPOT_DISCLOSURE_GUIDE_NAME,
        BLIND_SPOT_DISCLOSURE_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        for stale_phrase in BLIND_SPOT_DISCLOSURE_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in guide_text:
                issues.append(
                    ValidationIssue(
                        BLIND_SPOT_DISCLOSURE_GUIDE_NAME,
                        "blind-spot disclosure guide should name disclosure "
                        f"gap routes instead of stale scaffold '{stale_phrase}'",
                    )
                )
    return issues
