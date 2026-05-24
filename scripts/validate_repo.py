#!/usr/bin/env python3
"""Local validator and catalog builder helpers for aoa-evals source packages."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shlex
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

import yaml
from jsonschema import Draft202012Validator, SchemaError

import eval_catalog_contract
import eval_capsule_contract
import eval_section_contract
import eval_comparison_spine_contract
import eval_proof_contract_helpers
import validate_nested_agents

REPO_ROOT = Path(__file__).resolve().parents[1]
FORMAT_CHECKER = Draft202012Validator.FORMAT_CHECKER
RFC3339_DATE_TIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)


@FORMAT_CHECKER.checks("date-time", raises=(ValueError,))
def _is_date_time(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if RFC3339_DATE_TIME_RE.fullmatch(value) is None:
        return False
    normalized = value[:-1] + "+00:00" if value[-1:].lower() == "z" else value
    normalized = normalized.replace("t", "T", 1)
    parsed = datetime.fromisoformat(normalized)
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def repo_root_from_env(env_name: str, default: Path) -> Path:
    override = os.environ.get(env_name)
    if not override:
        return default
    return Path(override).expanduser().resolve()


def is_abyss_stack_source_root(path: Path) -> bool:
    return (
        path.exists()
        and (path / "README.md").is_file()
        and (
            path
            / "mechanics"
            / "governed-execution"
            / "parts"
            / "return-policy"
            / "schemas"
            / "runtime-return-event.schema.json"
        ).is_file()
        and (path / "scripts" / "validate_stack.py").is_file()
    )


def resolve_abyss_stack_root(default: Path) -> Path:
    override = os.environ.get("ABYSS_STACK_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    default_root = default.expanduser().resolve()
    home_src_root = (Path.home() / "src" / "abyss-stack").resolve()

    for candidate in (default_root, home_src_root):
        if is_abyss_stack_source_root(candidate):
            return candidate
    return default_root


AOA_TECHNIQUES_ROOT = repo_root_from_env(
    "AOA_TECHNIQUES_ROOT", REPO_ROOT.parent / "aoa-techniques"
)
AOA_SKILLS_ROOT = repo_root_from_env("AOA_SKILLS_ROOT", REPO_ROOT.parent / "aoa-skills")
AOA_AGENTS_ROOT = repo_root_from_env("AOA_AGENTS_ROOT", REPO_ROOT.parent / "aoa-agents")
AOA_PLAYBOOKS_ROOT = repo_root_from_env(
    "AOA_PLAYBOOKS_ROOT", REPO_ROOT.parent / "aoa-playbooks"
)
AOA_MEMO_ROOT = repo_root_from_env("AOA_MEMO_ROOT", REPO_ROOT.parent / "aoa-memo")
AOA_ROUTING_ROOT = repo_root_from_env("AOA_ROUTING_ROOT", REPO_ROOT.parent / "aoa-routing")
AOA_KAG_ROOT = repo_root_from_env("AOA_KAG_ROOT", REPO_ROOT.parent / "aoa-kag")
AOA_SDK_ROOT = repo_root_from_env("AOA_SDK_ROOT", REPO_ROOT.parent / "aoa-sdk")
AOA_STATS_ROOT = repo_root_from_env("AOA_STATS_ROOT", REPO_ROOT.parent / "aoa-stats")
AGENTS_OF_ABYSS_ROOT = repo_root_from_env(
    "AGENTS_OF_ABYSS_ROOT", REPO_ROOT.parent / "Agents-of-Abyss"
)
ABYSS_STACK_ROOT = resolve_abyss_stack_root(REPO_ROOT.parent / "abyss-stack")
SOURCE_EVALS_DIR_NAME = "evals"
COMPARISON_FAMILY_BY_BASELINE_MODE = {
    "fixed-baseline": ("comparison", "fixed-baseline"),
    "peer-compare": ("comparison", "peer-compare"),
    "longitudinal-window": ("comparison", "longitudinal-window"),
}
EVAL_INDEX_NAME = "EVAL_INDEX.md"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
ROADMAP_NAME = "ROADMAP.md"
DESIGN_NAME = "DESIGN.md"
DESIGN_AGENTS_NAME = "DESIGN.AGENTS.md"
GITHUB_AGENTS_NAME = ".github/AGENTS.md"
AGENTS_DISTRICT_NAME = ".agents/AGENTS.md"
SPARK_LANE_AGENTS_NAME = ".agents/spark/AGENTS.md"
SPARK_LANE_SWARM_NAME = ".agents/spark/SWARM.md"
PROOF_TOPOLOGY_NAME = "docs/PROOF_TOPOLOGY.md"
AGENT_INDEX_NAME = "docs/AGENT_INDEX.md"
AGENT_INDEX_CHAIN_DECISION_NAME = "docs/decisions/0103-agent-index-chain-surface.md"
LEGACY_NAMING_NAME = "docs/LEGACY_NAMING.md"
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME = (
    "docs/decisions/0091-legacy-naming-single-bridge-language.md"
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k legacy_naming_single_bridge_language"
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME = (
    "docs/decisions/0096-legacy-naming-posture-guide.md"
)
LEGACY_NAMING_POSTURE_GUIDE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k legacy_naming_posture_guide"
)
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
PART_LOCAL_TEST_PLACEMENT_DECISION_NAME = "docs/decisions/0050-part-local-test-placement.md"
ROOT_ROUTE_CARD_GUARD_DECISION_NAME = "docs/decisions/0051-root-route-card-guard.md"
GENERATED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0073-generated-route-residue-guard.md"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0076-active-mechanic-route-residue-guard.md"
)
ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0077-root-authored-route-residue-guard.md"
)
ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME = (
    "docs/decisions/0092-active-legacy-parent-wording-boundary.md"
)
ACTIVE_LEGACY_PARENT_WORDING_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k active_legacy_parent_wording"
)
DECISION_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0078-decision-route-residue-guard.md"
)
REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0079-repo-config-route-residue-guard.md"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0080-source-bundle-route-residue-guard.md"
)
SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME = (
    "docs/decisions/0104-source-eval-tree-topology.md"
)
EVALS_AGENTS_NAME = "evals/AGENTS.md"
SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS = (
    "python scripts/validate_repo.py",
    "python scripts/build_catalog.py --check",
    "python scripts/generate_eval_report_index.py --check",
    "python -m pytest -q",
)
SOURCE_EVAL_TREE_TOPOLOGY_DECISION_REQUIRED_TOKENS = (
    "Source Eval Tree Topology",
    "`evals/<claim-family>/<eval-name>/`",
    "recursive",
    "evals/AGENTS.md#validation",
    "source-tree topology path",
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/0081-mechanic-payload-route-residue-guard.md"
)
ROOT_ROUTE_CARD_ONLY_DISTRICTS: dict[str, tuple[str, ...]] = {
    "config": ("AGENTS.md", "README.md"),
    "examples": ("AGENTS.md", "README.md"),
    "fixtures": ("AGENTS.md", "README.md"),
    "manifests": ("AGENTS.md", "README.md"),
    "reports": ("AGENTS.md", "README.md"),
    "runners": ("AGENTS.md", "README.md"),
    "schemas": ("AGENTS.md", "README.md"),
    "scorers": ("AGENTS.md", "README.md"),
    "templates": ("AGENTS.md", "README.md"),
}
ROOT_ROUTE_CARD_README_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    "config/README.md": (
        "compatibility route card",
        "Active root config payloads route to the operation that owns them",
        "Operating Card",
        "mechanics/agon/parts/*/config/",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/config/",
    ),
    "examples/README.md": (
        "compatibility route card",
        "Active root examples payloads route beside the source that owns their",
        "Operating Card",
        "evals/**/examples/",
        "mechanics/audit/parts/",
    ),
    "fixtures/README.md": (
        "compatibility route card",
        "Active fixture families live under the owning mechanic part",
        "Operating Card",
        "mechanics/proof-infra/parts/fixture-families/fixtures/",
        "mechanics/comparison-spine/parts/",
    ),
    "manifests/README.md": (
        "compatibility route card",
        "Active root manifest payloads route next to the mechanic part",
        "Operating Card",
        "mechanics/agon/parts/*/manifests/",
        "mechanics/recurrence/parts/control-plane-integrity/manifests/",
        "mechanics/recurrence/parts/portable-proof-beacons/manifests/",
    ),
    "reports/README.md": (
        "compatibility route card",
        "Active root reports payloads route to the owning bundle or mechanic part",
        "Operating Card",
        "Current top-level shared dossiers",
        "none",
        "mechanics/proof-loop/parts/route-smoke/reports/",
        "mechanics/release-support/parts/",
    ),
    "runners/README.md": (
        "compatibility route card",
        "Operating Card",
        "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
        "Use [AGENTS.md](AGENTS.md) for runner contract rules",
    ),
    "schemas/README.md": (
        "compatibility route card",
        "Active root schema payloads route to mechanic-local owners",
        "Operating Card",
        "mechanics/proof-object/parts/eval-contracts/schemas/",
        "mechanics/proof-infra/parts/reportable-contracts/schemas/",
        "mechanics/questbook/parts/",
    ),
    "scorers/README.md": (
        "compatibility route card",
        "Operating Card",
        "mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py",
        "Use [AGENTS.md](AGENTS.md) for scorer helper rules",
    ),
    "templates/README.md": (
        "compatibility route card",
        "Active root template payloads route to the eval authoring template",
        "Operating Card",
        "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    ),
}
ROOT_ROUTE_CARD_README_FORBIDDEN_TOKENS = (
    "Shared fixture naming discipline:",
    "Shared dossier naming discipline",
    "Do not recreate active root runner payloads",
    "Do not recreate active root scorer helper aliases",
)
ROOT_ROUTE_CARD_GUARD_DECISION_REQUIRED_TOKENS = (
    "Root Route-card Guard",
    "route-card-only surfaces",
    "docs/PROOF_TOPOLOGY.md",
    "validator allowlist",
    "does not forbid bundle-local examples or reports",
)
GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Generated Route Residue Guard",
    "structured references",
    "route-card-only root district",
    "part-local generated readers",
    "content_markdown",
    "python -m pytest -q tests/test_validate_repo.py -k generated_route_residue",
)
GENERATED_READER_INDEX_REQUIRED_TOKENS = (
    "# Generated Reader Index",
    "repo-wide derived reader surfaces",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.example.json",
    "source owner surface",
    'Source surfaces answer\n"what is true?"',
)
GENERATED_AGENTS_REQUIRED_TOKENS = (
    "repo-wide derived reader surfaces only",
    "Authored source surfaces keep doctrine",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "generated/quest_catalog.min.example.json",
    "generated/quest_dispatch.min.example.json",
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k active_mechanic_route_residue"
)
ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k root_authored_route_residue"
)
DECISION_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k decision_route_residue"
)
REPO_CONFIG_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k repo_config_route_residue"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k source_bundle_route_residue"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_payload_route_residue"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Active Mechanic Route Residue Guard",
    "authored mechanics route cards",
    "route-card-only root district",
    "same part root",
    "`evals/<family>/<eval>/...`",
    "legacy parent route",
    ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
)
ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Root Authored Route Residue Guard",
    "root-facing authored surfaces",
    "route-card-only root district",
    "docs/decisions/",
    "historical context",
    "`evals/<family>/<eval>/...`",
    ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
)
ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS = (
    "Active Legacy Parent Wording Boundary",
    "legacy parent form",
    "active route wording",
    "`runtime-evidence`",
    "evidence class",
    "not the parent mechanic",
    "schema filename",
    ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
)
DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Decision Route Residue Guard",
    "decision records",
    "historical context",
    "route-card-only root district",
    "`evals/<family>/<eval>/...`",
    "active `mechanics/...`",
    DECISION_ROUTE_RESIDUE_COMMAND,
)
REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Repo Config Route Residue Guard",
    ".gitignore",
    ".github/workflows/",
    "legacy mechanic parent",
    "route-card-only root district",
    "not historical memory",
    REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
)
SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Source Bundle Route Residue Guard",
    "source proof objects",
    "bundle-local path",
    "repo-qualified sibling",
    "legacy mechanic parent",
    "route-card-only root district",
    SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Payload Route Residue Guard",
    "active mechanics payload",
    "part-local path",
    "repo-qualified sibling",
    "legacy mechanic parent",
    "route-card-only root district",
    "structured manifest route fields",
    "root-authored docs globs",
    MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
)
ROOT_DESIGN_REQUIRED_TOKENS = (
    "bounded proof organ",
    "proof object",
    "generated surface helps navigation",
    "runtime candidates",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "docs/ARCHITECTURE.md",
    "docs/EVAL_PHILOSOPHY.md",
    "docs/decisions/",
)
ARCHITECTURE_PROOF_MODEL_DECISION_NAME = (
    "docs/decisions/0093-architecture-proof-model-contract.md"
)
ARCHITECTURE_PROOF_MODEL_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k architecture_proof_model"
)
ARCHITECTURE_REQUIRED_TOKENS = (
    "technical proof model",
    "Use this file for the proof model",
    "DESIGN.md",
    "docs/PROOF_TOPOLOGY.md",
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
)
ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS = (
    "It is not the system design thesis",
    "but they are not themselves eval bundles",
    "but they are not themselves proof surfaces",
)
ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS = (
    "Architecture Proof Model Contract",
    "technical proof model",
    "DESIGN.md",
    "docs/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "mechanics as operation support",
    "owner-named evals-native",
    "legacy bridge layering",
    ARCHITECTURE_PROOF_MODEL_COMMAND,
)
DESIGN_AGENTS_REQUIRED_TOKENS = (
    "agent-facing guidance",
    "nearest card",
    "bundle-local review",
    "source proof object",
    "generated companions",
    "Active mechanic packages",
    "Before changing package boundaries",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "active mechanics, and file-movement boundaries",
    "Maintained agent lanes",
    ".agents/spark/",
    "closeout",
)
ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready",
)
DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "Future mechanic packages",
    "Before package growth",
    "before mechanics or file movement",
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
    "A new `mechanics/` parent",
    "No remaining named candidate family is promoted by symmetry",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME = (
    "docs/decisions/0106-memory-consumer-proof-boundary.md"
)
MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS = (
    "`aoa-evals`",
    "reviewed `aoa-memo` object ids and provenance",
    "can cite reviewed recall as bounded context",
    "proof authority stays with",
    "eval bundle or owning mechanic",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS = (
    "Memory is not proof.",
    "Reviewed `aoa-memo` memory can provide recall context only when the eval cites",
    "object ids, provenance, lifecycle, and generated read models",
    "`aoa-evals` has route_only memory posture until a local memo port exists.",
    "Session evidence routes through `.aoa` or source proof artifacts before any",
    "later `aoa-memo` reviewed intake.",
    "Treat `aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs",
    "access-plane evidence for inspection and review",
)
MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS = (
    "Memory evidence context",
    "reviewed `aoa-memo` object ids, provenance, lifecycle, generated memory read models",
    "`aoa_memo` MCP access-plane dry-runs",
    "memory is not proof; `aoa-evals` stays route_only until a local memo port exists",
    "MCP output is inspection evidence only",
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
PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready operations",
    "while Phase 4 maps the topology",
    "before mechanics growth starts from a root path",
    "A future `mechanics/` package",
    "It is not the roadmap",
    "The goal is not a decorative tree",
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
    "docs/decisions/0100-active-mechanics-topology-wording.md"
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k "
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
    "docs/PROOF_TOPOLOGY.md",
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
    "docs/LEGACY_NAMING.md",
    "posture guide",
    "accepted-input",
    "active topology",
    "generated projections",
    "archive details",
    "not authorize starting new work from legacy directories",
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Posture Guide",
    "docs/LEGACY_NAMING.md",
    "posture guide",
    "not a global archive map",
    "archive details",
    "PROVENANCE.md",
    LEGACY_NAMING_POSTURE_GUIDE_COMMAND,
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Single-Bridge Language",
    "docs/LEGACY_NAMING.md",
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
    "DESIGN.md",
    "DESIGN.AGENTS.md",
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    "ROADMAP.md",
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
    "docs/decisions/0009-legacy-naming-containment.md",
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
    "DESIGN.md",
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    "ROADMAP.md",
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
    "docs/decisions/0071-mechanic-legacy-skeleton-contract.md",
    "docs/decisions/0075-mechanic-provenance-entry-contract.md",
    "docs/decisions/0082-mechanic-parent-direction-contract.md",
    "docs/decisions/0089-mechanic-legacy-single-bridge.md",
    "docs/decisions/0090-mechanic-provenance-bridge-posture.md",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
)
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_AGENTS_NAME = "mechanics/AGENTS.md"
MECHANIC_PARENT_ALLOWLIST_DECISION_NAME = (
    "docs/decisions/0052-mechanic-parent-allowlist.md"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME = (
    "docs/decisions/0083-mechanic-evidence-dimension-ledger.md"
)
MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME = (
    "docs/decisions/0084-mechanic-root-district-reconnaissance.md"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME = (
    "docs/decisions/0085-root-authored-surface-classification.md"
)
MECHANICS_ROOT_ALLOWED_FILES = (
    "AGENTS.md",
    "EVIDENCE_CLUSTERS.md",
    "README.md",
)
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
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_evidence_dimension"
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
    "docs/decisions/0101-mechanic-evidence-route-refs.md"
)
MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_evidence_route_refs"
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
MECHANIC_ROOT_DISTRICT_RECON_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_root_district_recon"
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
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k root_authored_surface_classification"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION = "Residual Root-authored Surface Classification"
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS = (
    "Surface",
    "Root role",
    "Mechanic boundary",
    "Validation guard",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS: dict[str, tuple[str, ...]] = {
    "docs": (
        "AGENTS.md",
        "AGENTS_ROOT_REFERENCE.md",
        "AGENT_INDEX.md",
        "ARCHITECTURE.md",
        "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        "BASELINE_COMPARISON_GUIDE.md",
        "BLIND_SPOT_DISCLOSURE_GUIDE.md",
        "COMPARISON_SPINE_GUIDE.md",
        "EVAL_PHILOSOPHY.md",
        "EVAL_REVIEW_GUIDE.md",
        "EVAL_RUBRIC.md",
        "FIXTURE_SURFACE_GUIDE.md",
        "LEGACY_NAMING.md",
        "PORTABLE_EVAL_BOUNDARY_GUIDE.md",
        "PROOF_TOPOLOGY.md",
        "QUESTBOOK_EVAL_INTEGRATION.md",
        "README.md",
        "REGRESSION_PROOF_SURFACES.md",
        "RELEASING.md",
        "REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        "REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md",
        "SCORE_SEMANTICS_GUIDE.md",
        "SHARED_PROOF_INFRA_GUIDE.md",
        "VERDICT_INTERPRETATION_GUIDE.md",
        "BOUNDARY_ROUTE_CHECKLIST.md",
    ),
    "scripts": (
        "AGENTS.md",
        "build_catalog.py",
        "eval_capsule_contract.py",
        "eval_catalog_contract.py",
        "eval_comparison_spine_contract.py",
        "eval_proof_contract_helpers.py",
        "eval_section_contract.py",
        "generate_eval_report_index.py",
        "release_check.py",
        "validate_nested_agents.py",
        "validate_repo.py",
        "validate_semantic_agents.py",
    ),
    "tests": (
        "AGENTS.md",
        "test_build_catalog.py",
        "test_current_direction_routes.py",
        "test_downstream_feed_contracts.py",
        "test_memo_contradiction_phase_alpha_gap_report.py",
        "test_memo_contradiction_phase_alpha_rerun_report.py",
        "test_memo_writeback_act_phase_alpha_report.py",
        "test_nested_agents_docs.py",
        "test_roadmap_parity.py",
        "test_validate_repo.py",
        "test_validate_semantic_agents.py",
        "test_verification_honesty_local_report.py",
    ),
}
AGENT_INDEX_REQUIRED_TOKENS = (
    "pass-through index for agents",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "nearest `AGENTS.md`",
    "docs/PROOF_TOPOLOGY.md",
    "mechanics/README.md",
    "docs/decisions/README.md",
    "route-card-only",
    "compatibility districts",
    "mechanics/<parent>/parts/<part>/VALIDATION.md",
    "mechanics/<parent>/parts/AGENTS.md",
    "Executable validation commands belong in the nearest `AGENTS.md`",
)
AGENT_INDEX_DECISION_REQUIRED_TOKENS = (
    "Agent Index Chain Surface",
    "docs/AGENT_INDEX.md",
    "docs/README.md",
    "active mechanic parent",
    "repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation",
    "route-card-only root districts",
    "Executable validation commands remain in the nearest `AGENTS.md`",
)
READ_MODEL_COMMAND_OWNER_PATHS = (
    ".github/pull_request_template.md",
    "CONTRIBUTING.md",
    "README.md",
    "ROADMAP.md",
    "AUDIT.md",
    "docs/README.md",
    "docs/AGENT_INDEX.md",
    "docs/PROOF_TOPOLOGY.md",
    "docs/LEGACY_NAMING.md",
    "docs/RELEASING.md",
    "docs/REGRESSION_PROOF_SURFACES.md",
    "evals/README.md",
    "generated/README.md",
    "quests/README.md",
    "quests/LIFECYCLE.md",
    "mechanics/README.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
)
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
    "docs/AGENT_INDEX.md",
    "docs/PROOF_TOPOLOGY.md",
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
    "Recommended Reading Paths",
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
AUDIT_SURFACE_ROLE_REQUIRED_TOKENS = (
    "Audit Surface Map",
    "AGENTS.md#audit-and-review-route",
    "owns route law",
    "AGENTS.md#verify",
    "Route cards own the commands",
)
ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS = (
    "# Proof Direction Roadmap",
    "active direction surface for `aoa-evals`",
    "roadmap owns direction and sequencing",
    "release history: [CHANGELOG.md](CHANGELOG.md)",
    "## Update Rule",
    "## Current Direction",
    "## Direction Anchors",
    "## Horizons",
)
ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS = (
    "Route residue guard family",
    "generated/readout, active mechanic, root-authored, decision, repo-config, source-bundle, and mechanic-payload residue guards",
    "owner contracts",
)
ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS = (
    LEGACY_NAMING_NAME,
    "Legacy naming",
    "active names",
    "legacy bridge posture",
)
ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS = (
    "Mechanics evidence",
    "parent evidence",
    "root district posture",
    "residual root-authored surface classification",
)
ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS = (
    "Mechanic lower index",
    "DIRECTION.md",
    "part/payload source surfaces",
    "parts index synchronization",
    "payload coverage",
)
ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS = (
    "Legacy bridge",
    "single controlled bridge posture",
    "active mechanic surfaces",
    "runtime evidence limits",
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
MECHANIC_ROUTE_CARD_FILES = tuple(
    route
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
    for route in (
        f"mechanics/{parent_name}/AGENTS.md",
        f"mechanics/{parent_name}/README.md",
        f"mechanics/{parent_name}/DIRECTION.md",
        f"mechanics/{parent_name}/PARTS.md",
    )
)
MECHANIC_PARENT_README_FILES = tuple(
    f"mechanics/{parent_name}/README.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PARENT_AGENTS_FILES = tuple(
    f"mechanics/{parent_name}/AGENTS.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PART_CONTRACT_FILES = tuple(
    f"mechanics/{parent_name}/PARTS.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_DIRECTION_FILES = tuple(
    f"mechanics/{parent_name}/DIRECTION.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PROVENANCE_FILES = tuple(
    f"mechanics/{parent_name}/PROVENANCE.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/README.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_INDEX_FILES = tuple(
    f"mechanics/{parent_name}/legacy/INDEX.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_DISTILLATION_LOG_FILES = tuple(
    f"mechanics/{parent_name}/legacy/DISTILLATION_LOG.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_RAW_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/raw/README.md"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_SKELETON_FILES = (
    MECHANIC_PROVENANCE_FILES
    + MECHANIC_LEGACY_README_FILES
    + MECHANIC_LEGACY_INDEX_FILES
    + MECHANIC_LEGACY_DISTILLATION_LOG_FILES
    + MECHANIC_LEGACY_RAW_README_FILES
)
MECHANIC_LEGACY_SKELETON_DECISION_NAME = (
    "docs/decisions/0071-mechanic-legacy-skeleton-contract.md"
)
MECHANIC_PART_CONTRACT_REQUIRED_TOKENS = (
    "## Part Contract",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
)
MECHANIC_PART_README_REQUIRED_TOKENS = (
    "## Source Surfaces",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
MECHANIC_PART_README_STOP_LINE_LEAD_IN = (
    "Boundary: this part supports its local proof operation. These claims stay outside\n"
    "the part:"
)
MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS = (
    "This part must not claim:",
    "Do not use this part to claim:",
)
MECHANIC_PART_README_CONTRACT_DECISION_NAME = (
    "docs/decisions/0074-mechanic-part-readme-contract.md"
)
MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME = (
    "docs/decisions/0086-mechanic-part-payload-inventory.md"
)
MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_payload_inventory"
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME = (
    "docs/decisions/0097-mechanic-parent-guidance-boundary.md"
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_guidance_boundary"
)
MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME = (
    "docs/decisions/0087-mechanic-part-validation-command-reachability.md"
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME = (
    "docs/decisions/0102-mechanic-part-validation-command-ownership.md"
)
MECHANIC_PART_VALIDATION_COMMAND_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_validation_command"
)
MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME = (
    "docs/decisions/0088-mechanic-parts-index-synchronization.md"
)
MECHANIC_PARTS_INDEX_SYNC_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_parts_index_sync"
)
MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME = (
    "docs/decisions/0094-mechanic-part-source-surface-reference-guard.md"
)
MECHANIC_PART_SOURCE_SURFACE_REF_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_source_surface"
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME = (
    "docs/decisions/0095-mechanic-part-source-surfaces-section-contract.md"
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_source_surfaces_section"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME = (
    "docs/decisions/0089-mechanic-legacy-single-bridge.md"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_legacy_single_bridge"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME = (
    "docs/decisions/0090-mechanic-provenance-bridge-posture.md"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_bridge_posture"
)
MECHANIC_PART_ALLOWED_PAYLOAD_DIRS = (
    "config",
    "docs",
    "examples",
    "fixtures",
    "generated",
    "manifests",
    "reports",
    "runners",
    "schemas",
    "scorers",
    "scripts",
    "seeds",
    "templates",
    "tests",
)
MECHANIC_THIN_PART_REQUIRED_TOKENS = (
    "eval-backed thin support route",
    "payload subdirectories are absent by design",
    "source eval package stays under `evals/`",
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
MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part README Contract",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`## Source Surfaces`",
    "`## Inputs`",
    "`## Outputs`",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "`## Validation`",
    "parent `PARTS.md`",
    "orphan part",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract",
)
MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Payload Inventory",
    "`mechanics/<parent>/parts/<part>/`",
    "payload subdirectory",
    "eval-backed thin support route",
    "part README",
    "unexpected payload class",
    "empty payload subdirectory",
    "unexpected part-root file",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "mechanics/AGENTS.md#validation",
    "focused mechanic part payload-inventory guard",
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
MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Reachability",
    "`## Validation`",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "python command",
    "reachable path",
    "payload coverage anchor",
    "naked route-wide command",
    "stale validation path",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "mechanics/AGENTS.md#validation",
    "focused mechanic part validation-command guard",
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Ownership",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`mechanics/<parent>/parts/<part>/VALIDATION.md`",
    "`mechanics/<parent>/parts/AGENTS.md`",
    "mechanic index surfaces",
    "centralized child validation",
    "python command",
    "payload coverage anchor",
    "stale validation path",
    "README files remain contract maps",
    "nearest `AGENTS.md`",
)
MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS = (
    "Mechanic PARTS Index Synchronization",
    "`mechanics/<parent>/PARTS.md`",
    "actual part directory",
    "declared part route",
    "stale local part route",
    "cross-parent reference",
    MECHANIC_PARTS_INDEX_SYNC_COMMAND,
)
MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Source Surface Reference Guard",
    "`## Source Surfaces`",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "repo-relative path",
    "repo-qualified sibling ref",
    "placeholder route",
    "stale source surface ref",
    MECHANIC_PART_SOURCE_SURFACE_REF_COMMAND,
)
MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Source Surfaces Section Contract",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`## Source Surfaces`",
    "at least one path-like source ref",
    "plural section",
    "not `## Source Surface`",
    "not `## Active Surfaces`",
    MECHANIC_PART_SOURCE_SURFACES_SECTION_COMMAND,
)
MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Single Bridge",
    "`PROVENANCE.md`",
    "single controlled bridge",
    "active mechanic surfaces",
    "legacy archive",
    "active surface",
    "direct archive-internal references",
    "must not carry archive details",
    "JSON",
    "YAML",
    MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
)
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
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Bridge Posture",
    "Current Applicability",
    "active-to-archive bridge",
    "Review Log",
    "Use active surfaces first:",
    "`DIRECTION.md`",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
)
MECHANIC_PARENT_DIRECTION_DECISION_NAME = (
    "docs/decisions/0082-mechanic-parent-direction-contract.md"
)
MECHANIC_PARENT_DIRECTION_COMMAND = (
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_direction"
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
MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "git history",
    "INDEX.md",
)
MECHANIC_LEGACY_README_REQUIRED_TOKENS = (
    "../PROVENANCE.md",
    "INDEX.md",
    "DISTILLATION_LOG.md",
    "raw/README.md",
    "archive-local route",
    "current active route",
)
MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS = (
    "raw payload",
    "archive-local index or accounting log",
    "forgotten residue",
    "current active route",
    "active part route",
    "raw-only archive route",
)
MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Archive Boundary",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "archive-local route",
    "archive-local index",
    "accounting log",
    "`../PROVENANCE.md`",
    "Current Applicability",
    "Review Log",
    "current active route",
    "unindexed raw payloads",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_legacy_skeleton",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_legacy_raw_payload",
)
MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS = (
    "active",
    "legacy/README.md",
    "legacy archive owns",
    "archive details",
)
MECHANIC_PROVENANCE_ENTRY_DECISION_NAME = (
    "docs/decisions/0075-mechanic-provenance-entry-contract.md"
)
MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Entry Contract",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "active route first",
    "not active topology",
    "archive details",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
)
MECHANIC_PARENT_CLASS_DECISION_NAME = (
    "docs/decisions/0072-mechanic-parent-class-contract.md"
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
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_class",
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
GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES = tuple(
    f"mechanics/{wrong_parent}/"
    for wrong_parent, _correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES = tuple(
    f"mechanics/{wrong_parent}"
    for wrong_parent, _correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES = tuple(
    f"{district_name}/" for district_name in ROOT_ROUTE_CARD_ONLY_DISTRICTS
)
GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES = tuple(ROOT_ROUTE_CARD_ONLY_DISTRICTS)
GENERATED_ROUTE_RESIDUE_SKIP_KEYS = frozenset(
    {
        "content_markdown",
    }
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>(?:"
    + "|".join(re.escape(district) for district in ROOT_ROUTE_CARD_ONLY_DISTRICTS)
    + r")(?:/[A-Za-z0-9._*<>-]+)+/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>mechanics/(?:"
    + "|".join(
        re.escape(wrong_parent)
        for wrong_parent, _correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES
    )
    + r")(?:/[A-Za-z0-9._*<>-]+)*/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_TOKEN_STRIP_CHARS = "`.,;:)]}\"'"
ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES = (
    ".agents/spark/SWARM.md",
    "AGENTS.md",
    "AUDIT.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "DESIGN.AGENTS.md",
    "DESIGN.md",
    "EVAL_INDEX.md",
    "EVAL_SELECTION.md",
    "QUESTBOOK.md",
    "README.md",
    "ROADMAP.md",
    "evals/AGENTS.md",
)
ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    "Former root",
    "former root",
    "historical root",
    "Do not recreate",
    "compatibility route card",
    "mapped through",
    "route-card",
    "route card",
)
DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    *ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS,
    "legacy",
    "provenance",
    "old root",
    "previous root",
    "stale authored path example",
)
ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "docs/RELEASING.md": (
        "runtime-evidence example refs",
    ),
    "docs/PROOF_TOPOLOGY.md": (
        "audit runtime-evidence packets",
    ),
    "mechanics/boundary-bridge/README.md": (
        "runtime-evidence schema refs",
    ),
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md": (
        "runtime-evidence schema",
    ),
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json": (
        "runtime-evidence schema refs",
    ),
    "mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json": (
        "runtime-evidence bridge",
    ),
    "mechanics/audit/parts/README.md": (
        "# Runtime Evidence Parts",
        "`runtime-evidence` mechanic",
    ),
    "mechanics/titan/README.md": (
        "This package routes Titan canary work",
    ),
    "mechanics/titan/parts/README.md": (
        "# Titan Canaries Parts",
        "Titan-canary-owned",
    ),
    "reports/README.md": (
        "Proof-release reports",
    ),
}
MECHANIC_PARENT_ALLOWLIST_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Allowlist",
    "no invented parent packages",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "AoA-aligned",
    "evals-native",
    "validator allowlist",
    "Active parents are active, not merely plausible candidates",
)
PROOF_OBJECT_MECHANIC_README_NAME = "mechanics/proof-object/README.md"
PROOF_OBJECT_MECHANIC_AGENTS_NAME = "mechanics/proof-object/AGENTS.md"
PROOF_OBJECT_MECHANIC_PARTS_NAME = "mechanics/proof-object/PARTS.md"
PROOF_OBJECT_MECHANIC_PROVENANCE_NAME = "mechanics/proof-object/PROVENANCE.md"
PROOF_OBJECT_PARTS_README_NAME = "mechanics/proof-object/parts/README.md"
PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-authoring/README.md"
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-contracts/README.md"
)
PROOF_OBJECT_CONTRACT_PART_DECISION_NAME = (
    "docs/decisions/0048-proof-object-contract-parts.md"
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/0069-proof-object-part-owner-split-contract.md"
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME = (
    "docs/decisions/0105-proof-object-eval-part-names.md"
)
PROOF_LOOP_MECHANIC_README_NAME = "mechanics/proof-loop/README.md"
PROOF_LOOP_MECHANIC_AGENTS_NAME = "mechanics/proof-loop/AGENTS.md"
PROOF_LOOP_MECHANIC_PARTS_NAME = "mechanics/proof-loop/PARTS.md"
PROOF_LOOP_MECHANIC_PROVENANCE_NAME = "mechanics/proof-loop/PROVENANCE.md"
PROOF_LOOP_LEGACY_INDEX_NAME = "mechanics/proof-loop/legacy/INDEX.md"
PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/proof-loop/legacy/DISTILLATION_LOG.md"
)
PROOF_LOOP_LEGACY_RAW_README_NAME = "mechanics/proof-loop/legacy/raw/README.md"
PROOF_LOOP_PARTS_README_NAME = "mechanics/proof-loop/parts/README.md"
PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME = (
    "mechanics/proof-loop/parts/route-smoke/README.md"
)
PROOF_LOOP_SMOKE_REPORT_NAME = (
    "mechanics/proof-loop/parts/route-smoke/reports/"
    "proof-loop-local-route-smoke-v1.md"
)
PROOF_LOOP_SMOKE_DECISION_NAME = "docs/decisions/0020-proof-loop-local-smoke-report.md"
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME = (
    "docs/decisions/0030-proof-loop-route-smoke-part.md"
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME = (
    "docs/decisions/0060-proof-loop-route-smoke-contract.md"
)
PROOF_LOOP_LOCAL_REPORT_NAME = (
    "evals/workflow/aoa-verification-honesty/reports/"
    "aoa-evals-slice-19-lifecycle-contract.report.json"
)
PROOF_LOOP_LOCAL_REPORT_DECISION_NAME = (
    "docs/decisions/0022-proof-loop-bundle-local-report.md"
)
RECEIPT_INTAKE_DRY_REVIEW_NAME = (
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json"
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME = (
    "docs/decisions/0024-receipt-intake-dry-review.md"
)
RELEASE_SUPPORT_READINESS_AUDIT_NAME = (
    "mechanics/release-support/parts/readiness-audit/reports/"
    "release-support-readiness-audit-v1.json"
)
RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME = (
    "docs/decisions/0025-release-support-readiness-audit.md"
)
STRATEGIC_CLOSEOUT_AUDIT_NAME = (
    "mechanics/release-support/parts/strategic-closeout/reports/"
    "strategic-closeout-audit-v1.json"
)
STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME = (
    "docs/decisions/0026-strategic-closeout-audit.md"
)
RELEASE_PREP_PR_HANDOFF_NAME = (
    "mechanics/release-support/parts/pr-handoff/reports/"
    "release-prep-pr-handoff-v1.json"
)
RELEASE_PREP_PR_HANDOFF_DECISION_NAME = (
    "docs/decisions/0027-release-prep-pr-handoff.md"
)
REPO_VALIDATION_WORKFLOW_NAME = ".github/workflows/repo-validation.yml"
REPO_VALIDATION_AOA_MEMO_REF = "97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f"
REPO_VALIDATION_AOA_MEMO_PIN_DECISION_NAME = (
    "docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md"
)
COMPARISON_SPINE_MECHANIC_README_NAME = "mechanics/comparison-spine/README.md"
COMPARISON_SPINE_MECHANIC_AGENTS_NAME = "mechanics/comparison-spine/AGENTS.md"
COMPARISON_SPINE_MECHANIC_PARTS_NAME = "mechanics/comparison-spine/PARTS.md"
COMPARISON_SPINE_PARTS_README_NAME = "mechanics/comparison-spine/parts/README.md"
COMPARISON_SPINE_OVERVIEW_PART_README_NAME = (
    "mechanics/comparison-spine/parts/spine-overview/README.md"
)
COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/README.md"
)
COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/README.md"
)
COMPARISON_SPINE_OVERVIEW_REPORT_NAME = (
    "mechanics/comparison-spine/parts/spine-overview/reports/"
    "comparison-spine-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/reports/"
    "same-task-baseline-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/fixtures/"
    "frozen-same-task-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v1.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v2.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v2/README.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v2.md"
)
COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "stress-recovery-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/fixtures/"
    "repeated-window-bounded-v1/README.md"
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_NAME = (
    "docs/decisions/0029-comparison-spine-report-parts.md"
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_NAME = (
    "docs/decisions/0040-comparison-spine-fixture-parts.md"
)
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0059-comparison-spine-part-contract-guard.md"
)
COMPARISON_SPINE_PROVENANCE_NAME = "mechanics/comparison-spine/PROVENANCE.md"
COMPARISON_SPINE_LEGACY_INDEX_NAME = "mechanics/comparison-spine/legacy/INDEX.md"
PROOF_INFRA_MECHANIC_README_NAME = "mechanics/proof-infra/README.md"
PROOF_INFRA_MECHANIC_AGENTS_NAME = "mechanics/proof-infra/AGENTS.md"
PROOF_INFRA_MECHANIC_PARTS_NAME = "mechanics/proof-infra/PARTS.md"
PROOF_INFRA_FIXTURE_FAMILIES_README_NAME = (
    "mechanics/proof-infra/parts/fixture-families/README.md"
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME = (
    "mechanics/proof-infra/parts/fixture-families/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/README.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/AGENTS.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py"
)
FIXTURE_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json"
)
RUNNER_CONTRACT_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json"
)
REPORT_SUMMARY_SCHEMA_NAME = (
    "mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json"
)
PROOF_INFRA_PROVENANCE_NAME = "mechanics/proof-infra/PROVENANCE.md"
PROOF_INFRA_LEGACY_INDEX_NAME = "mechanics/proof-infra/legacy/INDEX.md"
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME = (
    "docs/decisions/0041-proof-infra-fixture-families.md"
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME = (
    "docs/decisions/0049-proof-infra-reportable-contracts.md"
)
PUBLICATION_RECEIPTS_MECHANIC_README_NAME = "mechanics/publication-receipts/README.md"
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_NAME = "mechanics/publication-receipts/AGENTS.md"
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME = "mechanics/publication-receipts/PROVENANCE.md"
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME = (
    "mechanics/publication-receipts/parts/receipt-payload/README.md"
)
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME = (
    "mechanics/publication-receipts/parts/stats-envelope-mirror/README.md"
)
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME = (
    "mechanics/publication-receipts/parts/live-publisher/README.md"
)
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME = (
    "mechanics/publication-receipts/parts/intake-dry-review/README.md"
)
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0057-publication-receipts-part-contract-guard.md"
)
PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME = "mechanics/publication-receipts/legacy/INDEX.md"
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/publication-receipts/legacy/DISTILLATION_LOG.md"
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME = (
    "mechanics/publication-receipts/legacy/raw/README.md"
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
    "docs/decisions/0058-release-support-part-contract-guard.md"
)
RELEASE_SUPPORT_LEGACY_INDEX_NAME = "mechanics/release-support/legacy/INDEX.md"
RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/release-support/legacy/DISTILLATION_LOG.md"
)
RELEASE_SUPPORT_LEGACY_RAW_README_NAME = "mechanics/release-support/legacy/raw/README.md"
TITAN_MECHANIC_README_NAME = "mechanics/titan/README.md"
TITAN_MECHANIC_AGENTS_NAME = "mechanics/titan/AGENTS.md"
TITAN_MECHANIC_DIRECTION_NAME = "mechanics/titan/DIRECTION.md"
TITAN_PARTS_INDEX_README_NAME = "mechanics/titan/parts/README.md"
TITAN_SEED_BOUNDARY_PART_README_NAME = "mechanics/titan/parts/seed-boundary/README.md"
TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME = "mechanics/titan/parts/seed-boundary/seeds"
TITAN_SEED_BOUNDARY_SEEDS_README_NAME = "mechanics/titan/parts/seed-boundary/seeds/README.md"
TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME = "mechanics/titan/parts/seed-boundary/seeds/AGENTS.md"
TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME = (
    "docs/decisions/0055-titan-seed-boundary-contract.md"
)
AGON_MECHANIC_README_NAME = "mechanics/agon/README.md"
AGON_MECHANIC_AGENTS_NAME = "mechanics/agon/AGENTS.md"
AGON_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0054-agon-part-contract-guard.md"
)
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
RECURRENCE_MECHANIC_DECISION_NAME = "docs/decisions/0031-recurrence-mechanic-package.md"
RECURRENCE_SUPPORT_PARTS_DECISION_NAME = (
    "docs/decisions/0039-recurrence-support-parts-expansion.md"
)
RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_NAME = (
    "docs/decisions/0042-recurrence-portable-proof-beacons-part.md"
)
RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME = (
    "docs/decisions/0066-recurrence-control-plane-contract.md"
)
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
CHECKPOINT_MECHANIC_DECISION_NAME = "docs/decisions/0032-checkpoint-mechanic-package.md"
CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0062-checkpoint-part-contract-guard.md"
)
EXPERIENCE_MECHANIC_README_NAME = "mechanics/experience/README.md"
EXPERIENCE_MECHANIC_AGENTS_NAME = "mechanics/experience/AGENTS.md"
EXPERIENCE_MECHANIC_PARTS_NAME = "mechanics/experience/PARTS.md"
EXPERIENCE_MECHANIC_PROVENANCE_NAME = "mechanics/experience/PROVENANCE.md"
EXPERIENCE_PROTOCOL_PART_README_NAME = (
    "mechanics/experience/parts/protocol-integrity/README.md"
)
EXPERIENCE_CERTIFICATION_PART_README_NAME = (
    "mechanics/experience/parts/certification-gate/README.md"
)
EXPERIENCE_ADOPTION_PART_README_NAME = (
    "mechanics/experience/parts/adoption-federation/README.md"
)
EXPERIENCE_GOVERNANCE_PART_README_NAME = (
    "mechanics/experience/parts/governance-runtime-boundary/README.md"
)
EXPERIENCE_OFFICE_PART_README_NAME = (
    "mechanics/experience/parts/office-release-train/README.md"
)
EXPERIENCE_MECHANIC_DECISION_NAME = "docs/decisions/0033-experience-mechanic-package.md"
EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME = (
    "docs/decisions/0043-experience-verdict-residue-parts.md"
)
EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0063-experience-part-contract-guard.md"
)
ANTIFRAGILITY_MECHANIC_README_NAME = "mechanics/antifragility/README.md"
ANTIFRAGILITY_MECHANIC_AGENTS_NAME = "mechanics/antifragility/AGENTS.md"
ANTIFRAGILITY_MECHANIC_PARTS_NAME = "mechanics/antifragility/PARTS.md"
ANTIFRAGILITY_PARTS_README_NAME = "mechanics/antifragility/parts/README.md"
ANTIFRAGILITY_MECHANIC_PROVENANCE_NAME = "mechanics/antifragility/PROVENANCE.md"
ANTIFRAGILITY_POSTURE_PART_README_NAME = (
    "mechanics/antifragility/parts/posture-review/README.md"
)
ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME = (
    "mechanics/antifragility/parts/stress-recovery-window/README.md"
)
ANTIFRAGILITY_STRESS_WINDOW_DOC_NAME = (
    "mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md"
)
ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME = (
    "mechanics/antifragility/parts/repair-proof/README.md"
)
ANTIFRAGILITY_MECHANIC_DECISION_NAME = (
    "docs/decisions/0034-antifragility-mechanic-package.md"
)
ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0061-antifragility-part-contract-guard.md"
)
METHOD_GROWTH_MECHANIC_README_NAME = "mechanics/method-growth/README.md"
METHOD_GROWTH_MECHANIC_AGENTS_NAME = "mechanics/method-growth/AGENTS.md"
METHOD_GROWTH_MECHANIC_PARTS_NAME = "mechanics/method-growth/PARTS.md"
METHOD_GROWTH_MECHANIC_PROVENANCE_NAME = "mechanics/method-growth/PROVENANCE.md"
METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME = (
    "mechanics/method-growth/parts/candidate-lineage/README.md"
)
METHOD_GROWTH_OWNER_LANDING_PART_README_NAME = (
    "mechanics/method-growth/parts/owner-landing/README.md"
)
METHOD_GROWTH_MECHANIC_DECISION_NAME = (
    "docs/decisions/0035-method-growth-mechanic-package.md"
)
METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/0068-method-growth-part-owner-split-contract.md"
)
RPG_MECHANIC_README_NAME = "mechanics/rpg/README.md"
RPG_MECHANIC_AGENTS_NAME = "mechanics/rpg/AGENTS.md"
RPG_MECHANIC_PARTS_NAME = "mechanics/rpg/PARTS.md"
RPG_MECHANIC_PROVENANCE_NAME = "mechanics/rpg/PROVENANCE.md"
RPG_PROGRESS_UNLOCKS_PART_README_NAME = (
    "mechanics/rpg/parts/progression-unlocks/README.md"
)
RPG_MECHANIC_DECISION_NAME = "docs/decisions/0036-rpg-mechanic-package.md"
RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME = (
    "docs/decisions/0067-rpg-progression-unlocks-contract.md"
)
GROWTH_CYCLE_MECHANIC_README_NAME = "mechanics/growth-cycle/README.md"
GROWTH_CYCLE_MECHANIC_AGENTS_NAME = "mechanics/growth-cycle/AGENTS.md"
GROWTH_CYCLE_MECHANIC_PARTS_NAME = "mechanics/growth-cycle/PARTS.md"
GROWTH_CYCLE_PARTS_README_NAME = "mechanics/growth-cycle/parts/README.md"
GROWTH_CYCLE_MECHANIC_PROVENANCE_NAME = "mechanics/growth-cycle/PROVENANCE.md"
GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME = (
    "mechanics/growth-cycle/parts/diagnosis-gate/README.md"
)
GROWTH_CYCLE_MECHANIC_DECISION_NAME = (
    "docs/decisions/0037-growth-cycle-mechanic-package.md"
)
GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME = (
    "docs/decisions/0065-growth-cycle-diagnosis-gate-contract.md"
)
REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME = (
    "docs/decisions/0099-repair-diagnosis-route-boundary.md"
)
DISTILLATION_MECHANIC_README_NAME = "mechanics/distillation/README.md"
DISTILLATION_MECHANIC_AGENTS_NAME = "mechanics/distillation/AGENTS.md"
DISTILLATION_MECHANIC_PARTS_NAME = "mechanics/distillation/PARTS.md"
DISTILLATION_MECHANIC_PROVENANCE_NAME = "mechanics/distillation/PROVENANCE.md"
DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME = (
    "mechanics/distillation/parts/compost-provenance/README.md"
)
DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME = (
    "mechanics/distillation/parts/runtime-candidate-adoption/README.md"
)
DISTILLATION_MECHANIC_DECISION_NAME = (
    "docs/decisions/0038-distillation-mechanic-package.md"
)
DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0064-distillation-part-contract-guard.md"
)
QUESTBOOK_MECHANIC_README_NAME = "mechanics/questbook/README.md"
QUESTBOOK_MECHANIC_AGENTS_NAME = "mechanics/questbook/AGENTS.md"
QUESTBOOK_MECHANIC_PARTS_NAME = "mechanics/questbook/PARTS.md"
QUESTBOOK_MECHANIC_PROVENANCE_NAME = "mechanics/questbook/PROVENANCE.md"
QUESTBOOK_SOURCE_RECORD_PART_README_NAME = (
    "mechanics/questbook/parts/source-record-contract/README.md"
)
QUESTBOOK_DISPATCH_READER_PART_README_NAME = (
    "mechanics/questbook/parts/dispatch-reader/README.md"
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/0070-questbook-part-owner-split-contract.md"
)
AUDIT_MECHANIC_README_NAME = "mechanics/audit/README.md"
AUDIT_MECHANIC_AGENTS_NAME = "mechanics/audit/AGENTS.md"
AUDIT_MECHANIC_PROVENANCE_NAME = "mechanics/audit/PROVENANCE.md"
AUDIT_PARTS_README_NAME = "mechanics/audit/parts/README.md"
AUDIT_LEGACY_INDEX_NAME = "mechanics/audit/legacy/INDEX.md"
AUDIT_LEGACY_DISTILLATION_LOG_NAME = "mechanics/audit/legacy/DISTILLATION_LOG.md"
AUDIT_LEGACY_RAW_README_NAME = "mechanics/audit/legacy/raw/README.md"
AUDIT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0053-audit-part-contract-guard.md"
)
AUDIT_SELECTED_EVIDENCE_PART_README_NAME = (
    "mechanics/audit/parts/selected-evidence-packets/README.md"
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME = (
    "mechanics/audit/parts/artifact-verdict-hooks/README.md"
)
AUDIT_CANDIDATE_READERS_PART_README_NAME = (
    "mechanics/audit/parts/candidate-readers/README.md"
)
AUDIT_INTEGRITY_REVIEW_PART_README_NAME = (
    "mechanics/audit/parts/integrity-review/README.md"
)
BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_NAME = "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md"
BOUNDARY_BRIDGE_MECHANIC_README_NAME = "mechanics/boundary-bridge/README.md"
BOUNDARY_BRIDGE_MECHANIC_AGENTS_NAME = "mechanics/boundary-bridge/AGENTS.md"
BOUNDARY_BRIDGE_MECHANIC_PARTS_NAME = "mechanics/boundary-bridge/PARTS.md"
BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_NAME = "mechanics/boundary-bridge/PROVENANCE.md"
BOUNDARY_BRIDGE_LEGACY_INDEX_NAME = "mechanics/boundary-bridge/legacy/INDEX.md"
BOUNDARY_BRIDGE_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/boundary-bridge/legacy/DISTILLATION_LOG.md"
)
BOUNDARY_BRIDGE_LEGACY_RAW_README_NAME = (
    "mechanics/boundary-bridge/legacy/raw/README.md"
)
BOUNDARY_BRIDGE_PARTS_README_NAME = "mechanics/boundary-bridge/parts/README.md"
BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/compatibility-map/README.md"
)
BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md"
)
BOUNDARY_BRIDGE_ORCHESTRATOR_PROOF_ANCHORS_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md"
)
BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/0056-boundary-bridge-part-contract-guard.md"
)
SIBLING_CANARY_MATRIX_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/"
    "sibling_canary_matrix.json"
)
SIBLING_CANARY_RUNNER_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/"
    "run_sibling_canary.py"
)
SIBLING_CANARY_COMMAND = (
    f"python {SIBLING_CANARY_RUNNER_NAME} --repo-root . --format json"
)
SIBLING_CANARY_EXPLICIT_MATRIX_COMMAND = (
    f"python {SIBLING_CANARY_RUNNER_NAME} --repo-root . --matrix {SIBLING_CANARY_MATRIX_NAME}"
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
    "docs/PROOF_TOPOLOGY.md",
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
PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "proof-object completeness review",
    "bundle-local review",
    "Source eval packages stay under `evals/`",
    "python scripts/build_catalog.py --check",
    "AGENTS.md#validation",
)
PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source proof objects",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "EVAL.md and eval.yaml",
    "eval-local support artifacts",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "eval-authoring",
    "eval-contracts",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "Source eval packages stay under `evals/`",
    "AGENTS.md#validation",
)
PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for proof-object authoring and contract support parts",
    "source eval bundle for proof meaning",
    "source `evals/**/EVAL.md` and `evals/**/eval.yaml`",
    "## Part Admission Route",
    "`eval-authoring/`",
    "`eval-contracts/`",
    "stronger-owner split",
    "mechanics/proof-object/AGENTS.md#validation",
    "generated-reader check",
    "generated-reader freshness checks",
)
PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS = (
    "They do not own source eval meaning and do not replace generated readers",
)
PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS = (
    "Eval Authoring",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "actual source proof",
    "template",
    "doctrine or accepted proof meaning",
    "sibling refs outrank source eval packages",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS = (
    "Eval Contracts",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "schema-backed contract validation",
    "claim invention",
    "schema acceptance reads as eval-local review",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "proof-object completeness review",
    "does not move `evals/`",
    "generated readers",
    "bundle-local review",
)
PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/",
    "source bundles stay under `evals/`",
    "generated readers stay",
    "python scripts/validate_repo.py",
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Proof-object Part Owner-split Contract",
    "mechanics/proof-object/parts/eval-authoring/README.md",
    "mechanics/proof-object/parts/eval-contracts/README.md",
    "`## Stronger Owner Split`",
    "source proof object remains",
    "Source proof bundle meaning stays under `evals/`",
    "generated readers, reports, receipts, runtime candidates, sibling refs, quests",
    "Schema acceptance may prove metadata shape",
    "python -m pytest -q tests/test_validate_repo.py -k proof_object_part_owner_split",
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS = (
    "Proof-object Eval Part Names",
    "bundle-authoring",
    "eval-authoring",
    "bundle-contracts",
    "eval-contracts",
    "active directory topology",
    "source eval packages into mechanics",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Step Owners",
    "EVAL_SELECTION.md",
    "mechanics/proof-object/",
    "mechanics/proof-infra/",
    "mechanics/audit/",
    "mechanics/publication-receipts/",
    "mechanics/boundary-bridge/",
    "PARTS.md",
    "route-smoke",
    "generated readers remain derived readers below bundle-local proof authority",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "active proof-loop route",
    "source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Keep generated readers subordinate",
    "Keep receipts below reviewed reports",
    "mechanics/proof-loop/PARTS.md",
    "Keep route-smoke reports",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-loop/",
    "pick proof question",
    "existing mechanics",
    "does not own bundle meaning",
    "does not create runtime dispatch",
    "does not allow receipts",
)
PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS = (
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "docs/decisions/0020-proof-loop-local-smoke-report.md",
    "docs/decisions/0030-proof-loop-route-smoke-part.md",
    "Former root report paths are provenance only",
)
PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-loop",
    "route-smoke",
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "Do not create new proof-loop work in legacy",
)
PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active proof-loop",
)
PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS = (
    "bounded route-smoke",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "aoa-verification-honesty",
    "no eval result receipt",
    "no bundle promotion",
    "defer/handoff",
    "No runtime candidate packet is accepted by this smoke",
    "No sibling proof ref is required by this smoke",
)
PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "aoa-verification-honesty",
    "bounded route-smoke",
    "no eval result receipt",
    "no bundle promotion",
    "no runtime dispatch",
    "no sibling-owner approval",
)
PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "Proof Loop / Part Index",
    "proof question -> selection route -> source proof object",
    "route-smoke",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "not standalone mechanics",
    "no eval result receipt",
)
PROOF_LOOP_PARTS_README_REQUIRED_TOKENS = (
    "Proof Loop / Parts Route",
    "## Operating Card",
    "| role | lower index for active proof-loop part artifacts |",
    "## Active Parts",
    "route-smoke/README.md",
    "## Owner Pressure Routes",
    "| source proof object meaning | `mechanics/proof-object/` plus affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |",
    "| support contract pressure | `mechanics/proof-infra/` |",
    "| candidate evidence packet | `mechanics/audit/` |",
    "| receipt publication or receipt-intake pressure | `mechanics/publication-receipts/` |",
    "## Part Admission Route",
    "| one local loop path needs public-safe routeability proof | bounded route-smoke report with no receipt publication | `route-smoke/README.md` |",
    "mechanics/proof-loop/parts/AGENTS.md#validation",
)
PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS = (
    "Route Smoke Part",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "bounded route-smoke report artifact",
    "no eval result receipt",
    "route-smoke report read as eval-result run",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "route-smoke",
    "root `reports/`",
    "mechanics/proof-loop/PARTS.md",
    "does not create an eval result receipt",
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Proof Loop Route-Smoke Contract",
    "mechanics/proof-loop/parts/route-smoke/README.md",
    "part-level contract",
    "stronger owner split",
    "stop-lines",
    "no eval result receipt",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS = (
    "aoa-verification-honesty",
    "aoa-evals slice 19 quest lifecycle contract",
    "No receipt publisher run was attempted",
    "No runtime mutation or machine maintenance check was attempted",
    "`python scripts/release_check.py`",
)
PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_LOCAL_REPORT_NAME,
    "bundle-local report",
    "reports/summary.schema.json",
    "validate every bundle-local `*.report.json`",
    "no eval result receipt",
    "no bundle status is promoted",
)
RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS = (
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "eval-result-receipt.schema.json",
    "stats-event-envelope.schema.json",
    "publish_live_receipts.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "dry_review_only",
    "not_published",
    "not_created",
    "not_attempted",
    "publication pressure routes to a receipt envelope",
    "runtime acceptance pressure",
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS = (
    RECEIPT_INTAKE_DRY_REVIEW_NAME,
    "eval_result_receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "candidate_payload_preview",
    "event_id",
    "dry review is weaker than a receipt",
    "Do not infer that an eval result receipt was published",
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
REPO_VALIDATION_AOA_MEMO_PIN_DECISION_REQUIRED_TOKENS = (
    REPO_VALIDATION_WORKFLOW_NAME,
    REPO_VALIDATION_AOA_MEMO_REF,
    "pinned CI-lane update",
    "latest-sibling canary",
    "GitHub `Repo Validation`",
    "does not mutate `aoa-memo`",
    "does not weaken path validation",
)
COMPARISON_SPINE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/COMPARISON_SPINE_GUIDE.md",
    "docs/BASELINE_COMPARISON_GUIDE.md",
    "docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
    "generated/comparison_spine.json",
    "mechanics/comparison-spine/PARTS.md",
    COMPARISON_SPINE_OVERVIEW_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME,
    COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME,
    COMPARISON_SPINE_PROVENANCE_NAME,
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "style-only movement",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "baseline_mode",
    "comparison_surface",
    "fixtures/contract.json",
    "generated/comparison_spine.json",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/",
    "generated/comparison_spine.json",
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "pressure-to-route maps",
)
COMPARISON_SPINE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "Parts carry comparison-spine fixture and readout surfaces",
    "Source claim meaning stays in `evals/**/EVAL.md`",
    "fixture and readout surfaces",
    "| repo-global score or broad growth proof | source bundle review plus `longitudinal-window` evidence and growth/progression owner route |",
)
COMPARISON_SPINE_PARTS_README_REQUIRED_TOKENS = (
    "spine-overview/",
    "fixed-baseline/",
    "peer-compare/",
    "longitudinal-window/",
    "AGENTS.md#validation",
)
COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_OVERVIEW_PART_REQUIRED_TOKENS = (
    "comparison-spine-proof-flow-v1.md",
    "cross-mode",
    "generated/comparison_spine.json",
    "| overview dossier as comparison result | source bundle comparison surface plus mode-specific part report |",
    "| fixed-baseline, peer-compare, and longitudinal-window collapsed into one score | mode-specific part route plus bundle-local review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_FIXED_BASELINE_PART_REQUIRED_TOKENS = (
    "frozen-same-task-v1",
    "same-task-baseline-proof-flow-v1.md",
    "fixed-baseline",
    "repo-global score",
    "baseline_target_label",
    "| one fixed-baseline result as repo-global score | source bundle review plus comparison-spine bounded read |",
    "| broad growth from same-task regression evidence | `longitudinal-window` evidence plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PEER_COMPARE_PART_REQUIRED_TOKENS = (
    "bounded-change-paired-v1",
    "bounded-change-paired-v2",
    "artifact-process-paired-proof-flow-v1.md",
    "artifact-process-paired-proof-flow-v2.md",
    "Peer-compare",
    "matched_surface",
    "| peer comparison into fixed-baseline by association | source bundle `baseline_mode` and fixed-baseline part route |",
    "| peer-compare blur as broad capability growth or repo-global score | bounded comparison read plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_LONGITUDINAL_PART_REQUIRED_TOKENS = (
    "repeated-window-bounded-v1",
    "repeated-window-proof-flow-v1.md",
    "repeated-window-proof-flow-v2.md",
    "stress-recovery-window-proof-flow-v1.md",
    "broad growth proof",
    "cross-window invariants",
    "| ordered-window movement as broad growth by association | source bundle claim plus growth/progression owner review |",
    "| repeated-window or stress-recovery evidence as runtime health or antifragility acceptance | `abyss-stack` runtime route or `mechanics/antifragility/` owner route |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Comparison Spine Part Contract Guard",
    "mechanics/comparison-spine/parts/spine-overview/README.md",
    "mechanics/comparison-spine/parts/fixed-baseline/README.md",
    "mechanics/comparison-spine/parts/peer-compare/README.md",
    "mechanics/comparison-spine/parts/longitudinal-window/README.md",
    "part-level contracts",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "stronger owner split",
    "stop-lines",
    "broad growth",
    "pressure-to-owner routes",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/parts/",
    "paired_readout_path",
    "generated `proof_artifacts`",
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "does not make a shared dossier stronger than the source proof object",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_REQUIRED_TOKENS = (
    "fixed-baseline/fixtures/frozen-same-task-v1/",
    "peer-compare/fixtures/bounded-change-paired-v1/",
    "peer-compare/fixtures/bounded-change-paired-v2/",
    "longitudinal-window/fixtures/repeated-window-bounded-v1/",
    "Bundle source truth stays in `evals/**/EVAL.md`",
    "does not make a fixture family stronger than the source proof object",
    "mechanics/comparison-spine/PROVENANCE.md",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
COMPARISON_SPINE_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/frozen-same-task-v1/",
    "fixtures/bounded-change-paired-v1/",
    "fixtures/bounded-change-paired-v2/",
    "fixtures/repeated-window-bounded-v1/",
    "active fixed-baseline fixture family",
    "active peer-compare fixture family",
    "active longitudinal-window fixture family",
)
PROOF_INFRA_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/SHARED_PROOF_INFRA_GUIDE.md",
    "fixtures/README.md",
    PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
    PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME,
    FIXTURE_CONTRACT_SCHEMA_NAME,
    RUNNER_CONTRACT_SCHEMA_NAME,
    REPORT_SUMMARY_SCHEMA_NAME,
    "reports/README.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "generated catalog `proof_artifacts`",
    "shared_fixture_family_path",
    "mechanics/proof-infra/parts/fixture-families/fixtures/",
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "report_schema_path",
    "root infrastructure districts stay route-card districts unless a part-local owner exists",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "shared proof infrastructure",
    "fixtures/contract.json",
    "runners/contract.json",
    "reports/summary.schema.json",
    "generated catalog `proof_artifacts`",
    "bundle-local interpretation",
    "parts/fixture-families/fixtures/",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "fixture-families",
    "reportable-contracts",
    "bundle support need",
    "shared_fixture_family_path",
    "runner_surface_path",
    "Fixture-family parent pressure",
    "Boundary Routes",
    "AGENTS.md#validation",
)
PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS = (
    "bundle support need",
    "public-safe reusable family",
    "shared_fixture_family_path",
    "ambiguity-bounded-v1",
    "verification-honesty-v1",
    "witness-trace-v1",
    "Family-name parent pressure",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "generic shared fixture-family support",
    "public-safe reusable support",
    "bundle-local `EVAL.md`",
    "evals/**/fixtures/contract.json",
    "shared_fixture_family_path",
    "Family-name parent pressure",
    "centralized-child-validation",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS = (
    "bundle-local runner contract",
    "reportable proof contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "fixture-contract.schema.json",
    "runner-contract.schema.json",
    "report-summary.schema.json",
    "`evals/<family>/<eval>/EVAL.md`",
    "tests/test_bounded_rubric_breakdown.py",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "reportable-contracts",
    "bundle-local runner contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "Schema weakening pressure",
    "Root alias pressure",
    "centralized-child-validation",
    "bounded rubric scorer test",
)
PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES = (
    "It does not own bundle meaning",
    "It does not own bundle-local meaning",
    "Keep the family weaker than the bundle-local claim",
    "Keep the shared runner surface weaker than bundle-local interpretation",
    "Do not add hidden benchmark cases",
    "Do not add hidden harness logic",
    "Do not recreate active root aliases",
)
PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/ambiguity-bounded-v1/README.md",
    "fixtures/verification-honesty-v1/README.md",
    "mechanics/proof-infra/parts/fixture-families/fixtures",
    "runners/reportable_proof_contract.md",
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
    "scorers/bounded_rubric_breakdown.py",
    "schemas/runner-contract.schema.json",
    "Former root paths are provenance only",
)
PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/",
    "shared proof contract",
    "generated proof_artifacts",
    "Decision 0041",
    "Decision 0049",
    "bundle-local `EVAL.md`",
    "schema weakening",
    "repo-global scoring",
)
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/fixture-families/",
    "generic shared fixture families",
    "no narrower active mechanic",
    "Root `fixtures/` remains a compatibility route card",
    "does not make fixture families stronger than bundle-local meaning",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "root `runners/`, `scorers/`, and `schemas/` remain compatibility route cards",
    "does not make reportable contracts stronger than bundle-local meaning",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py",
    "mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "eval_result_receipt",
    "stats-event-envelope",
    "optional receipt",
    "bundle-local verdict meaning",
    "repo-global score",
    "python scripts/validate_repo.py",
    "python scripts/validate_semantic_agents.py",
)


def validate_proof_object_parts_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_PARTS_README_NAME,
        tokens=PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for forbidden_token in PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        PROOF_OBJECT_PARTS_README_NAME,
                        "proof-object parts route should use a positive operating card",
                    )
                )
    return issues
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "eval-result receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "bundle-local report",
    "aoa-stats",
    "append-only",
    "public-safe",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/publication-receipts/",
    "eval-result receipt",
    "stats-event-envelope",
    "aoa-stats",
    "does not move `.aoa/live_receipts/`",
    "bundle-local report",
    "repo-global score",
)
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PUBLICATION_RECEIPTS_LEGACY_INDEX_REQUIRED_TOKENS = (
    "docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "reports/eval-result-receipt-intake-dry-review-v1.json",
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
)
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "publication-receipts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "Do not create new publication receipt work in legacy",
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active publication-receipts",
)
PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_REQUIRED_TOKENS = (
    "Receipt Payload Part",
    "eval_result_receipt",
    "schemas/eval-result-receipt.schema.json",
    "examples/eval_result_receipt.example.json",
    "reviewed bounded report",
    "source bundle",
    "The payload is a publication sidecar",
    "schema-valid payload reads as a published receipt",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_REQUIRED_TOKENS = (
    "Stats Envelope Mirror Part",
    "schemas/stats-event-envelope.schema.json",
    "canonical `aoa-stats`",
    "event-kind vocabulary",
    "owner-local live receipt log",
    "dry-review artifacts",
    "mirror edit reads as canonical `aoa-stats` schema work",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_REQUIRED_TOKENS = (
    "Live Publisher Part",
    "scripts/publish_live_receipts.py",
    "tests/test_publish_live_receipts.py",
    "tests/test_live_receipt_log.py",
    "append-only JSONL writes",
    "duplicate `event_id` skips",
    "dry-review payload preview looks publishable",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_REQUIRED_TOKENS = (
    "Intake Dry Review Part",
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "`receipt_status` stays",
    "`not_published`",
    "top-level `event_kind`, `event_id`, `observed_at`, `object_ref`,",
    "`.aoa/live_receipts/` append appears",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Publication Receipts Part Contract Guard",
    "mechanics/publication-receipts/parts/receipt-payload/README.md",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/README.md",
    "mechanics/publication-receipts/parts/live-publisher/README.md",
    "mechanics/publication-receipts/parts/intake-dry-review/README.md",
    "part-level contracts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "stronger owner split",
    "stop-lines",
    "not_published",
    "python scripts/validate_repo.py",
)
RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "PARTS.md",
    "docs/RELEASING.md",
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
    "python scripts/validate_repo.py",
    "python scripts/validate_semantic_agents.py",
    "python scripts/release_check.py",
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
    "docs/RELEASING.md",
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
    "python scripts/validate_repo.py",
    "python scripts/release_check.py",
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
    "docs/decisions/0014-release-support-mechanic-package.md",
)
RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-release",
    "release-support",
    "readiness-audit",
    "strategic-closeout",
    "pr-handoff",
    "Do not create new release-support work in legacy",
)
RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)
TITAN_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "mechanics/titan/parts/seed-boundary/seeds/AGENTS.md",
    "validate_titan_canary_surfaces",
    "seed canary",
    "aoa-agents",
    "future executable scorer",
    "full incarnation proof",
    "hidden arena",
    "mutation gate",
    "judgment gate",
    "python scripts/validate_repo.py",
)
TITAN_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Titan seed canaries",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed-boundary evidence only",
    "mutation gate",
    "judgment gate",
    "validate_titan_canary_surfaces",
    "python scripts/validate_repo.py",
)
TITAN_MECHANIC_DIRECTION_REQUIRED_TOKENS = (
    "aoa-agents",
    "Titan role classes",
    "bearer identity",
    "summon boundary law",
    "incarnation posture",
    "seed-boundary",
    "seed-boundary evidence",
)
TITAN_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/titan/",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "validate_titan_canary_surfaces",
    "moves the seed YAML files",
    "full incarnation proof",
    "future executable scorer",
    "owner-named evals-native",
    "aoa-agents",
)
TITAN_INCARNATION_CANARIES_REQUIRED_TOKENS = (
    "mechanics/titan/README.md",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed canaries",
    "full incarnation proof",
    "runtime cohort",
    "summon authority",
    "memory sovereignty",
    "AGENTS.md#validation",
)
TITAN_SUMMON_DISCIPLINE_REQUIRED_TOKENS = (
    "mechanics/titan/README.md",
    "seed-defined",
    "named Titan targets",
    "generic role",
    "hidden background arena",
    "full incarnation",
)
TITAN_SEED_BOUNDARY_SEEDS_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "Titan seed canaries",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed-local route card",
    "full incarnation proof",
    "runtime activation",
    "validate_titan_canary_surfaces",
    "Filename or identifier drift",
    "centralized-child-validation",
)
TITAN_SEED_BOUNDARY_SEEDS_README_REQUIRED_TOKENS = (
    "Titan Canary Seeds",
    "mechanics/titan/parts/seed-boundary/seeds/",
    "titan*.yaml",
    "seed-defined",
    "id` or `eval_id",
    "full incarnation proof",
    "Use [AGENTS.md](AGENTS.md#validation)",
    "parent `mechanics/titan/parts/AGENTS.md` lane",
)
TITAN_SEED_BOUNDARY_PART_README_REQUIRED_TOKENS = (
    "Seed Boundary Part",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "validate_titan_canary_surfaces",
    "aoa-agents",
    "aoa-memo",
    "runtime activation",
    "summon authority",
    "memory sovereignty",
    "canary presence reads as proof",
    "python scripts/validate_repo.py",
)
TITAN_PARTS_INDEX_README_REQUIRED_TOKENS = (
    "# Titan / Parts Route",
    "## Operating Card",
    "| role | lower index for active Titan proof-seed parts |",
    "## Active Parts",
    "| `seed-boundary/` | seed-defined Titan boundary canary family and seed-local route law | `seed-boundary/README.md` |",
    "## Owner Pressure Routes",
    "| canary presence reads as incarnation, summon authority, or runtime cohort proof | keep the part seed-defined and route stronger claims to Titan/runtime owners |",
    "| canary presence reads as memory sovereignty | route to `aoa-memo` before proof adoption |",
    "| executable scorer-backed proof pressure appears | wait for scorer, fixture, report, and validator contracts |",
    "## Part Admission Route",
    "| seed-defined Titan canary YAML | current source shape and validator lane match the seed-boundary contract | `seed-boundary/README.md` |",
    "mechanics/titan/parts/AGENTS.md#validation",
)
TITAN_SEED_BOUNDARY_ROUTE_SURFACE_NAMES = (
    TITAN_MECHANIC_AGENTS_NAME,
    TITAN_MECHANIC_DIRECTION_NAME,
    "mechanics/titan/PARTS.md",
    TITAN_PARTS_INDEX_README_NAME,
    TITAN_SEED_BOUNDARY_PART_README_NAME,
    "mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
    TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME,
    TITAN_SEED_BOUNDARY_SEEDS_README_NAME,
)
TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES = (
    "not full incarnation proof",
    "not incarnation proof",
    "not full proof by themselves",
    "not named after the canary artifact form",
    "Do not split named Titan",
    "This part is seed-defined only. It does not create",
    "Do not use canary presence as proof",
    "These files are boundary-check seeds, not full eval bundles",
    "These files are seed-defined boundary checks. They are not full eval bundles",
    "Seed canaries are not full incarnation proof",
    "Seed canaries do not activate",
    "Seed canaries do not grant",
    "Seed canaries do not create",
    "Seed canaries do not bypass",
    "They do not grant summon authority",
    "Do not claim full incarnation proof",
    "Do not bypass mutation gate",
    "Do not move canary files",
)
TITAN_SEED_BOUNDARY_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Titan Seed-boundary Contract",
    "mechanics/titan/parts/seed-boundary/README.md",
    "titan-canaries",
    "stronger owner split",
    "stop-lines",
    "aoa-agents",
    "aoa-memo",
    "runtime activation",
    "python scripts/validate_repo.py",
)
AGON_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "PARTS.md",
    "court-prebinding",
    "sophian-threshold-alignment",
    "part-local seed/config/docs",
    "observe-only recurrence hooks",
    "no_live_verdict",
    "bundle-local review",
    "python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check",
    "python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py",
    "python -m pytest -q mechanics/agon/parts/*/tests/test_agon*.py",
    "live verdict",
)
AGON_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Agon proof-alignment loop",
    "part-local source config",
    "generated registry",
    "observe-only recurrence",
    "no_live_verdict",
    "bundle-local review",
)
AGON_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/agon/",
    "mechanics/agon/parts/",
    "seed prebindings",
    "part-local",
    "PARTS.md",
    "live verdict",
    "Tree of Sophia promotion",
)
AGON_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "generated",
    "validator",
)
AGON_PART_README_CONTRACTS = (
    (
        "mechanics/agon/parts/court-prebinding/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_eval_prebinding_registry.min.json",
            "no_live_verdict",
            "no_closure_grant",
        ),
    ),
    (
        "mechanics/agon/parts/ccs-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_ccs_eval_alignment_registry.min.json",
            "CCS law",
            "center law",
        ),
    ),
    (
        "mechanics/agon/parts/vds-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_vds_eval_alignment_registry.min.json",
            "no-live-verdict",
            "live verdict emission or acceptance pressure",
        ),
    ),
    (
        "mechanics/agon/parts/mechanical-trial-suites/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_mechanical_trial_eval_suite_registry.min.json",
            "candidate-only eval-suite",
            "arena run, live protocol, or trial execution pressure",
        ),
    ),
    (
        "mechanics/agon/parts/retention-rank-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_retention_rank_eval_alignment_registry.min.json",
            "retention execution",
            "no-mutation alignment evidence",
        ),
    ),
    (
        "mechanics/agon/parts/epistemic-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_epistemic_eval_alignment_registry.min.json",
            "doctrine rewrite",
            "owner-truth takeover",
        ),
    ),
    (
        "mechanics/agon/parts/slc-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_slc_eval_alignment_registry.min.json",
            "schools, lineages, and campaigns",
            "non-canon alignment",
        ),
    ),
    (
        "mechanics/agon/parts/kag-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_kag_eval_alignment_registry.min.json",
            "KAG canon",
            "KAG candidate promotion",
        ),
    ),
    (
        "mechanics/agon/parts/sophian-threshold-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_sophian_eval_alignment_registry.min.json",
            "Tree of Sophia canon",
            "Tree of Sophia canon write",
        ),
    ),
)
AGON_PART_README_STALE_STOP_LINE_PHRASES = (
    "Do not grant live verdict",
    "Do not weaken `no_live_verdict`",
    "Do not treat generated prebindings as court law",
    "Do not rewrite center law",
    "Do not issue live verdicts",
    "Do not let local registry output outrank",
    "Do not emit or accept a live verdict",
    "Do not turn verdict draft status",
    "Do not let generated draft-status records outrank",
    "Do not run an arena",
    "Do not issue verdicts",
    "Do not use candidate eval-suite output as proof",
    "Do not mutate rank",
    "Do not treat eval alignment as promotion",
    "Do not let generated rank-pressure records outrank",
    "Do not rewrite doctrine",
    "Do not issue live verdict",
    "Do not let generated epistemic records outrank",
    "Do not canonize",
    "Do not treat SLC alignment as owner acceptance",
    "Do not promote a KAG candidate",
    "Do not use generated KAG alignment records as proof",
    "Do not write Tree of Sophia canon",
    "Do not transfer canon authority",
)
AGON_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Agon Part Contract Guard",
    "mechanics/agon/parts/court-prebinding/README.md",
    "mechanics/agon/parts/sophian-threshold-alignment/README.md",
    "part-level contracts",
    "no new Agon parent",
    "stronger owner split",
    "stop-lines",
    "python scripts/validate_repo.py",
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
RECURRENCE_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
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
CHECKPOINT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
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
EXPERIENCE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "experience pressure",
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "evals/boundary/aoa-experience-protocol-integrity/EVAL.md",
    "evals/boundary/aoa-experience-certification-gate-integrity/EVAL.md",
    "runtime distillation candidate adoption",
    "Stronger Owner Split",
    "Stop-Lines",
    "| live workspace runtime or service dispatch pressure | `abyss-stack` runtime route |",
    "| office installation or assistant operational authority pressure | `aoa-agents` and owner operator route |",
    "| operator certification, release approval, deployment approval, or rollout promotion pressure | Agents-of-Abyss, release-support, and owner approval route |",
    "| owner-local adoption, consent, or acceptance pressure | owner repository adoption route |",
    "| memory sovereignty, recall authority, or memo canon pressure | `aoa-memo` memory route |",
    "| live router behavior or routing-layer authorship pressure | `aoa-routing` route-authority lane |",
    "| KAG promotion into owner repositories pressure | `aoa-kag` graph route plus owner adoption route |",
    "| Tree-of-Sophia runtime write or authored-meaning pressure | Tree-of-Sophia authored-meaning route |",
    "| broad Experience success pressure | bundle-local proof object plus source-owner evidence review |",
    "python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py",
)
EXPERIENCE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Experience proof work",
    "mechanics/experience/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create Experience parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
EXPERIENCE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "Continuity-context",
    "| live runtime activation or service dispatch | `abyss-stack` runtime route |",
    "| office installation or assistant operational authority | `aoa-agents` and owner operator route |",
    "| operator certification, release approval, deployment approval, or rollout promotion | Agents-of-Abyss, release-support, and owner approval route |",
    "| owner-local adoption, consent, or acceptance | owner repository adoption route |",
    "| memory canon, recall authority, or memory sovereignty | `aoa-memo` memory route |",
    "| route activation or routing-layer authorship | `aoa-routing` route-authority lane |",
    "| KAG forced adoption into owner repositories | `aoa-kag` graph route plus owner adoption route |",
    "| direct ToS runtime write or ToS-authored meaning | Tree-of-Sophia authored-meaning route |",
    "| broad Experience success | bundle-local proof object plus source-owner evidence review |",
)
EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
EXPERIENCE_PROTOCOL_PART_REQUIRED_TOKENS = (
    "aoa-experience-protocol-integrity",
    "mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/README.md",
    "mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py",
    "| Experience doctrine pressure | Agents-of-Abyss center route |",
    "| underlying-experience success pressure | owner evidence and source-review route |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_CERTIFICATION_PART_REQUIRED_TOKENS = (
    "experience certification gate proof",
    "mechanics/experience/parts/certification-gate/fixtures/experience-certification-gate-integrity-v1/README.md",
    "rollback_drill_verdict",
    "| certification authority pressure | Agents-of-Abyss and owner operator certification route |",
    "| release approval pressure | release-support and owner approval route |",
    "| runtime health pressure | `abyss-stack` runtime health route |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_ADOPTION_PART_REQUIRED_TOKENS = (
    "Experience adoption proof",
    "federation-harvest",
    "KAG/ToS boundary",
    "| owner-local adoption pressure | owner repository adoption route |",
    "| routing authorship pressure | `aoa-routing` route-authority lane |",
    "| runtime distillation candidate adoption pressure | `mechanics/distillation/parts/runtime-candidate-adoption/` |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_GOVERNANCE_PART_REQUIRED_TOKENS = (
    "Experience governance and runtime-boundary",
    "APPEAL_REVIEW_VERDICT.md",
    "STAY_ORDER_ENFORCEMENT_VERDICT.md",
    "VOTE_SEAL_INTEGRITY_VERDICT.md",
    "REPLAY_HISTORY_INTEGRITY_VERDICT.md",
    "authority-resolution",
    "constitution-runtime",
    "| governance authority pressure | Agents-of-Abyss center governance route |",
    "| runtime enforcement pressure | `abyss-stack` runtime route |",
    "python scripts/validate_repo.py",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_OFFICE_PART_REQUIRED_TOKENS = (
    "Experience office and release-train",
    "REPLAY_AUDIT_VERDICTS.md",
    "SERVICE_MESH_REGRESSION_VERDICTS.md",
    "mechanics/experience/parts/certification-gate/schemas/rollback_drill_verdict_v1.json",
    "| office installation pressure | Agents-of-Abyss, `aoa-agents`, and owner operator route |",
    "| release approval pressure | Agents-of-Abyss, release-support, and owner approval route |",
    "| release-support publication pressure | `release-support` publication posture route inside `aoa-evals` |",
    "python scripts/validate_repo.py",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
EXPERIENCE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/experience/",
    "AoA-aligned",
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "Source proof bundles stay under `evals/`",
    "operator certification",
    "owner-local adoption",
    "python scripts/validate_repo.py",
)
EXPERIENCE_VERDICT_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "mechanics/experience/parts/governance-runtime-boundary/docs/",
    "mechanics/experience/parts/office-release-train/docs/",
    "APPEAL_REVIEW_VERDICT.md",
    "SERVICE_MESH_REGRESSION_VERDICTS.md",
    "existing active parts",
    "does not grant governance authority",
    "python scripts/validate_repo.py",
)
EXPERIENCE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Experience Part Contract Guard",
    "mechanics/experience/parts/protocol-integrity/README.md",
    "mechanics/experience/parts/certification-gate/README.md",
    "mechanics/experience/parts/adoption-federation/README.md",
    "mechanics/experience/parts/governance-runtime-boundary/README.md",
    "mechanics/experience/parts/office-release-train/README.md",
    "live runtime activation",
    "operator certification",
    "owner-local adoption",
    "governance authority",
    "memory canon",
    "routing authorship",
    "broad Experience success",
    "python scripts/validate_repo.py",
)
ANTIFRAGILITY_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "stress or repair pressure",
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "evals/stress/aoa-antifragility-posture/EVAL.md",
    "evals/comparison/longitudinal-window/aoa-stress-recovery-window/EVAL.md",
    "evals/workflow/aoa-repair-boundedness/EVAL.md",
    "mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "Stronger Owner Split",
    "Stop-Lines",
    "| global resilience or federation-health pressure | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| live runtime self-healing pressure | runtime owner or `abyss-stack` runtime route |",
    "| deletion, cleanup, or owner-local repair authority pressure | owner repository repair and cleanup route |",
    "| one-score antifragility pressure | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| route, stats, memo, or generated-reader authority pressure | owning route, stats, memo, generated-source, and owner-receipt routes |",
    "| diagnosis-cause discipline or growth-cycle movement pressure | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "python scripts/validate_repo.py --eval aoa-stress-recovery-window",
)
ANTIFRAGILITY_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "antifragility proof work",
    "mechanics/antifragility/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "comparison-spine",
    "audit",
    "Create antifragility parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
ANTIFRAGILITY_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-diagnosis-cause-discipline",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "| global resilience or federation health | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| one-score health or antifragility movement | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| deletion theater, cleanup authority, runtime self-healing, or owner-local repair execution | owner repository or `abyss-stack` runtime route |",
    "| route, memo, stats, KAG, playbook, or generated-reader truth promotion | owning route, memo, stats, KAG, playbook, generated-source, and owner-receipt routes |",
    "| diagnosis-cause discipline or growth-cycle movement | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
)
ANTIFRAGILITY_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "| role | lower index for active eval-side Antifragility proof parts |",
    "## Active Parts",
    "| `posture-review/` | first-wave owner-local antifragility posture support |",
    "| `stress-recovery-window/` | repeated-window stress recovery support with comparison-spine readout |",
    "| `repair-proof/` | bounded repair-proof support with owner acceptance route |",
    "## Owner Pressure Routes",
    "| global resilience or federation health | `Agents-of-Abyss` doctrine route plus source-owner evidence review |",
    "| one-score health or antifragility movement | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| runtime repair, live self-healing, cleanup authority, or owner-local repair execution | owner repository or `abyss-stack` runtime route |",
    "| source proof meaning or verdict support | affected `evals/**/EVAL.md`, `evals/**/eval.yaml`, and bundle-local report contract |",
    "| diagnosis-cause discipline or growth-cycle movement | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "## Part Admission Route",
    "| new antifragility pressure | recurring operation with distinct inputs, outputs, owner split, and validation | parent `PARTS.md` update plus decision review |",
    "mechanics/antifragility/parts/AGENTS.md#validation",
)
ANTIFRAGILITY_PARTS_README_FORBIDDEN_TOKENS = (
    "The parts support proof review. They do not own source proof bundle meaning",
)
ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
ANTIFRAGILITY_POSTURE_PART_REQUIRED_TOKENS = (
    "aoa-antifragility-posture",
    "mechanics/antifragility/parts/posture-review/schemas/antifragility_eval_report_v1.json",
    "source eval package stays under `evals/`",
    "owner repository owns the local",
    "| repo-global resilience pressure | `Agents-of-Abyss` doctrine route plus owner evidence review |",
    "| repeated-window improvement pressure | `stress-recovery-window` and `comparison-spine` longitudinal routes |",
    "| runtime repair or live self-healing pressure | owner repository or `abyss-stack` runtime route |",
    "| source-ownership transfer pressure | owner repository receipt route |",
    "| route hints, stats, memory, or generated-reader authority pressure | owner receipts plus owning route, stats, memo, and generated-source routes |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_STRESS_WINDOW_PART_REQUIRED_TOKENS = (
    "aoa-stress-recovery-window",
    "mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md",
    "mechanics/antifragility/parts/stress-recovery-window/fixtures/stress-recovery-window-bounded-v1/README.md",
    "mechanics/antifragility/parts/stress-recovery-window/schemas/stress_recovery_window_eval_report_v1.json",
    "mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md",
    "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
    "comparison-spine",
    "audit",
    "| federation-wide resilience pressure | `Agents-of-Abyss` doctrine route plus owner evidence review |",
    "| live health or runtime recovery authority pressure | runtime owner or `abyss-stack` runtime route |",
    "| one-score antifragility movement pressure | `aoa-stats` vector-window route plus AoA doctrine review |",
    "| route, KAG, memo, playbook, or generated-reader authority pressure | owning route, KAG, memo, playbook, generated-source, and owner-evidence routes |",
    "| comparison acceptance pressure | `mechanics/comparison-spine/parts/longitudinal-window/` readout route |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_STRESS_WINDOW_DOC_REQUIRED_TOKENS = (
    "It answers a narrow question",
    "This remains a proof surface",
    "Workflow ownership stays with the owner route",
    "Federation-wide vibe-check pressure routes back to named owner evidence",
    "| route hints outranking owner receipts | owner receipt route before route-hint interpretation |",
    "| memo pattern objects standing in for current-run truth | owner evidence route before memo context |",
    "| regrounding success from ticket existence alone | regrounding evidence route with outcome conditions |",
    "| KAG quarantine exit as healthy re-entry | KAG condition route plus explicit re-entry evidence |",
    "| single-number movement pressure | split-axis stress-recovery readout route |",
)
ANTIFRAGILITY_REPAIR_PROOF_PART_REQUIRED_TOKENS = (
    "aoa-repair-boundedness",
    "mechanics/antifragility/parts/repair-proof/fixtures/repair-boundedness-v1/README.md",
    "repair-proof route",
    "aoa-diagnosis-cause-discipline",
    "| final owner-object quality pressure | owner repository acceptance route |",
    "| permanent stability pressure | owner repository regression and follow-through route |",
    "| authority widening after a repair pressure | owner approval and route-law review |",
    "| repair parent topology pressure | `mechanics/antifragility/` parent route plus evidence-cluster review |",
    "| `aoa-diagnosis-cause-discipline` pressure | `mechanics/growth-cycle/parts/diagnosis-gate/` route |",
    "| growth-cycle improvement pressure | growth-cycle proof route |",
    "python scripts/build_catalog.py --check",
) + ANTIFRAGILITY_PART_README_COMMON_REQUIRED_TOKENS
ANTIFRAGILITY_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
ANTIFRAGILITY_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/antifragility/",
    "AoA-aligned",
    "posture-review",
    "stress-recovery-window",
    "repair-proof",
    "Source proof bundles stay under `evals/`",
    "comparison-spine",
    "audit",
    "aoa-diagnosis-cause-discipline",
    "python scripts/validate_repo.py",
)
ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Antifragility Part Contract Guard",
    "mechanics/antifragility/parts/posture-review/README.md",
    "mechanics/antifragility/parts/stress-recovery-window/README.md",
    "mechanics/antifragility/parts/repair-proof/README.md",
    "global resilience",
    "live self-healing",
    "permanent stability",
    "repair parent",
    "growth-cycle completion",
    "growth-cycle/diagnosis-gate",
    "python scripts/validate_repo.py",
)
METHOD_GROWTH_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "growth-refinery pressure",
    "candidate-lineage",
    "owner-landing",
    "evals/capability/aoa-candidate-lineage-integrity/EVAL.md",
    "evals/boundary/aoa-owner-fit-routing-quality/EVAL.md",
    "mechanics/method-growth/parts/candidate-lineage/fixtures/candidate-lineage-v1/README.md",
    "mechanics/method-growth/parts/owner-landing/fixtures/owner-fit-routing-v1/README.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "| final owner-object quality pressure | final owner repository acceptance route |",
    "| owner-local acceptance or activation pressure | final owner repository route |",
    "| lineage coherence implies owner fit pressure | `owner-landing` route plus owner review |",
    "| owner-fit routing implies final quality pressure | final owner repository acceptance route |",
    "| derivative first-authoring pressure for `aoa-routing` or `aoa-kag` | source owner plus derivative-surface owner route |",
    "| universal growth score pressure | bundle-local proof review plus owner evidence route |",
    "| diagnosis-cause discipline or repair success pressure | `mechanics/growth-cycle/parts/diagnosis-gate/` or `mechanics/antifragility/parts/repair-proof/` route |",
    "| memory canon or seed truth pressure | `aoa-memo` memory route or `Dionysus` seed route |",
    "diagnosis-cause discipline",
    "python scripts/validate_repo.py --eval aoa-owner-fit-routing-quality",
)
METHOD_GROWTH_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "method-growth proof work",
    "mechanics/method-growth/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create method-growth parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
METHOD_GROWTH_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "candidate-lineage",
    "owner-landing",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-diagnosis-cause-discipline",
    "| final owner-object quality | final owner repository acceptance route |",
    "| owner-local activation | final owner repository route |",
    "| lineage-as-owner-fit proof | `owner-landing` route plus owner review |",
    "| owner-fit-as-final-quality proof | final owner repository acceptance route |",
    "| derivative first-authoring drift | source owner plus derivative-surface owner route |",
    "| universal growth score | bundle-local proof review plus owner evidence route |",
    "| diagnosis-cause ownership or repair success | `growth-cycle/diagnosis-gate` or `antifragility/repair-proof` route |",
    "| memory canon | `aoa-memo` memory route |",
    "| seed truth | `Dionysus` seed route |",
)
METHOD_GROWTH_CANDIDATE_LINEAGE_PART_REQUIRED_TOKENS = (
    "aoa-candidate-lineage-integrity",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/method-growth/parts/candidate-lineage/fixtures/candidate-lineage-v1/README.md",
    "lineage proof route",
    "| owner-fit routing proof pressure | `mechanics/method-growth/parts/owner-landing/` route |",
    "| final object quality or final owner-object quality pressure | final owner repository acceptance route |",
    "| owner-local acceptance, activation, or landed meaning pressure | final owner repository route |",
    "| skip owner-local evidence or receipts pressure | final owner repository evidence route |",
    "| seed truth pressure | `Dionysus` seed route |",
    "| memory canon pressure | `aoa-memo` memory route |",
    "| practice canon pressure | `aoa-techniques` technique route |",
    "| stats truth pressure | `aoa-stats` derived-summary route |",
    "| hidden promotion from a clean lineage chain pressure | owner review plus owner-landing route |",
    "| universal growth score pressure | bundle-local proof review plus owner evidence route |",
    "python scripts/build_catalog.py --check",
)
METHOD_GROWTH_OWNER_LANDING_PART_REQUIRED_TOKENS = (
    "aoa-owner-fit-routing-quality",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/method-growth/parts/owner-landing/fixtures/owner-fit-routing-v1/README.md",
    "owner-landing proof route",
    "derivative-drift",
    "| final owner-object quality pressure | final owner repository acceptance route |",
    "| owner-local acceptance, activation, or future maintenance pressure | final owner repository route |",
    "| permanent routing from one owner-fit read pressure | owner repository review plus routing surface review |",
    "| derivative first-authoring for `aoa-routing` or `aoa-kag` pressure | source owner plus derivative-surface owner route |",
    "| skill truth pressure | `aoa-skills` skill route |",
    "| technique truth pressure | `aoa-techniques` technique route |",
    "| playbook truth pressure | `aoa-playbooks` playbook route |",
    "| memory truth pressure | `aoa-memo` memory route |",
    "| seed truth pressure | `Dionysus` seed route |",
    "| stats truth pressure | `aoa-stats` derived-summary route |",
    "| lineage coherence implies owner fit pressure | `candidate-lineage` evidence plus owner review |",
    "| universal growth score pressure | bundle-local proof review plus owner evidence route |",
    "python scripts/build_catalog.py --check",
)
METHOD_GROWTH_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
METHOD_GROWTH_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/method-growth/",
    "AoA-aligned",
    "candidate-lineage",
    "owner-landing",
    "Source proof bundles stay under `evals/`",
    "aoa-diagnosis-cause-discipline",
    "aoa-repair-boundedness",
    "final owner-object truth",
    "python scripts/validate_repo.py",
)
METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Method-growth Part Owner-split Contract",
    "mechanics/method-growth/parts/candidate-lineage/README.md",
    "mechanics/method-growth/parts/owner-landing/README.md",
    "`## Stronger Owner Split`",
    "lineage proof only",
    "owner-fit routing proof only",
    "final owner truth stays with the owning repositories",
    "derivative first-authoring",
    "python -m pytest -q tests/test_validate_repo.py -k method_growth_part_owner_split",
)
RPG_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "progression or unlock pressure",
    "progression-unlocks",
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json",
    "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
    "Stronger Owner Split",
    "Stop-Lines",
    "| universal agent score or broad capability growth | `mechanics/rpg/parts/progression-unlocks/` can hold bounded evidence; broad growth reading routes through `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |",
    "| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates and proof review |",
    "python scripts/validate_repo.py",
)
RPG_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "RPG proof work",
    "mechanics/rpg/PARTS.md",
    "PROVENANCE.md",
    "progression evidence",
    "unlock proof",
    "Create RPG parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
RPG_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "progression-unlocks",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "growth-cycle",
    "| universal score, automatic rank, or broad capability growth | bounded progression evidence plus comparison/growth owner review |",
    "| generated-card authority | source support plus generated-reader route before citation |",
)
RPG_PROGRESS_UNLOCKS_PART_REQUIRED_TOKENS = (
    "Progression Unlocks Part",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json",
    "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
    "progression evidence",
    "unlock proof",
    "| quest completion or quest acceptance | quest source owner and questbook lifecycle route with proof refs |",
    "| universal rank, one global score, automatic rank assignment, or broad capability growth | bounded progression evidence plus `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |",
    "| runtime equip state, runtime activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |",
    "| growth-cycle diagnosis, repair, harvest, closeout, or longitudinal movement | `mechanics/growth-cycle/`, `mechanics/antifragility/`, closeout, and comparison owner routes |",
    "| generated-card authority | generated support source, schema/example review, and bundle-local proof citation route |",
    "python scripts/build_catalog.py --check",
)
RPG_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
RPG_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/rpg/",
    "AoA-aligned",
    "progression-unlocks",
    "docs/PROGRESSION_EVIDENCE_MODEL.md",
    "docs/UNLOCK_PROOF_BRIDGE.md",
    "Quest source records stay under",
    "growth-cycle",
    "pressure-to-owner route map",
    "runtime equip",
    "python scripts/validate_repo.py",
)
RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "RPG Progression-unlocks Contract",
    "mechanics/rpg/parts/progression-unlocks/README.md",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "pressure-to-owner route map",
    "quest source owner and questbook lifecycle route",
    "runtime route after owner gates",
    "generated unlock cards remain",
    "Diagnosis, repair, harvest, closeout, and longitudinal movement",
    "python -m pytest -q tests/test_validate_repo.py -k rpg_progression_unlocks",
)
GROWTH_CYCLE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "diagnosis pressure",
    "diagnosis-gate",
    "evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md",
    "evals/workflow/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "repair proof under `antifragility`",
    "repeated-window movement under",
    "| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success from tidy diagnosis pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| repair boundedness, owner fit, or final object quality pressure | repair-proof route plus owner repository acceptance route |",
    "| broad capability growth or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed closeout acceptance, donor harvest approval, or quest promotion pressure | closeout, donor, questbook, and target owner routes |",
    "| memory canon, runtime activation, hidden automation, or owner-local landing pressure | `aoa-memo`, `abyss-stack`, `aoa-skills` or `aoa-playbooks`, and owner repository routes |",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Growth Cycle diagnosis proof work",
    "mechanics/growth-cycle/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create growth-cycle parts from a recurring proof operation",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "diagnosis-gate",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-diagnosis-cause-discipline",
    "| cause certainty | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| owner-fit proof or final object quality | owner repository acceptance route |",
    "| broad capability growth or universal progression score | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed-closeout acceptance, donor harvest approval, or quest promotion | closeout, donor, questbook, and target owner routes |",
    "| memory canon | `aoa-memo` memory route |",
    "| runtime activation or hidden automation | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "| owner-local landing | owner repository acceptance route |",
)
GROWTH_CYCLE_PARTS_README_REQUIRED_TOKENS = (
    "# Growth-cycle / Parts Route",
    "## Operating Card",
    "| role | lower index for active Growth Cycle proof parts |",
    "## Active Parts",
    "| `diagnosis-gate/` | cause-hypothesis discipline before repair, progression, closeout, quest, memory, runtime, or owner acceptance claims | `diagnosis-gate/README.md` |",
    "## Owner Pressure Routes",
    "| cause certainty | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| broad capability growth or universal progression score | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| runtime activation or hidden automation | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "## Part Admission Route",
    "| diagnosis or self-diagnosis evidence needs cause-hypothesis discipline | source bundle and part contract already exist | `diagnosis-gate/README.md` |",
    "mechanics/growth-cycle/parts/AGENTS.md#validation",
)
GROWTH_CYCLE_DIAGNOSIS_GATE_PART_REQUIRED_TOKENS = (
    "Diagnosis Gate Part",
    "eval-backed thin support route",
    "payload subdirectories are absent by design",
    "evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "symptom refs",
    "probable cause hypotheses",
    "aoa-repair-boundedness",
    "mechanics/antifragility/parts/repair-proof/",
    "| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| owner-fit proof pressure | owner repository acceptance route |",
    "| final object quality proof pressure | owner repository acceptance route |",
    "| broad growth score or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed closeout acceptance pressure | closeout route plus owner acceptance |",
    "| donor harvest approval pressure | donor harvest route plus target owner acceptance |",
    "| quest promotion pressure | `mechanics/questbook/` route plus owner acceptance |",
    "| memory canon pressure | `aoa-memo` memory route |",
    "| runtime activation or hidden automation pressure | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "| owner acceptance or owner-local landing pressure | owner repository acceptance route |",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
GROWTH_CYCLE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/growth-cycle/",
    "AoA-aligned",
    "diagnosis-gate",
    "aoa-diagnosis-cause-discipline",
    "Source proof bundles stay under `evals/`",
    "aoa-repair-boundedness",
    "aoa-longitudinal-growth-snapshot",
    "No root file movement",
    "python scripts/validate_repo.py",
)
GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Growth-cycle Diagnosis-gate Contract",
    "mechanics/growth-cycle/parts/diagnosis-gate/README.md",
    "eval-backed thin support route",
    "cause-hypothesis discipline",
    "repair parent",
    "owner-fit proof",
    "broad growth score",
    "donor-harvest approval",
    "quest-promotion",
    "owner-local landing authority",
    "python scripts/validate_repo.py",
)
REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Repair Diagnosis Route Boundary",
    "mechanics/antifragility/parts/repair-proof/",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "aoa-repair-boundedness",
    "aoa-diagnosis-cause-discipline",
    "`repair` remains a wrong parent form",
    "Diagnosis-cause discipline is not an antifragility part",
    "repair proof is not diagnosis proof",
    "python -m pytest -q tests/test_validate_repo.py -k repair_diagnosis_route_boundary",
)
DISTILLATION_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "distillation pressure",
    "compost-provenance",
    "runtime-candidate-adoption",
    "evals/artifact/aoa-compost-provenance-preservation/EVAL.md",
    "evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "| summary-as-proof pressure | source trace, source bundle, and bundle-local review route |",
    "| raw deletion authority pressure | owner repository source-retention route |",
    "| proof verdict without bundle-local review pressure | bundle-local review route |",
    "| memory canon, recall sovereignty, or live memory-ledger pressure | `aoa-memo` memory route |",
    "| runtime activation or hidden runtime-store pressure | `abyss-stack` runtime route |",
    "| owner acceptance, owner-local adoption, or final promotion pressure | owner repository acceptance route |",
    "| Tree-of-Sophia canon or compost authority pressure | Tree-of-Sophia canon route |",
    "| KAG bridge promotion or graph lift pressure | `aoa-kag` graph-lift route |",
    "| memo contradiction or confirmed writeback-act pressure | owning eval bundle or mechanic part route |",
    "| memo recall pressure | `mechanics/recurrence/parts/memory-recall/` route |",
    "python scripts/validate_repo.py --eval aoa-compost-provenance-preservation",
)
DISTILLATION_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Distillation proof work",
    "mechanics/distillation/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create Distillation parts from a recurring proof operation",
    "python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity",
)
DISTILLATION_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "compost-provenance",
    "runtime-candidate-adoption",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-compost-provenance-preservation",
    "aoa-memo-reviewed-candidate-adoption-integrity",
    "| summary-as-proof or raw deletion authority | source trace, source bundle, owner source-retention route |",
    "| memory canon or live memory-ledger behavior | `aoa-memo` memory route |",
    "| runtime activation or hidden runtime-store truth | `abyss-stack` runtime route |",
    "| owner acceptance, owner-local adoption, or final promotion | owner repository acceptance route |",
    "| ToS canon or compost authority | Tree-of-Sophia canon route |",
    "| KAG bridge promotion or graph lift | `aoa-kag` graph-lift route |",
    "| generic adoption readiness | `mechanics/experience/parts/adoption-federation/` route |",
    "| memo recall after active recurrence routing | `mechanics/recurrence/parts/memory-recall/` route |",
    "| nearby contradiction or base writeback proof | owning eval bundle or mechanic part route |",
)
DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
DISTILLATION_COMPOST_PROVENANCE_PART_REQUIRED_TOKENS = (
    "Compost Provenance Part",
    "evals/artifact/aoa-compost-provenance-preservation/EVAL.md",
    "mechanics/distillation/parts/compost-provenance/fixtures/compost-provenance-v1/README.md",
    "| ToS canon pressure | Tree-of-Sophia canon route |",
    "| principle truth pressure | Tree-of-Sophia authored-meaning route |",
    "| compost canon pressure | Tree-of-Sophia compost route |",
    "| original run quality pressure | owner repository source-artifact route |",
    "| witness trace honesty pressure | witness-source evidence route |",
    "| artifact-quality verdict pressure | bundle-local artifact review route |",
    "| artifact/process comparison pressure | `comparison-spine` route |",
    "| memory canon pressure | `aoa-memo` memory route |",
    "| operational ownership transfer pressure | owner repository transfer route |",
    "python scripts/validate_repo.py --eval aoa-compost-provenance-preservation",
) + DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS
DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_REQUIRED_TOKENS = (
    "Runtime Candidate Adoption Part",
    "evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md",
    "mechanics/distillation/parts/runtime-candidate-adoption/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md",
    "distillation_claim_candidate",
    "aoa-memo-writeback-act-integrity",
    "| final promotion pressure | owner approval and durable memory review route |",
    "| memory canon or memo object truth pressure | `aoa-memo` memory-object route |",
    "| live memory-ledger behavior pressure | `aoa-memo` and `abyss-stack` runtime route |",
    "| memo recall implementation pressure | `mechanics/recurrence/parts/memory-recall/` and `aoa-memo` route |",
    "| runtime pack contract authority pressure | `aoa-agents` runtime artifact route |",
    "| live receipt append behavior pressure | `publication-receipts` and runtime receipt route |",
    "| Experience adoption federation pressure | `mechanics/experience/parts/adoption-federation/` |",
    "| KAG lift or bridge-ready truth pressure | `aoa-kag` graph-lift route |",
    "| owner-local adoption or final owner acceptance pressure | owner repository route |",
    "python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity",
) + DISTILLATION_PART_README_COMMON_REQUIRED_TOKENS
DISTILLATION_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
DISTILLATION_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/distillation/",
    "AoA-aligned",
    "compost-provenance",
    "runtime-candidate-adoption",
    "Source proof bundles stay under `evals/`",
    "summary-as-proof",
    "aoa-memo-writeback-act-integrity",
    "python scripts/validate_repo.py",
)
DISTILLATION_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Distillation Part Contract Guard",
    "mechanics/distillation/parts/compost-provenance/README.md",
    "mechanics/distillation/parts/runtime-candidate-adoption/README.md",
    "ToS canon",
    "memory canon",
    "runtime promotion",
    "receipt publication",
    "Experience adoption federation",
    "KAG lift",
    "owner-local acceptance",
    "python scripts/validate_repo.py",
)
QUESTBOOK_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "quests/",
    "quests/LIFECYCLE.md",
    "source-record-contract",
    "dispatch-reader",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "lane/state",
    "Quests route eval-bundle",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source quest record",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "mechanics/questbook/PROVENANCE.md",
    "quests/LIFECYCLE.md",
    "generated quest reader",
    "lane/state",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "source-record-contract",
    "dispatch-reader",
    "generated quest reader",
    "source quest record",
    "old top-level quest source path revived as alias",
    "AGENTS.md#validation",
)
QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS = (
    "Quest Source Record Contract",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json",
    "quests/<lane>/<state>/AOA-EV-Q-*.yaml",
    "quests/LIFECYCLE.md",
    "QUESTBOOK.md",
    "generated projection input",
    "source quest record identity",
    "aoa-quest-harvest",
    "roadmap direction",
    "owner acceptance",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS = (
    "Quest Dispatch Reader",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "scripts/build_catalog.py",
    "generated projection contract",
    "source quest truth",
    "live task assignment",
    "proof-surface promotion",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS = (
    "quests/LIFECYCLE.md",
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
    "proof-loop",
    "route-smoke",
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME = (
    "docs/decisions/0098-agon-quest-note-provenance-route.md"
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS = (
    "mechanics/agon/PROVENANCE.md",
    "Agon legacy archive",
    "archive-local accounting",
    "schema-backed source quest records",
    "markdown quest notes",
    "quests/",
    "python -m pytest -q tests/test_validate_repo.py -k quest_route",
)
QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/questbook/",
    "source quest records",
    "generated quest",
    "lane/state",
    "no empty taxonomy",
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Questbook Part Owner-split Contract",
    "mechanics/questbook/parts/source-record-contract/README.md",
    "mechanics/questbook/parts/dispatch-reader/README.md",
    "`## Stronger Owner Split`",
    "Source quest records stay under `quests/<lane>/<state>/`",
    "Human visibility stays",
    "Generated quest readers stay under root `generated/`",
    "aoa-quest-harvest",
    "live task assignment",
    "python -m pytest -q tests/test_validate_repo.py -k questbook_part_owner_split",
)
AUDIT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
    "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json",
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json",
    "candidate-only",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "runtime or trace artifact",
    "selected evidence packet",
    "runtime candidate reader",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/audit/",
    "runtime evidence selection",
    "artifact-to-verdict",
    "generated readers",
    "bundle-local review",
    "does not turn runtime evidence into proof canon",
)
AUDIT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for `audit` part-local candidate-evidence suboperations",
    "## Active Parts",
    "`selected-evidence-packets/`",
    "`artifact-verdict-hooks/`",
    "`candidate-readers/`",
    "`integrity-review/`",
    "## Part Admission Route",
    "source surfaces",
    "drift-catching validation",
    "stronger-owner boundary",
    "mechanics/audit/AGENTS.md#validation",
)
AUDIT_PARTS_README_FORBIDDEN_TOKENS = (
    "Do not create another part unless",
)
AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
AUDIT_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/runtime-evidence/",
    "mechanics/audit/",
    "schemas/runtime-evidence-selection.schema.json",
    "mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json",
    "generated/runtime_candidate_template_index.min.json",
    "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
)
AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "runtime-evidence",
    "audit",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "Do not create new audit work in legacy",
)
AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)
AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Audit Part Contract Guard",
    "selected-evidence-packets",
    "artifact-verdict-hooks",
    "candidate-readers",
    "integrity-review",
    "inputs, outputs",
    "stronger-owner split",
    "candidate-only",
    "python scripts/validate_repo.py",
)
AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "runtime-evidence-selection.schema.json",
    "runtime_evidence_selection.*.example.json",
    "candidate-only",
    "bundle-local review",
    "overread-routing notes",
    "runtime-owner review and bundle-local eval review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
)
AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "TRACE_EVAL_BRIDGE.md",
    "artifact-to-verdict-hook.schema.json",
    "mechanic-local hook examples",
    "review metadata",
    "route to the owning eval bundle",
    "bundle-local review",
    "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
)
AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "generate_runtime_candidate_template_index.py",
    "runtime_candidate_template_index.min.json",
    "runtime_candidate_intake.min.json",
    "Reader changes start in",
    "generated reader content needs to change",
)
AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "RUNTIME_INTEGRITY_REVIEW.md",
    "runtime-integrity-review.schema.json",
    "runtime_integrity_review.example.json",
    "candidate-only",
    "runtime continuity activation is requested",
    "route to Experience and runtime-owner gates",
    "python -m pytest -q tests/test_validate_repo.py -k runtime_integrity_review",
)
BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_REQUIRED_TOKENS = (
    "compatibility map",
    "repo-qualified ref",
    "current/legacy/rejected/unresolved",
    "latest-sibling canary",
    "pinned `Repo Validation` ref",
    REPO_VALIDATION_AOA_MEMO_REF,
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    "AGENTS.md#validation",
    "Authority-transfer pressure routes to the sibling owner",
)
BOUNDARY_BRIDGE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    "mechanics/boundary-bridge/PARTS.md",
    "mechanics/boundary-bridge/parts/README.md",
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    REPO_VALIDATION_WORKFLOW_NAME,
    "latest-sibling canary",
    "pinned public-lane refresh",
    "current/legacy/rejected/unresolved",
    "route through the sibling owner before changing it",
    "bundle-local review",
)
BOUNDARY_BRIDGE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "repo-qualified ref",
    "sibling owner route",
    "compatibility posture",
    "latest-sibling canary",
    SIBLING_CANARY_COMMAND,
)
BOUNDARY_BRIDGE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "compatibility-map",
    "latest-sibling-canary",
    "Parts stay as limbs of `boundary-bridge`",
    "sibling owner route",
)
BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
BOUNDARY_BRIDGE_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/sibling-proof-refs/",
    "mechanics/boundary-bridge/",
    "docs/SIBLING_PROOF_REFS.md",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    "docs/ORCHESTRATOR_PROOF_ALIGNMENT.md",
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md",
    "generated/phase_alpha_eval_matrix.min.json",
    "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
)
BOUNDARY_BRIDGE_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "boundary-bridge",
    "compatibility-map",
    "latest-sibling-canary",
    "orchestrator-proof-anchors",
    "phase-alpha-eval-matrix",
    "mechanics/sibling-proof-refs/",
    "Do not create new boundary-bridge work in legacy",
)
BOUNDARY_BRIDGE_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active boundary-bridge",
)
BOUNDARY_BRIDGE_PARTS_README_REQUIRED_TOKENS = (
    "compatibility-map/",
    "latest-sibling-canary/",
    "AGENTS.md#validation",
)
BOUNDARY_BRIDGE_COMPATIBILITY_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "authored compatibility map",
    "current, legacy, rejected, or unresolved posture",
    "sibling owner acceptance",
    "sibling edit pressure appears",
)
BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py",
    "GitHub `Repo Validation`",
    "sibling edit pressure appears",
    "GitHub `Repo Validation` replacement pressure appears",
)
BOUNDARY_BRIDGE_ORCHESTRATOR_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "aoa-agents",
    "aoa-playbooks",
    "aoa-memo",
    "creating an `orchestrator` mechanic",
    "python scripts/build_catalog.py --check",
)
BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Boundary Bridge Part Contract Guard",
    "mechanics/boundary-bridge/parts/compatibility-map/README.md",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md",
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md",
    "part-level contracts",
    "sibling authority",
    "orchestrator",
    "latest-sibling-canary",
    "python scripts/validate_repo.py",
)
BOUNDARY_BRIDGE_DECISION_REQUIRED_TOKENS = (
    "mechanics/boundary-bridge/",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    "latest-sibling canary",
    "current, legacy, rejected, or unresolved",
    "does not authorize editing sibling repositories",
)
SIBLING_CANARY_EXPECTED_REPOS = (
    "aoa-techniques",
    "aoa-skills",
    "aoa-agents",
    "aoa-playbooks",
    "aoa-memo",
    "aoa-routing",
    "aoa-kag",
    "aoa-sdk",
    "aoa-stats",
    "abyss-stack",
)
SCHEMAS_DIR_NAME = "schemas"
EVAL_FRONTMATTER_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json"
)
EVAL_MANIFEST_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json"
)
GENERATED_DIR_NAME = "generated"
EXAMPLES_DIR_NAME = "examples"
FULL_CATALOG_NAME = eval_catalog_contract.FULL_CATALOG_NAME
MIN_CATALOG_NAME = eval_catalog_contract.MIN_CATALOG_NAME
CATALOG_VERSION = eval_catalog_contract.CATALOG_VERSION
CATALOG_SOURCE_OF_TRUTH = eval_catalog_contract.CATALOG_SOURCE_OF_TRUTH
CAPSULE_NAME = eval_capsule_contract.CAPSULE_NAME
CAPSULE_VERSION = eval_capsule_contract.CAPSULE_VERSION
CAPSULE_SOURCE_OF_TRUTH = eval_capsule_contract.CAPSULE_SOURCE_OF_TRUTH
SECTION_NAME = eval_section_contract.SECTIONS_NAME
SECTION_VERSION = eval_section_contract.SECTION_VERSION
SECTION_SOURCE_OF_TRUTH = eval_section_contract.SECTION_SOURCE_OF_TRUTH
COMPARISON_SPINE_NAME = eval_comparison_spine_contract.COMPARISON_SPINE_NAME
COMPARISON_SPINE_VERSION = eval_comparison_spine_contract.COMPARISON_SPINE_VERSION
COMPARISON_SPINE_SOURCE_OF_TRUTH = eval_comparison_spine_contract.COMPARISON_SPINE_SOURCE_OF_TRUTH
ARTIFACT_PROCESS_GUIDE_NAME = "docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md"
REPEATED_WINDOW_GUIDE_NAME = "docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md"
SHARED_PROOF_INFRA_GUIDE_NAME = "docs/SHARED_PROOF_INFRA_GUIDE.md"
QUESTBOOK_NAME = "QUESTBOOK.md"
QUESTS_README_NAME = "quests/README.md"
QUESTS_AGENTS_NAME = "quests/AGENTS.md"
QUEST_LIFECYCLE_NAME = "quests/LIFECYCLE.md"
QUESTBOOK_INTEGRATION_NAME = "docs/QUESTBOOK_EVAL_INTEGRATION.md"
QUEST_SCHEMA_NAME = "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json"
QUEST_DISPATCH_SCHEMA_NAME = "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json"
QUEST_CATALOG_NAME = "generated/quest_catalog.min.json"
QUEST_DISPATCH_NAME = "generated/quest_dispatch.min.json"
QUEST_CATALOG_EXAMPLE_NAME = "generated/quest_catalog.min.example.json"
QUEST_DISPATCH_EXAMPLE_NAME = "generated/quest_dispatch.min.example.json"
QUEST_SOURCE_LANES = (
    "proof",
    "trace",
    "orchestrator",
    "unlock",
    "runtime",
    "closeout",
    "agon",
    "harvest",
    "questbook",
)
QUEST_SOURCE_STATES = (
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
)
FOUNDATION_QUEST_NAMES = (
    "AOA-EV-Q-0001",
    "AOA-EV-Q-0002",
    "AOA-EV-Q-0003",
    "AOA-EV-Q-0004",
)
CLOSED_QUEST_STATES = {"done", "dropped"}
QUESTBOOK_INTEGRATION_REQUIRED_TOKENS = (
    "proof",
    "regression",
    "verdict-bridge",
    "example-only",
    "repo-local review projection",
)
QUESTBOOK_NOTE_REQUIRED_TOKENS = (
    "# Questbook Obligation Index",
    "public human obligation index",
    "proof",
    "regression",
    "verdict-bridge",
)
QUESTS_README_REQUIRED_TOKENS = (
    "# Quest Source Records",
    "source quest record district",
    "human questbook index",
    "mechanics/questbook/",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "source eval packages under `evals/`",
)
QUESTS_AGENTS_REQUIRED_TOKENS = (
    "source quest record district",
    "mechanics/questbook/",
    "generated quest files as dispatch readers",
    "source quest records",
    "schema-backed YAML",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "validate_repo.py",
)
QUEST_LIFECYCLE_REQUIRED_TOKENS = (
    "# Quest Lifecycle Contract",
    "State Matrix",
    "Open-index posture",
    "Return posture",
    "Promotion posture",
    "Proof-Loop Return Use",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "below eval result receipt",
    "Open states",
    "Closed states",
    "`QUESTBOOK.md` must list open quest IDs and leave closed quest IDs out",
)
QUEST_SCHEMA_TITLE = "work_quest_v1"
QUEST_SCHEMA_VERSION = "work_quest_v1"
QUEST_DISPATCH_SCHEMA_TITLE = "quest_dispatch_v1"
QUEST_DISPATCH_SCHEMA_VERSION = "quest_dispatch_v1"
QUEST_DISPATCH_ARTIFACT_OVERRIDES = {
    "AOA-EV-Q-0001": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0002": [
        "bounded_plan",
        "evaluation_result",
        "verification_result",
    ],
    "AOA-EV-Q-0003": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0004": [
        "recurrence_evidence",
        "promotion_decision",
    ],
}
ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS = {
    "repo_layer_selection",
    "evidence_closure",
    "bounded_next_step",
}
ORCHESTRATOR_PROOF_QUESTS = {
    "AOA-EV-Q-0006": ("aoa-agents:router", "repo_layer_selection"),
    "AOA-EV-Q-0007": ("aoa-agents:review", "evidence_closure"),
    "AOA-EV-Q-0008": ("aoa-agents:bounded_execution", "bounded_next_step"),
}
ORCHESTRATOR_CLASS_CATALOG_NAME = "generated/orchestrator_class_catalog.min.json"
ORCHESTRATOR_PROOF_ALIGNMENT_NAME = (
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/"
    "ORCHESTRATOR_PROOF_ALIGNMENT.md"
)
ORCHESTRATOR_PROOF_REQUIRED_TOKENS = (
    "## Router",
    "## Review",
    "## Bounded execution",
    "## Boundary rule",
    "Proof surfaces judge work.",
)
PROGRESSION_EVIDENCE_MODEL_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md"
)
PROGRESSION_EVIDENCE_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json"
)
PROGRESSION_EVIDENCE_EXAMPLE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json"
)
UNLOCK_PROOF_BRIDGE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md"
)
UNLOCK_PROOF_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json"
)
UNLOCK_PROOF_EXAMPLE_NAME = "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json"
PROGRESSION_EVIDENCE_REQUIRED_TOKENS = (
    "## Core route",
    "Progression evidence is quest-scoped or route-scoped proof.",
    "| one universal score or broad capability growth | keep multi-axis deltas here; route broad comparison through comparison/growth owner review |",
    "| quest acceptance or state-transition pressure | quest owner route plus cited evidence |",
    "cautions are first-class proof",
)
UNLOCK_PROOF_REQUIRED_TOKENS = (
    "## Core route",
    "`gated_grant`",
    "It interprets reviewed evidence",
    "| runtime equip or activation pressure | `abyss-stack` runtime route plus owner gates |",
    "| one proof object as a universal agent ranking | multi-axis progression evidence plus owner review |",
)

MIRRORED_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "report_format",
    "comparison_surface",
)
MIN_ENTRY_KEYS = eval_catalog_contract.MIN_ENTRY_KEYS
KNOWN_REPOS = eval_catalog_contract.KNOWN_REPOS
NO_ADDITIONAL_STARTER_BUNDLES_TEXT = (
    "No additional planned starter bundles are currently named publicly."
)

REQUIRED_HEADINGS = set(eval_section_contract.CANONICAL_HEADINGS)
VISIBLE_ROOTS = (
    REPO_ROOT,
    AOA_TECHNIQUES_ROOT,
    AOA_SKILLS_ROOT,
    AOA_AGENTS_ROOT,
    AOA_PLAYBOOKS_ROOT,
    AOA_MEMO_ROOT,
    AOA_ROUTING_ROOT,
    AOA_KAG_ROOT,
    AOA_SDK_ROOT,
    ABYSS_STACK_ROOT,
)
REPO_REF_PREFIX = "repo:"
REPO_REF_ROOTS = {
    "aoa-evals": REPO_ROOT,
    "aoa-techniques": AOA_TECHNIQUES_ROOT,
    "aoa-skills": AOA_SKILLS_ROOT,
    "aoa-agents": AOA_AGENTS_ROOT,
    "aoa-playbooks": AOA_PLAYBOOKS_ROOT,
    "aoa-memo": AOA_MEMO_ROOT,
    "aoa-routing": AOA_ROUTING_ROOT,
    "aoa-kag": AOA_KAG_ROOT,
    "aoa-sdk": AOA_SDK_ROOT,
    "abyss-stack": ABYSS_STACK_ROOT,
}
ARTIFACT_VERDICT_HOOK_SCHEMA_NAME = "artifact-to-verdict-hook.schema.json"
ARTIFACT_VERDICT_HOOK_SCHEMA_PATH = (
    "mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json"
)
ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR = "mechanics/audit/parts/artifact-verdict-hooks/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS = (
    ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR,
    "mechanics/checkpoint/parts/a2a-summon-return/examples",
    "mechanics/checkpoint/parts/restartable-inquiry/examples",
    "mechanics/checkpoint/parts/self-agent-posture/examples",
)
RUNTIME_EVIDENCE_SELECTION_SCHEMA_NAME = "runtime-evidence-selection.schema.json"
RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH = (
    "mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json"
)
RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR = "mechanics/audit/parts/selected-evidence-packets/examples"
STATS_EVENT_ENVELOPE_SCHEMA_NAME = "stats-event-envelope.schema.json"
EVAL_RESULT_RECEIPT_SCHEMA_NAME = "eval-result-receipt.schema.json"
PUBLICATION_RECEIPTS_PARTS_ROOT = "mechanics/publication-receipts/parts"
STATS_EVENT_ENVELOPE_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/stats-envelope-mirror/schemas/{STATS_EVENT_ENVELOPE_SCHEMA_NAME}"
)
EVAL_RESULT_RECEIPT_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/schemas/{EVAL_RESULT_RECEIPT_SCHEMA_NAME}"
)
EVAL_RESULT_RECEIPT_GUIDE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md"
)
EVAL_RESULT_RECEIPT_EXAMPLE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/examples/eval_result_receipt.example.json"
)
EVAL_RESULT_RECEIPT_PUBLISHER_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/live-publisher/scripts/publish_live_receipts.py"
)
LIVE_EVAL_RECEIPT_LOG_NAME = ".aoa/live_receipts/eval-result-receipts.jsonl"
EVAL_RESULT_RECEIPT_REQUIRED_TOKENS = (
    "## Core Rule",
    "`eval_result_receipt`",
    "`stats-event-envelope`",
    "`supersedes`",
    "meaning stays with bundle-local review",
    "repo-global score",
    "## Receipt Pressure Routes",
    "Proof-canon pressure routes",
)
RUNTIME_INTEGRITY_REVIEW_DOC_NAME = "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md"
RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME = "runtime-integrity-review.schema.json"
RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH = (
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
)
RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME = "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
RUNTIME_INTEGRITY_REVIEW_BUDGET_REF = (
    "Agents-of-Abyss:mechanics/experience/parts/continuity-context/CONTRACT.md#stronger-owner-split"
)
RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS = (
    "`candidate_only`",
    "`human_review_needed`",
    "`budget_ref`",
    "`evidence_refs`",
    "`replay_requirements`",
    "`forbidden_claims`",
    "`sealed_verdict`",
    "`activation_authority`",
    "`owner_override`",
    "`canon_write`",
    "Proof-canon pressure routes to bundle-local proof review.",
    "Runtime-continuity activation pressure routes to Experience and runtime-owner",
)
RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS = (
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
    "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    "`candidate_only`",
    "`human_review_needed`",
)
RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS = (
    "repo:aoa-evals/mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
    "repo:aoa-evals/mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "repo:aoa-routing/docs/LIVE_SESSION_REENTRY_ROUTE_REVIEW.md",
    "repo:aoa-agents/docs/SELF_AGENCY_CONTINUITY_LANE.md",
    "repo:aoa-memo/mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
    "repo:aoa-memo/mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md",
)
RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS = (
    "selected_evidence_only",
    "owner_local_replay_required",
    "fail_closed",
    "publication_requires_review",
)
RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS = (
    "sealed_verdict",
    "activation_authority",
    "owner_override",
    "canon_write",
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_NAME = "runtime-candidate-template-index.schema.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH = (
    "mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json"
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"
RUNTIME_CANDIDATE_INTAKE_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py"
)
RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py"
)
EVAL_REPORT_INDEX_NAME = "generated/eval_report_index.min.json"
EVAL_REPORT_INDEX_DECISION_NAME = "docs/decisions/0023-eval-report-index-reader.md"
PHASE_ALPHA_EVAL_MATRIX_PART_NAME = "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix"
PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/schemas/phase-alpha-eval-matrix.schema.json"
)
PHASE_ALPHA_EVAL_MATRIX_EXAMPLE_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/examples/phase_alpha_eval_matrix.example.json"
)
PHASE_ALPHA_EVAL_MATRIX_SCRIPT_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/scripts/generate_phase_alpha_eval_matrix.py"
)
PHASE_ALPHA_EVAL_MATRIX_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/generated/phase_alpha_eval_matrix.min.json"
)
NORMALIZED_RUNTIME_ARTIFACT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
ARTIFACT_VERDICT_HOOK_EXAMPLES = {
    "AOA-P-0014": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json",
    "AOA-P-0006": "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
    "AOA-P-0018": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json",
    "AOA-P-0008": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
    "AOA-P-0009": "mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json",
    "AOA-P-0031": "mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json",
    "AOA-P-0032": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
}
RUNTIME_EVIDENCE_SELECTION_EXAMPLES: dict[str, dict[str, Any]] = {
    "runtime_evidence_selection.workhorse-local.example.json": {
        "target_eval": None,
        "source_schema_ref": "repo:abyss-stack/mechanics/inference-pilots/parts/local-trials/schemas/runtime-benchmark.schema.json",
        "candidate_eval_refs": ["candidate:fixed-baseline-runtime-latency-tradeoff"],
    },
    "runtime_evidence_selection.return-anchor-integrity.example.json": {
        "target_eval": "aoa-return-anchor-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        "candidate_eval_refs": ["candidate:aoa-return-anchor-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json": {
        "target_eval": "aoa-memo-recall-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-recall-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json": {
        "target_eval": "aoa-memo-writeback-act-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-writeback-act-integrity"],
    },
    "runtime_evidence_selection.runtime-chaos-window.example.json": {
        "target_eval": "aoa-stress-recovery-window",
        "source_schema_ref": "repo:abyss-stack/mechanics/runtime-repair/parts/degradation-receipts/schemas/service-degradation-receipt.schema.json",
        "candidate_eval_refs": ["candidate:aoa-stress-recovery-window"],
        "allowed_ref_roots": ["mechanics"],
    },
}
TRACE_EVAL_HOOK_EXPECTATIONS = {
    "AOA-P-0014": {
        "eval_anchor": "aoa-verification-honesty",
        "artifact_contract_refs": [
            "repo:aoa-playbooks/playbooks/local-stack-diagnosis/PLAYBOOK.md#expected-artifacts",
            "repo:aoa-playbooks/docs/alpha-readiness/local-stack-diagnosis.md",
            "repo:aoa-agents/examples/alpha_reference_routes/local-stack-diagnosis.example.json",
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
            "repo:aoa-agents/schemas/self-agent-checkpoint.schema.json",
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
            "repo:aoa-playbooks/docs/alpha-readiness/validation-driven-remediation.md",
            "repo:aoa-agents/examples/alpha_reference_routes/validation-driven-remediation.example.json",
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
            "repo:aoa-agents/schemas/artifact.route_decision.schema.json",
            "repo:aoa-agents/schemas/artifact.bounded_plan.schema.json",
            "repo:aoa-agents/schemas/artifact.verification_result.schema.json",
            "repo:aoa-agents/schemas/artifact.transition_decision.schema.json",
            "repo:aoa-agents/schemas/artifact.distillation_pack.schema.json",
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
            "repo:aoa-sdk/docs/A2A_WAVE5_CODEX_RETURN_CHECKPOINT.md",
            "repo:aoa-sdk/examples/a2a/codex_local_target.example.json",
            "repo:aoa-sdk/examples/a2a/return_transition_decision.example.json",
            "repo:aoa-sdk/examples/a2a/checkpoint_bridge_plan.example.json",
            "repo:aoa-sdk/examples/a2a/reviewed_closeout_request.example.json",
            "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json",
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
            "repo:aoa-playbooks/examples/playbook_stress_lane.runtime-timeout-chaos.example.json",
            "repo:aoa-playbooks/examples/playbook_reentry_gate.retrieval-outage-honesty.example.json",
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
COMPARISON_SURFACE_COMMON_KEYS = (
    "shared_family_path",
    "paired_readout_path",
    "integrity_sidecar",
    "selection_question",
)
COMPARISON_SURFACE_ALLOWED_KEYS = {
    "fixed-baseline": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "previous-version": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "peer-compare": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("peer_surfaces", "matched_surface")
    ),
    "longitudinal-window": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "window_family_label")
    ),
}
INTEGRITY_RISK_CLASSES = (
    "style-over-substance",
    "artifact/process collapse",
    "baseline by association",
    "growth by association",
    "peer-compare blur",
    "fixed-baseline drift",
    "longitudinal overclaim",
    "schema-clean but claim-overstated",
    "routing overreach",
)
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class EvalBundleRecord:
    name: str
    bundle_dir: Path
    eval_md_path: Path
    eval_yaml_path: Path
    metadata: dict[str, Any]
    manifest: dict[str, Any]
    sections: dict[str, str]


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_paths_by_name = {
        STATS_EVENT_ENVELOPE_SCHEMA_NAME: Path(STATS_EVENT_ENVELOPE_SCHEMA_PATH),
        EVAL_RESULT_RECEIPT_SCHEMA_NAME: Path(EVAL_RESULT_RECEIPT_SCHEMA_PATH),
    }
    if schema_name in schema_paths_by_name:
        schema_relative_path = schema_paths_by_name[schema_name]
    else:
        schema_candidate = Path(schema_name)
        schema_relative_path = (
            schema_candidate
            if schema_candidate.parent != Path(".")
            else Path(SCHEMAS_DIR_NAME) / schema_candidate
        )
    schema_path = REPO_ROOT / schema_relative_path
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def get_schema_validator_with_format(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(
        schema,
        format_checker=FORMAT_CHECKER,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-evals source packages.")
    parser.add_argument(
        "--eval",
        help="Validate a single eval bundle by directory name.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or REPO_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def display_location(path: Path) -> str:
    for root in VISIBLE_ROOTS:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


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


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
) -> bool:
    active_validator = validator or get_schema_validator(schema_name)
    schema_errors = sorted(
        active_validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid YAML: {exc}"))
        return None
    return data


def load_json_payload(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid JSON: {exc}"))
        return None


def load_live_orchestrator_class_ids(issues: list[ValidationIssue]) -> set[str] | None:
    catalog_path = AOA_AGENTS_ROOT / ORCHESTRATOR_CLASS_CATALOG_NAME
    if not AOA_AGENTS_ROOT.exists():
        return None
    payload = load_json_payload(catalog_path, issues)
    if not isinstance(payload, dict):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, AOA_AGENTS_ROOT),
                "orchestrator class catalog must be an object",
            )
        )
        return set()
    entries = payload.get("orchestrator_classes")
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, AOA_AGENTS_ROOT),
                "orchestrator class catalog must expose an orchestrator_classes list",
            )
        )
        return set()
    class_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, AOA_AGENTS_ROOT)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must be an object",
                )
            )
            continue
        class_id = entry.get("id")
        if not isinstance(class_id, str) or not class_id:
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, AOA_AGENTS_ROOT)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must expose a string id",
                )
            )
            continue
        class_ids.add(class_id)
    return class_ids


def validate_orchestrator_class_ref(
    orchestrator_class_ref: object,
    *,
    location: str,
    issues: list[ValidationIssue],
    live_class_ids: set[str] | None,
) -> str | None:
    if not isinstance(orchestrator_class_ref, str):
        issues.append(ValidationIssue(location, "quest orchestrator_class_ref must be a string"))
        return None
    repo_name, separator, class_id = orchestrator_class_ref.partition(":")
    if separator != ":" or repo_name != "aoa-agents" or not class_id:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must use the form 'aoa-agents:<class_id>'",
            )
        )
        return None
    if live_class_ids is not None and class_id not in live_class_ids:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must resolve in aoa-agents/generated/orchestrator_class_catalog.min.json",
            )
        )
        return None
    return class_id


def validate_quest_projection_record(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> None:
    schema_path = repo_root / QUEST_SCHEMA_NAME
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"{schema_path.relative_to(repo_root).as_posix()} could not be loaded for quest projection: {exc}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(quest_data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        error_path = format_schema_path(error.absolute_path)
        detail = f" at '{error_path}'" if error_path else ""
        raise ValueError(
            f"{quest_path.relative_to(repo_root).as_posix()} violates {QUEST_SCHEMA_NAME}{detail}: {error.message}"
        )

def quest_sort_key(quest_name: str) -> tuple[int, str]:
    suffix = quest_name.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_name)
    except ValueError:
        return (sys.maxsize, quest_name)


def discover_quest_paths(repo_root: Path) -> list[Path]:
    quests_dir = repo_root / "quests"
    if not quests_dir.is_dir():
        return []
    return sorted(
        {
            path
            for path in quests_dir.rglob("AOA-EV-Q-*.yaml")
            if path.is_file()
        },
        key=lambda path: quest_sort_key(path.stem),
    )


def discover_quest_names(repo_root: Path) -> list[str]:
    quest_names = sorted(
        {path.stem for path in discover_quest_paths(repo_root)},
        key=quest_sort_key,
    )
    if not quest_names:
        return list(FOUNDATION_QUEST_NAMES)
    return quest_names


def missing_foundation_quest_names(quest_names: Iterable[str]) -> list[str]:
    quest_name_set = set(quest_names)
    return [quest_name for quest_name in FOUNDATION_QUEST_NAMES if quest_name not in quest_name_set]


def should_validate_questbook_surface(repo_root: Path) -> bool:
    questbook_paths = (
        repo_root / QUESTBOOK_NAME,
        repo_root / QUESTBOOK_INTEGRATION_NAME,
        repo_root / QUEST_SCHEMA_NAME,
        repo_root / QUEST_DISPATCH_SCHEMA_NAME,
        repo_root / QUEST_CATALOG_EXAMPLE_NAME,
        repo_root / QUEST_DISPATCH_EXAMPLE_NAME,
    )
    if any(path.exists() for path in questbook_paths):
        return True
    return bool(discover_quest_paths(repo_root))


def quest_source_path_shape_issue(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> str | None:
    relative_path = quest_path.relative_to(repo_root).as_posix()
    parts = quest_path.relative_to(repo_root).parts
    if len(parts) != 4 or parts[0] != "quests" or not parts[3].endswith(".yaml"):
        return "quest source path must use quests/<lane>/<state>/<quest-id>.yaml"
    lane = parts[1]
    state = parts[2]
    if lane not in QUEST_SOURCE_LANES:
        allowed = ", ".join(QUEST_SOURCE_LANES)
        return f"quest lane '{lane}' is not allowed; expected one of: {allowed}"
    if state not in QUEST_SOURCE_STATES:
        allowed = ", ".join(QUEST_SOURCE_STATES)
        return f"quest state directory '{state}' is not allowed; expected one of: {allowed}"
    quest_state = quest_data.get("state")
    if isinstance(quest_state, str) and state != quest_state:
        return f"quest state directory '{state}' must match state '{quest_state}'"
    if quest_path.stem != quest_data.get("id"):
        return f"quest source filename in {relative_path} must match quest id"
    return None


def validate_quest_schema_envelope(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    expected_title: str,
    expected_schema_version: str,
) -> bool:
    if not validate_inline_schema(schema, location=location, issues=issues):
        return False
    if not isinstance(schema, dict):
        return False

    ok = True
    if schema.get("title") != expected_title:
        issues.append(
            ValidationIssue(location, f"schema title must be '{expected_title}'")
        )
        ok = False
    if schema.get("type") != "object":
        issues.append(ValidationIssue(location, "schema must describe an object"))
        ok = False
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(location, "schema must forbid additional properties")
        )
        ok = False
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(ValidationIssue(location, "schema properties must be an object"))
        return False
    schema_version = properties.get("schema_version")
    if not isinstance(schema_version, dict) or schema_version.get("const") != expected_schema_version:
        issues.append(
            ValidationIssue(
                location,
                f"schema_version must be a const of '{expected_schema_version}'",
            )
        )
        ok = False
    required = schema.get("required")
    if not isinstance(required, list):
        issues.append(ValidationIssue(location, "schema required list is missing"))
        ok = False
    else:
        for field in ("schema_version", "id", "public_safe"):
            if field not in required:
                issues.append(
                    ValidationIssue(location, f"schema must require '{field}'")
                )
                ok = False
    return ok


def validate_quest_lifecycle_surface(
    repo_root: Path,
    quest_schema: dict[str, Any] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    lifecycle_text = require_tokens(
        repo_root=repo_root,
        path_name=QUEST_LIFECYCLE_NAME,
        tokens=QUEST_LIFECYCLE_REQUIRED_TOKENS,
        issues=issues,
    )
    if not lifecycle_text:
        return issues

    schema_states: list[str] = []
    if isinstance(quest_schema, dict):
        properties = quest_schema.get("properties")
        if isinstance(properties, dict):
            state_schema = properties.get("state")
            if isinstance(state_schema, dict):
                raw_enum = state_schema.get("enum")
                if isinstance(raw_enum, list):
                    schema_states = [item for item in raw_enum if isinstance(item, str)]
    if not schema_states:
        schema_states = list(QUEST_SOURCE_STATES)

    if tuple(schema_states) != QUEST_SOURCE_STATES:
        issues.append(
            ValidationIssue(
                QUEST_SCHEMA_NAME,
                "quest state enum must match the lifecycle state order",
            )
        )

    for state in schema_states:
        table_token = f"| `{state}` |"
        if table_token not in lifecycle_text:
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"quest lifecycle matrix must include state '{state}'",
                )
            )

    for state in sorted(CLOSED_QUEST_STATES):
        if f"`{state}` | closed; not listed as open" not in lifecycle_text:
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"closed state '{state}' must be marked closed in the lifecycle matrix",
                )
            )
    for state in QUEST_SOURCE_STATES:
        if (
            state not in CLOSED_QUEST_STATES
            and f"| `{state}` | listed in `QUESTBOOK.md`" not in lifecycle_text
        ):
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"open state '{state}' must be marked listed in QUESTBOOK.md",
                )
            )
    return issues


def build_expected_quest_catalog_entry(
    quest: dict[str, Any],
    *,
    source_path: str,
) -> dict[str, Any]:
    entry = {
        "id": quest["id"],
        "title": quest["title"],
        "repo": quest["repo"],
        "theme_ref": quest.get("theme_ref", ""),
        "milestone_ref": quest.get("milestone_ref", ""),
        "state": quest["state"],
        "band": quest["band"],
        "kind": quest["kind"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "owner_surface": quest["owner_surface"],
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    for optional_key in (
        "orchestrator_class_ref",
        "capability_target",
        "playbook_family_refs",
        "proof_surface_refs",
        "memory_surface_refs",
    ):
        if optional_key in quest:
            entry[optional_key] = quest[optional_key]
    return entry


def build_expected_quest_dispatch_entry(
    quest: dict[str, Any],
    *,
    quest_name: str,
    source_path: str,
) -> dict[str, Any]:
    activation = quest.get("activation")
    if not isinstance(activation, dict):
        activation = {}
    requires_artifacts = QUEST_DISPATCH_ARTIFACT_OVERRIDES.get(quest_name)
    if requires_artifacts is None:
        kind = quest.get("kind")
        if kind == "harvest":
            requires_artifacts = ["recurrence_evidence", "promotion_decision"]
        else:
            requires_artifacts = ["bounded_plan", "work_result", "verification_result"]
    entry = {
        "schema_version": QUEST_DISPATCH_SCHEMA_VERSION,
        "id": quest["id"],
        "repo": quest["repo"],
        "state": quest["state"],
        "band": quest["band"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "control_mode": quest["control_mode"],
        "delegate_tier": quest["delegate_tier"],
        "split_required": quest["split_required"],
        "write_scope": quest["write_scope"],
        "requires_artifacts": requires_artifacts,
        "activation_mode": activation.get("mode"),
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    if "fallback_tier" in quest:
        entry["fallback_tier"] = quest.get("fallback_tier")
    if "wrapper_class" in quest:
        entry["wrapper_class"] = quest.get("wrapper_class")
    for optional_key in ("orchestrator_class_ref", "capability_target"):
        if optional_key in quest:
            entry[optional_key] = quest.get(optional_key)
    return entry


def load_quest_projection_records(repo_root: Path) -> list[tuple[str, dict[str, Any], str]]:
    records: list[tuple[str, dict[str, Any], str]] = []
    quest_paths = discover_quest_paths(repo_root)
    if not quest_paths:
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in FOUNDATION_QUEST_NAMES
        ]
    quest_names = [path.stem for path in quest_paths]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    if duplicate_names:
        raise ValueError(f"duplicate quest source id(s): {', '.join(duplicate_names)}")
    missing_foundation = missing_foundation_quest_names(quest_names)
    if missing_foundation:
        missing_display = ", ".join(missing_foundation)
        raise ValueError(f"missing required foundation quest files: {missing_display}")
    for quest_path in quest_paths:
        quest_name = quest_path.stem
        try:
            quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is missing") from exc
        except yaml.YAMLError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is invalid YAML: {exc}") from exc
        if not isinstance(quest_data, dict):
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must be a YAML mapping")
        validate_quest_projection_record(repo_root, quest_path, quest_data)
        shape_issue = quest_source_path_shape_issue(repo_root, quest_path, quest_data)
        if shape_issue is not None:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()}: {shape_issue}")
        if quest_data.get("schema_version") != QUEST_SCHEMA_VERSION:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep schema_version '{QUEST_SCHEMA_VERSION}'")
        if quest_data.get("repo") != "aoa-evals":
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep repo 'aoa-evals'")
        if quest_data.get("id") != quest_name:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep id '{quest_name}'")
        if quest_data.get("public_safe") is not True:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep public_safe true")
        records.append((quest_name, quest_data, quest_path.relative_to(repo_root).as_posix()))
    return records


def build_quest_catalog_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_catalog_entry(quest_data, source_path=source_path)
        for _, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


def build_quest_dispatch_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_dispatch_entry(
            quest_data,
            quest_name=quest_name,
            source_path=source_path,
        )
        for quest_name, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    questbook_path = repo_root / QUESTBOOK_NAME
    integration_path = repo_root / QUESTBOOK_INTEGRATION_NAME
    orchestrator_alignment_path = repo_root / ORCHESTRATOR_PROOF_ALIGNMENT_NAME
    quest_schema_path = repo_root / QUEST_SCHEMA_NAME
    quest_dispatch_schema_path = repo_root / QUEST_DISPATCH_SCHEMA_NAME
    quest_catalog_path = repo_root / QUEST_CATALOG_NAME
    quest_dispatch_path = repo_root / QUEST_DISPATCH_NAME
    quest_catalog_example_path = repo_root / QUEST_CATALOG_EXAMPLE_NAME
    quest_dispatch_example_path = repo_root / QUEST_DISPATCH_EXAMPLE_NAME
    quest_paths = discover_quest_paths(repo_root)
    if quest_paths:
        quest_names = [path.stem for path in quest_paths]
    else:
        quest_names = list(FOUNDATION_QUEST_NAMES)
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in quest_names
        ]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    for quest_name in duplicate_names:
        issues.append(
            ValidationIssue(
                "quests",
                f"duplicate quest source id '{quest_name}'",
            )
        )
    for quest_name in missing_foundation_quest_names(quest_names):
        issues.append(
            ValidationIssue(
                "quests",
                f"missing required foundation quest file '{quest_name}.yaml'",
            )
        )

    questbook_text = read_text_or_issue(questbook_path, issues, root=repo_root)
    integration_text = read_text_or_issue(integration_path, issues, root=repo_root)

    quest_schema = load_json_payload(quest_schema_path, issues)
    if quest_schema is not None:
        validate_quest_schema_envelope(
            quest_schema,
            location=relative_location(quest_schema_path, repo_root),
            issues=issues,
            expected_title=QUEST_SCHEMA_TITLE,
            expected_schema_version=QUEST_SCHEMA_VERSION,
        )
    issues.extend(validate_quest_lifecycle_surface(repo_root, quest_schema))
    quest_dispatch_schema = load_json_payload(quest_dispatch_schema_path, issues)
    if quest_dispatch_schema is not None:
        validate_quest_schema_envelope(
            quest_dispatch_schema,
            location=relative_location(quest_dispatch_schema_path, repo_root),
            issues=issues,
            expected_title=QUEST_DISPATCH_SCHEMA_TITLE,
            expected_schema_version=QUEST_DISPATCH_SCHEMA_VERSION,
        )

    if questbook_text:
        for token in QUESTBOOK_NOTE_REQUIRED_TOKENS:
            if token not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must mention '{token}'",
                    )
                )

    if integration_text:
        for token in QUESTBOOK_INTEGRATION_REQUIRED_TOKENS:
            if token not in integration_text:
                issues.append(
                    ValidationIssue(
                        relative_location(integration_path, repo_root),
                        f"integration note must mention '{token}'",
                    )
                )

    expected_catalog_entries: list[dict[str, Any]] = []
    expected_dispatch_entries: list[dict[str, Any]] = []
    valid_quest_ids: list[str] = []
    active_quest_ids: list[str] = []
    closed_quest_ids: list[str] = []
    live_orchestrator_class_ids: set[str] | None = None
    needs_orchestrator_alignment_doc = False
    for quest_name, quest_path in zip(quest_names, quest_paths, strict=True):
        quest_data = load_yaml_file(quest_path, issues)
        if not isinstance(quest_data, dict):
            continue
        location = relative_location(quest_path, repo_root)
        if not validate_against_schema(quest_data, QUEST_SCHEMA_NAME, location, issues):
            continue
        shape_issue = quest_source_path_shape_issue(repo_root, quest_path, quest_data)
        if shape_issue is not None:
            issues.append(ValidationIssue(location, shape_issue))
        if quest_data.get("schema_version") != QUEST_SCHEMA_VERSION:
            issues.append(
                ValidationIssue(location, f"schema_version must be '{QUEST_SCHEMA_VERSION}'")
            )
        if quest_data.get("repo") != "aoa-evals":
            issues.append(ValidationIssue(location, "quest repo must be 'aoa-evals'"))
        if quest_data.get("id") != quest_name:
            issues.append(
                ValidationIssue(location, f"quest id must match filename '{quest_name}'")
            )
        if quest_data.get("public_safe") is not True:
            issues.append(ValidationIssue(location, "quest must set public_safe to true"))
        orchestrator_class_ref = quest_data.get("orchestrator_class_ref")
        capability_target = quest_data.get("capability_target")
        if orchestrator_class_ref is None and capability_target is not None:
            issues.append(
                ValidationIssue(
                    location,
                    "quest must not declare capability_target without orchestrator_class_ref",
                )
            )
        if orchestrator_class_ref is not None:
            needs_orchestrator_alignment_doc = True
            if live_orchestrator_class_ids is None:
                live_orchestrator_class_ids = load_live_orchestrator_class_ids(issues)
            validate_orchestrator_class_ref(
                orchestrator_class_ref,
                location=location,
                issues=issues,
                live_class_ids=live_orchestrator_class_ids,
            )
            if capability_target not in ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS:
                issues.append(
                    ValidationIssue(
                        location,
                        "quest capability_target must resolve to a supported orchestrator capability",
                    )
                )
        expected_orchestrator_pair = ORCHESTRATOR_PROOF_QUESTS.get(quest_name)
        if expected_orchestrator_pair is not None:
            expected_ref, expected_target = expected_orchestrator_pair
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "orchestrator proof quests must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != ORCHESTRATOR_PROOF_ALIGNMENT_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quests must keep owner_surface {ORCHESTRATOR_PROOF_ALIGNMENT_NAME}",
                    )
                )
            if orchestrator_class_ref != expected_ref:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quest must keep orchestrator_class_ref '{expected_ref}'",
                    )
                )
            if capability_target != expected_target:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quest must keep capability_target '{expected_target}'",
                    )
                )
        if quest_name == "AOA-EV-Q-0005":
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "progression evidence quest must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != PROGRESSION_EVIDENCE_MODEL_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"progression evidence quest must keep owner_surface {PROGRESSION_EVIDENCE_MODEL_NAME}",
                    )
                )
        if quest_name == "AOA-EV-Q-0009":
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "unlock proof bridge quest must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != UNLOCK_PROOF_BRIDGE_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"unlock proof bridge quest must keep owner_surface {UNLOCK_PROOF_BRIDGE_NAME}",
                    )
                )
        if quest_data.get("state") in CLOSED_QUEST_STATES:
            closed_quest_ids.append(quest_name)
        else:
            active_quest_ids.append(quest_name)

        if quest_data.get("id") != quest_name:
            continue
        source_path = quest_path.relative_to(repo_root).as_posix()
        valid_quest_ids.append(quest_name)
        expected_catalog_entries.append(
            build_expected_quest_catalog_entry(quest_data, source_path=source_path)
        )
        expected_dispatch_entries.append(
            build_expected_quest_dispatch_entry(
                quest_data,
                quest_name=quest_name,
                source_path=source_path,
            )
        )

    if orchestrator_alignment_path.exists():
        needs_orchestrator_alignment_doc = True
    if needs_orchestrator_alignment_doc:
        orchestrator_doc_text = read_text_or_issue(
            orchestrator_alignment_path,
            issues,
            root=repo_root,
        )
        if orchestrator_doc_text:
            for token in ORCHESTRATOR_PROOF_REQUIRED_TOKENS:
                if token not in orchestrator_doc_text:
                    issues.append(
                        ValidationIssue(
                            relative_location(orchestrator_alignment_path, repo_root),
                            f"orchestrator proof alignment note must mention '{token}'",
                        )
                    )

    if "AOA-EV-Q-0009" in valid_quest_ids:
        issues.extend(validate_unlock_proof_bridge_surface(repo_root))

    if questbook_text:
        for quest_name in active_quest_ids:
            if quest_name not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must reference active quest id '{quest_name}'",
                    )
                )
        for quest_name in closed_quest_ids:
            if quest_name in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must not list closed quest id '{quest_name}'",
                    )
                )

    expected_catalog_by_id = {
        entry["id"]: entry for entry in expected_catalog_entries
    }
    actual_live_catalog = load_json_payload(quest_catalog_path, issues)
    actual_live_catalog_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(actual_live_catalog, list):
        unexpected_ids: list[str] = []
        for item in actual_live_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_live_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    f"generated quest catalog has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_live_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    "generated quest catalog is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_path, repo_root),
                "generated quest catalog must be an array",
            )
        )
    actual_catalog = load_json_payload(quest_catalog_example_path, issues)
    if isinstance(actual_catalog, list):
        actual_catalog_by_id: dict[str, dict[str, Any]] = {}
        unexpected_ids: list[str] = []
        for item in actual_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    f"generated quest catalog example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example is out of date or mismatched",
                )
            )
        elif any(
            actual_catalog_by_id.get(quest_id) != actual_live_catalog_by_id.get(quest_id)
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example must match generated quest catalog",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_example_path, repo_root),
                "generated quest catalog example must be an array",
            )
        )
    expected_dispatch_by_id = {
        entry["id"]: entry for entry in expected_dispatch_entries
    }
    actual_live_dispatch = load_json_payload(quest_dispatch_path, issues)
    actual_live_dispatch_by_id: dict[str, dict[str, Any]] = {}
    invalid_live_dispatch_ids: set[str] = set()
    if isinstance(actual_live_dispatch, list):
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_live_dispatch):
            location = f"{relative_location(quest_dispatch_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_live_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_live_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    f"generated quest dispatch has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_live_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_live_dispatch_ids
        ]
        if any(
            actual_live_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_live_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    "generated quest dispatch is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_path, repo_root),
                "generated quest dispatch must be an array",
            )
        )
    actual_dispatch = load_json_payload(quest_dispatch_example_path, issues)
    if isinstance(actual_dispatch, list):
        actual_dispatch_by_id: dict[str, dict[str, Any]] = {}
        invalid_example_dispatch_ids: set[str] = set()
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_dispatch):
            location = f"{relative_location(quest_dispatch_example_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_example_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    f"generated quest dispatch example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_example_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_example_dispatch_ids
        ]
        if any(
            actual_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example is out of date or mismatched",
                )
            )
        elif any(
            actual_dispatch_by_id.get(quest_id) != actual_live_dispatch_by_id.get(quest_id)
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example must match generated quest dispatch",
                )
            )
        else:
            for quest_id in comparable_example_dispatch_ids:
                item = actual_dispatch_by_id.get(quest_id)
                if item is None:
                    continue
                requires_artifacts = item.get("requires_artifacts")
                if not isinstance(requires_artifacts, list) or not requires_artifacts:
                    issues.append(
                        ValidationIssue(
                            relative_location(quest_dispatch_example_path, repo_root),
                            "dispatch example must keep requires_artifacts as a non-empty example-only list",
                        )
                    )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_example_path, repo_root),
                "generated quest dispatch example must be an array",
            )
        )

    return issues


def validate_unlock_proof_bridge_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    progression_doc_path = repo_root / PROGRESSION_EVIDENCE_MODEL_NAME
    progression_schema_path = repo_root / PROGRESSION_EVIDENCE_SCHEMA_NAME
    progression_example_path = repo_root / PROGRESSION_EVIDENCE_EXAMPLE_NAME
    doc_path = repo_root / UNLOCK_PROOF_BRIDGE_NAME
    schema_path = repo_root / UNLOCK_PROOF_SCHEMA_NAME
    example_path = repo_root / UNLOCK_PROOF_EXAMPLE_NAME

    progression_doc_text = read_text_or_issue(
        progression_doc_path,
        issues,
        root=repo_root,
    )
    if progression_doc_text:
        for token in PROGRESSION_EVIDENCE_REQUIRED_TOKENS:
            if token not in progression_doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(progression_doc_path, repo_root),
                        f"progression evidence note must mention '{token}'",
                    )
                )

    progression_schema_payload = load_json_payload(progression_schema_path, issues)
    if isinstance(progression_schema_payload, dict):
        if progression_schema_payload.get("title") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    "progression evidence schema title must be 'progression_evidence_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(progression_schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif progression_schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_schema_path, repo_root),
                "progression evidence schema must be a JSON object",
            )
        )

    progression_example_payload = load_json_payload(progression_example_path, issues)
    if isinstance(progression_example_payload, dict):
        validate_against_schema(
            progression_example_payload,
            PROGRESSION_EVIDENCE_SCHEMA_NAME,
            relative_location(progression_example_path, repo_root),
            issues,
        )
        if progression_example_payload.get("schema_version") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example schema_version must be 'progression_evidence_v1'",
                )
            )
        if progression_example_payload.get("public_safe") is not True:
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep public_safe true",
                )
            )
        if not progression_example_payload.get("cautions"):
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep cautions explicit",
                )
            )
    elif progression_example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_example_path, repo_root),
                "progression evidence example must be a JSON object",
            )
        )

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in UNLOCK_PROOF_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"unlock proof bridge note must mention '{token}'",
                    )
                )

    schema_payload = load_json_payload(schema_path, issues)
    if isinstance(schema_payload, dict):
        if schema_payload.get("title") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    "unlock proof schema title must be 'unlock_proof_catalog_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(schema_path, repo_root),
                "unlock proof schema must be a JSON object",
            )
        )

    example_text = read_text_or_issue(example_path, issues, root=repo_root)
    example_payload = load_json_payload(example_path, issues)
    if isinstance(example_payload, dict):
        validate_against_schema(
            example_payload,
            UNLOCK_PROOF_SCHEMA_NAME,
            relative_location(example_path, repo_root),
            issues,
        )
        if example_payload.get("schema_version") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example schema_version must be 'unlock_proof_catalog_v1'",
                )
            )
        proofs = example_payload.get("proofs")
        if not isinstance(proofs, list) or not proofs:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must expose a non-empty proofs list",
                )
            )
        else:
            for index, proof in enumerate(proofs):
                if not isinstance(proof, dict):
                    continue
                if proof.get("public_safe") is not True:
                    issues.append(
                        ValidationIssue(
                            f"{relative_location(example_path, repo_root)}.proofs[{index}]",
                            "unlock proof example entries must keep public_safe true",
                        )
                    )
        if example_payload.get("notes") and "Example only." not in str(example_payload.get("notes")):
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example notes must keep example-only posture explicit",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "unlock proof example must be a JSON object",
            )
        )

    if example_text:
        if "AOA-PB-Q-0004" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not keep legacy playbook quest id 'AOA-PB-Q-0004'",
                )
            )
        if "AOA-EV-PROG-0002" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not reference missing progression evidence id 'AOA-EV-PROG-0002'",
                )
            )

    return issues


def validate_eval_result_receipt_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_path = repo_root / EVAL_RESULT_RECEIPT_GUIDE_NAME
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    payload_schema_path = repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    example_path = repo_root / EVAL_RESULT_RECEIPT_EXAMPLE_NAME

    guide_text = read_text_or_issue(guide_path, issues, root=repo_root)
    if guide_text:
        for token in EVAL_RESULT_RECEIPT_REQUIRED_TOKENS:
            if token not in guide_text:
                issues.append(
                    ValidationIssue(
                        relative_location(guide_path, repo_root),
                        f"eval result receipt guide must mention '{token}'",
                    )
                )

    envelope_schema = load_json_payload(envelope_schema_path, issues)
    envelope_validator: Draft202012Validator | None = None
    if isinstance(envelope_schema, dict):
        envelope_schema_valid = True
        if envelope_schema.get("title") != "aoa-evals stats event envelope":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope schema title must be 'aoa-evals stats event envelope'",
                )
            )
            envelope_schema_valid = False
        canonical_schema_ref = envelope_schema.get("x-canonical_schema_ref")
        if canonical_schema_ref != "repo:aoa-stats/schemas/stats-event-envelope.schema.json":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope mirror must point to repo:aoa-stats/schemas/stats-event-envelope.schema.json",
                )
            )
            envelope_schema_valid = False
        canonical_envelope_path = AOA_STATS_ROOT / SCHEMAS_DIR_NAME / STATS_EVENT_ENVELOPE_SCHEMA_NAME
        if canonical_envelope_path.exists():
            canonical_envelope = load_json_payload(canonical_envelope_path, issues)
            if isinstance(canonical_envelope, dict):
                local_enum = (
                    envelope_schema.get("properties", {})
                    .get("event_kind", {})
                    .get("enum")
                )
                canonical_enum = (
                    canonical_envelope.get("properties", {})
                    .get("event_kind", {})
                    .get("enum")
                )
                if local_enum != canonical_enum:
                    issues.append(
                        ValidationIssue(
                            relative_location(envelope_schema_path, repo_root),
                            "stats event envelope mirror enum must match ../aoa-stats/schemas/stats-event-envelope.schema.json",
                        )
                    )
        try:
            Draft202012Validator.check_schema(envelope_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            envelope_schema_valid = False
        if envelope_schema_valid:
            envelope_validator = get_schema_validator_with_format(envelope_schema)
    elif envelope_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(envelope_schema_path, repo_root),
                "stats event envelope schema must be a JSON object",
            )
        )

    payload_schema = load_json_payload(payload_schema_path, issues)
    payload_validator: Draft202012Validator | None = None
    if isinstance(payload_schema, dict):
        payload_schema_valid = True
        if payload_schema.get("title") != "aoa-evals eval result receipt":
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    "eval result receipt schema title must be 'aoa-evals eval result receipt'",
                )
            )
            payload_schema_valid = False
        try:
            Draft202012Validator.check_schema(payload_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            payload_schema_valid = False
        if payload_schema_valid:
            payload_validator = get_schema_validator_with_format(payload_schema)
    elif payload_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(payload_schema_path, repo_root),
                "eval result receipt schema must be a JSON object",
            )
        )

    example_payload = load_json_payload(example_path, issues)
    if isinstance(example_payload, dict):
        if envelope_validator is not None:
            validate_against_schema(
                example_payload,
                STATS_EVENT_ENVELOPE_SCHEMA_NAME,
                relative_location(example_path, repo_root),
                issues,
                validator=envelope_validator,
            )
        if example_payload.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must keep event_kind as 'eval_result_receipt'",
                )
            )

        object_ref = example_payload.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = example_payload.get("evidence_refs")
        seen_primary = False
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                ref = evidence_ref.get("ref")
                if isinstance(ref, str):
                    parse_repo_ref(
                        ref,
                        location=f"{relative_location(example_path, repo_root)}.evidence_refs[{index}].ref",
                        issues=issues,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
        if not seen_primary:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must include one primary evidence ref",
                )
            )

        payload = example_payload.get("payload")
        if isinstance(payload, dict):
            if payload_validator is not None:
                validate_against_schema(
                    payload,
                    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                    f"{relative_location(example_path, repo_root)}.payload",
                    issues,
                    validator=payload_validator,
                )
            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.bundle_ref",
                    issues=issues,
                )
            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.report_ref",
                    issues=issues,
                )
            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.eval_name must match object_ref.id",
                    )
                )
            if (
                isinstance(report_ref, str)
                and isinstance(evidence_refs, list)
                and report_ref
                not in {
                    entry.get("ref")
                    for entry in evidence_refs
                    if isinstance(entry, dict)
                }
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.report_ref must also appear in evidence_refs",
                    )
                )
            interpretation_bound = payload.get("interpretation_bound")
            if isinstance(interpretation_bound, str) and "Example only." not in interpretation_bound:
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example interpretation_bound must keep example-only posture explicit",
                    )
                )
        else:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example payload must be an object",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "eval result receipt example must be a JSON object",
            )
        )

    return issues


def validate_live_receipt_log(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    log_path = repo_root / LIVE_EVAL_RECEIPT_LOG_NAME
    log_location = relative_location(log_path, repo_root)
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    envelope_schema_location = relative_location(envelope_schema_path, repo_root)
    if envelope_schema_path.exists():
        envelope_schema = load_json_payload(envelope_schema_path, issues)
    elif repo_root != REPO_ROOT:
        envelope_schema = load_schema(STATS_EVENT_ENVELOPE_SCHEMA_NAME)
    else:
        envelope_schema = load_json_payload(envelope_schema_path, issues)
    if not isinstance(envelope_schema, dict):
        if envelope_schema is not None:
            issues.append(ValidationIssue(envelope_schema_location, "stats event envelope schema must be a JSON object"))
        return issues
    if not validate_inline_schema(envelope_schema, location=envelope_schema_location, issues=issues):
        return issues
    envelope_validator = get_schema_validator_with_format(envelope_schema)
    try:
        raw_lines = log_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [ValidationIssue(log_location, "file is missing")]

    receipt_count = 0
    seen_event_ids: set[str] = set()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()
        if not line:
            continue

        receipt_count += 1
        entry_location = f"{log_location}:{line_number}"
        try:
            receipt = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(ValidationIssue(entry_location, f"invalid JSON: {exc.msg}"))
            continue
        if not isinstance(receipt, dict):
            issues.append(
                ValidationIssue(entry_location, "live eval receipt log entry must be a JSON object")
            )
            continue

        validate_against_schema(
            receipt,
            STATS_EVENT_ENVELOPE_SCHEMA_NAME,
            entry_location,
            issues,
            validator=envelope_validator,
        )
        if receipt.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "live eval receipt log entry must keep event_kind as 'eval_result_receipt'",
                )
            )

        event_id = receipt.get("event_id")
        if isinstance(event_id, str) and event_id:
            if event_id in seen_event_ids:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        f"duplicate event_id '{event_id}' is not allowed in the live eval receipt log",
                    )
                )
            seen_event_ids.add(event_id)

        object_ref = receipt.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = receipt.get("evidence_refs")
        seen_primary = False
        evidence_ref_values: set[str] = set()
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                raw_ref = evidence_ref.get("ref")
                if isinstance(raw_ref, str):
                    evidence_ref_values.add(raw_ref)
                    parse_repo_ref(
                        raw_ref,
                        location=f"{entry_location}.evidence_refs[{index}].ref",
                        issues=issues,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
            if not seen_primary:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log entry must include one primary evidence ref",
                    )
                )

        payload = receipt.get("payload")
        if isinstance(payload, dict):
            validate_against_schema(
                payload,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{entry_location}.payload",
                issues,
            )

            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{entry_location}.payload.bundle_ref",
                    issues=issues,
                )
                if bundle_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.bundle_ref must also appear in evidence_refs",
                        )
                    )

            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{entry_location}.payload.report_ref",
                    issues=issues,
                )
                if report_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.report_ref must also appear in evidence_refs",
                        )
                    )

            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.eval_name must match object_ref.id",
                    )
                )

            if (
                isinstance(object_ref, dict)
                and isinstance(object_ref.get("version"), str)
                and isinstance(payload.get("bundle_status"), str)
                and payload["bundle_status"] != object_ref["version"]
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.bundle_status must match object_ref.version when version is present",
                    )
                )

    if receipt_count == 0:
        issues.append(
            ValidationIssue(
                log_location,
                "live eval receipt log must contain at least one receipt entry",
            )
        )
    return issues


def load_mapping_entries(
    payload: Any,
    *,
    array_key: str,
    key_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "payload must be an object"))
        return {}
    items = payload.get(array_key)
    if not isinstance(items, list):
        issues.append(ValidationIssue(location, f"missing array '{array_key}'"))
        return {}

    entries: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_location = f"{location}.{array_key}[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(item_location, "entry must be an object"))
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            issues.append(
                ValidationIssue(item_location, f"entry must expose string key '{key_name}'")
            )
            continue
        if key in entries:
            issues.append(
                ValidationIssue(item_location, f"duplicate entry for '{key_name}' value '{key}'")
            )
            continue
        entries[key] = item
    return entries


def validate_inline_schema(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    if not isinstance(schema, dict):
        issues.append(ValidationIssue(location, "schema must parse to an object"))
        return False
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        issues.append(ValidationIssue(location, f"invalid JSON schema: {exc.message}"))
        return False
    return True


def parse_repo_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(
            ValidationIssue(location, "reference must include a repo name and repo-relative path")
        )
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = REPO_REF_ROOTS.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if not repo_root.exists():
        return repo_name, target, anchor or None
    if not target.exists():
        issues.append(
            ValidationIssue(
                location,
                f"reference target does not exist: {repo_name}/{path_text}",
            )
        )
        return None

    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(
                ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'")
            )
            return None
        if anchor not in markdown_anchors(target):
            issues.append(
                ValidationIssue(location, f"markdown anchor does not exist for ref '{raw_ref}'")
            )
            return None

    return repo_name, target, anchor or None


def parse_named_surface_ref(
    raw_ref: Any,
    *,
    prefix_name: str,
    repo_root: Path,
    location: str,
    issues: list[ValidationIssue],
) -> tuple[Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None

    prefix = f"{prefix_name}:"
    if not raw_ref.startswith(prefix):
        issues.append(ValidationIssue(location, f"reference must start with '{prefix}'"))
        return None

    path_text, _, anchor = raw_ref[len(prefix) :].partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if not repo_root.exists():
        return target, anchor or None
    if not target.exists():
        issues.append(
            ValidationIssue(
                location,
                f"reference target does not exist: {prefix_name}/{path_text}",
            )
        )
        return None
    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(
                ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'")
            )
            return None
        if anchor not in markdown_anchors(target):
            issues.append(
                ValidationIssue(
                    location,
                    f"anchor '{anchor}' was not found in {prefix_name}/{path_text}",
                )
            )
            return None

    return target, anchor or None


def _abyss_stack_ref_boundary_message(allowed_roots: Sequence[str]) -> str:
    if tuple(allowed_roots) == ("Logs",):
        return "reference must stay inside 'repo:abyss-stack/Logs/'"
    if len(allowed_roots) == 1:
        return f"reference must stay inside 'repo:abyss-stack/{allowed_roots[0]}/'"
    allowed_text = " or ".join(f"'repo:abyss-stack/{root}/'" for root in allowed_roots)
    return f"reference must stay inside {allowed_text}"


def validate_abyss_stack_ref(
    raw_ref: Any,
    *,
    allowed_roots: Sequence[str] = ("Logs",),
    location: str,
    issues: list[ValidationIssue],
) -> PurePosixPath | None:
    boundary_message = _abyss_stack_ref_boundary_message(allowed_roots)
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if "#" in raw_ref:
        issues.append(ValidationIssue(location, "operational evidence refs must not include markdown anchors"))
        return None
    if "\\" in raw_ref:
        issues.append(ValidationIssue(location, "reference must use forward slashes"))
        return None
    if not raw_ref.startswith("repo:abyss-stack/"):
        issues.append(ValidationIssue(location, boundary_message))
        return None

    path_text = raw_ref[len("repo:abyss-stack/") :]
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    ref_path = PurePosixPath(path_text)
    if ref_path.is_absolute():
        issues.append(ValidationIssue(location, "reference path must be repo-relative"))
        return None
    if any(part in {"", ".", ".."} for part in ref_path.parts):
        issues.append(ValidationIssue(location, "reference path must not contain empty, '.' or '..' segments"))
        return None
    if len(ref_path.parts) < 2 or ref_path.parts[0] not in set(allowed_roots):
        issues.append(ValidationIssue(location, boundary_message))
        return None

    return ref_path


def validate_abyss_stack_logs_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> PurePosixPath | None:
    return validate_abyss_stack_ref(
        raw_ref,
        allowed_roots=("Logs",),
        location=location,
        issues=issues,
    )


def validate_json_against_inline_schema(
    data: Any,
    schema: dict[str, Any],
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = Draft202012Validator(schema)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"report violation at '{error_path}': {error.message}"
        else:
            message = f"report violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def requires_materialized_comparison_artifacts(manifest: dict[str, Any] | None) -> bool:
    if not isinstance(manifest, dict):
        return False
    return (
        manifest.get("report_format") == "comparative-summary"
        and manifest.get("baseline_mode") != "none"
    )


def validate_repo_relative_contract_path(
    repo_root: Path,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    normalized_path = ensure_repo_relative_path(raw_path, location, issues)
    if not normalized_path:
        return None
    resolved_path = repo_root / normalized_path
    if not resolved_path.exists():
        issues.append(
            ValidationIssue(
                location,
                f"path '{normalized_path}' does not exist",
            )
        )
        return None
    return normalized_path


def validate_raw_repo_relative_path(
    raw_value: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_value, str):
        return None
    normalized_path = ensure_repo_relative_path(raw_value, location, issues)
    return normalized_path or None


def validate_raw_repo_relative_path_list(
    payload: dict[str, Any],
    key: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> list[str]:
    raw_values = payload.get(key, [])
    if not isinstance(raw_values, list):
        return []

    normalized_paths: list[str] = []
    for index, raw_value in enumerate(raw_values):
        normalized_path = validate_raw_repo_relative_path(
            raw_value,
            location=f"{location}.{key}[{index}]",
            issues=issues,
        )
        if normalized_path is not None:
            normalized_paths.append(normalized_path)
    return normalized_paths


def validate_comparison_eval_target(
    raw_name: Any,
    *,
    location: str,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_name, str) or not raw_name:
        issues.append(
            ValidationIssue(location, "comparison target must be a non-empty eval name")
        )
        return None
    if raw_name not in known_eval_names:
        issues.append(
            ValidationIssue(location, f"comparison target '{raw_name}' does not exist")
        )
        return None
    return raw_name


def validate_comparison_surface_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any],
    *,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> None:
    baseline_mode = manifest.get("baseline_mode")
    if baseline_mode == "none":
        return

    location = relative_location(bundle_dir / "eval.yaml", repo_root)
    comparison_surface = manifest.get("comparison_surface")
    if not isinstance(comparison_surface, dict):
        issues.append(
            ValidationIssue(
                location,
                "comparison bundle must define comparison_surface in eval.yaml",
            )
        )
        return

    allowed_keys = COMPARISON_SURFACE_ALLOWED_KEYS.get(baseline_mode, set())
    unexpected_keys = sorted(set(comparison_surface) - allowed_keys)
    if unexpected_keys:
        issues.append(
            ValidationIssue(
                location,
                f"comparison_surface has unexpected keys for baseline_mode '{baseline_mode}': {', '.join(unexpected_keys)}",
            )
        )

    shared_family_path = comparison_surface.get("shared_family_path")
    normalized_shared_family_path = None
    if isinstance(shared_family_path, str):
        normalized_shared_family_path = validate_repo_relative_contract_path(
            repo_root,
            shared_family_path,
            location=f"{location}.comparison_surface.shared_family_path",
            issues=issues,
        )

    paired_readout_path = comparison_surface.get("paired_readout_path")
    normalized_paired_readout_path = None
    if isinstance(paired_readout_path, str):
        normalized_paired_readout_path = validate_repo_relative_contract_path(
            repo_root,
            paired_readout_path,
            location=f"{location}.comparison_surface.paired_readout_path",
            issues=issues,
        )

    integrity_sidecar = comparison_surface.get("integrity_sidecar")
    validate_comparison_eval_target(
        integrity_sidecar,
        location=f"{location}.comparison_surface.integrity_sidecar",
        known_eval_names=known_eval_names,
        issues=issues,
    )

    if baseline_mode in {"fixed-baseline", "previous-version", "longitudinal-window"}:
        validate_comparison_eval_target(
            comparison_surface.get("anchor_surface"),
            location=f"{location}.comparison_surface.anchor_surface",
            known_eval_names=known_eval_names,
            issues=issues,
        )

    if baseline_mode == "peer-compare":
        raw_peer_surfaces = comparison_surface.get("peer_surfaces")
        if not isinstance(raw_peer_surfaces, list):
            issues.append(
                ValidationIssue(
                    f"{location}.comparison_surface.peer_surfaces",
                    "peer_surfaces must be a list",
                )
            )
        else:
            for index, raw_name in enumerate(raw_peer_surfaces):
                validate_comparison_eval_target(
                    raw_name,
                    location=f"{location}.comparison_surface.peer_surfaces[{index}]",
                    known_eval_names=known_eval_names,
                    issues=issues,
                )

    fixture_contract_path = bundle_dir / "fixtures" / "contract.json"
    fixture_contract = eval_catalog_contract.load_optional_json(fixture_contract_path)
    if isinstance(fixture_contract, dict):
        fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(
            fixture_contract
        )
        fixture_family_path = fixture_family_paths[0] if fixture_family_paths else None
        if (
            isinstance(fixture_family_path, str)
            and normalized_shared_family_path is not None
            and fixture_family_path.replace("\\", "/") != normalized_shared_family_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.shared_family_path must match fixtures/contract.json shared_fixture_family_path",
                )
            )

    runner_contract_path = bundle_dir / "runners" / "contract.json"
    runner_contract = eval_catalog_contract.load_optional_json(runner_contract_path)
    if isinstance(runner_contract, dict):
        paired_readout_paths = eval_proof_contract_helpers.collect_paired_readout_paths(
            runner_contract
        )
        runner_paired_readout_path = paired_readout_paths[0] if paired_readout_paths else None
        if (
            isinstance(runner_paired_readout_path, str)
            and normalized_paired_readout_path is not None
            and runner_paired_readout_path.replace("\\", "/") != normalized_paired_readout_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.paired_readout_path must match runners/contract.json paired_readout_path",
                )
            )


def parse_eval_markdown(
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    try:
        text = eval_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(eval_md_path), "file is missing"))
        return None, {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, {}

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, {}

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, {}

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, {}

    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in body.splitlines():
        heading_match = re.match(r"^##\s+(.+?)\s*$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return metadata, sections


def find_support_artifacts(bundle_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    for folder_name in ("examples", "checks", "notes"):
        folder = bundle_dir / folder_name
        if folder.is_dir():
            artifacts.extend(sorted(folder.glob("*.md")))
    return artifacts


def resolve_manifest_path(bundle_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return bundle_dir / candidate


def normalize_repo_name(raw: str) -> str:
    return eval_catalog_contract.normalize_repo_name(raw)


def is_repo_relative_path(raw_path: str) -> bool:
    return eval_catalog_contract.is_repo_relative_path(raw_path)


def ensure_repo_relative_path(raw_path: str, location: str, issues: list[ValidationIssue]) -> str:
    value, contract_issues = eval_catalog_contract.ensure_repo_relative_path(raw_path, location)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return value


def extract_table_eval_names(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start_index = next(
            index for index, line in enumerate(lines) if line.strip() == heading
        )
    except StopIteration:
        return []

    table_lines: list[str] = []
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines and not stripped:
            break
        if table_lines:
            break

    pattern = re.compile(r"^\|\s*(aoa-[a-z0-9-]+)\s*\|")
    return [
        pattern.match(line).group(1)
        for line in table_lines
        if pattern.match(line)
    ]


def load_starter_eval_names(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> list[str]:
    index_path = repo_root / EVAL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))
        return []

    starter_names = extract_table_eval_names(text, "## Starter eval bundles")
    if not starter_names:
        issues.append(
            ValidationIssue(
                relative_location(index_path, repo_root),
                "missing or empty 'Starter eval bundles' table",
            )
        )
    return starter_names


def has_evidence_kind(evidence: Sequence[dict[str, Any]], kind: str) -> bool:
    return any(item.get("kind") == kind for item in evidence)


def load_evidence_texts(
    bundle_dir: Path,
    evidence: Sequence[dict[str, Any]],
    *,
    kind: str,
) -> list[str]:
    texts: list[str] = []
    for item in evidence:
        if item.get("kind") != kind:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.is_file():
            continue
        try:
            texts.append(resolved_path.read_text(encoding="utf-8").lower())
        except OSError:
            continue
    return texts


def contains_phrase_group(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def validate_status_specific_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    required_evidence_by_status = {
        "portable": ("portable_review",),
        "baseline": ("portable_review",),
        "canonical": ("portable_review", "canonical_readiness"),
    }
    status = manifest.get("status")
    for kind in required_evidence_by_status.get(status, ()):
        if not has_evidence_kind(evidence, kind):
            issues.append(
                ValidationIssue(
                    location,
                    f"status '{status}' requires an evidence entry with kind '{kind}'",
                )
            )

    if status == "bounded":
        support_note_text = "\n".join(
            load_evidence_texts(bundle_dir, evidence, kind="support_note")
        )
        if not support_note_text:
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires an evidence entry with kind 'support_note'",
                )
            )
            return

        phrase_groups = (
            ("approve for bounded", "approve for bounded promotion"),
            ("readout",),
            ("failure",),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions",
                )
            )


def validate_status_portability_monotonicity(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    required_portability_by_status = {
        "draft": "local-shaped",
        "bounded": "local-shaped",
        "portable": "portable",
        "baseline": "portable",
        "canonical": "broad",
    }
    status = manifest.get("status")
    portability_level = manifest.get("portability_level")
    required_portability = required_portability_by_status.get(status)
    if required_portability is None:
        return
    if portability_level != required_portability:
        issues.append(
            ValidationIssue(
                location,
                f"status '{status}' requires portability_level '{required_portability}' but found '{portability_level}'",
            )
        )


def validate_public_safety_reviewed_at(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    status = manifest.get("status")
    raw_value = manifest.get("public_safety_reviewed_at")
    if raw_value is None:
        if status == "canonical":
            issues.append(
                ValidationIssue(
                    location,
                    "status 'canonical' requires public_safety_reviewed_at with a fresh YYYY-MM-DD review date",
                )
            )
        return

    if not isinstance(raw_value, str) or not raw_value:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a non-empty string",
            )
        )
        return

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_value):
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must use YYYY-MM-DD format",
            )
        )
        return

    try:
        reviewed_date = date.fromisoformat(raw_value)
    except ValueError:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a valid calendar date",
            )
        )
        return
    if reviewed_date > date.today():
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must not be in the future",
            )
        )


def validate_comparative_summary_contract(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    if manifest.get("report_format") != "comparative-summary":
        return

    if not has_evidence_kind(evidence, "support_note"):
        issues.append(
            ValidationIssue(
                location,
                "report_format 'comparative-summary' requires an evidence entry with kind 'support_note'",
            )
        )
        return

    support_note_text = "\n".join(
        load_evidence_texts(bundle_dir, evidence, kind="support_note")
    )
    baseline_mode = manifest.get("baseline_mode")

    if baseline_mode in {"fixed-baseline", "previous-version"}:
        phrase_groups = (
            ("baseline",),
            ("noisy variation",),
            ("style-only", "style only"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must state the baseline target, noisy variation, and style-only overread limits in a support note",
                )
            )
    elif baseline_mode == "peer-compare":
        phrase_groups = (
            ("matched",),
            ("side-by-side", "side by side"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'peer-compare' must state matched conditions and side-by-side interpretation limits in a support note",
                )
            )
    elif baseline_mode == "longitudinal-window":
        phrase_groups = (
            ("ordered",),
            ("window",),
            ("same bounded workflow surface", "anchor workflow surface"),
            ("no clear directional movement", "mixed or unstable movement"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'longitudinal-window' must state ordered windows, cross-window invariants, and cautious movement interpretation in a support note",
                )
            )


def extract_bulleted_eval_names(text: str, label: str) -> list[str]:
    lines = text.splitlines()
    names: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                break
            if not stripped.startswith("- "):
                break
            names.extend(re.findall(r"aoa-[a-z0-9-]+", stripped))
    return names


def validate_eval_frontmatter(
    eval_name: str,
    metadata: dict[str, Any],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_md_path)
    valid = validate_against_schema(metadata, EVAL_FRONTMATTER_SCHEMA_NAME, location, issues)
    if metadata.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )
        valid = False
    return valid


def validate_eval_headings(
    sections: dict[str, str],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_md_path)
    section_pairs, pair_issues = eval_section_contract.extract_section_pairs(
        eval_md_path,
        location=location,
    )
    contract_issues = eval_section_contract.collect_section_contract_issues(
        section_pairs or list(sections.items()),
        location=location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in [*pair_issues, *contract_issues]
    )


def validate_eval_manifest(
    eval_name: str,
    manifest: Any,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_yaml_path)
    if not isinstance(manifest, dict):
        issues.append(ValidationIssue(location, "manifest must parse to a mapping"))
        return False

    valid = validate_against_schema(manifest, EVAL_MANIFEST_SCHEMA_NAME, location, issues)
    if manifest.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "'name' must match the directory name")
        )
        valid = False
    return valid


def validate_manifest_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    evidence = manifest.get("evidence", [])

    for item in evidence:
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.exists():
            issues.append(
                ValidationIssue(
                    location,
                    f"evidence path '{raw_path}' does not exist",
                )
            )

    if manifest.get("baseline_mode") != "none":
        has_baseline_readiness = any(
            item.get("kind") == "baseline_readiness" for item in evidence
        )
        if not has_baseline_readiness:
            issues.append(
                ValidationIssue(
                    location,
                    "baseline_mode is not 'none' but no evidence entry with kind 'baseline_readiness' is present",
                )
            )

    validate_status_portability_monotonicity(manifest, location, issues)
    validate_status_specific_evidence(manifest, bundle_dir, location, evidence, issues)
    validate_public_safety_reviewed_at(manifest, location, issues)
    validate_comparative_summary_contract(
        manifest,
        bundle_dir,
        location,
        evidence,
        issues,
    )


def validate_mirrored_manifest_fields(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    source_location = relative_location(eval_md_path)
    for field_name in MIRRORED_FIELDS:
        if metadata.get(field_name) != manifest.get(field_name):
            issues.append(
                ValidationIssue(
                    location,
                    f"field '{field_name}' does not match {source_location}",
                )
            )


def normalize_technique_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized, contract_issues = eval_catalog_contract.normalize_technique_dependency_refs(
        manifest,
        eval_yaml_path,
        eval_yaml_path.parents[2],
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return normalized


def normalize_skill_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized, contract_issues = eval_catalog_contract.normalize_skill_dependency_refs(
        manifest,
        eval_yaml_path,
        eval_yaml_path.parents[2],
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return normalized


def dependency_repo_root(repo_name: str) -> Path | None:
    if repo_name == "aoa-techniques":
        return AOA_TECHNIQUES_ROOT
    if repo_name == "aoa-skills":
        return AOA_SKILLS_ROOT
    return None


def validate_dependency_target_exists(
    repo_name: str,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not raw_path:
        return

    repo_root = dependency_repo_root(repo_name)
    if repo_root is None or not repo_root.exists():
        return

    target_path = repo_root / raw_path
    if not target_path.is_file():
        issues.append(
            ValidationIssue(
                location,
                f"dependency target does not exist: {repo_name}/{raw_path}",
            )
        )


def validate_dependency_drift(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    frontmatter_techniques = metadata.get("technique_dependencies", [])
    manifest_technique_refs = normalize_technique_dependency_refs(manifest, eval_yaml_path, issues)
    manifest_techniques = [item["id"] for item in manifest_technique_refs]
    if frontmatter_techniques != manifest_techniques:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path),
                f"ordered technique refs do not match {relative_location(eval_md_path)}.technique_dependencies",
            )
        )
    for index, item in enumerate(manifest_technique_refs):
        validate_dependency_target_exists(
            item["repo"],
            item["path"],
            location=f"{relative_location(eval_yaml_path)}.technique_dependencies[{index}].path",
            issues=issues,
        )

    frontmatter_skills = metadata.get("skill_dependencies", [])
    manifest_skill_refs = normalize_skill_dependency_refs(manifest, eval_yaml_path, issues)
    manifest_skills = [item["name"] for item in manifest_skill_refs]
    if frontmatter_skills != manifest_skills:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path),
                f"ordered skill refs do not match {relative_location(eval_md_path)}.skill_dependencies",
            )
        )
    for index, item in enumerate(manifest_skill_refs):
        validate_dependency_target_exists(
            item["repo"],
            item["path"],
            location=f"{relative_location(eval_yaml_path)}.skill_dependencies[{index}].path",
            issues=issues,
        )


def validate_manifest_relations(
    eval_name: str,
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> None:
    seen_pairs: set[tuple[str, str]] = set()
    relations = manifest.get("relations", [])

    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        relation_type = relation.get("type")
        target = relation.get("target")
        if not isinstance(relation_type, str) or not isinstance(target, str):
            continue

        location = f"{relative_location(eval_yaml_path)}.relations[{index}]"
        pair = (relation_type, target)
        if target == eval_name:
            issues.append(
                ValidationIssue(location, "relation target cannot point to the same eval")
            )
        if target not in known_eval_names:
            issues.append(
                ValidationIssue(location, f"relation target '{target}' does not exist")
            )
        if pair in seen_pairs:
            issues.append(
                ValidationIssue(
                    location,
                    f"duplicate relation '{relation_type}' -> '{target}'",
                )
            )
        seen_pairs.add(pair)


def validate_bundle_report_artifacts(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    schema_path = bundle_dir / "reports" / "summary.schema.json"
    example_path = bundle_dir / "reports" / "example-report.json"
    has_schema = schema_path.is_file()
    has_example = example_path.is_file()
    required_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else None
    requires_materialized = requires_materialized_comparison_artifacts(manifest)

    if has_schema and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report schema exists but reports/example-report.json is missing",
            )
        )
    elif requires_materialized and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/example-report.json",
            )
        )

    if has_example and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report example exists but reports/summary.schema.json is missing",
            )
        )
    elif requires_materialized and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/summary.schema.json",
            )
        )

    if not has_schema or not has_example:
        return

    schema_location = relative_location(schema_path, repo_root)
    example_location = relative_location(example_path, repo_root)
    schema_issues: list[ValidationIssue] = []
    schema = load_json_payload(schema_path, schema_issues)
    issues.extend(schema_issues)
    if schema is None or not validate_inline_schema(
        schema,
        location=schema_location,
        issues=issues,
    ):
        return

    example_payload = load_json_payload(example_path, issues)
    if example_payload is None:
        return
    example_valid = validate_json_against_inline_schema(
        example_payload,
        schema,
        location=example_location,
        issues=issues,
    )
    if manifest is not None and manifest.get("report_format") == "comparative-summary":
        validate_comparative_report_mode_contract(
            schema,
            example_payload,
            required_mode=required_mode,
            schema_location=schema_location,
            example_location=example_location,
            issues=issues,
        )
    if example_valid and required_mode == "longitudinal-window":
        validate_longitudinal_report_example(
            example_payload,
            location=example_location,
            issues=issues,
        )

    for report_path in sorted(schema_path.parent.glob("*.report.json")):
        validate_actual_bundle_report_artifact(
            report_path,
            schema,
            repo_root=repo_root,
            manifest=manifest,
            issues=issues,
        )


def validate_actual_bundle_report_artifact(
    report_path: Path,
    schema: dict[str, Any],
    *,
    repo_root: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    report_location = relative_location(report_path, repo_root)
    report_payload = load_json_payload(report_path, issues)
    if report_payload is None:
        return

    validate_json_against_inline_schema(
        report_payload,
        schema,
        location=report_location,
        issues=issues,
    )

    if not isinstance(report_payload, dict) or not isinstance(manifest, dict):
        return

    expected_name = manifest.get("name")
    if isinstance(expected_name, str) and report_payload.get("eval_name") != expected_name:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report eval_name must match manifest name '{expected_name}'",
            )
        )

    expected_status = manifest.get("status")
    if isinstance(expected_status, str) and report_payload.get("bundle_status") != expected_status:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report bundle_status must match manifest status '{expected_status}'",
            )
        )


LONGITUDINAL_GROWTH_CLAIM_PHRASES = (
    "broad capability growth",
    "general capability growth",
)
LONGITUDINAL_GROWTH_NEGATION_CUES = (
    "does not",
    "do not",
    "did not",
    "doesn't",
    "don't",
    "cannot",
    "can't",
    "is not",
    "isn't",
    "not prove",
    "not proven",
    "not support",
    "not supported",
    "not imply",
    "not implied",
    "without proving",
    "without implying",
)
LONGITUDINAL_GROWTH_POST_NEGATION_CUES = (
    "is not proven",
    "is not supported",
    "is not implied",
    "not proven",
    "not supported",
    "not implied",
)


def claim_boundary_overclaims_longitudinal_growth(claim_boundary: str) -> bool:
    clauses = [
        clause.strip()
        for clause in re.split(r"[.;:\n]+", claim_boundary.lower())
        if clause.strip()
    ]
    for clause in clauses:
        for phrase in LONGITUDINAL_GROWTH_CLAIM_PHRASES:
            if phrase not in clause:
                continue
            if clause_negates_longitudinal_growth_phrase(clause, phrase):
                continue
            return True
    return False


def clause_negates_longitudinal_growth_phrase(clause: str, phrase: str) -> bool:
    phrase_index = clause.find(phrase)
    if phrase_index == -1:
        return False

    for cue in LONGITUDINAL_GROWTH_NEGATION_CUES:
        cue_index = clause.find(cue)
        if cue_index == -1:
            continue
        if cue_index <= phrase_index <= cue_index + len(cue) + 80:
            return True

    trailing_window = clause[phrase_index : phrase_index + len(phrase) + 80]
    return any(cue in trailing_window for cue in LONGITUDINAL_GROWTH_POST_NEGATION_CUES)


def validate_longitudinal_report_example(
    example_payload: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(example_payload, dict):
        return

    claim_boundary = example_payload.get("claim_boundary")
    if isinstance(claim_boundary, str):
        if claim_boundary_overclaims_longitudinal_growth(claim_boundary):
            issues.append(
                ValidationIssue(
                    f"{location}.claim_boundary",
                    "longitudinal example report claim_boundary must stay weaker than broad or general capability growth",
                )
            )

    limitations = example_payload.get("limitations")
    if isinstance(limitations, list):
        lowered_limitations = [
            item.lower()
            for item in limitations
            if isinstance(item, str)
        ]
        if not any("general capability growth" in item for item in lowered_limitations):
            issues.append(
                ValidationIssue(
                    f"{location}.limitations",
                    "longitudinal example report limitations must name that the report does not prove general capability growth",
                )
            )

    windows = example_payload.get("windows")
    if not isinstance(windows, list):
        return

    seen_window_ids: set[str] = set()
    last_order: int | None = None
    for index, window in enumerate(windows):
        if not isinstance(window, dict):
            continue

        window_id = window.get("window_id")
        if isinstance(window_id, str):
            if window_id in seen_window_ids:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_id",
                        f"longitudinal example report window_id '{window_id}' must be unique",
                    )
                )
            seen_window_ids.add(window_id)

        window_order = window.get("window_order")
        if isinstance(window_order, int):
            if last_order is not None and window_order <= last_order:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_order",
                        "longitudinal example report window_order values must be strictly increasing",
                    )
                )
            last_order = window_order

        transition_note = window.get("transition_note")
        if index == 0 and transition_note is None:
            continue
        if not isinstance(transition_note, str) or not transition_note.strip():
            issues.append(
                ValidationIssue(
                    f"{location}.windows[{index}].transition_note",
                    "longitudinal example report non-initial windows must include a non-empty transition_note",
                )
            )


def validate_comparative_report_mode_contract(
    schema: dict[str, Any],
    example_payload: Any,
    *,
    required_mode: str | None,
    schema_location: str,
    example_location: str,
    issues: list[ValidationIssue],
) -> None:
    if required_mode is None:
        return

    required_fields = schema.get("required", [])
    if "comparison_mode" not in required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "comparative-summary report schema must require 'comparison_mode'",
            )
        )
    properties = schema.get("properties", {})
    comparison_mode_schema = properties.get("comparison_mode")
    if not isinstance(comparison_mode_schema, dict) or comparison_mode_schema.get("const") != required_mode:
        issues.append(
            ValidationIssue(
                schema_location,
                f"comparative-summary report schema must pin comparison_mode to '{required_mode}'",
            )
        )

    if not isinstance(example_payload, dict):
        return
    if example_payload.get("comparison_mode") != required_mode:
        issues.append(
            ValidationIssue(
                example_location,
                f"comparative-summary report example must set comparison_mode to '{required_mode}'",
            )
        )


def validate_bundle_fixture_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "fixtures" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship fixtures/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, FIXTURE_CONTRACT_SCHEMA_NAME, location, issues):
        return

    validate_raw_repo_relative_path(
        payload.get("shared_fixture_family_path"),
        location=f"{location}.shared_fixture_family_path",
        issues=issues,
    )
    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        location=location,
        issues=issues,
    )
    fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(payload)
    for index, shared_fixture_family_path in enumerate(fixture_family_paths):
        field_name = (
            "shared_fixture_family_path"
            if index == 0
            else f"{eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY}[{index - 1}]"
        )
        validate_repo_relative_contract_path(
            repo_root,
            shared_fixture_family_path,
            location=f"{location}.{field_name}",
            issues=issues,
        )


def validate_bundle_runner_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "runners" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship runners/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, RUNNER_CONTRACT_SCHEMA_NAME, location, issues):
        return

    for field_name in ("runner_surface_path", "report_schema_path", "report_example_path", "paired_readout_path"):
        raw_value = payload.get(field_name)
        if isinstance(raw_value, str):
            validate_repo_relative_contract_path(
                repo_root,
                raw_value,
                location=f"{location}.{field_name}",
                issues=issues,
            )

    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        location=location,
        issues=issues,
    )
    additional_paired_readout_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
    )
    for index, value in enumerate(additional_paired_readout_paths):
        validate_repo_relative_contract_path(
            repo_root,
            value,
            location=(
                f"{location}.{eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY}[{index}]"
            ),
            issues=issues,
        )

    for field_name in ("fixture_contract_paths", "scorer_helper_paths"):
        values = payload.get(field_name, [])
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            if not isinstance(value, str):
                continue
            validate_repo_relative_contract_path(
                repo_root,
                value,
                location=f"{location}.{field_name}[{index}]",
                issues=issues,
            )


def validate_bundle_proof_artifacts(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    validate_bundle_report_artifacts(repo_root, bundle_dir, manifest, issues)
    validate_bundle_fixture_contract(repo_root, bundle_dir, manifest, issues)
    validate_bundle_runner_contract(repo_root, bundle_dir, manifest, issues)


def expected_source_eval_relative_dir(
    eval_name: str,
    manifest: dict[str, Any],
) -> Path | None:
    baseline_mode = manifest.get("baseline_mode")
    family_parts = COMPARISON_FAMILY_BY_BASELINE_MODE.get(str(baseline_mode))
    if family_parts is not None:
        return Path(*family_parts, eval_name)

    category = manifest.get("category")
    if not isinstance(category, str) or not category.strip():
        return None
    return Path(category, eval_name)


def validate_source_eval_tree_location(
    repo_root: Path,
    bundle_dir: Path,
    eval_name: str,
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    expected_relative = expected_source_eval_relative_dir(eval_name, manifest)
    if expected_relative is None:
        return
    try:
        actual_relative = bundle_dir.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
    except ValueError:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"source eval directory must live under {SOURCE_EVALS_DIR_NAME}/",
            )
        )
        return

    if actual_relative != expected_relative:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path, repo_root),
                "source eval directory must match claim-family topology: "
                f"expected {SOURCE_EVALS_DIR_NAME}/{expected_relative.as_posix()}",
            )
        )


def validate_bundle(
    repo_root: Path,
    eval_name: str,
    known_eval_names: set[str],
    eval_dirs: Mapping[str, Path] | None = None,
) -> tuple[list[ValidationIssue], EvalBundleRecord | None]:
    issues: list[ValidationIssue] = []
    eval_dirs = eval_dirs or discover_eval_dirs(repo_root)
    bundle_dir = eval_dirs.get(eval_name, repo_root / SOURCE_EVALS_DIR_NAME / eval_name)
    eval_md_path = bundle_dir / "EVAL.md"
    eval_yaml_path = bundle_dir / "eval.yaml"

    if not bundle_dir.is_dir():
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "source eval package directory is missing",
            )
        )
        return issues, None

    if not eval_md_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_md_path, repo_root), "file is missing"))
    if not eval_yaml_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_yaml_path, repo_root), "file is missing"))

    if not find_support_artifacts(bundle_dir):
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "missing support artifact under examples/*.md, checks/*.md, or notes/*.md",
            )
        )

    metadata: dict[str, Any] | None = None
    manifest: dict[str, Any] | None = None
    sections: dict[str, str] = {}
    frontmatter_valid = False
    manifest_valid = False

    if eval_md_path.is_file():
        metadata, sections = parse_eval_markdown(eval_md_path, issues)
        if metadata is not None:
            frontmatter_valid = validate_eval_frontmatter(eval_name, metadata, eval_md_path, issues)
            validate_eval_headings(sections, eval_md_path, issues)
            capsule_source_issues = eval_capsule_contract.validate_capsule_source_sections(
                sections,
                eval_md_path,
                repo_root,
            )
            issues.extend(
                ValidationIssue(issue.location, issue.message)
                for issue in capsule_source_issues
            )

    if eval_yaml_path.is_file():
        loaded_manifest = load_yaml_file(eval_yaml_path, issues)
        if loaded_manifest is not None:
            manifest_valid = validate_eval_manifest(eval_name, loaded_manifest, eval_yaml_path, issues)
            if isinstance(loaded_manifest, dict):
                manifest = loaded_manifest
                validate_source_eval_tree_location(
                    repo_root,
                    bundle_dir,
                    eval_name,
                    manifest,
                    eval_yaml_path,
                    issues,
                )
                validate_manifest_evidence(manifest, bundle_dir, eval_yaml_path, issues)
                if manifest_valid:
                    validate_comparison_surface_contract(
                        repo_root,
                        bundle_dir,
                        manifest,
                        known_eval_names=known_eval_names,
                        issues=issues,
                    )

    validate_bundle_proof_artifacts(repo_root, bundle_dir, manifest, issues)

    if metadata is not None and manifest is not None and frontmatter_valid and manifest_valid:
        validate_mirrored_manifest_fields(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
        )
        validate_dependency_drift(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
        )
        validate_manifest_relations(
            eval_name,
            manifest,
            eval_yaml_path,
            known_eval_names,
            issues,
        )
        record = EvalBundleRecord(
            name=eval_name,
            bundle_dir=bundle_dir,
            eval_md_path=eval_md_path,
            eval_yaml_path=eval_yaml_path,
            metadata=metadata,
            manifest=manifest,
            sections=sections,
        )
        return issues, record

    return issues, None


def validate_eval_index(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_path = repo_root / EVAL_INDEX_NAME
    location = relative_location(index_path, repo_root)
    counts = Counter(starter_names)

    if selected_evals is None:
        eval_dirs = set(discover_eval_dirs(repo_root))

        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

        starter_set = set(counts.keys())

        for extra in sorted(starter_set - eval_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{extra}' has no matching source eval package directory",
                )
            )
    else:
        for name in sorted(selected_evals):
            count = counts.get(name, 0)
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

    return issues


def validate_eval_selection(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    selection_path = repo_root / EVAL_SELECTION_NAME
    try:
        text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(EVAL_SELECTION_NAME, "file is missing")]

    location = relative_location(selection_path, repo_root)
    names_in_selection = set(re.findall(r"aoa-[a-z0-9-]+", text))
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    issues: list[ValidationIssue] = []

    for token in (
        "# Eval Bundle Selection Chooser",
        "repository-wide chooser for public eval bundles",
    ):
        if token not in text:
            issues.append(
                ValidationIssue(
                    location,
                    f"EVAL_SELECTION.md must mention '{token}'",
                )
            )

    for name in sorted(names_to_check):
        if name not in names_in_selection:
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{name}' is missing from EVAL_SELECTION.md",
                )
            )

    return issues


def validate_starter_bundle_contract(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    eval_dirs = discover_eval_dirs(repo_root)

    for name in sorted(names_to_check):
        bundle_dir = eval_dirs.get(name, repo_root / SOURCE_EVALS_DIR_NAME / name)
        manifest_path = bundle_dir / "eval.yaml"
        location = relative_location(bundle_dir, repo_root)

        example_report = bundle_dir / "examples" / "example-report.md"
        if not example_report.is_file():
            issues.append(
                ValidationIssue(
                    location,
                    "starter bundle is missing examples/example-report.md",
                )
            )

        manifest_issues: list[ValidationIssue] = []
        manifest = load_yaml_file(manifest_path, manifest_issues)
        issues.extend(manifest_issues)
        if not isinstance(manifest, dict):
            continue

        evidence = manifest.get("evidence", [])
        if not evidence:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include at least one manifest evidence entry",
                )
            )
            continue

        has_integrity_check = any(
            item.get("kind") == "integrity_check" for item in evidence
        )
        if not has_integrity_check:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'integrity_check'",
                )
            )

        has_origin_need = any(
            item.get("kind") == "origin_need" for item in evidence
        )
        if not has_origin_need:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'origin_need'",
                )
            )

    return issues


def validate_roadmap_parity(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    roadmap_path = repo_root / ROADMAP_NAME
    try:
        roadmap_text = roadmap_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(ROADMAP_NAME, "file is missing")]

    location = relative_location(roadmap_path, repo_root)
    issues: list[ValidationIssue] = []
    for token in ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS:
        if token not in roadmap_text:
            issues.append(
                ValidationIssue(
                    location,
                    f"ROADMAP.md must include '{token}'",
                )
            )

    starter_set = set(starter_names)
    bundle_names = set(discover_eval_dirs(repo_root))
    current_public_surface_names = set(
        extract_bulleted_eval_names(roadmap_text, "Current public surface:")
    )
    names_to_check = current_public_surface_names
    if selected_evals is not None:
        names_to_check = current_public_surface_names.intersection(selected_evals)

    for name in sorted(names_to_check):
        if name not in bundle_names:
            issues.append(
                ValidationIssue(
                    location,
                    "roadmap 'Current public surface' eval "
                    f"'{name}' has no matching source eval package directory",
                )
            )
            continue
        if name not in starter_set:
            issues.append(
                ValidationIssue(
                    location,
                    f"roadmap 'Current public surface' eval '{name}' must appear in EVAL_INDEX.md starter bundles",
                )
            )

    if selected_evals is not None:
        return issues

    index_path = repo_root / EVAL_INDEX_NAME
    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return issues

    roadmap_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in roadmap_text
    index_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in index_text
    if roadmap_has_absence_note != index_has_absence_note:
        issues.append(
            ValidationIssue(
                location,
                f"absence note '{NO_ADDITIONAL_STARTER_BUNDLES_TEXT}' must stay synchronized with {EVAL_INDEX_NAME}",
            )
        )

    return issues


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    for token in tokens:
        search_text = text
        if part_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join(
                (
                    text,
                    part_validation_route_text(repo_root, path_name),
                )
            )
        elif mechanic_parent_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join(
                (
                    text,
                    mechanic_parent_validation_route_text(repo_root, path_name),
                )
            )
        if token not in search_text:
            issues.append(
                ValidationIssue(path_name, f"file must mention '{token}'")
            )
    return text


def validate_agent_index_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(
        repo_root=repo_root,
        path_name=AGENT_INDEX_NAME,
        tokens=AGENT_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AGENT_INDEX_CHAIN_DECISION_NAME,
        tokens=AGENT_INDEX_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="README.md",
        tokens=(AGENT_INDEX_NAME, "repo to authority class"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/README.md",
        tokens=("AGENT_INDEX.md", "Agent Index", "Mechanics Refactor Path"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(AGENT_INDEX_NAME, "pass-through reader"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=(AGENT_INDEX_NAME, "Agent index chain"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=(AGENT_INDEX_NAME, "agent-facing pass-through index"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(AGENT_INDEX_CHAIN_DECISION_NAME, "Agent Index Chain Surface"),
        issues=issues,
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


def validate_releasing_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root=repo_root,
        path_name="docs/RELEASING.md",
        tokens=RELEASING_ROUTE_MAP_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for stale_phrase in RELEASING_FORBIDDEN_STATUS_LEDGER_TOKENS:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        "docs/RELEASING.md",
                        "release guide must route readiness artifacts to live-status owners instead of stale status-ledger negative wording "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_source_eval_tree_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(
        repo_root=repo_root,
        path_name=SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
        tokens=SOURCE_EVAL_TREE_TOPOLOGY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )

    decision_text = read_text_or_issue(
        repo_root / SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if decision_text and markdown_python_commands(
        markdown_heading_section(decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME,
                "decision validation must route executable commands to evals/AGENTS.md#validation",
            )
        )

    require_tokens(
        repo_root=repo_root,
        path_name=EVALS_AGENTS_NAME,
        tokens=("source-tree topology", *SOURCE_EVAL_TREE_TOPOLOGY_COMMANDS),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME, "Source Eval Tree Topology"),
        issues=issues,
    )

    return issues


def validate_root_readme_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root=repo_root,
        path_name="README.md",
        tokens=ROOT_README_SURFACE_REQUIRED_TOKENS,
        issues=issues,
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
    require_tokens(
        repo_root=repo_root,
        path_name="docs/README.md",
        tokens=(
            "aoa-evals Bounded Proof Canon",
            "Eval Bundle Selection Chooser",
            "Eval Bundle Index",
        ),
        issues=issues,
    )

    return issues


def validate_memory_consumer_proof_boundary_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(
        repo_root=repo_root,
        path_name="README.md",
        tokens=MEMORY_CONSUMER_PROOF_BOUNDARY_README_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/EVAL_PHILOSOPHY.md",
        tokens=MEMORY_CONSUMER_PROOF_BOUNDARY_PHILOSOPHY_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=MEMORY_CONSUMER_PROOF_BOUNDARY_TOPOLOGY_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME,
        tokens=MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MEMORY_CONSUMER_PROOF_BOUNDARY_DECISION_NAME,
            "Memory Consumer Proof Boundary",
        ),
        issues=issues,
    )

    return issues


def validate_eval_philosophy_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root=repo_root,
        path_name="docs/EVAL_PHILOSOPHY.md",
        tokens=EVAL_PHILOSOPHY_ROUTE_MAP_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for stale_phrase in EVAL_PHILOSOPHY_FORBIDDEN_FLAT_NEGATIVE_TOKENS:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        "docs/EVAL_PHILOSOPHY.md",
                        "eval philosophy should route proof pressure through positive distinctions instead of flat negative slogan wording "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_docs_readme_route_map(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root=repo_root,
        path_name="docs/README.md",
        tokens=DOCS_README_ROUTE_MAP_REQUIRED_TOKENS,
        issues=issues,
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

    topology_section = markdown_heading_section(text, "Topology And Route Maps")
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        token = f"../mechanics/{parent_name}/README.md"
        if token not in topology_section:
            issues.append(
                ValidationIssue(
                    "docs/README.md",
                    "docs route map must include every active mechanic parent in Topology And Route Maps; "
                    f"missing {token}",
                )
            )

    return issues


def validate_audit_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(
        repo_root=repo_root,
        path_name="AUDIT.md",
        tokens=AUDIT_SURFACE_ROLE_REQUIRED_TOKENS,
        issues=issues,
    )
    agents_text = require_tokens(
        repo_root=repo_root,
        path_name="AGENTS.md",
        tokens=AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS,
        issues=issues,
    )
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

    text = require_tokens(
        repo_root=repo_root,
        path_name=GITHUB_AGENTS_NAME,
        tokens=GITHUB_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
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
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
            issues=issues,
        )

    return issues


def validate_validator_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    scripts_text = require_tokens(
        repo_root=repo_root,
        path_name="scripts/AGENTS.md",
        tokens=VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS,
        issues=issues,
    )
    tests_text = require_tokens(
        repo_root=repo_root,
        path_name="tests/AGENTS.md",
        tokens=VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS,
        issues=issues,
    )
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
    design_text = require_tokens(
        repo_root=repo_root,
        path_name=DESIGN_NAME,
        tokens=ROOT_DESIGN_REQUIRED_TOKENS,
        issues=issues,
    )
    architecture_text = require_tokens(
        repo_root=repo_root,
        path_name="docs/ARCHITECTURE.md",
        tokens=ARCHITECTURE_REQUIRED_TOKENS,
        issues=issues,
    )
    design_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=DESIGN_AGENTS_NAME,
        tokens=DESIGN_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="AGENTS.md",
        tokens=ROOT_AGENTS_DESIGN_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=DECISION_SURFACE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/TEMPLATE.md",
        tokens=DECISION_TEMPLATE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/AGENTS.md",
        tokens=(
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
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        tokens=ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
        tokens=ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            "Architecture Proof Model Contract",
            ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
            "Active Mechanics Topology Wording",
        ),
        issues=issues,
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
    if architecture_text:
        for stale_phrase in ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS:
            if stale_phrase in architecture_text:
                issues.append(
                    ValidationIssue(
                        "docs/ARCHITECTURE.md",
                        "architecture should route related surfaces positively instead of stale negative role scaffold "
                        f"'{stale_phrase}'",
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
    return issues


def validate_root_route_card_districts(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        district = repo_root / district_name
        if not district.is_dir():
            issues.append(
                ValidationIssue(
                    district_name,
                    "route-card-only root district is missing",
                )
            )
            continue

        allowed = set(allowed_names)
        for allowed_name in allowed_names:
            if not (district / allowed_name).is_file():
                issues.append(
                    ValidationIssue(
                        f"{district_name}/{allowed_name}",
                        "route-card file is missing",
                    )
                )

        for path in sorted(district.rglob("*")):
            relative_name = path.relative_to(district).as_posix()
            if relative_name not in allowed:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "active payload or stray directory must not live in a route-card-only root district",
                    )
                )

    for path_name, tokens in ROOT_ROUTE_CARD_README_REQUIRED_TOKENS.items():
        text = require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
            issues=issues,
        )
        if text:
            first_heading = next(
                (line.strip() for line in text.splitlines() if line.startswith("# ")),
                "",
            )
            if "Route" not in first_heading:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "route-card-only root README heading must name itself as a Route surface",
                    )
                )
            for forbidden_token in ROOT_ROUTE_CARD_README_FORBIDDEN_TOKENS:
                if forbidden_token in text:
                    issues.append(
                        ValidationIssue(
                            path_name,
                            "route-card-only root README must keep operational discipline in AGENTS.md",
                        )
                    )

    require_tokens(
        repo_root=repo_root,
        path_name=ROOT_ROUTE_CARD_GUARD_DECISION_NAME,
        tokens=ROOT_ROUTE_CARD_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(ROOT_ROUTE_CARD_GUARD_DECISION_NAME, "Root Route-card Guard"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "no active root examples payload",
            "no active root config payload",
            "no active root manifest payload",
            "no active root reports payload",
            "compatibility route",
        ),
        issues=issues,
    )

    return issues


def validate_generated_route_residue_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues = validate_generated_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name="generated/README.md",
        tokens=GENERATED_READER_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="generated/AGENTS.md",
        tokens=GENERATED_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GENERATED_ROUTE_RESIDUE_DECISION_NAME,
        tokens=GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(GENERATED_ROUTE_RESIDUE_DECISION_NAME, "Generated Route Residue Guard"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Generated route residue", "same part root"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("generated/readout JSON", "same part"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


def validate_agent_lane_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=AGENTS_DISTRICT_NAME,
        tokens=AGENTS_DISTRICT_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=SPARK_LANE_AGENTS_NAME,
        tokens=SPARK_LANE_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=SPARK_LANE_SWARM_NAME,
        tokens=SPARK_LANE_SWARM_REQUIRED_TOKENS,
        issues=issues,
    )
    swarm_text = read_text_or_issue(repo_root / SPARK_LANE_SWARM_NAME, issues, root=repo_root)
    if swarm_text and markdown_python_commands(swarm_text):
        issues.append(
            ValidationIssue(
                SPARK_LANE_SWARM_NAME,
                "Spark SWARM context must route executable commands to .agents/spark/AGENTS.md instead of carrying python command lines",
            )
        )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0017-spark-agent-lane-placement.md",
        tokens=SPARK_LANE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="README.md",
        tokens=(AGENTS_DISTRICT_NAME, SPARK_LANE_AGENTS_NAME),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/PROOF_TOPOLOGY.md",
        tokens=(".agents/", ".agents/spark/", "Agent guidance"),
        issues=issues,
    )
    if (repo_root / "Spark").exists():
        issues.append(
            ValidationIssue(
                "Spark/",
                "root-local Spark lane must stay moved to .agents/spark/",
            )
        )
    return issues


def validate_quest_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTS_README_NAME,
        tokens=QUESTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTS_AGENTS_NAME,
        tokens=QUESTS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUEST_LIFECYCLE_NAME,
        tokens=QUEST_LIFECYCLE_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, stale_token in (
        (QUESTS_README_NAME, "It is not `QUESTBOOK.md`"),
        (QUESTS_README_NAME, "Quests are not eval bundles."),
        (QUEST_LIFECYCLE_NAME, "It is not `QUESTBOOK.md`"),
        (QUEST_LIFECYCLE_NAME, "does not create an eval result receipt"),
    ):
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if stale_token in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "quest route surfaces should use positive role routing instead of stale negative scaffold "
                    f"'{stale_token}'",
                )
            )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0004-questbook-topology.md",
        tokens=("QUESTBOOK.md", "generated quest", "lane/state", "eval bundles"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0018-quest-lane-state-source-layout.md",
        tokens=(
            "quests/<lane>/<state>/",
            "generated quest readers",
            "legacy path vocabulary",
            "stale top-level quest source files",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0021-quest-lifecycle-contract.md",
        tokens=QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
        tokens=AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for stale_path in sorted((repo_root / "quests").glob("AOA-EV-Q-*.yaml")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level quest source files must stay moved to quests/<lane>/<state>/",
            )
        )
    for stale_path in sorted((repo_root / "quests").glob("AOE-Q-AGON-*.md")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level Agon quest notes must stay behind mechanics/agon/PROVENANCE.md",
            )
        )
    for markdown_path in sorted((repo_root / "quests").rglob("*.md")):
        relative_parts = markdown_path.relative_to(repo_root).parts
        if relative_parts in {
            ("quests", "README.md"),
            ("quests", "AGENTS.md"),
            ("quests", "LIFECYCLE.md"),
        }:
            continue
        issues.append(
            ValidationIssue(
                relative_location(markdown_path, repo_root),
                "markdown quest notes must not live under active quest lifecycle paths; "
                "route lineage through the owning mechanic PROVENANCE.md",
            )
        )
    return issues


def validate_proof_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    topology_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=PROOF_TOPOLOGY_REQUIRED_TOKENS,
        issues=issues,
    )
    decision_text = require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0005-proof-topology-map.md",
        tokens=PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    roadmap_text = require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=(PROOF_TOPOLOGY_NAME, "Proof Topology Map"),
        issues=issues,
    )
    if topology_text:
        for stale_phrase in PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in topology_text:
                issues.append(
                    ValidationIssue(
                        PROOF_TOPOLOGY_NAME,
                        f"proof topology must describe active mechanics, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    if decision_text:
        for stale_phrase in PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in decision_text:
                issues.append(
                    ValidationIssue(
                        "docs/decisions/0005-proof-topology-map.md",
                        f"proof topology decision must describe the active mechanics atlas, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    if roadmap_text:
        for stale_phrase in ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING:
            if stale_phrase in roadmap_text:
                issues.append(
                    ValidationIssue(
                        "ROADMAP.md",
                        f"roadmap must describe active mechanics direction, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    return issues


def validate_legacy_naming_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=LEGACY_NAMING_REQUIRED_TOKENS,
        issues=issues,
    )
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
    archive_detail_surface_paths: set[str] = set(
        LEGACY_EXTERNAL_ARCHIVE_DETAIL_SURFACE_NAMES
    )
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
    route_management_surface_paths: set[str] = set(
        LEGACY_EXTERNAL_ROUTE_MANAGEMENT_SURFACE_NAMES
    )
    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        for allowed_name in allowed_names:
            route_management_surface_paths.add(f"{district_name}/{allowed_name}")
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
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
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0009-legacy-naming-containment.md",
        tokens=LEGACY_NAMING_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
        tokens=LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
        tokens=LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            "Legacy Naming Single-Bridge Language",
            LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "Legacy Naming Posture Guide",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="README.md",
        tokens=(LEGACY_NAMING_NAME, "accepted-input"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/PROOF_TOPOLOGY.md",
        tokens=(LEGACY_NAMING_NAME, "generated-projection", "provenance-bridge"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="CHANGELOG.md",
        tokens=(
            "Legacy Naming Single-Bridge Language",
            "Legacy Naming Posture Guide",
            "single controlled bridge",
        ),
        issues=issues,
    )
    return issues


def validate_mechanics_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanics_parent_allowlist(repo_root))
    issues.extend(validate_mechanic_parent_direction_surfaces(repo_root))
    issues.extend(validate_mechanic_parts_index_sync_surfaces(repo_root))
    issues.extend(validate_mechanic_index_command_ownership(repo_root))
    issues.extend(validate_mechanic_lower_parts_index_operating_cards(repo_root))
    issues.extend(validate_mechanic_legacy_single_bridge_surfaces(repo_root))
    issues.extend(validate_mechanic_part_readme_contract_surfaces(repo_root))
    issues.extend(validate_mechanic_part_validation_command_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_entry_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_bridge_posture_surfaces(repo_root))
    issues.extend(validate_mechanic_root_district_recon_surfaces(repo_root))
    issues.extend(validate_root_authored_surface_classification(repo_root))
    issues.extend(validate_active_mechanic_route_residue_surfaces(repo_root))
    issues.extend(validate_mechanic_payload_route_residue_surfaces(repo_root))
    for path_name in FORBIDDEN_ACTIVE_MECHANICS_PATHS:
        if (repo_root / path_name).exists():
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy mechanics path must not exist as an active route",
                )
            )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=MECHANICS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=MECHANICS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PART_LOCAL_TEST_PLACEMENT_DECISION_NAME,
        tokens=PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(PART_LOCAL_TEST_PLACEMENT_DECISION_NAME, "Part-local Test Placement"),
            issues=issues,
        )
    for path_name in MECHANIC_PART_CONTRACT_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PART_CONTRACT_REQUIRED_TOKENS,
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_README_CONTRACT_DECISION_NAME,
        tokens=MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_README_CONTRACT_DECISION_NAME,
            "Mechanic Part README Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
            "Mechanic Provenance Entry Contract",
        ),
        issues=issues,
    )
    for path_name in MECHANIC_LEGACY_RAW_README_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS,
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_MECHANIC_README_NAME,
        tokens=PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_MECHANIC_AGENTS_NAME,
        tokens=PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_MECHANIC_PARTS_NAME,
        tokens=PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    issues.extend(validate_proof_object_parts_route_surface(repo_root))
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME,
        tokens=PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME,
        tokens=PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_MECHANIC_PROVENANCE_NAME,
        tokens=PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0010-proof-object-mechanic-package.md",
        tokens=PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_CONTRACT_PART_DECISION_NAME,
        tokens=PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME,
        tokens=PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME,
        tokens=PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME,
            "Proof-object Part Owner-split Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_README_NAME,
        tokens=PROOF_LOOP_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_AGENTS_NAME,
        tokens=PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_PARTS_NAME,
        tokens=PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_PARTS_README_NAME,
        tokens=PROOF_LOOP_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME,
        tokens=PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME,
        tokens=PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME,
            "Proof Loop Route-Smoke Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_PROVENANCE_NAME,
        tokens=PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_LEGACY_INDEX_NAME,
        tokens=PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME,
        tokens=PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_LEGACY_RAW_README_NAME,
        tokens=PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0019-proof-loop-mechanic-package.md",
        tokens=PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    issues.extend(validate_proof_loop_smoke_report_surfaces(repo_root))
    issues.extend(validate_proof_loop_local_report_surfaces(repo_root))
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_MECHANIC_README_NAME,
        tokens=COMPARISON_SPINE_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_MECHANIC_AGENTS_NAME,
        tokens=COMPARISON_SPINE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_MECHANIC_PARTS_NAME,
        tokens=COMPARISON_SPINE_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_PARTS_README_NAME,
        tokens=COMPARISON_SPINE_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_OVERVIEW_PART_README_NAME,
        tokens=COMPARISON_SPINE_OVERVIEW_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME,
        tokens=COMPARISON_SPINE_FIXED_BASELINE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME,
        tokens=COMPARISON_SPINE_PEER_COMPARE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME,
        tokens=COMPARISON_SPINE_LONGITUDINAL_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME,
            "Comparison Spine Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0011-comparison-spine-mechanic-package.md",
        tokens=COMPARISON_SPINE_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_REPORT_PARTS_DECISION_NAME,
        tokens=COMPARISON_SPINE_REPORT_PARTS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_FIXTURE_PARTS_DECISION_NAME,
        tokens=COMPARISON_SPINE_FIXTURE_PARTS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_PROVENANCE_NAME,
        tokens=COMPARISON_SPINE_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=COMPARISON_SPINE_LEGACY_INDEX_NAME,
        tokens=COMPARISON_SPINE_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_MECHANIC_README_NAME,
        tokens=PROOF_INFRA_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_MECHANIC_AGENTS_NAME,
        tokens=PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_MECHANIC_PARTS_NAME,
        tokens=PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_FIXTURE_FAMILIES_README_NAME,
        tokens=PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS,
        issues=issues,
    )
    fixture_families_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME,
        tokens=PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_REPORTABLE_CONTRACTS_README_NAME,
        tokens=PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS,
        issues=issues,
    )
    reportable_contracts_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME,
        tokens=PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, text in (
        (PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_NAME, fixture_families_agents_text),
        (PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_NAME, reportable_contracts_agents_text),
    ):
        if not text:
            continue
        for stale_phrase in PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "proof-infra part AGENTS cards should use operating cards and owner route tables instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_PROVENANCE_NAME,
        tokens=PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_LEGACY_INDEX_NAME,
        tokens=PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0012-proof-infra-mechanic-package.md",
        tokens=PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_FIXTURE_FAMILIES_DECISION_NAME,
        tokens=PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_NAME,
        tokens=PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_MECHANIC_README_NAME,
        tokens=PUBLICATION_RECEIPTS_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_MECHANIC_AGENTS_NAME,
        tokens=PUBLICATION_RECEIPTS_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME,
        tokens=PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME,
        tokens=PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME,
        tokens=PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME,
        tokens=PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME,
        tokens=PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME,
            "Publication Receipts Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME,
        tokens=PUBLICATION_RECEIPTS_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME,
        tokens=PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME,
        tokens=PUBLICATION_RECEIPTS_LEGACY_RAW_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0013-publication-receipts-mechanic-package.md",
        tokens=PUBLICATION_RECEIPTS_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_MECHANIC_README_NAME,
        tokens=RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
        tokens=RELEASE_SUPPORT_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_MECHANIC_PARTS_NAME,
        tokens=RELEASE_SUPPORT_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_MECHANIC_PARTS_README_NAME,
        tokens=RELEASE_SUPPORT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
        tokens=RELEASE_SUPPORT_READINESS_AUDIT_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
        tokens=RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
        tokens=RELEASE_SUPPORT_PR_HANDOFF_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME,
            "Release Support Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME,
        tokens=RELEASE_SUPPORT_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_LEGACY_INDEX_NAME,
        tokens=RELEASE_SUPPORT_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME,
        tokens=RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_LEGACY_RAW_README_NAME,
        tokens=RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0014-release-support-mechanic-package.md",
        tokens=RELEASE_SUPPORT_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_MECHANIC_README_NAME,
        tokens=TITAN_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_MECHANIC_AGENTS_NAME,
        tokens=TITAN_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_MECHANIC_DIRECTION_NAME,
        tokens=TITAN_MECHANIC_DIRECTION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0015-titan-mechanic-package.md",
        tokens=TITAN_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
        tokens=TITAN_INCARNATION_CANARIES_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
        tokens=TITAN_SUMMON_DISCIPLINE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME,
        tokens=TITAN_SEED_BOUNDARY_SEEDS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_SEED_BOUNDARY_SEEDS_README_NAME,
        tokens=TITAN_SEED_BOUNDARY_SEEDS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_PARTS_INDEX_README_NAME,
        tokens=TITAN_PARTS_INDEX_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_SEED_BOUNDARY_PART_README_NAME,
        tokens=TITAN_SEED_BOUNDARY_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name in TITAN_SEED_BOUNDARY_ROUTE_SURFACE_NAMES:
        route_text = read_text_or_issue(
            repo_root / path_name,
            issues,
            root=repo_root,
        )
        for stale_phrase in TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES:
            if route_text and stale_phrase in route_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "Titan seed-boundary route surfaces must route pressure through owner maps instead of stale negative claim-limit phrasing",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
        tokens=TITAN_SEED_BOUNDARY_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
            "Titan Seed-boundary Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AGON_MECHANIC_README_NAME,
        tokens=AGON_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AGON_MECHANIC_AGENTS_NAME,
        tokens=AGON_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0016-agon-mechanic-package.md",
        tokens=AGON_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in AGON_PART_README_CONTRACTS:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
            issues=issues,
        )
        readme_text = read_text_or_issue(
            repo_root / path_name,
            issues,
            root=repo_root,
        )
        for stale_phrase in AGON_PART_README_STALE_STOP_LINE_PHRASES:
            if readme_text and stale_phrase in readme_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "Agon part README Stop-Lines must route pressure through owner tables instead of stale imperative stop-line phrasing",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=AGON_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=AGON_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(AGON_PART_CONTRACT_GUARD_DECISION_NAME, "Agon Part Contract Guard"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MECHANIC_README_NAME,
        tokens=RECURRENCE_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MECHANIC_AGENTS_NAME,
        tokens=RECURRENCE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MECHANIC_PARTS_NAME,
        tokens=RECURRENCE_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_CONTROL_PLANE_PART_README_NAME,
        tokens=RECURRENCE_CONTROL_PLANE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_ANCHOR_RETURN_PART_README_NAME,
        tokens=RECURRENCE_ANCHOR_RETURN_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MEMORY_RECALL_PART_README_NAME,
        tokens=RECURRENCE_MEMORY_RECALL_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_RECURSOR_BOUNDARY_PART_README_NAME,
        tokens=RECURRENCE_RECURSOR_BOUNDARY_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_STATS_REGROUNDING_PART_README_NAME,
        tokens=RECURRENCE_STATS_REGROUNDING_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_PORTABLE_PROOF_BEACONS_PART_README_NAME,
        tokens=RECURRENCE_PORTABLE_PROOF_BEACONS_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    portable_proof_beacons_agents_text = require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME,
        tokens=RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_REQUIRED_TOKENS,
        issues=issues,
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
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MECHANIC_PROVENANCE_NAME,
        tokens=RECURRENCE_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_MECHANIC_DECISION_NAME,
        tokens=RECURRENCE_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_SUPPORT_PARTS_DECISION_NAME,
        tokens=RECURRENCE_SUPPORT_PARTS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_NAME,
        tokens=RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME,
        tokens=RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME,
            "Recurrence Control-plane Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_MECHANIC_README_NAME,
        tokens=CHECKPOINT_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_MECHANIC_AGENTS_NAME,
        tokens=CHECKPOINT_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_MECHANIC_PARTS_NAME,
        tokens=CHECKPOINT_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_A2A_PART_README_NAME,
        tokens=CHECKPOINT_A2A_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME,
        tokens=CHECKPOINT_RESTARTABLE_INQUIRY_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_SELF_AGENT_PART_README_NAME,
        tokens=CHECKPOINT_SELF_AGENT_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_SELF_AGENT_POSTURE_DOC_NAME,
        tokens=CHECKPOINT_SELF_AGENT_POSTURE_DOC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_MECHANIC_PROVENANCE_NAME,
        tokens=CHECKPOINT_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_MECHANIC_DECISION_NAME,
        tokens=CHECKPOINT_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=CHECKPOINT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
            "Checkpoint Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_MECHANIC_README_NAME,
        tokens=EXPERIENCE_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_MECHANIC_AGENTS_NAME,
        tokens=EXPERIENCE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_MECHANIC_PARTS_NAME,
        tokens=EXPERIENCE_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_PROTOCOL_PART_README_NAME,
        tokens=EXPERIENCE_PROTOCOL_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_CERTIFICATION_PART_README_NAME,
        tokens=EXPERIENCE_CERTIFICATION_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_ADOPTION_PART_README_NAME,
        tokens=EXPERIENCE_ADOPTION_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_GOVERNANCE_PART_README_NAME,
        tokens=EXPERIENCE_GOVERNANCE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_OFFICE_PART_README_NAME,
        tokens=EXPERIENCE_OFFICE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_MECHANIC_PROVENANCE_NAME,
        tokens=EXPERIENCE_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_MECHANIC_DECISION_NAME,
        tokens=EXPERIENCE_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME,
        tokens=EXPERIENCE_VERDICT_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=EXPERIENCE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
            "Experience Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_MECHANIC_README_NAME,
        tokens=ANTIFRAGILITY_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_MECHANIC_AGENTS_NAME,
        tokens=ANTIFRAGILITY_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_MECHANIC_PARTS_NAME,
        tokens=ANTIFRAGILITY_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_PARTS_README_NAME,
        tokens=ANTIFRAGILITY_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    antifragility_parts_readme = read_text_or_issue(
        repo_root / ANTIFRAGILITY_PARTS_README_NAME,
        issues,
        root=repo_root,
    )
    for forbidden_token in ANTIFRAGILITY_PARTS_README_FORBIDDEN_TOKENS:
        if antifragility_parts_readme and forbidden_token in antifragility_parts_readme:
            issues.append(
                ValidationIssue(
                    ANTIFRAGILITY_PARTS_README_NAME,
                    "Antifragility parts lower index should use an operating card and owner pressure routes instead of stale negative boundary scaffold "
                    f"'{forbidden_token}'",
                )
            )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_POSTURE_PART_README_NAME,
        tokens=ANTIFRAGILITY_POSTURE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME,
        tokens=ANTIFRAGILITY_STRESS_WINDOW_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_STRESS_WINDOW_DOC_NAME,
        tokens=ANTIFRAGILITY_STRESS_WINDOW_DOC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME,
        tokens=ANTIFRAGILITY_REPAIR_PROOF_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_MECHANIC_PROVENANCE_NAME,
        tokens=ANTIFRAGILITY_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_MECHANIC_DECISION_NAME,
        tokens=ANTIFRAGILITY_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME,
            "Antifragility Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_MECHANIC_README_NAME,
        tokens=METHOD_GROWTH_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_MECHANIC_AGENTS_NAME,
        tokens=METHOD_GROWTH_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_MECHANIC_PARTS_NAME,
        tokens=METHOD_GROWTH_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME,
        tokens=METHOD_GROWTH_CANDIDATE_LINEAGE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_OWNER_LANDING_PART_README_NAME,
        tokens=METHOD_GROWTH_OWNER_LANDING_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_MECHANIC_PROVENANCE_NAME,
        tokens=METHOD_GROWTH_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_MECHANIC_DECISION_NAME,
        tokens=METHOD_GROWTH_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME,
        tokens=METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME,
            "Method-growth Part Owner-split Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_MECHANIC_README_NAME,
        tokens=RPG_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_MECHANIC_AGENTS_NAME,
        tokens=RPG_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_MECHANIC_PARTS_NAME,
        tokens=RPG_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_PROGRESS_UNLOCKS_PART_README_NAME,
        tokens=RPG_PROGRESS_UNLOCKS_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_MECHANIC_PROVENANCE_NAME,
        tokens=RPG_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_MECHANIC_DECISION_NAME,
        tokens=RPG_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
        tokens=RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
            "RPG Progression-unlocks Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_MECHANIC_README_NAME,
        tokens=GROWTH_CYCLE_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_MECHANIC_AGENTS_NAME,
        tokens=GROWTH_CYCLE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_MECHANIC_PARTS_NAME,
        tokens=GROWTH_CYCLE_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_PARTS_README_NAME,
        tokens=GROWTH_CYCLE_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME,
        tokens=GROWTH_CYCLE_DIAGNOSIS_GATE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_MECHANIC_PROVENANCE_NAME,
        tokens=GROWTH_CYCLE_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_MECHANIC_DECISION_NAME,
        tokens=GROWTH_CYCLE_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME,
        tokens=GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME,
            "Growth-cycle Diagnosis-gate Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
        tokens=REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
            "Repair Diagnosis Route Boundary",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_MECHANIC_README_NAME,
        tokens=DISTILLATION_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_MECHANIC_AGENTS_NAME,
        tokens=DISTILLATION_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_MECHANIC_PARTS_NAME,
        tokens=DISTILLATION_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME,
        tokens=DISTILLATION_COMPOST_PROVENANCE_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME,
        tokens=DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_MECHANIC_PROVENANCE_NAME,
        tokens=DISTILLATION_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_MECHANIC_DECISION_NAME,
        tokens=DISTILLATION_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=DISTILLATION_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
            "Distillation Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_MECHANIC_README_NAME,
        tokens=QUESTBOOK_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_MECHANIC_AGENTS_NAME,
        tokens=QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_MECHANIC_PARTS_NAME,
        tokens=QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_SOURCE_RECORD_PART_README_NAME,
        tokens=QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_DISPATCH_READER_PART_README_NAME,
        tokens=QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_MECHANIC_PROVENANCE_NAME,
        tokens=QUESTBOOK_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0006-questbook-mechanic-package.md",
        tokens=QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0021-quest-lifecycle-contract.md",
        tokens=QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
        tokens=QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
            "Questbook Part Owner-split Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_MECHANIC_README_NAME,
        tokens=AUDIT_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_MECHANIC_AGENTS_NAME,
        tokens=AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_MECHANIC_PROVENANCE_NAME,
        tokens=AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    audit_parts_text = require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_PARTS_README_NAME,
        tokens=AUDIT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if audit_parts_text:
        for forbidden_token in AUDIT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in audit_parts_text:
                issues.append(
                    ValidationIssue(
                        AUDIT_PARTS_README_NAME,
                        "audit parts index should expose a positive part-admission route",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_LEGACY_INDEX_NAME,
        tokens=AUDIT_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_LEGACY_DISTILLATION_LOG_NAME,
        tokens=AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_LEGACY_RAW_README_NAME,
        tokens=AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_SELECTED_EVIDENCE_PART_README_NAME,
        tokens=AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
        tokens=AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_CANDIDATE_READERS_PART_README_NAME,
        tokens=AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_INTEGRITY_REVIEW_PART_README_NAME,
        tokens=AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=AUDIT_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(AUDIT_PART_CONTRACT_GUARD_DECISION_NAME, "Audit Part Contract Guard"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0007-audit-mechanic-package.md",
        tokens=AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_NAME,
        tokens=BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_MECHANIC_README_NAME,
        tokens=BOUNDARY_BRIDGE_MECHANIC_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_MECHANIC_AGENTS_NAME,
        tokens=BOUNDARY_BRIDGE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_MECHANIC_PARTS_NAME,
        tokens=BOUNDARY_BRIDGE_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_NAME,
        tokens=BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_LEGACY_INDEX_NAME,
        tokens=BOUNDARY_BRIDGE_LEGACY_INDEX_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_LEGACY_DISTILLATION_LOG_NAME,
        tokens=BOUNDARY_BRIDGE_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_LEGACY_RAW_README_NAME,
        tokens=BOUNDARY_BRIDGE_LEGACY_RAW_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_PARTS_README_NAME,
        tokens=BOUNDARY_BRIDGE_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME,
        tokens=BOUNDARY_BRIDGE_COMPATIBILITY_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_README_NAME,
        tokens=BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_ORCHESTRATOR_PROOF_ANCHORS_PART_README_NAME,
        tokens=BOUNDARY_BRIDGE_ORCHESTRATOR_PART_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME,
        tokens=BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME,
            "Boundary Bridge Part Contract Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/0008-boundary-bridge-mechanic-package.md",
        tokens=BOUNDARY_BRIDGE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=REPO_VALIDATION_AOA_MEMO_PIN_DECISION_NAME,
        tokens=REPO_VALIDATION_AOA_MEMO_PIN_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    issues.extend(validate_repo_validation_workflow_surface(repo_root))
    matrix_path = repo_root / SIBLING_CANARY_MATRIX_NAME
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(SIBLING_CANARY_MATRIX_NAME, "file is missing"))
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                SIBLING_CANARY_MATRIX_NAME,
                f"invalid JSON: {exc}",
            )
        )
    else:
        entries = matrix.get("entries") if isinstance(matrix, dict) else None
        if not isinstance(entries, list):
            issues.append(
                ValidationIssue(
                    SIBLING_CANARY_MATRIX_NAME,
                    "entries must be a list",
                )
            )
        else:
            repos = {
                entry.get("repo")
                for entry in entries
                if isinstance(entry, dict) and isinstance(entry.get("repo"), str)
            }
            for repo_name in SIBLING_CANARY_EXPECTED_REPOS:
                if repo_name not in repos:
                    issues.append(
                        ValidationIssue(
                            SIBLING_CANARY_MATRIX_NAME,
                            f"missing sibling canary entry for {repo_name}",
                        )
                    )
            for entry in entries:
                if (
                    isinstance(entry, dict)
                    and entry.get("repo") == "abyss-stack"
                    and entry.get("resolver") != "abyss-stack-source"
                ):
                    issues.append(
                        ValidationIssue(
                            SIBLING_CANARY_MATRIX_NAME,
                            "abyss-stack sibling canary entry must use resolver 'abyss-stack-source'",
                        )
                    )
    return issues


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
        commands = markdown_python_commands(text)
        if commands:
            issues.append(
                ValidationIssue(
                    relative_name,
                    "mechanic index surfaces must route executable validation commands to the nearest AGENTS.md instead of carrying python command blocks",
                )
            )

    return issues


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


def validate_mechanic_lower_parts_index_operating_cards(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_paths = sorted((repo_root / "mechanics").glob("*/parts/README.md"))

    for path in index_paths:
        relative_name = path.relative_to(repo_root).as_posix()
        require_tokens(
            repo_root=repo_root,
            path_name=relative_name,
            tokens=MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS,
            issues=issues,
        )

    return issues


def validate_mechanic_index_surface_roles(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        validate_mechanic_part_role_heading(
            path_name=parts_index_name,
            text=parts_index_text,
            parent_name=parent_name,
            part_name="part",
            role_name="Index",
            issues=issues,
        )

        parts_route_name = f"mechanics/{parent_name}/parts/README.md"
        parts_route_path = repo_root / parts_route_name
        if parts_route_path.is_file():
            parts_route_text = read_text_or_issue(
                parts_route_path,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=parts_route_name,
                text=parts_route_text,
                parent_name=parent_name,
                part_name="parts",
                role_name="Route",
                issues=issues,
            )

    return issues


def validate_repo_validation_workflow_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    workflow_path = repo_root / REPO_VALIDATION_WORKFLOW_NAME
    try:
        workflow_text = workflow_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(REPO_VALIDATION_WORKFLOW_NAME, "file is missing"))
        return issues

    memo_checkout = re.search(
        r"(?ms)^\s+- name: Checkout aoa-memo\b(?P<block>.*?)(?=^\s+- name: |\Z)",
        workflow_text,
    )
    if memo_checkout is None:
        issues.append(
            ValidationIssue(
                REPO_VALIDATION_WORKFLOW_NAME,
                "missing Checkout aoa-memo step",
            )
        )
        return issues

    memo_block = memo_checkout.group("block")
    if "repository: 8Dionysus/aoa-memo" not in memo_block:
        issues.append(
            ValidationIssue(
                REPO_VALIDATION_WORKFLOW_NAME,
                "Checkout aoa-memo step must use repository 8Dionysus/aoa-memo",
            )
        )
    if f"ref: {REPO_VALIDATION_AOA_MEMO_REF}" not in memo_block:
        issues.append(
            ValidationIssue(
                REPO_VALIDATION_WORKFLOW_NAME,
                f"aoa-memo checkout ref must be {REPO_VALIDATION_AOA_MEMO_REF}",
            )
        )
    return issues


def validate_proof_loop_smoke_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_SMOKE_REPORT_NAME,
        tokens=PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_SMOKE_DECISION_NAME,
        tokens=PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME,
        tokens=PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_README_NAME,
        tokens=(PROOF_LOOP_SMOKE_REPORT_NAME, "bounded route-smoke", "no eval result receipt"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="reports/README.md",
        tokens=(PROOF_LOOP_SMOKE_REPORT_NAME, "route-smoke report"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            PROOF_LOOP_SMOKE_DECISION_NAME,
            PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME,
            "Further proof-loop examples",
        ),
        issues=issues,
    )
    return issues


def validate_proof_loop_local_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_LOCAL_REPORT_NAME,
        tokens=PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_LOCAL_REPORT_DECISION_NAME,
        tokens=PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_MECHANIC_README_NAME,
        tokens=(PROOF_LOOP_LOCAL_REPORT_NAME, "First Bundle-Local Report", "no eval result receipt"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_INFRA_MECHANIC_README_NAME,
        tokens=("`*.report.json`", "`evals/<family>/<eval>/reports/summary.schema.json`"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/README.md",
        tokens=("Mechanic And Evidence Anchors",),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/README.md",
        tokens=(PROOF_LOOP_LOCAL_REPORT_NAME, "First Proof Loop Bundle-Local Report"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=("Proof loop route", "mechanics/proof-loop/README.md"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="CHANGELOG.md",
        tokens=(PROOF_LOOP_LOCAL_REPORT_NAME, "bundle-local report validation"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(PROOF_LOOP_LOCAL_REPORT_DECISION_NAME, "Further proof-loop examples"),
        issues=issues,
    )
    return issues


def validate_receipt_intake_dry_review_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    review_path = repo_root / RECEIPT_INTAKE_DRY_REVIEW_NAME
    location = RECEIPT_INTAKE_DRY_REVIEW_NAME

    require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_NAME,
        tokens=RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME,
        tokens=RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "Receipt Intake Dry Review",
                "`receipt_status` stays `not_published`",
            ),
        ),
        (
            PUBLICATION_RECEIPTS_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "dry review",
                "`receipt_status` as `not_published`",
            ),
        ),
        (
            "reports/README.md",
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "receipt-intake",
                "`not_published`",
            ),
        ),
        (
            "docs/README.md",
            ("Mechanic And Evidence Anchors",),
        ),
        ("docs/README.md", (RECEIPT_INTAKE_DRY_REVIEW_NAME, "Receipt Intake Dry Review")),
        (
            "ROADMAP.md",
            ("Publication receipt posture", "mechanics/publication-receipts/README.md"),
        ),
        ("CHANGELOG.md", (RECEIPT_INTAKE_DRY_REVIEW_NAME, "validator coverage")),
        (
            "docs/decisions/README.md",
            (RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME, "real eval-result receipt publication"),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    payload = load_json_payload(review_path, issues)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "receipt intake dry review must be a JSON object"))
        return issues

    for field in (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    ):
        if field in payload:
            issues.append(
                ValidationIssue(
                    location,
                    f"receipt intake dry review must not contain publishable receipt field {field!r}",
                )
            )

    expected_refs = {
        "source_report_ref": f"repo:aoa-evals/{PROOF_LOOP_LOCAL_REPORT_NAME}",
        "source_bundle_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/EVAL.md",
        "source_manifest_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/eval.yaml",
        "report_index_ref": "repo:aoa-evals/generated/eval_report_index.min.json",
        "receipt_payload_schema_ref": f"repo:aoa-evals/{EVAL_RESULT_RECEIPT_SCHEMA_PATH}",
        "event_envelope_schema_ref": f"repo:aoa-evals/{STATS_EVENT_ENVELOPE_SCHEMA_PATH}",
        "publisher_ref": f"repo:aoa-evals/{EVAL_RESULT_RECEIPT_PUBLISHER_NAME}",
        "owner_local_log_ref": f"repo:aoa-evals/{LIVE_EVAL_RECEIPT_LOG_NAME}",
    }
    for key, expected in expected_refs.items():
        value = payload.get(key)
        if value != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))
            continue
        local_path = repo_root / expected.removeprefix("repo:aoa-evals/")
        if not local_path.exists():
            issues.append(ValidationIssue(location, f"{key} target is missing: {expected}"))

    expected_top_level = {
        "artifact_kind": "receipt_intake_dry_review",
        "schema_version": 1,
        "review_id": "eval-result-receipt-intake-dry-review-v1",
        "reviewed_at": "2026-05-19",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    source_report_path = repo_root / PROOF_LOOP_LOCAL_REPORT_NAME
    source_report = load_json_payload(source_report_path, issues)
    manifest = load_yaml_file(source_eval_dir(repo_root, "aoa-verification-honesty") / "eval.yaml", issues)
    report_index = load_json_payload(repo_root / EVAL_REPORT_INDEX_NAME, issues)
    preview = payload.get("candidate_payload_preview")

    payload_schema = load_json_payload(
        repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH,
        issues,
    )
    payload_validator: Draft202012Validator | None = None
    if isinstance(payload_schema, dict):
        try:
            Draft202012Validator.check_schema(payload_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    EVAL_RESULT_RECEIPT_SCHEMA_PATH,
                    f"invalid JSON schema: {exc.message}",
                )
            )
        else:
            payload_validator = get_schema_validator_with_format(payload_schema)

    if isinstance(preview, dict):
        if payload_validator is not None:
            validate_against_schema(
                preview,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{location}.candidate_payload_preview",
                issues,
                validator=payload_validator,
            )

        if isinstance(source_report, dict):
            expected_report_values = {
                "eval_name": source_report.get("eval_name"),
                "bundle_status": source_report.get("bundle_status"),
                "verdict": source_report.get("verdict"),
            }
            for key, expected in expected_report_values.items():
                if preview.get(key) != expected:
                    issues.append(
                        ValidationIssue(
                            f"{location}.candidate_payload_preview",
                            f"{key} must match source report value {expected!r}",
                        )
                    )
            case_count = len(source_report.get("per_case_breakdown", []))
            if preview.get("case_count") != case_count:
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "case_count must match source report per_case_breakdown length",
                    )
                )

        if isinstance(manifest, dict):
            if preview.get("report_format") != manifest.get("report_format"):
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "report_format must match source manifest report_format",
                    )
                )
            if preview.get("bundle_status") != manifest.get("status"):
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "bundle_status must match source manifest status",
                    )
                )
            if manifest.get("baseline_mode") == "none" and preview.get("comparison_mode") != "none":
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "comparison_mode must stay 'none' when the source manifest baseline_mode is 'none'",
                    )
                )

        if preview.get("claim_scope") != "bundle_scoped":
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "claim_scope must stay 'bundle_scoped' for this dry review",
                )
            )
        if preview.get("bundle_ref") != expected_refs["source_bundle_ref"]:
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "bundle_ref must match the dry review source_bundle_ref",
                )
            )
        if preview.get("report_ref") != expected_refs["source_report_ref"]:
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "report_ref must match the dry review source_report_ref",
                )
            )
        interpretation_bound = preview.get("interpretation_bound")
        if not isinstance(interpretation_bound, str):
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "interpretation_bound must be a string",
                )
            )
        else:
            for token in (
                "Dry review only.",
                "publication pressure routes to a receipt envelope",
                ".aoa/live_receipts/",
                "verdict meaning stays with bundle-local review",
            ):
                if token not in interpretation_bound:
                    issues.append(
                        ValidationIssue(
                            f"{location}.candidate_payload_preview.interpretation_bound",
                            f"interpretation_bound must mention '{token}'",
                        )
                    )
    else:
        issues.append(
            ValidationIssue(location, "candidate_payload_preview must be a JSON object")
        )

    if isinstance(report_index, dict):
        reports = report_index.get("reports")
        indexed_paths = {
            entry.get("source_report_path")
            for entry in reports
            if isinstance(entry, dict)
        } if isinstance(reports, list) else set()
        if PROOF_LOOP_LOCAL_REPORT_NAME not in indexed_paths:
            issues.append(
                ValidationIssue(
                    location,
                    f"report_index_ref must index {PROOF_LOOP_LOCAL_REPORT_NAME}",
                )
            )

    source_alignment = payload.get("source_alignment")
    if isinstance(source_alignment, dict):
        for key in (
            "eval_name_matches_report",
            "bundle_status_matches_manifest",
            "report_format_matches_manifest",
            "verdict_matches_report",
        ):
            if source_alignment.get(key) is not True:
                issues.append(ValidationIssue(f"{location}.source_alignment", f"{key} must be true"))
        if source_alignment.get("case_count_source") != "per_case_breakdown length":
            issues.append(
                ValidationIssue(
                    f"{location}.source_alignment",
                    "case_count_source must stay 'per_case_breakdown length'",
                )
            )
    else:
        issues.append(ValidationIssue(location, "source_alignment must be a JSON object"))

    checks = payload.get("intake_checks")
    if isinstance(checks, list):
        by_id = {entry.get("check_id"): entry for entry in checks if isinstance(entry, dict)}
        expected_check_results = {
            "source_report_exists": "pass",
            "source_report_is_indexed": "pass",
            "candidate_payload_preview_validates_against_payload_schema": "pass",
            "stats_event_envelope_created": "not_attempted",
            "receipt_publisher_run": "not_attempted",
            "owner_local_live_log_append": "not_attempted",
        }
        for check_id, expected_result in expected_check_results.items():
            entry = by_id.get(check_id)
            if not isinstance(entry, dict):
                issues.append(ValidationIssue(f"{location}.intake_checks", f"missing check_id {check_id!r}"))
                continue
            if entry.get("result") != expected_result:
                issues.append(
                    ValidationIssue(
                        f"{location}.intake_checks.{check_id}",
                        f"result must be {expected_result!r}",
                    )
                )
            evidence_ref = entry.get("evidence_ref")
            if not isinstance(evidence_ref, str) or not evidence_ref.startswith("repo:aoa-evals/"):
                issues.append(
                    ValidationIssue(
                        f"{location}.intake_checks.{check_id}",
                        "evidence_ref must point at a repo:aoa-evals/ surface",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "intake_checks must be a list"))

    publication_boundary = payload.get("publication_boundary")
    if isinstance(publication_boundary, dict):
        expected_boundary_values = {
            "publication_status": "dry_review_only",
            "receipt_status": "not_published",
            "event_envelope_status": "not_created",
            "live_log_append_status": "not_attempted",
            "publisher_execution_status": "not_attempted",
        }
        for key, expected in expected_boundary_values.items():
            if publication_boundary.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{location}.publication_boundary",
                        f"{key} must be {expected!r}",
                    )
                )
        boundary = publication_boundary.get("boundary")
        if not isinstance(boundary, str):
            issues.append(
                ValidationIssue(
                    f"{location}.publication_boundary",
                    "boundary must be a string",
                )
            )
        else:
            for token in (
                "receipt envelope pressure",
                "stats sidecar pressure",
                "live log pressure",
                "proof or bundle promotion pressure",
                "runtime acceptance pressure",
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

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
    else:
        for token in (
            "Publication pressure routes",
            "live receipt memory append routes",
            "runtime evidence acceptance routes",
            "bundle promotion routes",
            "strategic closeout stays with the goal owner",
        ):
            if token not in claim_limit:
                issues.append(
                    ValidationIssue(location, f"claim_limit must mention '{token}'")
                )

    return issues


def validate_release_support_readiness_audit_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    audit_path = repo_root / RELEASE_SUPPORT_READINESS_AUDIT_NAME
    location = RELEASE_SUPPORT_READINESS_AUDIT_NAME

    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_READINESS_AUDIT_NAME,
        tokens=RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME,
        tokens=RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
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
            (
                RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                "readiness audits",
                "GitHub `Repo Validation`",
            ),
        ),
        (
            "docs/RELEASING.md",
            (
                RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                "local release-prep reviewability evidence",
                "current git, GitHub, tag, release, PR, and objective evidence",
            ),
        ),
        (
            "mechanics/release-support/parts/readiness-audit/README.md",
            (
                RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                "GitHub PR approval and Repo Validation",
                "current goal review",
            ),
        ),
        (
            "docs/README.md",
            ("Mechanic And Evidence Anchors",),
        ),
        (
            "docs/README.md",
            (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "Release Support Readiness Audit"),
        ),
        (
            "ROADMAP.md",
            ("Release-support posture", "mechanics/release-support/README.md"),
        ),
        ("CHANGELOG.md", (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "goal completion")),
        (
            "docs/decisions/README.md",
            (RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME, "release-prep PR handoff"),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    payload = load_json_payload(audit_path, issues)
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

    required_requirement_ids = {
        "root_design_spine",
        "decision_memory",
        "roadmap_quest_and_lifecycle_route",
        "proof_topology_legacy_and_mechanics",
        "proof_loop_materialization",
        "generated_reader_freshness",
        "local_release_gate_coverage",
        "sibling_boundary_and_canary",
    }
    requirements = payload.get("requirements_review")
    if isinstance(requirements, list):
        seen_requirement_ids: set[str] = set()
        for index, requirement in enumerate(requirements):
            req_location = f"{location}.requirements_review[{index}]"
            if not isinstance(requirement, dict):
                issues.append(ValidationIssue(req_location, "requirement entry must be an object"))
                continue
            requirement_id = requirement.get("requirement_id")
            if isinstance(requirement_id, str):
                seen_requirement_ids.add(requirement_id)
            else:
                issues.append(ValidationIssue(req_location, "requirement_id must be a string"))
            if requirement.get("status") != "ready_for_release_prep_review":
                issues.append(
                    ValidationIssue(
                        req_location,
                        "status must stay 'ready_for_release_prep_review'",
                    )
                )
            evidence_refs = requirement.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                issues.append(ValidationIssue(req_location, "evidence_refs must be a non-empty list"))
            else:
                for ref_index, evidence_ref in enumerate(evidence_refs):
                    parse_repo_ref(
                        evidence_ref,
                        location=f"{req_location}.evidence_refs[{ref_index}]",
                        issues=issues,
                    )
            claim_limit = requirement.get("claim_limit")
            if not isinstance(claim_limit, str) or len(claim_limit) < 20:
                issues.append(ValidationIssue(req_location, "claim_limit must be a meaningful string"))
        missing_requirement_ids = required_requirement_ids - seen_requirement_ids
        for requirement_id in sorted(missing_requirement_ids):
            issues.append(
                ValidationIssue(
                    f"{location}.requirements_review",
                    f"missing requirement_id {requirement_id!r}",
                )
            )
    else:
        issues.append(ValidationIssue(location, "requirements_review must be a list"))

    required_commands = {
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract",
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
    }
    verification_snapshot = payload.get("verification_snapshot")
    if isinstance(verification_snapshot, list):
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
    else:
        issues.append(ValidationIssue(location, "verification_snapshot must be a list"))

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
                issues.append(
                    ValidationIssue(
                        f"{location}.publication_boundary",
                        f"{key} must be {expected!r}",
                    )
                )
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

    open_requirements = payload.get("open_requirements_before_publication")
    if isinstance(open_requirements, list):
        joined_open_requirements = "\n".join(
            item for item in open_requirements if isinstance(item, str)
        )
        for token in (
            "review the accumulated diff",
            "open a PR",
            "observe GitHub Repo Validation",
            "merge only after required checks are green",
            "create any tag or GitHub Release only after",
            "goal completion audit",
        ):
            if token not in joined_open_requirements:
                issues.append(
                    ValidationIssue(
                        f"{location}.open_requirements_before_publication",
                        f"open requirements must mention '{token}'",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "open_requirements_before_publication must be a list"))

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
    else:
        for token in (
            "does not publish a release",
            "create a tag",
            "open or approve a PR",
            "observe GitHub Repo Validation",
            "publish an eval result receipt",
            "mutate sibling repos",
            "mark the aoa-evals strategic goal complete",
        ):
            if token not in claim_limit:
                issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))

    return issues


def validate_strategic_closeout_audit_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    audit_path = repo_root / STRATEGIC_CLOSEOUT_AUDIT_NAME
    location = STRATEGIC_CLOSEOUT_AUDIT_NAME

    require_tokens(
        repo_root=repo_root,
        path_name=STRATEGIC_CLOSEOUT_AUDIT_NAME,
        tokens=STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME,
        tokens=STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
        (
            "docs/README.md",
            ("Mechanic And Evidence Anchors",),
        ),
        (
            "docs/README.md",
            (STRATEGIC_CLOSEOUT_AUDIT_NAME, "Strategic Closeout Audit"),
        ),
        (
            "mechanics/release-support/parts/strategic-closeout/README.md",
            (
                STRATEGIC_CLOSEOUT_AUDIT_NAME,
                "goal open",
                "GitHub",
                "current objective audit",
            ),
        ),
        (
            "docs/RELEASING.md",
            (
                STRATEGIC_CLOSEOUT_AUDIT_NAME,
                "requirement-by-requirement handoff evidence",
                "current objective audit and landing evidence",
            ),
        ),
        (
            RELEASE_SUPPORT_MECHANIC_README_NAME,
            (
                STRATEGIC_CLOSEOUT_AUDIT_NAME,
                "Strategic Closeout Audit",
                "Goal completion routes",
            ),
        ),
        (
            "ROADMAP.md",
            ("Release-support posture", "mechanics/release-support/README.md"),
        ),
        ("CHANGELOG.md", (STRATEGIC_CLOSEOUT_AUDIT_NAME, "goal completion")),
        (
            "docs/decisions/README.md",
            (STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME, "Goal completion"),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    payload = load_json_payload(audit_path, issues)
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
        "current_objective_ref": "thread goal: deep mechanics refactor as proof-side organ with evidence-derived parent map, part contracts, active-first legacy, and source-of-truth validation",
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

    required_requirement_ids = {
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
    }
    requirements = payload.get("requirements_review")
    if isinstance(requirements, list):
        seen_requirement_ids: set[str] = set()
        for index, requirement in enumerate(requirements):
            req_location = f"{location}.requirements_review[{index}]"
            if not isinstance(requirement, dict):
                issues.append(ValidationIssue(req_location, "requirement entry must be an object"))
                continue
            requirement_id = requirement.get("requirement_id")
            if isinstance(requirement_id, str):
                seen_requirement_ids.add(requirement_id)
            else:
                issues.append(ValidationIssue(req_location, "requirement_id must be a string"))
            if requirement.get("status") != "satisfied_for_local_refactor":
                issues.append(
                    ValidationIssue(
                        req_location,
                        "status must stay 'satisfied_for_local_refactor'",
                    )
                )
            evidence_refs = requirement.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                issues.append(ValidationIssue(req_location, "evidence_refs must be a non-empty list"))
            else:
                for ref_index, evidence_ref in enumerate(evidence_refs):
                    parse_repo_ref(
                        evidence_ref,
                        location=f"{req_location}.evidence_refs[{ref_index}]",
                        issues=issues,
                    )
            claim_limit = requirement.get("claim_limit")
            if not isinstance(claim_limit, str) or len(claim_limit) < 40:
                issues.append(ValidationIssue(req_location, "claim_limit must be a meaningful string"))
        missing_requirement_ids = required_requirement_ids - seen_requirement_ids
        for requirement_id in sorted(missing_requirement_ids):
            issues.append(
                ValidationIssue(
                    f"{location}.requirements_review",
                    f"missing requirement_id {requirement_id!r}",
                )
            )
    else:
        issues.append(ValidationIssue(location, "requirements_review must be a list"))

    required_trap_ids = {
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
        missing_trap_ids = required_trap_ids - seen_trap_ids
        for trap_id in sorted(missing_trap_ids):
            issues.append(
                ValidationIssue(
                    f"{location}.trap_review",
                    f"missing trap_id {trap_id!r}",
                )
            )
    else:
        issues.append(ValidationIssue(location, "trap_review must be a list"))

    required_commands = {
        "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py tests/test_validate_repo.py -k strategic_closeout",
        "python -m pytest -q tests/test_validate_repo.py -k generated_route_residue",
        ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
        MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
        ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
        ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
        DECISION_ROUTE_RESIDUE_COMMAND,
        REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
        SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract",
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
    }
    verification_snapshot = payload.get("verification_snapshot")
    if isinstance(verification_snapshot, list):
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
    else:
        issues.append(ValidationIssue(location, "verification_snapshot must be a list"))

    open_items = payload.get("open_items_before_goal_completion")
    if isinstance(open_items, list):
        joined_open_items = "\n".join(item for item in open_items if isinstance(item, str))
        for token in (
            "requirement-by-requirement mechanics objective audit",
            "cross-root evidence clusters",
            "payload coverage anchors",
            "PROVENANCE.md",
            "old names",
            "full local validation battery",
            "requested landing route",
            "GitHub Repo Validation",
            "clean worktree",
        ):
            if token not in joined_open_items:
                issues.append(
                    ValidationIssue(
                        f"{location}.open_items_before_goal_completion",
                        f"open items must mention '{token}'",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "open_items_before_goal_completion must be a list"))

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
    else:
        for token in (
            "does not mark the goal complete",
            "does not treat PR or GitHub landing alone as objective completion",
            "does not publish a release",
            "does not create a tag",
            "does not publish a GitHub Release",
            "does not publish an eval result receipt",
            "does not promote any bundle",
            "does not accept runtime evidence",
            "does not mutate sibling repos",
        ):
            if token not in claim_limit:
                issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))

    return issues


def validate_release_prep_pr_handoff_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    handoff_path = repo_root / RELEASE_PREP_PR_HANDOFF_NAME
    location = RELEASE_PREP_PR_HANDOFF_NAME

    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_PREP_PR_HANDOFF_NAME,
        tokens=RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RELEASE_PREP_PR_HANDOFF_DECISION_NAME,
        tokens=RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
        (
            "docs/README.md",
            ("Mechanic And Evidence Anchors",),
        ),
        (
            "docs/README.md",
            (RELEASE_PREP_PR_HANDOFF_NAME, "Release Prep PR Handoff"),
        ),
        (
            "mechanics/release-support/parts/pr-handoff/README.md",
            (
                RELEASE_PREP_PR_HANDOFF_NAME,
                "branch",
                "GitHub evidence",
                "goal completion",
            ),
        ),
        (
            "docs/RELEASING.md",
            (
                RELEASE_PREP_PR_HANDOFF_NAME,
                "pre-PR snapshot",
                "current git and GitHub evidence for live branch, commit, push, PR",
            ),
        ),
        (
            RELEASE_SUPPORT_MECHANIC_README_NAME,
            (
                RELEASE_PREP_PR_HANDOFF_NAME,
                "Release Prep PR Handoff",
                "snapshot status for branch",
            ),
        ),
        (
            RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
            (
                RELEASE_PREP_PR_HANDOFF_NAME,
                "live PR or GitHub `Repo Validation` state",
            ),
        ),
        (
            "ROADMAP.md",
            ("Release-support posture", "mechanics/release-support/README.md"),
        ),
        ("CHANGELOG.md", (RELEASE_PREP_PR_HANDOFF_NAME, "goal completion")),
        (
            "docs/decisions/README.md",
            (RELEASE_PREP_PR_HANDOFF_DECISION_NAME, "live PR status"),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    payload = load_json_payload(handoff_path, issues)
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
        expected_status = {
            "branch_status": "not_created_by_this_handoff",
            "commit_status": "not_created_by_this_handoff",
            "push_status": "not_attempted",
            "pr_status": "not_opened",
            "repo_validation_status": "not_observed_for_this_uncommitted_diff",
            "merge_status": "not_attempted",
            "tag_status": "not_created",
            "github_release_status": "not_published",
        }
        for key, expected in expected_status.items():
            if github_status.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{location}.pre_handoff_github_status",
                        f"pre_handoff {key} must be {expected!r}",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "pre_handoff_github_status must be a JSON object"))

    required_group_ids = {
        "root_design_and_route",
        "decision_memory",
        "roadmap_changelog_quests",
        "proof_topology_legacy_mechanics",
        "active_proof_loop",
        "agent_lane_and_generated_readers",
        "validators_and_tests",
    }
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
            evidence_refs = group.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                issues.append(ValidationIssue(group_location, "evidence_refs must be a non-empty list"))
            else:
                for ref_index, evidence_ref in enumerate(evidence_refs):
                    parse_repo_ref(
                        evidence_ref,
                        location=f"{group_location}.evidence_refs[{ref_index}]",
                        issues=issues,
                    )
        missing_group_ids = required_group_ids - seen_group_ids
        for group_id in sorted(missing_group_ids):
            issues.append(
                ValidationIssue(
                    f"{location}.changed_surface_groups",
                    f"missing group_id {group_id!r}",
                )
            )
    else:
        issues.append(ValidationIssue(location, "changed_surface_groups must be a list"))

    draft_pr_body = payload.get("draft_pr_body")
    if isinstance(draft_pr_body, list):
        joined_pr_body = "\n".join(item for item in draft_pr_body if isinstance(item, str))
        for token in (
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
        ):
            if token not in joined_pr_body:
                issues.append(
                    ValidationIssue(
                        f"{location}.draft_pr_body",
                        f"draft PR body must mention '{token}'",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "draft_pr_body must be a list"))

    required_commands = {
        "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_validate_repo.py -k release_prep_pr_handoff",
        "python -m pytest -q tests/test_validate_repo.py -k generated_route_residue",
        ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
        MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
        ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
        ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
        DECISION_ROUTE_RESIDUE_COMMAND,
        REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
        SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract",
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
    }
    verification_snapshot = payload.get("verification_snapshot")
    if isinstance(verification_snapshot, list):
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
    else:
        issues.append(ValidationIssue(location, "verification_snapshot must be a list"))

    landing_steps = payload.get("landing_steps")
    if isinstance(landing_steps, list):
        joined_landing_steps = "\n".join(item for item in landing_steps if isinstance(item, str))
        for token in (
            "create a branch",
            "commit the intended accumulated diff",
            "push the branch",
            "open a PR",
            "watch GitHub Repo Validation",
            "merge only after required checks are green",
            "worktree is clean",
            "final owner-visible completion audit",
        ):
            if token not in joined_landing_steps:
                issues.append(
                    ValidationIssue(
                        f"{location}.landing_steps",
                        f"landing steps must mention '{token}'",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "landing_steps must be a list"))

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
    else:
        for token in (
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
        ):
            if token not in claim_limit:
                issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))

    return issues


def validate_comparison_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    comparison_records = [
        record for record in records if record.manifest.get("baseline_mode") != "none"
    ]
    if selected_evals is not None:
        comparison_records = [
            record for record in comparison_records if record.name in selected_evals
        ]
    if not comparison_records:
        return []

    issues: list[ValidationIssue] = []
    doctrine_path = repo_root / "docs" / "COMPARISON_SPINE_GUIDE.md"
    readme_path = repo_root / "README.md"
    docs_readme_path = repo_root / "docs" / "README.md"
    selection_path = repo_root / EVAL_SELECTION_NAME
    index_path = repo_root / EVAL_INDEX_NAME

    try:
        doctrine_text = doctrine_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue("docs/COMPARISON_SPINE_GUIDE.md", "file is missing")]

    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        readme_text = ""
        issues.append(ValidationIssue("README.md", "file is missing"))

    try:
        docs_readme_text = docs_readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        docs_readme_text = ""
        issues.append(ValidationIssue("docs/README.md", "file is missing"))

    try:
        selection_text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        selection_text = ""
        issues.append(ValidationIssue(EVAL_SELECTION_NAME, "file is missing"))

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        index_text = ""
        issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))

    if "generated reader index" not in readme_text:
        issues.append(
            ValidationIssue(
                "README.md",
                "README.md must route generated comparison readers through the generated reader index",
            )
        )

    if "Comparison Spine Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Comparison Spine Guide",
            )
        )
    if "generated/comparison_spine.json" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must reference generated/comparison_spine.json",
            )
        )

    if "## Pick Comparison Surface" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must include a 'Pick Comparison Surface' chooser section",
            )
        )

    if "comparison spine" not in index_text.lower():
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the comparison spine as a public program layer",
            )
        )

    doctrine_names = {record.name for record in comparison_records}
    doctrine_names.add("aoa-eval-integrity-check")
    for name in sorted(doctrine_names):
        if name not in doctrine_text:
            issues.append(
                ValidationIssue(
                    "docs/COMPARISON_SPINE_GUIDE.md",
                    f"comparison doctrine must mention '{name}'",
                )
            )

    for record in comparison_records:
        comparison_surface = record.manifest.get("comparison_surface")
        if not isinstance(comparison_surface, dict):
            continue
        selection_question = comparison_surface.get("selection_question")
        if isinstance(selection_question, str) and selection_question not in selection_text:
            issues.append(
                ValidationIssue(
                    EVAL_SELECTION_NAME,
                    f"EVAL_SELECTION.md must include the comparison selector question for '{record.name}'",
                )
            )

    return issues


def validate_artifact_process_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / "docs" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    selection_text = read_text_or_issue(
        repo_root / EVAL_SELECTION_NAME,
        issues,
        root=repo_root,
    )
    index_text = read_text_or_issue(
        repo_root / EVAL_INDEX_NAME,
        issues,
        root=repo_root,
    )

    if "Artifact Process Separation Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Artifact Process Separation Guide",
            )
        )
    if "## Artifact Process Layer" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the artifact/process layer as a bounded program layer",
            )
        )
    if "standalone artifact and workflow surfaces" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must say that the artifact/process bridge is read only after the standalone artifact and workflow surfaces",
            )
        )

    for phrase in (
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
        "matched conditions",
        "style-over-substance",
        "mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md",
        "mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    ARTIFACT_PROCESS_GUIDE_NAME,
                    f"artifact/process doctrine must mention '{phrase}'",
                )
            )

    record_map = {record.name: record for record in records}
    bundle_phrase_checks = {
        "aoa-artifact-review-rubric": ("artifact-side reading",),
        "aoa-bounded-change-quality": ("process-side reading",),
        "aoa-output-vs-process-gap": ("matched-condition", "side_by_side_note"),
        "aoa-witness-trace-integrity": ("adjacent witness context",),
        "aoa-compost-provenance-preservation": ("adjacent compost context",),
    }
    for name, phrases in bundle_phrase_checks.items():
        record = record_map.get(name)
        if record is None:
            continue
        bundle_text = "\n".join(record.sections.values())
        for phrase in phrases:
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"artifact/process distinctness wording must mention '{phrase}'",
                    )
                )
    return issues


def validate_repeated_window_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    if selected_evals is not None and "aoa-longitudinal-growth-snapshot" not in selected_evals:
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / "docs" / "REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    selection_text = read_text_or_issue(
        repo_root / EVAL_SELECTION_NAME,
        issues,
        root=repo_root,
    )
    index_text = read_text_or_issue(
        repo_root / EVAL_INDEX_NAME,
        issues,
        root=repo_root,
    )

    if "Repeated Window Discipline Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Repeated Window Discipline Guide",
            )
        )
    for phrase in (
        "aoa-longitudinal-growth-snapshot",
        "context_note",
        "transition_note",
        "after",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    REPEATED_WINDOW_GUIDE_NAME,
                    f"repeated-window doctrine must mention '{phrase}'",
                )
            )

    if "context_note" not in selection_text or "transition_note" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must explain context_note and transition_note for repeated-window reading",
            )
        )
    if "mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must reference mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md for repeated-window discipline",
            )
        )

    record_map = {record.name: record for record in records}
    record = record_map.get("aoa-longitudinal-growth-snapshot")
    if record is not None:
        bundle_text = "\n".join(record.sections.values())
        for phrase in ("context_note", "transition_note"):
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"longitudinal bundle wording must mention '{phrase}'",
                    )
                )
    return issues


def validate_integrity_taxonomy_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-eval-integrity-check",
        "aoa-regression-same-task",
        "aoa-output-vs-process-gap",
        "aoa-longitudinal-growth-snapshot",
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    eval_text = read_text_or_issue(
        source_eval_dir(repo_root, "aoa-eval-integrity-check") / "EVAL.md",
        issues,
        root=repo_root,
    )
    review_text = read_text_or_issue(
        source_eval_dir(repo_root, "aoa-eval-integrity-check") / "notes" / "review-contract.md",
        issues,
        root=repo_root,
    )
    example_report_location = "evals/capability/aoa-eval-integrity-check/examples/example-report.md"
    example_report_text = read_text_or_issue(
        source_eval_dir(repo_root, "aoa-eval-integrity-check") / "examples" / "example-report.md",
        issues,
        root=repo_root,
    )
    schema_location = "evals/capability/aoa-eval-integrity-check/reports/summary.schema.json"
    schema_payload = load_json_payload(
        source_eval_dir(repo_root, "aoa-eval-integrity-check") / "reports" / "summary.schema.json",
        issues,
    )
    schema_enum: list[str] = []
    if isinstance(schema_payload, dict):
        properties = schema_payload.get("properties", {})
        if isinstance(properties, dict):
            per_target_breakdown = properties.get("per_target_breakdown", {})
            if isinstance(per_target_breakdown, dict):
                items = per_target_breakdown.get("items", {})
                if isinstance(items, dict):
                    item_properties = items.get("properties", {})
                    if isinstance(item_properties, dict):
                        risk_schema = item_properties.get("integrity_risk_class", {})
                        if isinstance(risk_schema, dict):
                            raw_enum = risk_schema.get("enum", [])
                            if isinstance(raw_enum, list):
                                schema_enum = [
                                    item
                                    for item in raw_enum
                                    if isinstance(item, str)
                                ]
    if tuple(schema_enum) != INTEGRITY_RISK_CLASSES:
        issues.append(
            ValidationIssue(
                schema_location,
                "integrity_risk_class enum must match the public integrity risk taxonomy",
            )
        )

    for phrase in INTEGRITY_RISK_CLASSES:
        if phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/notes/review-contract.md",
                    f"integrity review contract must mention '{phrase}'",
                )
            )
        if phrase not in eval_text and phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/EVAL.md",
                    f"integrity sidecar surfaces must mention '{phrase}' in EVAL.md or review-contract.md",
                )
            )
        if phrase not in example_report_text:
            issues.append(
                ValidationIssue(
                    example_report_location,
                    f"integrity example report must mention '{phrase}'",
                )
            )
    return issues


def validate_shared_proof_infra_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    fixture_relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
    }
    runner_relevant_names = fixture_relevant_names | {
        "aoa-longitudinal-growth-snapshot",
    }
    relevant_names = fixture_relevant_names | runner_relevant_names
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / "docs" / "SHARED_PROOF_INFRA_GUIDE.md",
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    fixtures_agents_text = read_text_or_issue(
        repo_root / "fixtures" / "AGENTS.md",
        issues,
        root=repo_root,
    )
    reports_agents_text = read_text_or_issue(
        repo_root / "reports" / "AGENTS.md",
        issues,
        root=repo_root,
    )
    runner_surface_text = read_text_or_issue(
        repo_root / PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
        issues,
        root=repo_root,
    )

    if "Shared Proof Infra Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Shared Proof Infra Guide",
            )
        )
    for phrase in (
        "additional_shared_fixture_family_paths",
        "additional_paired_readout_paths",
        "shared_fixture_family_path",
        "paired_readout_path",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    SHARED_PROOF_INFRA_GUIDE_NAME,
                    f"shared proof infra guide must mention '{phrase}'",
                )
            )

    if "additional_shared_fixture_family_paths" not in fixtures_agents_text:
        issues.append(
            ValidationIssue(
                "fixtures/AGENTS.md",
                "fixtures/AGENTS.md must describe additional_shared_fixture_family_paths",
            )
        )
    if "additional_paired_readout_paths" not in reports_agents_text:
        issues.append(
            ValidationIssue(
                "reports/AGENTS.md",
                "reports/AGENTS.md must describe additional_paired_readout_paths",
            )
        )
    if "additional_paired_readout_paths" not in runner_surface_text:
        issues.append(
            ValidationIssue(
                PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
                (
                    f"{PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME} "
                    "must describe additional_paired_readout_paths"
                ),
            )
        )

    fixture_bundle_names = (
        selected_evals.intersection(fixture_relevant_names)
        if selected_evals is not None
        else fixture_relevant_names
    )
    runner_bundle_names = (
        selected_evals.intersection(runner_relevant_names)
        if selected_evals is not None
        else runner_relevant_names
    )
    fixture_contracts_with_additional = 0
    runner_contracts_with_additional = 0
    for name in fixture_bundle_names:
        fixture_payload = eval_catalog_contract.load_optional_json(
            source_eval_dir(repo_root, name) / "fixtures" / "contract.json"
        )
        fixture_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            fixture_payload if isinstance(fixture_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        )
        if fixture_paths:
            fixture_contracts_with_additional += 1
    for name in runner_bundle_names:
        runner_payload = eval_catalog_contract.load_optional_json(
            source_eval_dir(repo_root, name) / "runners" / "contract.json"
        )
        runner_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            runner_payload if isinstance(runner_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        )
        if runner_paths:
            runner_contracts_with_additional += 1

    minimum_fixture_count = 1 if selected_evals is not None and fixture_bundle_names else 2
    minimum_runner_count = 1 if selected_evals is not None and runner_bundle_names else 2
    if fixture_bundle_names and fixture_contracts_with_additional < minimum_fixture_count:
        issues.append(
            ValidationIssue(
                "fixtures/README.md",
                "shared proof infra must be exercised by fixture contracts in more than one bundle family",
            )
        )
    if runner_bundle_names and runner_contracts_with_additional < minimum_runner_count:
        issues.append(
            ValidationIssue(
                "reports/README.md",
                "shared proof infra must be exercised by runner contracts in more than one bundle family",
            )
        )
    return issues


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        raise FileNotFoundError(f"missing source eval directory at {source_root}")

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_name = eval_dir.name
        if eval_name in eval_dirs:
            raise ValueError(
                "duplicate source eval directory name "
                f"'{eval_name}' at {relative_location(eval_dirs[eval_name], repo_root)} "
                f"and {relative_location(eval_dir, repo_root)}"
            )
        eval_dirs[eval_name] = eval_dir
    return eval_dirs


def discover_eval_names(repo_root: Path) -> list[str]:
    return sorted(discover_eval_dirs(repo_root))


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    try:
        return discover_eval_dirs(repo_root).get(
            eval_name,
            repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
        )
    except (FileNotFoundError, ValueError):
        return repo_root / SOURCE_EVALS_DIR_NAME / eval_name


def collect_catalog_records(
    repo_root: Path,
    eval_names: Sequence[str] | None = None,
) -> tuple[list[ValidationIssue], list[EvalBundleRecord]]:
    eval_dirs = discover_eval_dirs(repo_root)
    all_eval_names = sorted(eval_dirs)
    selected_names = list(eval_names) if eval_names is not None else all_eval_names
    known_eval_names = set(all_eval_names)

    issues: list[ValidationIssue] = []
    records: list[EvalBundleRecord] = []
    for name in selected_names:
        bundle_issues, record = validate_bundle(
            repo_root,
            name,
            known_eval_names,
            eval_dirs=eval_dirs,
        )
        issues.extend(bundle_issues)
        if record is not None:
            records.append(record)
    return issues, records


def full_catalog_entry(repo_root: Path, record: EvalBundleRecord) -> dict[str, Any]:
    return eval_catalog_contract.full_catalog_entry(repo_root, record)


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    return eval_catalog_contract.project_min_catalog(full_catalog)


def project_min_catalog_safely(
    full_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    try:
        return project_min_catalog(full_catalog)
    except (KeyError, TypeError):
        issues.append(
            ValidationIssue(
                location,
                f"{label} is malformed; min projection could not be computed",
            )
        )
        return None


def validate_catalog_metadata(
    actual_catalog: dict[str, Any],
    expected_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
) -> None:
    if (
        actual_catalog.get("catalog_version") != expected_catalog["catalog_version"]
        or actual_catalog.get("source_of_truth") != expected_catalog["source_of_truth"]
    ):
        issues.append(
            ValidationIssue(
                location,
                f"{label} metadata is out of date; run 'python scripts/build_catalog.py'",
            )
        )


def build_catalog_payloads(
    repo_root: Path,
    records: list[EvalBundleRecord],
) -> tuple[dict[str, Any], dict[str, Any]]:
    return eval_catalog_contract.build_catalog_payloads(repo_root, records)


def build_capsule_payload(
    repo_root: Path,
    records: list[EvalBundleRecord],
    full_catalog: dict[str, Any],
) -> dict[str, Any]:
    return eval_capsule_contract.build_capsule_payload(repo_root, records, full_catalog)


def build_comparison_spine_payload(
    repo_root: Path,
    records: list[EvalBundleRecord],
    full_catalog: dict[str, Any],
) -> dict[str, Any]:
    return eval_comparison_spine_contract.build_comparison_spine_payload(
        repo_root,
        records,
        full_catalog,
    )


def read_json_file(path: Path, issues: list[ValidationIssue], repo_root: Path) -> Any | None:
    payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return payload


def write_json_file(path: Path, payload: Any, compact: bool = False) -> None:
    eval_catalog_contract.write_json_file(path, payload, compact=compact)


def iter_generated_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    generated_root = repo_root / GENERATED_DIR_NAME
    if generated_root.is_dir():
        paths.update(path for path in generated_root.glob("*.json") if path.is_file())
    mechanics_root = repo_root / "mechanics"
    if mechanics_root.is_dir():
        paths.update(
            path
            for path in mechanics_root.rglob("generated/*.json")
            if path.is_file()
        )
    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def format_generated_json_location(file_location: str, json_path: Sequence[str | int]) -> str:
    suffix = ""
    for part in json_path:
        if isinstance(part, int):
            suffix += f"[{part}]"
        else:
            suffix += f".{part}"
    return f"{file_location}{suffix}"


def mechanic_part_root_for_generated_json(path: Path, repo_root: Path) -> Path | None:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return None
    if len(parts) < 6:
        return None
    if parts[0] != "mechanics" or parts[2] != "parts" or parts[4] != "generated":
        return None
    return repo_root.joinpath(*parts[:4])


def generated_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = value.strip().replace("\\", "/")
    if not normalized or normalized.startswith("repo:"):
        return None

    for exact_route in GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{exact_route}'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{prefix}'"
            )

    part_root = mechanic_part_root_for_generated_json(source_file, repo_root)
    if part_root is not None:
        part_local_path = part_root / normalized
        if part_local_path.exists():
            return None

    for exact_route in GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{exact_route}/'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{prefix}'"
            )

    return None


def validate_generated_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def walk_json(
        value: Any,
        *,
        source_file: Path,
        file_location: str,
        json_path: list[str | int],
    ) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in GENERATED_ROUTE_RESIDUE_SKIP_KEYS:
                    continue
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, key],
                )
            return
        if isinstance(value, list):
            for index, child in enumerate(value):
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, index],
                )
            return
        if not isinstance(value, str):
            return

        message = generated_route_residue_message(
            value,
            source_file=source_file,
            repo_root=repo_root,
        )
        if message is None:
            return
        issues.append(
            ValidationIssue(
                format_generated_json_location(file_location, json_path),
                message,
            )
        )

    for path in iter_generated_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in contract_issues
        )
        if payload is None:
            continue
        walk_json(
            payload,
            source_file=path,
            file_location=file_location,
            json_path=[],
        )

    return issues


def iter_active_mechanic_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    mechanics_readme = repo_root / MECHANICS_README_NAME
    if mechanics_readme.is_file():
        paths.add(mechanics_readme)

    mechanics_root = repo_root / "mechanics"
    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = mechanics_root / parent_name
        for route_card_name in ("AGENTS.md", "README.md", "PARTS.md"):
            route_card = parent_root / route_card_name
            if route_card.is_file():
                paths.add(route_card)

        parts_root = parent_root / "parts"
        parts_readme = parts_root / "README.md"
        if parts_readme.is_file():
            paths.add(parts_readme)
        if not parts_root.is_dir():
            continue
        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            part_readme = part_root / "README.md"
            if part_readme.is_file():
                paths.add(part_readme)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def mechanic_owner_root_for_route_card(path: Path, repo_root: Path) -> Path:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return repo_root / "mechanics"

    if len(parts) >= 5 and parts[0] == "mechanics" and parts[2] == "parts":
        return repo_root.joinpath(*parts[:4])
    if len(parts) >= 2 and parts[0] == "mechanics":
        return repo_root.joinpath(*parts[:2])
    return repo_root / "mechanics"


def normalize_active_mechanic_route_token(token: str) -> str:
    normalized = token.strip().replace("\\", "/")
    normalized = normalized.strip(ACTIVE_MECHANIC_ROUTE_RESIDUE_TOKEN_STRIP_CHARS)
    return normalized.rstrip("/")


def root_route_card_reference_is_allowed(normalized: str) -> bool:
    if "/" not in normalized:
        return True
    district_name, remainder = normalized.split("/", 1)
    if district_name not in ROOT_ROUTE_CARD_ONLY_DISTRICTS:
        return False
    if not remainder:
        return True
    return remainder in ROOT_ROUTE_CARD_ONLY_DISTRICTS[district_name]


def active_mechanic_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None

    owner_root = mechanic_owner_root_for_route_card(source_file, repo_root)
    if (owner_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "active mechanic route card must not point at route-card-only root "
        f"district payload '{normalized}'; use a part-local path under the "
        f"same part root, a bundle-local `evals/<family>/<eval>/...` path, or the "
        f"root route card '{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def active_mechanic_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "active mechanic route card must use the active mechanic parent "
                f"`mechanics/{correct_route}/`, not legacy parent route "
                f"`{wrong_route}/`"
            )
    return None


def validate_active_mechanic_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_active_mechanic_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = active_mechanic_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = active_mechanic_legacy_parent_residue_message(
                    match.group("token")
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_active_mechanic_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_active_mechanic_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name=ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME,
        tokens=ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME,
            "Active Mechanic Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Active mechanic route residue", "same part root"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("authored mechanics route cards", "legacy parent route"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


def iter_root_authored_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()

    for path_name in ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES:
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    docs_root = repo_root / "docs"
    if docs_root.is_dir():
        paths.update(path for path in docs_root.glob("*.md") if path.is_file())

    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        district = repo_root / district_name
        for allowed_name in allowed_names:
            path = district / allowed_name
            if path.is_file():
                paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def root_authored_route_context_allows(
    lines: Sequence[str],
    line_number: int,
) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS)


def root_authored_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "root-facing authored surface must not point at route-card-only root "
        f"district payload '{normalized}'; use `evals/<family>/<eval>/...`, an "
        "active `mechanics/...` route, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def validate_root_authored_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_root_authored_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if root_authored_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = root_authored_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_root_authored_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_root_authored_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name=ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME,
        tokens=ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME,
            "Root Authored Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Root authored route residue", "`evals/<family>/<eval>/...`"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("root-facing authored surfaces", "historical context"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


def iter_decision_route_residue_files(repo_root: Path) -> list[Path]:
    decisions_root = repo_root / "docs" / "decisions"
    if not decisions_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in decisions_root.glob("*.md")
            if path.name not in {"AGENTS.md", "README.md", "TEMPLATE.md"}
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def decision_route_context_allows(
    lines: Sequence[str],
    line_number: int,
) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS)


def decision_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "decision record must not present route-card-only root district payload "
        f"'{normalized}' as a current route; mark it as former root or "
        "historical context, route to `evals/<family>/<eval>/...` or active "
        f"`mechanics/...`, or cite the root route card '{district_name}/README.md' "
        f"or '{district_name}/AGENTS.md'"
    )


def validate_decision_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_decision_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if decision_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = decision_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_decision_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_decision_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_ROUTE_RESIDUE_DECISION_NAME,
        tokens=DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            DECISION_ROUTE_RESIDUE_DECISION_NAME,
            "Decision Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Decision route residue", "historical context"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("decision records", "former root"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


def iter_repo_config_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for path_name in (".gitignore", "pytest.ini"):
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    workflows_root = repo_root / ".github" / "workflows"
    if workflows_root.is_dir():
        paths.update(path for path in workflows_root.glob("*.yml") if path.is_file())
        paths.update(path for path in workflows_root.glob("*.yaml") if path.is_file())

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def repo_config_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "repo config surface must not point at route-card-only root district "
        f"payload '{normalized}'; use an active `mechanics/...` route, "
        f"`evals/<family>/<eval>/...`, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def repo_config_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "repo config surface must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/`"
            )
    return None


def validate_repo_config_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_repo_config_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = repo_config_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = repo_config_legacy_parent_residue_message(
                    match.group("token")
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_repo_config_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_repo_config_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name=REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME,
        tokens=REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME,
            "Repo Config Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Repo config route residue", ".gitignore"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("repo config surfaces", "legacy mechanic parent"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES = frozenset(
    {".json", ".md", ".txt", ".yaml", ".yml"}
)


def iter_source_bundle_route_residue_files(repo_root: Path) -> list[Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in source_root.rglob("*")
            if path.is_file() and path.suffix in SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def bundle_root_for_source_file(path: Path, repo_root: Path) -> Path | None:
    try:
        path.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
    except ValueError:
        return None

    for parent in (path.parent, *path.parents):
        if parent == repo_root:
            break
        try:
            parent.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
        except ValueError:
            continue
        if (parent / "EVAL.md").is_file() and (parent / "eval.yaml").is_file():
            return parent
    return None


def source_bundle_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if normalized.startswith("repo:"):
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None

    bundle_root = bundle_root_for_source_file(source_file, repo_root)
    if bundle_root is not None and (bundle_root / normalized).exists():
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "source bundle must not carry ambiguous route-card-only root district "
        f"payload '{normalized}'; use a bundle-local path that exists under the "
        "owning eval package, `evals/<family>/<target>/...`, a repo-qualified sibling ref, "
        f"or the root route card '{district_name}/README.md' or "
        f"'{district_name}/AGENTS.md'"
    )


def source_bundle_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "source bundle must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/` or "
                "a provenance/legacy route with explicit historical context"
            )
    return None


def validate_source_bundle_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_source_bundle_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = source_bundle_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = source_bundle_legacy_parent_residue_message(
                    match.group("token")
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_source_bundle_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_source_bundle_route_residue(repo_root)
    require_tokens(
        repo_root=repo_root,
        path_name=SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME,
        tokens=SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME,
            "Source Bundle Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source bundle route residue", "repo-qualified sibling"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("source proof bundles", "repo-qualified sibling"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


MECHANIC_PAYLOAD_ROUTE_RESIDUE_SUFFIXES = frozenset(
    {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_ROUTE_CARD_NAMES = frozenset(
    {"AGENTS.md", "PARTS.md", "PROVENANCE.md", "README.md"}
)


def iter_mechanic_payload_route_residue_files(repo_root: Path) -> list[Path]:
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in mechanics_root.rglob("*")
            if path.is_file()
            and path.suffix in MECHANIC_PAYLOAD_ROUTE_RESIDUE_SUFFIXES
            and path.name not in MECHANIC_PAYLOAD_ROUTE_RESIDUE_ROUTE_CARD_NAMES
            and "legacy" not in path.relative_to(repo_root).parts
            and "generated" not in path.relative_to(repo_root).parts
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def mechanic_payload_owner_root_for_source_file(path: Path, repo_root: Path) -> Path:
    try:
        relative_parts = path.relative_to(repo_root).parts
    except ValueError:
        return repo_root / "mechanics"

    if (
        len(relative_parts) >= 4
        and relative_parts[0] == "mechanics"
        and relative_parts[2] == "parts"
    ):
        return repo_root.joinpath(*relative_parts[:4])
    if len(relative_parts) >= 2 and relative_parts[0] == "mechanics":
        return repo_root.joinpath(*relative_parts[:2])
    return repo_root / "mechanics"


def mechanic_payload_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None
    if normalized.startswith("repo:"):
        return None
    if root_route_card_reference_is_allowed(normalized):
        return None

    owner_root = mechanic_payload_owner_root_for_source_file(source_file, repo_root)
    if (owner_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None
    if (repo_root / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "active mechanics payload must not carry ambiguous route-card-only "
        f"root district payload '{normalized}'; use a path that resolves under "
        "the same mechanic or part root, an active repo path, a repo-qualified "
        f"sibling ref, or the root route card '{district_name}/README.md' or "
        f"'{district_name}/AGENTS.md'"
    )


def mechanic_payload_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "active mechanics payload must not point at legacy mechanic "
                f"parent `{wrong_route}/`; use active "
                f"`mechanics/{correct_route}/` or a provenance/legacy route "
                "with explicit historical context"
            )
    return None


def validate_mechanic_payload_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_mechanic_payload_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = mechanic_payload_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = mechanic_payload_legacy_parent_residue_message(
                    match.group("token")
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


MECHANIC_MANIFEST_STRUCTURED_ROUTE_KEYS = frozenset(
    {
        "generated_surfaces",
        "observed_surfaces",
        "proof_surfaces",
        "source_files",
        "source_surfaces",
        "validation_surfaces",
    }
)


def iter_json_string_values_for_keys(
    payload: Any, keys: frozenset[str]
) -> Iterable[tuple[str, str]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in keys and isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        yield key, item
            yield from iter_json_string_values_for_keys(value, keys)
    elif isinstance(payload, list):
        for item in payload:
            yield from iter_json_string_values_for_keys(item, keys)


def repo_relative_path_or_glob_exists(repo_root: Path, value: str) -> bool:
    normalized = value.split("#", 1)[0].strip().strip("`")
    if not normalized or normalized.startswith(("repo:", "component:")):
        return True
    if "<" in normalized or ">" in normalized:
        return True
    if "*" in normalized:
        return any(repo_root.glob(normalized))
    return (repo_root / normalized).exists()


def validate_mechanic_manifest_path_glob_routes(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    mechanics_root = repo_root / "mechanics"
    if not mechanics_root.is_dir():
        return issues

    for path in sorted(mechanics_root.glob("**/manifests/**/*.json")):
        if "legacy" in path.relative_to(repo_root).parts:
            continue
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        for key, value in iter_json_string_values_for_keys(payload, frozenset({"path_globs"})):
            if not value.startswith("docs/"):
                continue
            if repo_relative_path_or_glob_exists(repo_root, value):
                continue
            issues.append(
                ValidationIssue(
                    path.relative_to(repo_root).as_posix(),
                    "mechanic manifest path_globs must not point at unresolved root-authored docs globs; use current repo-relative mechanic paths or an existing root-owned docs surface",
                )
            )
        for key, value in iter_json_string_values_for_keys(
            payload, MECHANIC_MANIFEST_STRUCTURED_ROUTE_KEYS
        ):
            normalized = normalize_active_mechanic_route_token(value)
            if not normalized:
                continue
            if root_route_card_reference_is_allowed(normalized):
                continue
            district_name = normalized.split("/", 1)[0]
            if district_name not in ROOT_ROUTE_CARD_ONLY_DISTRICTS:
                continue
            issues.append(
                ValidationIssue(
                    path.relative_to(repo_root).as_posix(),
                    "mechanic manifest structured route fields must not use "
                    f"route-card-only root district payload `{normalized}`; "
                    "use the current repo-relative mechanic path",
                )
            )

    return issues


def validate_mechanic_payload_route_residue_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues = validate_mechanic_payload_route_residue(repo_root)
    issues.extend(validate_mechanic_manifest_path_glob_routes(repo_root))
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME,
        tokens=MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_DECISION_NAME,
            "Mechanic Payload Route Residue Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Mechanic payload route residue", "repo-qualified sibling"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("active mechanics payload", "repo-qualified sibling"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
        issues=issues,
    )
    return issues


def validate_generated_catalogs(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    min_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME

    expected_full, expected_min = build_catalog_payloads(repo_root, records)
    actual_full = read_json_file(full_path, issues, repo_root)
    actual_min = read_json_file(min_path, issues, repo_root)

    if actual_full is None or actual_min is None:
        return issues

    full_location = relative_location(full_path, repo_root)
    min_location = relative_location(min_path, repo_root)
    if target_eval_names is None:
        if actual_full != expected_full:
            issues.append(
                ValidationIssue(
                    full_location,
                    "generated catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min != expected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "generated min catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min = project_min_catalog_safely(
            actual_full,
            location=full_location,
            label="generated catalog",
            issues=issues,
        )
        if projected_min is None:
            return issues
        if actual_min != projected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "min catalog must stay a projection of the full catalog",
                )
            )
        return issues

    validate_catalog_metadata(
        actual_full,
        expected_full,
        location=full_location,
        label="generated catalog",
        issues=issues,
    )
    validate_catalog_metadata(
        actual_min,
        expected_min,
        location=min_location,
        label="generated min catalog",
        issues=issues,
    )

    full_entries, full_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_full,
        array_key="evals",
        key_name="name",
        location=full_location,
    )
    min_entries, min_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_min,
        array_key="evals",
        key_name="name",
        location=min_location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in full_entry_issues + min_entry_issues
    )

    expected_full_entries = {
        record.name: full_catalog_entry(repo_root, record)
        for record in records
    }
    expected_min_entries = {
        name: project_min_catalog(
            {
                "catalog_version": CATALOG_VERSION,
                "source_of_truth": CATALOG_SOURCE_OF_TRUTH,
                "evals": [entry],
            }
        )["evals"][0]
        for name, entry in expected_full_entries.items()
    }

    for eval_name in target_eval_names:
        actual_full_entry = full_entries.get(eval_name)
        actual_min_entry = min_entries.get(eval_name)
        if actual_full_entry is None:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog is missing eval '{eval_name}'",
                )
            )
            continue
        if actual_min_entry is None:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog is missing eval '{eval_name}'",
                )
            )
            continue

        expected_full_entry = expected_full_entries[eval_name]
        expected_min_entry = expected_min_entries[eval_name]
        if actual_full_entry != expected_full_entry:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min_entry != expected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min_catalog_payload = project_min_catalog_safely(
            {
                "catalog_version": actual_full.get("catalog_version"),
                "source_of_truth": actual_full.get("source_of_truth"),
                "evals": [actual_full_entry],
            },
            location=full_location,
            label=f"generated catalog entry for '{eval_name}'",
            issues=issues,
        )
        if projected_min_catalog_payload is None:
            continue
        projected_min_entry = projected_min_catalog_payload["evals"][0]
        if actual_min_entry != projected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' must stay a projection of the full catalog",
                )
            )

    return issues


def validate_generated_capsules(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    capsule_path = repo_root / GENERATED_DIR_NAME / CAPSULE_NAME
    capsule_location = relative_location(capsule_path, repo_root)

    expected_full, _expected_min = build_catalog_payloads(repo_root, records)
    expected_capsules = build_capsule_payload(repo_root, records, expected_full)
    actual_capsules = read_json_file(capsule_path, issues, repo_root)
    if actual_capsules is None:
        return issues

    if not isinstance(actual_capsules, dict):
        issues.append(
            ValidationIssue(capsule_location, "generated capsules payload must be an object")
        )
        return issues

    if actual_capsules.get("capsule_version") != CAPSULE_VERSION:
        issues.append(
            ValidationIssue(capsule_location, f"capsule_version must be {CAPSULE_VERSION}")
        )
    if actual_capsules.get("source_of_truth") != CAPSULE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(capsule_location, "source_of_truth does not match the capsule contract")
        )

    if target_eval_names is None:
        if actual_capsules != expected_capsules:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    "generated capsules are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        expected_entries, expected_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            expected_capsules,
            array_key="evals",
            key_name="name",
            location=capsule_location,
        )
        actual_entries, actual_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            actual_capsules,
            array_key="evals",
            key_name="name",
            location=capsule_location,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in expected_entry_issues + actual_entry_issues
        )
        for eval_name in target_eval_names:
            actual_entry = actual_entries.get(eval_name)
            if actual_entry is None:
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsules are missing eval '{eval_name}'",
                    )
                )
                continue
            if actual_entry != expected_entries[eval_name]:
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsule entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                    )
                )

    alignment_issues: list[ValidationIssue] = []
    actual_full = read_json_file(full_path, alignment_issues, repo_root)
    issues.extend(alignment_issues)
    if isinstance(actual_full, dict):
        contract_issues = eval_capsule_contract.validate_capsule_alignment(
            actual_full,
            actual_capsules,
            location=capsule_location,
            target_eval_names=set(target_eval_names) if target_eval_names is not None else None,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in contract_issues
        )

    return issues


def validate_generated_sections(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    sections_path = repo_root / GENERATED_DIR_NAME / SECTION_NAME
    sections_location = relative_location(sections_path, repo_root)

    expected_sections, section_contract_issues = eval_section_contract.build_sections_payload(
        repo_root,
        records,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in section_contract_issues
    )
    if section_contract_issues:
        return issues

    actual_sections = read_json_file(sections_path, issues, repo_root)
    if actual_sections is None:
        return issues
    if not isinstance(actual_sections, dict):
        issues.append(
            ValidationIssue(sections_location, "generated sections payload must be an object")
        )
        return issues

    if actual_sections.get("section_version") != SECTION_VERSION:
        issues.append(
            ValidationIssue(sections_location, f"section_version must be {SECTION_VERSION}")
        )
    if actual_sections.get("source_of_truth") != SECTION_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(sections_location, "source_of_truth does not match the section contract")
        )

    if target_eval_names is None:
        if actual_sections != expected_sections:
            issues.append(
                ValidationIssue(
                    sections_location,
                    "generated sections are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        expected_entries, expected_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            expected_sections,
            array_key="evals",
            key_name="name",
            location=sections_location,
        )
        actual_entries, actual_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            actual_sections,
            array_key="evals",
            key_name="name",
            location=sections_location,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in expected_entry_issues + actual_entry_issues
        )
        for eval_name in target_eval_names:
            actual_entry = actual_entries.get(eval_name)
            if actual_entry is None:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated sections are missing eval '{eval_name}'",
                    )
                )
                continue
            if actual_entry != expected_entries[eval_name]:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                    )
                )

    actual_full = read_json_file(full_path, issues, repo_root)
    if not isinstance(actual_full, dict):
        return issues

    catalog_entries, catalog_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_full,
        array_key="evals",
        key_name="name",
        location=relative_location(full_path, repo_root),
    )
    section_entries, section_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_sections,
        array_key="evals",
        key_name="name",
        location=sections_location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in catalog_entry_issues + section_entry_issues
    )
    if catalog_entry_issues or section_entry_issues:
        return issues

    catalog_names = set(catalog_entries)
    section_names = set(section_entries)
    if target_eval_names is not None:
        target_name_set = set(target_eval_names)
        catalog_names &= target_name_set
        section_names &= target_name_set

    for missing in sorted(catalog_names - section_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections are missing eval '{missing}' from generated/eval_catalog.json",
            )
        )
    for extra in sorted(section_names - catalog_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections include unknown eval '{extra}' from generated/eval_catalog.json",
            )
        )

    for eval_name in sorted(catalog_names & section_names):
        catalog_entry = catalog_entries[eval_name]
        section_entry = section_entries[eval_name]
        for field_name in ("category", "status", "verdict_shape", "eval_path"):
            if section_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{eval_name}' must align with full catalog field '{field_name}'",
                    )
                )

    return issues


def validate_generated_comparison_spine(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    comparison_spine_path = repo_root / GENERATED_DIR_NAME / COMPARISON_SPINE_NAME
    comparison_spine_location = relative_location(comparison_spine_path, repo_root)
    comparison_target_names = {
        record.name
        for record in records
        if record.manifest.get("baseline_mode") != "none"
    }
    if target_eval_names is not None:
        comparison_target_names &= set(target_eval_names)
    if not comparison_target_names and target_eval_names is not None:
        return issues

    expected_full, _expected_min = build_catalog_payloads(repo_root, records)
    expected_comparison_spine = build_comparison_spine_payload(repo_root, records, expected_full)
    actual_comparison_spine = read_json_file(comparison_spine_path, issues, repo_root)
    if actual_comparison_spine is None:
        return issues
    if not isinstance(actual_comparison_spine, dict):
        issues.append(
            ValidationIssue(
                comparison_spine_location,
                "generated comparison spine payload must be an object",
            )
        )
        return issues

    if actual_comparison_spine.get("comparison_spine_version") != COMPARISON_SPINE_VERSION:
        issues.append(
            ValidationIssue(
                comparison_spine_location,
                f"comparison_spine_version must be {COMPARISON_SPINE_VERSION}",
            )
        )
    if actual_comparison_spine.get("source_of_truth") != COMPARISON_SPINE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                comparison_spine_location,
                "source_of_truth does not match the comparison spine contract",
            )
        )

    if target_eval_names is None:
        if actual_comparison_spine != expected_comparison_spine:
            issues.append(
                ValidationIssue(
                    comparison_spine_location,
                    "generated comparison spine is out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        expected_entries, expected_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            expected_comparison_spine,
            array_key="evals",
            key_name="name",
            location=comparison_spine_location,
        )
        actual_entries, actual_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            actual_comparison_spine,
            array_key="evals",
            key_name="name",
            location=comparison_spine_location,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in expected_entry_issues + actual_entry_issues
        )
        for eval_name in sorted(comparison_target_names):
            actual_entry = actual_entries.get(eval_name)
            if actual_entry is None:
                issues.append(
                    ValidationIssue(
                        comparison_spine_location,
                        f"generated comparison spine is missing eval '{eval_name}'",
                    )
                )
                continue
            if actual_entry != expected_entries[eval_name]:
                issues.append(
                    ValidationIssue(
                        comparison_spine_location,
                        f"generated comparison spine entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                    )
                )

    actual_full = read_json_file(full_path, issues, repo_root)
    if not isinstance(actual_full, dict):
        return issues

    contract_issues = eval_comparison_spine_contract.validate_comparison_spine_alignment(
        actual_full,
        actual_comparison_spine,
        location=comparison_spine_location,
        target_eval_names=comparison_target_names if comparison_target_names else None,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return issues


def validate_runtime_integrity_review_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    doc_path = repo_root / RUNTIME_INTEGRITY_REVIEW_DOC_NAME
    docs_map_path = repo_root / "docs" / "README.md"
    landing_path = repo_root / "mechanics" / "agon" / "legacy" / "raw" / "AGON_WAVE10_EVAL_LANDING.md"
    schema_path = repo_root / RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    example_path = repo_root / RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"runtime integrity review guide must mention '{token}'",
                    )
                )

    docs_map_text = read_text_or_issue(docs_map_path, issues, root=repo_root)
    if docs_map_text and "RUNTIME_INTEGRITY_REVIEW.md" not in docs_map_text:
        issues.append(
            ValidationIssue(
                relative_location(docs_map_path, repo_root),
                "docs/README.md must route mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
            )
        )

    landing_text = read_text_or_issue(landing_path, issues, root=repo_root)
    if landing_text:
        for token in RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS:
            if token not in landing_text:
                issues.append(
                    ValidationIssue(
                        relative_location(landing_path, repo_root),
                        f"Agon Wave X landing note must mention '{token}'",
                    )
                )

    schema = load_json_payload(schema_path, issues)
    if schema is None:
        return issues
    schema_location = relative_location(schema_path, repo_root)
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    if schema.get("title") != "aoa-evals runtime integrity review":
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema title must be 'aoa-evals runtime integrity review'",
            )
        )
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must keep top-level additionalProperties set to false",
            )
        )
    required_fields = schema.get("required")
    expected_required_fields = {
        "schema_version",
        "owner_repo",
        "surface_kind",
        "status",
        "budget_ref",
        "evidence_refs",
        "replay_requirements",
        "human_review_needed",
        "forbidden_claims",
        "notes",
    }
    if not isinstance(required_fields, list) or set(required_fields) != expected_required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must require the full owner-local contract field set",
            )
        )
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must define object properties",
            )
        )
    else:
        const_fields = {
            "schema_version": "runtime_integrity_review_v1",
            "owner_repo": "aoa-evals",
            "surface_kind": "runtime_integrity_review",
            "status": "candidate_only",
            "budget_ref": RUNTIME_INTEGRITY_REVIEW_BUDGET_REF,
            "human_review_needed": True,
        }
        for field_name, expected_value in const_fields.items():
            field_schema = properties.get(field_name)
            if not isinstance(field_schema, dict) or field_schema.get("const") != expected_value:
                issues.append(
                    ValidationIssue(
                        schema_location,
                        f"runtime integrity review schema must keep '{field_name}' bound to its owner-local constant",
                    )
                )

        evidence_schema = properties.get("evidence_refs")
        if (
            not isinstance(evidence_schema, dict)
            or evidence_schema.get("type") != "array"
            or evidence_schema.get("uniqueItems") is not True
            or evidence_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
            or evidence_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep evidence_refs as an exact-count unique repo-ref array",
                )
            )
        else:
            evidence_items = evidence_schema.get("items")
            if (
                not isinstance(evidence_items, dict)
                or evidence_items.get("type") != "string"
                or evidence_items.get("pattern") != r"^repo:[^\s]+/.+$"
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep evidence_refs items constrained to repo-qualified refs",
                    )
                )

        replay_schema = properties.get("replay_requirements")
        if (
            not isinstance(replay_schema, dict)
            or replay_schema.get("type") != "object"
            or replay_schema.get("additionalProperties") is not False
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep replay_requirements as a closed object",
                )
            )
        else:
            replay_required = replay_schema.get("required")
            if not isinstance(replay_required, list) or set(replay_required) != set(
                RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must require the full replay_requirements key set",
                    )
                )
            replay_properties = replay_schema.get("properties")
            if not isinstance(replay_properties, dict):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must define replay_requirements properties",
                    )
                )
            else:
                for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS:
                    field_schema = replay_properties.get(field_name)
                    if not isinstance(field_schema, dict) or field_schema.get("const") is not True:
                        issues.append(
                            ValidationIssue(
                                schema_location,
                                f"runtime integrity review schema must keep replay_requirements.{field_name} bound to true",
                            )
                        )

        forbidden_schema = properties.get("forbidden_claims")
        if (
            not isinstance(forbidden_schema, dict)
            or forbidden_schema.get("type") != "array"
            or forbidden_schema.get("uniqueItems") is not True
            or forbidden_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
            or forbidden_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep forbidden_claims as an exact-count unique array",
                )
            )
        else:
            forbidden_items = forbidden_schema.get("items")
            forbidden_enum = forbidden_items.get("enum") if isinstance(forbidden_items, dict) else None
            if not isinstance(forbidden_enum, list) or set(forbidden_enum) != set(
                RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep forbidden_claims bound to the no-authority guard set",
                    )
                )

        notes_schema = properties.get("notes")
        if (
            not isinstance(notes_schema, dict)
            or notes_schema.get("type") != "string"
            or notes_schema.get("minLength") != 1
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep notes as a non-empty string",
                )
            )
    schema_validator = Draft202012Validator(schema)

    payload = load_json_payload(example_path, issues)
    if payload is None:
        return issues
    location = relative_location(example_path, repo_root)
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "runtime integrity review example must be an object"))
        return issues

    validate_against_schema(
        payload,
        RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME,
        location,
        issues,
        validator=schema_validator,
    )

    if payload.get("schema_version") != "runtime_integrity_review_v1":
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example schema_version must be 'runtime_integrity_review_v1'",
            )
        )
    if payload.get("owner_repo") != "aoa-evals":
        issues.append(ValidationIssue(location, "owner_repo must remain aoa-evals"))
    if payload.get("surface_kind") != "runtime_integrity_review":
        issues.append(ValidationIssue(location, "surface_kind must remain runtime_integrity_review"))
    if payload.get("status") != "candidate_only":
        issues.append(ValidationIssue(location, "status must remain candidate_only"))

    if payload.get("budget_ref") != RUNTIME_INTEGRITY_REVIEW_BUDGET_REF:
        issues.append(
            ValidationIssue(
                location,
                "budget_ref must stay bound to the Experience continuity-context owner split surface",
            )
        )
    else:
        parse_named_surface_ref(
            payload.get("budget_ref"),
            prefix_name="Agents-of-Abyss",
            repo_root=AGENTS_OF_ABYSS_ROOT,
            location=f"{location}.budget_ref",
            issues=issues,
        )

    evidence_refs = payload.get("evidence_refs")
    resolved_evidence_refs: set[str] = set()
    if not isinstance(evidence_refs, list):
        issues.append(ValidationIssue(f"{location}.evidence_refs", "evidence_refs must be a list"))
    else:
        for index, ref in enumerate(evidence_refs):
            resolution = parse_repo_ref(
                ref,
                location=f"{location}.evidence_refs[{index}]",
                issues=issues,
            )
            if resolution is None:
                continue
            repo_name, target_path, anchor = resolution
            normalized_ref = f"repo:{repo_name}/{target_path.relative_to(REPO_REF_ROOTS[repo_name]).as_posix()}"
            if anchor:
                normalized_ref = f"{normalized_ref}#{anchor}"
            resolved_evidence_refs.add(normalized_ref)
        if resolved_evidence_refs and resolved_evidence_refs != set(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS):
            issues.append(
                ValidationIssue(
                    location,
                    "evidence_refs must resolve to the bounded W10 runtime integrity review surfaces",
                )
            )

    expected_replay_requirements = {field_name: True for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS}
    if payload.get("replay_requirements") != expected_replay_requirements:
        issues.append(
            ValidationIssue(
                location,
                "replay_requirements must keep selected-evidence, owner-local replay, fail-closed, and review-required posture",
            )
        )

    if payload.get("human_review_needed") is not True:
        issues.append(ValidationIssue(location, "human_review_needed must remain true"))

    forbidden_claims = payload.get("forbidden_claims")
    if not isinstance(forbidden_claims, list):
        issues.append(
            ValidationIssue(
                f"{location}.forbidden_claims",
                "forbidden_claims must be a list",
            )
        )
    elif set(forbidden_claims) != set(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS):
        issues.append(
            ValidationIssue(
                location,
                "forbidden_claims must exactly preserve the bounded no-authority guard",
            )
        )

    notes = payload.get("notes")
    if not isinstance(notes, str) or "Candidate only." not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep candidate-only posture explicit",
            )
        )
    elif "activation pressure to Experience or runtime-owner gates" not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep activation routing explicit",
            )
        )

    return issues


def expected_contract_test_refs(record: EvalBundleRecord) -> set[str]:
    refs: set[str] = set()
    for item in record.manifest.get("evidence", []):
        if not isinstance(item, dict):
            continue
        if item.get("kind") not in {"integrity_check", "support_note"}:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue
        refs.add(
            f"repo:aoa-evals/{record.bundle_dir.relative_to(REPO_ROOT).as_posix()}/{raw_path}"
        )
    return refs


def validate_trace_eval_bridge_surfaces(
    repo_root: Path,
    records: list[EvalBundleRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    schema_path = repo_root / ARTIFACT_VERDICT_HOOK_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)
    schema = load_json_payload(schema_path, issues)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    playbooks_by_id: dict[str, dict[str, Any]] | None = None
    if AOA_PLAYBOOKS_ROOT.exists():
        playbook_registry_path = AOA_PLAYBOOKS_ROOT / "generated" / "playbook_registry.min.json"
        playbook_registry_location = display_location(playbook_registry_path)
        playbook_registry = load_json_payload(playbook_registry_path, issues)
        playbooks_by_id = load_mapping_entries(
            playbook_registry,
            array_key="playbooks",
            key_name="id",
            location=playbook_registry_location,
            issues=issues,
        )

    eval_catalog_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME
    eval_catalog_location = relative_location(eval_catalog_path, repo_root)
    eval_catalog = load_json_payload(eval_catalog_path, issues)
    evals_by_name = load_mapping_entries(
        eval_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_location,
        issues=issues,
    )

    records_by_name = {record.name: record for record in records}

    for playbook_id, example_name in ARTIFACT_VERDICT_HOOK_EXAMPLES.items():
        example_path = repo_root / example_name
        location = relative_location(example_path, repo_root)
        payload = load_json_payload(example_path, issues)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            issues.append(ValidationIssue(location, "example payload must be an object"))
            continue

        validate_against_schema(
            payload,
            ARTIFACT_VERDICT_HOOK_SCHEMA_NAME,
            location,
            issues,
            validator=schema_validator,
        )

        if payload.get("playbook_id") != playbook_id:
            issues.append(
                ValidationIssue(location, f"playbook_id must be '{playbook_id}'")
            )

        expected_hook = TRACE_EVAL_HOOK_EXPECTATIONS[playbook_id]
        if payload.get("eval_anchor") != expected_hook["eval_anchor"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval_anchor must be '{expected_hook['eval_anchor']}' for {playbook_id}",
                )
            )

        eval_anchor = payload.get("eval_anchor")
        if not isinstance(eval_anchor, str):
            continue
        catalog_entry = evals_by_name.get(eval_anchor)
        if catalog_entry is None:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval_anchor '{eval_anchor}' does not resolve in generated/eval_catalog.min.json",
                )
            )
            continue

        playbook_entry = playbooks_by_id.get(playbook_id) if playbooks_by_id is not None else None
        if playbooks_by_id is not None:
            if playbook_entry is None:
                issues.append(
                    ValidationIssue(location, f"playbook_id '{playbook_id}' does not resolve in aoa-playbooks")
                )
                continue

            playbook_eval_anchors = playbook_entry.get("eval_anchors")
            if not isinstance(playbook_eval_anchors, list) or eval_anchor not in playbook_eval_anchors:
                issues.append(
                    ValidationIssue(
                        location,
                        f"eval_anchor '{eval_anchor}' is not present in aoa-playbooks eval_anchors for {playbook_id}",
                    )
                )

            expected_artifacts = playbook_entry.get("expected_artifacts")
            if payload.get("artifact_inputs") != expected_artifacts:
                issues.append(
                    ValidationIssue(
                        location,
                        "artifact_inputs must exactly match aoa-playbooks expected_artifacts",
                    )
                )
            if not isinstance(expected_artifacts, list) or payload.get("verification_surface") not in expected_artifacts:
                issues.append(
                    ValidationIssue(
                        location,
                        "verification_surface must resolve inside the playbook artifact input set",
                    )
                )

        if payload.get("artifact_contract_refs") != expected_hook["artifact_contract_refs"]:
            issues.append(
                ValidationIssue(
                    location,
                    "artifact_contract_refs do not match the bounded cross-repo contract refs for this hook",
                )
            )

        if payload.get("trace_surfaces") != expected_hook["trace_surfaces"]:
            issues.append(
                ValidationIssue(
                    location,
                    "trace_surfaces do not match the bounded sidecar posture for this hook",
                )
            )

        if payload.get("verification_surface") != expected_hook["verification_surface"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"verification_surface must be '{expected_hook['verification_surface']}'",
                )
            )

        expected_bundle_ref = f"repo:aoa-evals/{catalog_entry.get('eval_path')}"
        if payload.get("verdict_bundle_ref") != expected_bundle_ref:
            issues.append(
                ValidationIssue(
                    location,
                    f"verdict_bundle_ref must equal '{expected_bundle_ref}'",
                )
            )

        verdict_bundle_resolution = parse_repo_ref(
            payload.get("verdict_bundle_ref"),
            location=f"{location}.verdict_bundle_ref",
            issues=issues,
        )
        if verdict_bundle_resolution is not None:
            _repo_name, verdict_bundle_path, _anchor = verdict_bundle_resolution
            expected_bundle_path = repo_root / str(catalog_entry.get("eval_path"))
            if verdict_bundle_path != expected_bundle_path:
                issues.append(
                    ValidationIssue(
                        location,
                        "verdict_bundle_ref must resolve to the selected eval anchor bundle path",
                    )
                )

        record = records_by_name.get(eval_anchor)
        if record is None:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval anchor '{eval_anchor}' does not resolve to a local bundle record",
                )
            )
            continue

        expected_report_expectation = {
            "report_format": record.manifest.get("report_format"),
            "verdict_shape": record.manifest.get("verdict_shape"),
            "review_required": record.manifest.get("review_required"),
        }
        if payload.get("report_expectation") != expected_report_expectation:
            issues.append(
                ValidationIssue(
                    location,
                    "report_expectation must exactly match the selected eval bundle manifest",
                )
            )

        resolved_contract_test_refs: set[str] = set()
        contract_test_refs = payload.get("contract_test_refs")
        if not isinstance(contract_test_refs, list):
            issues.append(
                ValidationIssue(f"{location}.contract_test_refs", "contract_test_refs must be a list")
            )
        else:
            for index, ref in enumerate(contract_test_refs):
                resolution = parse_repo_ref(
                    ref,
                    location=f"{location}.contract_test_refs[{index}]",
                    issues=issues,
                )
                if resolution is None:
                    continue
                repo_name, target_path, _anchor = resolution
                resolved_contract_test_refs.add(
                    f"repo:{repo_name}/{target_path.relative_to(REPO_REF_ROOTS[repo_name]).as_posix()}"
                )
        if resolved_contract_test_refs and resolved_contract_test_refs != expected_contract_test_refs(record):
            issues.append(
                ValidationIssue(
                    location,
                    "contract_test_refs must resolve to the selected bundle's integrity check and support note",
                )
            )

        for field_name in ("artifact_contract_refs", "trace_surfaces"):
            refs = payload.get(field_name)
            if not isinstance(refs, list):
                issues.append(
                    ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a list")
                )
                continue
            for index, ref in enumerate(refs):
                parse_repo_ref(
                    ref,
                    location=f"{location}.{field_name}[{index}]",
                    issues=issues,
                )

    return issues


def validate_runtime_evidence_selection_surfaces(
    repo_root: Path,
    records: list[EvalBundleRecord],
    *,
    target_eval_names: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    selected_examples: list[tuple[Path, dict[str, Any]]] = []
    for example_name, expectations in RUNTIME_EVIDENCE_SELECTION_EXAMPLES.items():
        target_eval = expectations.get("target_eval")
        example_path = repo_root / RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR / example_name
        if target_eval_names is None:
            selected_examples.append((example_path, expectations))
            continue
        if target_eval in target_eval_names:
            selected_examples.append((example_path, expectations))

    if not selected_examples:
        return issues

    schema_path = repo_root / RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)
    schema = load_json_payload(schema_path, issues)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    record_names = {record.name for record in records}

    for example_path, expectations in selected_examples:
        target_eval = expectations.get("target_eval")
        allowed_ref_roots = tuple(expectations.get("allowed_ref_roots", ["Logs"]))
        location = relative_location(example_path, repo_root)
        payload = load_json_payload(example_path, issues)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            issues.append(ValidationIssue(location, "example payload must be an object"))
            continue

        validate_against_schema(
            payload,
            RUNTIME_EVIDENCE_SELECTION_SCHEMA_NAME,
            location,
            issues,
            validator=schema_validator,
        )

        expected_schema_ref = expectations["source_schema_ref"]
        if payload.get("source_schema_ref") != expected_schema_ref:
            issues.append(
                ValidationIssue(
                    location,
                    f"source_schema_ref must equal '{expected_schema_ref}'",
                )
            )

        schema_resolution = parse_repo_ref(
            payload.get("source_schema_ref"),
            location=f"{location}.source_schema_ref",
            issues=issues,
        )
        if schema_resolution is not None:
            repo_name, target_path, _anchor = schema_resolution
            if repo_name != "abyss-stack":
                issues.append(
                    ValidationIssue(
                        location,
                        "source_schema_ref must resolve inside abyss-stack tracked schema space",
                    )
                )
            expected_schema_path = ABYSS_STACK_ROOT / expected_schema_ref[len("repo:abyss-stack/") :]
            if target_path != expected_schema_path:
                issues.append(
                    ValidationIssue(
                        location,
                        "source_schema_ref must resolve to the expected abyss-stack schema",
                    )
                )

        expected_candidate_eval_refs = expectations["candidate_eval_refs"]
        if payload.get("candidate_eval_refs") != expected_candidate_eval_refs:
            issues.append(
                ValidationIssue(
                    location,
                    f"candidate_eval_refs must equal {expected_candidate_eval_refs!r}",
                )
            )
        elif target_eval is not None and target_eval not in record_names:
            issues.append(
                ValidationIssue(
                    location,
                    f"candidate eval '{target_eval}' does not resolve to a local bundle record",
                )
            )

        for field_name in ("source_manifests", "excluded_artifacts"):
            refs = payload.get(field_name, [])
            if refs is None:
                continue
            if not isinstance(refs, list):
                issues.append(ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a list"))
                continue
            for index, ref in enumerate(refs):
                validate_abyss_stack_ref(
                    ref,
                    allowed_roots=allowed_ref_roots,
                    location=f"{location}.{field_name}[{index}]",
                    issues=issues,
                )

        selected_evidence = payload.get("selected_evidence")
        if not isinstance(selected_evidence, list):
            issues.append(
                ValidationIssue(f"{location}.selected_evidence", "selected_evidence must be a list")
            )
            continue
        for index, item in enumerate(selected_evidence):
            item_location = f"{location}.selected_evidence[{index}]"
            if not isinstance(item, dict):
                issues.append(ValidationIssue(item_location, "selected evidence entry must be an object"))
                continue
            validate_abyss_stack_ref(
                item.get("artifact_ref"),
                allowed_roots=allowed_ref_roots,
                location=f"{item_location}.artifact_ref",
                issues=issues,
            )

    return issues


def load_runtime_candidate_template_index_builder(repo_root: Path):
    module_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_candidate_template_index",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load runtime candidate template index generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_runtime_candidate_template_index(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
    generated_location = relative_location(generated_path, repo_root)
    schema_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)

    schema = load_json_payload(schema_path, issues)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    try:
        builder = load_runtime_candidate_template_index_builder(repo_root)
        expected = builder.build_runtime_candidate_template_index_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated template index must be an object"))
        return issues

    validate_against_schema(
        payload,
        RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_NAME,
        generated_location,
        issues,
        validator=schema_validator,
    )

    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated runtime candidate template index is out of date or mismatched",
            )
        )

    templates = payload.get("templates")
    if not isinstance(templates, list):
        issues.append(ValidationIssue(generated_location, "templates must be a list"))
        return issues

    expected_refs = {
        relative_location(path, repo_root)
        for path in sorted((repo_root / RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR).glob("runtime_evidence_selection.*.example.json"))
    }
    for examples_dir in ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS:
        expected_refs.update(
            relative_location(path, repo_root)
            for path in sorted((repo_root / examples_dir).glob("artifact_to_verdict_hook.*.example.json"))
        )
    indexed_refs = {
        entry.get("source_example_ref")
        for entry in templates
        if isinstance(entry, dict) and isinstance(entry.get("source_example_ref"), str)
    }
    if indexed_refs != expected_refs:
        missing = sorted(expected_refs - indexed_refs)
        extra = sorted(indexed_refs - expected_refs)
        if missing:
            issues.append(
                ValidationIssue(generated_location, "missing example refs in template index: " + ", ".join(missing))
            )
        if extra:
            issues.append(
                ValidationIssue(generated_location, "unexpected example refs in template index: " + ", ".join(extra))
            )

    eval_catalog_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME
    eval_catalog_location = relative_location(eval_catalog_path, repo_root)
    eval_catalog = load_json_payload(eval_catalog_path, issues)
    if not isinstance(eval_catalog, dict):
        return issues
    evals_by_name = load_mapping_entries(
        eval_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_location,
        issues=issues,
    )

    for index, entry in enumerate(templates):
        location = f"{generated_location}.templates[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "template entry must be an object"))
            continue

        required_runtime_artifacts = entry.get("required_runtime_artifacts")
        if isinstance(required_runtime_artifacts, list):
            normalized_artifacts = [
                artifact
                for artifact in required_runtime_artifacts
                if isinstance(artifact, str) and bool(NORMALIZED_RUNTIME_ARTIFACT_RE.fullmatch(artifact))
            ]
            if len(normalized_artifacts) != len(required_runtime_artifacts):
                issues.append(
                    ValidationIssue(
                        location,
                        "required_runtime_artifacts must stay normalized to lowercase runtime artifact names",
                    )
                )
            if len(required_runtime_artifacts) != len(set(required_runtime_artifacts)):
                issues.append(
                    ValidationIssue(
                        location,
                        "required_runtime_artifacts must not duplicate runtime artifact names",
                    )
                )

        source_example_ref = entry.get("source_example_ref")
        if not isinstance(source_example_ref, str):
            continue
        example_path = repo_root / source_example_ref
        example_payload = load_json_payload(example_path, issues)
        if example_payload is None or not isinstance(example_payload, dict):
            continue

        template_kind = entry.get("template_kind")
        if template_kind == "runtime_evidence_selection":
            if entry.get("template_name") != example_payload.get("selection_id"):
                issues.append(ValidationIssue(location, "template_name must match selection_id"))
            target_eval = example_payload.get("target_eval")
            if entry.get("eval_anchor") != target_eval:
                issues.append(ValidationIssue(location, "eval_anchor must match target_eval"))
            expected_bundle_ref = None
            if isinstance(target_eval, str):
                catalog_entry = evals_by_name.get(target_eval)
                if catalog_entry is None:
                    issues.append(
                        ValidationIssue(location, f"eval_anchor '{target_eval}' does not resolve in eval catalog")
                    )
                else:
                    expected_bundle_ref = f"repo:aoa-evals/{catalog_entry.get('eval_path')}"
            if entry.get("verdict_bundle_ref") != expected_bundle_ref:
                issues.append(ValidationIssue(location, "verdict_bundle_ref must match the resolved eval bundle or stay null"))
            selected_evidence = example_payload.get("selected_evidence")
            expected_artifacts = []
            if isinstance(selected_evidence, list):
                expected_artifacts = []
                for item in selected_evidence:
                    if not isinstance(item, dict):
                        continue
                    evidence_role = item.get("evidence_role")
                    if isinstance(evidence_role, str) and evidence_role not in expected_artifacts:
                        expected_artifacts.append(evidence_role)
            if entry.get("required_runtime_artifacts") != expected_artifacts:
                issues.append(ValidationIssue(location, "required_runtime_artifacts must match selected evidence roles"))
            review_posture = example_payload.get("review_posture")
            expected_review_required = bool(
                isinstance(review_posture, dict) and review_posture.get("human_review_required") is True
            )
            if entry.get("review_required") is not expected_review_required:
                issues.append(ValidationIssue(location, "review_required must match review_posture.human_review_required"))
        elif template_kind == "artifact_to_verdict_hook":
            if entry.get("template_name") != example_payload.get("hook_id"):
                issues.append(ValidationIssue(location, "template_name must match hook_id"))
            if entry.get("playbook_id") != example_payload.get("playbook_id"):
                issues.append(ValidationIssue(location, "playbook_id must match the source hook example"))
            if entry.get("eval_anchor") != example_payload.get("eval_anchor"):
                issues.append(ValidationIssue(location, "eval_anchor must match the source hook example"))
            if entry.get("verdict_bundle_ref") != example_payload.get("verdict_bundle_ref"):
                issues.append(ValidationIssue(location, "verdict_bundle_ref must match the source hook example"))
            expected_artifacts = example_payload.get("artifact_inputs")
            if entry.get("required_runtime_artifacts") != expected_artifacts:
                issues.append(ValidationIssue(location, "required_runtime_artifacts must match artifact_inputs"))
            report_expectation = example_payload.get("report_expectation")
            expected_review_required = bool(
                isinstance(report_expectation, dict) and report_expectation.get("review_required") is True
            )
            if entry.get("review_required") is not expected_review_required:
                issues.append(ValidationIssue(location, "review_required must match report_expectation.review_required"))

    return issues


def load_runtime_candidate_intake_builder(repo_root: Path):
    module_path = repo_root / RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_candidate_intake",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load runtime candidate intake generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_phase_alpha_eval_matrix_builder(repo_root: Path):
    module_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_phase_alpha_eval_matrix",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load phase alpha eval matrix generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_eval_report_index_builder(repo_root: Path):
    module_path = repo_root / "scripts" / "generate_eval_report_index.py"
    spec = importlib.util.spec_from_file_location(
        "generate_eval_report_index",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load eval report index generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_runtime_candidate_intake(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / RUNTIME_CANDIDATE_INTAKE_NAME
    generated_location = relative_location(generated_path, repo_root)

    try:
        builder = load_runtime_candidate_intake_builder(repo_root)
        expected = builder.build_runtime_candidate_intake_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated runtime candidate intake must be an object"))
        return issues
    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated runtime candidate intake is out of date or mismatched",
            )
        )
    if payload.get("schema_version") != 1:
        issues.append(ValidationIssue(generated_location, "schema_version must equal 1"))
    if payload.get("layer") != "aoa-evals":
        issues.append(ValidationIssue(generated_location, "layer must equal 'aoa-evals'"))
    expected_source_of_truth = {
        "runtime_candidate_template_index": "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "eval_review_guide": "docs/EVAL_REVIEW_GUIDE.md",
        "trace_eval_bridge": "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "runtime_bench_promotion_guide": "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    }
    if payload.get("source_of_truth") != expected_source_of_truth:
        issues.append(ValidationIssue(generated_location, "source_of_truth must stay stable"))

    templates = payload.get("templates")
    if not isinstance(templates, list):
        issues.append(ValidationIssue(generated_location, "templates must be a list"))
        return issues

    template_index_payload = load_json_payload(repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME, issues)
    if not isinstance(template_index_payload, dict):
        return issues
    templates_by_key = {
        (entry.get("template_kind"), entry.get("template_name")): entry
        for entry in template_index_payload.get("templates", [])
        if isinstance(entry, dict)
    }
    intake_keys = [
        (entry.get("template_kind"), entry.get("template_name"))
        for entry in templates
        if isinstance(entry, dict)
    ]
    if intake_keys != sorted(intake_keys):
        issues.append(ValidationIssue(generated_location, "templates must stay ordered by template_kind and template_name"))
    if len(intake_keys) != len(set(intake_keys)):
        issues.append(ValidationIssue(generated_location, "templates must not duplicate template entries"))
    if set(intake_keys) != set(templates_by_key):
        missing = sorted(set(templates_by_key) - set(intake_keys))
        extra = sorted(set(intake_keys) - set(templates_by_key))
        if missing:
            issues.append(
                ValidationIssue(
                    generated_location,
                    "missing template entries in runtime candidate intake: "
                    + ", ".join(f"{kind}:{name}" for kind, name in missing),
                )
            )
        if extra:
            issues.append(
                ValidationIssue(
                    generated_location,
                    "unexpected template entries in runtime candidate intake: "
                    + ", ".join(f"{kind}:{name}" for kind, name in extra),
                )
            )

    review_guide_by_kind = {
        "artifact_to_verdict_hook": "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "runtime_evidence_selection": "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    }

    for index, entry in enumerate(templates):
        location = f"{generated_location}.templates[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "template entry must be an object"))
            continue
        key = (entry.get("template_kind"), entry.get("template_name"))
        source_entry = templates_by_key.get(key)
        if source_entry is None:
            continue

        for field_name in (
            "playbook_id",
            "eval_anchor",
            "verdict_bundle_ref",
            "required_runtime_artifacts",
            "review_required",
        ):
            if entry.get(field_name) != source_entry.get(field_name):
                issues.append(ValidationIssue(location, f"{field_name} must match mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"))

        template_kind = entry.get("template_kind")
        expected_review_guide = review_guide_by_kind.get(template_kind, "docs/EVAL_REVIEW_GUIDE.md")
        if entry.get("review_guide_ref") != expected_review_guide:
            issues.append(ValidationIssue(location, "review_guide_ref must stay aligned with the template kind"))

        owner_review_refs = entry.get("owner_review_refs")
        if not isinstance(owner_review_refs, list) or not owner_review_refs:
            issues.append(ValidationIssue(location, "owner_review_refs must stay a non-empty list"))
        else:
            expected_owner_review_refs = [
                expected_review_guide,
                "docs/EVAL_REVIEW_GUIDE.md",
                source_entry.get("source_example_ref"),
            ]
            expected_owner_review_refs = [
                item for item in expected_owner_review_refs if isinstance(item, str) and item
            ]
            deduped: list[str] = []
            for item in expected_owner_review_refs:
                if item not in deduped:
                    deduped.append(item)
            if owner_review_refs != deduped:
                issues.append(ValidationIssue(location, "owner_review_refs must stay aligned with the source example and review guides"))
            for ref in owner_review_refs:
                if not isinstance(ref, str):
                    continue
                if not (repo_root / ref).exists():
                    issues.append(ValidationIssue(location, f"owner_review_ref '{ref}' must point to a live local file"))

        if entry.get("candidate_acceptance_posture") != "candidate_until_eval_review":
            issues.append(ValidationIssue(location, "candidate_acceptance_posture must stay 'candidate_until_eval_review'"))

    return issues


def validate_eval_report_index(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / EVAL_REPORT_INDEX_NAME
    generated_location = relative_location(generated_path, repo_root)

    try:
        builder = load_eval_report_index_builder(repo_root)
        expected = builder.build_eval_report_index_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated eval report index must be an object"))
        return issues
    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated eval report index is out of date or mismatched",
            )
        )
    if payload.get("schema_version") != 1:
        issues.append(ValidationIssue(generated_location, "schema_version must equal 1"))
    if payload.get("layer") != "aoa-evals":
        issues.append(ValidationIssue(generated_location, "layer must equal 'aoa-evals'"))
    expected_source_of_truth = {
        "bundle_reports": "evals/**/reports/*.report.json",
        "bundle_report_schema": "evals/**/reports/summary.schema.json",
        "bundle_manifest": "evals/**/eval.yaml",
        "eval_review_guide": "docs/EVAL_REVIEW_GUIDE.md",
    }
    if payload.get("source_of_truth") != expected_source_of_truth:
        issues.append(ValidationIssue(generated_location, "source_of_truth must stay stable"))
    boundary = payload.get("interpretation_boundary")
    if not isinstance(boundary, str) or not all(
        token in boundary
        for token in ("not a receipt", "promotion signal", "runtime acceptance", "verdict authority")
    ):
        issues.append(
            ValidationIssue(
                generated_location,
                "interpretation_boundary must keep receipt, promotion, runtime, and verdict authority limits explicit",
            )
        )

    reports = payload.get("reports")
    if not isinstance(reports, list):
        issues.append(ValidationIssue(generated_location, "reports must be a list"))
        return issues

    keys: list[tuple[str, str]] = []
    source_paths: list[str] = []
    for index, entry in enumerate(reports):
        location = f"{generated_location}.reports[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "report entry must be an object"))
            continue

        eval_name = entry.get("eval_name")
        report_id = entry.get("report_id")
        source_report_path = entry.get("source_report_path")
        if not isinstance(eval_name, str) or not eval_name:
            issues.append(ValidationIssue(location, "eval_name must be a non-empty string"))
            continue
        if not isinstance(report_id, str) or not report_id:
            issues.append(ValidationIssue(location, "report_id must be a non-empty string"))
            continue
        if not isinstance(source_report_path, str) or not source_report_path.endswith(".report.json"):
            issues.append(ValidationIssue(location, "source_report_path must point to a bundle-local .report.json"))
            continue

        keys.append((eval_name, report_id))
        source_paths.append(source_report_path)
        report_path = repo_root / source_report_path
        if not report_path.is_file():
            issues.append(ValidationIssue(location, f"source_report_path does not exist: {source_report_path}"))
            continue

        report_payload = load_json_payload(report_path, issues)
        if not isinstance(report_payload, dict):
            continue
        for field_name in ("eval_name", "bundle_status", "verdict", "case_family", "claim_boundary"):
            if entry.get(field_name) != report_payload.get(field_name):
                issues.append(
                    ValidationIssue(location, f"{field_name} must match source_report_path")
                )
        limitations = report_payload.get("limitations")
        expected_limitations_count = len(limitations) if isinstance(limitations, list) else 0
        if entry.get("limitations_count") != expected_limitations_count:
            issues.append(ValidationIssue(location, "limitations_count must match source_report_path"))

        report_eval_dir = PurePosixPath(source_report_path).parents[1]
        if entry.get("source_bundle_ref") != f"{report_eval_dir.as_posix()}/EVAL.md":
            issues.append(ValidationIssue(location, "source_bundle_ref must point to the owning bundle EVAL.md"))
        if entry.get("manifest_ref") != f"{report_eval_dir.as_posix()}/eval.yaml":
            issues.append(ValidationIssue(location, "manifest_ref must point to the owning bundle eval.yaml"))
        if entry.get("report_schema_ref") != f"{report_eval_dir.as_posix()}/reports/summary.schema.json":
            issues.append(ValidationIssue(location, "report_schema_ref must point to the owning bundle report schema"))
        for ref_field in ("source_bundle_ref", "manifest_ref", "report_schema_ref"):
            ref_value = entry.get(ref_field)
            if isinstance(ref_value, str) and not (repo_root / ref_value).exists():
                issues.append(ValidationIssue(location, f"{ref_field} does not exist: {ref_value}"))

        if entry.get("report_posture") != "bounded_report_output":
            issues.append(ValidationIssue(location, "report_posture must stay 'bounded_report_output'"))
        authority_boundary = entry.get("authority_boundary")
        if not isinstance(authority_boundary, str) or "derived index only" not in authority_boundary:
            issues.append(ValidationIssue(location, "authority_boundary must keep derived-index posture explicit"))
        if entry.get("receipt_status") != "not_a_receipt":
            issues.append(ValidationIssue(location, "receipt_status must stay 'not_a_receipt'"))

    if keys != sorted(keys):
        issues.append(ValidationIssue(generated_location, "reports must stay ordered by eval_name and report_id"))
    if len(keys) != len(set(keys)):
        issues.append(ValidationIssue(generated_location, "reports must not duplicate eval_name/report_id entries"))
    if len(source_paths) != len(set(source_paths)):
        issues.append(ValidationIssue(generated_location, "reports must not duplicate source_report_path entries"))

    return issues


def markdown_heading_section(text: str, heading: str) -> str:
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


def markdown_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug_compact_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def validate_mechanic_part_role_heading(
    *,
    path_name: str,
    text: str,
    parent_name: str,
    part_name: str,
    role_name: str,
    issues: list[ValidationIssue],
) -> None:
    heading = markdown_h1(text)
    heading_compact = slug_compact_token(heading)
    missing: list[str] = []
    if slug_compact_token(parent_name) not in heading_compact:
        missing.append("parent mechanic")
    if slug_compact_token(part_name) not in heading_compact:
        missing.append("local role token")
    if role_name.lower() not in heading.lower():
        missing.append(role_name)
    if " / " not in heading:
        missing.append("Parent / Part heading shape")
    if missing:
        issues.append(
            ValidationIssue(
                path_name,
                "mechanic route H1 must name parent mechanic, local role token, and role; missing "
                + ", ".join(missing),
            )
        )


def markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if cells[0] == "Parent":
            continue
        if all(set(cell.replace(" ", "")) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    return rows


def mechanic_part_validation_block(readme_text: str) -> str:
    return markdown_heading_section(readme_text, "Validation")


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


SOURCE_SURFACE_CODE_REF_RE = re.compile(r"`([^`\n]+)`")
SOURCE_SURFACE_FILE_REF_RE = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9_.-]*$")


def mechanic_part_source_surface_refs(readme_text: str) -> list[str]:
    section = markdown_heading_section(readme_text, "Source Surfaces")
    refs: list[str] = []
    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(section):
        ref = match.group(1).strip()
        if not ref:
            continue
        if source_surface_ref_is_path_like(ref):
            refs.append(ref)
    return list(dict.fromkeys(refs))


def source_surface_ref_is_path_like(ref: str) -> bool:
    return (
        ref.startswith(("repo:", ".", "/"))
        or "/" in ref
        or "*" in ref
        or "?" in ref
        or "[" in ref
        or SOURCE_SURFACE_FILE_REF_RE.search(ref) is not None
    )


def source_surface_ref_resolution_issue(repo_root: Path, ref: str) -> str | None:
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


MECHANIC_PART_SLUG_PATTERN = r"[a-z0-9][a-z0-9_.-]+"


def mechanic_parts_index_declared_slugs(
    parts_index_text: str,
    parent_name: str,
) -> set[str]:
    declared: set[str] = set()

    full_path_pattern = re.compile(
        rf"mechanics/{re.escape(parent_name)}/parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)"
    )
    declared.update(full_path_pattern.findall(parts_index_text))

    relative_path_pattern = re.compile(
        rf"(?:^|[^A-Za-z0-9_./-])parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)",
        re.MULTILINE,
    )
    declared.update(relative_path_pattern.findall(parts_index_text))

    heading_pattern = re.compile(
        rf"^###\s+`?({MECHANIC_PART_SLUG_PATTERN})`?\s*$",
        re.MULTILINE,
    )
    declared.update(heading_pattern.findall(parts_index_text))

    lines = parts_index_text.splitlines()
    index = 0
    while index < len(lines) - 1:
        line = lines[index].strip()
        next_line = lines[index + 1].strip()
        if line.startswith("|") and next_line.startswith("|"):
            header_cells = [cell.strip().lower() for cell in line.strip("|").split("|")]
            separator_cells = [
                cell.strip().replace(" ", "")
                for cell in next_line.strip("|").split("|")
            ]
            is_separator = bool(separator_cells) and all(
                set(cell) <= {"-", ":"} and "-" in cell for cell in separator_cells
            )
            if header_cells and "part" in header_cells[0] and is_separator:
                row_index = index + 2
                while row_index < len(lines) and lines[row_index].strip().startswith("|"):
                    first_cell = lines[row_index].strip().strip("|").split("|")[0]
                    declared.update(
                        re.findall(rf"`({MECHANIC_PART_SLUG_PATTERN})`", first_cell)
                    )
                    row_index += 1
                index = row_index
                continue
        index += 1

    return declared


def validation_command_referenced_paths(command: str) -> tuple[list[str], str | None]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return [], f"validation command cannot be parsed: {exc}"

    if not parts:
        return [], None

    paths: list[str] = []
    if (
        len(parts) > 3
        and parts[1] == "-m"
        and parts[2] == "pytest"
    ):
        for token in parts[3:]:
            if token.startswith("-") or token in {"and", "|"}:
                continue
            if token.endswith(".py") or "/" in token:
                paths.append(token.split("::", 1)[0])
        return paths, None

    if len(parts) > 1:
        first_arg = parts[1]
        if first_arg.endswith(".py") or "/" in first_arg:
            paths.append(first_arg)
    return paths, None


def part_payload_directories(part_root: Path) -> list[Path]:
    return [
        child
        for child in sorted(part_root.iterdir(), key=lambda item: item.name)
        if child.is_dir() and child.name in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS
    ]


def validation_section_has_payload_coverage_anchor(
    part_relative: str,
    validation_section: str,
    commands: Sequence[str],
) -> bool:
    part_prefix = f"{part_relative.rstrip('/')}/"
    if any(part_prefix in command for command in commands):
        return True
    if any("scripts/validate_repo.py --eval " in command for command in commands):
        return True

    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(validation_section):
        ref = match.group(1).strip().rstrip("/")
        if ref == part_relative or ref.startswith(part_prefix):
            return True
    return False


PART_README_PATH_RE = re.compile(
    r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$"
)
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


def part_readme_path_name(path_name: str) -> bool:
    return PART_README_PATH_RE.match(path_name) is not None


def mechanic_parent_readme_path_name(path_name: str) -> bool:
    return MECHANIC_PARENT_README_PATH_RE.match(path_name) is not None


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""

    parent_name = match.group(1)
    agents_path = repo_root / "mechanics" / parent_name / "AGENTS.md"
    if not agents_path.is_file():
        return ""
    return agents_path.read_text(encoding="utf-8")


def part_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = PART_README_PATH_RE.match(readme_name)
    if match is None:
        return ""

    parent_name, part_name = match.groups()
    part_relative = f"mechanics/{parent_name}/parts/{part_name}"
    validation_name = f"{part_relative}/VALIDATION.md"
    chunks: list[str] = []

    validation_path = repo_root / validation_name
    if validation_path.is_file():
        chunks.append(validation_path.read_text(encoding="utf-8"))

    agents_path = repo_root / "mechanics" / parent_name / "parts" / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
        if child_section:
            chunks.append(child_section)

    return "\n\n".join(chunks)


def mechanic_part_validation_sources(
    repo_root: Path,
    parent_name: str,
    part_root: Path,
    readme_name: str,
    readme_text: str,
    issues: list[ValidationIssue],
) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []

    readme_section = mechanic_part_validation_block(readme_text)
    sources.append((readme_name, readme_section))

    part_relative = part_root.relative_to(repo_root).as_posix()
    validation_name = f"{part_relative}/VALIDATION.md"
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        validation_text = read_text_or_issue(validation_path, issues, root=repo_root)
        if validation_text:
            sources.append((validation_name, validation_text))
    else:
        issues.append(
            ValidationIssue(
                validation_name,
                "part validation route marker is missing",
            )
        )

    parts_agents_name = f"mechanics/{parent_name}/parts/AGENTS.md"
    parts_agents_path = repo_root / parts_agents_name
    if parts_agents_path.is_file():
        agents_text = read_text_or_issue(parts_agents_path, issues, root=repo_root)
        if agents_text:
            child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
            if child_section:
                sources.append((parts_agents_name, child_section))
            else:
                issues.append(
                    ValidationIssue(
                        parts_agents_name,
                        f"missing centralized child validation block for `{validation_name}`",
                    )
                )
    else:
        issues.append(
            ValidationIssue(
                parts_agents_name,
                "parent parts AGENTS validation lane is missing",
            )
        )

    return sources


def validate_mechanic_part_readme_contract_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}/parts",
                    "active mechanic parent must expose a parts/ directory",
                )
            )
            continue

        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )

        for path in sorted(parts_root.iterdir(), key=lambda item: item.name):
            relative = path.relative_to(repo_root).as_posix()
            if path.is_file():
                if path.name not in {"AGENTS.md", "README.md"}:
                    issues.append(
                        ValidationIssue(
                            relative,
                            "unexpected mechanics parts root file must be a route README or a part directory",
                        )
                    )
                continue
            if not path.is_dir():
                issues.append(
                    ValidationIssue(
                        relative,
                        "unexpected mechanics parts root entry must be a part directory",
                    )
                )
                continue

            readme_name = f"{relative}/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=readme_name,
                text=readme_text,
                parent_name=parent_name,
                part_name=path.name,
                role_name="Part",
                issues=issues,
            )
            validation_name = f"{relative}/VALIDATION.md"
            validation_path = repo_root / validation_name
            if validation_path.is_file():
                validation_text = read_text_or_issue(
                    validation_path,
                    issues,
                    root=repo_root,
                )
                validate_mechanic_part_role_heading(
                    path_name=validation_name,
                    text=validation_text,
                    parent_name=parent_name,
                    part_name=path.name,
                    role_name="Validation",
                    issues=issues,
                )
            part_route_text = "\n\n".join(
                (
                    readme_text,
                    part_validation_route_text(repo_root, readme_name),
                )
            )
            route_tokens = (
                readme_name,
                f"parts/{path.name}/README.md",
                f"`{path.name}`",
            )
            if parts_index_text and not any(token in parts_index_text for token in route_tokens):
                issues.append(
                    ValidationIssue(
                        parts_index_name,
                        f"parent PARTS.md must route concrete part `{readme_name}` by README path or exact part slug",
                    )
                )
            require_tokens(
                repo_root=repo_root,
                path_name=readme_name,
                tokens=MECHANIC_PART_README_REQUIRED_TOKENS,
                issues=issues,
            )
            for stale_lead_in in MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS:
                if readme_text and stale_lead_in in readme_text:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            "mechanic part README must introduce Stop-Lines as a local proof-operation boundary, not the old part-claim scaffold",
                        )
                    )
            source_refs = mechanic_part_source_surface_refs(readme_text)
            if readme_text and "## Source Surfaces" in readme_text and not source_refs:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part README Source Surfaces must name at least one path-like source ref",
                    )
                )
            for ref in source_refs:
                ref_issue = source_surface_ref_resolution_issue(repo_root, ref)
                if ref_issue is not None:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            f"{ref_issue}: `{ref}`",
                        )
                    )
            payload_dir_count = 0
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                child_relative = child.relative_to(repo_root).as_posix()
                if child.is_file():
                    if child.name not in {"AGENTS.md", "README.md", "VALIDATION.md"}:
                        issues.append(
                            ValidationIssue(
                                child_relative,
                                "unexpected part-root file must move under a payload subdirectory or be routed by the part contract",
                            )
                        )
                    continue
                if not child.is_dir():
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected part-root entry must be a payload subdirectory",
                        )
                    )
                    continue
                if child.name not in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS:
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected payload class directory under mechanic part",
                        )
                    )
                    continue
                payload_dir_count += 1
                if not any(child.iterdir()):
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "empty payload subdirectory under mechanic part",
                        )
                    )
                    continue
                if part_route_text:
                    payload_tokens = (
                        f"{child.name}/",
                        f"`{child.name}`",
                        child_relative,
                    )
                    if not any(token in part_route_text for token in payload_tokens):
                        issues.append(
                            ValidationIssue(
                                readme_name,
                                f"part README must route payload subdirectory `{child.name}/`",
                            )
                        )
            if payload_dir_count == 0 and readme_text:
                missing_thin_tokens = [
                    token
                    for token in MECHANIC_THIN_PART_REQUIRED_TOKENS
                    if token not in readme_text
                ]
                if missing_thin_tokens:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            "mechanic part with no payload subdirectories must "
                            "declare an eval-backed thin support route; missing "
                            + ", ".join(repr(token) for token in missing_thin_tokens),
                        )
                    )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        tokens=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    payload_decision_text = read_text_or_issue(
        repo_root / MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if payload_decision_text and markdown_python_commands(
        markdown_heading_section(payload_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
            "Mechanic Part Payload Inventory",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload subdirectory", "mechanic part"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("payload subdirectory", "unexpected payload class"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
            "Mechanic Part Source Surface Reference Guard",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Source Surfaces", "stale source surface ref"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "repo-relative path"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
            "Mechanic Part Source Surfaces Section Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("## Source Surfaces", "at least one path-like source ref"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "plural section"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_parts_index_sync_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            continue

        actual_parts = {
            path.name
            for path in parts_root.iterdir()
            if path.is_dir()
        }
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        if not parts_index_text:
            continue

        declared_parts = mechanic_parts_index_declared_slugs(
            parts_index_text,
            parent_name,
        )
        for part_name in sorted(actual_parts - declared_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md must declare actual part directory `{part_name}` as a local part route",
                )
            )
        for part_name in sorted(declared_parts - actual_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md declares stale local part route `{part_name}` with no matching actual part directory",
                )
            )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
        tokens=MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
            "Mechanic PARTS Index Synchronization",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("declared part route", "stale local part route"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("actual part directory", "cross-parent reference"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE = re.compile(
    r"(?:mechanics/[a-z0-9-]+/)?legacy/(?:README\.md|INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES = (".md", ".json", ".yaml", ".yml", ".py")
MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE = re.compile(
    r"legacy/(?:INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)


def validate_mechanic_legacy_single_bridge_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue

        for path in sorted(parent_root.rglob("*")):
            if not path.is_file() or path.suffix not in MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES:
                continue
            relative_parts = path.relative_to(parent_root).parts
            if "legacy" in relative_parts:
                continue
            text = read_text_or_issue(path, issues, root=repo_root)
            if text is None:
                continue
            if path.name == "PROVENANCE.md":
                for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                    issues.append(
                        ValidationIssue(
                            path.relative_to(repo_root).as_posix(),
                            f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                        )
                    )
                continue
            for match in MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        f"active mechanic surface must route legacy archive details through PROVENANCE.md, not direct `{match.group(0)}`",
                    )
                )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            "Mechanic Legacy Single Bridge",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("single controlled bridge", "active mechanic surfaces", "legacy archive"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("single controlled bridge", "active mechanic surfaces", "legacy archive"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("single controlled bridge", "active mechanic surfaces", "legacy archive"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_part_validation_command_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        parts_root = repo_root / "mechanics" / parent_name / "parts"
        if not parts_root.is_dir():
            continue

        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            if not part_root.is_dir():
                continue
            readme_name = part_root.relative_to(repo_root).as_posix() + "/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            if not readme_text:
                continue

            sources = mechanic_part_validation_sources(
                repo_root,
                parent_name,
                part_root,
                readme_name,
                readme_text,
                issues,
            )
            readme_validation_section = mechanic_part_validation_block(readme_text)
            readme_commands = markdown_python_commands(readme_validation_section)
            if readme_commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part README validation section must route executable commands to VALIDATION.md or parent parts/AGENTS.md instead of carrying python command blocks",
                    )
                )

            command_locations: dict[str, str] = {}
            commands: list[str] = []
            for location, source_text in sources:
                for command in markdown_python_commands(source_text):
                    if command in command_locations:
                        continue
                    command_locations[command] = location
                    commands.append(command)

            if not commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must list at least one python command",
                    )
                )
                continue

            part_relative = part_root.relative_to(repo_root).as_posix()
            combined_validation_route = "\n\n".join(source_text for _, source_text in sources)
            if part_payload_directories(part_root) and not validation_section_has_payload_coverage_anchor(
                part_relative,
                combined_validation_route,
                commands,
            ):
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must include a payload coverage anchor, such as a part-local path or specific `python scripts/validate_repo.py --eval ...`; naked route-wide commands are not enough for parts with payload",
                    )
                )

            for command in commands:
                command_location = command_locations.get(command, readme_name)
                command_paths, parse_issue = validation_command_referenced_paths(command)
                if parse_issue:
                    issues.append(ValidationIssue(command_location, parse_issue))
                    continue
                for command_path in command_paths:
                    if any(token in command_path for token in ("*", "?", "[")):
                        continue
                    if command_path.startswith("/"):
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"validation command must use repo-relative path, not absolute path `{command_path}`",
                            )
                        )
                        continue
                    if not (repo_root / command_path).exists():
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"part validation command has stale validation path `{command_path}`",
                            )
                        )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        tokens=MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    validation_command_decision_text = read_text_or_issue(
        repo_root / MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if validation_command_decision_text and markdown_python_commands(
        markdown_heading_section(validation_command_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
        tokens=MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
            MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
            "Mechanic Part Validation Command Reachability",
            "Mechanic Part Validation Command Ownership",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload coverage anchor", "stale validation path"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("part validation route", "payload coverage anchor"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_parent_class_map(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    active_parents = set(ACTIVE_MECHANIC_PARENT_NAMES)
    aoa_parents = set(AOA_ALIGNED_MECHANIC_PARENT_NAMES)
    evals_native_parents = set(EVALS_NATIVE_MECHANIC_PARENT_NAMES)

    overlap = sorted(aoa_parents & evals_native_parents)
    if overlap:
        issues.append(
            ValidationIssue(
                "scripts/validate_repo.py",
                "mechanic parent class sets must be disjoint: " + ", ".join(overlap),
            )
        )

    missing = sorted(active_parents - (aoa_parents | evals_native_parents))
    extra = sorted((aoa_parents | evals_native_parents) - active_parents)
    if missing:
        issues.append(
            ValidationIssue(
                "scripts/validate_repo.py",
                "active mechanic parents missing from class sets: " + ", ".join(missing),
            )
        )
    if extra:
        issues.append(
            ValidationIssue(
                "scripts/validate_repo.py",
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

    aoa_section = markdown_heading_section(text, "AoA-aligned parents")
    evals_native_section = markdown_heading_section(text, "Evals-native parents")
    dimension_section = markdown_heading_section(
        text, "Active Parent Evidence Dimension Ledger"
    )
    route_refs_section = markdown_heading_section(
        text, MECHANIC_EVIDENCE_ROUTE_REFS_SECTION
    )
    wrong_parent_section = markdown_heading_section(text, "Former Wrong Parent Forms")
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
    for cells in markdown_table_rows(dimension_section):
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
    for cells in markdown_table_rows(route_refs_section):
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
                if source_surface_ref_is_path_like(match.group(1).strip())
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
                ref_issue = source_surface_ref_resolution_issue(repo_root, ref)
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

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
            "Mechanic Evidence Dimension Ledger",
            MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
            "Mechanic Evidence Route Refs",
        ),
        issues=issues,
    )
    require_tokens(
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
    require_tokens(
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
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
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

    recon_section = markdown_heading_section(
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
    for cells in markdown_table_rows(recon_section):
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

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
        tokens=MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
            "Mechanic Root-district Reconnaissance",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Root District Reconnaissance Ledger", "root-district"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=("Focused mechanic topology checks", MECHANIC_ROOT_DISTRICT_RECON_COMMAND),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Root District Reconnaissance Ledger", "mechanic-owned payload"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_root_authored_surface_classification(
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

    section = markdown_heading_section(
        text, ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION
    )
    if not section:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                f"mechanics evidence cluster map must contain section {ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION!r}",
            )
        )

    for token in ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS:
        if token not in section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
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
            issues.append(
                ValidationIssue(
                    district_name,
                    "classified root-authored district is missing",
                )
            )
            continue
        allowed = set(allowed_names)
        actual_names = {
            path.name
            for path in district.iterdir()
            if path.is_file()
        }
        for file_name in sorted(actual_names - allowed):
            issues.append(
                ValidationIssue(
                    f"{district_name}/{file_name}",
                    "unclassified root-authored surface must be routed, moved, or added to the residual classification ledger",
                )
            )
        for file_name in sorted(allowed - actual_names):
            issues.append(
                ValidationIssue(
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
    for cells in markdown_table_rows(section):
        if not cells or cells[0] == "Surface":
            continue
        surface_name = cells[0].strip("`")
        if surface_name not in expected_surfaces:
            continue
        if surface_name in ledger_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root-authored surface `{surface_name}` must appear only once in the residual classification ledger",
                )
            )
        ledger_rows[surface_name] = cells
        if len(cells) != len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS):
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
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
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"root-authored surface `{surface_name}` row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        if "mechanic-owned payload" not in row_text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root-authored surface `{surface_name}` row must state its mechanic-owned payload boundary",
                )
            )
        if "root-owned" not in row_text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root-authored surface `{surface_name}` row must state its root-owned role",
                )
            )

    for surface_name in sorted(expected_surfaces):
        if surface_name not in ledger_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root-authored surface `{surface_name}` must appear in the residual classification ledger",
                )
            )

    for surface_name in sorted(actual_surfaces - expected_surfaces):
        issues.append(
            ValidationIssue(
                surface_name,
                "unclassified root-authored surface must not remain in root districts",
            )
        )

    require_tokens(
        repo_root=repo_root,
        path_name=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        tokens=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
            "Root-authored Surface Classification",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION, "unclassified root-authored surface"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_legacy_raw_payload_accounting(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        legacy_root = repo_root / "mechanics" / parent_name / "legacy"
        raw_root = legacy_root / "raw"
        if not raw_root.is_dir():
            continue

        index_path = legacy_root / "INDEX.md"
        log_path = legacy_root / "DISTILLATION_LOG.md"
        if not index_path.is_file() or not log_path.is_file():
            continue

        accounting_text = (
            index_path.read_text(encoding="utf-8")
            + "\n"
            + log_path.read_text(encoding="utf-8")
        )
        index_text = index_path.read_text(encoding="utf-8")

        for path in sorted(raw_root.rglob("*")):
            if not path.is_file() or path.name == "README.md":
                continue
            legacy_relative = path.relative_to(legacy_root).as_posix()
            if legacy_relative not in accounting_text and path.name not in accounting_text:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must be referenced by the archive-local index or accounting log",
                    )
                )
                continue

            raw_index_lines = [
                line
                for line in index_text.splitlines()
                if legacy_relative in line or path.name in line
            ]
            if not raw_index_lines:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must have an archive-local INDEX.md row that maps it to a current active route",
                    )
                )
                continue

            active_part_route = f"mechanics/{parent_name}/parts/"
            package_wide_route = (
                f"mechanics/{parent_name}/DIRECTION.md",
                f"mechanics/{parent_name}/PARTS.md",
            )
            has_active_route = any(
                "/legacy/" not in line
                and (
                    active_part_route in line
                    or all(route in line for route in package_wide_route)
                )
                for line in raw_index_lines
            )
            if not has_active_route:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload INDEX.md row must map to a current active part route or package-wide DIRECTION/PARTS route, not only a raw-only archive route",
                    )
                )

    return issues


def validate_mechanic_provenance_entry_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS,
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text:
            for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                    )
                )

    return issues


def validate_mechanic_provenance_bridge_posture_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
            issues=issues,
        )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
            "Mechanic Provenance Bridge Posture",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "`PROVENANCE.md` is the active-to-archive bridge",
            "Use active surfaces first:",
            "legacy archive",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "`PROVENANCE.md` is the active-to-archive bridge",
            "Use active surfaces first:",
            "legacy archive",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=(
            "`PROVENANCE.md` is the active-to-archive bridge",
            "Use active surfaces first:",
            "legacy archive",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="DESIGN.md",
        tokens=(
            "single controlled bridge",
            "active-to-archive bridge",
            "legacy archive",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_parent_direction_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_DIRECTION_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_DIRECTION_REQUIRED_TOKENS,
            issues=issues,
        )

    for path_name in MECHANIC_PARENT_README_FILES:
        require_tokens(
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

    for parent_name, path_name in zip(
        ACTIVE_MECHANIC_PARENT_NAMES,
        MECHANIC_PARENT_AGENTS_FILES,
        strict=True,
    ):
        require_tokens(
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

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_DIRECTION_DECISION_NAME,
        tokens=MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARENT_DIRECTION_DECISION_NAME,
            "Mechanic Parent Direction Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Mechanic parent direction", "`DIRECTION.md`"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("DIRECTION.md", "current operating direction"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("DIRECTION.md", "current operating direction", "Entry Route"),
        issues=issues,
    )
    require_tokens(
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

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
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

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
        tokens=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
            "Mechanic Parent Guidance Boundary",
        ),
        issues=issues,
    )
    require_tokens(
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
    allowed_parents = set(ACTIVE_MECHANIC_PARENT_NAMES)
    issues.extend(validate_mechanic_parent_class_map(repo_root))
    issues.extend(validate_mechanic_legacy_raw_payload_accounting(repo_root))
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

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        if not (mechanics_root / parent_name).is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}",
                    "declared mechanic parent directory is missing",
                )
            )

    require_tokens(
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
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=tuple(f"`{parent_name}`" for parent_name in ACTIVE_MECHANIC_PARENT_NAMES),
        issues=issues,
    )
    require_tokens(
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
    for path_name in MECHANIC_LEGACY_SKELETON_FILES:
        if not (repo_root / path_name).is_file():
            issues.append(
                ValidationIssue(
                    path_name,
                    "active mechanic parent must expose PROVENANCE.md and archive-local legacy entry/accounting surfaces",
                )
            )
    for path_name in MECHANIC_LEGACY_README_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_README_REQUIRED_TOKENS,
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "top-level mechanics parents are validator allowlisted",
            "mechanics/EVIDENCE_CLUSTERS.md",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(MECHANIC_PARENT_ALLOWLIST_DECISION_NAME, "Mechanic Parent Allowlist"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_LEGACY_SKELETON_DECISION_NAME,
            "Mechanic Legacy Archive Boundary",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_CLASS_DECISION_NAME,
        tokens=MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARENT_CLASS_DECISION_NAME,
            "Mechanic Parent Class Contract",
        ),
        issues=issues,
    )

    return issues


def validate_active_legacy_parent_wording(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, forbidden_tokens in ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN.items():
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if not text:
            continue
        for token in forbidden_tokens:
            if token in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"active route wording must not use legacy parent form {token!r}",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
        tokens=ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
            "Active Legacy Parent Wording Boundary",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="CHANGELOG.md",
        tokens=("Active Legacy Parent Wording Boundary", "runtime evidence"),
        issues=issues,
    )
    return issues


def validate_eval_report_index_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=EVAL_REPORT_INDEX_DECISION_NAME,
        tokens=(
            EVAL_REPORT_INDEX_NAME,
            "derived reader",
            "not_a_receipt",
            "no report verdict is promoted into generated authority",
            "scripts/generate_eval_report_index.py",
        ),
        issues=issues,
    )
    for path_name in (
        "docs/README.md",
        "CHANGELOG.md",
        "generated/AGENTS.md",
        "mechanics/proof-loop/README.md",
        "mechanics/proof-infra/README.md",
        "reports/README.md",
    ):
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(EVAL_REPORT_INDEX_NAME,),
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=("Generated report readers", "generated/README.md"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(EVAL_REPORT_INDEX_DECISION_NAME,),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="scripts/release_check.py",
        tokens=("scripts/generate_eval_report_index.py", "--check"),
        issues=issues,
    )
    return issues


def validate_phase_alpha_eval_matrix(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_NAME
    generated_location = relative_location(generated_path, repo_root)
    schema_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME
    schema_location = relative_location(schema_path, repo_root)

    schema = load_json_payload(schema_path, issues)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    if not AOA_PLAYBOOKS_ROOT.exists():
        return issues

    try:
        builder = load_phase_alpha_eval_matrix_builder(repo_root)
        expected = builder.build_phase_alpha_eval_matrix_payload()
    except Exception as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated phase alpha eval matrix must be an object"))
        return issues

    validate_against_schema(
        payload,
        PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME,
        generated_location,
        issues,
    )

    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated phase alpha eval matrix is out of date or mismatched",
            )
        )

    if payload.get("runtime_lanes") != {"primary": "llama.cpp", "control": "llama.cpp-second-pass"}:
        issues.append(
            ValidationIssue(
                generated_location,
                "runtime_lanes must stay {'primary': 'llama.cpp', 'control': 'llama.cpp-second-pass'}",
            )
        )

    playbook_matrix_path = AOA_PLAYBOOKS_ROOT / "generated" / "phase_alpha_run_matrix.min.json"
    playbook_matrix_location = display_location(playbook_matrix_path)
    playbook_matrix = load_json_payload(playbook_matrix_path, issues)
    playbook_runs = load_mapping_entries(
        playbook_matrix,
        array_key="runs",
        key_name="run_id",
        location=playbook_matrix_location,
        issues=issues,
    )

    runs = payload.get("runs")
    if not isinstance(runs, list):
        issues.append(ValidationIssue(generated_location, "runs must be a list"))
        return issues

    seen_run_ids: list[str] = []
    for index, item in enumerate(runs):
        location = f"{generated_location}.runs[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(location, "run entry must be an object"))
            continue
        run_id = item.get("run_id")
        if not isinstance(run_id, str):
            issues.append(ValidationIssue(location, "run_id must be a string"))
            continue
        seen_run_ids.append(run_id)
        source_run = playbook_runs.get(run_id)
        if source_run is None:
            issues.append(ValidationIssue(location, f"run_id '{run_id}' does not resolve in aoa-playbooks"))
            continue

        for field_name in ("sequence", "playbook_id", "playbook_name"):
            if item.get(field_name) != source_run.get(field_name):
                issues.append(ValidationIssue(location, f"{field_name} must match aoa-playbooks phase alpha run matrix"))

        if item.get("runtime_lane") != source_run.get("runtime_path_key"):
            issues.append(ValidationIssue(location, "runtime_lane must match aoa-playbooks runtime_path_key"))

        required_evals = item.get("required_evals")
        if not isinstance(required_evals, list) or not required_evals:
            issues.append(ValidationIssue(location, "required_evals must be a non-empty list"))
            continue

        observed_anchors: list[str] = []
        for eval_index, eval_item in enumerate(required_evals):
            eval_location = f"{location}.required_evals[{eval_index}]"
            if not isinstance(eval_item, dict):
                issues.append(ValidationIssue(eval_location, "required eval entry must be an object"))
                continue
            eval_anchor = eval_item.get("eval_anchor")
            if not isinstance(eval_anchor, str):
                issues.append(ValidationIssue(eval_location, "eval_anchor must be a string"))
                continue
            observed_anchors.append(eval_anchor)
            evidence_refs = eval_item.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                issues.append(ValidationIssue(eval_location, "evidence_refs must be a non-empty list"))
                continue
            if len(evidence_refs) != len(set(evidence_refs)):
                issues.append(ValidationIssue(eval_location, "evidence_refs must not duplicate refs"))
            for ref_index, ref in enumerate(evidence_refs):
                ref_location = f"{eval_location}.evidence_refs[{ref_index}]"
                if not isinstance(ref, str) or not ref:
                    issues.append(ValidationIssue(ref_location, "evidence ref must be a non-empty string"))
                    continue
                if ref.startswith("repo:"):
                    parse_repo_ref(ref, location=ref_location, issues=issues)
                else:
                    validate_repo_relative_contract_path(
                        repo_root,
                        ref,
                        location=ref_location,
                        issues=issues,
                    )

        if observed_anchors != source_run.get("eval_anchors"):
            issues.append(ValidationIssue(location, "required_evals must stay ordered to aoa-playbooks eval_anchors"))

    if seen_run_ids != [item.get("run_id") for item in runs if isinstance(item, dict)]:
        issues.append(ValidationIssue(generated_location, "runs must keep deterministic ordering"))
    if set(seen_run_ids) != set(playbook_runs):
        missing = sorted(set(playbook_runs) - set(seen_run_ids))
        extra = sorted(set(seen_run_ids) - set(playbook_runs))
        if missing:
            issues.append(ValidationIssue(generated_location, "missing phase alpha runs: " + ", ".join(missing)))
        if extra:
            issues.append(ValidationIssue(generated_location, "unexpected phase alpha runs: " + ", ".join(extra)))

    return issues


def validate_titan_canary_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canary_dir = repo_root / TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME
    canary_paths = sorted(canary_dir.glob("titan*.yaml"))
    if not canary_paths:
        issues.append(
            ValidationIssue(
                TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME,
                "Titan seed YAML files must be present under mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
            )
        )
        return issues

    for canary_path in canary_paths:
        location = relative_location(canary_path, repo_root)
        payload = load_yaml_file(canary_path, issues)
        if not isinstance(payload, dict):
            if payload is not None:
                issues.append(ValidationIssue(location, "Titan canary must be a YAML mapping"))
            continue
        canary_id = payload.get("id") or payload.get("eval_id")
        if canary_id != canary_path.stem:
            issues.append(ValidationIssue(location, "Titan canary id must match the filename stem"))
        if "version" in payload and not isinstance(payload.get("version"), int):
            issues.append(ValidationIssue(location, "Titan canary version must be an integer"))
        if not any(
            isinstance(payload.get(field), str) and payload[field].strip()
            for field in ("purpose", "claim", "kind", "description", "objective")
        ):
            issues.append(ValidationIssue(location, "Titan canary must expose purpose, claim, kind, description, or objective"))
        checks = payload.get("checks")
        if checks is not None:
            if not isinstance(checks, list) or not checks:
                issues.append(ValidationIssue(location, "Titan canary checks must be a non-empty list when present"))
                continue
            for index, check in enumerate(checks):
                check_location = f"{location}.checks[{index}]"
                if not isinstance(check, dict):
                    issues.append(ValidationIssue(check_location, "Titan canary check must be an object"))
                    continue
                if not isinstance(check.get("name"), str) or not check["name"].strip():
                    issues.append(
                        ValidationIssue(
                            check_location,
                            "Titan canary check name must be a non-empty string",
                        )
                    )
                if not any(
                    isinstance(check.get(field), str) and check[field].strip()
                    for field in ("assert", "command", "expect", "rule")
                ):
                    issues.append(
                        ValidationIssue(
                            check_location,
                            "Titan canary check must expose assert, command, expect, or rule",
                        )
                    )
        failure_examples = payload.get("failure_examples")
        if failure_examples is None:
            if not any(
                key in payload
                for key in (
                    "expected_failure",
                    "expected_result",
                    "expected",
                    "forbidden",
                    "description",
                    "checks",
                    "required_fields",
                )
            ):
                issues.append(
                    ValidationIssue(
                        location,
                        "Titan canary must expose failure_examples, expected_failure, expected_result, expected, forbidden, checks, or required_fields",
                    )
                )
        elif not isinstance(failure_examples, list) or not failure_examples:
            issues.append(
                ValidationIssue(
                    location,
                    "Titan canary failure_examples must be a non-empty list when present",
                )
            )
        elif not all(isinstance(item, str) and item.strip() for item in failure_examples):
            issues.append(
                ValidationIssue(
                    location,
                    "Titan canary failure_examples must be non-empty strings",
                )
            )

    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def validate_root_topology_domain(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_agent_index_surface(repo_root))
    issues.extend(validate_root_readme_surface_role(repo_root))
    issues.extend(validate_memory_consumer_proof_boundary_surfaces(repo_root))
    issues.extend(validate_eval_philosophy_route_map_surface(repo_root))
    issues.extend(validate_docs_readme_route_map(repo_root))
    issues.extend(validate_read_model_command_ownership(repo_root))
    issues.extend(validate_releasing_route_map_surface(repo_root))
    issues.extend(validate_source_eval_tree_topology_surfaces(repo_root))
    issues.extend(validate_audit_surface_role(repo_root))
    issues.extend(validate_github_agent_surface(repo_root))
    issues.extend(validate_index_surface_roles(repo_root))
    issues.extend(validate_validator_surface_role(repo_root))
    issues.extend(validate_mechanic_index_surface_roles(repo_root))
    issues.extend(validate_root_design_surfaces(repo_root))
    issues.extend(validate_root_route_card_districts(repo_root))
    issues.extend(validate_root_authored_route_residue_surfaces(repo_root))
    issues.extend(validate_decision_route_residue_surfaces(repo_root))
    issues.extend(validate_repo_config_route_residue_surfaces(repo_root))
    issues.extend(validate_source_bundle_route_residue_surfaces(repo_root))
    issues.extend(validate_agent_lane_surfaces(repo_root))
    issues.extend(validate_quest_route_surfaces(repo_root))
    issues.extend(validate_proof_topology_surfaces(repo_root))
    issues.extend(validate_legacy_naming_surfaces(repo_root))
    issues.extend(validate_mechanics_surfaces(repo_root))
    issues.extend(validate_active_legacy_parent_wording(repo_root))
    issues.extend(validate_generated_route_residue_surfaces(repo_root))
    issues.extend(validate_eval_report_index_route_surfaces(repo_root))
    return issues


def validate_source_eval_entry_domain(
    repo_root: Path,
    *,
    starter_names: Sequence[str],
    selected_evals: set[str] | None,
    selected_starter_evals: set[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        validate_eval_index(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_eval_selection(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_starter_bundle_contract(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_roadmap_parity(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )
    return issues


def validate_source_eval_doctrine_domain(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
    *,
    selected_evals: set[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        validate_comparison_doctrine_surfaces(
            repo_root,
            records,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_artifact_process_doctrine_surfaces(
            repo_root,
            records,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_repeated_window_doctrine_surfaces(
            repo_root,
            records,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_integrity_taxonomy_surfaces(
            repo_root,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_shared_proof_infra_surfaces(
            repo_root,
            selected_evals=selected_evals,
        )
    )
    return issues


def validate_repo_wide_evidence_readout_domain(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_trace_eval_bridge_surfaces(repo_root, records))
    issues.extend(validate_runtime_integrity_review_surface(repo_root))
    issues.extend(validate_eval_result_receipt_surfaces(repo_root))
    issues.extend(validate_receipt_intake_dry_review_surface(repo_root))
    issues.extend(validate_release_support_readiness_audit_surface(repo_root))
    issues.extend(validate_strategic_closeout_audit_surface(repo_root))
    issues.extend(validate_release_prep_pr_handoff_surface(repo_root))
    issues.extend(validate_live_receipt_log(repo_root))
    issues.extend(
        validate_runtime_evidence_selection_surfaces(
            repo_root,
            records,
        )
    )
    issues.extend(validate_runtime_candidate_template_index(repo_root))
    issues.extend(validate_runtime_candidate_intake(repo_root))
    issues.extend(validate_eval_report_index(repo_root))
    issues.extend(validate_phase_alpha_eval_matrix(repo_root))
    issues.extend(validate_titan_canary_surfaces(repo_root))
    issues.extend(validate_generated_catalogs(repo_root, records))
    issues.extend(validate_generated_capsules(repo_root, records))
    issues.extend(validate_generated_sections(repo_root, records))
    issues.extend(validate_generated_comparison_spine(repo_root, records))
    return issues


def validate_target_eval_readout_domain(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
    *,
    target_evals: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        validate_runtime_evidence_selection_surfaces(
            repo_root,
            records,
            target_eval_names=set(target_evals),
        )
    )
    issues.extend(
        validate_generated_catalogs(
            repo_root,
            records,
            target_eval_names=target_evals,
        )
    )
    issues.extend(
        validate_generated_capsules(
            repo_root,
            records,
            target_eval_names=target_evals,
        )
    )
    issues.extend(
        validate_generated_sections(
            repo_root,
            records,
            target_eval_names=target_evals,
        )
    )
    issues.extend(
        validate_generated_comparison_spine(
            repo_root,
            records,
            target_eval_names=target_evals,
        )
    )
    return issues


def run_validation(
    repo_root: Path,
    eval_name: str | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if repo_root.resolve() == REPO_ROOT.resolve() and eval_name is None:
        issues.extend(validate_root_topology_domain(repo_root))
    source_evals_dir_exists = (repo_root / SOURCE_EVALS_DIR_NAME).is_dir()
    try:
        all_eval_names = discover_eval_names(repo_root)
    except FileNotFoundError:
        issues.append(ValidationIssue(SOURCE_EVALS_DIR_NAME, "directory is missing"))
        all_eval_names = []
    starter_names = load_starter_eval_names(repo_root, issues)
    starter_set = set(starter_names)

    if eval_name is not None:
        if eval_name not in all_eval_names:
            raise ValueError(f"unknown eval '{eval_name}'")
        target_evals = [eval_name]
        selected_evals = {eval_name}
        selected_starter_evals = selected_evals.intersection(starter_set)
    else:
        target_evals = all_eval_names
        selected_evals = None
        selected_starter_evals = None

    if all_eval_names:
        source_issues, records = collect_catalog_records(repo_root, target_evals)
    else:
        source_issues, records = [], []
    issues.extend(source_issues)

    if source_evals_dir_exists:
        issues.extend(
            validate_source_eval_entry_domain(
                repo_root,
                starter_names=starter_names,
                selected_evals=selected_evals,
                selected_starter_evals=selected_starter_evals,
            )
        )
    if source_evals_dir_exists and not source_issues:
        issues.extend(
            validate_source_eval_doctrine_domain(
                repo_root,
                records,
                selected_evals=selected_evals,
            )
        )

    if source_evals_dir_exists and eval_name is None and not source_issues:
        all_source_issues, all_records = collect_catalog_records(repo_root)
        if not all_source_issues:
            issues.extend(
                validate_repo_wide_evidence_readout_domain(
                    repo_root,
                    all_records,
                )
            )
    elif source_evals_dir_exists and eval_name is not None and not source_issues:
        issues.extend(
            validate_target_eval_readout_domain(
                repo_root,
                records,
                target_evals=target_evals,
            )
        )

    issues.extend(validate_questbook_surface(repo_root))

    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, eval_name=args.eval)
        if args.eval is None:
            issues.extend(
                ValidationIssue(location, message)
                for location, message in validate_nested_agents.run_validation(repo_root)
            )
    except ValueError as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    if issues:
        scope = args.eval if args.eval else "repository"
        print(f"Validation failed for {scope}.")
        print(format_issues(issues))
        return 1

    if args.eval:
        print(f"Validation passed for eval '{args.eval}'.")
    else:
        eval_count = len(discover_eval_names(repo_root))
        print(f"Validation passed for {eval_count} eval bundles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
