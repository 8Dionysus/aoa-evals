"""Mechanics-facing root-authored surface contracts."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from validators import docs_decisions
from validators.common import ValidationIssue, read_text_or_issue


ACTIVE_MECHANIC_PARENT_NAMES = (
    "agon",
    "antifragility",
    "audit",
    "boundary-bridge",
    "checkpoint",
    "comparison-spine",
    "distillation",
    "experience",
    "growth-cycle",
    "method-growth",
    "proof-infra",
    "proof-loop",
    "proof-object",
    "publication-receipts",
    "questbook",
    "recurrence",
    "release-support",
    "rpg",
    "titan",
)
AOA_ALIGNED_MECHANIC_PARENT_NAMES = (
    "agon",
    "antifragility",
    "audit",
    "boundary-bridge",
    "checkpoint",
    "distillation",
    "experience",
    "growth-cycle",
    "method-growth",
    "questbook",
    "recurrence",
    "release-support",
    "rpg",
)
EVALS_NATIVE_MECHANIC_PARENT_NAMES = (
    "comparison-spine",
    "proof-infra",
    "proof-loop",
    "proof-object",
    "publication-receipts",
    "titan",
)
FORMER_WRONG_MECHANIC_PARENT_ROUTES = (
    ("agon-proof", "agon"),
    ("titan-canaries", "titan"),
    ("proof-release", "release-support"),
    ("runtime-evidence", "audit"),
    ("sibling-proof-refs", "boundary-bridge"),
    ("repair", "antifragility/repair-proof"),
)

MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
MECHANICS_EVIDENCE_CLUSTERS = Path(MECHANICS_EVIDENCE_CLUSTERS_NAME)
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROADMAP_NAME = "ROADMAP.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
PART_LOCAL_TEST_PLACEMENT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0050-part-local-test-placement.md"
)

MECHANICS_REQUIRED_TOKENS = (
    "operation atlas",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "proof-object",
    "proof-loop",
    "comparison-spine",
    "proof-infra",
    "publication-receipts",
    "release-support",
    "titan",
    "agon",
    "questbook",
    "audit",
    "boundary-bridge",
    "Candidate families",
    "Candidate families stay evidence-only",
    "Current candidate promotion state: empty",
    "recurrence",
    "checkpoint",
    "experience",
    "antifragility",
    "method-growth",
    "rpg",
    "growth-cycle",
    "distillation",
    "Package taxonomy requires source surfaces, inputs, outputs, boundaries",
    "proof-layer operation",
    "Parent Class Summary",
    "AoA-aligned parents",
    "Evals-native parents",
    "owner-named evals-native",
    "Concrete wrong-parent mappings live in",
)
MECHANICS_AGENTS_REQUIRED_TOKENS = (
    "repeatable proof-layer operations",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "source proof objects",
    "generated readers",
    "runtime candidates",
)
MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS = (
    "parent-mechanic evidence gate",
    "Evidence Standard",
    "Root District Reconnaissance Ledger",
    "AoA-aligned parents",
    "Evals-native parents",
    "Class Membership Contract",
    "cross-root evidence",
    "owner-named evals-native",
    "aoa-agents` keeps stronger Titan law",
    "`agon`",
    "`audit`",
    "`boundary-bridge`",
    "`recurrence`",
    "`checkpoint`",
    "`experience`",
    "`antifragility`",
    "`method-growth`",
    "`rpg`",
    "`growth-cycle`",
    "`distillation`",
    "`release-support`",
    "`titan`",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "Legacy Rule",
    "PROVENANCE.md",
    "legacy archive",
    "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane.",
    "Single documents, reports, and canary forms route as parts under the right parent",
)
PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS = (
    "Part-local Test Placement",
    "mechanics/<mechanic>/parts/<part>/tests/",
    "Root `tests/` remains the repository-wide test district",
    "python -m pytest -q",
    "does not create a new parent mechanic from a test name",
)

MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0083-mechanic-evidence-dimension-ledger.md"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_dimension"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS = (
    "Active Parent Evidence Dimension Ledger",
    "Meaning/doctrine",
    "Proof pressure",
    "Contracts/payloads",
    "Builders/readouts",
    "Quest/deferred pressure",
    "Owner split and stop-lines",
    "Legacy/provenance",
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS = (
    "Parent",
    "Class",
    "Meaning/doctrine",
    "Proof pressure",
    "Contracts/payloads",
    "Builders/readouts",
    "Quest/deferred pressure",
    "Owner split and stop-lines",
    "Legacy/provenance",
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS = (
    "Mechanic Evidence Dimension Ledger",
    "Active Parent Evidence Dimension Ledger",
    "meaning/doctrine",
    "proof pressure",
    "contracts/payloads",
    "builders/readouts",
    "quest/deferred pressure",
    "owner split and stop-lines",
    "owner-named evals-native",
    "legacy/provenance",
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
)
MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0101-mechanic-evidence-route-refs.md"
)
MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_route_refs"
)
MECHANIC_EVIDENCE_ROUTE_REFS_SECTION = "Active Parent Evidence Route Refs"
MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS = (
    MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
    "concrete local route refs",
    "repo-relative",
    "non-mechanics route ref",
    "living non-mechanics evidence",
    "rationale-only decision",
    "generic root validator",
)
MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS = (
    "Parent",
    "Route refs",
)
MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT = 3
MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS = frozenset(
    {
        "scripts/validate_repo.py",
        "tests/test_validate_repo.py",
    }
)
MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES = (
    "docs/decisions/",
)
MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS = (
    "Mechanic Evidence Route Refs",
    MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
    "concrete local route refs",
    "repo-relative",
    "non-mechanics route ref",
    "living non-mechanics evidence",
    "rationale-only decision",
    "generic root validator",
    "cross-root evidence",
    MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND,
)

MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0084-mechanic-root-district-reconnaissance.md"
)
MECHANIC_ROOT_DISTRICT_RECON_COMMAND = (
    "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon"
)
MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS = (
    "Root District Reconnaissance Ledger",
    "Current root posture",
    "Mechanics relationship",
    "Validation guard",
    "root-district",
)
MECHANIC_ROOT_DISTRICT_RECON_COLUMNS = (
    "District",
    "Authority class",
    "Current root posture",
    "Mechanics relationship",
    "Validation guard",
)
MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS = (
    "docs",
    "evals",
    "fixtures",
    "schemas",
    "examples",
    "scripts",
    "tests",
    "config",
    "manifests",
    "generated",
    "reports",
    "runners",
    "scorers",
    "templates",
    "quests",
    "mechanics",
)
MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS = (
    "config",
    "examples",
    "fixtures",
    "manifests",
    "reports",
    "runners",
    "schemas",
    "scorers",
    "templates",
)
MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    "docs": ("source guidance", "mechanic-owned docs"),
    "evals": ("source proof object", "source eval packages stay out of mechanics"),
    "fixtures": ("route-card-only", "mechanics/proof-infra/parts/fixture-families/fixtures/"),
    "schemas": ("route-card-only", "mechanics/proof-object/parts/eval-contracts/schemas/"),
    "examples": ("route-card-only", "evals/**/examples/"),
    "scripts": ("repo-wide", "mechanic-owned scripts"),
    "tests": ("repo-wide", "mechanics/<mechanic>/parts/<part>/tests/"),
    "config": ("route-card-only", "mechanics/agon/parts/*/config/"),
    "manifests": ("route-card-only", "mechanics/recurrence/parts/"),
    "generated": ("derived readers", "part-local generated"),
    "reports": ("route-card-only", "mechanics/release-support/parts/"),
    "runners": ("route-card-only", "mechanics/proof-infra/parts/reportable-contracts/runners/"),
    "scorers": ("route-card-only", "mechanics/proof-infra/parts/reportable-contracts/scorers/"),
    "templates": ("route-card-only", "mechanics/proof-object/parts/eval-authoring/templates/"),
    "quests": ("source quest records", "mechanics/questbook/parts/"),
    "mechanics": ("operation atlas", "mechanics/EVIDENCE_CLUSTERS.md"),
}
MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS = (
    "Mechanic Root-district Reconnaissance",
    "Root District Reconnaissance Ledger",
    "Source Eval Tree Topology",
    "`evals/<claim-family>/<eval-name>/`",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "docs",
    "evals",
    "fixtures",
    "schemas",
    "examples",
    "scripts",
    "tests",
    "config",
    "manifests",
    "generated",
    "reports",
    "runners",
    "scorers",
    "templates",
    "quests",
    "mechanics",
    "route-card-only",
    "mechanic-owned payload",
    "mechanics/AGENTS.md#validation",
)

MECHANIC_PARENT_CLASS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0072-mechanic-parent-class-contract.md"
)
MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Class Contract",
    "AoA-aligned mechanics",
    "evals-native mechanics",
    "owner-named evals-native",
    "aoa-agents` keeps Titan role, bearer, summon, and incarnation law",
    "every AoA-aligned parent appears in the AoA-aligned table",
    "owner-named evals-native parents state the stronger owner split",
    "the two class sets are disjoint",
    "former wrong parent forms",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_parent_class",
)

ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS = (
    "Mechanics evidence",
    "parent evidence",
    "root district posture",
    "residual root-authored surface classification",
)

ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0085-root-authored-surface-classification.md"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND = (
    "python -m pytest -q tests/test_mechanics_topology.py"
)

ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION = "Residual Root-authored Surface Classification"
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS = (
    "Surface",
    "Root role",
    "Mechanic boundary",
    "Validation guard",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS = (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    "Root role",
    "Mechanic boundary",
    "Validation guard",
    "root-owned",
    "mechanic-owned payload",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS = (
    "Root-authored Surface Classification",
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    "docs/",
    "scripts/",
    "tests/",
    "root-owned",
    "mechanic-owned payload",
    "unclassified root-authored surface",
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS: dict[str, tuple[str, ...]] = {
    "docs": (
        "AGENTS.md",
        "README.md",
        "architecture/AGENT_INDEX.md",
        "architecture/AOA_EVALS_MCP_CONTRACT.md",
        "architecture/ARCHITECTURE.md",
        "architecture/LEGACY_NAMING.md",
        "architecture/PROOF_TOPOLOGY.md",
        "architecture/ROUTE_RESIDUE_GUARDS.md",
        "architecture/topology_contract.yaml",
        "testing/AGENTS.md",
        "testing/TEST_TOPOLOGY.md",
        "testing/test_inventory.json",
        "validation/AGENTS.md",
        "validation/COMMAND_AUTHORITY.md",
        "validation/SCRIPT_TOPOLOGY.md",
        "validation/VALIDATOR_TOPOLOGY.md",
        "validation/script_inventory.json",
        "validation/validation_lanes.json",
        "validation/validator_inventory.json",
        "guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        "guides/BASELINE_COMPARISON_GUIDE.md",
        "guides/BLIND_SPOT_DISCLOSURE_GUIDE.md",
        "guides/BOUNDARY_ROUTE_CHECKLIST.md",
        "guides/COMPARISON_SPINE_GUIDE.md",
        "guides/EVAL_PHILOSOPHY.md",
        "guides/EVAL_REVIEW_GUIDE.md",
        "guides/EVAL_RUBRIC.md",
        "guides/FIXTURE_SURFACE_GUIDE.md",
        "guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md",
        "guides/REGRESSION_PROOF_SURFACES.md",
        "guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        "guides/SCORE_SEMANTICS_GUIDE.md",
        "guides/SHARED_PROOF_INFRA_GUIDE.md",
        "guides/VERDICT_INTERPRETATION_GUIDE.md",
        "operations/AGENTS_ROOT_REFERENCE.md",
        "operations/QUESTBOOK_EVAL_INTEGRATION.md",
        "operations/RELEASING.md",
        "operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md",
    ),
    "scripts": (
        "AGENTS.md",
        "build_catalog.py",
        "eval_capsule_contract.py",
        "eval_catalog_contract.py",
        "eval_comparison_spine_contract.py",
        "eval_proof_contract_helpers.py",
        "eval_section_contract.py",
        "generate_decision_indexes.py",
        "generate_eval_report_index.py",
        "ci_gate.py",
        "release_check.py",
        "validation_lanes.py",
        "validate_nested_agents.py",
        "validate_repo.py",
        "validate_semantic_agents.py",
        "validators/__init__.py",
        "validators/agon.py",
        "validators/antifragility.py",
        "validators/audit.py",
        "validators/artifact_hooks.py",
        "validators/boundary_bridge.py",
        "validators/checkpoint.py",
        "validators/common.py",
        "validators/comparison_spine.py",
        "validators/distillation.py",
        "validators/docs_decisions.py",
        "validators/docs_routes.py",
        "validators/docs_topology.py",
        "validators/eval_bundles.py",
        "validators/evidence_readouts.py",
        "validators/experience.py",
        "validators/generated_parity.py",
        "validators/growth_cycle.py",
        "validators/mechanic_legacy.py",
        "validators/mechanic_parents.py",
        "validators/mechanic_parts.py",
        "validators/mechanics.py",
        "validators/mechanics_routes.py",
        "validators/method_growth.py",
        "validators/phase_alpha_matrix.py",
        "validators/proof_infra.py",
        "validators/proof_loop.py",
        "validators/proof_object.py",
        "validators/publication_receipts.py",
        "validators/questbook.py",
        "validators/recurrence.py",
        "validators/release_support.py",
        "validators/report_index.py",
        "validators/root_authority.py",
        "validators/root_context.py",
        "validators/root_guidance.py",
        "validators/root_route_cards.py",
        "validators/root_topology.py",
        "validators/route_residue.py",
        "validators/rpg.py",
        "validators/runtime_audit.py",
        "validators/runtime_candidates.py",
        "validators/source_eval_domains.py",
        "validators/source_doctrine.py",
        "validators/source_eval_contracts.py",
        "validators/titan.py",
        "validators/validation_topology.py",
    ),
    "tests": (
        "AGENTS.md",
        "test_build_catalog.py",
        "test_comparison_surface_contracts.py",
        "test_current_direction_routes.py",
        "test_decision_indexes.py",
        "test_docs_topology.py",
        "test_downstream_feed_contracts.py",
        "test_quest_and_reader_surfaces.py",
        "test_eval_source_topology.py",
        "test_generated_parity.py",
        "test_generated_route_residue.py",
        "test_guidance_surface_routes.py",
        "test_index_surface_roles.py",
        "test_mechanic_evidence_ledger.py",
        "test_memo_contradiction_phase_alpha_gap_report.py",
        "test_memo_contradiction_phase_alpha_rerun_report.py",
        "test_memo_writeback_act_phase_alpha_report.py",
        "test_mechanic_legacy_bridge.py",
        "test_mechanic_legacy_archive_routes.py",
        "test_mechanic_manifest_routes.py",
        "test_mechanic_part_contracts.py",
        "test_mechanic_part_validation_commands.py",
        "test_mechanic_parent_direction.py",
        "test_mechanic_parent_topology.py",
        "test_mechanic_parts_index.py",
        "test_mechanic_root_district_recon.py",
        "test_mechanic_surface_contracts.py",
        "test_mechanics_topology.py",
        "test_nested_agents_docs.py",
        "test_roadmap_parity.py",
        "test_read_model_command_ownership.py",
        "test_repo_validation_workflow.py",
        "test_root_surface_roles.py",
        "test_route_residue.py",
        "test_runtime_evidence_surfaces.py",
        "test_report_schema_contracts.py",
        "test_script_topology.py",
        "test_test_topology.py",
        "test_validate_repo.py",
        "test_validation_topology.py",
        "test_validate_semantic_agents.py",
        "test_verification_honesty_local_report.py",
        "validate_repo_fixtures.py",
    ),
}

SOURCE_SURFACE_CODE_REF_RE = re.compile(r"`([^`\n]+)`")
SOURCE_SURFACE_FILE_REF_RE = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9_.-]*$")


def _markdown_heading_section(text: str, heading: str) -> str:
    marker = ""
    heading_level = 0
    start = -1
    for level in (3, 2):
        pattern = re.compile(rf"(?m)^{'#' * level} {re.escape(heading)}\s*$")
        match = pattern.search(text)
        if match:
            marker = match.group(0)
            heading_level = level
            start = match.start()
            break
    if start == -1:
        return ""
    next_h2 = text.find("\n## ", start + len(marker))
    next_h3 = text.find("\n### ", start + len(marker)) if heading_level > 2 else -1
    candidates = [index for index in (next_h2, next_h3) if index != -1]
    end = min(candidates) if candidates else len(text)
    return text[start:end]


def _markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows


def _require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: tuple[str, ...],
    issues: list[ValidationIssue],
) -> None:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return
    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in docs_decisions.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))


def validate_mechanics_root_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=MECHANICS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=MECHANICS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PART_LOCAL_TEST_PLACEMENT_DECISION_NAME,
        tokens=PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(PART_LOCAL_TEST_PLACEMENT_DECISION_NAME, "Part-local Test Placement"),
        issues=issues,
    )
    return issues


def _source_surface_ref_is_path_like(ref: str) -> bool:
    return (
        ref.startswith(("repo:", ".", "/"))
        or "/" in ref
        or "*" in ref
        or "?" in ref
        or "[" in ref
        or SOURCE_SURFACE_FILE_REF_RE.search(ref) is not None
    )


def _source_surface_ref_resolution_issue(repo_root: Path, ref: str) -> str | None:
    if ref.startswith("repo:"):
        return None
    if ref.startswith(("http://", "https://")):
        return None
    if ref.startswith("/"):
        return "source surface ref must be repo-relative or repo-qualified, not absolute"
    if ".." in PurePosixPath(ref).parts:
        return "source surface ref must not traverse outside the repository"
    if "<" in ref or ">" in ref:
        return None

    if any(char in ref for char in "*?["):
        if any(repo_root.glob(ref)):
            return None
        return "stale source surface ref must resolve as a repo-relative glob"

    if (repo_root / ref.rstrip("/")).exists():
        return None
    return "stale source surface ref must resolve as a repo-relative path"


def validate_mechanic_parent_class_map(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    active_parents = set(ACTIVE_MECHANIC_PARENT_NAMES)
    aoa_parents = set(AOA_ALIGNED_MECHANIC_PARENT_NAMES)
    evals_native_parents = set(EVALS_NATIVE_MECHANIC_PARENT_NAMES)

    overlap = sorted(aoa_parents & evals_native_parents)
    if overlap:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanics.py",
                "mechanic parent class sets must be disjoint: " + ", ".join(overlap),
            )
        )

    missing = sorted(active_parents - (aoa_parents | evals_native_parents))
    extra = sorted((aoa_parents | evals_native_parents) - active_parents)
    if missing:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanics.py",
                "active mechanic parents missing from class sets: " + ", ".join(missing),
            )
        )
    if extra:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanics.py",
                "mechanic class sets contain non-active parents: " + ", ".join(extra),
            )
        )

    text = read_text_or_issue(repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME, issues, root=repo_root)
    if not text:
        return issues
    if "currently plausible" in text:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                "active mechanic parents must be described as active allowlisted parents, not merely plausible candidates",
            )
        )
    for token in ("owner-named evals-native", "`aoa-agents` keeps stronger Titan law"):
        if token not in text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence cluster map must mention {token!r}",
                )
            )

    aoa_section = _markdown_heading_section(text, "AoA-aligned parents")
    evals_native_section = _markdown_heading_section(text, "Evals-native parents")
    dimension_section = _markdown_heading_section(
        text, "Active Parent Evidence Dimension Ledger"
    )
    route_refs_section = _markdown_heading_section(
        text, MECHANIC_EVIDENCE_ROUTE_REFS_SECTION
    )
    wrong_parent_section = _markdown_heading_section(text, "Former Wrong Parent Forms")
    for section_name, section_text in (
        ("Active Parent Evidence Dimension Ledger", dimension_section),
        (MECHANIC_EVIDENCE_ROUTE_REFS_SECTION, route_refs_section),
        ("AoA-aligned parents", aoa_section),
        ("Evals-native parents", evals_native_section),
        ("Former Wrong Parent Forms", wrong_parent_section),
    ):
        if not section_text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence cluster map must contain section {section_name!r}",
                )
            )

    for token in MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS:
        if token not in dimension_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence dimension ledger must mention {token!r}",
                )
            )

    for token in MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS:
        if token not in route_refs_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence route refs ledger must mention {token!r}",
                )
            )

    expected_class_by_parent = {
        parent_name: "AoA-aligned" for parent_name in AOA_ALIGNED_MECHANIC_PARENT_NAMES
    }
    expected_class_by_parent.update(
        {parent_name: "evals-native" for parent_name in EVALS_NATIVE_MECHANIC_PARENT_NAMES}
    )
    ledger_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(dimension_section):
        parent_cell = cells[0] if cells else ""
        parent_name = parent_cell.strip("`")
        if parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
            if parent_name in ledger_rows:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"active parent `{parent_name}` must appear only once in the evidence dimension ledger",
                    )
                )
            ledger_rows[parent_name] = cells
            if len(cells) != len(MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence dimension ledger row for `{parent_name}` must have {len(MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS)} columns",
                    )
                )
                continue
            expected_class = expected_class_by_parent[parent_name]
            if cells[1] != expected_class:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence dimension ledger row for `{parent_name}` must use class `{expected_class}`",
                    )
                )
            for column_name, cell in zip(
                MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS[2:],
                cells[2:],
                strict=True,
            ):
                if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence dimension ledger row for `{parent_name}` must fill `{column_name}`",
                        )
                    )

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        if parent_name not in ledger_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"active parent `{parent_name}` must appear in the evidence dimension ledger",
                )
            )

    route_ref_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(route_refs_section):
        parent_cell = cells[0] if cells else ""
        parent_name = parent_cell.strip("`")
        if parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
            if parent_name in route_ref_rows:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"active parent `{parent_name}` must appear only once in the evidence route refs ledger",
                    )
                )
            route_ref_rows[parent_name] = cells
            if len(cells) != len(MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must have {len(MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS)} columns",
                    )
                )
                continue
            route_refs = [
                match.group(1).strip()
                for match in SOURCE_SURFACE_CODE_REF_RE.finditer(cells[1])
                if _source_surface_ref_is_path_like(match.group(1).strip())
            ]
            route_refs = list(dict.fromkeys(route_refs))
            if len(route_refs) < MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must name at least {MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT} path-like route refs",
                    )
                )
            parent_prefix = f"mechanics/{parent_name}/"
            if not any(ref.startswith(parent_prefix) for ref in route_refs):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include an active parent route under `{parent_prefix}`",
                    )
                )
            if not any(not ref.startswith("mechanics/") for ref in route_refs):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include at least one non-mechanics route ref",
                    )
                )
            living_non_mechanics_refs = [
                ref
                for ref in route_refs
                if not ref.startswith("mechanics/")
                and ref not in MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS
                and not any(
                    ref.startswith(prefix)
                    for prefix in MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES
                )
            ]
            if not living_non_mechanics_refs:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include living non-mechanics evidence; rationale-only decision refs are not enough",
                    )
                )
            for ref in route_refs:
                if ref in MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` must not use generic root validator route `{ref}` as parent evidence",
                        )
                    )
                if ref.startswith("repo:") or "<" in ref or ">" in ref:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` must use concrete local repo-relative route refs, not `{ref}`",
                        )
                    )
                    continue
                ref_issue = _source_surface_ref_resolution_issue(repo_root, ref)
                if ref_issue is not None:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` has stale route ref: {ref_issue}: `{ref}`",
                        )
                    )

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        if parent_name not in route_ref_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"active parent `{parent_name}` must appear in the evidence route refs ledger",
                )
            )

    for parent_name in AOA_ALIGNED_MECHANIC_PARENT_NAMES:
        row_token = f"| `{parent_name}` |"
        if row_token not in aoa_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"AoA-aligned parent `{parent_name}` must appear in the AoA-aligned table",
                )
            )
        if row_token in evals_native_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"AoA-aligned parent `{parent_name}` must not appear in the evals-native table",
                )
            )

    for parent_name in EVALS_NATIVE_MECHANIC_PARENT_NAMES:
        row_token = f"| `{parent_name}` |"
        if row_token not in evals_native_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"evals-native parent `{parent_name}` must appear in the evals-native table",
                )
            )
        if row_token in aoa_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"evals-native parent `{parent_name}` must not appear in the AoA-aligned table",
                )
            )

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        row_token = f"| `{wrong_parent}` | `{correct_route}` |"
        if row_token not in wrong_parent_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"former wrong parent `{wrong_parent}` must map to `{correct_route}`",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "Active Parent Evidence Dimension Ledger",
            MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
            "meaning/doctrine",
            "owner-named evals-native",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "Active Parent Evidence Dimension Ledger",
            MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
            "owner split and stop-lines",
            "owner-named evals-native",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_CLASS_DECISION_NAME,
        tokens=MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    return issues


def validate_mechanic_root_district_recon_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = read_text_or_issue(
        repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME,
        issues,
        root=repo_root,
    )
    if not text:
        return issues

    recon_section = _markdown_heading_section(
        text, "Root District Reconnaissance Ledger"
    )
    if not recon_section:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                "mechanics evidence cluster map must contain section 'Root District Reconnaissance Ledger'",
            )
        )

    for token in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS:
        if token not in recon_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanic root-district reconnaissance must mention {token!r}",
                )
            )

    recon_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(recon_section):
        district_cell = cells[0] if cells else ""
        district_name = district_cell.strip("`")
        if district_name not in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS:
            continue
        if district_name in recon_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` must appear only once in the reconnaissance ledger",
                )
            )
        recon_rows[district_name] = cells
        if len(cells) != len(MECHANIC_ROOT_DISTRICT_RECON_COLUMNS):
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` reconnaissance row must have {len(MECHANIC_ROOT_DISTRICT_RECON_COLUMNS)} columns",
                )
            )
            continue
        for column_name, cell in zip(
            MECHANIC_ROOT_DISTRICT_RECON_COLUMNS[1:],
            cells[1:],
            strict=True,
        ):
            if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"root district `{district_name}` reconnaissance row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        for token in MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS[district_name]:
            if token not in row_text:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"root district `{district_name}` reconnaissance row must mention '{token}'",
                    )
                )
        if (
            district_name in MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS
            and "route-card-only" not in row_text
        ):
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` reconnaissance row must preserve route-card-only posture",
                )
            )

    for district_name in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS:
        if district_name not in recon_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` must appear in the reconnaissance ledger",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
        tokens=MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Root District Reconnaissance Ledger", "root-district"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=("Focused mechanic topology checks", MECHANIC_ROOT_DISTRICT_RECON_COMMAND),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Root District Reconnaissance Ledger", "mechanic-owned payload"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_root_authored_surface_classification(repo_root: Path) -> list[ValidationIssue]:
    issues: list[tuple[str, str]] = []
    evidence_path = repo_root / MECHANICS_EVIDENCE_CLUSTERS
    if not evidence_path.is_file():
        return [
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                "mechanics evidence cluster map is missing",
            )
        ]

    text = evidence_path.read_text(encoding="utf-8")
    section = _markdown_heading_section(text, ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION)
    if not section:
        issues.append(
            (
                MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                f"mechanics evidence cluster map must contain section {ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION!r}",
            )
        )

    for token in ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS:
        if token not in section:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface classification must mention {token!r}",
                )
            )

    expected_surfaces = {
        f"{district_name}/{file_name}"
        for district_name, file_names in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items()
        for file_name in file_names
    }
    actual_surfaces: set[str] = set()
    for district_name, allowed_names in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items():
        district = repo_root / district_name
        if not district.is_dir():
            issues.append((district_name, "classified root-authored district is missing"))
            continue
        allowed = set(allowed_names)
        if district_name == "docs":
            actual_names = {
                path.relative_to(district).as_posix()
                for path in district.rglob("*")
                if path.is_file() and path.relative_to(district).parts[:1] != ("decisions",)
            }
        elif district_name == "scripts":
            actual_names = {
                path.relative_to(district).as_posix()
                for path in district.rglob("*")
                if path.is_file() and "__pycache__" not in path.relative_to(district).parts
            }
        else:
            actual_names = {path.name for path in district.iterdir() if path.is_file()}
        for file_name in sorted(actual_names - allowed):
            issues.append(
                (
                    f"{district_name}/{file_name}",
                    "unclassified root-authored surface must be routed, moved, or added to the residual classification ledger",
                )
            )
        for file_name in sorted(allowed - actual_names):
            issues.append(
                (
                    f"{district_name}/{file_name}",
                    "classified root-authored surface is missing; update the residual classification ledger if it moved",
                )
            )
        actual_surfaces.update(
            f"{district_name}/{file_name}"
            for file_name in actual_names
            if file_name in allowed
        )

    ledger_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(section):
        if not cells or cells[0] == "Surface":
            continue
        surface_name = cells[0].strip("`")
        if surface_name not in expected_surfaces:
            continue
        if surface_name in ledger_rows:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must appear only once in the residual classification ledger",
                )
            )
        ledger_rows[surface_name] = cells
        if len(cells) != len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS):
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must have {len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS)} columns",
                )
            )
            continue
        for column_name, cell in zip(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS[1:],
            cells[1:],
            strict=True,
        ):
            if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                issues.append(
                    (
                        MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                        f"root-authored surface `{surface_name}` row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        if "mechanic-owned payload" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its mechanic-owned payload boundary",
                )
            )
        if "root-owned" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its root-owned role",
                )
            )

    for surface_name in sorted(expected_surfaces):
        if surface_name not in ledger_rows:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must appear in the residual classification ledger",
                )
            )

    for surface_name in sorted(actual_surfaces - expected_surfaces):
        issues.append((surface_name, "unclassified root-authored surface must not remain in root districts"))

    validation_issues = [
        ValidationIssue(location, message) for location, message in issues
    ]
    _require_tokens(
        repo_root=repo_root,
        path_name=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        tokens=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS,
        issues=validation_issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
            "Root-authored Surface Classification",
        ),
        issues=validation_issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
            "unclassified root-authored surface",
        ),
        issues=validation_issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=validation_issues,
    )
    return validation_issues
