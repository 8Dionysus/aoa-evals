"""Shared route-residue validator constants and context."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Callable, Iterable

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue
from validators.root_route_cards import ROOT_ROUTE_CARD_ONLY_DISTRICTS


SOURCE_EVALS_DIR_NAME = "evals"
MECHANICS_README_NAME = "mechanics/README.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"

ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS = (
    "Route residue guard family",
    "generated/readout, active mechanic, root-authored, decision, repo-config, source-bundle, and mechanic-payload residue guards",
    "owner contracts",
)


@dataclass(frozen=True)
class RouteResidueContext:
    require_tokens: Callable[[Path, str, Iterable[str], list[ValidationIssue]], str]


ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>(?:"
    + "|".join(re.escape(district) for district in ROOT_ROUTE_CARD_ONLY_DISTRICTS)
    + r")(?:/[A-Za-z0-9._*<>-]+)+/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE = re.compile(
    r"(?<![\w./:-])(?P<token>mechanics/(?:"
    + "|".join(
        re.escape(wrong_parent)
        for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
    )
    + r")(?:/[A-Za-z0-9._*<>-]+)*/?)"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_TOKEN_STRIP_CHARS = "`.,;:)]}\"'"


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
