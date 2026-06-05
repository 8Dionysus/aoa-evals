"""Eval philosophy, proof-guide, review, and blind-spot route validation."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_guidance_common import reject_tokens, require_tokens

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


def validate_eval_philosophy_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root,
        "docs/guides/EVAL_PHILOSOPHY.md",
        EVAL_PHILOSOPHY_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if text:
        reject_tokens(
            text=text,
            path_name="docs/guides/EVAL_PHILOSOPHY.md",
            tokens=EVAL_PHILOSOPHY_FORBIDDEN_FLAT_NEGATIVE_TOKENS,
            message_template=(
                "eval philosophy should route proof pressure through positive distinctions instead of "
                "flat negative slogan wording '{token}'"
            ),
            issues=issues,
        )

    return issues


def validate_portable_eval_boundary_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = require_tokens(
        repo_root,
        PORTABLE_EVAL_BOUNDARY_GUIDE_NAME,
        PORTABLE_EVAL_BOUNDARY_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        reject_tokens(
            text=guide_text,
            path_name=PORTABLE_EVAL_BOUNDARY_GUIDE_NAME,
            tokens=PORTABLE_EVAL_BOUNDARY_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template=(
                "portable eval boundary guide should route portability through positive review criteria "
                "instead of stale scaffold '{token}'"
            ),
            issues=issues,
        )
    return issues


def validate_score_semantics_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = require_tokens(
        repo_root,
        SCORE_SEMANTICS_GUIDE_NAME,
        SCORE_SEMANTICS_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        reject_tokens(
            text=guide_text,
            path_name=SCORE_SEMANTICS_GUIDE_NAME,
            tokens=SCORE_SEMANTICS_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template="score semantics guide should name interpretation route criteria instead of stale scaffold '{token}'",
            issues=issues,
        )
    return issues


def validate_eval_review_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = require_tokens(
        repo_root,
        EVAL_REVIEW_GUIDE_NAME,
        EVAL_REVIEW_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        reject_tokens(
            text=guide_text,
            path_name=EVAL_REVIEW_GUIDE_NAME,
            tokens=EVAL_REVIEW_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template="eval review guide should name maturity gap routes instead of stale scaffold '{token}'",
            issues=issues,
        )
    return issues


def validate_blind_spot_disclosure_guide_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_text = require_tokens(
        repo_root,
        BLIND_SPOT_DISCLOSURE_GUIDE_NAME,
        BLIND_SPOT_DISCLOSURE_GUIDE_REQUIRED_TOKENS,
        issues,
    )
    if guide_text:
        reject_tokens(
            text=guide_text,
            path_name=BLIND_SPOT_DISCLOSURE_GUIDE_NAME,
            tokens=BLIND_SPOT_DISCLOSURE_GUIDE_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template="blind-spot disclosure guide should name disclosure gap routes instead of stale scaffold '{token}'",
            issues=issues,
        )
    return issues
