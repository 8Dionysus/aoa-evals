"""Root authority, proof-topology, legacy, and agent-route contracts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators import docs_decisions
from validators import mechanics as mechanics_validator
from validators import root_route_cards as root_route_cards_validator
from validators.common import ValidationIssue, read_text_or_issue


EVAL_INDEX_NAME = "EVAL_INDEX.md"
ROADMAP_NAME = "ROADMAP.md"
DESIGN_NAME = "DESIGN.md"
DESIGN_AGENTS_NAME = "DESIGN.AGENTS.md"
GITHUB_AGENTS_NAME = ".github/AGENTS.md"
AGENTS_DISTRICT_NAME = ".agents/AGENTS.md"
SPARK_LANE_AGENTS_NAME = ".agents/spark/AGENTS.md"
SPARK_LANE_SWARM_NAME = ".agents/spark/SWARM.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
AGENT_INDEX_NAME = "docs/architecture/AGENT_INDEX.md"
AGENT_INDEX_CHAIN_DECISION_NAME = "docs/decisions/AOA-EV-D-0103-agent-index-chain-surface.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0091-legacy-naming-single-bridge-language.md"
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language"
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0096-legacy-naming-posture-guide.md"
)
LEGACY_NAMING_POSTURE_GUIDE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_posture_guide"
)
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
MECHANICS_README_NAME = "mechanics/README.md"

ROOT_DESIGN_REQUIRED_TOKENS = (
    "bounded proof organ",
    "proof object",
    "generated surface helps navigation",
    "runtime candidates",
    "bundle-local review turns candidate help",
    "proof meaning comes from source refs, owner routes, generated parity",
    "Local owner truth stays authoritative",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "docs/architecture/ARCHITECTURE.md",
    "docs/guides/EVAL_PHILOSOPHY.md",
    "docs/decisions/",
)
ARCHITECTURE_PROOF_MODEL_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0093-architecture-proof-model-contract.md"
)
ARCHITECTURE_PROOF_MODEL_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k architecture_proof_model"
)
ARCHITECTURE_REQUIRED_TOKENS = (
    "technical proof model",
    "Use this file for the proof model",
    "DESIGN.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "### Mechanics",
    "proof-layer operation",
    "### Layer 5: proof operation support",
    "AoA-aligned mechanics",
    "Evals-native mechanics",
    "owner-named evals-native",
    "Artifact forms",
    "PROVENANCE.md",
    "single controlled bridge",
    "regression visibility with bounded comparison semantics",
    "growth tracking with explicit claim limits",
)
ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS = (
    "It is not the system design thesis",
    "but they are not themselves eval bundles",
    "but they are not themselves proof surfaces",
)
ARCHITECTURE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "regression visibility without metric theater",
    "growth tracking without inflated claims",
)
ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS = (
    "Architecture Proof Model Contract",
    "technical proof model",
    "DESIGN.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "mechanics as operation support",
    "owner-named evals-native",
    "legacy bridge layering",
    "bounded comparison semantics",
    "explicit claim limits",
    ARCHITECTURE_PROOF_MODEL_COMMAND,
)
DESIGN_AGENTS_REQUIRED_TOKENS = (
    "agent-facing guidance",
    "nearest card",
    "bundle-local review",
    "source proof object",
    "generated companions",
    "Quest source records carry return routes",
    "Proof-meaning checks need source refs, owner routes, generated parity",
    "Active mechanic packages",
    "Before changing package boundaries",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "active mechanics, and file-movement boundaries",
    "Maintained agent lanes",
    ".agents/spark/",
    "closeout",
)
ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING = ("mechanic-ready",)
ROOT_DESIGN_FORBIDDEN_ROUTE_SCAFFOLD = (
    "without requiring a full local AoA deployment",
    "They do not become proof acceptance without",
    "A polished single run is not enough",
    "it is not ready to make a strong claim",
    "Green file presence alone is not proof",
    "This file does not override local owner truth",
    "without a compatibility decision",
)
DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "Future mechanic packages",
    "Before package growth",
    "before mechanics or file movement",
)
DESIGN_AGENTS_FORBIDDEN_ROUTE_SCAFFOLD = (
    "they do not replace the\nsource surface",
    "not eval\nbundles and not roadmap direction",
    "Presence-only checks are not enough for proof meaning",
    "but they do not own proof meaning",
    "Negative boundaries stay narrow",
    "not a home base",
)
ROOT_AGENTS_DESIGN_REQUIRED_TOKENS = (
    "DESIGN.md",
    "DESIGN.AGENTS.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "docs/decisions/",
)
GITHUB_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "GitHub platform route",
    "root `AGENTS.md` owns branch/PR/CI/merge",
    "Repo Validation",
    "## Boundary Routes",
    "CI-green pressure",
    "public-safe and deterministic",
)
GITHUB_AGENTS_STALE_ROUTE_PHRASES = (
    "Do not encode sibling-repo doctrine",
    "Do not add secrets",
    "Do not make CI green",
)
DECISION_SURFACE_REQUIRED_TOKENS = (
    "bounded proof",
    "source surface",
    "generated",
    "runtime",
    "sibling",
)
DECISION_TEMPLATE_REQUIRED_TOKENS = (
    "## Context",
    "## Options Considered",
    "## Decision",
    "## Consequences",
    "## Current Applicability",
    "## Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "## Validation",
)
AGENTS_DISTRICT_REQUIRED_TOKENS = (
    ".agents/<lane>/",
    ".agents/skills/",
    ".agents/spark/",
    "Proof authority stays",
    "python scripts/validate_repo.py",
    "python scripts/validate_nested_agents.py",
)
SPARK_LANE_AGENTS_REQUIRED_TOKENS = (
    ".agents/spark/",
    "fast-loop lane",
    "one bounded claim",
    "Bundle-local `EVAL.md`",
    "eval.yaml",
    "generated/AGENTS.md",
    "python scripts/validate_nested_agents.py",
)
SPARK_LANE_SWARM_REQUIRED_TOKENS = (
    ".agents/spark/SWARM.md",
    "one bounded eval bundle",
    "Boundary Keeper",
    "repo validation",
    "build catalog",
    ".agents/spark/AGENTS.md#validation",
)
SPARK_LANE_DECISION_REQUIRED_TOKENS = (
    "Spark/",
    ".agents/spark/",
    ".agents/AGENTS.md",
    "does not let Spark",
    "does not make `.agents/` a doctrine center",
    "`Spark/` is absent",
)
PROOF_TOPOLOGY_REQUIRED_TOKENS = (
    "Convex topology",
    "source proof objects",
    "derived readers",
    "candidate evidence",
    "Memory evidence context",
    "receipts",
    "quest obligations",
    "decisions",
    "legacy lineage",
    "mechanic operations",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "Root Technical Districts",
    "after mechanics movement",
    "additional root path becomes",
    "part-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/`",
    "generated surfaces are companions",
    "candidate packets enter bundle-local review before verdict meaning",
    "quest records carry obligation return routes",
    "source truth stays with the source surface; decisions preserve route rationale",
    "source proof surfaces keep verdict meaning; guidance owns edit route and validation",
    "proof canon stays with source proof objects",
    "verdict meaning stays with reviewed reports and source bundles",
    "at least one living non-mechanics evidence route in addition to validator and rationale refs",
    "active topology starts at the current owner route",
    "A new `mechanics/` parent",
    "No remaining named candidate family is promoted by symmetry",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0106-memory-consumer-proof-boundary.md"
)
MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS = (
    "`aoa-evals`",
    "reviewed `aoa-memo` object ids and provenance",
    "can cite reviewed recall as bounded context",
    "proof authority stays with",
    "eval bundle or owning mechanic",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS = (
    "Reviewed memory routes recall into proof review.",
    "`aoa-evals` can cite reviewed `aoa-memo` object ids, provenance, lifecycle, and",
    "generated read models as bounded recall context",
    "Proof authority stays",
    "selected evidence, scoring or verdict logic",
    "`aoa-evals` keeps route_only memory posture until a local memo port exists.",
    "Session evidence routes through `.aoa` or source proof artifacts before any",
    "later `aoa-memo` reviewed intake.",
    "Durable memory, local memo candidates, and export packets route through reviewed",
    "owner surfaces with visible provenance",
    "`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs are",
    "access-plane evidence for inspection and review",
    "Owner surfaces keep proof authority and durable write authority.",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS = (
    "Memory evidence context",
    "reviewed `aoa-memo` object ids, provenance, lifecycle, generated memory read models",
    "`aoa_memo` MCP access-plane dry-runs",
    "reviewed memory provides recall context; local proof authority stays with the eval bundle or owning mechanic",
    "`aoa-evals` stays route_only until a local memo port exists",
    "MCP output remains inspection evidence",
    "durable memory lands only in `aoa-memo`",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Memory Consumer Proof Boundary",
    "route_only memory posture",
    "object ids, provenance, lifecycle, and generated read models",
    "Memory is not proof.",
    "does not create a local memo port",
    "Durable memory lands only in `aoa-memo`.",
    "`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs",
    "access-plane evidence only",
    "direct durable",
    "write authority",
    "python scripts/validate_repo.py",
    "python scripts/validate_semantic_agents.py",
)
PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready operations",
    "while Phase 4 maps the topology",
    "before mechanics growth starts from a root path",
    "A future `mechanics/` package",
    "It is not the roadmap",
    "The goal is not a decorative tree",
)
PROOF_TOPOLOGY_FORBIDDEN_ROUTE_SCAFFOLD = (
    "quests are obligations, not eval bundles",
    "package movement is not planned",
    "no active root examples payload should live here",
    "no active root reports payload should live here",
    "no active root config payload",
    "not proof canon",
    "without owning proof meaning",
    "not a verdict source",
    "a generic root validator file and a rationale-only decision ref are not enough",
    "without stealing their authority",
    "do not move the file yet",
    "are not historical memory",
    "should\nnot point",
    "should not look like",
    "no sibling authority transfer",
    "no empty package taxonomy",
)
PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready operations",
    "Keep physical movement deferred",
    "This decision does not create `mechanics/`.",
)
ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING = (
    "mechanic-ready artifact classes",
    "mechanics and legacy topology decision before any package creation or move",
    "runtime-evidence intake decision",
    "future mechanic packages",
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0100-active-mechanics-topology-wording.md"
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k "
    "'root_design or design_agents or proof_topology'"
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS = (
    "Active Mechanics Topology Wording",
    "active mechanics",
    "stale preparatory wording",
    "PROVENANCE.md",
    "archive details",
    ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND,
)
PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS = (
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics",
    "source proof objects",
    "candidate evidence",
    "legacy lineage",
    "mechanic operations",
    "active `mechanics/` atlas",
)
LEGACY_NAMING_REQUIRED_TOKENS = (
    "Legacy Naming Posture",
    "posture guide",
    "archive details",
    "active",
    "historical",
    "accepted-input",
    "generated-projection",
    "candidate-only",
    "provenance-bridge",
    "active-first route",
    "PROVENANCE.md",
    "single controlled bridge",
    "active mechanic surfaces",
    "Active Owner Lookup",
    "Route Rules",
)
LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS = (
    "It is not an archive map",
    "Do not put legacy archive details in this file",
    "## Current Active Owners",
    "Wrong parent forms such as",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "The old `Spark/` root path",
)
LEGACY_NAMING_DECISION_REQUIRED_TOKENS = (
    "docs/architecture/LEGACY_NAMING.md",
    "posture guide",
    "accepted-input",
    "active topology",
    "generated projections",
    "archive details",
    "not authorize starting new work from legacy directories",
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Posture Guide",
    "docs/architecture/LEGACY_NAMING.md",
    "posture guide",
    "not a global archive map",
    "archive details",
    "PROVENANCE.md",
    LEGACY_NAMING_POSTURE_GUIDE_COMMAND,
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Single-Bridge Language",
    "docs/architecture/LEGACY_NAMING.md",
    "`PROVENANCE.md`",
    "single controlled bridge",
    "archive details",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
)
LEGACY_NAMING_SECOND_ACTIVE_BRIDGE_RE = re.compile(
    r"(?:enter|enters|mapped)\s+through\s+`mechanics/[^`]+/PROVENANCE\.md`"
    r"\s+and\s+`mechanics/[^`]+/legacy/INDEX\.md`"
    r"|Use package\s+`PROVENANCE\.md`,\s+`legacy/INDEX\.md`",
    re.MULTILINE,
)
LEGACY_NAMING_DIRECT_MECHANIC_LEGACY_INDEX_RE = re.compile(
    r"`mechanics/[a-z0-9-]+/legacy/INDEX\.md`"
)
LEGACY_EXTERNAL_ARCHIVE_DETAIL_RE = re.compile(
    r"(?:mechanics/[a-z0-9-]+/)?legacy/(?:INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
LEGACY_EXTERNAL_ARCHIVE_DETAIL_SURFACE_NAMES = (
    DESIGN_NAME,
    DESIGN_AGENTS_NAME,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    ROADMAP_NAME,
    "CHANGELOG.md",
)
LEGACY_EXTERNAL_ROUTE_MANAGEMENT_FORBIDDEN_WORDING = (
    "validator-backed retirement",
    "before physical movement, deletion, or retirement",
    "move any package-local legacy surface",
    "retirement or containment posture",
    "retired root",
    "aliases retired",
    "retire-after table",
)
LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_FORBIDDEN_WORDING = (
    "Inside the archive, every raw payload",
    "raw payload accounting now requires",
    "raw payload accounting now rejects",
    "raw-only archive route",
)
LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_SURFACE_NAMES = (
    DESIGN_NAME,
    DESIGN_AGENTS_NAME,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    ROADMAP_NAME,
    "CHANGELOG.md",
)
LEGACY_EXTERNAL_ROUTE_MANAGEMENT_SURFACE_NAMES = (
    LEGACY_NAMING_NAME,
    ROADMAP_NAME,
    DESIGN_AGENTS_NAME,
    "docs/decisions/AOA-EV-D-0009-legacy-naming-containment.md",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
    LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
)
LEGACY_SINGLE_BRIDGE_RESIDUE_RE = re.compile(
    r"(?:enter|enters|entered|lookup starts from the active route and then enters)\s+"
    r"`PROVENANCE\.md`,\s+`legacy/INDEX\.md`"
    r"|`PROVENANCE\.md`\s+and\s+`legacy/INDEX\.md`"
    r"|`mechanics/[a-z0-9-]+/PROVENANCE\.md`\s+and\s+`mechanics/[a-z0-9-]+/legacy/INDEX\.md`"
    r"|entered through\s+`PROVENANCE\.md`\s+and\s+then\s+through\s+`legacy/INDEX\.md`",
    re.MULTILINE,
)
LEGACY_SINGLE_BRIDGE_RESIDUE_SURFACES = (
    DESIGN_NAME,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    ROADMAP_NAME,
    "CHANGELOG.md",
    "schemas/README.md",
    "schemas/AGENTS.md",
    "manifests/README.md",
    "manifests/AGENTS.md",
    "config/README.md",
    "config/AGENTS.md",
    "examples/README.md",
    "examples/AGENTS.md",
    "fixtures/README.md",
    "fixtures/AGENTS.md",
    "reports/README.md",
    "reports/AGENTS.md",
    "runners/README.md",
    "runners/AGENTS.md",
    "scorers/README.md",
    "scorers/AGENTS.md",
    "templates/README.md",
    "templates/AGENTS.md",
    "docs/decisions/AOA-EV-D-0071-mechanic-legacy-skeleton-contract.md",
    "docs/decisions/AOA-EV-D-0075-mechanic-provenance-entry-contract.md",
    "docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md",
    "docs/decisions/AOA-EV-D-0089-mechanic-legacy-single-bridge.md",
    "docs/decisions/AOA-EV-D-0090-mechanic-provenance-bridge-posture.md",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
)
DECISION_STATUS_DETAIL_MARKERS = (";", "superseded by")
AGENT_INDEX_REQUIRED_TOKENS = (
    "pass-through index for agents",
    "path needs an explicit owner route",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "nearest `AGENTS.md`",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/README.md",
    "docs/decisions/README.md",
    "route-card-only",
    "compatibility districts",
    "mechanics/<parent>/parts/<part>/VALIDATION.md",
    "mechanics/<parent>/parts/AGENTS.md",
    "Executable validation commands belong in the nearest `AGENTS.md`",
)
AGENT_INDEX_FORBIDDEN_ROUTE_SCAFFOLD = (
    "path name is not enough",
    "An agent should expect only",
    "should it be part-local",
)
AGENT_INDEX_DECISION_REQUIRED_TOKENS = (
    "Agent Index Chain Surface",
    "docs/architecture/AGENT_INDEX.md",
    "docs/README.md",
    "active mechanic parent",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "route-card-only root districts",
    "Executable validation commands remain in the nearest `AGENTS.md`",
)
READ_MODEL_COMMAND_OWNER_PATHS = (
    ".github/pull_request_template.md",
    "CONTRIBUTING.md",
    "EVAL_SELECTION.md",
    "README.md",
    "ROADMAP.md",
    "AUDIT.md",
    "docs/README.md",
    "docs/architecture/AGENT_INDEX.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "docs/architecture/LEGACY_NAMING.md",
    "docs/operations/RELEASING.md",
    "docs/guides/REGRESSION_PROOF_SURFACES.md",
    "evals/README.md",
    "generated/README.md",
    "quests/README.md",
    "quests/LIFECYCLE.md",
    "mechanics/README.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
)
AUDIT_SURFACE_ROLE_REQUIRED_TOKENS = (
    "Audit Surface Map",
    "AGENTS.md#audit-and-review-route",
    "owns route law",
    "AGENTS.md#verify",
    "Route cards own the commands",
    "Route outward for:",
    "reusable technique truth: `aoa-techniques`",
    "execution workflow meaning: `aoa-skills`",
    "artifact-contract meaning",
    "sanitized evidence route",
)
AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS = (
    "## Audit and review route",
    "`AUDIT.md` is the audit surface map",
    "approval gates",
    "Claim pressure routes",
    "generated reader, chooser doc, or index outranking source proof",
    "private dataset, secret-bearing fixture, hidden telemetry, or skipped validation",
    "Review severity",
    "P0",
    "P1",
    "report shape",
)
ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES = (
    "Hard boundaries:",
    "bounded evals must not become total intelligence scores",
    "generated readers, chooser docs, and indexes must not outrank",
    "validation\n  that was not run must not be presented as public proof",
    "Do not use decisions as release notes",
)
INDEX_SURFACE_ROLE_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    EVAL_INDEX_NAME: (
        "# Eval Bundle Index",
        "repository-wide agent-facing index of public eval bundles",
        "bundle-local",
    ),
    "docs/decisions/README.md": (
        "# Decision Records Index",
        "agent-facing index",
        "decision rationale",
        "docs/decisions/AGENTS.md#validation",
    ),
    MECHANICS_README_NAME: (
        "# Mechanics Operation Atlas",
        "operation atlas",
        "Top-down route",
    ),
}
VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS = (
    "## Applies to",
    "## Role",
    "root contract mesh",
    "authority class",
    "Part-local validators",
    "bounded proof posture",
    "precise failures",
    "tests/test_validate_repo.py",
)
VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS = (
    "## Applies to",
    "## Role",
    "root validator regression mesh",
    "scripts/validate_repo.py",
    "repository-wide invariant",
    "mechanic-owned tests",
    "incidental prose",
    "Expected-output pressure",
    "public-safe",
)
VALIDATOR_AGENT_SURFACE_STALE_ROUTE_PHRASES = (
    "## Guidance for `scripts/`",
    "## Guidance for `tests/`",
    "Validator changes must not weaken bounded proof posture",
    "Do not move a part-local test back",
    "Do not update expected outputs",
)
ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS = (
    LEGACY_NAMING_NAME,
    "Legacy naming",
    "active names",
    "legacy bridge posture",
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


def validate_decision_status_lines(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    decisions_root = repo_root / "docs" / "decisions"
    if not decisions_root.exists():
        return issues

    for decision_path in sorted(decisions_root.glob("AOA-EV-D-[0-9][0-9][0-9][0-9]-*.md")):
        relative_path = decision_path.relative_to(repo_root).as_posix()
        try:
            lines = decision_path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            issues.append(ValidationIssue(relative_path, f"failed to read decision: {exc}"))
            continue
        for line_number, line in enumerate(lines, start=1):
            if not line.startswith("- Status:"):
                continue
            status = line.removeprefix("- Status:").strip()
            normalized_status = status.lower()
            if any(marker in normalized_status for marker in DECISION_STATUS_DETAIL_MARKERS):
                issues.append(
                    ValidationIssue(
                        f"{relative_path}:{line_number}",
                        "decision status should stay atomic; put applicability or supersession detail in dated Current Applicability and Review Log",
                    )
                )
            break
    return issues


def validate_agent_index_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    _require_tokens(repo_root, AGENT_INDEX_NAME, AGENT_INDEX_REQUIRED_TOKENS, issues)
    index_text = read_text_or_issue(repo_root / AGENT_INDEX_NAME, issues, root=repo_root)
    if index_text:
        for stale_phrase in AGENT_INDEX_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in index_text:
                issues.append(
                    ValidationIssue(
                        AGENT_INDEX_NAME,
                        "agent index should name explicit owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    _require_tokens(repo_root, AGENT_INDEX_CHAIN_DECISION_NAME, AGENT_INDEX_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, "README.md", (AGENT_INDEX_NAME, "repo to authority class"), issues)
    _require_tokens(repo_root, "docs/README.md", ("AGENT_INDEX.md", "Agent Index", "Mechanics Refactor Path"), issues)
    _require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (AGENT_INDEX_NAME, "pass-through reader"), issues)
    _require_tokens(repo_root, ROADMAP_NAME, (AGENT_INDEX_NAME, "Agent index chain"), issues)
    _require_tokens(repo_root, MECHANICS_EVIDENCE_CLUSTERS_NAME, (AGENT_INDEX_NAME, "agent-facing pass-through index"), issues)
    _require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (AGENT_INDEX_CHAIN_DECISION_NAME, "Agent Index Chain Surface"),
        issues,
    )

    return issues


def validate_read_model_command_ownership(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in READ_MODEL_COMMAND_OWNER_PATHS:
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if not text:
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "guidance surface must route executable validation commands to the nearest AGENTS.md instead of carrying python command lines",
                )
            )

    return issues


def validate_memory_consumer_proof_boundary_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    _require_tokens(repo_root, "README.md", MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS, issues)
    _require_tokens(repo_root, "docs/guides/EVAL_PHILOSOPHY.md", MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS, issues)
    _require_tokens(repo_root, PROOF_TOPOLOGY_NAME, MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS, issues)
    _require_tokens(repo_root, MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME, MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME, "Memory Consumer Proof Boundary"),
        issues,
    )

    return issues


def validate_audit_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    _require_tokens(repo_root, "AUDIT.md", AUDIT_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    agents_text = _require_tokens(repo_root, "AGENTS.md", AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS, issues)
    if agents_text:
        for stale_phrase in ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES:
            if stale_phrase in agents_text:
                issues.append(
                    ValidationIssue(
                        "AGENTS.md",
                        "root audit route should expose claim pressure routes "
                        "instead of stale negative boundary scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_github_agent_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = _require_tokens(repo_root, GITHUB_AGENTS_NAME, GITHUB_AGENTS_REQUIRED_TOKENS, issues)
    if text:
        for stale_phrase in GITHUB_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        GITHUB_AGENTS_NAME,
                        ".github route card should use an operating card and boundary route table "
                        "instead of stale negative platform scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_index_surface_roles(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name, tokens in INDEX_SURFACE_ROLE_REQUIRED_TOKENS.items():
        _require_tokens(repo_root, path_name, tokens, issues)

    return issues


def validate_validator_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    scripts_text = _require_tokens(repo_root, "scripts/AGENTS.md", VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    tests_text = _require_tokens(repo_root, "tests/AGENTS.md", VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    for path_name, text in (
        ("scripts/AGENTS.md", scripts_text),
        ("tests/AGENTS.md", tests_text),
    ):
        if not text:
            continue
        for stale_phrase in VALIDATOR_AGENT_SURFACE_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "validator AGENTS cards should route pressure through owner maps "
                        "instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_root_design_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    design_text = _require_tokens(repo_root, DESIGN_NAME, ROOT_DESIGN_REQUIRED_TOKENS, issues)
    architecture_text = _require_tokens(repo_root, "docs/architecture/ARCHITECTURE.md", ARCHITECTURE_REQUIRED_TOKENS, issues)
    design_agents_text = _require_tokens(repo_root, DESIGN_AGENTS_NAME, DESIGN_AGENTS_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, "AGENTS.md", ROOT_AGENTS_DESIGN_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, DECISION_RECORDS_README_NAME, DECISION_SURFACE_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, "docs/decisions/TEMPLATE.md", DECISION_TEMPLATE_REQUIRED_TOKENS, issues)
    _require_tokens(
        repo_root,
        "docs/decisions/AGENTS.md",
        (
            "source surface",
            "validate_repo.py",
            "sibling",
            "Amendment Route",
            "Review Log",
            "Current Applicability",
            "Previous assumption",
            "New reality",
            "Status",
            "Superseded by",
            "strikethrough",
            "active route",
            "owner surface",
            "validation evidence",
        ),
        issues,
    )
    _require_tokens(repo_root, ARCHITECTURE_PROOF_MODEL_DECISION_NAME, ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME, ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (
            ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            "Architecture Proof Model Contract",
            ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
            "Active Mechanics Topology Wording",
        ),
        issues,
    )
    if design_text:
        for stale_phrase in ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in design_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_NAME,
                        f"root design must describe active mechanic authority, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in ROOT_DESIGN_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in design_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_NAME,
                        "root design should route proof pressure through positive owner "
                        f"language instead of stale scaffold '{stale_phrase}'",
                    )
                )
    if architecture_text:
        for stale_phrase in ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS:
            if stale_phrase in architecture_text:
                issues.append(
                    ValidationIssue(
                        "docs/architecture/ARCHITECTURE.md",
                        "architecture should route related surfaces positively instead of stale negative role scaffold "
                        f"'{stale_phrase}'",
                    )
                )
        for stale_phrase in ARCHITECTURE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in architecture_text:
                issues.append(
                    ValidationIssue(
                        "docs/architecture/ARCHITECTURE.md",
                        "architecture long-term direction should name the proof route "
                        f"instead of stale scaffold '{stale_phrase}'",
                    )
                )
    if design_agents_text:
        for stale_phrase in DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in design_agents_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_AGENTS_NAME,
                        f"agent design must describe active mechanic packages, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in DESIGN_AGENTS_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in design_agents_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_AGENTS_NAME,
                        "agent design should name owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    return issues


def validate_agent_lane_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(repo_root, AGENTS_DISTRICT_NAME, AGENTS_DISTRICT_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, SPARK_LANE_AGENTS_NAME, SPARK_LANE_AGENTS_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, SPARK_LANE_SWARM_NAME, SPARK_LANE_SWARM_REQUIRED_TOKENS, issues)
    swarm_text = read_text_or_issue(repo_root / SPARK_LANE_SWARM_NAME, issues, root=repo_root)
    if swarm_text and markdown_python_commands(swarm_text):
        issues.append(
            ValidationIssue(
                SPARK_LANE_SWARM_NAME,
                "Spark SWARM context must route executable commands to .agents/spark/AGENTS.md instead of carrying python command lines",
            )
        )
    _require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0017-spark-agent-lane-placement.md",
        SPARK_LANE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require_tokens(repo_root, "README.md", (AGENTS_DISTRICT_NAME, SPARK_LANE_AGENTS_NAME), issues)
    _require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (".agents/", ".agents/spark/", "Agent guidance"), issues)
    if (repo_root / "Spark").exists():
        issues.append(ValidationIssue("Spark/", "root-local Spark lane must stay moved to .agents/spark/"))
    return issues


def validate_proof_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    topology_text = _require_tokens(repo_root, PROOF_TOPOLOGY_NAME, PROOF_TOPOLOGY_REQUIRED_TOKENS, issues)
    decision_text = _require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS,
        issues,
    )
    roadmap_text = _require_tokens(repo_root, ROADMAP_NAME, (PROOF_TOPOLOGY_NAME, "Proof Topology Map"), issues)
    if topology_text:
        for stale_phrase in PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in topology_text:
                issues.append(
                    ValidationIssue(
                        PROOF_TOPOLOGY_NAME,
                        f"proof topology must describe active mechanics, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in PROOF_TOPOLOGY_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in topology_text:
                issues.append(
                    ValidationIssue(
                        PROOF_TOPOLOGY_NAME,
                        "proof topology should name owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    if decision_text:
        for stale_phrase in PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in decision_text:
                issues.append(
                    ValidationIssue(
                        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
                        f"proof topology decision must describe the active mechanics atlas, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    if roadmap_text:
        for stale_phrase in ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING:
            if stale_phrase in roadmap_text:
                issues.append(
                    ValidationIssue(
                        ROADMAP_NAME,
                        f"roadmap must describe active mechanics direction, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    return issues


def validate_legacy_naming_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(repo_root, LEGACY_NAMING_NAME, LEGACY_NAMING_REQUIRED_TOKENS, issues)
    text = read_text_or_issue(repo_root / LEGACY_NAMING_NAME, issues, root=repo_root)
    if text:
        for forbidden_token in LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        LEGACY_NAMING_NAME,
                        "legacy naming posture guide must not carry concrete legacy-name inventories or wrong-parent maps; use active topology surfaces or owning legacy archives",
                    )
                )
        for match in LEGACY_NAMING_SECOND_ACTIVE_BRIDGE_RE.finditer(text):
            issues.append(
                ValidationIssue(
                    LEGACY_NAMING_NAME,
                    "legacy naming map must keep `PROVENANCE.md` as the single controlled bridge from active mechanic surfaces; `legacy/INDEX.md` may appear only as archive-internal detail after that bridge",
                )
            )
        for match in LEGACY_NAMING_DIRECT_MECHANIC_LEGACY_INDEX_RE.finditer(text):
            issues.append(
                ValidationIssue(
                    LEGACY_NAMING_NAME,
                    "legacy naming posture guide must not carry direct mechanic legacy index paths; route to the active mechanic and package PROVENANCE.md",
                )
            )
    for path_name in LEGACY_SINGLE_BRIDGE_RESIDUE_SURFACES:
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        if LEGACY_SINGLE_BRIDGE_RESIDUE_RE.search(surface_text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy route wording must cross only through PROVENANCE.md; archive index, distillation log, and raw lineage are archive-internal after that bridge",
                )
            )
    archive_detail_surface_paths: set[str] = set(LEGACY_EXTERNAL_ARCHIVE_DETAIL_SURFACE_NAMES)
    decisions_root = repo_root / "docs" / "decisions"
    if decisions_root.is_dir():
        archive_detail_surface_paths.update(
            path.relative_to(repo_root).as_posix()
            for path in sorted(decisions_root.glob("*.md"))
        )
    for path_name in sorted(archive_detail_surface_paths):
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for match in LEGACY_EXTERNAL_ARCHIVE_DETAIL_RE.finditer(surface_text):
            issues.append(
                ValidationIssue(
                    path_name,
                    f"legacy route wording must cross only through PROVENANCE.md; external surfaces must not carry archive-internal detail `{match.group(0)}`",
                )
            )
    for path_name in LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_SURFACE_NAMES:
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for stale_phrase in LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_FORBIDDEN_WORDING:
            if stale_phrase in surface_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"external legacy boundary wording must not carry archive-local accounting detail: '{stale_phrase}'",
                    )
                )
    route_management_surface_paths: set[str] = set(LEGACY_EXTERNAL_ROUTE_MANAGEMENT_SURFACE_NAMES)
    for district_name, allowed_names in root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        for allowed_name in allowed_names:
            route_management_surface_paths.add(f"{district_name}/{allowed_name}")
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue
        for path in sorted(parent_root.rglob("*.md")):
            if "legacy" in path.relative_to(parent_root).parts:
                continue
            route_management_surface_paths.add(path.relative_to(repo_root).as_posix())

    for path_name in sorted(route_management_surface_paths):
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for stale_phrase in LEGACY_EXTERNAL_ROUTE_MANAGEMENT_FORBIDDEN_WORDING:
            if stale_phrase in surface_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"external legacy boundary wording must not present legacy as a movement, deletion, or retirement route: '{stale_phrase}'",
                    )
                )
    _require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0009-legacy-naming-containment.md",
        LEGACY_NAMING_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require_tokens(repo_root, LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME, LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(repo_root, LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME, LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS, issues)
    _require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            "Legacy Naming Single-Bridge Language",
            LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "Legacy Naming Posture Guide",
        ),
        issues,
    )
    _require_tokens(repo_root, "README.md", (LEGACY_NAMING_NAME, "accepted-input"), issues)
    _require_tokens(repo_root, PROOF_TOPOLOGY_NAME, (LEGACY_NAMING_NAME, "generated-projection", "provenance-bridge"), issues)
    _require_tokens(repo_root, ROADMAP_NAME, ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS, issues)
    _require_tokens(
        repo_root,
        "CHANGELOG.md",
        (
            "Legacy Naming Single-Bridge Language",
            "Legacy Naming Posture Guide",
            "single controlled bridge",
        ),
        issues,
    )
    return issues
